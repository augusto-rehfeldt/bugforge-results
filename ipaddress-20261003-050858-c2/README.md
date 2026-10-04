*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: IPv6Interface.ip should preserve the interface’s scope ID

Target: `ipaddress.IPv6Interface.ip`

Property: For any valid scoped IPv6 address string a and prefix length p in [0, 128], IPv6Interface(f'{a}/{p}').ip must equal IPv6Address(a), including its scope_id.

### Draft issue: ipaddress.IPv6Interface.ip drops the IPv6 scope ID

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** The ipaddress documentation, under IPv6Interface, says it implements the same attributes as IPv4Interface; the documented ip attribute is “An IPv4Address object with the address of the interface.” For IPv6Interface this is an IPv6Address object.

**Expected:** IPv6Address('fe80::1%eth0'), with scope_id 'eth0'

**Actual:** IPv6Address('fe80::1'), with scope_id None

**Reproducer:**

```python
import ipaddress as ip

s = 'fe80::1%eth0/0'
try:
    a, p = s.rsplit('/', 1)
    expected = ip.IPv6Address(a)
    if not 0 <= int(p) <= 128 or not expected.scope_id:
        raise ValueError('invalid prefix or missing scope')
    actual = ip.IPv6Interface(s).ip
    if actual != expected or actual.scope_id != expected.scope_id:
        print(f'REFUTATION CONFIRMED: {s!r} actual: {actual!r} expected: {expected!r}')
    else:
        print('REFUTATION REJECTED: actual matches the scoped address')
except ValueError as e:
    print(f'REFUTATION REJECTED: invalid input: {e}')
```

**Output:**

```
REFUTATION CONFIRMED: 'fe80::1%eth0/0' actual: IPv6Address('fe80::1') expected: IPv6Address('fe80::1%eth0')
```

Judge: BUG (medium) -- The input is valid: scoped IPv6 addresses are supported, and /0 is a valid interface prefix. The documented ip attribute returns the interface's address; dropping its scope ID changes that address and its equality semantics. The reproducer correctly compares against IPv6Address('fe80::1%eth0'). No listed issue or supplied upstream change handles this behaviour.

