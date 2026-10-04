import random
import time
from packaging.specifiers import Specifier


def main():
    # Documented equality: a valid specifier equals its original string.
    for text in ("==1.2.3", ">=1"):
        expected_equal = True
        actual_equal = Specifier(text) == text
        print(
            "SANITY:",
            repr(text),
            "actual =", actual_equal,
            "expected =", expected_equal,
        )
        if actual_equal != expected_equal:
            print("SANITY FAILED")
            return

    rng = random.Random(1729)
    deadline = time.monotonic() + 175
    tested = 0

    def check(text):
        nonlocal tested
        tested += 1
        s = Specifier(text)
        if s != text:
            return False

        # Python's required hash for an object equal to this string.
        expected = hash(text)
        actual = hash(s)
        if actual == expected:
            return False

        # Repeat with a newly constructed object to rule out flakiness.
        repeated = Specifier(text)
        repeated_actual = hash(repeated)
        repeated_expected = hash(text)
        if (
            repeated == text
            and repeated_actual == actual
            and repeated_expected == expected
            and repeated_actual != repeated_expected
        ):
            print(
                "COUNTEREXAMPLE:",
                repr(text),
                "actual =", actual,
                "expected =", expected,
            )
            return True
        return False

    edge_cases = (
        "==1.2.3",
        ">=1",
        "!=2.0",
        "~=1.4",
        "==1",
        "==1.0",
        "==1.0.0",
        "  ==1.2.3  ",
        ">= 1",
        "\t!=2.0\n",
        "==1.2.*",
        "!=1.*",
        "==1.0rc1",
        "==1.0.post1",
        "==1.0.dev1",
        "==1!1.0",
        "==1.0+local.1",
    )
    for text in edge_cases:
        if time.monotonic() >= deadline:
            break
        if check(text):
            return

    while time.monotonic() < deadline:
        op = rng.choice(("==", "!=", ">=", "<=", ">", "<", "~="))
        count = rng.randint(2 if op == "~=" else 1, 5)
        parts = [str(rng.randint(0, 100)) for _ in range(count)]
        version = ".".join(parts)

        if rng.randrange(5) == 0:
            version = str(rng.randint(0, 5)) + "!" + version

        suffix = rng.choice(("", "", "a1", "b2", "rc1", ".post1", ".dev1"))
        version += suffix
        if op in ("==", "!="):
            if not suffix and rng.randrange(5) == 0:
                version += ".*"
            elif rng.randrange(5) == 0:
                version += "+local.1"

        text = (
            rng.choice(("", " ", "\t"))
            + op
            + rng.choice(("", " "))
            + version
            + rng.choice(("", " ", "\n"))
        )
        if check(text):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()