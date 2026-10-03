import math
import random
import statistics
import time


def reference_overlap():
    # For N(0, s) and N(0, 2s), the densities intersect at
    # x/s = sqrt(8*log(2)/3). Integrate the wider density inside
    # these intersections and the narrower density outside them.
    t = math.sqrt(8.0 * math.log(2.0) / 3.0)
    return math.erf(t / (2.0 * math.sqrt(2.0))) + math.erfc(
        t / math.sqrt(2.0)
    )


EXPECTED = reference_overlap()
TOLERANCE = 1e-12


def evaluate(a):
    try:
        actual = statistics.NormalDist(0.0, a).overlap(
            statistics.NormalDist(0.0, 2.0 * a)
        )
        failed = not math.isfinite(actual) or abs(actual - EXPECTED) > TOLERANCE
        return failed, actual
    except Exception as exc:
        return True, ("exception", type(exc).__name__, str(exc))


def main():
    sanity_ok = True
    for a in (1.0, 3.0):
        failed, actual = evaluate(a)
        print("SANITY:", repr(a), "actual =", repr(actual),
              "expected =", repr(EXPECTED))
        sanity_ok = sanity_ok and not failed
    if not sanity_ok:
        print("SANITY FAILED")
        return

    deadline = time.monotonic() + 175.0
    rng = random.Random(8675309)
    count = 0

    edges = [
        1e150,
        math.nextafter(1e150, 0.0),
        1e100,
        math.nextafter(1e100, math.inf),
    ]
    edges.extend(10.0 ** k for k in range(100, 151))

    def inputs():
        yield from edges
        while time.monotonic() < deadline:
            if rng.randrange(2):
                a = 10.0 ** rng.uniform(100.0, 150.0)
            else:
                k = rng.randrange(100, 150)
                a = (1.0 + 9.0 * rng.random()) * (10.0 ** k)
            if math.isfinite(a) and 1e100 <= a <= 1e150:
                yield a

    for a in inputs():
        if time.monotonic() >= deadline:
            break
        count += 1
        failed, actual = evaluate(a)
        if failed:
            failed_again, actual_again = evaluate(a)
            if failed_again:
                literal = ((0.0, a), (0.0, 2.0 * a))
                print("COUNTEREXAMPLE:", repr(literal),
                      "actual =", repr(actual_again),
                      "expected =", repr(EXPECTED))
                return

    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()