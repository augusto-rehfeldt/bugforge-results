*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `difflib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: HtmlDiff line wrapping exhausts the recursion limit on long lines

Target: `difflib.HtmlDiff.make_table`

Property: For any finite nonempty ASCII string s containing only letters, HtmlDiff(wrapcolumn=1).make_table([s], [s]) must return an HTML table string rather than raise RecursionError, including when len(s) exceeds the interpreter's recursion limit.

### Draft issue: HtmlDiff.make_table raises RecursionError when wrapping long lines at column 1

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

**Documented behaviour:** HtmlDiff.make_table documentation: "Compares fromlines and tolines (lists of strings) and returns a string which is a complete HTML table containing a side by side, line by line comparison with change highlights." HtmlDiff constructor documentation: "wrapcolumn -- column number where lines are broken and wrapped, defaults to None where lines are not wrapped."

**Expected:** Return an HTML table string with the identical lines wrapped at column 1.

**Actual:** Raises RecursionError: maximum recursion depth exceeded.

**Reproducer:**

```python
import difflib

s = "a" * 999
expected = "HTML table string (no exception)"
if not (s and s.isascii() and s.isalpha()):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        result = difflib.HtmlDiff(wrapcolumn=1).make_table([s], [s])
        valid = isinstance(result, str) and "<table" in result and "</table>" in result
        actual = expected if valid else repr(result)
    except Exception as e:
        valid = False
        actual = f"{type(e).__name__}: {e}"
    if valid:
        print("REFUTATION REJECTED: documented HTML table returned")
    else:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' actual: RecursionError: maximum recursion depth exceeded expected: HTML table string (no exception)
```

Judge: BUG (medium) -- The reproducer supplies valid lists of identical ASCII strings and a valid wrapcolumn. The documented wrapping operation should produce an HTML table; a 999-character line is not an unreasonable resource demand. RecursionError exposes an implementation limit in line wrapping, not a documented input restriction. The supplied upstream diff does not change the wrapping implementation, and no duplicate issues are listed. Although this example does not establish that the string exceeds the recursion limit, its observed failure still demonstrates the bug.

