*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `datetime`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Out-of-range integer years raise OverflowError instead of documented ValueError

Target: `datetime.date`

Property: For every Python integer year outside 1 <= year <= 9999, date(year, 1, 1) must raise ValueError, rather than another exception.

### Draft issue: datetime.date raises OverflowError instead of documented ValueError for very large integer years

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

**Documented behaviour:** Python datetime documentation, date Objects, date(year, month, day): "If an argument outside those ranges is given, ValueError is raised." The listed year range is "MINYEAR <= year <= MAXYEAR".

**Expected:** ValueError for date(-(1 << 100), 1, 1).

**Actual:** OverflowError.

**Reproducer:**

```python
import datetime

args = (-(1 << 100), 1, 1)
y, m, d = args
if not all(type(x) is int for x in args) or (m, d) != (1, 1):
    print("REFUTATION REJECTED:", "invalid argument types or month/day")
elif datetime.MINYEAR <= y <= datetime.MAXYEAR:
    print("REFUTATION REJECTED:", "year is within the documented range")
else:
    expected = ("exception", "ValueError")
    try:
        result = datetime.date(*args)
        actual = ("date", (result.year, result.month, result.day))
    except Exception as e:
        actual = ("exception", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", args, actual, expected)
    else:
        print("REFUTATION REJECTED:", "observed the documented ValueError")
```

**Output:**

```
REFUTATION CONFIRMED: (-1267650600228229401496703205376, 1, 1) ('exception', 'OverflowError') ('exception', 'ValueError')
```

Judge: BUG (low) -- The reproducer uses exact Python integers and valid month/day values. The year is outside the documented range, for which the cited constructor documentation explicitly promises ValueError. Instead, the observed OverflowError violates that promise, apparently during conversion to a bounded C integer before range validation. None of the listed issues clearly identifies this same behaviour.

