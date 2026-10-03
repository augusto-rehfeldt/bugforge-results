import math
import random
import statistics
import time


def reference(x):
    t = math.exp(-abs(x))
    return (2.0 * t) / (math.pi * (1.0 + t * t))


def evaluate(pdf, x):
    try:
        return ("result", pdf(x))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def valid(outcome):
    if outcome[0] != "result":
        return False
    try:
        return math.isfinite(outcome[1]) and outcome[1] >= 0.0
    except (TypeError, ValueError, OverflowError):
        return False


def main():
    start = time.monotonic()
    pdf = statistics.kde(
        [0.0], 1.0, kernel="sigmoid", cumulative=False
    )

    sanity_ok = True
    for x in (0.0, 1.0):
        actual = evaluate(pdf, x)
        expected = reference(x)
        agrees = (
            valid(actual)
            and math.isclose(actual[1], expected, rel_tol=1e-12, abs_tol=0.0)
        )
        print("SANITY:", repr(x), "actual =", repr(actual),
              "expected =", repr(expected), "agrees =", agrees)
        sanity_ok = sanity_ok and agrees
    if not sanity_ok:
        print("SANITY FAILED")
        return

    edges = [
        720.0,
        1000.0,
        math.nextafter(720.0, math.inf),
        math.nextafter(1000.0, -math.inf),
        721.0,
        730.0,
        740.0,
        745.0,
        746.0,
        750.0,
        800.0,
        900.0,
    ]
    rng = random.Random(20260719)
    tested = 0

    def check(x):
        nonlocal tested
        tested += 1
        actual = evaluate(pdf, x)
        if valid(actual):
            return False
        repeated = evaluate(pdf, x)
        if valid(repeated):
            return False
        case = {
            "data": [0.0],
            "h": 1.0,
            "kernel": "sigmoid",
            "cumulative": False,
            "x": x,
        }
        print("COUNTEREXAMPLE:", repr(case),
              "actual =", repr(repeated),
              "expected =", repr(reference(x)))
        return True

    for x in edges:
        if check(x):
            return

    while time.monotonic() - start < 175.0:
        x = rng.uniform(720.0, 1000.0)
        if check(x):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()