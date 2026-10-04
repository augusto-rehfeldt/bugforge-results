import random
import time
from html.parser import HTMLParser


class Recorder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.declarations = []

    def handle_decl(self, decl):
        self.declarations.append(decl)


def actual(s):
    parser = Recorder()
    try:
        parser.feed(s)
        parser.close()
        return parser.declarations
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def expected(s):
    return [s[2:-1]]


def main():
    deadline = time.monotonic() + 175.0
    for s in ('<!DOCTYPE html>', '<!DOCTYPE html SYSTEM "example.dtd">'):
        got, want = actual(s), expected(s)
        print("SANITY:", repr(s), "actual:", repr(got), "expected:", repr(want))
        if got != want:
            print("SANITY FAILED")
            return

    tested = 0

    def check(identifier):
        nonlocal tested
        s = '<!DOCTYPE html SYSTEM "' + identifier + '">'
        want = expected(s)
        got = actual(s)
        tested += 1
        if got != want:
            repeated = actual(s)
            if repeated == got:
                print("COUNTEREXAMPLE:")
                print(repr(s))
                print("actual:", repr(repeated))
                print("expected:", repr(want))
                return True
        return False

    edges = [
        "a>b",
        ">",
        ">a",
        "a>",
        ">a>",
        ">>",
        "a>>b",
        ">>>",
        "example.dtd>",
        ">example.dtd",
        "path/to/a>b.dtd",
        "a>b>c",
        "a > b",
        "> >",
        "a'b>c",
        "a>b?x=y",
        "a>b#fragment",
    ]
    for identifier in edges:
        if check(identifier):
            return

    rng = random.Random(20260719)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~/?:#[]@!$&'()*+,;=% "
    while time.monotonic() < deadline:
        length = rng.randint(0, 256)
        chars = [rng.choice(alphabet) for _ in range(length)]
        for _ in range(rng.randint(1, 8)):
            chars.insert(rng.randrange(len(chars) + 1), ">")
        if check("".join(chars)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()