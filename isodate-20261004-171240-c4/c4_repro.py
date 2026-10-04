from decimal import Decimal
from isodate import Duration, duration_isoformat, parse_duration

inp = {"years": 1, "months": -1}
try:
    d = Duration(**inp)
    months = 12 * inp["years"] + inp["months"]
    expected = Duration(months=months)
    if not (months > 0 and d == expected):
        print("REFUTATION REJECTED:", "input is not the claimed positive calendar duration")
    else:
        text = duration_isoformat(d)
        try:
            parsed = parse_duration(text)
            actual = {
                "formatted": text,
                "calendar_months": 12 * getattr(parsed, "years", Decimal(0))
                + getattr(parsed, "months", Decimal(0)),
            }
            broken = parsed != expected
        except Exception as e:
            actual = {"formatted": text, "parse_error": str(e)}
            broken = True
        if broken:
            print("REFUTATION CONFIRMED:", inp, "actual =", actual,
                  "expected =", {"calendar_months": months})
        else:
            print("REFUTATION REJECTED:", "formatted duration has the expected value")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))