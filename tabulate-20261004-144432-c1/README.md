*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `tabulate`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `tabulate` 0.10.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Disabling alignment crashes the AsciiDoc formatter

Target: `tabulate.tabulate`

Property: For nonempty rectangular tables of nonempty ASCII text cells, tabulate(rows, tablefmt='asciidoc', disable_numparse=True, stralign=None) must return a table string without raising an exception, including when headers are supplied.

### Draft issue: AsciiDoc output raises KeyError when stralign=None

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `tabulate` 0.10.0

**Documented behaviour:** The README's column-alignment documentation states: "To disable alignment, use numalign=None and stralign=None." AsciiDoc is listed as a supported table format without an exception to this option.

**Expected:** Return an AsciiDoc table string without raising an exception.

**Actual:** tabulate([['abc']], tablefmt='asciidoc', disable_numparse=True, stralign=None) raises KeyError: None.

**Reproducer:**

```python
import tabulate

case = dict(rows=[["abc"]], tablefmt="asciidoc",
            disable_numparse=True, stralign=None)
rows = case["rows"]
valid = bool(rows) and bool(rows[0]) and all(
    len(row) == len(rows[0]) and all(
        isinstance(cell, str) and bool(cell) and cell.isascii()
        for cell in row
    ) for row in rows
)
# Documented alignment disabling applies to these text-only cells.
expected = "a table string without raising an exception" if valid else None

if not valid:
    print("REFUTATION REJECTED:", "invalid input")
else:
    try:
        result = tabulate.tabulate(
            rows, **{k: v for k, v in case.items() if k != "rows"}
        )
        actual = ("result", result)
        broken = not isinstance(result, str)
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", case, "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "returned a table string", actual)
```

**Output:**

```
REFUTATION CONFIRMED: {'rows': [['abc']], 'tablefmt': 'asciidoc', 'disable_numparse': True, 'stralign': None} actual: ('exception', 'KeyError', 'None') expected: a table string without raising an exception
```

Judge: BUG (medium) -- The reproducer supplies a valid nonempty rectangular table of ASCII text cells. With numeric parsing disabled, stralign=None exercises the documented option to disable text alignment. AsciiDoc is supported without a documented restriction on this option, so raising KeyError violates that promise. The listed Python 3.11 support PR does not report or fix this behavior. The reproducer establishes the failure without headers; it does not test the headers variant.

