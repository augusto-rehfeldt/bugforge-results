import html
import random
import time


def reference(digits):
    # Compare normalized decimal strings without integer conversion limits.
    normalized = digits.lstrip("0") or "0"
    maximum = "1114111"
    if (len(normalized), normalized) > (len(maximum), maximum):
        return "\ufffd"
    value = 0
    for digit in normalized:
        value = value * 10 + ord(digit) - ord("0")
    if value == 0 or 0xD800 <= value <= 0xDFFF:
        return "\ufffd"
    # The ordinary sanity inputs avoid HTML5's special control mappings.
    return chr(value)


def actual(text):
    try:
        return ("result", html.unescape(text))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    deadline = start + 175

    for digits in ("65", "128512"):
        text = "&#" + digits + ";"
        expected = reference(digits)
        observed = actual(text)
        print("SANITY:", repr(text), repr(observed), repr(expected))
        if observed != ("result", expected):
            print("SANITY FAILED")
            return

    tested = 0

    def check(digits):
        nonlocal tested
        text = "&#" + digits + ";"
        expected = reference(digits)
        observed = actual(text)
        tested += 1
        if observed != ("result", expected):
            repeated = actual(text)
            if repeated != ("result", expected):
                print("COUNTEREXAMPLE:", repr(text),
                      "actual =", repr(repeated),
                      "expected =", repr(expected))
                return True
        return False

    edge_cases = [
        "1114112",
        "1114113",
        "9999999",
    ]
    edge_cases.extend("9" * size for size in (4299, 4300, 4301, 5000))
    edge_cases.extend(
        "0" * zeros + "1114112"
        for zeros in (1, 10, 4292, 4293, 4294, 4993, 10000, 100000)
    )

    for digits in edge_cases:
        if time.monotonic() >= deadline:
            break
        if check(digits):
            return

    rng = random.Random(20260317)
    while time.monotonic() < deadline:
        mode = rng.randrange(3)
        if mode == 0:
            size = rng.choice((4299, 4300, 4301, 5000))
            digits = str(rng.randrange(1, 10)) + "".join(
                str(rng.randrange(10)) for _ in range(size - 1)
            )
        elif mode == 1:
            zeros = rng.choice(
                (0, 1, 4292, 4293, 4294, 4993, 10000, 100000)
            )
            digits = "0" * zeros + str(rng.randrange(1114112, 100000000))
        else:
            size = rng.randrange(8, 20001)
            digits = str(rng.randrange(1, 10)) + "".join(
                str(rng.randrange(10)) for _ in range(size - 1)
            )
        if check(digits):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()