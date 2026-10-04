import random
import time
import unicodedata

import idna
from idna import idnadata


# Unicode 17.0 Beria Erfe lowercase letters:
# U+16EBB..U+16ED3 all have General_Category=Ll, Bidi_Class=L,
# CCC=0, and no decomposition mapping. Each singleton is NFC-stable.
# For a singleton L label, RFC 5893's LTR start/end rules hold, and
# there are no forbidden bidi classes or conflicting number types.
def unicode17_reference(ch):
    cp = ord(ch)
    if ch in ("a", "z") or 0x16EBB <= cp <= 0x16ED3:
        return None
    raise ValueError("Outside the independently specified reference domain")


# Decode the installed IDNA PVALID table directly, without invoking
# check_label or any of its validation helpers.
def is_pvalid(cp):
    for packed in idnadata.codepoint_classes["PVALID"]:
        start = packed >> 32
        stop = packed & 0xFFFFFFFF
        if start <= cp < stop:
            return True
    return False


def observe(label):
    try:
        return ("return", idna.check_label(label))
    except Exception as exc:
        return ("raise", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175.0

    for label in ("a", "z"):
        expected = ("return", unicode17_reference(label))
        actual = observe(label)
        print("SANITY:", repr(label), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    candidates = [
        chr(cp) for cp in range(0x16EBB, 0x16ED4)
        if is_pvalid(cp)
    ]
    tested = 0

    def test(label):
        nonlocal tested
        expected = ("return", unicode17_reference(label))
        actual = observe(label)
        tested += 1
        if actual != expected:
            repeated = observe(label)
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr(label),
                      "actual:", repr(repeated), "expected:", repr(expected))
                return True
        return False

    # Hand-picked boundary and interior cases first, emphasizing missing
    # host bidi data. Host Unicode data is never used as the reference.
    hand_picked = [chr(cp) for cp in (0x16EBB, 0x16ED3, 0x16EBC, 0x16EC7)]
    ordered = []
    for label in hand_picked + sorted(
        candidates,
        key=lambda ch: (unicodedata.bidirectional(ch) != "", ord(ch))
    ):
        if label in candidates and label not in ordered:
            ordered.append(label)

    for label in ordered:
        if time.monotonic() >= deadline:
            break
        if test(label):
            return

    rng = random.Random(170016)
    if candidates:
        for _ in range(100000):
            if time.monotonic() >= deadline:
                break
            if test(rng.choice(candidates)):
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()