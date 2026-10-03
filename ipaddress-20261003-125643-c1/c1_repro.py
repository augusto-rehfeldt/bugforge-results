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