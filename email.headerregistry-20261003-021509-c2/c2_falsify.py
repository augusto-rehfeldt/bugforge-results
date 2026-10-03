import base64
import random
import re
import time
from email.errors import InvalidBase64PaddingDefect
from email.headerregistry import HeaderRegistry, UnstructuredHeader

WORD = re.compile(r"=\?utf-8\?b\?([A-Za-z0-9+/]*={0,2})\?=", re.I)


def reference(value):
    # Base64 represents three bytes with four characters. For complete
    # ASCII byte strings, lengths congruent to 2 or 3 require padding.
    for match in WORD.finditer(value):
        payload = match.group(1)
        data = payload.rstrip("=")
        required = (-len(data)) % 4
        supplied = len(payload) - len(data)
        if len(data) % 4 in (2, 3) and supplied < required:
            return True
    return False


def parser_reports_padding(value):
    return any(
        isinstance(d, InvalidBase64PaddingDefect)
        for d in UnstructuredHeader.value_parser(value).all_defects
    )


def actual(value):
    return any(
        isinstance(d, InvalidBase64PaddingDefect)
        for d in HeaderRegistry()("Subject", value).defects
    )


def word(text, strip_padding=True):
    payload = base64.b64encode(text.encode("ascii")).decode("ascii")
    if strip_padding:
        payload = payload.rstrip("=")
    return "=?utf-8?b?" + payload + "?="


def main():
    deadline = time.monotonic() + 175
    tested = 0

    for value in ("ordinary subject", "before =?utf-8?b?YQ==?= after"):
        expected = reference(value)
        try:
            observed = actual(value)
            parsed = parser_reports_padding(value)
        except Exception:
            print("SANITY FAILED")
            return
        print("SANITY:", repr(value), "actual:", observed, "expected:", expected)
        if observed != expected or parsed != expected:
            print("SANITY FAILED")
            return

    def check(value):
        nonlocal tested
        expected = reference(value)
        # The target property is conditional on this parser defect.
        if not expected or not parser_reports_padding(value):
            return False
        tested += 1
        observed = actual(value)
        if observed != expected:
            # Repeat both sides of the implication on the identical input.
            repeated = actual(value)
            if parser_reports_padding(value) and repeated != expected:
                print("COUNTEREXAMPLE:", repr(value))
                print("actual:", repeated)
                print("expected:", expected)
                return True
        return False

    handpicked = ["=?utf-8?b?YQ?="]
    for text in ("a", "ab", "abcd", "abcde", " ", "  ", "Hello", "\t"):
        bad = word(text)
        good = word("ordinary", False)
        handpicked.extend([
            bad,
            "before " + bad,
            bad + " after",
            "before " + bad + " after",
            good + " " + bad,
            bad + " " + good,
            bad + " " + bad,
            "before " + good + " " + bad + " after",
            "(" + bad + ")",
            bad + "\t" + good,
        ])

    for value in handpicked:
        if check(value):
            return

    rng = random.Random(2047)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,_-"
    while time.monotonic() < deadline:
        parts = []
        for _ in range(rng.randint(1, 6)):
            length = rng.choice([1, 2, 4, 5, 7, 8, 10, 11, 16, 17, 28, 29])
            text = "".join(rng.choice(alphabet) for _ in range(length))
            parts.append(word(text, rng.random() < 0.8))
        separator = rng.choice([" ", "  ", "\t", " ordinary ", " / "])
        value = separator.join(parts)
        value = rng.choice(["", "prefix ", "ordinary text ("]) + value
        value += rng.choice(["", " suffix", ") ordinary text"])
        if check(value):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()