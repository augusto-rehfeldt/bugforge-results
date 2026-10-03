*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `datetime`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Fractional-second UTC offsets must not collapse to UTC

Target: `datetime.time.fromisoformat`

Property: For every integer n with 1 <= abs(n) <= 999999, let t = time(12, 34, 56, tzinfo=timezone(timedelta(microseconds=n))). Then time.fromisoformat(t.isoformat()).utcoffset() must equal timedelta(microseconds=n).

### Draft issue: datetime.time.fromisoformat loses subsecond-only UTC offsets

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `datetime`

**Documented behaviour:** Python datetime documentation, time.fromisoformat: "Return a time corresponding to a time_string in any valid ISO 8601 format, with the following exceptions:" and "Time zone offsets may have fractional seconds." The time.isoformat documentation specifies that UTC offsets can be emitted as '+HH:MM:SS.ffffff'.

**Expected:** datetime.timedelta(microseconds=1)

**Actual:** datetime.timedelta(0)

**Reproducer:**

```python
import datetime as d

try:
    expected = d.timedelta(microseconds=1)
    t = d.time(12, 34, 56, tzinfo=d.timezone(expected))
    s = t.isoformat()
    if s != "12:34:56+00:00:00.000001":
        print("REFUTATION REJECTED: reported input was not reproduced")
    else:
        # Valid time and offset, in documented +HH:MM:SS.ffffff form.
        actual = d.time.fromisoformat(s).utcoffset()
        if actual != expected:
            print(f"REFUTATION CONFIRMED: {s!r} actual={actual!r} expected={expected!r}")
        else:
            print("REFUTATION REJECTED: actual equals documented expectation")
except Exception as e:
    print(f"REFUTATION REJECTED: {type(e).__name__}: {e}")
```

**Output:**

```
REFUTATION CONFIRMED: '12:34:56+00:00:00.000001' actual=datetime.timedelta(0) expected=datetime.timedelta(microseconds=1)
```

Judge: BUG (medium) -- The reproducer uses a valid timezone offset and the documented fractional-second offset format emitted by time.isoformat(). Parsing it silently loses the nonzero offset, violating the promise to return the corresponding time. The cited merged PR broadly expands ISO 8601 support but does not specifically report or fix this offset-loss behaviour, so it does not establish a duplicate.

