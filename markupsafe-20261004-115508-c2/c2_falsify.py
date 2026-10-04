import random
import time
from markupsafe import EscapeFormatter, escape


class TrustedHTML:
    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


def reference_escape_text(text):
    return (
        text.replace("&", "&amp;")
        .replace(">", "&gt;")
        .replace("<", "&lt;")
        .replace("'", "&#39;")
        .replace('"', "&#34;")
    )


def main():
    for text in ("ordinary text", '<b title="x">&\'</b>'):
        expected = reference_escape_text(text)
        actual = str(escape(text))
        print("SANITY:", repr(text), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    formatter = EscapeFormatter(escape)
    tested = 0
    deadline = time.monotonic() + 175.0

    def observe(html):
        try:
            return ("result", str(formatter.format_field(TrustedHTML(html), "")))
        except Exception as exc:
            return ("exception", type(exc).__name__, str(exc))

    def check(html):
        nonlocal tested
        tested += 1
        # Documented definition: __html__ returns trusted HTML unchanged.
        expected = html
        actual = observe(html)
        if actual != ("result", expected):
            repeated = observe(html)
            if repeated == actual:
                displayed = actual[1] if actual[0] == "result" else actual
                print(
                    "COUNTEREXAMPLE:",
                    repr(html),
                    "actual=" + repr(displayed),
                    "expected=" + repr(expected),
                )
                return True
        return False

    edges = [
        "",
        "ordinary text",
        "<b>x</b>",
        "&",
        "'",
        '"',
        "&amp;",
        "&#39;",
        "&#x3c;",
        "<>",
        'a & b <span title="\'">x</span>',
        "\x00",
        "\n\t",
        "caf\u00e9 \U0001f600",
    ]
    for html in edges:
        if check(html):
            return

    rng = random.Random(947321)
    atoms = [
        "", "a", "ordinary text", "<", ">", "&", "'", '"',
        "<b>x</b>", "&amp;", "&lt;", "&quot;", "&#39;", "&#x3c;",
        "\x00", "\n", "\t", "\u00e9", "\U0001f600",
    ]
    while time.monotonic() < deadline:
        html = "".join(rng.choice(atoms) for _ in range(rng.randrange(65)))
        if check(html):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()