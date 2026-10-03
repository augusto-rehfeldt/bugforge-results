import datetime
import random
import time


def offset_microseconds(offset):
    return ((offset.days * 86400 + offset.seconds) * 1_000_000
            + offset.microseconds)


def check(k):
    d = datetime.datetime(
        2024, 1, 2, 12,
        tzinfo=datetime.timezone(datetime.timedelta(microseconds=k)),
    )
    text = d.isoformat()
    try:
        offset = datetime.datetime.fromisoformat(text).utcoffset()
        actual = None if offset is None else offset_microseconds(offset)
    except Exception as exc:
        actual = ("exception", type(exc).__name__, str(exc))
    return text, actual


def main():
    # Exact reference: a fixed offset of k microseconds has offset k.
    for k in (3_600_000_000, -19_800_000_000):
        text, actual = check(k)
        print("SANITY:", repr(text), "actual:", repr(actual),
              "expected:", repr(k), "(microseconds)")
        if actual != k:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0
    rng = random.Random(20240102)
    edges = [
        1, -1, 500000, -500000, 999999, -999999,
        2, -2, 999, -999, 1000, -1000,
        499999, -499999, 500001, -500001,
        999998, -999998,
    ]

    def test(k):
        nonlocal tested
        text, actual = check(k)
        tested += 1
        if actual != k:
            retry_text, retry_actual = check(k)
            if retry_text == text and retry_actual == actual:
                print("COUNTEREXAMPLE:", repr(text),
                      "actual:", repr(actual),
                      "expected:", repr(k), "(microseconds)")
                return True
        return False

    for k in edges:
        if time.monotonic() >= deadline:
            break
        if test(k):
            return

    while time.monotonic() < deadline:
        k = rng.randint(1, 999999)
        if rng.getrandbits(1):
            k = -k
        if test(k):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()