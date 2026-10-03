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