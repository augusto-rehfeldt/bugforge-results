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