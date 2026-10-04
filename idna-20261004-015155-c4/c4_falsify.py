import random
import time
import unicodedata
import idna


def reference(domain):
    trailing_dot = domain.endswith(".")
    labels = domain[:-1].split(".") if trailing_dot else domain.split(".")
    classes = [[unicodedata.bidirectional(c) for c in label] for label in labels]

    # RFC 5893 applies to every label when any label contains R, AL, or AN.
    bidi_domain = any(c in {"R", "AL", "AN"} for cs in classes for c in cs)
    if bidi_domain:
        for cs in classes:
            if not cs or cs[0] not in {"L", "R", "AL"}:
                return ("error", "IDNABidiError")
            rtl = cs[0] in {"R", "AL"}
            allowed = (
                {"R", "AL", "AN", "EN", "ES", "CS", "ET", "ON", "BN", "NSM"}
                if rtl else
                {"L", "EN", "ES", "CS", "ET", "ON", "BN", "NSM"}
            )
            if any(c not in allowed for c in cs):
                return ("error", "IDNABidiError")
            ending = next((c for c in reversed(cs) if c != "NSM"), None)
            if ending not in ({"R", "AL", "EN", "AN"} if rtl else {"L", "EN"}):
                return ("error", "IDNABidiError")
            if rtl and "EN" in cs and "AN" in cs:
                return ("error", "IDNABidiError")

    # All inputs here contain only lowercase ASCII, digits, or Hebrew letters.
    encoded = [
        label.encode("ascii") if label.isascii()
        else b"xn--" + label.encode("punycode")
        for label in labels
    ]
    return ("result", b".".join(encoded) + (b"." if trailing_dot else b""))


def actual(domain):
    try:
        return ("result", idna.encode(domain))
    except Exception as exc:
        return ("error", type(exc).__name__)


def main():
    deadline = time.monotonic() + 175
    for domain in ("example.com", "\u05d0"):
        expected = reference(domain)
        observed = actual(domain)
        print("SANITY:", repr(domain), "actual =", repr(observed),
              "expected =", repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(domain):
        nonlocal tested
        expected = reference(domain)
        observed = actual(domain)
        tested += 1
        if observed != expected:
            repeated = actual(domain)
            if repeated == observed:
                print("COUNTEREXAMPLE:", repr(domain),
                      "actual =", repr(observed),
                      "expected =", repr(expected))
                return True
        return False

    hand_picked = ["0.\u05d0", "123.\u05d0"]
    for digits in ("0", "123", "9" * 63, "0" * 63, "0123456789"):
        for hebrew in ("\u05d0", "\u05ea", "\u05d0" * 10):
            for domain in (digits + "." + hebrew, hebrew + "." + digits):
                hand_picked.extend((domain, domain + "."))

    for domain in hand_picked:
        if check(domain):
            return

    rng = random.Random(5893)
    letters = "".join(chr(c) for c in range(0x05D0, 0x05EB))
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        digits = "".join(rng.choice("0123456789")
                         for _ in range(rng.randint(1, 63)))
        hebrew = "".join(rng.choice(letters)
                         for _ in range(rng.randint(1, 10)))
        labels = [digits, hebrew]
        if rng.randrange(2):
            labels.reverse()
        domain = ".".join(labels) + ("." if rng.randrange(2) else "")
        if check(domain):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()