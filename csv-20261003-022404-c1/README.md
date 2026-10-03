*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `csv`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: writeheader loses distinct field names that compare equal

Target: `csv.DictWriter.writeheader`

Property: For a finite sequence of field names accepted as dictionary keys, writeheader() must produce the same CSV row as csv.writer(...).writerow(fieldnames) under identical formatting parameters. In particular, distinct field names that compare equal must retain their individual string representations.

### Draft issue: csv.DictWriter.writeheader loses field-name representations for equal keys

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

**Documented behaviour:** Python csv documentation, DictWriter.writeheader(): “Write a row with the field names (as specified in the constructor) to the writer’s file object, formatted according to the current dialect.”

**Expected:** '1,True\r\n'

**Actual:** 'True,True\r\n'

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'fieldnames': [1, True], 'formatting': {}} actual: 'True,True\r\n' expected: '1,True\r\n'
```

Judge: BUG (low) -- The documented promise is to write the constructor's field names, and no restriction excludes non-string dictionary keys or distinct objects that compare equal. The reproducer correctly compares identical formatting. writeheader() constructs a dictionary mapping field names to themselves; because 1 and True are equal keys, True overwrites the value for 1, corrupting the first header. The supplied upstream diff does not change this behavior, and the listed return-value issue is unrelated.

