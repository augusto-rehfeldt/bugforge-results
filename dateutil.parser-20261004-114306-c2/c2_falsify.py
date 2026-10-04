import datetime
import random
import time
from dateutil.parser import isoparser

parser = isoparser()
deadline = time.monotonic() + 175
tested = 0


def days_before_year(year):
    n = year - 1
    return 365 * n + n // 4 - n // 100 + n // 400


def week_one_monday(year):
    jan4 = days_before_year(year) + 4
    return jan4 - (jan4 - 1) % 7


def weeks_in_year(year):
    return (week_one_monday(year + 1) - week_one_monday(year)) // 7


def reference(year, week, day):
    if not 1 <= week <= weeks_in_year(year) or not 1 <= day <= 7:
        raise ValueError("Invalid ISO week date")
    ordinal = week_one_monday(year) + 7 * (week - 1) + day - 1
    return datetime.date.fromordinal(ordinal)


def spell(year, week, day, basic):
    if basic:
        return f"{year:04d}W{week:02d}{day}"
    return f"{year:04d}-W{week:02d}-{day}"


def call(text):
    try:
        return ("result", parser.parse_isodate(text))
    except Exception as exc:
        return ("exception", type(exc), str(exc))


def rejected(outcome):
    return outcome[0] == "exception" and issubclass(outcome[1], ValueError)


def main():
    global tested

    for year, week, day, basic in [
        (2020, 53, 7, False),
        (2021, 1, 1, True),
    ]:
        text = spell(year, week, day, basic)
        expected = reference(year, week, day)
        actual = call(text)
        print(f"SANITY: {text!r} actual={actual!r} expected={expected!r}")
        if actual != ("result", expected):
            print("SANITY FAILED")
            return

    eligible = [
        year for year in range(1, 9999)
        if weeks_in_year(year) == 52
    ]

    def check(year, day, basic):
        global tested
        text = spell(year, 53, day, basic)
        try:
            reference(year, 53, day)
        except ValueError:
            pass
        else:
            raise AssertionError("Reference accepted a nonexistent week")

        actual = call(text)
        tested += 1
        if rejected(actual):
            return False

        confirmation = call(text)
        if rejected(confirmation):
            return False

        print("COUNTEREXAMPLE:")
        print(repr(text))
        print(f"actual: {confirmation!r}")
        print("expected: ValueError (ISO week 53 does not exist)")
        return True

    for year in [2021, 1, 9998, 1900, 2000, 2100, 2014, 2022]:
        if weeks_in_year(year) != 52:
            continue
        for day in [1, 7, 4, 2, 3, 5, 6]:
            for basic in [False, True]:
                if time.monotonic() >= deadline:
                    print(f"NO COUNTEREXAMPLE {tested}")
                    return
                if check(year, day, basic):
                    return

    rng = random.Random(872341)
    cases = [
        (year, day, basic)
        for year in eligible
        for day in range(1, 8)
        for basic in [False, True]
    ]
    rng.shuffle(cases)

    for year, day, basic in cases:
        if time.monotonic() >= deadline:
            break
        if check(year, day, basic):
            return

    print(f"NO COUNTEREXAMPLE {tested}")


if __name__ == "__main__":
    main()