import heapq
import random
import time


def reference(values):
    # A single sorted stream must be reproduced unchanged.
    result = []
    for value in values:
        result.append(value)
    return result


def wrapped_iterator(values):
    backing_iterator = iter(values)

    class StaticNextIterator:
        def __iter__(self):
            return self

        __next__ = staticmethod(lambda: next(backing_iterator))

    return StaticNextIterator()


def actual_result(values):
    try:
        return list(heapq.merge(wrapped_iterator(values)))
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}


def main():
    deadline = time.monotonic() + 175.0

    sanity_failed = False
    for index, values in enumerate(([], [-5, -1, -1, 0, 8]), 1):
        expected = reference(values)
        try:
            actual = list(heapq.merge(iter(values)))
        except Exception as exc:
            actual = {"exception": type(exc).__name__, "message": str(exc)}
        print("SANITY", index, "actual:", repr(actual), "expected:", repr(expected))
        if actual != expected:
            sanity_failed = True

    if sanity_failed:
        print("SANITY FAILED")
        return

    tested = 0

    def check(values):
        nonlocal tested
        tested += 1
        expected = reference(values)
        actual = actual_result(values)
        if actual != expected:
            repeated = actual_result(values)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr(values))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    edge_cases = [
        [],
        [0],
        [-1],
        [0, 0],
        [-3, -3, 0, 2, 2],
        list(range(-100, 101)),
        [-(10**100), 0, 10**100],
    ]

    for values in edge_cases:
        if time.monotonic() >= deadline:
            break
        if check(values):
            return

    rng = random.Random(1729)
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        length = rng.choice([0, 1, 2, 3, 10, 100, 1000])
        values = sorted(rng.randint(-10000, 10000) for _ in range(length))
        if check(values):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()