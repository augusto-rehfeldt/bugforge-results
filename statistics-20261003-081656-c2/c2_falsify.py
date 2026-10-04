import math
import random
import statistics
import time
from fractions import Fraction


def reference(data):
    # Compute the documented population variance using exact arithmetic.
    values = [Fraction.from_float(x) for x in data]
    mean = sum(values, Fraction(0)) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    numerator = math.isqrt(variance.numerator)
    denominator = math.isqrt(variance.denominator)
    assert numerator * numerator == variance.numerator
    assert denominator * denominator == variance.denominator
    return float(Fraction(numerator, denominator))


def call(data, supplied_mean):
    try:
        result = (
            statistics.pstdev(data, mu=0.0)
            if supplied_mean
            else statistics.pstdev(data)
        )
        return ("result", result)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def evaluate(data, expected):
    omitted = call(data, False)
    supplied = call(data, True)
    actual = {"mu omitted": omitted, "mu=0.0": supplied}
    failed = any(
        outcome[0] != "result"
        or not math.isclose(outcome[1], expected, rel_tol=1e-15, abs_tol=0.0)
        for outcome in (omitted, supplied)
    )
    if not failed:
        failed = not math.isclose(
            omitted[1], supplied[1], rel_tol=1e-15, abs_tol=0.0
        )
    return failed, actual


def main():
    deadline = time.monotonic() + 175.0

    sanity_failed = False
    for data in ([-3.0, 3.0], [-0.5, 0.5]):
        expected = reference(data)
        failed, actual = evaluate(data, expected)
        print("SANITY:", repr(data), "actual=", repr(actual),
              "expected=", repr(expected))
        sanity_failed |= failed
    if sanity_failed:
        print("SANITY FAILED")
        return

    edges = [
        1e160,
        math.nextafter(1e160, math.inf),
        1e170,
        1e180,
        1e200,
        1e250,
        math.nextafter(1e300, 0.0),
        1e300,
    ]
    rng = random.Random(20260719)
    tested = 0

    def inputs():
        yield from edges
        while True:
            a = 10.0 ** rng.uniform(160.0, 300.0)
            if math.isfinite(a) and 1e160 <= a <= 1e300:
                yield a

    for a in inputs():
        if time.monotonic() >= deadline:
            break
        data = [-a, a]
        expected = reference(data)
        tested += 1
        failed, actual = evaluate(data, expected)
        if failed:
            repeated_failure, repeated_actual = evaluate(data, expected)
            if repeated_failure and repeated_actual == actual:
                print(
                    "COUNTEREXAMPLE:",
                    repr({"data": data, "mu": 0.0}),
                    "actual=", repr(repeated_actual),
                    "expected=", repr(expected),
                )
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()