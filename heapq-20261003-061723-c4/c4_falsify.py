import heapq
import random
import time


class Item:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


def reference(n, xs):
    # Stable insertion sort, comparing integer priorities directly.
    ordered = []
    for item in xs:
        i = len(ordered)
        while i > 0 and item.priority < ordered[i - 1].priority:
            i -= 1
        ordered.insert(i, item)
    return ordered[:n]


def same_identities(left, right):
    return len(left) == len(right) and all(
        a is b for a, b in zip(left, right)
    )


def names(items):
    return [item.name for item in items]


def make_items(priorities):
    return [Item("x" + str(i), p) for i, p in enumerate(priorities)]


def main():
    deadline = time.monotonic() + 175
    tested = 0

    for number, priorities, n in [
        (1, [8, 2, 5, -1, 3], 3),
        (2, [0, 1, 2, 3, 4], 2),
    ]:
        xs = make_items(priorities)
        expected = reference(n, xs)
        actual = heapq.nsmallest(n, xs)
        ok = same_identities(actual, expected)
        print("Sanity {}: actual={!r}, expected={!r}, agree={}".format(
            number, names(actual), names(expected), ok
        ))
        if not ok:
            print("SANITY FAILED")
            return

    def check(priorities, n, labels=None):
        nonlocal tested
        xs = (
            make_items(priorities)
            if labels is None
            else [Item(label, p) for label, p in zip(labels, priorities)]
        )
        expected = reference(n, xs)
        actual = heapq.nsmallest(n, xs)
        tested += 1
        if same_identities(actual, expected):
            return False

        repeated = heapq.nsmallest(n, xs)
        if not same_identities(actual, repeated):
            return False

        literal = {
            "n": n,
            "xs": [(item.name, item.priority) for item in xs],
        }
        print("COUNTEREXAMPLE:")
        print(repr(literal))
        print("actual:", repr(names(repeated)))
        print("expected:", repr(names(expected)))
        return True

    hand_picked = [
        ([1, 1, 1, 1, 0], 4, ["a", "b", "c", "d", "e"]),
        ([0, 0], 1, None),
        ([1, 1, 1, 1, 1], 4, None),
        ([2, 2, 1, 2, 0, 2], 4, None),
        ([-1, -1, -1, -2, -1, -2], 3, None),
        ([3, 2, 1, 0], 3, None),
    ]
    for priorities, n, labels in hand_picked:
        if check(priorities, n, labels):
            return

    rng = random.Random(728193)
    while time.monotonic() < deadline:
        size = rng.randint(2, 100)
        n = rng.randint(1, size - 1)
        priorities = [rng.randint(-3, 3) for _ in range(size)]
        if check(priorities, n):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()