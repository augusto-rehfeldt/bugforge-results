import random
import time
import tabulate


def reference(rows):
    # The documented property concerns separation, not numeric rendering.
    return {
        "returns_string": True,
        "separated_labels": [label for _, label in rows],
    }


def observe(rows):
    try:
        result = tabulate.tabulate(
            rows, tablefmt=tabulate.simple_separated_format("|")
        )
    except Exception as exc:
        return {
            "exception": type(exc).__name__,
            "message": str(exc),
        }, None

    if not isinstance(result, str):
        return {"returns_string": False}, result

    labels = []
    for line in result.splitlines():
        parts = line.split("|")
        if len(parts) != 2 or not parts[0].strip():
            return {
                "returns_string": True,
                "invalid_separation": True,
            }, result
        labels.append(parts[1].strip())

    return {
        "returns_string": True,
        "separated_labels": labels,
    }, result


def main():
    started = time.monotonic()
    deadline = started + 175
    tested = 0

    for n in (12, -7):
        rows = [[n, "large"], [1.5, "small"]]
        expected = reference(rows)
        observed, actual = observe(rows)
        tested += 1
        if observed != expected:
            print("SANITY FAILED")
            print("Input:", repr(rows))
            print("Actual:", repr(actual if actual is not None else observed))
            print("Expected:", repr(expected))
            return
        print("SANITY OK:", repr(rows), repr(actual), flush=True)

    def check(n):
        nonlocal tested
        rows = [[n, "large"], [1.5, "small"]]
        expected = reference(rows)
        observed, actual = observe(rows)
        tested += 1
        if observed == expected:
            return False

        repeated, repeated_actual = observe(rows)
        if repeated == expected:
            return False

        print("COUNTEREXAMPLE:")
        print(repr(rows))
        print("Actual:", repr(
            repeated_actual if repeated_actual is not None else repeated
        ))
        print("Expected:", repr(expected))
        return True

    # All integers below have at most 1000 decimal digits.
    edges = [
        10**308,
        10**309,
        10**999,
        10**1000 - 1,
        int(float.fromhex("0x1.fffffffffffffp+1023")),
    ]
    for magnitude in edges:
        for delta in (0, -1, 1):
            value = magnitude + delta
            if value >= 10**1000:
                continue
            for sign in (1, -1):
                if time.monotonic() >= deadline:
                    print("NO COUNTEREXAMPLE", tested)
                    return
                if check(sign * value):
                    return

    rng = random.Random(20250308)
    while time.monotonic() < deadline:
        digits = rng.choice((308, 309, 310, 999, 1000, rng.randint(308, 1000)))
        magnitude = rng.randrange(10**(digits - 1), 10**digits)
        if check(rng.choice((-1, 1)) * magnitude):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()