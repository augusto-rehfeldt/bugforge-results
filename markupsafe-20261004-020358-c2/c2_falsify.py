import random
import string
import time
import markupsafe

Markup = markupsafe.Markup


def reference_escape(text):
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "'": "&#39;",
        '"': "&#34;",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def observe(letter, replacement):
    try:
        result = Markup(letter).translate({ord(letter): replacement})
        return ("result", str(result), isinstance(result, Markup),
                type(result).__name__)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175
    for text in ("ordinary text", "A&B <tag> \"quoted\" 'text'"):
        expected = reference_escape(text)
        actual = markupsafe.escape(text)
        agrees = str(actual) == expected and isinstance(actual, Markup)
        print("SANITY:", repr(text), agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    tested = 0

    def check(letter, replacement):
        nonlocal tested
        tested += 1
        expected = reference_escape(replacement)
        actual = observe(letter, replacement)
        if actual[0] == "result" and actual[1] == expected and actual[2]:
            return False

        repeated = observe(letter, replacement)
        if repeated != actual:
            return False

        if actual[0] == "result":
            description = (
                f"{actual[3]}({actual[1]!r}), "
                f"isinstance(Markup)={actual[2]}"
            )
        else:
            description = f"raises {actual[1]}({actual[2]!r})"
        print(
            "COUNTEREXAMPLE:",
            repr((letter, replacement)),
            "actual=" + description,
            "expected=Markup(" + repr(expected) + ")",
        )
        return True

    edge_cases = [
        "", "hello", "&", "<", ">", "'", '"',
        "<script>alert('x')</script>",
        "<b>Hello & goodbye</b>",
        "é雪🙂<&>\"'", "\x00<&", "&amp;", "a\nb\t<c>",
    ]
    for replacement in edge_cases:
        for letter in string.ascii_letters:
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check(letter, replacement):
                return

    rng = random.Random(20260221)
    alphabet = string.ascii_letters + string.digits + " &<>\"'\n\té雪🙂\x00"
    while time.monotonic() < deadline:
        letter = rng.choice(string.ascii_letters)
        replacement = "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(129))
        )
        if check(letter, replacement):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()