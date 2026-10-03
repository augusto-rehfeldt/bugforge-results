import html.parser
import random
import sys
import time

def reference(tag):
    prefix = '<div title="&#'
    suffix = ';">'
    assert tag.startswith(prefix) and tag.endswith(suffix)
    digits = tag[len(prefix):-len(suffix)]
    assert digits and all('0' <= c <= '9' for c in digits)
    value = 0
    for c in digits:
        value = value * 10 + (ord(c) - ord('0'))
    assert value == 65
    return ("OK", [("div", [("title", chr(value))])])

class Recorder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []

    def handle_starttag(self, tag, attrs):
        self.events.append((tag, attrs))

def actual(tag):
    parser = Recorder()
    try:
        parser.feed(tag)
        parser.close()
        return ("OK", parser.events)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))

def make_tag(n):
    return '<div title="&#' + '0' * n + '65;">'

def main():
    # Explicitly enable the interpreter's default conversion limit.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(sys.int_info.default_max_str_digits)
        limit = sys.get_int_max_str_digits()
    else:
        limit = 4300

    for n in (0, 3):
        tag = make_tag(n)
        expected = reference(tag)
        observed = actual(tag)
        print("SANITY:", repr(tag), repr(observed), repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(n):
        nonlocal tested
        tag = make_tag(n)
        expected = reference(tag)
        observed = actual(tag)
        tested += 1
        if observed != expected:
            repeated = actual(tag)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr(tag))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    edges = [
        limit - 3, limit - 2, limit - 1, limit,
        limit + 1, limit + 2, 4300, 4301,
        2 * limit, 10 * limit, 100 * limit,
    ]
    for n in dict.fromkeys(max(0, n) for n in edges):
        if time.monotonic() >= deadline:
            break
        if check(n):
            return

    rng = random.Random(20260719)
    while time.monotonic() < deadline:
        if rng.randrange(2):
            n = max(0, limit + rng.randint(-16, 32))
        else:
            n = rng.randint(max(4300, limit), 100 * max(4300, limit))
        if check(n):
            return

    print("NO COUNTEREXAMPLE", tested)

if __name__ == "__main__":
    main()