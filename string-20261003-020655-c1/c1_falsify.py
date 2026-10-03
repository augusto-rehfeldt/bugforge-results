import random
import string
import time


class FalseySep(str):
    __bool__ = lambda self: False


def reference(s, sep):
    return sep.join(map(str.capitalize, s.split(sep)))


def main():
    for s, sep in [("hello WORLD", " "), ("a|b", "|")]:
        actual = string.capwords(s, sep)
        expected = reference(s, sep)
        print("SANITY:", repr((s, sep)), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    tested = 0

    def check(s, sep):
        nonlocal tested
        expected = reference(s, sep)
        actual = string.capwords(s, sep)
        tested += 1
        if actual != expected:
            repeated_actual = string.capwords(s, sep)
            repeated_expected = reference(s, sep)
            if repeated_actual != repeated_expected:
                # repr records the string value; the class identifies its type.
                print("COUNTEREXAMPLE:")
                print(
                    "{'s': %r, 'sep': %r, 'sep_class': 'FalseySep'}"
                    % (s, sep)
                )
                print("actual:", repr(repeated_actual))
                print("expected:", repr(repeated_expected))
                return True
        return False

    for delimiter in ["|", ",", "::"]:
        sep = FalseySep(delimiter)
        for s in [
            delimiter.join(["a", "b"]),
            delimiter.join(["hello", "WORLD", "three words"]),
            delimiter.join(["", "a", "", "b", ""]),
            "",
            delimiter,
            "  MIXED case  ",
        ]:
            if check(s, sep):
                return

    rng = random.Random(1729)
    alphabet = "abcXYZ012 \t\nßé"
    while time.monotonic() - started < 175:
        sep = FalseySep(rng.choice(["|", ",", "::"]))
        words = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(25)))
            for _ in range(rng.randrange(2, 10))
        ]
        if check(sep.join(words), sep):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()