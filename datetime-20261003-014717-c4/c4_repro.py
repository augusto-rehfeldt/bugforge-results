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