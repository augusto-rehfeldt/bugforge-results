import difflib
import random
import time
from html.parser import HTMLParser


class SourceCells(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "td" and dict(attrs).get("nowrap") == "nowrap":
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.current is not None:
            self.cells.append("".join(self.current))
            self.current = None


def actual(s):
    parser = SourceCells()
    parser.feed(difflib.HtmlDiff().make_table([s], [s]))
    parser.close()
    return parser.cells


def reference(s):
    # Identical lines must appear verbatim in both source-text cells.
    return [s, s]


def main():
    for s in ("ABC", "HelloWorld"):
        observed = actual(s)
        expected = reference(s)
        print("SANITY:", repr(s), repr(observed), repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 180
    rng = random.Random(1729)
    tested = 0
    edges = [
        "A\u0001B",
        "A\u0001\u0001B",
        "AB\u0001CD",
        "A\u0001B\u0001C",
        "a\u0001z",
        "AAAA\u0001BBBB",
    ]

    def candidates():
        yield from edges
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        while True:
            n = rng.randint(2, 256)
            chars = [rng.choice(letters) for _ in range(n)]
            for _ in range(rng.randint(1, 16)):
                chars.insert(rng.randrange(1, len(chars)), "\u0001")
            yield "".join(chars)

    for s in candidates():
        if time.monotonic() >= deadline:
            break
        tested += 1
        expected = reference(s)
        observed = actual(s)
        if observed != expected:
            repeated = actual(s)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr(s))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()