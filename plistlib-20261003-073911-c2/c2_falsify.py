import datetime
import io
import plistlib
import random
import time

UTC = datetime.UTC


class FoldTZ(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=1 if dt.fold == 0 else 0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def __repr__(self):
        return "FoldTZ()"


TZ = FoldTZ()


def reference(values):
    # Exact arithmetic, independent of plistlib and astimezone.
    result = []
    for value in values:
        if value.tzinfo is TZ:
            offset = datetime.timedelta(hours=1 if value.fold == 0 else 0)
        else:
            offset = value.utcoffset()
        wall = value.replace(tzinfo=None, fold=0)
        result.append((wall - offset).replace(tzinfo=UTC))
    return result


def roundtrip(values):
    stream = io.BytesIO()
    plistlib.dump(
        values, stream, fmt=plistlib.FMT_BINARY, aware_datetime=True
    )
    stream.seek(0)
    return plistlib.load(stream, aware_datetime=True)


def observe(values):
    try:
        return ("result", roundtrip(values))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def agrees(actual, expected):
    return (
        actual[0] == "result"
        and actual[1] == expected
        and all(value.tzinfo is UTC for value in actual[1])
    )


def pair(fields, reverse=False):
    first = datetime.datetime(*fields, tzinfo=TZ, fold=0)
    second = datetime.datetime(*fields, tzinfo=TZ, fold=1)
    return [second, first] if reverse else [first, second]


def main():
    deadline = time.monotonic() + 175
    sanity_inputs = [
        [datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=UTC)],
        [
            datetime.datetime(
                2024, 6, 15, 12, 30, 0,
                tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30)),
            )
        ],
    ]

    sanity_ok = True
    for index, values in enumerate(sanity_inputs, 1):
        expected = reference(values)
        actual = observe(values)
        ok = agrees(actual, expected)
        print(
            f"SANITY {index}: {'PASS' if ok else 'FAIL'} "
            f"actual={actual!r} expected={expected!r}"
        )
        sanity_ok = sanity_ok and ok

    if not sanity_ok:
        print("SANITY FAILED")
        return

    tested = 0

    def check(values):
        nonlocal tested
        expected = reference(values)
        actual = observe(values)
        tested += 1
        if agrees(actual, expected):
            return False

        repeated = observe(values)
        if repeated != actual or agrees(repeated, expected):
            return False

        print("COUNTEREXAMPLE:")
        print(repr(values))
        print("actual:", repr(actual[1] if actual[0] == "result" else actual))
        print("expected:", repr(expected))
        return True

    edges = [
        (2024, 10, 27, 1, 30, 0),
        (2001, 1, 1, 0, 0, 0),
        (2000, 2, 29, 0, 0, 0),
        (1970, 1, 1, 0, 0, 0),
        (9998, 12, 31, 23, 59, 59),
    ]
    for fields in edges:
        for reverse in (False, True):
            if check(pair(fields, reverse)):
                return

    rng = random.Random(0xF01D)
    while time.monotonic() < deadline:
        year = rng.randint(2, 9998)
        month = rng.randint(1, 12)
        base = datetime.datetime(year, month, 1)
        next_month = (
            datetime.datetime(year + 1, 1, 1)
            if month == 12
            else datetime.datetime(year, month + 1, 1)
        )
        day = rng.randint(1, (next_month - base).days)
        fields = (
            year, month, day,
            rng.randrange(24), rng.randrange(60), rng.randrange(60),
        )
        if check(pair(fields, bool(rng.getrandbits(1)))):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()