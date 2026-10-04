import unicodedata as ud
import random
import time

u = ud.ucd_3_2_0


def reference_nfd(text):
    """Canonical decomposition and ordering using only Unicode 3.2 metadata."""
    def decompose(ch):
        cp = ord(ch)
        if 0xAC00 <= cp <= 0xD7A3:
            index = cp - 0xAC00
            result = [
                chr(0x1100 + index // 588),
                chr(0x1161 + (index % 588) // 28),
            ]
            if index % 28:
                result.append(chr(0x11A7 + index % 28))
            return result
        mapping = u.decomposition(ch)
        if not mapping or mapping.startswith("<"):
            return [ch]
        result = []
        for token in mapping.split():
            result.extend(decompose(chr(int(token, 16))))
        return result

    ordered = []
    for ch in text:
        for part in decompose(ch):
            ccc = u.combining(part)
            position = len(ordered)
            if ccc:
                while position:
                    previous = u.combining(ordered[position - 1])
                    if previous == 0 or previous <= ccc:
                        break
                    position -= 1
            ordered.insert(position, part)
    return "".join(ordered)


def main():
    deadline = time.monotonic() + 170
    tested = 0

    for text in ("caf\u00e9", "a\u0301\u0316"):
        expected = reference_nfd(text)
        actual = u.normalize("NFD", text)
        print("SANITY:", repr(text), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    def eligible(x, y):
        return (
            u.category(x) == "Cn"
            and u.combining(x) == 0
            and u.decomposition(x) == ""
            and 0 < u.combining(y) < ud.combining(x)
            and u.decomposition(y) == ""
        )

    def check(x, y):
        nonlocal tested
        if not eligible(x, y):
            return False
        text = "a" + x + y
        expected = reference_nfd(text)
        assert expected == text
        tested += 1
        actual = u.normalize("NFD", text)
        if actual != expected:
            repeated = u.normalize("NFD", text)
            if repeated == actual:
                print(
                    "COUNTEREXAMPLE:", repr(text),
                    "actual =", repr(actual),
                    "expected =", repr(expected),
                )
                return True
        return False

    for x, y in (
        ("\u1ab0", "\u0316"),
        ("\u1ab0", "\u0323"),
        ("\u1ab0", "\u0334"),
        ("\u1dc0", "\u0316"),
        ("\u1dc1", "\u0323"),
        ("\u1ab4", "\u0334"),
    ):
        if time.monotonic() >= deadline:
            break
        if check(x, y):
            return

    xs = []
    ys_by_class = {}
    for cp in range(0x110000):
        if time.monotonic() >= deadline:
            break
        ch = chr(cp)
        old_ccc = u.combining(ch)
        if old_ccc > 0 and u.decomposition(ch) == "":
            ys_by_class.setdefault(old_ccc, []).append(ch)
        if (
            u.category(ch) == "Cn"
            and old_ccc == 0
            and ud.combining(ch) > 0
            and u.decomposition(ch) == ""
        ):
            xs.append(ch)

    choices = [
        (x, [
            y
            for ccc, characters in ys_by_class.items()
            if ccc < ud.combining(x)
            for y in characters
        ])
        for x in xs
    ]
    choices = [(x, ys) for x, ys in choices if ys]
    rng = random.Random(0x32C0FFEE)

    for _ in range(100000):
        if not choices or time.monotonic() >= deadline:
            break
        x, ys = rng.choice(choices)
        if check(x, rng.choice(ys)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()