import random
import time
import more_itertools


def reference(items):
    for i in range(len(items)):
        for j in range(i):
            if bool(items[i] == items[j]):
                return False
    return True


def actual(items):
    try:
        return more_itertools.all_unique(items, key=None)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175.0
    for items in ([1, 2, 3], [1, 2, 1]):
        expected = reference(items)
        result = actual(items)
        print("SANITY:", repr(items), "actual:", repr(result),
              "expected:", repr(expected))
        if result != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check_set(s):
        nonlocal tested
        for items in ([set(s), frozenset(s)], [frozenset(s), set(s)]):
            expected = reference(items)
            result = actual(items)
            tested += 1
            if result != expected:
                repeated = actual(items)
                if repeated != expected:
                    print("COUNTEREXAMPLE:", repr(items),
                          "actual:", repr(repeated), "expected:", repr(expected))
                    return True
        return False

    edge_cases = [
        set(),
        {0},
        {1},
        {-1},
        {0, 1},
        {-1, 0, 1},
        set(range(10)),
        {-10**100, 0, 10**100},
        set(range(-100, 101)),
    ]
    for s in edge_cases:
        if check_set(s):
            return

    rng = random.Random(20260217)
    while time.monotonic() < deadline:
        size = rng.randrange(0, 129)
        s = {rng.randrange(-10000, 10001) for _ in range(size)}
        if check_set(s):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()