import random
import time
from sortedcontainers import SortedDict


def check(pairs):
    d = SortedDict()

    def failing_pairs():
        for key, value in pairs:
            yield key, value
        raise RuntimeError("intentional generator failure")

    try:
        d.update(failing_pairs())
    except RuntimeError:
        pass

    actual = list(d.keys())
    expected = sorted(dict.keys(d))
    return actual, expected


def main():
    sanity_inputs = [
        [(3, 30), (1, 10), (2, 20)],
        [(2, 20), (-1, 7), (2, 99), (0, 0)],
    ]
    for i, pairs in enumerate(sanity_inputs, 1):
        reference = {}
        for key, value in pairs:
            reference[key] = value
        expected = sorted(reference)
        d = SortedDict()
        d.update(pairs)
        actual = list(d.keys())
        agrees = actual == expected and dict(d) == reference
        print("SANITY {}: {}".format(i, agrees))
        if not agrees:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    deadline = start + 175
    tested = 0

    def test(pairs):
        nonlocal tested
        tested += 1
        actual, expected = check(pairs)
        if actual != expected:
            repeated_actual, repeated_expected = check(pairs)
            if repeated_actual != repeated_expected:
                print("COUNTEREXAMPLE:")
                print(repr(pairs))
                print("actual:", repr(repeated_actual))
                print("expected:", repr(repeated_expected))
                return True
        return False

    hand_picked = [
        [(1, 10)],
        [(0, 0)],
        [(-1, -10)],
        [(2, 20), (1, 10)],
        [(1, 10), (1, 11)],
        [(-10**100, 1), (10**100, 2), (0, 3)],
        [(k, -k) for k in range(100, -1, -1)],
    ]
    for pairs in hand_picked:
        if time.monotonic() >= deadline:
            break
        if test(pairs):
            return

    rng = random.Random(8675309)
    while time.monotonic() < deadline:
        size = rng.randint(1, 256)
        pairs = [
            (rng.randint(-1000, 1000), rng.randint(-10**6, 10**6))
            for _ in range(size)
        ]
        if test(pairs):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()