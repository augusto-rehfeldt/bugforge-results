import ipaddress
import random
import time


def reference_add_zero(literal):
    # Adding zero preserves both the address and its significant scope ID.
    return ipaddress.IPv6Address(literal)


def observe(literal):
    expected = reference_add_zero(literal)
    actual = ipaddress.IPv6Address(literal) + 0
    return actual, expected


def main():
    for literal, increment, expected_literal in (
        ("::1", 0, "::1"),
        ("2001:db8::1", 1, "2001:db8::2"),
    ):
        actual = ipaddress.IPv6Address(literal) + increment
        expected = ipaddress.IPv6Address(expected_literal)
        ok = actual == expected
        print("SANITY:", repr(literal), increment, str(actual),
              str(expected), "OK" if ok else "FAILED")
        if not ok:
            print("SANITY FAILED")
            return

    rng = random.Random(20250308)
    deadline = time.monotonic() + 180
    tested = 0

    edges = [
        "fe80::1%eth0",
        "fe80::1%1",
        "::%zone",
        "::1%lo",
        "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff%edge",
        "::ffff:192.0.2.1%eth0",
        "2001:db8::%0",
    ]

    def inputs():
        yield from edges
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"
        while time.monotonic() < deadline:
            value = rng.getrandbits(128)
            # Eight hexadecimal groups are valid without relying on formatting
            # from the module under test.
            address = ":".join(
                format((value >> shift) & 0xffff, "x")
                for shift in range(112, -1, -16)
            )
            scope = "".join(
                rng.choice(alphabet) for _ in range(rng.randint(1, 32))
            )
            yield address + "%" + scope

    for literal in inputs():
        actual, expected = observe(literal)
        tested += 1
        if actual != expected:
            # Reconstruct both operands and repeat the failing operation.
            repeated_actual, repeated_expected = observe(literal)
            if repeated_actual != repeated_expected:
                print(
                    "COUNTEREXAMPLE:", repr(literal),
                    "actual =", repr(repeated_actual),
                    "expected =", repr(repeated_expected),
                )
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()