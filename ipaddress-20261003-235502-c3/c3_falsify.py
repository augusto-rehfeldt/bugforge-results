import ipaddress
import random
import string
import time


def merge_intervals(intervals):
    merged = []
    for lo, hi in sorted(intervals):
        if merged and lo <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def reference(parent_start, parent_prefix, child_start, child_prefix):
    parent_end = parent_start + (1 << (128 - parent_prefix)) - 1
    child_end = child_start + (1 << (128 - child_prefix)) - 1
    assert parent_start <= child_start <= child_end <= parent_end
    return [
        (lo, hi)
        for lo, hi in (
            (parent_start, child_start - 1),
            (child_end + 1, parent_end),
        )
        if lo <= hi
    ]


def check(parent_text, child_text, expected):
    try:
        parent = ipaddress.IPv6Network(parent_text)
        child = ipaddress.IPv6Network(child_text)
        result = list(parent.address_exclude(child))
        intervals = [
            (
                int(net.network_address),
                int(net.network_address) + (1 << (128 - net.prefixlen)) - 1,
            )
            for net in result
        ]
        coverage = merge_intervals(intervals)
        actual = {
            "networks": [str(net) for net in result],
            "coverage": coverage,
        }
        return coverage == expected, actual
    except Exception as exc:
        return False, {
            "exception": type(exc).__name__,
            "message": str(exc),
        }


def main():
    base = int("fe80" + "0" * 28, 16)

    sanity_cases = [
        ("fe80::/126", "fe80::/128", base, 128),
        ("fe80::/126", "fe80::2/127", base + 2, 127),
    ]
    for index, (parent, child, child_start, child_prefix) in enumerate(
        sanity_cases, 1
    ):
        expected = reference(base, 126, child_start, child_prefix)
        ok, actual = check(parent, child, expected)
        print("SANITY", index, repr(actual), "expected =", repr(expected))
        if not ok:
            print("SANITY FAILED")
            return

    expected = reference(base, 126, base, 128)
    rng = random.Random(20250308)
    alphabet = string.ascii_letters
    hand_picked = [
        "a", "eth", "A", "z", "Z", "ethA", "ETH",
        "a" * 64, "Z" * 256, alphabet,
    ]
    deadline = time.monotonic() + 175
    tested = 0
    index = 0

    while time.monotonic() < deadline:
        if index < len(hand_picked):
            zone = hand_picked[index]
        else:
            length = rng.choice([1, 2, 3, 4, 8, 16, 64, 256, 1024])
            zone = "".join(rng.choice(alphabet) for _ in range(length))
        index += 1

        inputs = ("fe80::%" + zone + "/126", "fe80::%" + zone + "/128")
        ok, actual = check(*inputs, expected)
        tested += 1
        if not ok:
            confirmed_ok, confirmed_actual = check(*inputs, expected)
            if not confirmed_ok:
                print(
                    "COUNTEREXAMPLE:", repr(inputs),
                    "actual =", repr(confirmed_actual),
                    "expected =", repr(expected),
                )
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()