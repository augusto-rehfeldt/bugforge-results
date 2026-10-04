import math
import multiprocessing
import random
import signal
import time
from fractions import Fraction

SAMPLES = 128
DEADLINE = time.monotonic() + 175.0
HAS_ALARM = all(
    hasattr(signal, name)
    for name in ("SIGALRM", "setitimer", "ITIMER_REAL")
)


class TimedOut(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimedOut()


if HAS_ALARM:
    signal.signal(signal.SIGALRM, alarm_handler)


def reference_mean(alpha, beta):
    # Exact arithmetic avoids overflow in alpha + beta.
    a = Fraction.from_float(alpha)
    b = Fraction.from_float(beta)
    return float(a / (a + b))


def sample(alpha, beta, seed, count):
    rng = random.Random(seed)
    try:
        values = [rng.betavariate(alpha, beta) for _ in range(count)]
        return {
            "mean": math.fsum(values) / count,
            "all_zero": all(x == 0.0 for x in values),
            "valid_outputs": all(math.isfinite(x) and 0.0 <= x <= 1.0
                                 for x in values),
        }
    except TimedOut:
        raise
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}


def sample_worker(connection, alpha, beta, seed, count):
    try:
        connection.send("ready")
        connection.recv()
        connection.send(sample(alpha, beta, seed, count))
    finally:
        connection.close()


def measure(alpha, beta, seed, count, timeout=1.0):
    if not HAS_ALARM:
        context = multiprocessing.get_context("spawn")
        parent, child = context.Pipe()
        process = context.Process(
            target=sample_worker,
            args=(child, alpha, beta, seed, count),
        )
        process.start()
        child.close()
        try:
            # Do not charge interpreter startup against sampling time.
            parent.recv()
            parent.send("start")
            if parent.poll(timeout):
                return parent.recv()
            return {"timeout_seconds": timeout}
        except Exception as exc:
            return {"exception": type(exc).__name__, "message": str(exc)}
        finally:
            if process.is_alive():
                process.terminate()
            process.join()
            parent.close()

    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        return sample(alpha, beta, seed, count)
    except TimedOut:
        return {"timeout_seconds": timeout}
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)


def fails(actual, expected, tolerance):
    return (
        "mean" not in actual
        or not actual["valid_outputs"]
        or actual["all_zero"]
        or abs(actual["mean"] - expected) > tolerance
    )


tested = 0


def check(alpha, seed):
    global tested
    beta = alpha
    assert math.isfinite(alpha) and alpha > 0.0
    expected = reference_mean(alpha, beta)
    actual = measure(alpha, beta, seed, SAMPLES)
    tested += 1
    if fails(actual, expected, 0.01):
        repeated = measure(alpha, beta, seed, SAMPLES)
        if fails(repeated, expected, 0.01):
            case = {
                "alpha": alpha,
                "beta": beta,
                "seed": seed,
                "samples": SAMPLES,
            }
            print("COUNTEREXAMPLE:", repr(case),
                  "actual:", repr({"first": actual, "rerun": repeated}),
                  "expected:", repr({"mean": expected}))
            raise SystemExit(0)


def main():
    # Statistical sanity checks, with deterministic seeds and generous tolerances.
    for alpha, beta, seed in [(1.0, 1.0, 12345), (2.0, 2.0, 67890)]:
        expected = reference_mean(alpha, beta)
        actual = measure(alpha, beta, seed, 20000, timeout=2.0)
        print("SANITY:", repr((alpha, beta, seed)), repr(actual),
              "expected_mean:", repr(expected))
        if fails(actual, expected, 0.02):
            print("SANITY FAILED")
            raise SystemExit(0)

    edges = [
        9e307,
        8.99e307,
        math.nextafter(8.99e307, math.inf),
        math.nextafter(9e307, 0.0),
        math.nextafter(9e307, math.inf),
        math.nextafter(1e308, 0.0),
        1e308,
    ]

    for alpha in edges:
        for seed in [0, 1, 2, 42, 8675309, -1, 2**64 - 1]:
            if time.monotonic() >= DEADLINE:
                print("NO COUNTEREXAMPLE", tested)
                raise SystemExit(0)
            check(alpha, seed)

    inputs = random.Random(20250308)
    while time.monotonic() < DEADLINE:
        alpha = 8.99e307 + (1e308 - 8.99e307) * inputs.random()
        check(alpha, inputs.getrandbits(64))

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()