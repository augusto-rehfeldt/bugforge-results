import ipaddress
import random
import time


def reference(address):
    # Construct the documented address independently of IPv6Interface.ip.
    return ipaddress.IPv6Address(address)


def agrees(actual, expected):
    return actual == expected and actual.scope_id == expected.scope_id


def check(address, prefix):
    text = f"{address}/{prefix}"
    expected = reference(address)
    actual = ipaddress.IPv6Interface(text).ip
    if not agrees(actual, expected):
        # Independently reconstruct both sides to confirm the failure.
        expected = reference(address)
        actual = ipaddress.IPv6Interface(text).ip
        if not agrees(actual, expected):
            print(
                "COUNTEREXAMPLE:",
                repr(text),
                "actual:",
                repr(actual),
                "expected:",
                repr(expected),
            )
            return False
    return True


def main():
    for address, prefix in [("::1", 128), ("2001:db8::1234", 64)]:
        actual = ipaddress.IPv6Interface(f"{address}/{prefix}").ip
        expected = reference(address)
        ok = agrees(actual, expected)
        print(
            "SANITY:",
            repr(f"{address}/{prefix}"),
            "actual:",
            repr(actual),
            "expected:",
            repr(expected),
            "PASS" if ok else "FAIL",
        )
        if not ok:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    count = 0

    for address in [
        "fe80::1%eth0",
        "fe80::abcd%3",
        "::1%zone",
        "::%zone",
        "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff%eth0",
    ]:
        for prefix in (0, 64, 127, 128):
            count += 1
            if not check(address, prefix):
                return

    rng = random.Random(20250308)
    while time.monotonic() < deadline:
        base = str(ipaddress.IPv6Address(rng.getrandbits(128)))
        scope = rng.choice(
            ["eth0", "3", "zone", f"zone{rng.randrange(1000000)}"]
        )
        address = f"{base}%{scope}"
        prefix = rng.choice([0, 64, 127, 128, rng.randrange(129)])
        count += 1
        if not check(address, prefix):
            return

    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()