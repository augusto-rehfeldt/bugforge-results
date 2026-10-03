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