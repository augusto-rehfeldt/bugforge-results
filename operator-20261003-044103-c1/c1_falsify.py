import operator
import random
import time


class S(list):
    def __init__(self, values, mode):
        super().__init__(values)
        self.mode = mode

    def __iadd__(self, other):
        if self.mode == "fresh99":
            return [99]
        if self.mode == "fresh_empty":
            return []
        if self.mode == "fresh_sum":
            return [sum(self) + sum(other)]
        if self.mode == "mutate_reverse":
            self.reverse()
            return list(other)
        if self.mode == "mutate_clear":
            self.clear()
            return [99] + list(other)
        raise AssertionError("Unknown mode")


def observe(original, result, rhs):
    return {
        "result": list(result),
        "result_type": type(result).__name__,
        "original_after": list(original),
        "rhs_after": list(rhs),
        "result_is_original": result is original,
    }


def actual_case(spec):
    a = S(spec["initial"], spec["mode"])
    b = list(spec["rhs"])
    result = operator.iconcat(a, b)
    return observe(a, result, b)


def expected_case(spec):
    a = S(spec["initial"], spec["mode"])
    original = a
    b = list(spec["rhs"])
    a += b
    return observe(original, a, b)


def main():
    deadline = time.monotonic() + 175.0

    for initial, rhs in [([], []), ([1, 2], [3, 4])]:
        a = list(initial)
        b = list(rhs)
        actual = observe(a, operator.iconcat(a, b), b)

        a = list(initial)
        original = a
        b = list(rhs)
        a += b
        expected = observe(original, a, b)

        print("SANITY:", repr((initial, rhs)), actual == expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(spec):
        nonlocal tested
        actual = actual_case(spec)
        expected = expected_case(spec)
        tested += 1
        if actual != expected:
            repeated_actual = actual_case(spec)
            repeated_expected = expected_case(spec)
            if (repeated_actual == actual
                    and repeated_expected == expected
                    and repeated_actual != repeated_expected):
                print("COUNTEREXAMPLE:")
                print(repr(spec))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    modes = (
        "fresh99",
        "fresh_empty",
        "fresh_sum",
        "mutate_reverse",
        "mutate_clear",
    )

    # Minimal documented case first.
    if check({"mode": "fresh99", "initial": [1], "rhs": [2]}):
        return

    for mode in modes:
        for initial in ([], [1], [1, 2], [0, -1, 0]):
            for rhs in ([], [2], [3, 4], [0, -2]):
                if time.monotonic() >= deadline:
                    print("NO COUNTEREXAMPLE", tested)
                    return
                if check({
                    "mode": mode,
                    "initial": list(initial),
                    "rhs": list(rhs),
                }):
                    return

    rng = random.Random(20250308)
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        spec = {
            "mode": rng.choice(modes),
            "initial": [
                rng.randint(-100, 100) for _ in range(rng.randrange(20))
            ],
            "rhs": [
                rng.randint(-100, 100) for _ in range(rng.randrange(20))
            ],
        }
        if check(spec):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()