import csv
import io

fields = [1, True]
formatting = {}
case = {"fieldnames": fields, "formatting": formatting}
try:
    for field in fields:
        hash(field)  # Valid dictionary keys; fieldnames is a finite sequence.
    actual, expected = io.StringIO(), io.StringIO()
    csv.DictWriter(actual, fieldnames=fields, **formatting).writeheader()
    csv.writer(expected, **formatting).writerow(fields)
    actual, expected = actual.getvalue(), expected.getvalue()
    if actual != expected:
        print("REFUTATION CONFIRMED:", case, "actual:", repr(actual),
              "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
except Exception as exc:
    print("REFUTATION REJECTED:", type(exc).__name__, str(exc))