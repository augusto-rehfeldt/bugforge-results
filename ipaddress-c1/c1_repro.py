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