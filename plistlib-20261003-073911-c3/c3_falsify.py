import datetime
import io
import plistlib
import random
import time


class FoldTZ(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5 if dt.fold else -4)

    def dst(self, dt):
        return datetime.timedelta(0)

    def __repr__(self):
        return "FoldTZ()"


TZ = FoldTZ()
UTC = datetime.UTC


def reference(xs):
    # Independently apply the definition UTC = wall time - UTC offset.
    result = []
    for x in xs:
        wall = datetime.datetime(
            x.year, x.month, x.day, x.hour, x.minute, x.second
        )
        if x.tzinfo is TZ:
            offset = datetime.timedelta(hours=-5 if x.fold else -4)
        elif x.tzinfo is UTC:
            offset = datetime.timedelta(0)
        else:
            raise AssertionError("Unexpected reference timezone")
        result.append((wall - offset).replace(tzinfo=UTC))
    return result


def roundtrip(xs):
    buffer = io.BytesIO()
    plistlib.dump(
        xs, buffer, fmt=plistlib.FMT_BINARY, aware_datetime=True
    )
    return plistlib.loads(buffer.getvalue(), aware_datetime=True)


def observe(xs):
    try:
        return ("result", roundtrip(xs))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def pair(fields, reverse=False):
    xs = [
        datetime.datetime(*fields, tzinfo=TZ, fold=0),
        datetime.datetime(*fields, tzinfo=TZ, fold=1),
    ]
    return xs[::-1] if reverse else xs


def main():
    sanity_inputs = [
        [datetime.datetime(2024, 6, 15, 12, 34, 56, tzinfo=UTC)],
        [datetime.datetime(2024, 6, 15, 12, 34, 56, tzinfo=TZ, fold=1)],
    ]
    for number, xs in enumerate(sanity_inputs, 1):
        expected = reference(xs)
        actual = observe(xs)
        ok = actual == ("result", expected)
        print(
            "SANITY {}: actual={!r}, expected={!r}, agrees={}".format(
                number, actual, expected, ok
            )
        )
        if not ok:
            print("SANITY FAILED")
            return

    tested = 0
    deadline = time.monotonic() + 170

    def check(xs):
        nonlocal tested
        tested += 1
        expected = reference(xs)
        actual = observe(xs)
        if actual == ("result", expected):
            return False
        repeated = observe(xs)
        if repeated == ("result", expected):
            return False
        print("COUNTEREXAMPLE:")
        print(repr(xs))
        print("actual:", repr(repeated))
        print("expected:", repr(expected))
        return True

    edges = [
        (2024, 11, 3, 1, 30, 0),
        (2001, 1, 1, 0, 0, 0),
        (1970, 1, 1, 0, 0, 0),
        (1999, 12, 31, 23, 59, 59),
        (2000, 2, 29, 23, 59, 59),
        (1900, 3, 1, 0, 0, 0),
        (2100, 12, 31, 23, 59, 59),
    ]
    for fields in edges:
        for reverse in (False, True):
            if check(pair(fields, reverse)):
                return

    rng = random.Random(0xF01D)
    start = datetime.datetime(1900, 1, 1)
    span = (datetime.datetime(2101, 1, 1) - start).days * 86400
    while time.monotonic() < deadline:
        wall = start + datetime.timedelta(seconds=rng.randrange(span))
        fields = (
            wall.year, wall.month, wall.day,
            wall.hour, wall.minute, wall.second,
        )
        for reverse in (False, True):
            if check(pair(fields, reverse)):
                return

    print("NO COUNTEREXAMPLE")
    print(tested)


if __name__ == "__main__":
    main()