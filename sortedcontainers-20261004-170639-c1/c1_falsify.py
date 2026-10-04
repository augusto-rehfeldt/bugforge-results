import random
import time
from sortedcontainers import SortedDict


class M(dict):
    def __iter__(self):
        return iter(())


def reference(initial, entries):
    result = dict(initial)
    result.update(M(entries))
    return result


def evaluate(initial, entries):
    expected = reference(initial, entries)
    try:
        d = SortedDict(initial)
        d.update(M(entries))
        actual = dict(d)
    except Exception as exc:
        actual = ("EXCEPTION", type(exc).__name__, str(exc))
    return actual, expected


def main():
    deadline = time.monotonic() + 175.0

    for index, (initial, entries) in enumerate([
        ({1: 10, 3: 30}, {2: 20}),
        ({-2: 5, 0: 7}, {-2: 9, 4: 11}),
    ], 1):
        expected = dict(initial)
        for key, value in entries.items():
            expected[key] = value
        d = SortedDict(initial)
        d.update(entries)
        actual = dict(d)
        print("SANITY", index, actual, expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(initial, entries):
        nonlocal tested
        tested += 1
        actual, expected = evaluate(initial, entries)
        if actual != expected:
            repeated_actual, repeated_expected = evaluate(initial, entries)
            if repeated_actual == actual and repeated_expected == expected:
                print("COUNTEREXAMPLE:")
                print(repr({"initial": initial, "M_entries": entries}))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    for size in (100, 1, 2, 9, 10, 11, 99, 101, 200):
        initial = {i: -i for i in range(size)}
        threshold = size // 10
        for count in dict.fromkeys((1, max(1, threshold - 1),
                                   max(1, threshold), threshold + 1)):
            entries = {size + i: 1000 + i for i in range(count)}
            if check(initial, entries):
                return
            overwrite = {i: 2000 + i for i in range(min(count, size))}
            if check(initial, overwrite):
                return

    rng = random.Random(20260719)
    while time.monotonic() < deadline:
        size = rng.randint(1, 500)
        keys = rng.sample(range(-2000, 2001), size)
        initial = {key: rng.randint(-10000, 10000) for key in keys}
        count = rng.choice([
            1, max(1, size // 10 - 1),
            max(1, size // 10), size // 10 + 1,
            rng.randint(1, 100),
        ])
        incoming_keys = rng.sample(range(-2500, 2501), count)
        entries = {
            key: rng.randint(-10000, 10000) for key in incoming_keys
        }
        if check(initial, entries):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()