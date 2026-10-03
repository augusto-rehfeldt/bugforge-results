# bugforge: `datetime`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: ISO-format parsing loses subsecond UTC offsets

Target: `datetime.datetime.fromisoformat`

Property: For a datetime d with tzinfo=timezone(timedelta(microseconds=k)), where 1 <= abs(k) <= 999999, datetime.fromisoformat(d.isoformat()).utcoffset() must equal d.utcoffset(): parsing must preserve the fractional-second UTC offset emitted by isoformat().

### Draft issue: datetime.fromisoformat loses fractional UTC offsets smaller than one second

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

**Documented behaviour:** Python datetime documentation, datetime.fromisoformat(): "Return a datetime corresponding to a date_string in any valid ISO 8601 format, with the following exceptions:" followed by "Time zone offsets may have fractional seconds." datetime.isoformat() documents its aware output as "YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM[:SS[.ffffff]]".

**Expected:** Parsing '2024-01-02T12:00:00+00:00:00.000001' preserves utcoffset() == timedelta(microseconds=1).

**Actual:** Parsing returns a datetime with a zero UTC offset.

**Reproducer:**

```python
import datetime as dt

try:
    offset = dt.timedelta(microseconds=1)
    d = dt.datetime(2024, 1, 2, 12, tzinfo=dt.timezone(offset))
    s = d.isoformat()
    if s != "2024-01-02T12:00:00+00:00:00.000001":
        print("REFUTATION REJECTED: input does not match documented isoformat output")
    else:
        expected = offset // dt.timedelta(microseconds=1)
        actual = dt.datetime.fromisoformat(s).utcoffset() // dt.timedelta(microseconds=1)
        if actual != expected:
            print(f"REFUTATION CONFIRMED: {s!r} actual: {actual} expected: {expected} (microseconds)")
        else:
            print("REFUTATION REJECTED: fractional-second offset preserved")
except Exception as e:
    print(f"REFUTATION REJECTED: {type(e).__name__}: {e}")
```

**Output:**

```
REFUTATION CONFIRMED: '2024-01-02T12:00:00+00:00:00.000001' actual: 0 expected: 1 (microseconds)
```

Judge: BUG (medium) -- The reproducer uses a valid fixed-offset datetime and verifies the documented isoformat output. fromisoformat explicitly supports fractional-second time zone offsets, but silently discards the nonzero one-microsecond offset. The expected value is computed exactly using timedelta integer division, not floating-point arithmetic. None of the listed issues or pull requests concerns this behavior.

