*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Valid MIME version numbers can exceed Python's integer-conversion limit

Target: `email.headerregistry.MIMEVersionHeader.parse`

Property: For values consisting of two nonempty ASCII decimal digit strings separated by '.', HeaderRegistry()('MIME-Version', value) must construct a header without raising a parsing exception, including when either digit string exceeds Python's active integer-string conversion limit.

### Draft issue: MIME-Version header parsing leaks ValueError for oversized numeric components

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** MIMEVersionHeader.value_parser documents the grammar as "mime-version = [CFWS] 1*digit [CFWS] \".\" [CFWS] 1*digit [CFWS]". BaseHeader's subclass contract states: "The parser should not, insofar as practical, raise any errors. Defects should be added to the list instead." Neither grammar repetition imposes a digit-count bound.

**Expected:** Construct the header without raising; record a defect if the version components cannot be represented under the active conversion limit.

**Actual:** Header construction raises ValueError when the major version contains 4301 digits and the integer-string conversion limit is 4300.

**Reproducer:**

```python
import re
import sys
import email.headerregistry as hr

limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
value = "1" * (limit + 1 if limit else 4301) + ".0"
expected = "constructed without exception" if re.fullmatch(r"[0-9]+\.[0-9]+", value) else None

if expected is None:
    print("REFUTATION REJECTED: input does not match the documented grammar")
else:
    try:
        hr.HeaderRegistry()("MIME-Version", value)
    except Exception as e:
        print(f"REFUTATION CONFIRMED: input={value!r}\nactual: {type(e).__name__}: {e}\nexpected: {expected}")
    else:
        print("REFUTATION REJECTED: constructed without exception")
```

**Output:**

```
111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111.0'
actual: ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits() to increase the limit
expected: constructed without exception
```

Judge: BUG (medium) -- The reproducer supplies nonempty ASCII digit sequences matching the documented MIME-version grammar. The active integer-conversion limit causes an uncaught ValueError rather than a constructed header with defects, contrary to the parser's documented error-tolerance contract. Handling this predictable conversion failure is practical and does not require disabling the safety limit. No supplied issue or upstream change addresses it.

