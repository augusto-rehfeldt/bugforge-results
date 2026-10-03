*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: IPv6Interface.with_prefixlen loses the scope ID

Target: `ipaddress.IPv6Interface.with_prefixlen`

Property: For every IPv6Interface i constructed from 'fe80::1%' + zone + '/' + str(p), with a nonempty ASCII alphabetic zone and integer p in [0, 128], IPv6Interface(i.with_prefixlen) must equal i, retaining both its scope ID and prefix length.

### Draft issue: ipaddress.IPv6Interface.with_prefixlen drops IPv6 scope IDs

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** The IPv6Interface documentation inherits the IPv4Interface attribute with_prefixlen: "A string representation of the interface with the mask in prefix notation." The IPv6Address documentation permits a scope zone ID appended with '%'.

**Expected:** with_prefixlen returns 'fe80::1%eth/0', preserving scope 'eth' and prefix length 0 on reconstruction.

**Actual:** with_prefixlen returns 'fe80::1/0'; reconstruction retains prefix length 0 but loses the scope ID.

**Reproducer:**

```python
import ipaddress as ip

s = 'fe80::1%eth/0'
address, prefix = s.split('/')
base, zone = address.split('%')
p = int(prefix)
try:
    if not (zone.isascii() and zone.isalpha() and 0 <= p <= 128):
        raise ValueError('input outside documented domain')
    i = ip.IPv6Interface(s)
    expected = (int(ip.IPv6Address(base)), zone, p)
    if (int(i), i.scope_id, i.network.prefixlen) != expected:
        raise ValueError('constructor did not retain the valid input')
except ValueError as e:
    print('REFUTATION REJECTED:', str(e))
else:
    text = i.with_prefixlen
    try:
        j = ip.IPv6Interface(text)
        actual = (int(j), j.scope_id, j.network.prefixlen)
    except ValueError as e:
        actual = str(e)
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, 'actual:', (text, actual),
              'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'scope and prefix survived roundtrip')
```

**Output:**

```
REFUTATION CONFIRMED: fe80::1%eth/0 actual: ('fe80::1/0', (338288524927261089654018896841347694593, None, 0)) expected: (338288524927261089654018896841347694593, 'eth', 0)
```

Judge: BUG (medium) -- The valid scoped input is accepted and its scope retained by the constructor, but with_prefixlen omits that scope. A string representation of the interface should retain its documented scoped address and prefix. The supplied upstream diff does not fix with_prefixlen. The listed issue concerns the separate ip property, not this serialization behavior.

