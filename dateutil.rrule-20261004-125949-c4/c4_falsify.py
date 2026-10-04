import datetime
import random
import time
from dateutil.rrule import rrulestr


def reference(year, month, day, hour, minute, second, tz):
    return [datetime.datetime(year, month, day, hour, minute, second, tzinfo=tz)]


def run(s, tzids):
    try:
        return ("result", list(rrulestr(s, tzids=tzids, forceset=True)))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def matches(actual, expected):
    return (
        actual[0] == "result"
        and len(actual[1]) == 1
        and actual[1][0] == expected[0]
        and actual[1][0].replace(tzinfo=None) == expected[0].replace(tzinfo=None)
        and actual[1][0].tzinfo is expected[0].tzinfo
    )


def main():
    deadline = time.monotonic() + 175
    for index, fields in enumerate(
        [(2025, 1, 1, 12, 0, 0), (2000, 2, 29, 23, 59, 59)], 1
    ):
        expected = reference(*fields, None)
        s = "RDATE:" + expected[0].strftime("%Y%m%dT%H%M%S")
        actual = run(s, {})
        if not matches(actual, expected):
            print("SANITY FAILED")
            return
        print("SANITY {}: reference agrees".format(index))

    edges = [
        ("CustomZone", (2025, 1, 1, 12, 0, 0), 7200),
        ("ZeroZone", (2000, 2, 29, 0, 0, 0), 0),
        ("EastZone", (2024, 12, 31, 23, 59, 59), 86399),
        ("WestZone", (2024, 1, 1, 0, 0, 0), -86399),
        ("OddZone", (1900, 3, 1, 12, 34, 56), 19801),
    ]
    rng = random.Random(731905)
    tested = 0

    def cases():
        yield from edges
        while True:
            year = rng.randint(1900, 2100)
            month = rng.randint(1, 12)
            first = datetime.date(year, month, 1)
            next_month = (
                datetime.date(year + 1, 1, 1)
                if month == 12
                else datetime.date(year, month + 1, 1)
            )
            day = rng.randint(1, (next_month - first).days)
            fields = (
                year, month, day,
                rng.randrange(24), rng.randrange(60), rng.randrange(60),
            )
            yield "Zone{}".format(rng.randrange(100000)), fields, rng.randint(-86399, 86399)

    for name, fields, offset in cases():
        if time.monotonic() >= deadline:
            break
        tz = datetime.timezone(datetime.timedelta(seconds=offset))
        expected = reference(*fields, tz)
        y, mo, d, h, mi, sec = fields
        s = "RDATE;TZID={}:{:04d}{:02d}{:02d}T{:02d}{:02d}{:02d}".format(
            name, y, mo, d, h, mi, sec
        )
        tzids = {name: tz}
        actual = run(s, tzids)
        tested += 1
        if not matches(actual, expected):
            confirmed = run(s, tzids)
            if confirmed == actual and not matches(confirmed, expected):
                print("COUNTEREXAMPLE:")
                print(repr({"s": s, "tzids": tzids, "forceset": True}))
                print("actual:", repr(confirmed))
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()