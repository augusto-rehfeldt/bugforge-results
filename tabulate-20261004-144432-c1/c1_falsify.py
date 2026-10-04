import random
import string
import time
from tabulate import tabulate


def reference(case):
    """Documented property: valid text tables must return a string."""
    rows = case["rows"]
    assert isinstance(rows, list) and rows
    width = len(rows[0])
    assert width > 0

    def valid_cell(cell):
        return (
            isinstance(cell, str)
            and bool(cell)
            and all(c in string.ascii_letters for c in cell)
        )

    assert all(len(row) == width for row in rows)
    assert all(valid_cell(cell) for row in rows for cell in row)
    if "headers" in case:
        assert len(case["headers"]) == width
        assert all(valid_cell(cell) for cell in case["headers"])
    return "a table string without raising an exception"


def evaluate(case):
    kwargs = dict(case)
    rows = kwargs.pop("rows")
    try:
        result = tabulate(rows, **kwargs)
        return isinstance(result, str), ("result", result)
    except Exception as exc:
        return False, ("exception", type(exc).__name__, str(exc))


def make_case(rows, headers=None, both=False):
    case = {
        "rows": rows,
        "tablefmt": "asciidoc",
        "disable_numparse": True,
        "stralign": None,
    }
    if headers is not None:
        case["headers"] = headers
    if both:
        case["numalign"] = None
    return case


def main():
    deadline = time.monotonic() + 175
    tested = 0

    # Ordinary, aligned inputs check the independently defined return contract.
    for case in (
        {
            "rows": [["abc"]],
            "tablefmt": "asciidoc",
            "disable_numparse": True,
        },
        {
            "rows": [["Alice", "Paris"], ["Bob", "Rome"]],
            "headers": ["Name", "City"],
            "tablefmt": "asciidoc",
            "disable_numparse": True,
        },
    ):
        expected = reference(case)
        ok, actual = evaluate(case)
        tested += 1
        print("SANITY:", repr(case), repr(actual), "EXPECTED:", expected)
        if not ok:
            print("SANITY FAILED")
            return

    def check(case):
        nonlocal tested
        expected = reference(case)
        ok, actual = evaluate(case)
        tested += 1
        if not ok:
            repeated_ok, repeated_actual = evaluate(case)
            if not repeated_ok:
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("ACTUAL:", repr(actual))
                print("REPEATED ACTUAL:", repr(repeated_actual))
                print("EXPECTED:", expected)
                return True
        return False

    edges = [
        make_case([["abc"]]),
        make_case([["abc"]], both=True),
        make_case([["abc"]], ["Header"]),
        make_case([["abc"]], ["Header"], both=True),
    ]
    for rows in (
        [["a", "bc"]],
        [["a"], ["abcdef"]],
        [["a", "Longword"], ["Longerword", "b"]],
        [["A"] * 12],
        [["Alphabetic" * 100]],
    ):
        for both in (False, True):
            edges.append(make_case(rows, both=both))
            edges.append(make_case(rows, ["Header"] * len(rows[0]), both))

    for case in edges:
        if time.monotonic() >= deadline:
            break
        if check(case):
            return

    rng = random.Random(731924)
    while time.monotonic() < deadline:
        height = rng.randint(1, 15)
        width = rng.randint(1, 12)

        def text():
            return "".join(
                rng.choice(string.ascii_letters)
                for _ in range(rng.randint(1, 80))
            )

        rows = [[text() for _ in range(width)] for _ in range(height)]
        headers = [text() for _ in range(width)] if rng.randrange(2) else None
        if check(make_case(rows, headers, bool(rng.randrange(2)))):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()