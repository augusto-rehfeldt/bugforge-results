import random
import time
from decimal import Decimal
from datetime import timedelta

from isodate import Duration, duration_isoformat, parse_duration


def reference_months(years, months):
    return 12 * years + months


def check(years, months):
    expected = reference_months(years, months)
    try:
        text = duration_isoformat(Duration(years=years, months=months))
        try:
            parsed = parse_duration(text)
        except Exception as exc:
            return False, {
                "formatted": text,
                "parse_error": (type(exc).__name__, str(exc)),
            }, expected

        if isinstance(parsed, Duration):
            actual_months = Decimal(parsed.years) * 12 + Decimal(parsed.months)
            valid = actual_months == expected and parsed.tdelta == timedelta(0)
        else:
            actual_months = None
            valid = False

        return valid, {
            "formatted": text,
            "parsed_calendar_months": actual_months,
            "parsed": repr(parsed),
        }, expected
    except Exception as exc:
        return False, {
            "error": (type(exc).__name__, str(exc)),
        }, expected


def main():
    for years, months in ((1, 0), (0, 11)):
        ok, actual, expected = check(years, months)
        print(
            "SANITY:",
            repr({"years": years, "months": months}),
            "actual =", repr(actual),
            "expected_calendar_months =", expected,
            "PASS" if ok else "FAIL",
        )
        if not ok:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0
    rng = random.Random(20260717)
    edges = [
        (1, 1), (1, 11), (1, 6),
        (2, 1), (2, 11),
        (99, 1), (99, 11),
        (100, 1), (100, 11),
    ]

    for index in range(10000):
        if time.monotonic() - start >= 175:
            break
        if index < len(edges):
            years, magnitude = edges[index]
        else:
            years = rng.randint(1, 100)
            magnitude = rng.randint(1, 11)

        months = -magnitude
        ok, actual, expected = check(years, months)
        tested += 1
        if not ok:
            confirmed_ok, confirmed_actual, confirmed_expected = check(years, months)
            if not confirmed_ok:
                print("COUNTEREXAMPLE:")
                print(repr({"years": years, "months": months}))
                print("actual =", repr(confirmed_actual))
                print("expected =", repr({
                    "calendar_months": confirmed_expected,
                    "canonical_iso": "P%dM" % confirmed_expected,
                }))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()