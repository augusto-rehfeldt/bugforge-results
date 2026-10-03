*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `csv`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: has_header rejects valid CSV with carriage-return record terminators

Target: `csv.Sniffer.has_header`

Property: For valid rectangular CSV text consisting of a header and at least two data records, with comma-separated fields and records terminated by '\r', Sniffer.has_header(sample) must return a bool rather than raise csv.Error.

### Draft issue: csv.Sniffer.has_header raises csv.Error for valid CR-terminated CSV

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `csv`

**Documented behaviour:** Python csv documentation, Sniffer.has_header(sample): "Analyze the sample text (presumed to be in CSV format) and return True if the first row appears to be a series of column headers." The Dialect.lineterminator documentation also states: "The reader is hard-coded to recognise either '\r' or '\n' as end-of-line."

**Expected:** Return a bool for the valid sample (normally True).

**Actual:** Raises csv.Error: new-line character seen in unquoted field - do you need to open the file with newline=''?

**Reproducer:**

```python
import csv
import io

s = "name,age\r1,2\r3,4\r"
try:
    rows = list(csv.reader(io.StringIO(s, newline=""), delimiter=",", strict=True))
    valid = rows == [["name", "age"], ["1", "2"], ["3", "4"]]
except csv.Error:
    valid = False

if not valid:
    print("REFUTATION REJECTED:", "input failed independent CSV validation")
else:
    expected = bool
    try:
        value = csv.Sniffer().has_header(s)
        actual = ("result", value)
        broken = type(value) is not expected
    except csv.Error as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = False
    if broken:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no violation of the claimed bool/csv.Error property;", actual)
```

**Output:**

```
REFUTATION CONFIRMED: 'name,age\r1,2\r3,4\r' actual: ('exception', 'Error', "new-line character seen in unquoted field - do you need to open the file with newline=''?") expected: <class 'bool'>
```

Judge: BUG (medium) -- The reproducer independently validates the sample as three rectangular CSV records using newline=''. Bare '\r' record endings are explicitly supported by csv.reader. has_header internally reads the sample through StringIO without appropriate newline handling, causing an avoidable parsing error rather than returning its documented boolean result. This is not merely an inaccurate header heuristic. The supplied upstream diff leaves this parsing path unchanged, and no duplicate was found.

