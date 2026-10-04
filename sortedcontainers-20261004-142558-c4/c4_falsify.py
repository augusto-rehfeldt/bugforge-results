import random
import time
from sortedcontainers import SortedDict


def reference(d):
    return sorted(dict.keys(d), key=lambda x: x)


def run_case(initial, absent, value):
    blocked = None

    def key(x):
        if x == blocked:
            raise ValueError("deliberate key-function failure")
        return x

    d = SortedDict(key, {x: x for x in initial})
    blocked = absent
    raised = False
    try:
        d.setdefault(absent, value)
    except ValueError:
        raised = True
    finally:
        blocked = None

    actual = list(d.keys())
    expected = reference(d)
    return raised, actual, expected


def main():
    for initial, inserted in [([3, -1, 2], 0), ([0, -10, 10], 20)]:
        d = SortedDict(lambda x: x, {x: x for x in initial})
        d.setdefault(inserted, "ordinary")
        actual, expected = list(d.keys()), reference(d)
        print("SANITY:", actual, expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(initial, absent, value):
        nonlocal tested
        tested += 1
        first = run_case(initial, absent, value)
        if first[0] and first[1] != first[2]:
            second = run_case(initial, absent, value)
            if second == first:
                case = {
                    "initial_keys": initial,
                    "absent_key": absent,
                    "value": value,
                }
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("actual:", repr(second[1]))
                print("expected:", repr(second[2]))
                return True
        return False

    edges = [
        ([0], 1),
        ([0], -1),
        ([-1, 1], 0),
        ([1, 2, 3], 4),
        ([1, 2, 3], -100),
        ([-10**100, 0, 10**100], 10**101),
        (list(range(100)), 50 + 10**6),
    ]
    for initial, absent in edges:
        if check(initial, absent, "value"):
            return

    rng = random.Random(20260402)
    while time.monotonic() < deadline:
        size = rng.randint(1, 200)
        initial = rng.sample(range(-10000, 10001), size)
        occupied = set(initial)
        absent = rng.randint(-20000, 20000)
        while absent in occupied:
            absent = rng.randint(-20000, 20000)
        if check(initial, absent, rng.randint(-1000, 1000)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()