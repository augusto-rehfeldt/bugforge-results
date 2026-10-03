import ipaddress
import random
import string
import time


def reference(text):
    address, separator, scope = text.partition("%")
    if "::" in address:
        left, right = address.split("::")
        left = left.split(":") if left else []
        right = right.split(":") if right else []
        words = left + ["0"] * (8 - len(left) - len(right)) + right
    else:
        words = address.split(":")
    assert len(words) == 8
    result = ":".join(format(int(word, 16), "04x") for word in words)
    return result + (separator + scope if separator else "")


def observe(address):
    try:
        return ("result", address.exploded)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    for text in ("fe80::1", "2001:db8::abcd"):
        expected = reference(text)
        actual = observe(ipaddress.IPv6Address(text))
        print("SANITY:", repr(text), "actual =", repr(actual),
              "expected =", repr(expected))
        if actual != ("result", expected):
            print("SANITY FAILED")
            return

    rng = random.Random(1729)
    deadline = time.monotonic() + 175
    tested = 0
    edges = [
        "a", "eth", "Ethernet", "A", "z", "Z",
        "a" * 16, "Z" * 16, "abcdefghijklmnop",
        "ABCDEFGHIJKLMNOP", "aZ" * 8,
    ]

    def scopes():
        yield from edges
        while time.monotonic() < deadline:
            yield "".join(
                rng.choice(string.ascii_letters)
                for _ in range(rng.randint(1, 16))
            )

    for scope in scopes():
        if time.monotonic() >= deadline:
            break
        text = "fe80::1%" + scope
        try:
            address = ipaddress.IPv6Address(text)
        except ValueError:
            continue

        tested += 1
        expected = reference(text)
        actual = observe(address)
        if actual != ("result", expected):
            # Reconstruct and repeat the exact failing input.
            repeated = observe(ipaddress.IPv6Address(text))
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(text),
                      "actual =", repr(actual),
                      "expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()