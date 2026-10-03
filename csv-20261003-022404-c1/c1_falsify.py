import csv
import io
import random
import time


def actual(fieldnames, formatting):
    stream = io.StringIO(newline="")
    csv.DictWriter(stream, fieldnames=fieldnames, **formatting).writeheader()
    return stream.getvalue()


def expected(fieldnames, formatting):
    stream = io.StringIO(newline="")
    csv.writer(stream, **formatting).writerow(fieldnames)
    return stream.getvalue()


def outcome(function, fieldnames, formatting):
    try:
        return ("result", function(fieldnames, formatting))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    for fields in (["name", "age"], ["a,b", 'say "hello"', "line\nbreak", ""]):
        got = outcome(actual, fields, {})
        want = outcome(expected, fields, {})
        print("SANITY:", repr(fields), repr(got), repr(want))
        if got != want or want[0] != "result":
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(fields, formatting):
        nonlocal tested
        tested += 1
        got = outcome(actual, fields, formatting)
        want = outcome(expected, fields, formatting)
        if got != want:
            got_again = outcome(actual, fields, formatting)
            want_again = outcome(expected, fields, formatting)
            if got_again == got and want_again == want:
                print("COUNTEREXAMPLE:")
                print(repr({"fieldnames": fields, "formatting": formatting}))
                print("actual:", repr(got))
                print("expected:", repr(want))
                return True
        return False

    formats = [
        {},
        {"delimiter": ";", "lineterminator": "\n"},
        {"quoting": csv.QUOTE_ALL},
        {"quoting": csv.QUOTE_NONNUMERIC},
        {"quoting": csv.QUOTE_NONE, "escapechar": "\\"},
        {"delimiter": "|", "quotechar": "'", "doublequote": False,
         "escapechar": "\\", "lineterminator": "\r\n"},
    ]
    handpicked = [
        [1, True],
        [True, 1],
        [1, 1.0],
        [1.0, 1],
        [0, False],
        [False, 0],
        [0.0, -0.0],
        [-0.0, 0.0],
        [1, True, 1.0],
        [1.0, True, 1],
        [],
        ["ordinary", 2, None],
    ]
    for fields in handpicked:
        for formatting in formats:
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check(fields, formatting):
                return

    rng = random.Random(731902)
    pool = [
        0, False, 0.0, -0.0, 1, True, 1.0, 2, 2.0,
        -1, -1.0, None, "", "ordinary", "a,b", '"quoted"', "x\ny",
    ]
    while time.monotonic() < deadline:
        fields = [rng.choice(pool) for _ in range(rng.randrange(0, 25))]
        if check(fields, rng.choice(formats)):
            return
    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()