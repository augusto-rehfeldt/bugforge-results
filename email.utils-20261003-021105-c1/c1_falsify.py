import random
import string
import time
from email.utils import formataddr, parseaddr


def reference(pair):
    # The documented inverse property requires exact recovery of the pair.
    return pair


def evaluate(pair):
    try:
        return parseaddr(formataddr(pair))
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    for pair in [
        ("Alice", "alice@example.com"),
        ("Bob", '"a b"@example.com'),
    ]:
        expected = reference(pair)
        actual = evaluate(pair)
        print("SANITY:", repr(pair), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(20250308)
    deadline = time.monotonic() + 175
    tested = 0

    edge_cases = [
        ("Alice", '"a[b"@example.com'),
        ("A", '"[a"@example.com'),
        ("Bob", '"a["@example.com'),
        ("Carol", '"a[[b"@example.com'),
        ("Dave", '"a[b[c"@example.com'),
        ("Eve", '"[abc["@example.com'),
    ]

    def cases():
        yield from edge_cases
        while time.monotonic() < deadline:
            name = "".join(rng.choice(string.ascii_letters)
                           for _ in range(rng.randint(1, 24)))
            local = [rng.choice(string.ascii_letters)
                     for _ in range(rng.randint(1, 48))]
            for _ in range(rng.randint(1, 6)):
                local.insert(rng.randrange(len(local) + 1), "[")
            yield (name, '"' + "".join(local) + '"@example.com')

    for pair in cases():
        if time.monotonic() >= deadline:
            break
        tested += 1
        expected = reference(pair)
        actual = evaluate(pair)
        if actual != expected:
            repeated = evaluate(pair)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(pair),
                      "actual:", repr(actual), "expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()