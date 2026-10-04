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