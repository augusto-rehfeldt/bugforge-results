*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: GMT formatting accepts any aware datetime with zero UTC offset

Target: `email.utils.format_datetime`

Property: For every aware datetime dt whose utcoffset() equals datetime.timedelta(0), format_datetime(dt, usegmt=True) must return an RFC 2822 date string ending in ' GMT', without raising ValueError.

### Draft issue: email.utils.format_datetime rejects custom zero-offset tzinfo with usegmt=True

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The format_datetime docstring states: "If usegmt is True, dt must be an aware datetime with an offset of zero. In this case 'GMT' will be rendered instead of the normal +0000 required by RFC2822."

**Expected:** Return a date string ending in ' GMT' without raising ValueError for an aware zero-offset datetime.

**Actual:** Raises ValueError: usegmt option requires a UTC datetime.

**Reproducer:**

```python
import datetime as d
import email.utils

class ZeroOffset(d.tzinfo):
    def utcoffset(self, dt): return d.timedelta(0)
    def dst(self, dt): return d.timedelta(0)
    def tzname(self, dt): return "UTC"
    def __repr__(self): return "ZeroOffset()"

dt = d.datetime(1, 1, 1, tzinfo=ZeroOffset())
if dt.tzinfo is None or dt.utcoffset() != d.timedelta(0):
    print("REFUTATION REJECTED: input is not aware with zero offset")
else:
    expected = (
        f"{('Mon','Tue','Wed','Thu','Fri','Sat','Sun')[dt.weekday()]}, "
        f"{dt.day:02d} {'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[dt.month-1]} "
        f"{dt.year:04d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"
    )
    try:
        actual = ("result", email.utils.format_datetime(dt, usegmt=True))
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
    if actual != ("result", expected):
        print("REFUTATION CONFIRMED:", repr(dt), "actual:", actual, "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: result matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: datetime.datetime(1, 1, 1, 0, 0, tzinfo=ZeroOffset()) actual: ('exception', 'ValueError', 'usegmt option requires a UTC datetime') expected: 'Mon, 01 Jan 0001 00:00:00 GMT'
```

Judge: BUG (low) -- The custom tzinfo makes dt aware and returns an offset of zero, satisfying the explicit documented precondition. The implementation instead requires tzinfo to equal datetime.timezone.utc, rejecting other zero-offset implementations. This mismatch is independent of the chosen year; a modern year would avoid the separate RFC 2822 year-range concern. The listed roundtripping issue does not establish a duplicate of this rejection, and the upstream diff contains no fix.

