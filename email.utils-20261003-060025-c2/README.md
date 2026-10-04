*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Unencoded RFC 2231 continuation text is misinterpreted as charset metadata

Target: `email.utils.decode_params`

Property: For valid RFC 2231 continuations whose initial segment is unencoded and whose later segments are percent-encoded, decode_params must preserve apostrophes in the initial segment as literal value characters, not interpret them as charset/language separators. Specifically, decode_params([('text/plain', ''), ('filename*0', "a'b'"), ('filename*1*', '%63')]) should produce a filename value representing "a'b'c", with no declared charset or language.

### Draft issue: email.utils.decode_params misinterprets apostrophes in unencoded RFC 2231 initial segments

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The email.utils.decode_params documentation promises: "Decode parameters list according to RFC 2231." RFC 2231 section 4 places charset and language information in the initial encoded segment; an unencoded initial segment contains ordinary parameter text.

**Expected:** [('text/plain', ''), ('filename', (None, None, '"a\'b\'c"'))]

**Actual:** [('text/plain', ''), ('filename', ('a', 'b', '"c"'))]

**Reproducer:**

```python
import email.utils as u
import re
from urllib.parse import unquote

p = [('text/plain', ''), ('filename*0', "a'b'"), ('filename*1*', '%63')]
# RFC 2231: contiguous segments; only the starred segment is encoded.
valid = (p[0] == ('text/plain', '') and
         [k for k, v in p[1:]] == ['filename*0', 'filename*1*'] and
         re.fullmatch(r"[A-Za-z0-9']+", p[1][1]) and
         re.fullmatch(r"(?:%[0-9a-fA-F]{2})+", p[2][1]))
if not valid:
    print('REFUTATION REJECTED: invalid RFC 2231 input')
else:
    value = p[1][1] + unquote(p[2][1])
    quoted = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    expected = [p[0], ('filename', (None, None, quoted))]
    actual = u.decode_params(p.copy())
    if actual != expected:
        print('REFUTATION CONFIRMED:', 'input=', repr(p),
              'actual=', repr(actual), 'expected=', repr(expected))
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: input= [('text/plain', ''), ('filename*0', "a'b'"), ('filename*1*', '%63')] actual= [('text/plain', ''), ('filename', ('a', 'b', '"c"'))] expected= [('text/plain', ''), ('filename', (None, None, '"a\'b\'c"'))]
```

Judge: BUG (medium) -- The input is a valid mixed encoded/unencoded RFC 2231 continuation. Because filename*0 is unencoded, its apostrophes are literal characters, not charset/language delimiters. The output incorrectly interprets them after combining the segments, violating the documented RFC 2231 decoding promise. No listed issue duplicates this behaviour, and the supplied upstream diff does not fix it.

