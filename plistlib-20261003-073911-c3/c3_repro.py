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