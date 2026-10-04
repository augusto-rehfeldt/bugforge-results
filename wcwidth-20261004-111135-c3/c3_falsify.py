import random
import time
import wcwidth

def reference(s):
    # Independent of the reverse iterator: the property's documented
    # expected result is the reversal of the forward segmentation.
    return list(reversed(list(wcwidth.iter_graphemes(s))))

def actual(s):
    try:
        return ("result", list(wcwidth.iter_graphemes_reverse(s)))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))

for s in ("hello", "a\u0301b"):
    expected = reference(s)
    observed = actual(s)
    print("SANITY:", repr(s), repr(observed), repr(expected))
    if observed != ("result", expected):
        print("SANITY FAILED")
        raise SystemExit(0)

rng = random.Random(0xC0FFEE)
deadline = time.monotonic() + 175
tested = 0

def check(s):
    global tested
    expected = reference(s)
    observed = actual(s)
    tested += 1
    if observed != ("result", expected):
        # Repeat both computations on precisely the same input.
        repeated_expected = reference(s)
        repeated_actual = actual(s)
        if repeated_actual != ("result", repeated_expected):
            print("COUNTEREXAMPLE:")
            print(repr(s))
            if repeated_actual[0] == "result":
                print("actual:", repr(repeated_actual[1]))
            else:
                print("actual:", repr(repeated_actual))
            print("expected:", repr(repeated_expected))
            raise SystemExit(0)

ri = [chr(0x1F1E6 + i) for i in range(26)]
emoji = [
    "\U0001F469\u200d\U0001F4BB",
    "\U0001F468\u200d\U0001F469\u200d\U0001F467",
    "\U0001F3F3\ufe0f\u200d\U0001F308",
    "\U0001F469\U0001F3FD\u200d\U0001F680",
]
edges = [
    "", "a", "\u0301", "\u0301\u0308", "\ufe0f", "\u200d",
    "\r\n", "a\r\nb", "\r\r\n\n", "a\u0301\ufe0f",
    *emoji,
]
for s in edges:
    check(s)

prefixes = ["", "a", "\u0301", "\r\n", emoji[0], "\ufe0f"]
suffixes = ["", "b", "\u0301", "\ufe0f", "\u200d", "\r\n", emoji[1]]
for n in list(range(1, 65)) + [127, 128, 129, 511, 512, 513, 4095, 4096, 4097]:
    run = "".join(ri[i % 26] for i in range(n))
    for prefix in prefixes:
        for suffix in suffixes:
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                raise SystemExit(0)
            check(prefix + run + suffix)

tokens = [
    "a", "Z", "0", " ", "\r", "\n", "\r\n",
    "\u0301", "\u0308", "\u0327", "\ufe0e", "\ufe0f",
    "\u200d", "\U0001F600", "\U0001F3FD",
    *ri, *emoji,
]

while time.monotonic() < deadline:
    pieces = []
    for _ in range(rng.randrange(0, 100)):
        if rng.randrange(4) == 0:
            n = rng.choice([
                1, 2, 3, 4, 5, 7, 8, 9, 31, 32, 33,
                127, 128, 129, 1023, 1024, 1025,
            ])
            pieces.append("".join(rng.choice(ri) for _ in range(n)))
        else:
            pieces.append(rng.choice(tokens))
    check("".join(pieces))

print("NO COUNTEREXAMPLE", tested)