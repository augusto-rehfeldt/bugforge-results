*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Binary loading loses distinct UTC instants for fold-dependent datetimes

Target: `plistlib.load`

Property: For a list of timezone-aware datetime objects with zero microseconds, writing to io.BytesIO with dump(..., fmt=FMT_BINARY, aware_datetime=True), rewinding, and calling load(..., aware_datetime=True) must return each original datetime converted to datetime.UTC, preserving its UTC instant even when two inputs differ only in fold.

### Draft issue: plistlib binary writer conflates fold-distinct aware datetimes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** The plistlib documentation for dump states: "If aware_datetime is true and the value is datetime.datetime with tzinfo set, it will be converted to UTC timezone before writing it." The load documentation states: "When aware_datetime is true, datetime.datetime objects will be timezone-aware and use datetime.UTC as the timezone."

**Expected:** UTC datetimes 2024-10-27 00:30:00+00:00 and 2024-10-27 01:30:00+00:00.

**Actual:** Both loaded datetimes are 2024-10-27 00:30:00+00:00.

**Reproducer:**

```python
import datetime as d
import inspect
import io
import plistlib as p

class FoldTZ(d.tzinfo):
    def utcoffset(self, dt):
        return d.timedelta(hours=1 - dt.fold)
    def dst(self, dt):
        return d.timedelta(0)
    def tzname(self, dt):
        return "FoldTZ"
    def __repr__(self):
        return "FoldTZ()"

def main():
    if any("aware_datetime" not in inspect.signature(f).parameters
           for f in (p.dump, p.load)):
        print("REFUTATION REJECTED: this Python lacks aware_datetime support")
        return

    tz = FoldTZ()
    values = [d.datetime(2024, 10, 27, 1, 30, fold=f, tzinfo=tz)
              for f in (0, 1)]
    offsets = [v.utcoffset() for v in values]
    if not all(v.microsecond == 0 and isinstance(o, d.timedelta)
               and abs(o) < d.timedelta(days=1)
               for v, o in zip(values, offsets)):
        print("REFUTATION REJECTED: invalid aware datetime input")
        return

    expected = [(v.replace(tzinfo=None) - o).replace(tzinfo=d.timezone.utc,
                                                    fold=0)
                for v, o in zip(values, offsets)]
    stream = io.BytesIO()
    try:
        p.dump(values, stream, fmt=p.FMT_BINARY, aware_datetime=True)
        stream.seek(0)
        actual = p.load(stream, aware_datetime=True)
    except Exception as exc:
        actual = repr(exc)

    if actual != expected:
        print("REFUTATION CONFIRMED:",
              "input:", values, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: round-trip matches documented UTC instants")

main()
```

**Output:**

```
REFUTATION CONFIRMED: input: [datetime.datetime(2024, 10, 27, 1, 30, tzinfo=FoldTZ()), datetime.datetime(2024, 10, 27, 1, 30, fold=1, tzinfo=FoldTZ())] actual: [datetime.datetime(2024, 10, 27, 0, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2024, 10, 27, 0, 30, tzinfo=datetime.timezone.utc)] expected: [datetime.datetime(2024, 10, 27, 0, 30, tzinfo=datetime.timezone.utc), datetime.datetime(2024, 10, 27, 1, 30, tzinfo=datetime.timezone.utc)]
```

Judge: BUG (medium) -- The inputs are valid aware datetimes with distinct UTC instants: fold=0 has offset +01:00, while fold=1 has offset +00:00. The expected values correctly apply those offsets. Binary serialization appears to deduplicate the datetimes before UTC conversion because same-tzinfo datetime equality ignores fold, losing the second instant. This violates dump's documented UTC conversion promise, rather than showing an invalid expectation or a load timezone error. No matching issue or fix is listed, and the upstream diff does not address this behaviour.

