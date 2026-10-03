import datetime

args = (-(1 << 100), 1, 1)
y, m, d = args
if not all(type(x) is int for x in args) or (m, d) != (1, 1):
    print("REFUTATION REJECTED:", "invalid argument types or month/day")
elif datetime.MINYEAR <= y <= datetime.MAXYEAR:
    print("REFUTATION REJECTED:", "year is within the documented range")
else:
    expected = ("exception", "ValueError")
    try:
        result = datetime.date(*args)
        actual = ("date", (result.year, result.month, result.day))
    except Exception as e:
        actual = ("exception", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", args, actual, expected)
    else:
        print("REFUTATION REJECTED:", "observed the documented ValueError")