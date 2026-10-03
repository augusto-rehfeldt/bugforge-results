import html.parser
import random
import time


class Collector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def actual(text):
    try:
        parser = Collector()
        parser.feed(text)
        parser.close()
        return ("data", "".join(parser.parts))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def reference(text):
    # Parse decimal digits independently, saturating once outside Unicode.
    assert text.startswith("&#") and text.endswith(";")
    digits = text[2:-1]
    assert digits and all("0" <= digit <= "9" for digit in digits)
    value = 0
    for digit in digits:
        value = min(0x110000, value * 10 + ord(digit) - ord("0"))
    if value == 0 or value > 0x10FFFF or 0xD800 <= value <= 0xDFFF:
        return ("data", "\uFFFD")
    # The ordinary sanity cases avoid HTML's special control-code mappings.
    return ("data", chr(value))


def main():
    deadline = time.monotonic() + 180
    sanity_ok = True
    for text in ("&#65;", "&#1114112;"):
        expected = reference(text)
        result = actual(text)
        print("SANITY:", repr(text), "actual:", repr(result),
              "expected:", repr(expected))
        sanity_ok = sanity_ok and result == expected
    if not sanity_ok:
        print("SANITY FAILED")
        return

    tested = 0

    def check(n):
        nonlocal tested
        text = "&#" + "9" * n + ";"
        expected = reference(text)
        result = actual(text)
        tested += 1
        if result != expected:
            repeated = actual(text)
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr(text),
                      "actual:", repr(repeated), "expected:", repr(expected))
                return True
        return False

    for n in (4301, 4302, 4303, 4400, 5000, 10000, 100000):
        if time.monotonic() >= deadline:
            break
        if check(n):
            return

    rng = random.Random(20260403)
    while time.monotonic() < deadline:
        if check(rng.randint(4301, 100000)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()