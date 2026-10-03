*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Adding zero to a scoped IPv6 address loses its scope

Target: `ipaddress.IPv6Address.__add__`

Property: For every IPv6Address a constructed from a valid IPv6 literal with a nonempty scope ID, adding the integer zero must satisfy a + 0 == a, the additive identity law.

### Draft issue: ipaddress: IPv6Address integer addition discards scope ID

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** Python ipaddress documentation, “Arithmetic operators”: “Addition and subtraction of integers with address objects are supported.” The “Comparison operators” section also states: “Same IPv6 addresses with different scope zone IDs are not equal.” Together these make scope significant to the additive identity invariant.

**Expected:** IPv6Address('fe80::1%eth0'), equal to the original address.

**Actual:** IPv6Address('fe80::1'), unequal to the original because its scope ID is lost.

**Reproducer:**

```python
import ipaddress

s = 'fe80::1%eth0'
try:
    a = ipaddress.IPv6Address(s)
    if not a.scope_id or '%' in a.scope_id:
        print('REFUTATION REJECTED: invalid or empty scope ID')
    else:
        expected = ipaddress.IPv6Address(s)  # Identity preserves the full address.
        actual = a + 0
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual),
                  'expected =', repr(expected))
        else:
            print('REFUTATION REJECTED: additive identity holds')
except Exception as e:
    print('REFUTATION REJECTED:', type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: 'fe80::1%eth0' actual = IPv6Address('fe80::1') expected = IPv6Address('fe80::1%eth0')
```

Judge: BUG (medium) -- The reproducer uses a valid scoped IPv6 literal and correctly compares the result with the original full address. Documented integer addition should preserve identity when adding zero, while documented equality makes the scope significant. Silently dropping the scope violates that identity. None of the listed issues concerns scope loss, and the upstream diff does not fix arithmetic.

