import plistlib
import random
import time


def reference(d):
    # The documented round-trip result is the original dictionary.
    return {key: value for key, value in d.items()}


def check(d):
    expected = reference(d)
    try:
        actual = plistlib.loads(plistlib.dumps(d, fmt=plistlib.FMT_XML))
        return actual == expected, actual, expected
    except Exception as exc:
        return False, ("EXCEPTION", type(exc).__name__, str(exc)), expected


def main():
    start = time.monotonic()
    deadline = start + 175
    cases = 0

    for d in ({"ordinary": 1}, {"alpha": -2, "beta": 3}):
        ok, actual, expected = check(d)
        print("SANITY:", repr(d), "actual:", repr(actual),
              "expected:", repr(expected))
        if not ok:
            print("SANITY FAILED")
            return

    def test(d):
        nonlocal cases
        cases += 1
        ok, actual, expected = check(d)
        if not ok:
            repeated_ok, repeated_actual, repeated_expected = check(d)
            if not repeated_ok and repeated_actual == actual:
                print("COUNTEREXAMPLE:")
                print(repr(d))
                print("actual:", repr(repeated_actual))
                print("expected:", repr(repeated_expected))
                return True
        return False

    hand_picked = [
        {"a\rb": 1, "a\nb": 2},
        {"\r": 1},
        {"a\rb": 1},
        {"a\r\nb": 1, "a\nb": 2},
        {"\r": 1, "\n": 2, "\r\n": 3},
        {"a\r\rb": 1, "a\n\nb": 2},
        {"\ra": 1, "\na": 2},
        {"a\r": 1, "a\n": 2},
        {"": 0, "\r\n": -1},
    ]
    for d in hand_picked:
        if time.monotonic() >= deadline:
            break
        if test(d):
            return

    rng = random.Random(948173)
    alphabet = "ab \t\r\n<&>"
    while time.monotonic() < deadline:
        d = {}
        for _ in range(rng.randint(1, 6)):
            key = "".join(rng.choice(alphabet)
                          for _ in range(rng.randint(0, 10)))
            d[key] = rng.randint(-10, 10)
        if rng.random() < 0.7:
            prefix = rng.choice(["", "a", "ab"])
            suffix = rng.choice(["", "b", "ba"])
            d[prefix + "\r" + suffix] = 1
            d[prefix + "\n" + suffix] = 2
            if rng.random() < 0.5:
                d[prefix + "\r\n" + suffix] = 3
        if test(d):
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()