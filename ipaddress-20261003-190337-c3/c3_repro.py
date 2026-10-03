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