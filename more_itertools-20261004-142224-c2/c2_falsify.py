import math
import random
import sys
import time
from fractions import Fraction

from more_itertools import running_median


def reference(values):
    ordered = []
    results = []
    for value in values:
        ordered.append(Fraction.from_float(value))
        ordered.sort()
        size = len(ordered)
        middle = size // 2
        if size % 2:
            median = ordered[middle]
        else:
            median = (ordered[middle - 1] + ordered[middle]) / 2
        results.append(float(median))
    return results


def evaluate(values):
    try:
        return list(running_median(values))
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175.0

    for values in ([1.0, 1.0], [1.0, 3.0, 2.0, 4.0]):
        expected = reference(values)
        actual = evaluate(values)
        print("SANITY:", repr(values), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(values):
        nonlocal tested
        expected = reference(values)
        actual = evaluate(values)
        tested += 1
        if actual != expected:
            repeated = evaluate(values)
            if repeated != expected and repeated == actual:
                print("COUNTEREXAMPLE:", repr(values),
                      "actual:", repr(repeated), "expected:", repr(expected))
                return True
        return False

    largest = sys.float_info.max
    edge_values = [
        1e308,
        largest,
        math.nextafter(largest / 2.0, math.inf),
        largest / 2.0,
        math.nextafter(largest / 2.0, 0.0),
        1.0,
        sys.float_info.min,
        math.nextafter(0.0, 1.0),
    ]

    for value in edge_values:
        for length in range(2, 11):
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check([value] * length):
                return

    rng = random.Random(731921)
    while time.monotonic() < deadline:
        if rng.randrange(2):
            value = largest * rng.uniform(0.5000000000000001, 1.0)
        else:
            value = math.ldexp(rng.uniform(0.5, 1.0),
                               rng.randint(-1073, 1024))
        if not math.isfinite(value) or value <= 0.0:
            continue
        if check([value] * rng.randint(2, 10)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()