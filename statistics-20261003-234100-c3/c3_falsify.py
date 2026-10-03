import math
import random
import statistics
import time
from fractions import Fraction


def reference(data, weights):
    xs = [Fraction(x) for x in data]
    ws = [Fraction(w) for w in weights]
    return float(sum(ws) / sum(w / x for x, w in zip(xs, ws)))


def evaluate(data, weights, expected):
    try:
        actual = statistics.harmonic_mean(data, weights=weights)
        failed = not (
            math.isfinite(actual)
            and math.isclose(actual, expected, rel_tol=1e-14, abs_tol=0.0)
        )
        return failed, actual
    except Exception as exc:
        return True, (type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175.0

    sanity_failed = False
    for data, weights in [
        ([2.0, 4.0], [1.0, 1.0]),
        ([40.0, 60.0], [5.0, 30.0]),
    ]:
        expected = reference(data, weights)
        failed, actual = evaluate(data, weights, expected)
        print("SANITY:", repr(data), repr(weights),
              "actual =", repr(actual), "expected =", repr(expected))
        sanity_failed |= failed

    if sanity_failed:
        print("SANITY FAILED")
        return

    rng = random.Random(20260719)
    edges = [180, 250, 181, 249, 200, 215, 230]
    tested = 0

    for index in range(len(edges) + 10000):
        if time.monotonic() >= deadline:
            break
        k = edges[index] if index < len(edges) else rng.randint(180, 250)
        a = 10.0 ** k
        data = [a, 2 * a]
        weights = [1 / a, 1 / a]
        expected = reference(data, weights)
        failed, actual = evaluate(data, weights, expected)
        tested += 1

        if failed:
            failed_again, actual_again = evaluate(data, weights, expected)
            if failed_again:
                print("COUNTEREXAMPLE:")
                print(repr({"k": k, "data": data, "weights": weights}))
                print("actual =", repr(actual_again))
                print("expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()