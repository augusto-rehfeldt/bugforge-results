import configparser
import io
import random
import time

INVALID_WRITE_ERROR = getattr(configparser, "InvalidWriteError", None)


def check_value(value):
    parser = configparser.RawConfigParser()
    parser.add_section("s")
    parser.set("s", "key", value)
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        if INVALID_WRITE_ERROR is not None and isinstance(exc, INVALID_WRITE_ERROR):
            return ("InvalidWriteError",)
        return ("write exception", type(exc).__name__, str(exc))

    text = output.getvalue()
    fresh = configparser.RawConfigParser()
    try:
        fresh.read_string(text)
        actual = fresh.get("s", "key")
    except Exception as exc:
        return ("read exception", type(exc).__name__, str(exc), text)
    return ("value", actual, text)


def acceptable(result, expected):
    return result == ("InvalidWriteError",) or (
        result[0] == "value" and result[1] == expected
    )


def main():
    deadline = time.monotonic() + 175.0

    for ordinary in ("value", "ordinary text"):
        expected = ordinary  # Exact preservation is the independent reference.
        result = check_value(ordinary)
        agrees = result[0] == "value" and result[1] == expected
        print("SANITY:", repr(ordinary), "PASS" if agrees else "FAIL")
        if not agrees:
            print("SANITY FAILED")
            return

    tested = 0

    def test(left, right):
        nonlocal tested
        expected = left + "value" + right
        result = check_value(expected)
        tested += 1
        if acceptable(result, expected):
            return False

        repeated = check_value(expected)
        if acceptable(repeated, expected) or repeated != result:
            return False

        print("COUNTEREXAMPLE:")
        print(repr({"L": left, "R": right}))
        print("actual:", repr(result))
        print("expected:", repr(("exact value", expected, "or InvalidWriteError")))
        return True

    edges = [
        (" ", ""),
        ("", " "),
        ("\t", ""),
        ("", "\t"),
        (" ", " "),
        ("\t", "\t"),
        (" \t", "\t "),
        ("  ", ""),
        ("", "\t\t"),
        (" \t ", "\t \t"),
    ]
    for left, right in edges:
        if time.monotonic() >= deadline:
            break
        if test(left, right):
            return

    rng = random.Random(728193)
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        left = "".join(rng.choice(" \t") for _ in range(rng.randrange(9)))
        right = "".join(rng.choice(" \t") for _ in range(rng.randrange(9)))
        if not left and not right:
            continue
        if test(left, right):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()