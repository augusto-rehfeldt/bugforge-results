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