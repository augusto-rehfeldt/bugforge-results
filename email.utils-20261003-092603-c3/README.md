*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Strict parseaddr accepts an unterminated angle address

Target: `email.utils.parseaddr`

Property: For an ASCII display-name atom n and a valid ASCII addr-spec a, parseaddr(n + ' <' + a, strict=True) must return ('', ''), because the angle address is malformed without its required closing '>'.

### Draft issue: email.utils.parseaddr(strict=True) accepts angle address without closing '>'

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** email.utils.parseaddr docstring: "If strict is True, use a strict parser which rejects malformed inputs." It also states: "Return a tuple of realname and email address, unless the parse fails, in which case return a 2-tuple of ('', '')."

**Expected:** ('', '')

**Actual:** ('Alice', 'alice@example.com')

**Reproducer:**

```python
import re
from email.utils import parseaddr

n, a = "Alice", "alice@example.com"
s = n + " <" + a
if not (re.fullmatch(r"[A-Za-z]+", n, re.ASCII) and
        re.fullmatch(r"[A-Za-z]+@[A-Za-z]+\.[A-Za-z]+", a, re.ASCII)):
    print("REFUTATION REJECTED: invalid display-name atom or addr-spec")
else:
    # This valid name and addr-spec lack the angle address's required '>'.
    expected = ("", "") if s.count("<") != s.count(">") else None
    try:
        actual = parseaddr(s, strict=True)
    except Exception as e:
        print(f"REFUTATION REJECTED: {type(e).__name__}: {e}")
    else:
        if expected is not None and actual != expected:
            print(f"REFUTATION CONFIRMED: {s!r} actual={actual!r} expected={expected!r}")
        else:
            print("REFUTATION REJECTED: malformed input was rejected")
```

**Output:**

```
REFUTATION CONFIRMED: 'Alice <alice@example.com' actual=('Alice', 'alice@example.com') expected=('', '')
```

Judge: BUG (medium) -- strict=True explicitly promises to reject malformed inputs. The reproducer supplies a valid ASCII name and addr-spec but omits the required closing angle bracket, so rejection is the documented behavior. The observed result instead accepts the malformed address. Neither listed issue establishes a duplicate, and the supplied upstream diff shows no parseaddr fix.

