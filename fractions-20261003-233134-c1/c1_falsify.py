import fractions
import random
import sys
import time

def main():
    if sys.get_int_max_str_digits() == 0:
        sys.set_int_max_str_digits(sys.int_info.default_max_str_digits)
    limit = sys.get_int_max_str_digits()
    deadline = time.monotonic() + 175.0
    tested = 0

    def reference(n, d):
        # These inputs are in [1, 10), so their scientific exponent is zero.
        q, r = divmod(n * 100, d)
        if 2 * r > d or (2 * r == d and q % 2):
            q += 1
        whole, decimal = divmod(q, 100)
        return f"{whole}.{decimal:02d}e+00"

    def actual(x):
        try:
            return format(x, ".2e")
        except Exception as exc:
            return ("exception", type(exc).__name__, str(exc))

    for k in (3, 4):
        d = 10 ** k
        x = fractions.Fraction(d + 1, d)
        expected = reference(d + 1, d)
        result = actual(x)
        tested += 1
        print("SANITY:", repr(k), repr(result), repr(expected))
        if result != expected:
            print("SANITY FAILED")
            return

    def check(k):
        nonlocal tested
        d = 10 ** k
        n = d + 1
        x = fractions.Fraction(n, d)
        expected = reference(n, d)
        result = actual(x)
        tested += 1
        if result != expected:
            repeated = actual(x)
            if repeated != expected:
                print(
                    "COUNTEREXAMPLE:",
                    repr({
                        "k": k,
                        "int_max_str_digits": limit,
                        "format": ".2e",
                    }),
                    "actual=", repr(repeated),
                    "expected=", repr(expected),
                )
                return True
        return False

    edges = [
        limit - 2, limit - 1, limit, limit + 1, limit + 2,
        limit + 10, 2 * limit, 3, 5, 10,
    ]
    for k in dict.fromkeys(max(3, k) for k in edges):
        if time.monotonic() >= deadline:
            break
        if check(k):
            return

    rng = random.Random(20260719)
    while time.monotonic() < deadline:
        if rng.randrange(2):
            k = max(3, limit + rng.randint(-64, 64))
        else:
            k = rng.randint(max(3, limit // 2), 2 * limit + 64)
        if check(k):
            return

    print("NO COUNTEREXAMPLE", tested)

if __name__ == "__main__":
    main()