*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `csv`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: DictReader.line_num misses trailing blank lines at EOF

Target: `csv.DictReader`

Property: For a DictReader constructed over a finite iterable of CSV lines, after iteration is exhausted, line_num equals the number of physical lines consumed from that iterable, including trailing blank lines.

### Draft issue: csv.DictReader.line_num is stale after skipping trailing blank lines

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

**Documented behaviour:** The Python csv documentation, under DictReader.line_num, says: “The number of lines read from the source iterator. This is not the same as the number of records returned, as records can span multiple lines.”

**Expected:** After exhaustion, reader.line_num == 3.

**Actual:** All three source lines are consumed, but reader.line_num == 2.

**Reproducer:**

```python
import csv

lines = ['name\n', '\n', '\n']
if list(csv.reader(lines)) != [['name'], [], []]:
    print('REFUTATION REJECTED: input is not a header followed by valid blank CSV lines')
else:
    consumed = []
    reader = csv.DictReader(consumed.append(line) or line for line in lines)
    list(reader)
    actual, expected = reader.line_num, len(consumed)
    if actual != expected:
        print('REFUTATION CONFIRMED:', lines, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: line_num equals the number of source lines consumed')
```

**Output:**

```
REFUTATION CONFIRMED: ['name\n', '\n', '\n'] actual: 2 expected: 3
```

Judge: BUG (low) -- The input is valid, and the instrumented iterator correctly records three consumed physical lines. DictReader updates line_num after reading the first blank row, but not while skipping subsequent blank rows before StopIteration, leaving it stale. This violates the documented count of source lines read. The supplied upstream diff does not change DictReader. The listed property proposal is related but does not specifically report or demonstrate a fix for this exhaustion behaviour.

