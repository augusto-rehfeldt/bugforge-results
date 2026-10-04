*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `isodate`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `isodate` 0.7.2

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Small fractional years must not be formatted using scientific notation

Target: `isodate.duration_isoformat`

Property: For Duration(years=Decimal(10) ** -n), where n is an integer from 7 through 20 and all other components are zero, duration_isoformat must return an ISO 8601 duration representing that fractional year value, using decimal notation rather than an exponent such as '1E-7Y'.

### Draft issue: duration_isoformat emits invalid scientific notation for small Decimal year values

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `isodate` 0.7.2

**Documented behaviour:** "Format duration strings." — the supplied PUBLIC API documentation for duration_isoformat, described as formatting ISO 8601 durations.

**Expected:** P0.0000001Y

**Actual:** P1E-7Y

**Reproducer:**

```python
from decimal import Decimal
from isodate import Duration, duration_isoformat

years = Decimal(10) ** -7
d = Duration(years=years)
try:
    if not (years.is_finite() and years >= 0 and
            d.years == years and d.months == 0 and
            d.days == d.seconds == d.microseconds == 0):
        print("REFUTATION REJECTED: invalid year-only duration")
    else:
        # ISO 8601 permits a decimal fraction on the lowest-order component.
        expected = "P" + format(years, "f") + "Y"
        actual = duration_isoformat(d)
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"years": str(years), "actual": actual, "expected": expected})
        else:
            print("REFUTATION REJECTED: output matches the ISO 8601 expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'years': '1E-7', 'actual': 'P1E-7Y', 'expected': 'P0.0000001Y'}
```

Judge: BUG (medium) -- The reproducer supplies a valid Duration with an exact, nonnegative fractional year as its sole component. Formatting an ISO 8601 duration requires decimal notation: scientific notation is not valid for a duration component. The observed result therefore violates the formatter's stated purpose, rather than reflecting floating-point rounding. The listed pull request concerns unsupported argument types and explicitly leaves formatting rules unchanged, so it is not a duplicate. Only n=7 is demonstrated by this reproducer.

