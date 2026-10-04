import random
import time
from sortedcontainers import SortedSet


class Value:
    __slots__ = ("number",)
    failing = set()

    def __init__(self, number):
        object.__setattr__(self, "number", number)

    def __setattr__(self, name, value):
        raise AttributeError("immutable")

    def __hash__(self):
        if self.number in Value.failing:
            raise ValueError("temporary hash failure")
        return hash(self.number)

    def __eq__(self, other):
        if not isinstance(other, Value):
            return NotImplemented
        return self.number == other.number

    def __lt__(self, other):
        if not isinstance(other, Value):
            return NotImplemented
        return self.number < other.number

    def __repr__(self):
        return "Value(%r)" % self.number


def sanity(numbers, index):
    Value.failing.clear()
    reference = sorted(set(numbers))
    selected = reference[index]
    expected_remaining = reference[:]
    del expected_remaining[index]

    values = [Value(n) for n in numbers]
    s = SortedSet(values)
    popped = s.pop(index)
    actual = (
        popped.number,
        [v.number for v in s],
        [(n, Value(n) in s) for n in reference],
    )
    expected = (
        selected,
        expected_remaining,
        [(n, n in expected_remaining) for n in reference],
    )
    print("SANITY:", actual, expected)
    return actual == expected


def check(case):
    numbers, index = case
    Value.failing.clear()
    reference = sorted(set(numbers))
    selected = reference[index]
    originals = [Value(n) for n in reference]
    s = SortedSet(originals)

    Value.failing.add(selected)
    raised = False
    try:
        s.pop(index)
    except ValueError:
        raised = True
    finally:
        Value.failing.clear()

    # The reference is the property's documented membership/iteration
    # equivalence, not an assumption about exception rollback.
    iteration = list(s)
    comparisons = [
        (v.number, v in s, any(v == x for x in iteration))
        for v in originals
    ]
    actual = {
        "raised_ValueError": raised,
        "iteration": [v.number for v in iteration],
        "membership_equals_iteration": [
            (n, membership == present)
            for n, membership, present in comparisons
        ],
        "comparisons": comparisons,
    }
    expected = {
        "membership_equals_iteration": [(v.number, True) for v in originals]
    }
    failed = raised and any(a != b for _, a, b in comparisons)
    return failed, actual, expected


def main():
    start = time.monotonic()
    if not sanity([4, 1, 3, 1], 0):
        print("SANITY FAILED")
        return
    if not sanity([-3, 0, 8, 2], -1):
        print("SANITY FAILED")
        return

    cases = []
    for numbers in ([0], [-7], [1, 2], [-5, 0, 7], [9, -4, 3, 0, 12]):
        size = len(set(numbers))
        for index in (0, -1, size // 2):
            cases.append((list(numbers), index))

    rng = random.Random(184731)
    tested = 0
    while time.monotonic() - start < 175:
        if cases:
            case = cases.pop(0)
        else:
            size = rng.randint(1, 60)
            numbers = rng.sample(range(-10000, 10001), size)
            index = rng.choice((0, -1, size // 2, rng.randrange(size)))
            case = (numbers, index)

        failed, actual, expected = check(case)
        tested += 1
        if failed:
            confirmed, actual_again, expected_again = check(case)
            if confirmed:
                print("COUNTEREXAMPLE:")
                print(repr({"values": case[0], "pop_index": case[1]}))
                print("actual:", repr(actual_again))
                print("expected:", repr(expected_again))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()