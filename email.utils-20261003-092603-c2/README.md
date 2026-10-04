*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: RFC 2231 continuations fail to combine when attribute casing differs

Target: `email.utils.decode_params`

Property: For a valid RFC 2231 parameter split into numbered continuation segments, changing only the ASCII letter casing of the attribute name on individual segments must not change the decoded parameter value: all segments must still combine in numerical order into one parameter.

### Draft issue: email.utils.decode_params fails to combine RFC 2231 continuations with mixed-case attribute names

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** email.utils.decode_params docstring: "Decode parameters list according to RFC 2231." RFC 2231 extends MIME parameter syntax; RFC 2045 §5.1 specifies: "The matching of attributes is ALWAYS case-insensitive."

**Expected:** [('text/plain', ''), ('filename', '"report.txt"')]

**Actual:** [('text/plain', ''), ('filename', '"report"'), ('FILENAME', '".txt"')]

**Reproducer:**

```python
import email.utils, re

p = [('text/plain', ''), ('filename*0', 'report'), ('FILENAME*1', '.txt')]
s = [(re.fullmatch(r'([A-Za-z]+)\*(0|[1-9][0-9]*)', k), v) for k, v in p[1:]]
# These names and values are valid RFC 2045 tokens; attributes ignore case.
if (not all(m and re.fullmatch(r'[A-Za-z.]+', v) for m, v in s)
    or len({m[1].lower() for m, v in s}) != 1
    or sorted(int(m[2]) for m, v in s) != list(range(len(s)))):
    print('REFUTATION REJECTED: invalid continuation input')
else:
    expected = [p[0], (s[0][0][1].lower(),
                       '"' + ''.join(v for m, v in sorted(s, key=lambda x: int(x[0][2]))) + '"')]
    actual = email.utils.decode_params(p)
    if actual != expected:
        print('REFUTATION CONFIRMED:', 'input:', p, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: input: [('text/plain', ''), ('filename*0', 'report'), ('FILENAME*1', '.txt')] actual: [('text/plain', ''), ('filename', '"report"'), ('FILENAME', '".txt"')] expected: [('text/plain', ''), ('filename', '"report.txt"')]
```

Judge: BUG (medium) -- The input contains valid, contiguous RFC 2231 continuation segments numbered 0 and 1. MIME parameter attributes are case-insensitive, so filename and FILENAME identify the same parameter. The reproducer correctly expects their values to concatenate in numerical order; the failure is not merely output-name casing. decode_params instead separates the segments by attribute casing. No matching issue or fix is listed, and the upstream diff contains no change to this behavior.

