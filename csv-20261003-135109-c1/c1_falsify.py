import csv
import random
import time
from decimal import Decimal, InvalidOperation


def reference(sample, terminator):
    """Validate the restricted CSV grammar independently; infer its header."""
    assert sample.endswith(terminator)
    records = sample[:-len(terminator)].split(terminator)
    assert len(records) >= 3
    rows = [record.split(",") for record in records]
    assert all(len(row) == 2 for row in rows)
    assert all(field and field.isascii() and field.isalpha()
               for field in rows[0])
    for row in rows[1:]:
        for field in row:
            assert field and field == field.strip()
            try:
                value = Decimal(field)
            except InvalidOperation:
                raise AssertionError("Invalid numeric field")
            assert value.is_finite()
    return True


def invoke(sample):
    try:
        return ("result", csv.Sniffer().has_header(sample))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def violates(outcome):
    return (
        outcome[0] == "exception" and outcome[1] == "Error"
    ) or (
        outcome[0] == "result" and type(outcome[1]) is not bool
    )


def main():
    for sample in (
        "name,age\n1,2\n3,4\n",
        "left,right\r\n10,20\r\n30,40\r\n",
    ):
        terminator = "\r\n" if "\r\n" in sample else "\n"
        expected = reference(sample, terminator)
        actual = invoke(sample)
        print("SANITY:", repr(sample), "actual:", actual, "expected:", expected)
        if actual != ("result", expected):
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0

    def check(sample):
        nonlocal tested
        reference(sample, "\r")
        tested += 1
        actual = invoke(sample)
        if violates(actual):
            repeated = invoke(sample)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(sample),
                      "actual:", actual, "expected: bool")
                return True
        return False

    edges = (
        "name,age\r1,2\r3,4\r",
        "a,b\r0,0\r0,0\r",
        "Alpha,Beta\r-1,+2\r+3,-4\r",
        "x,y\r1.5,2.5\r3.5,4.5\r",
        "longheader,otherheader\r1000000000000000000,2\r3,4\r",
    )
    for sample in edges:
        if check(sample):
            return

    rng = random.Random(812739)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    while time.monotonic() - start < 180:
        headers = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 24)))
            for _ in range(2)
        ]
        records = [",".join(headers)]
        for _ in range(rng.randint(2, 30)):
            records.append(",".join(
                str(rng.randint(-10**12, 10**12)) for _ in range(2)
            ))
        if check("\r".join(records) + "\r"):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()