import plistlib

d = {'a\rb': 1, 'a\nb': 2}
valid = all(
    isinstance(k, str)
    and all(ord(c) in (9, 10, 13) or 32 <= ord(c) <= 0xD7FF
            or 0xE000 <= ord(c) <= 0xFFFD
            or 0x10000 <= ord(c) <= 0x10FFFF for c in k)
    and type(v) is int and -(1 << 63) <= v < (1 << 64)
    for k, v in d.items()
)
if not valid:
    print('REFUTATION REJECTED:', 'input outside documented domain')
else:
    expected = d.copy()
    actual = plistlib.loads(plistlib.dumps(d, fmt=plistlib.FMT_XML))
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(d), 'actual:', repr(actual),
              'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED:', 'round-trip equals input')