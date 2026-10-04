*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `isodate`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `isodate` 0.7.2

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Mixed-sign calendar components produce an invalid ISO 8601 duration

Target: `isodate.duration_isoformat`

Property: For integers y in 1..100 and m in 1..11, let d = Duration(years=y, months=-m), with all other components zero. duration_isoformat(d) must produce a valid ISO 8601 duration whose parsed value equals Duration(months=12*y-m). These inputs represent positive, integral numbers of calendar months.

### Draft issue: duration_isoformat changes the value of durations with mixed-sign years and months

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `isodate` 0.7.2

**Documented behaviour:** “Format duration strings.” — public API documentation for duration_isoformat; the function is the ISO 8601 duration formatter paired with parse_duration.

**Expected:** A valid ISO 8601 duration representing 11 calendar months, such as P11M.

**Actual:** -P1Y1M, which parses as -13 calendar months.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'years': 1, 'months': -1} actual = {'formatted': '-P1Y1M', 'calendar_months': Decimal('-13')} expected = {'calendar_months': 11}
```

Judge: BUG (medium) -- The reproducer verifies that Duration(years=1, months=-1) equals Duration(months=11) before formatting. The ISO 8601 formatter then produces a valid string representing a different, negative duration. This is a value-preservation error, not rounding or an invalid argument type. The listed pull request addresses unsupported input types, not mixed-sign Duration components.

