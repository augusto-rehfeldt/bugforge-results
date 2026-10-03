import ipaddress as ip

s = 'fe80::1%eth/0'
address, prefix = s.split('/')
base, zone = address.split('%')
p = int(prefix)
try:
    if not (zone.isascii() and zone.isalpha() and 0 <= p <= 128):
        raise ValueError('input outside documented domain')
    i = ip.IPv6Interface(s)
    expected = (int(ip.IPv6Address(base)), zone, p)
    if (int(i), i.scope_id, i.network.prefixlen) != expected:
        raise ValueError('constructor did not retain the valid input')
except ValueError as e:
    print('REFUTATION REJECTED:', str(e))
else:
    text = i.with_prefixlen
    try:
        j = ip.IPv6Interface(text)
        actual = (int(j), j.scope_id, j.network.prefixlen)
    except ValueError as e:
        actual = str(e)
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, 'actual:', (text, actual),
              'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'scope and prefix survived roundtrip')