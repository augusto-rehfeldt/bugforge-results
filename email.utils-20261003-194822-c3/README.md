*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Strict address parsing accepts consecutive dots in an unquoted local part

Target: `email.utils.parseaddr`

Property: For nonempty ASCII alphabetic strings a and b and a valid ASCII domain d, parseaddr(a + '..' + b + '@' + d, strict=True) must return ('', ''), because consecutive dots are invalid in an unquoted RFC 2822 local part.

### Draft issue: email.utils.parseaddr(strict=True) accepts consecutive dots in an unquoted local part

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** "If strict is True, use a strict parser which rejects malformed inputs." — email.utils.parseaddr docstring.

**Expected:** ('', '')

**Actual:** ('', 'a..b@example.com')

**Reproducer:**

```python
import email.utils
import re

a, b, d = 'a', 'b', 'example.com'
s = a + '..' + b + '@' + d
atom = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
domain = r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)+'

if not (re.fullmatch('[A-Za-z]+', a + b) and re.fullmatch(domain, d)):
    print('REFUTATION REJECTED:', 'invalid test parameters')
else:
    # Malformed strings are in scope: strict=True promises to reject them.
    expected = ('', s) if re.fullmatch(atom + r'(?:\.' + atom + r')*@' + domain, s) else ('', '')
    try:
        actual = email.utils.parseaddr(s, strict=True)
    except Exception as e:
        print('REFUTATION REJECTED:', type(e).__name__, str(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
        else:
            print('REFUTATION REJECTED:', 'result matches expectation')
```

**Output:**

```
REFUTATION CONFIRMED: 'a..b@example.com' ('', 'a..b@example.com') ('', '')
```

Judge: BUG (medium) -- The reproducer correctly expects rejection: a..b@example.com contains an empty, unquoted local-part atom and is malformed under RFC 2822. Malformed input is in scope because strict=True explicitly promises to reject it. The reported result instead preserves the invalid address. The supplied upstream diff shows no parseaddr fix, and the listed issues do not establish a duplicate of this strict-mode consecutive-dot case.

