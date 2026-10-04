*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `tabulate`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `tabulate` 0.10.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Mixed numeric columns should remain printable when an integer exceeds float range

Target: `tabulate.simple_separated_format`

Property: For two-column tables whose first column contains finite Python integers and floats and whose second column contains nonempty ASCII labels, tabulate(rows, tablefmt=simple_separated_format('|')) should produce a string with both columns separated by '|', rather than raising OverflowError. Restrict integers to at most 1000 decimal digits so Python's integer-string conversion limit is not implicated.

### Draft issue: Mixed large-integer and float columns raise OverflowError during formatting

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `tabulate` 0.10.0

**Documented behaviour:** The simple_separated_format docstring says: "Construct a simple TableFormat with columns separated by a separator." Its example demonstrates passing mixed text and numeric cells to tabulate with the resulting format. The tabulate API describes its operation as "Format a fixed width table for pretty printing."

**Expected:** Return a formatted string with two columns separated by '|', preserving the labels 'large' and 'small'.

**Actual:** Raises OverflowError: int too large to convert to float.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: [[1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 'large'], [1.5, 'small']] {'exception': 'OverflowError', 'message': 'int too large to convert to float'} {'returns_string': True, 'separated_labels': ['large', 'small']}
```

Judge: BUG (medium) -- The reproducer uses valid finite numeric cells and nonempty ASCII labels; the integer is within the stated digit limit. Formatting mixed numeric cells should not fail merely because a Python integer exceeds float range. This is an unhandled conversion overflow, not floating-point rounding or a separator-checking error. No duplicate was supplied.

