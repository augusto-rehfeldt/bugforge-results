*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Commas inside valid comments cause strict address parsing to reject a single mailbox

Target: `email.utils.getaddresses`

Property: For a field value consisting of one valid RFC 2822 mailbox followed by a balanced ASCII comment containing a comma, getaddresses([field], strict=True) must return exactly one tuple whose email component equals that mailbox's addr-spec, rather than [('', '')]. Restrict addr-specs to simple ASCII dot-atom local parts and DNS domains, and comments to ASCII letters, spaces, and commas.

### Draft issue: email.utils.getaddresses(strict=True) rejects valid mailboxes with commas in trailing comments

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The getaddresses docstring states: "Return a list of (REALNAME, EMAIL) or ('','') for each fieldvalue." It further states: "If strict is true, use a strict parser which rejects malformed inputs." RFC 2822 comments permit commas; such a comment does not make a mailbox malformed or introduce another address.

**Expected:** Exactly one tuple with email component 'alice@example.com'.

**Actual:** [('', '')]

**Reproducer:**

```python
import email.utils
import re

field = "alice@example.com" + " (team, west)"
# This RFC 2822 subset has a dot-atom addr-spec and balanced ASCII comment.
m = re.fullmatch(r"([A-Za-z]+(?:\.[A-Za-z]+)*@[A-Za-z]+(?:\.[A-Za-z]+)+) \(([A-Za-z ,]*)\)", field)
if not m:
    print("REFUTATION REJECTED: input not independently validated")
else:
    expected = [(m[2], m[1])]
    try:
        actual = email.utils.getaddresses([field], strict=True)
    except Exception as e:
        print("REFUTATION REJECTED:", type(e).__name__, str(e))
    else:
        if len(actual) != 1 or actual[0][1] != m[1]:
            print("REFUTATION CONFIRMED:", repr(field), actual, expected)
        else:
            print("REFUTATION REJECTED: one address with the expected addr-spec")
```

**Output:**

```
REFUTATION CONFIRMED: 'alice@example.com (team, west)' [('', '')] [('team, west', 'alice@example.com')]
```

Judge: BUG (medium) -- The reproducer uses a valid ASCII addr-spec followed by a balanced RFC 2822 comment. A comma inside that comment neither invalidates the mailbox nor separates addresses. The check correctly tests only the number of results and the email component, without requiring a particular real-name interpretation. Returning the failure sentinel rejects valid input contrary to the strict-parser contract. The listed security issues concern malformed-input handling, not this valid-comment regression, and the supplied upstream diff contains no fix.

