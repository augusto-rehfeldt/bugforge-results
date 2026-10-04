import random
import time
import wcwidth
from wcwidth import TextSizing, TextSizingParams

wrap = wcwidth.wrap
module_width = getattr(wcwidth, "width", wcwidth.wcswidth)


def reference_width(text):
    """Independent width calculation for ASCII and OSC 66 sized ASCII."""
    total = 0
    pos = 0
    while pos < len(text):
        if text.startswith("\x1b]66;", pos):
            header_end = text.find(";", pos + 5)
            if header_end < 0:
                raise ValueError("Incomplete sizing header")
            params = text[pos + 5:header_end]
            scale = 1
            for parameter in params.split(":"):
                if parameter.startswith("s="):
                    scale = int(parameter[2:])
            bel = text.find("\x07", header_end + 1)
            st = text.find("\x1b\\", header_end + 1)
            endings = [(bel, 1), (st, 2)]
            endings = [(end, size) for end, size in endings if end >= 0]
            if not endings:
                raise ValueError("Incomplete sizing payload")
            end, terminator_size = min(endings)
            payload = text[header_end + 1:end]
            if any(not (" " <= char <= "~") for char in payload):
                raise ValueError("Unexpected non-ASCII payload")
            total += scale * len(payload)
            pos = end + terminator_size
        else:
            char = text[pos]
            if not (" " <= char <= "~"):
                raise ValueError("Unexpected control character")
            total += 1
            pos += 1
    return total


for ordinary in ("hello", "a b  xyz"):
    expected = reference_width(ordinary)
    actual = module_width(ordinary)
    print("SANITY:", repr(ordinary), "actual =", actual, "expected =", expected)
    if actual != expected:
        print("SANITY FAILED")
        raise SystemExit(0)

deadline = time.monotonic() + 175
tested = 0
rng = random.Random(6602026)


def check(scale, k, W, p):
    global tested
    sized = TextSizing(
        TextSizingParams(scale=scale), "x" * k, "\x07"
    ).make_sequence()
    text = "a" * p + " " + sized

    # Verify the independent interpreter against the defining arithmetic,
    # without asking wrap (or the module's width function).
    assert reference_width(sized) == scale * k
    assert reference_width(text) == p + 1 + scale * k

    arguments = {
        "text": text,
        "width": W,
        "break_long_words": True,
    }
    tested += 1
    try:
        lines = wrap(text, width=W, break_long_words=True)
        widths = [reference_width(line) for line in lines]
        failed = any(value > W for value in widths)
        actual = {"lines": lines, "reference_widths": widths}
    except Exception as error:
        failed = True
        actual = {"exception": repr(error)}

    if not failed:
        return False

    # Require the same failure to recur.
    try:
        repeated_lines = wrap(text, width=W, break_long_words=True)
        repeated_widths = [reference_width(line) for line in repeated_lines]
        repeated = {
            "lines": repeated_lines,
            "reference_widths": repeated_widths,
        }
        repeated_failed = any(value > W for value in repeated_widths)
    except Exception as error:
        repeated = {"exception": repr(error)}
        repeated_failed = True

    if repeated_failed and repeated == actual:
        print("COUNTEREXAMPLE:")
        print(repr(arguments))
        print("actual:", repr(actual))
        print("expected:", repr({"every_line_width_at_most": W}))
        return True
    return False


edges = [
    (2, 1, 2, 1),
    (2, 2, 4, 1),
    (3, 1, 3, 1),
    (8, 1, 8, 1),
    (8, 10, 80, 1),
    (2, 10, 20, 9),
    (8, 10, 90, 10),
]
for scale in range(2, 9):
    for k in (1, 2, 10):
        for extra in (0, 1, 10):
            W = scale * k + extra
            for p in (0, extra, extra + 1, W - k - 1, W - 1):
                if 0 <= p < W:
                    edges.append((scale, k, W, p))

for case in edges:
    if time.monotonic() >= deadline:
        break
    if check(*case):
        raise SystemExit(0)

while time.monotonic() < deadline:
    scale = rng.randint(2, 8)
    k = rng.randint(1, 10)
    W = rng.randint(scale * k, scale * k + 10)
    if rng.random() < 0.85:
        low = W - scale * k
        high = W - k - 1
        p = rng.randint(low, high)
    else:
        p = rng.randrange(W)
    if check(scale, k, W, p):
        raise SystemExit(0)

print("NO COUNTEREXAMPLE", tested)