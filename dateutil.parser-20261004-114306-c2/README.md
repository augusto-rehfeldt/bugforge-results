*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.parser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: ISO date parser accepts week 53 in years with only 52 ISO weeks

Target: `dateutil.parser.isoparser.parse_isodate`

Property: For any year y in 1..9998 whose December 28 has ISO week number 52, and any weekday d in 1..7, parse_isodate(f'{y:04d}-W53-{d}') must raise ValueError: that week does not exist in ISO week-year y.

### Draft issue: parse_isodate accepts week 53 in ISO years with only 52 weeks

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The isoparser.parse_isodate docstring states: "Raises ValueError: If the string is not a valid ISO date." The isoparse documentation lists ISO week dates as supported: "YYYY-Www-D or YYYYWwwD - ISO week (day of week)".

**Expected:** ValueError for '2021-W53-1', since ISO year 2021 has no week 53.

**Actual:** Returns datetime.date(2022, 1, 3).

**Reproducer:**

```python
from datetime import date
from dateutil.parser.isoparser import isoparser

y, d = 2021, 1
s = f"{y:04d}-W53-{d}"
if not (1 <= y <= 9998 and 1 <= d <= 7
        and date(y, 12, 28).isocalendar().week == 52):
    print("REFUTATION REJECTED: invalid test premise")
else:
    # Documented YYYY-Www-D syntax; independently check ISO validity.
    try:
        expected = date.fromisocalendar(y, 53, d)
    except ValueError:
        expected = ValueError
    try:
        actual = isoparser().parse_isodate(s)
    except Exception as e:
        actual = type(e)
    if expected is ValueError and actual is not ValueError:
        print("REFUTATION CONFIRMED:", repr(s),
              "actual=", actual, "expected=ValueError")
    else:
        print("REFUTATION REJECTED:", repr(s),
              "actual=", actual, "expected=", expected)
```

**Output:**

```
REFUTATION CONFIRMED: '2021-W53-1' actual= 2022-01-03 expected=ValueError
```

Judge: BUG (medium) -- The reproducer correctly establishes that ISO year 2021 has only 52 weeks, independently confirmed by date.fromisocalendar. Although the string uses supported ISO week-date syntax, its week does not exist. parse_isodate documents ValueError for invalid ISO dates but instead silently normalizes it into the following ISO year. The listed relativedelta issue is unrelated. Upstream fix status was not checked.

