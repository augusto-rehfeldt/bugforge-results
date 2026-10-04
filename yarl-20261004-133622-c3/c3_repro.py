import re
from yarl import URL

s = 'http'
scheme = s + '\n'
valid = lambda x: re.fullmatch(r'[A-Za-z][A-Za-z0-9+.-]*', x) is not None

if not valid(s) or valid(scheme):
    print('REFUTATION REJECTED: invalid test setup')
else:
    u = URL('https://example.org/path')
    expected = 'raises ValueError'
    try:
        actual = ('returned', str(u.with_scheme(scheme)))
    except Exception as e:
        actual = 'raises ' + type(e).__name__
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(scheme),
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED: ValueError raised as documented')