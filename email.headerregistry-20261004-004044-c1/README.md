*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Address loses necessary quoting in domain literals

Target: `email.headerregistry.Address`

Property: For an ASCII addr_spec with local part 'user' and an RFC 5322 domain literal containing a valid quoted-pair, if Address(addr_spec=s) succeeds, constructing Address(addr_spec=Address(addr_spec=s).addr_spec) must also succeed and preserve username and domain.

### Draft issue: email.headerregistry.Address fails to escape closing brackets in domain literals

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** Address.__init__ documentation: "The addr_spec and the string value of the object are both quoted according to RFC5322 rules, but without any Content Transfer Encoding."

**Expected:** addr_spec preserves the escaped closing bracket, producing a parseable address whose username and domain match the original object's.

**Actual:** Address accepts 'user@[a\]b]' but serializes it as 'user@[a]b]'; reconstructing from that value raises ValueError.

**Reproducer:**

```python
import re
from email.headerregistry import Address

s = r'user@[a\]b]'
# RFC 5322: domain-literal = "[" *(dtext / quoted-pair) "]".
valid = re.fullmatch(r'user@\[(?:[\x21-\x5a\x5e-\x7e]|\\[\x09\x20-\x7e])*\]', s)
if not valid:
    print("REFUTATION REJECTED:", "input is not an RFC 5322 domain literal")
else:
    expected = ('user', re.sub(r'\\(.)', r'\1', s[5:]))
    try:
        a = Address(addr_spec=s)
    except Exception as e:
        print("REFUTATION REJECTED:", "initial construction failed:", repr(e))
    else:
        actual = {'initial': (a.username, a.domain), 'serialized': a.addr_spec}
        try:
            b = Address(addr_spec=a.addr_spec)
            result = (b.username, b.domain)
        except Exception as e:
            result = ('EXCEPTION', type(e).__name__, str(e))
        actual['reconstructed'] = result
        if actual['initial'] == expected and result != expected:
            print("REFUTATION CONFIRMED:", repr(s), actual, expected)
        else:
            print("REFUTATION REJECTED:", "reported failure not reproduced",
                  repr(s), actual, expected)
```

**Output:**

```
REFUTATION CONFIRMED: 'user@[a\\]b]' {'initial': ('user', '[a]b]'), 'serialized': 'user@[a]b]', 'reconstructed': ('EXCEPTION', 'ValueError', "Invalid addr_spec; only 'user@[a]' could be parsed from 'user@[a]b]'")} ('user', '[a]b]')
```

Judge: BUG (medium) -- The input is valid under RFC 5322's obsolete syntax: obs-dtext permits quoted-pair, including an escaped closing bracket. Address accepts it and decodes the domain correctly, but addr_spec emits the decoded bracket without escaping it. This violates the documented RFC 5322 quoting promise and makes the serialized address unparsable. The supplied upstream diff does not fix this behavior, and no duplicate is listed.

