import random
import time
from wcwidth import iter_graphemes, iter_graphemes_reverse

# Independent expected side: the documented reverse traversal, reordered
# last-to-first back into first-to-last. Never call iter_graphemes here.
def reference(s):
    return list(reversed(list(iter_graphemes_reverse(s))))


def actual(s):
    return list(iter_graphemes(s))


def main():
    start = time.monotonic()
    deadline = start + 175
    tested = 0

    for s, known in [
        ("hello", list("hello")),
        ("a\u0301b", ["a\u0301", "b"]),
    ]:
        expected = reference(s)
        got = actual(s)
        print("SANITY:", repr(s), repr(got), repr(expected), flush=True)
        if expected != known or got != expected:
            print("SANITY FAILED", flush=True)
            return

    def check(s):
        nonlocal tested
        tested += 1
        expected = reference(s)
        got = actual(s)
        if got != expected:
            # Confirm the same discrepancy on a fresh evaluation.
            again_expected = reference(s)
            again_got = actual(s)
            if again_got != again_expected:
                print("COUNTEREXAMPLE:", flush=True)
                print(repr(s), flush=True)
                print("actual:", repr(again_got), flush=True)
                print("expected:", repr(again_expected), flush=True)
                return True
        return False

    ri = [chr(0x1F1E6 + i) for i in range(26)]
    pieces = [
        "", "a", "b", "\r", "\n", "\r\n", "\x00",
        "\u0300", "\u0301", "\u0308", "\u034f", "\u20dd",
        "\u0301\u0308", "\u200d", "\u200c", "\ufe0e", "\ufe0f",
        "\U000E0100", "\u0600", "\u0903",
        "\u1100", "\u1161", "\u11a8", "\ua960", "\ud7b0",
        "\u1100\u1161\u11a8", "\uac00", "\uac01",
        "\U0001f44d", "\U0001f3fb", "\U0001f3ff",
        "\U0001f44d\U0001f3fd",
        "\U0001f469\u200d\U0001f4bb",
        "\U0001f468\u200d\U0001f469\u200d\U0001f467",
        "\u2764\ufe0f\u200d\U0001f525",
        "\u0915", "\u0937", "\u094d", "\u093c",
        "\u0915\u094d\u0937",
        "\u0915\u094d\u200d\u0937",
        "\u0995\u09cd\u09b7",
        "\u0d15\u0d4d\u0d37",
        "\u0c15\u0c4d\u0c37",
    ] + ri

    handpicked = list(pieces)
    for n in list(range(65)) + [127, 128, 129, 255, 256, 257, 1023]:
        run = "".join(ri[i % 26] for i in range(n))
        handpicked.extend([
            run,
            "\u0301" + run,
            run + "\u0301",
            "\r\n" + run + "\u200d",
            run + "\u0301" + run,
            "\u0301\u0308" + run + "\u0915\u094d\u0937",
        ])

    for s in handpicked:
        if time.monotonic() >= deadline:
            break
        if check(s):
            return

    for left in pieces:
        if time.monotonic() >= deadline:
            break
        for right in pieces:
            if time.monotonic() >= deadline:
                break
            if check(left + right):
                return

    rng = random.Random(0x4752415048454D45)
    while time.monotonic() < deadline:
        mode = rng.randrange(5)
        if mode == 0:
            s = "".join(rng.choice(pieces) for _ in range(rng.randrange(100)))
        elif mode == 1:
            run = "".join(rng.choice(ri) for _ in range(rng.randrange(1025)))
            s = rng.choice(pieces) + run + rng.choice(pieces)
        elif mode == 2:
            s = "\u0301" * rng.randrange(20)
            s += "".join(rng.choice(pieces) for _ in range(rng.randrange(150)))
        elif mode == 3:
            consonants = ["\u0915", "\u0937", "\u0995", "\u0d15"]
            links = ["\u094d", "\u09cd", "\u0d4d"]
            s = "".join(
                rng.choice(consonants) + rng.choice(links)
                + rng.choice(["", "\u200d", "\u0301", "\u093c"])
                for _ in range(rng.randrange(80))
            ) + rng.choice(pieces)
        else:
            chars = []
            for _ in range(rng.randrange(100)):
                if rng.randrange(4):
                    chars.append(rng.choice(pieces))
                else:
                    cp = rng.randrange(0x110000)
                    if not 0xD800 <= cp <= 0xDFFF:
                        chars.append(chr(cp))
            s = "".join(chars)
        if check(s):
            return

    print("NO COUNTEREXAMPLE", tested, flush=True)


if __name__ == "__main__":
    main()