*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `doc-bug`: RFC 2231 encoding without charset or language preserves the input

Target: `email.utils.encode_rfc2231`

Property: For every ASCII string s, encode_rfc2231(s, charset=None, language=None) == s.

### Draft issue: Clarify encode_rfc2231 docstring: values are quoted even without charset or language

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The encode_rfc2231 docstring states: "If neither charset nor language is given, then s is returned as-is."

**Expected:** The docstring promises 'a b' unchanged when charset and language are both None.

**Actual:** Returns 'a%20b'.

**Reproducer:**

```python
import email.utils

s = "a b"
if not s.isascii():
    print("REFUTATION REJECTED: input is not ASCII")
else:
    actual = email.utils.encode_rfc2231(s, charset=None, language=None)
    expected = s  # Documented return when neither argument is given.
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), repr(actual), repr(expected))
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: 'a b' 'a%20b' 'a b'
```

Judge: DOC_BUG (low) -- The ASCII input is valid and the reproducer correctly demonstrates a docstring mismatch. Percent-encoding the space is reasonable for an RFC 2231 encoder; the incorrect part is the promise that omitting charset and language returns the original string unchanged. The supplied upstream diff does not fix this mismatch, and the listed Unicode issue does not report the same behaviour.

