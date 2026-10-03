*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: IPv6Address.exploded should support valid scoped IPv6 addresses

Target: `ipaddress.IPv6Address.exploded`

Property: For every valid IPv6Address constructed from 'fe80::1%' followed by a nonempty ASCII alphabetic scope ID, accessing .exploded must return a string representing the address in longhand form, without raising an exception.

### Draft issue: IPv6Address.exploded raises AddressValueError for valid scoped addresses

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** The inherited exploded property in _IPAddressBase promises: "Return the longhand version of the IP address as a string." The IPv6Address documentation permits a scope zone ID appended using '%', giving 'ff02::1234%1' as an example.

**Expected:** fe80:0000:0000:0000:0000:0000:0000:0001%a

**Actual:** AddressValueError: Only hex digits permitted in '1%a' in 'fe80::1%a'

**Reproducer:**

```python
import ipaddress

s = 'fe80::1%' + 'a'
try:
    zone = s.split('%')[1]
    if not zone or not zone.isascii() or not zone.isalpha():
        raise ValueError('scope is not nonempty ASCII alphabetic')
    a = ipaddress.IPv6Address(s)
    n = 0xfe800000000000000000000000000001
    if a.scope_id != zone or int(a) != n:
        raise ValueError('input did not parse as the documented scoped address')
except Exception as e:
    print('REFUTATION REJECTED:', str(e))
else:
    expected = ':'.join(f'{(n >> i) & 65535:04x}' for i in range(112, -1, -16)) + '%' + zone
    try:
        actual = a.exploded
    except Exception as e:
        actual = (type(e).__name__, str(e))
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual), 'expected =', repr(expected))
    else:
        print('REFUTATION REJECTED: exploded matches the documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: 'fe80::1%a' actual = ('AddressValueError', "Only hex digits permitted in '1%a' in 'fe80::1%a'") expected = 'fe80:0000:0000:0000:0000:0000:0000:0001%a'
```

Judge: BUG (medium) -- IPv6Address accepts 'fe80::1%a' as a valid scoped address, and the reproducer verifies both its scope ID and numeric value. The computed longhand address is correct. The documented exploded property promises a longhand string, but instead raises AddressValueError while parsing the scope suffix as hexadecimal address content. No cited documentation excludes scoped addresses from this property. The existing issue concerns help() marking readonly properties and is unrelated.

