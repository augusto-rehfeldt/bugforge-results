import random
import time
from collections.abc import Set
from sortedcontainers import SortedDict


def reference(items, rhs):
    expected = set()
    for key in items:
        if key in rhs:
            expected.add(key)
    return expected


def evaluate(items, ranks, rhs):
    expected = reference(items, rhs)
    try:
        d = SortedDict(ranks.__getitem__, items)
        actual = d.keys() & rhs
        good = isinstance(actual, Set) and set(actual) == expected
        description = repr(actual)
        signature = ("result", type(actual).__name__, frozenset(actual))
    except Exception as exc:
        good = False
        description = "{}: {}".format(type(exc).__name__, repr(str(exc)))
        signature = ("exception", type(exc).__name__, str(exc))
    return good, description, expected, signature


def main():
    for number, rhs in enumerate(({1, 3}, set()), 1):
        items = {1: "a", 2: "b", 3: "c"}
        ranks = {1: 2, 2: 0, 3: 1}
        good, actual, expected, _ = evaluate(items, ranks, rhs)
        print("SANITY {}: actual={}, expected={}".format(
            number, actual, repr(expected)
        ))
        if not good:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 170
    tested = 0

    def check(items, ranks, rhs):
        nonlocal tested
        tested += 1
        good, actual, expected, signature = evaluate(items, ranks, rhs)
        if not good:
            again, actual_again, expected_again, signature_again = evaluate(
                items, ranks, rhs
            )
            if not again and signature_again == signature:
                print("COUNTEREXAMPLE:")
                print(repr({
                    "items": items,
                    "integer_ranks": ranks,
                    "intersection_set": rhs,
                }))
                print("actual:", actual_again)
                print("expected:", repr(expected_again))
                return True
        return False

    keys = [1j, 1 + 2j]
    items = dict(zip(keys, ("a", "b")))
    ranks = {keys[0]: 0, keys[1]: 1}
    for rhs in (set(), {keys[0]}, {keys[1]}, set(keys)):
        if check(items, ranks, rhs):
            return

    rng = random.Random(20260217)
    while time.monotonic() < deadline:
        count = rng.randint(2, 30)
        keys = []
        seen = set()
        while len(keys) < count:
            key = complex(rng.randint(-100, 100), rng.randint(-100, 100))
            if key not in seen:
                seen.add(key)
                keys.append(key)
        items = {key: index for index, key in enumerate(keys)}
        order = list(range(count))
        rng.shuffle(order)
        ranks = dict(zip(keys, order))

        subsets = (
            set(),
            {rng.choice(keys)},
            set(keys),
            {key for key in keys if rng.randrange(2)},
        )
        for rhs in subsets:
            if time.monotonic() >= deadline:
                break
            if check(items, ranks, rhs):
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()