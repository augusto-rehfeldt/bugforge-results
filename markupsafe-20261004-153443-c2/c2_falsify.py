import random
import time
from markupsafe import EscapeFormatter, escape


class SafeHTML:
    def __init__(self, spec, html):
        self.spec = spec
        self.html = html

    def __html_format__(self, spec):
        if spec != self.spec:
            raise ValueError("Unsupported format specification")
        return self.html


formatter = EscapeFormatter(escape)


def reference(spec, html):
    # The documented method returns HTML that is already safe.
    assert isinstance(spec, str) and spec
    assert type(html) is str
    return html


def evaluate(spec, html):
    try:
        result = formatter.format_field(SafeHTML(spec, html), spec)
        return ("result", result)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    for index, (spec, html) in enumerate(
        [("link", "hello"), ("label", "ordinary text")], 1
    ):
        expected = reference(spec, html)
        actual = evaluate(spec, html)
        agrees = actual[0] == "result" and actual[1] == expected
        print("SANITY", index, "OK" if agrees else "FAILED")
        if not agrees:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    tested = 0

    def check(spec, html):
        nonlocal tested
        expected = reference(spec, html)
        actual = evaluate(spec, html)
        tested += 1
        if actual[0] == "result" and actual[1] == expected:
            return False

        repeated = evaluate(spec, html)
        if repeated != actual:
            return False

        print("COUNTEREXAMPLE:")
        print(repr({"spec": spec, "html": html}))
        print("actual:", repr(actual[1] if actual[0] == "result" else actual))
        print("expected:", repr(expected))
        return True

    edge_cases = [
        ("link", "<em>hello</em>"),
        ("link", '<a href="/hello" title="greeting">hello</a>'),
        ("label", "<span title='quoted attribute'>hello</span>"),
        ("entity", "<p>&amp; &lt; &gt; &quot; &#39;</p>"),
        ("link", '<a href="/?a=1&amp;b=2">A &amp; B</a>'),
        ("empty", ""),
    ]
    for spec, html in edge_cases:
        if check(spec, html):
            return

    rng = random.Random(918273)
    tags = ["em", "strong", "span", "p", "a"]
    fragments = ["hello", "world", "&amp;", "&lt;", "&quot;", "&#39;", "é", "雪"]

    while time.monotonic() - started < 175:
        tag = rng.choice(tags)
        spec = rng.choice(["link", "label", "entity", "custom"])
        body = " ".join(rng.choice(fragments) for _ in range(rng.randrange(1, 8)))
        quote = rng.choice(['"', "'"])
        title = rng.choice(["greeting", "A &amp; B", "&quot;quoted&quot;"])
        html = (
            "<" + tag + " title=" + quote + title + quote + ">"
            + body + "</" + tag + ">"
        )
        if check(spec, html):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()