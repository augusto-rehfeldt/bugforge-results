import ipaddress
import random
import time


def reference(prefix, new_prefix):
    if new_prefix > prefix:
        return ("exception", "ValueError")
    return ("result", f"0.0.0.0/{new_prefix}")


def actual(prefix, new_prefix):
    try:
        result = ipaddress.IPv4Network(
            f"0.0.0.0/{prefix}"
        ).supernet(new_prefix=new_prefix)
        return ("result", str(result))
    except Exception as exc:
        return ("exception", type(exc).__name__)


def main():
    for prefix, new_prefix in [(24, 23), (24, 25)]:
        expected = reference(prefix, new_prefix)
        observed = actual(prefix, new_prefix)
        print(
            "SANITY:",
            repr((prefix, new_prefix)),
            "actual=",
            repr(observed),
            "expected=",
            repr(expected),
        )
        if observed != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    rng = random.Random(20240519)
    tested = 0
    edges = [1, 32] + list(range(2, 32))

    def check(p):
        nonlocal tested
        expected = reference(0, p)
        observed = actual(0, p)
        tested += 1
        if observed != expected:
            repeated = actual(0, p)
            if repeated == observed:
                case = {
                    "network": "0.0.0.0/0",
                    "new_prefix": p,
                }
                print(
                    "COUNTEREXAMPLE:",
                    repr(case),
                    "actual=",
                    repr(observed),
                    "expected=",
                    repr(expected),
                )
                return True
        return False

    for p in edges:
        if check(p):
            return

    for _ in range(10000):
        if time.monotonic() >= deadline:
            break
        if check(rng.randint(1, 32)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()