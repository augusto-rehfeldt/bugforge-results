*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Strict address parsing rejects valid IPv4 domain literals

Target: `email.utils.getaddresses`

Property: For every RFC 2822 mailbox of the form local@[a.b.c.d], where local is a nonempty ASCII alphabetic dot-atom and a, b, c, d are decimal integers from 0 through 255, getaddresses([mailbox], strict=True) must return [('', mailbox)], rather than treating the valid mailbox as a parsing failure.

### Draft issue: email.utils.getaddresses rejects valid domain-literal addresses in strict mode

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The email.utils documentation describes getaddresses as: "Return a list of 2-tuples of the form returned by parseaddr()." It specifies: "If strict is true, use a strict parser which rejects malformed inputs." RFC 2822 domain-literal mailboxes are valid inputs, not malformed ones.

**Expected:** [('', 'alice@[127.0.0.1]')]

**Actual:** [('', '')]

**Reproducer:**

```python
import email.utils
import re

mailbox = "alice@" + "[127.0.0.1]"
m = re.fullmatch(r"[A-Za-z]+(?:\.[A-Za-z]+)*@\[(\d+\.\d+\.\d+\.\d+)\]", mailbox, re.ASCII)
if not m or not all(0 <= int(n) <= 255 for n in m[1].split(".")):
    print("REFUTATION REJECTED:", "input is not the claimed RFC 2822 mailbox")
else:
    expected = [("", mailbox)]
    try:
        actual = email.utils.getaddresses([mailbox], strict=True)
    except Exception as exc:
        print("REFUTATION REJECTED:", "call did not return:", repr(exc))
    else:
        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(mailbox), "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED:", "actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: 'alice@[127.0.0.1]' actual: [('', '')] expected: [('', 'alice@[127.0.0.1]')]
```

Judge: BUG (medium) -- alice@[127.0.0.1] is a valid RFC 2822 mailbox: an ASCII dot-atom local part followed by a domain literal. The reproducer validates this input and compares against the correct address tuple. Rejecting it as malformed in strict mode breaks the documented parsing contract. No matching issue or fix is listed, and the supplied upstream diff does not change getaddresses.

