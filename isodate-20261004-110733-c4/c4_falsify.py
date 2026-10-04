import random
import time
from decimal import Decimal
import isodate


def reference_years(value):
    """Render a nonnegative Decimal exactly, without exponent notation."""
    sign, digits, exponent = value.as_tuple()
    assert not sign and value.is_finite()
    text = "".join(str(digit) for digit in digits)
    if exponent >= 0:
        text += "0" * exponent
    else:
        point = len(text) + exponent
        if point <= 0:
            text = "0." + "0" * (-point) + text
        else:
            text = text[:point] + "." + text[point:]
        text = text.rstrip("0").rstrip(".")
    return "P" + text + "Y"


def actual_for(years):
    try:
        return isodate.duration_isoformat(isodate.Duration(years=years))
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175
    sanity_ok = True
    for years in (Decimal(1), Decimal("0.5")):
        expected = reference_years(years)
        actual = actual_for(years)
        print("SANITY:", repr({"years": str(years)}),
              "actual:", repr(actual), "expected:", repr(expected))
        sanity_ok = sanity_ok and actual == expected

    if not sanity_ok:
        print("SANITY FAILED")
        return

    tested = 0

    def check(n):
        nonlocal tested
        years = Decimal(10) ** -n
        expected = "P0." + "0" * (n - 1) + "1Y"
        actual = actual_for(years)
        tested += 1
        if actual != expected:
            repeated = actual_for(years)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr({"n": n, "years": str(years)}))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    # Boundary control, exponent transition, and smallest allowed value first.
    for n in (6, 7, 20, 8, 19, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18):
        if check(n):
            return

    rng = random.Random(1729)
    for _ in range(10000):
        if time.monotonic() >= deadline:
            break
        if check(rng.randint(7, 20)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()