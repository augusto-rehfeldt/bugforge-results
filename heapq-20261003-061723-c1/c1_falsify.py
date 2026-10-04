import heapq
import random
import time


def reference(lists, selected):
    values = []
    for sequence in lists:
        for value in sequence:
            if value == selected:
                return ("exception", "StopIteration")
            values.append(value)
    # Independent insertion sort.
    ordered = []
    for value in values:
        position = len(ordered)
        ordered.append(value)
        while position and ordered[position - 1] > value:
            ordered[position] = ordered[position - 1]
            position -= 1
        ordered[position] = value
    return ("result", ordered)


def actual(lists, selected):
    def key(value):
        if value == selected:
            raise StopIteration("selected element")
        return value

    try:
        return ("result", list(heapq.merge(*lists, key=key)))
    except StopIteration:
        return ("exception", "StopIteration")
    except RuntimeError as exc:
        if isinstance(exc.__cause__, StopIteration):
            return ("exception", "StopIteration")
        return ("unexpected exception", type(exc).__name__, str(exc))
    except Exception as exc:
        return ("unexpected exception", type(exc).__name__, str(exc))


def main():
    started = time.monotonic()
    for index, lists in enumerate(
        ([[1, 3], [2, 4]], [[-5, -1, 2], [-5, 0, 2], [1, 7]]), 1
    ):
        expected = reference(lists, None)
        observed = actual(lists, None)
        print("SANITY", index, "actual:", repr(observed),
              "expected:", repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    cases = 0

    def check(lists, selected):
        nonlocal cases
        cases += 1
        expected = reference(lists, selected)
        observed = actual(lists, selected)
        if observed != expected:
            repeated = actual(lists, selected)
            if repeated == observed:
                print("COUNTEREXAMPLE:")
                print(repr({"lists": lists, "raise_StopIteration_on": selected}))
                print("actual:", repr(observed))
                print("expected:", repr(expected))
                return True
        return False

    hand_picked = [
        ([[1, 3], [2, 4]], 1),
        ([[1, 3], [2, 4]], 2),
        ([[1, 3], [2, 4]], 3),
        ([[1, 4, 7], [2, 5, 8], [3, 6, 9]], 4),
        ([[0, 0, 2], [0, 1, 3]], 0),
        ([[-4, -2, 0], [-3, -1, 1]], -2),
        ([[1], [2]], 1),
    ]
    for lists, selected in hand_picked:
        if check(lists, selected):
            return

    rng = random.Random(741923)
    while time.monotonic() - started < 175:
        lists = [
            sorted(rng.randint(-50, 50) for _ in range(rng.randint(1, 20)))
            for _ in range(rng.randint(2, 6))
        ]
        sequence = rng.choice(lists)
        selected = rng.choice(sequence)
        if check(lists, selected):
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()