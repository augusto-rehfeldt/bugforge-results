import calendar
import random
import time
from html.parser import HTMLParser


class StylesheetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "link":
            attributes = dict(attrs)
            if attributes.get("rel", "").lower() == "stylesheet":
                self.hrefs.append(attributes.get("href"))


def actual(css):
    page = calendar.HTMLCalendar().formatyearpage(
        2024, width=3, css=css, encoding="utf-8"
    )
    parser = StylesheetParser()
    parser.feed(page.decode("utf-8"))
    parser.close()
    return parser.hrefs[0] if len(parser.hrefs) == 1 else parser.hrefs


def observe(css):
    try:
        return actual(css)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 180
    for css in ("calendar.css", "ordinaryStyle.css"):
        expected = css
        result = observe(css)
        print("SANITY:", repr(css), "actual =", repr(result),
              "expected =", repr(expected))
        if result != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(2024)
    edges = [
        "a&notin;.css",
        'a"b.css',
        "a&b.css",
        '"a.css',
        'a".css',
        "&.css",
        'a&"b.css',
    ]
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&"'
    tested = 0

    def check(css):
        nonlocal tested
        tested += 1
        expected = css  # Documented stylesheet filename, unchanged.
        result = observe(css)
        if result != expected:
            repeated = observe(css)
            if repeated == result:
                inputs = {
                    "year": 2024,
                    "width": 3,
                    "encoding": "utf-8",
                    "css": css,
                }
                print("COUNTEREXAMPLE:", repr(inputs),
                      "actual =", repr(result), "expected =", repr(expected))
                return True
        return False

    for css in edges:
        if time.monotonic() >= deadline:
            break
        if check(css):
            return

    while time.monotonic() < deadline:
        css = "".join(rng.choice(alphabet)
                      for _ in range(rng.randint(1, 80))) + ".css"
        if check(css):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()