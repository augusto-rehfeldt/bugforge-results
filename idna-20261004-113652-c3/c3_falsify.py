import random
import time
import unicodedata

import idna


def make_label(letter, count):
    # These letters are NFC, IDNA-permitted letters without contextual rules.
    ulabel = unicodedata.normalize("NFC", letter * count)
    alabel = "xn--" + ulabel.encode("punycode").decode("ascii")
    return alabel, ulabel


def reference(alabel, ulabel):
    # An A-label must meet the DNS limit of 63 octets.
    if len(alabel.encode("ascii")) > 63:
        return ("error", "IDNAError")
    return ("unicode", ulabel)


def observe(alabel):
    try:
        return ("unicode", idna.decode(alabel))
    except idna.IDNAError:
        return ("error", "IDNAError")
    except Exception as exc:
        return ("unexpected exception", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 170
    tested = 0

    for letter, count in (("ü", 1), ("é", 10)):
        alabel, ulabel = make_label(letter, count)
        expected = reference(alabel, ulabel)
        actual = observe(alabel)
        tested += 1
        print("SANITY:", repr(alabel), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    def check(letter, count):
        nonlocal tested
        alabel, ulabel = make_label(letter, count)
        expected = reference(alabel, ulabel)
        actual = observe(alabel)
        tested += 1
        if actual != expected:
            repeated = observe(alabel)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(alabel),
                      "actual:", repr(actual), "expected:", repr(expected))
                return True
        return False

    # For ü, these include exactly 63, 64, and 65 ASCII octets.
    for count in (57, 58, 59, 60, 100, 256, 1000):
        if time.monotonic() >= deadline:
            break
        if check("ü", count):
            return

    rng = random.Random(5890)
    letters = ("ü", "é", "ñ", "å", "ø", "α", "ж")
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        letter = rng.choice(letters)
        count = rng.choice((rng.randint(1, 80), rng.randint(81, 2000)))
        if check(letter, count):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()