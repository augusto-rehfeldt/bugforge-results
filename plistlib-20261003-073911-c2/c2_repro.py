import datetime as d
import inspect
import io
import plistlib as p

class FoldTZ(d.tzinfo):
    def utcoffset(self, dt):
        return d.timedelta(hours=1 - dt.fold)
    def dst(self, dt):
        return d.timedelta(0)
    def tzname(self, dt):
        return "FoldTZ"
    def __repr__(self):
        return "FoldTZ()"

def main():
    if any("aware_datetime" not in inspect.signature(f).parameters
           for f in (p.dump, p.load)):
        print("REFUTATION REJECTED: this Python lacks aware_datetime support")
        return

    tz = FoldTZ()
    values = [d.datetime(2024, 10, 27, 1, 30, fold=f, tzinfo=tz)
              for f in (0, 1)]
    offsets = [v.utcoffset() for v in values]
    if not all(v.microsecond == 0 and isinstance(o, d.timedelta)
               and abs(o) < d.timedelta(days=1)
               for v, o in zip(values, offsets)):
        print("REFUTATION REJECTED: invalid aware datetime input")
        return

    expected = [(v.replace(tzinfo=None) - o).replace(tzinfo=d.timezone.utc,
                                                    fold=0)
                for v, o in zip(values, offsets)]
    stream = io.BytesIO()
    try:
        p.dump(values, stream, fmt=p.FMT_BINARY, aware_datetime=True)
        stream.seek(0)
        actual = p.load(stream, aware_datetime=True)
    except Exception as exc:
        actual = repr(exc)

    if actual != expected:
        print("REFUTATION CONFIRMED:",
              "input:", values, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: round-trip matches documented UTC instants")

main()