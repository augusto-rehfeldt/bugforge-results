import email.utils
import random
import string
import time


def reference(s):
    return s


def actual(s):
    return email.utils.encode_rfc2231(s, charset=None, language=None)


def main():
    for s in ("hello", "abc123"):
        expected = reference(s)
        result = actual(s)
        print("SANITY:", repr(s), repr(result), repr(expected))
        if result != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(s):
        nonlocal tested
        expected = reference(s)
        result = actual(s)
        tested += 1
        if result != expected:
            repeated = actual(s)
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr(s), repr(repeated), repr(expected))
                return True
        return False

    edges = [
        "", "a b", "%", "'", "/", "a/b", "a%b", "a'b",
        " ", "\t", "\r\n", "\x00", "\x7f",
        string.ascii_letters, string.digits, string.punctuation,
        "".join(chr(i) for i in range(128)),
    ]
    for s in edges:
        if check(s):
            return

    rng = random.Random(2231)
    alphabet = "".join(chr(i) for i in range(128))
    while time.monotonic() < deadline:
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(257)))
        if check(s):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()