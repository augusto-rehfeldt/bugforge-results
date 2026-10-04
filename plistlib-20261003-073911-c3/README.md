*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Binary dump merges equal fold datetimes representing different UTC instants

Target: `plistlib.dump`

Property: For a list xs of aware datetime.datetime objects, dump(xs, io.BytesIO(), fmt=plistlib.FMT_BINARY, aware_datetime=True), followed by loads of the buffer with aware_datetime=True, must produce [x.astimezone(datetime.UTC) for x in xs]. Restrict inputs to whole-second dates comfortably within datetime's range, including pairs sharing a tzinfo object and wall-clock fields but having different fold values and UTC offsets.

### Draft issue: plistlib binary writer conflates fold-distinct aware datetimes before UTC conversion

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** The plistlib documentation for dump's aware_datetime parameter states: “When true, datetime.datetime objects will be converted to UTC before writing.” The supported-types documentation includes datetime.datetime objects and lists.

**Expected:** [2024-11-03 05:30:00+00:00, 2024-11-03 06:30:00+00:00]

**Actual:** [2024-11-03 05:30:00+00:00, 2024-11-03 05:30:00+00:00]

**Reproducer:**

```python
import datetime as d
import io
import plistlib

class FoldTZ(d.tzinfo):
    def utcoffset(self, dt):
        return d.timedelta(hours=-4-dt.fold)
    def dst(self, dt):
        return d.timedelta(0)
    def tzname(self, dt):
        return "FoldTZ"
    def __repr__(self):
        return "FoldTZ()"

tz = FoldTZ()
xs = [d.datetime(2024, 11, 3, 1, 30, tzinfo=tz, fold=f) for f in (0, 1)]
try:
    if not (isinstance(xs, list) and all(
        isinstance(x, d.datetime) and x.microsecond == 0
        and isinstance(x.utcoffset(), d.timedelta)
        and abs(x.utcoffset()) < d.timedelta(days=1) for x in xs
    )):
        raise ValueError("input is not a supported list of aware whole-second datetimes")
    expected = [(x.replace(tzinfo=None) - x.utcoffset()).replace(tzinfo=d.UTC)
                for x in xs]
    buf = io.BytesIO()
    plistlib.dump(xs, buf, fmt=plistlib.FMT_BINARY, aware_datetime=True)
    actual = plistlib.loads(buf.getvalue(), aware_datetime=True)
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input=", xs, "actual=", actual,
              "expected=", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented UTC conversion")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: input= [datetime.datetime(2024, 11, 3, 1, 30, tzinfo=FoldTZ()), datetime.datetime(2024, 11, 3, 1, 30, fold=1, tzinfo=FoldTZ())] actual= [datetime.datetime(2024, 11, 3, 5, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2024, 11, 3, 5, 30, tzinfo=datetime.timezone.utc)] expected= [datetime.datetime(2024, 11, 3, 5, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2024, 11, 3, 6, 30, tzinfo=datetime.timezone.utc)]
```

Judge: BUG (medium) -- The inputs are valid aware, whole-second datetimes representing distinct UTC instants. The expected calculation correctly converts each to UTC, as documented. Binary serialization apparently deduplicates the datetimes before conversion: Python treats datetimes with identical wall-clock fields and the same tzinfo as equal despite differing fold values. That equality does not justify discarding distinct UTC instants when UTC conversion is promised. The supplied upstream diff does not fix this, and the listed issue is unrelated.

