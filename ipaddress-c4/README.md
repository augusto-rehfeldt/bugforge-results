# bugforge: `ipaddress`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: IPv4 /0 supernet bypasses documented prefix validation

Target: `ipaddress.IPv4Network.supernet`

Property: For IPv4Network('0.0.0.0/0'), calling supernet(new_prefix=p) with an integer p in [1, 32] must raise ValueError because p is larger than the existing prefix length.

### Draft issue: IPv4Network.supernet skips new_prefix validation for /0 networks

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `ipaddress`

**Documented behaviour:** Python ipaddress documentation, IPv4Network.supernet: "A ValueError is raised if new_prefix is larger than our prefix."

**Expected:** supernet(new_prefix=1) raises ValueError for IPv4Network('0.0.0.0/0').

**Actual:** Returns IPv4Network('0.0.0.0/0') without raising an exception.

**Reproducer:**

```python
import ipaddress

network, p = "0.0.0.0/0", 1
n = ipaddress.IPv4Network(network)
if not isinstance(p, int) or not 0 <= p <= 32:
    print("REFUTATION REJECTED: invalid IPv4 prefix")
else:
    expected = ("exception", "ValueError") if p > n.prefixlen else (
        "result", str(ipaddress.IPv4Network((int(n.network_address), p), strict=False))
    )
    try:
        actual = ("result", str(n.supernet(new_prefix=p)))
    except Exception as e:
        actual = ("exception", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", {"network": network, "new_prefix": p},
              "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'network': '0.0.0.0/0', 'new_prefix': 1} actual= ('result', '0.0.0.0/0') expected= ('exception', 'ValueError')
```

Judge: BUG (low) -- The reproducer uses a valid IPv4 network and integer prefix. The documented ValueError rule applies because 1 is larger than the existing prefix length of 0. Returning the unchanged /0 network violates that explicit promise; no duplicate is listed.

