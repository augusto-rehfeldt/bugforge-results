import random
import time
import unicodedata

u = unicodedata.ucd_3_2_0
deadline = time.monotonic() + 175.0
tested = 0


def reference_nfd(text):
    """Unicode 3.2 canonical decomposition and canonical ordering."""
    def decompose(ch):
        cp = ord(ch)
        if 0xAC00 <= cp < 0xAC00 + 11172:
            index = cp - 0xAC00
            result = [
                chr(0x1100 + index // 588),
                chr(0x1161 + (index % 588) // 28),
            ]
            trailing = index % 28
            if trailing:
                result.append(chr(0x11A7 + trailing))
            return result
        mapping = u.decomposition(ch)
        if not mapping or mapping.startswith("<"):
            return [ch]
        result = []
        for part in mapping.split():
            result.extend(decompose(chr(int(part, 16))))
        return result

    ordered = []
    for ch in text:
        for item in decompose(ch):
            cls = u.combining(item)
            ordered.append(item)
            if cls:
                pos = len(ordered) - 1
                while pos > 0 and u.combining(ordered[pos - 1]) > cls:
                    ordered[pos], ordered[pos - 1] = (
                        ordered[pos - 1], ordered[pos]
                    )
                    pos -= 1
    return "".join(ordered)


def expected(text):
    return reference_nfd(text) == text


for text in ("A\u0315", "\u00C5"):
    want = expected(text)
    actual = u.is_normalized("NFD", text)
    print("SANITY:", repr(text), actual, want)
    if actual != want:
        print("SANITY FAILED")
        raise SystemExit(0)


def eligible(cp):
    ch = chr(cp)
    return (
        u.category(ch) == "Cn"
        and u.combining(ch) == 0
        and unicodedata.combining(ch) > 0
    )


def check(cp):
    global tested
    text = "A\u0315" + chr(cp)
    want = expected(text)
    actual = u.is_normalized("NFD", text)
    tested += 1
    if actual != want:
        repeated = u.is_normalized("NFD", text)
        if repeated != want:
            print("COUNTEREXAMPLE:", repr(text), repeated, want)
            raise SystemExit(0)


# Try the requested starting point and other post-3.2 combining marks first.
hand_picked = (0x1AB0, 0x1AB1, 0x1DC0, 0x1DC1, 0x0350, 0x0353,
               0x035C, 0x1DCE, 0xA66F, 0xFE24)
for cp in hand_picked:
    if time.monotonic() >= deadline:
        break
    if eligible(cp):
        check(cp)

# Enumerate all qualifying marks, prioritizing classes that could reorder.
candidates = []
for cp in range(0x110000):
    if time.monotonic() >= deadline:
        break
    if eligible(cp):
        candidates.append(cp)

candidates.sort(
    key=lambda cp: (unicodedata.combining(chr(cp)) >= 232,
                    unicodedata.combining(chr(cp)), cp)
)
for cp in candidates:
    if time.monotonic() >= deadline:
        break
    check(cp)

# Fixed-seed randomized sampling from the valid candidate input space.
rng = random.Random(0x32AB0)
if candidates:
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        check(rng.choice(candidates))

print("NO COUNTEREXAMPLE", tested)