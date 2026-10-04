import email.utils
import random
import time


def reference_year(year):
    # RFC 2822 §4.3: add 1900 to an obsolete three-digit year.
    return year + 1900 if 100 <= year <= 999 else year


def observe(text):
    try:
        return email.utils.parsedate_tz(text)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def agrees(result, expected):
    return (
        isinstance(result, tuple)
        and len(result) == 10
        and result[0] == expected
    )


def main():
    deadline = time.monotonic() + 170

    for year in (2000, 2024):
        text = f"01 Jan {year} 12:00:00 +0000"
        expected = reference_year(year)
        actual = observe(text)
        print(f"SANITY: {text!r} actual={actual!r} expected_year={expected!r}")
        if not agrees(actual, expected):
            print("SANITY FAILED")
            return

    rng = random.Random(2822)
    tested = 0

    def inputs():
        yield from (100, 101, 499, 999, 189, 190, 199, 200, 998)
        for _ in range(100000):
            yield rng.randint(100, 999)

    for year in inputs():
        if time.monotonic() >= deadline:
            break

        text = f"01 Jan {year:03d} 12:00:00 +0000"
        expected = reference_year(year)
        actual = observe(text)
        tested += 1

        if not agrees(actual, expected):
            repeated = observe(text)
            if repeated == actual and not agrees(repeated, expected):
                print(
                    f"COUNTEREXAMPLE: {text!r} "
                    f"actual={repeated!r} expected_year={expected!r}"
                )
                return

    print(f"NO COUNTEREXAMPLE {tested}")


if __name__ == "__main__":
    main()