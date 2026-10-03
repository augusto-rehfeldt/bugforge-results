import ipaddress
import random
import time


def reference(address, prefix):
    # Apply the documented network definition to independently constructed
    # endpoints. Never call IPv6Network.is_global here.
    host_bits = 128 - prefix
    first = (address >> host_bits) << host_bits
    last = first + (1 << host_bits) - 1
    return (
        ipaddress.IPv6Address(first).is_global
        and ipaddress.IPv6Address(last).is_global
    )


def main():
    deadline = time.monotonic() + 170.0
    tested = 0

    for text in ("2606:4700::/32", "fc00::/7"):
        network = ipaddress.IPv6Network(text, strict=True)
        expected = reference(int(network.network_address), network.prefixlen)
        actual = network.is_global
        tested += 1
        print("SANITY:", repr(text), "actual=", actual, "expected=", expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    def check(address, prefix):
        nonlocal tested
        host_bits = 128 - prefix
        base = (address >> host_bits) << host_bits
        text = str(ipaddress.IPv6Address(base)) + "/" + str(prefix)
        network = ipaddress.IPv6Network(text, strict=True)
        expected = reference(base, prefix)
        actual = network.is_global
        tested += 1
        if actual != expected:
            repeated = ipaddress.IPv6Network(text, strict=True).is_global
            repeated_expected = reference(base, prefix)
            if repeated == actual and repeated_expected == expected:
                print(
                    "COUNTEREXAMPLE:",
                    repr(text),
                    "actual=", actual,
                    "expected=", expected,
                )
                return True
        return False

    edges = [
        ("2000::", 3),
        ("::", 0),
        ("::", 128),
        ("::1", 128),
        ("2001::", 23),
        ("2001:db8::", 32),
        ("3fff::", 20),
        ("3ffe:ffff:ffff:ffff:ffff:ffff:ffff:ffff", 128),
        ("3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff", 128),
        ("4000::", 2),
        ("fc00::", 7),
        ("fe80::", 10),
        ("ff00::", 8),
        ("::ffff:192.0.2.1", 128),
    ]

    anchors = [
        int(ipaddress.IPv6Address(text))
        for text in (
            "::", "::1", "2000::", "2001::", "2001:db8::",
            "3fff::", "4000::", "fc00::", "fe80::", "ff00::",
        )
    ]

    for text, prefix in edges:
        if check(int(ipaddress.IPv6Address(text)), prefix):
            return

    # Exercise every prefix length around classification boundaries.
    for prefix in range(129):
        for anchor in anchors:
            for delta in (-1, 0, 1):
                if time.monotonic() >= deadline:
                    print("NO COUNTEREXAMPLE", tested)
                    return
                address = (anchor + delta) % (1 << 128)
                if check(address, prefix):
                    return

    rng = random.Random(0x6E74776F726B)
    for _ in range(200000):
        if time.monotonic() >= deadline:
            break
        prefix = rng.randrange(129)
        if rng.randrange(2):
            address = rng.getrandbits(128)
        else:
            anchor = rng.choice(anchors)
            offset = rng.getrandbits(rng.randrange(129))
            address = (anchor + rng.choice((-1, 1)) * offset) % (1 << 128)
        if check(address, prefix):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()