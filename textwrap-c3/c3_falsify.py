import random
import textwrap
import time


def documented_property(result, width):
    # Indentation is part of each line, so every character counts.
    return all(len(line) <= width for line in result.split("\n"))


def reference_word_wrap(word, width, initial_indent, subsequent_indent):
    """Independent reference for ordinary single-word sanity cases."""
    lines = []
    remaining = word
    indent = initial_indent
    while remaining:
        capacity = width - len(indent)
        if capacity <= 0:
            raise ValueError("No room for a word character")
        lines.append(indent + remaining[:capacity])
        remaining = remaining[capacity:]
        indent = subsequent_indent
    return "\n".join(lines)


def invoke(case):
    return textwrap.TextWrapper(
        width=case["width"],
        initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"],
        break_long_words=True,
    ).fill(case["text"])


def main():
    sanity_cases = [
        dict(width=8, initial_indent=" ", subsequent_indent="  ", text="abc"),
        dict(width=3, initial_indent=" ", subsequent_indent=" ", text="abcdef"),
    ]
    for number, case in enumerate(sanity_cases, 1):
        expected = reference_word_wrap(
            case["text"], case["width"],
            case["initial_indent"], case["subsequent_indent"],
        )
        actual = invoke(case)
        agrees = actual == expected and documented_property(actual, case["width"])
        print("SANITY {}: reference={!r}, actual={!r}, agrees={}".format(
            number, expected, actual, agrees
        ))
        if not agrees:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(case):
        nonlocal tested
        actual = invoke(case)
        tested += 1
        if documented_property(actual, case["width"]):
            return False

        repeated = invoke(case)
        if repeated != actual or documented_property(repeated, case["width"]):
            return False

        print("COUNTEREXAMPLE:")
        print(repr(case))
        print("actual:", repr(actual))
        # Expected side is the documented bound, not a library-generated wrap.
        print("expected:", repr({
            "every_line_length_at_most": case["width"]
        }))
        return True

    hand_picked = [
        dict(width=1, initial_indent=" ", subsequent_indent="", text="a"),
        dict(width=1, initial_indent="  ", subsequent_indent="", text="a"),
        dict(width=1, initial_indent="", subsequent_indent=" ", text="aa"),
        dict(width=2, initial_indent="  ", subsequent_indent="", text="abc"),
        dict(width=2, initial_indent="", subsequent_indent="   ", text="abcde"),
    ]
    for case in hand_picked:
        if time.monotonic() >= deadline:
            break
        if check(case):
            return

    rng = random.Random(1729)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while time.monotonic() < deadline:
        width = rng.randint(1, 100)
        long_indent = " " * (width + rng.randint(0, 100))
        initial = ""
        subsequent = ""
        if rng.randrange(2):
            initial = long_indent
        else:
            subsequent = long_indent
        case = dict(
            width=width,
            initial_indent=initial,
            subsequent_indent=subsequent,
            text="".join(rng.choice(alphabet) for _ in range(rng.randint(1, 500))),
        )
        if check(case):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()