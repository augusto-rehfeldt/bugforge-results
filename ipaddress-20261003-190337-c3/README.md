*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: IPv6Network.is_global disagrees with endpoint classification

Target: `ipaddress.IPv6Network.is_global`

Property: For every IPv6Network n, n.is_global must equal (n.network_address.is_global and n.broadcast_address.is_global), as documented for network classification attributes.

### Draft issue: ipaddress: IPv6Network.is_global violates documented endpoint classification rule

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** Python ipaddress documentation, IPv4Network/IPv6Network classification attributes: "These attributes are true for the network as a whole if they are true for both the network address and the broadcast address." This includes is_global.

**Expected:** IPv6Network('::/0').is_global is False, matching the conjunction of its endpoints' is_global values.

**Actual:** IPv6Network('::/0').is_global is True.

**Reproducer:**

```python
import ipaddress

s = "::/0"
try:
    n = ipaddress.IPv6Network(s, strict=True)
except ValueError as e:
    print("REFUTATION REJECTED:", e)
else:
    actual = n.is_global
    expected = n.network_address.is_global and n.broadcast_address.is_global
    if actual != expected:
        print(f"REFUTATION CONFIRMED: {s!r} actual={actual} expected={expected}")
    else:
        print("REFUTATION REJECTED: result matches documented endpoint rule")
```

**Output:**

```
REFUTATION CONFIRMED: '::/0' actual=True expected=False
```

Judge: BUG (medium) -- The valid, canonical IPv6 network ::/0 violates the documented endpoint rule for network classification attributes. Its network address :: is not global, so the conjunction must be False, but the reproducer reports True. No existing issue or pull request is listed, and the supplied upstream diff does not fix this behavior.

