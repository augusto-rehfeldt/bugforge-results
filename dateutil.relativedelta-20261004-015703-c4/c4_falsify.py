import random
import time
from dateutil.relativedelta import relativedelta, TU

FIELDS = ("years", "months", "days", "hours", "minutes", "seconds", "microseconds")


def reference(offsets, left_n, right_n):
    # Identical integer offsets need no normalization here.
    # Documented weekday semantics: omitted N means +1.
    left_n = 1 if left_n is None else left_n
    right_n = 1 if right_n is None else right_n
    if left_n != right_n:
        raise ValueError("This checker requires equivalent specifications")
    return (True, True)


def observe(offsets, left_n=None, right_n=1):
    left_weekday = TU if left_n is None else TU(left_n)
    right_weekday = TU if right_n is None else TU(right_n)
    a = relativedelta(weekday=left_weekday, **offsets)
    b = relativedelta(weekday=right_weekday, **offsets)
    return (a == b, hash(a) == hash(b))


def main():
    for number, (offsets, n) in enumerate(
        [
            ({"days": 3, "hours": 2}, 1),
            ({"months": -2, "minutes": 15}, 2),
        ],
        1,
    ):
        expected = reference(offsets, n, n)
        actual = observe(offsets, n, n)
        print("SANITY", number, "actual:", actual, "expected:", expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0

    def check(offsets):
        nonlocal tested
        expected = reference(offsets, None, 1)
        actual = observe(offsets)
        tested += 1
        if actual != expected:
            repeated = observe(offsets)
            if repeated == actual:
                input_literal = {
                    "offsets": offsets,
                    "left_weekday": ("TU", None),
                    "right_weekday": ("TU", 1),
                }
                print("COUNTEREXAMPLE:")
                print(repr(input_literal))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    edges = [{}]
    for value in (0, 1, -1, 12, -12, 60, -60, 1000000, -1000000,
                  10**12, -(10**12)):
        for field in FIELDS:
            edges.append({field: value})
        edges.append(dict.fromkeys(FIELDS, value))

    for offsets in edges:
        if time.monotonic() - start >= 175:
            break
        if check(offsets):
            return

    rng = random.Random(20260719)
    while time.monotonic() - start < 175:
        offsets = {
            field: rng.randint(-(10**12), 10**12)
            for field in FIELDS
        }
        if check(offsets):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()