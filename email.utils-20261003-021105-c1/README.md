*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: formataddr is not inverted by parseaddr for valid quoted local parts containing '['

Target: `email.utils.formataddr`

Property: For pairs (name, address) where name is a nonempty ASCII alphabetic display name and address is an RFC 2822-valid addr-spec with a quoted ASCII local part containing '[', parseaddr(formataddr((name, address))) must equal (name, address), using parseaddr's default arguments.

### Draft issue: email.utils.parseaddr rejects a valid quoted local part containing '['

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** email.utils.formataddr documentation and docstring: "The inverse of parseaddr(), this takes a 2-tuple of the form (realname, email_address) and returns the string value suitable for an RFC 2822 From, To or Cc header."

**Expected:** ('Alice', '"a[b"@example.com')

**Actual:** ('', '')

**Reproducer:**

```python
import email.utils as e
import re

pair = ('Alice', '"a[b"@example.com')
name, address = pair
# RFC 2822 quoted-string qtext permits "["; example.com is a valid domain.
if not (re.fullmatch(r'[A-Za-z]+', name) and
        re.fullmatch(r'"[\x21\x23-\x5b\x5d-\x7e]+"@example\.com', address)):
    print('REFUTATION REJECTED: input validity not established')
else:
    expected = (name, address)  # Independently derived from the inverse promise.
    actual = e.parseaddr(e.formataddr(pair))
    if actual != expected:
        print('REFUTATION CONFIRMED:', pair, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: documented round trip succeeds')
```

**Output:**

```
REFUTATION CONFIRMED: ('Alice', '"a[b"@example.com') actual: ('', '') expected: ('Alice', '"a[b"@example.com')
```

Judge: BUG (low) -- The concrete input is valid: RFC 2822 permits '[' inside a quoted local part. formataddr produces 'Alice <"a[b"@example.com>', a valid mailbox, but default parseaddr rejects it, violating the documented inverse relationship. This is a strict-parsing false rejection, not invalid input or a documented limitation. None of the listed issues reports this specific behavior, and the shown upstream changes do not fix it.

