import math
import random
import time
from decimal import Decimal, localcontext


def reference(seed, low, high):
    """Symmetric triangular inverse CDF, without floating-point overflow."""
    u = Decimal.from_float(random.Random(seed).random())
    with localcontext() as ctx:
        ctx.prec = 100
        lo = Decimal.from_float(low)
        hi = Decimal.from_float(high)
        width = hi - lo
        if u <= Decimal("0.5"):
            value = lo + width * (u / 2).sqrt()
        else:
            value = hi - width * ((1 - u) / 2).sqrt()
        return float(value)


def observe(seed, low, high):
    try:
        return ("value", random.Random(seed).triangular(low, high))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def violates(result, low, high):
    return result[0] != "value" or not (low <= result[1] <= high)


def main():
    deadline = time.monotonic() + 175.0

    for seed, low, high in [(0, 0.0, 1.0), (1, -3.0, 7.0)]:
        expected = reference(seed, low, high)
        result = observe(seed, low, high)
        agrees = (
            result[0] == "value"
            and math.isclose(result[1], expected, rel_tol=1e-14, abs_tol=1e-14)
        )
        print("SANITY:", repr((seed, low, high, None)),
              "actual=", repr(result), "expected=", repr(expected),
              "agrees=", agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    tested = 0

    def check(seed, low, high):
        nonlocal tested
        assert math.isfinite(low) and math.isfinite(high) and low < high
        tested += 1
        result = observe(seed, low, high)
        if not violates(result, low, high):
            return False

        repeated = observe(seed, low, high)
        if repr(result) != repr(repeated) or not violates(repeated, low, high):
            return False

        expected = {
            "reference_sample": reference(seed, low, high),
            "required_interval": (low, high),
        }
        actual = result[1] if result[0] == "value" else result
        print("COUNTEREXAMPLE:", repr((seed, low, high, None)),
              "actual=", repr(actual), "expected=", repr(expected))
        return True

    edges = [
        (-1e308, 1e308),
        (-float.fromhex("0x1.fffffffffffffp+1023"),
         float.fromhex("0x1.fffffffffffffp+1023")),
        (-1.7e308, 1e308),
        (-1e308, 1.7e308),
    ]
    for low, high in edges:
        for seed in range(16):
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check(seed, low, high):
                return

    generator = random.Random(8675309)
    while time.monotonic() < deadline:
        low = -math.ldexp(generator.uniform(0.5, 1.0), 1024)
        high = math.ldexp(generator.uniform(0.5, 1.0), 1024)
        seed = generator.randrange(32)
        if check(seed, low, high):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()