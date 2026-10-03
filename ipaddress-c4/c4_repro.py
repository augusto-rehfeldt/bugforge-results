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