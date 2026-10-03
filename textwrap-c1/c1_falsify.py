import random
import string
import textwrap
import time


def documented_bound(lines, width):
    """Check the documented bound independently, using exact character counts."""
    for line in lines:
        length = sum(1 for _ in line)
        if length > width:
            return False
    return True


def run(case):
    return textwrap.TextWrapper(
        width=case["width"],
        initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"],
        break_long_words=True,
    ).wrap(case["text"])


def main():
    deadline = time.monotonic() + 175
    tested = 0

    sanity_cases = [
        dict(width=5, text="abcdefgh", initial_indent="", subsequent_indent=""),
        dict(width=6, text="abcdefgh", initial_indent=" ", subsequent_indent="  "),
    ]
    for case in sanity_cases:
        actual = run(case)
        expected = True  # The documented length bound must hold.
        agrees = documented_bound(actual, case["width"]) == expected
        print("SANITY:", repr(case), "agrees:", agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    def check(case):
        nonlocal tested
        tested += 1
        actual = run(case)
        if documented_bound(actual, case["width"]):
            return False

        # Repeat precisely the same input before reporting.
        repeated = run(case)
        if repeated != actual or documented_bound(repeated, case["width"]):
            return False

        print("COUNTEREXAMPLE:")
        print(repr(case))
        print("actual:", repr(repeated))
        print("expected:", repr(
            "Every returned line has length <= {}".format(case["width"])
        ))
        return True

    # Minimal boundary first, followed by below/equal/above-width indentation.
    edge_cases = [
        dict(width=1, text="a", initial_indent=" ", subsequent_indent=""),
    ]
    for width in (1, 2, 3, 8):
        for initial_length in (0, width - 1, width, width + 1):
            for subsequent_length in (0, width - 1, width, width + 1):
                for text in ("a", "ab", "abcdefghijk"):
                    edge_cases.append(dict(
                        width=width,
                        text=text,
                        initial_indent=" " * initial_length,
                        subsequent_indent=" " * subsequent_length,
                    ))

    for case in edge_cases:
        if time.monotonic() >= deadline:
            break
        if check(case):
            return

    rng = random.Random(20260719)
    while time.monotonic() < deadline:
        width = rng.randint(1, 100)
        case = dict(
            width=width,
            text="".join(
                rng.choice(string.ascii_letters)
                for _ in range(rng.randint(1, 500))
            ),
            initial_indent=" " * rng.randint(0, 2 * width + 1),
            subsequent_indent=" " * rng.randint(0, 2 * width + 1),
        )
        if check(case):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()