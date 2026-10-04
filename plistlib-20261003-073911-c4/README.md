*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Binary datetime deduplication loses distinct instants across a timezone fold

Target: `plistlib.loads`

Property: For two aware datetime objects a and b sharing the same tzinfo, with identical wall-clock fields but different fold values and different UTC offsets, loads(dumps([a, b], fmt=FMT_BINARY, aware_datetime=True), aware_datetime=True) must equal [a.astimezone(datetime.UTC), b.astimezone(datetime.UTC)].

### Draft issue: plistlib binary serialization conflates aware datetimes with different fold-dependent UTC offsets

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** The plistlib documentation for dump states: "When aware_datetime is true and the value is an aware datetime.datetime, it will be converted to UTC timezone before writing it." The load documentation states: "When aware_datetime is true, fields with type datetime.datetime will be created as aware datetime.datetime with datetime.UTC as tzinfo."

**Expected:** UTC datetimes 2020-06-15 12:00 and 2020-06-15 11:00.

**Actual:** Both decoded datetimes are 2020-06-15 12:00 UTC.

**Reproducer:**

```python
import datetime as d
import plistlib as p

class Zone(d.tzinfo):
    def utcoffset(self, dt):
        return d.timedelta(hours=dt.fold)
    def dst(self, dt):
        return d.timedelta(0)

try:
    z = Zone()
    values = [d.datetime(2020, 6, 15, 12, tzinfo=z, fold=f) for f in (0, 1)]
    offsets = [v.utcoffset() for v in values]
    if not (values[0].tzinfo is values[1].tzinfo
            and values[0].replace(tzinfo=None) == values[1].replace(tzinfo=None)
            and offsets == [d.timedelta(0), d.timedelta(hours=1)]):
        raise ValueError("input does not meet the reported conditions")
    expected = [(v.replace(tzinfo=None) - o).replace(tzinfo=d.timezone.utc)
                for v, o in zip(values, offsets)]
    actual = p.loads(p.dumps(values, fmt=p.FMT_BINARY, aware_datetime=True),
                     aware_datetime=True)
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input:", values,
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches the documented expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: input: [datetime.datetime(2020, 6, 15, 12, 0, tzinfo=<__main__.Zone object at 0x000001F754246BA0>), datetime.datetime(2020, 6, 15, 12, 0, fold=1, tzinfo=<__main__.Zone object at 0x000001F754246BA0>)] actual: [datetime.datetime(2020, 6, 15, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 6, 15, 12, 0, tzinfo=datetime.timezone.utc)] expected: [datetime.datetime(2020, 6, 15, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2020, 6, 15, 11, 0, tzinfo=datetime.timezone.utc)]
```

Judge: BUG (medium) -- The input contains valid aware datetimes whose fold-dependent offsets identify different UTC instants. The expected calculation correctly implements conversion to UTC, which the documentation explicitly promises. Binary serialization instead collapses the two values, consistent with deduplication using datetime equality, which ignores fold when tzinfo is shared. This is a serialization bug exposed by loads, not an invalid expectation or a documented limitation. The listed issue is unrelated, and the supplied upstream diff contains no fix.

