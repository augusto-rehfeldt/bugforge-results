import random
import time
from sortedcontainers import SortedDict


def reference(mapping):
    return {(key, value) for key, value in mapping.items()}


def evaluate(mapping, key_function=None):
    try:
        d = (SortedDict(mapping) if key_function is None
             else SortedDict(key_function, mapping))
        result = d.items() & d.items()
        members = set(result)
        return ("result", members)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    deadline = start + 175
    tested = 0

    for index, mapping in enumerate(
        [{1: "a", 2: "b"}, {-4: ("x", 1), 0: None, 7: 12}], 1
    ):
        expected = reference(mapping)
        actual = evaluate(mapping)
        passed = actual == ("result", expected)
        print("SANITY {}: {}".format(index, "PASS" if passed else "FAIL"))
        if not passed:
            print("SANITY FAILED")
            return

    def check(mapping):
        nonlocal tested
        tested += 1
        expected = reference(mapping)
        actual = evaluate(mapping, lambda k: k.real)
        if actual == ("result", expected):
            return False

        repeated = evaluate(mapping, lambda k: k.real)
        if repeated != actual:
            return False

        print("COUNTEREXAMPLE:")
        print(repr({
            "constructor": "SortedDict(lambda k: k.real, mapping)",
            "mapping": mapping,
        }))
        print("actual:", repr(actual))
        print("expected:", repr(expected))
        return True

    edges = [
        {},
        {1 + 0j: "a"},
        {1 + 0j: "a", 2 + 0j: "b"},
        {-3 + 2j: None, 0 - 4j: ("v", 1), 5 + 7j: frozenset({2})},
        {complex(i, -i): i for i in range(-10, 11)},
    ]
    for mapping in edges:
        if check(mapping):
            return

    rng = random.Random(1729)
    values = [None, False, 17, "a", "b", (1, "x"), frozenset({3, 4})]
    while time.monotonic() < deadline:
        size = rng.randrange(0, 65)
        real_parts = rng.sample(range(-100000, 100001), size)
        mapping = {
            complex(real, rng.randint(-10000, 10000)): rng.choice(values)
            for real in real_parts
        }
        if check(mapping):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()