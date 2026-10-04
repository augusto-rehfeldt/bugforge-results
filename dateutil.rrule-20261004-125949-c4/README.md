*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: TZID mapping should apply to RDATE properties

Target: `dateutil.rrule.rrulestr`

Property: For a valid RDATE-only recurrence string of the form 'RDATE;TZID=ZoneName:YYYYMMDDTHHMMSS', and tzids={ZoneName: tz} where tz is a fixed-offset tzinfo, list(rrulestr(s, tzids=tzids, forceset=True)) must contain exactly the specified local datetime with tzinfo=tz, rather than raising an unsupported-parameter exception.

### Draft issue: rrulestr rejects TZID on RDATE despite a supplied tzids mapping

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrulestr documentation describes tzids as: 'If given, a mapping of time zone names to tzinfo objects, or a callable taking a time zone name and returning a tzinfo object. This is used to retrieve the time zone when parsing TZID parameter.' This parameter description does not restrict TZID resolution to DTSTART.

**Expected:** One occurrence: 2025-01-01 12:00:00+02:00, using the supplied tzinfo object.

**Actual:** ValueError: unsupported RDATE parm: TZID=CUSTOMZONE

**Reproducer:**

```python
from datetime import datetime, timezone, timedelta
from dateutil.rrule import rrulestr

tz = timezone(timedelta(hours=2))
args = dict(s="RDATE;TZID=CustomZone:20250101T120000",
            tzids={"CustomZone": tz}, forceset=True)

try:
    header, value = args["s"].split(":")
    kind, parameter = header.split(";")
    key, zone = parameter.split("=")
    if (kind, key) != ("RDATE", "TZID"):
        raise ValueError("not an RDATE with TZID")
    resolved = args["tzids"][zone]  # Documented TZID mapping lookup.
    local = datetime.strptime(value, "%Y%m%dT%H%M%S")
    if local.strftime("%Y%m%dT%H%M%S") != value:
        raise ValueError("invalid date-time format")
    if not isinstance(resolved, timezone):
        raise ValueError("not a fixed-offset tzinfo")
    expected = [local.replace(tzinfo=resolved)]
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", str(e))
else:
    try:
        actual = list(rrulestr(**args))
        broken = (actual != expected or len(actual) != 1
                  or actual[0].tzinfo is not resolved)
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", args, "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'s': 'RDATE;TZID=CustomZone:20250101T120000', 'tzids': {'CustomZone': datetime.timezone(datetime.timedelta(seconds=7200))}, 'forceset': True} actual: ('exception', 'ValueError', 'unsupported RDATE parm: TZID=CUSTOMZONE') expected: [datetime.datetime(2025, 1, 1, 12, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))]
```

Judge: BUG (medium) -- RDATE with a TZID parameter is valid, and the documented tzids mapping resolves TZID parameters without limiting support to DTSTART. The reproducer correctly constructs the specified fixed-offset local datetime. Instead of resolving the supplied timezone, rrulestr rejects the parameter outright. The listed issue concerns DTSTART VALUE=DATE-TIME, not RDATE TZID, so it is not a duplicate.

