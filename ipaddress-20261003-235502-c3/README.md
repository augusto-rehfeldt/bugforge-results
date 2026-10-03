*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: IPv6 subnet exclusion must work for matching scope IDs

Target: `ipaddress.IPv6Network.address_exclude`

Property: For n = IPv6Network('fe80::%' + zone + '/126') and other = IPv6Network('fe80::%' + zone + '/128'), where zone is a nonempty ASCII alphabetic scope ID, list(n.address_exclude(other)) must complete successfully and produce networks covering exactly the integer addresses in n except int(other.network_address).

### Draft issue: IPv6Network.address_exclude raises AssertionError for contained scoped IPv6 networks

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** "Computes the network definitions resulting from removing the given network from this one. Returns an iterator of network objects. Raises ValueError if other is not completely contained in self." — ipaddress documentation, IPv6Network.address_exclude.

**Expected:** Complete successfully with networks covering exactly fe80::1 through fe80::3.

**Actual:** AssertionError: Error performing exclusion: s1: fe80::/127 s2: fe80::2/127 other: fe80::%a/128

**Reproducer:**

```python
import ipaddress

inputs = ('fe80::%a/126', 'fe80::%a/128')
try:
    n, other = map(ipaddress.IPv6Network, inputs)
    if not other.subnet_of(n):
        raise ValueError("other is not completely contained in n")
    expected = list(range(int(n.network_address) + 1,
                          int(n.network_address) + n.num_addresses))
except Exception as e:
    print("REFUTATION REJECTED:", inputs, "invalid input:", repr(e))
else:
    try:
        result = list(n.address_exclude(other))
        actual = {
            "networks": list(map(str, result)),
            "addresses": sorted(
                a for net in result
                for a in range(int(net.network_address),
                               int(net.network_address) + net.num_addresses)
            ),
        }
        broken = actual["addresses"] != expected
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", inputs, "actual =", actual,
              "expected =", expected)
    else:
        print("REFUTATION REJECTED:", inputs,
              "exclusion completed with exactly the expected coverage")
```

**Output:**

```
REFUTATION CONFIRMED: ('fe80::%a/126', 'fe80::%a/128') actual = {'exception': 'AssertionError', 'message': 'Error performing exclusion: s1: fe80::/127 s2: fe80::2/127 other: fe80::%a/128'} expected = [338288524927261089654018896841347694593, 338288524927261089654018896841347694594, 338288524927261089654018896841347694595]
```

Judge: BUG (medium) -- Both scoped IPv6 networks construct successfully, and other.subnet_of(n) confirms the documented containment precondition. The expected coverage correctly removes the first address from the four-address /126. Instead of returning the remaining network definitions, address_exclude raises an internal AssertionError: subdivision loses the scope ID, preventing comparison with the scoped excluded network. No supplied issue or upstream change handles this behaviour.

