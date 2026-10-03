*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: RFC 2231 continuation assembly should ignore parameter-name casing

Target: `email.headerregistry.ParameterizedMIMEHeader`

Property: For Content-Disposition values containing a filename split into RFC 2231 continuation parameters filename*0* and filename*1*, changing the ASCII letter casing of either parameter name must not change the resulting header.params['filename']; it must equal the concatenation of the decoded segments.

### Draft issue: email: Match RFC 2231 continuation parameter names case-insensitively

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** RFC 2231 §3 states: "The matching of attributes MUST be case-insensitive." ParameterizedMIMEHeader implements the documented MIME parameter mapping, and its source explicitly normalizes parameter names with .lower().

**Expected:** header.params['filename'] == 'report.txt'

**Actual:** header.params['filename'] == '.txt'

**Reproducer:**

```python
import email.headerregistry as hr
import re
from urllib.parse import unquote_to_bytes

s = "attachment; filename*0*=us-ascii''report; FILENAME*1*=.txt"
# Valid RFC 2231: case-insensitive attributes, consecutive segments,
# declared ASCII charset, empty language, and token-safe ASCII values.
m = re.fullmatch(
    r"attachment; filename\*0\*=us-ascii''([A-Za-z]+); filename\*1\*=([A-Za-z.]+)",
    s, re.I | re.ASCII,
)
if not m:
    print("REFUTATION REJECTED: input fails independent validity check")
else:
    expected = b"".join(unquote_to_bytes(v) for v in m.groups()).decode("ascii")
    actual = hr.HeaderRegistry()("Content-Disposition", s).params.get("filename")
    if actual != expected:
        print(f"REFUTATION CONFIRMED: {s!r} actual={actual!r} expected={expected!r}")
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: "attachment; filename*0*=us-ascii''report; FILENAME*1*=.txt" actual='.txt' expected='report.txt'
```

Judge: BUG (medium) -- The input is a valid RFC 2231 continuation with consecutive segments and an ASCII charset declaration. Attribute matching must be case-insensitive, so filename*0* and FILENAME*1* belong to the same parameter. The reproducer correctly computes the decoded concatenation. Returning only the second segment violates that requirement. No duplicate is listed, and the upstream mapping-type change does not address continuation matching.

