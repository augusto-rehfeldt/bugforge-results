import math
from tabulate import tabulate, simple_separated_format

rows = [[1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, "large"], [1.5, "small"]]
valid = all(
    len(row) == 2
    and ((type(n) is int and len(str(abs(n))) <= 1000)
         or (type(n) is float and math.isfinite(n)))
    and isinstance(label, str) and label and label.isascii()
    for row in rows for n, label in [row]
)
if not valid:
    print("REFUTATION REJECTED:", "input outside the stated domain")
else:
    expected = {"returns_string": True, "separated_labels": [r[1] for r in rows]}
    try:
        result = tabulate(rows, tablefmt=simple_separated_format("|"))
        parts = [line.split("|") for line in result.splitlines()] if isinstance(result, str) else []
        actual = {
            "returns_string": isinstance(result, str),
            "separated_labels": [p[1].strip() for p in parts] if all(len(p) == 2 for p in parts) else None,
        }
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", rows, actual, expected)
    else:
        print("REFUTATION REJECTED:", "returned a string with both columns separated by '|'")