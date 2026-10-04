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