import datetime as dt
import plistlib
import random
import time


class FoldTimezone(dt.tzinfo):
    def __init__(self, offset0, offset1):
        self.offsets = (offset0, offset1)

    def utcoffset(self, value):
        return dt.timedelta(seconds=self.offsets[value.fold])

    def dst(self, value):
        return dt.timedelta(0)


def reference(value, offsets):
    # Independent of plistlib and datetime.astimezone.
    wall = dt.datetime(
        value.year, value.month, value.day,
        value.hour, value.minute, value.second, value.microsecond
    )
    utc_wall = wall - dt.timedelta(seconds=offsets[value.fold])
    return utc_wall.replace(tzinfo=dt.UTC)


def roundtrip(values):
    return plistlib.loads(
        plistlib.dumps(
            values, fmt=plistlib.FMT_BINARY, aware_datetime=True
        ),
        aware_datetime=True,
    )


def main():
    start = time.monotonic()
    deadline = start + 175

    for i, (fields, offsets) in enumerate([
        ((2020, 6, 15, 12, 30, 45, 0), (0, 0)),
        ((2021, 1, 2, 0, 15, 0, 0), (3600, 3600)),
    ], 1):
        zone = FoldTimezone(*offsets)
        values = [dt.datetime(*fields, tzinfo=zone)]
        expected = [reference(v, offsets) for v in values]
        try:
            actual = roundtrip(values)
        except Exception as exc:
            print("Sanity", i, repr(exc), repr(expected))
            print("SANITY FAILED")
            return
        print("Sanity", i, repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    count = 0

    def check(fields, offsets, order):
        nonlocal count
        zone = FoldTimezone(*offsets)
        values = [
            dt.datetime(*fields, tzinfo=zone, fold=fold)
            for fold in order
        ]
        expected = [reference(v, offsets) for v in values]
        literal = {
            "wall_fields": fields,
            "offset_seconds_by_fold": offsets,
            "fold_order": order,
        }

        def run():
            try:
                actual = roundtrip(values)
                return actual != expected, actual
            except Exception as exc:
                return True, {
                    "exception": type(exc).__name__,
                    "message": str(exc),
                }

        failed, actual = run()
        count += 1
        if failed:
            failed_again, actual_again = run()
            if failed_again:
                print("COUNTEREXAMPLE:")
                print(repr(literal))
                print("actual:", repr(actual_again))
                print("expected:", repr(expected))
                return True
        return False

    hand_picked = [
        (2020, 6, 15, 12, 0, 0, 0),
        (2001, 1, 1, 0, 0, 0, 0),
        (2000, 12, 31, 23, 30, 0, 0),
        (2024, 2, 29, 0, 30, 0, 0),
        (2023, 11, 5, 1, 30, 0, 0),
    ]
    offset_pairs = [
        (0, 3600),
        (3600, 0),
        (-3600, 0),
        (-18000, -14400),
        (19800, 20700),
    ]
    for fields in hand_picked:
        for offsets in offset_pairs:
            for order in [(0, 1), (1, 0)]:
                if check(fields, offsets, order):
                    return

    rng = random.Random(8675309)
    while time.monotonic() < deadline:
        fields = (
            rng.randint(1900, 2100),
            rng.randint(1, 12),
            rng.randint(1, 28),
            rng.randrange(24),
            rng.randrange(60),
            rng.randrange(60),
            0,
        )
        offset0 = rng.randint(-95, 95) * 900
        offset1 = offset0
        while offset1 == offset0:
            offset1 = rng.randint(-95, 95) * 900
        for order in [(0, 1), (1, 0)]:
            if check(fields, (offset0, offset1), order):
                return

    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()