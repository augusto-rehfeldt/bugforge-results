import ipaddress
import random
import string
import time

ADDRESS = int("fe800000000000000000000000000001", 16)


def reference(zone, prefix):
    return (ADDRESS, zone, prefix)


def observe(text):
    try:
        original = ipaddress.IPv6Interface(text)
        rendered = original.with_prefixlen
        rebuilt = ipaddress.IPv6Interface(rendered)
        return {
            "with_prefixlen": rendered,
            "roundtrip": (int(rebuilt.ip), rebuilt.scope_id,
                          rebuilt.network.prefixlen),
            "equal": rebuilt == original,
        }
    except Exception as exc:
        return {"exception": (type(exc).__name__, str(exc))}


def matches(actual, expected):
    return actual.get("roundtrip") == expected and actual.get("equal") is True


def main():
    # Independent reference: fixed address value, parsed scope, and exact prefix.
    for prefix in (64, 128):
        text = "fe80::1/" + str(prefix)
        expected = reference(None, prefix)
        actual = observe(text)
        print("SANITY:", repr(text), "actual:", repr(actual),
              "expected:", repr(expected))
        if not matches(actual, expected):
            print("SANITY FAILED")
            return

    rng = random.Random(1729)
    deadline = time.monotonic() + 170
    count = 0

    def inputs():
        for zone in ("eth", "a", "Ethernet", "Z"):
            for prefix in (0, 64, 128, 1, 127):
                yield zone, prefix
        for _ in range(100000):
            zone = "".join(rng.choice(string.ascii_letters)
                           for _ in range(rng.randint(1, 64)))
            yield zone, rng.randint(0, 128)

    for zone, prefix in inputs():
        if time.monotonic() >= deadline:
            break
        text = "fe80::1%" + zone + "/" + str(prefix)
        expected = reference(zone, prefix)
        actual = observe(text)
        count += 1
        if not matches(actual, expected):
            repeated = observe(text)
            if repeated == actual and not matches(repeated, expected):
                print("COUNTEREXAMPLE:", repr(text),
                      "actual:", repr(repeated), "expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()