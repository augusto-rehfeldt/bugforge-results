import re
import urllib.parse as u

base = 'https://example.com/base/'
ref = '//other.example/a/../b'
b, r = u.urlsplit(base), u.urlsplit(ref)
if not (b.scheme == 'https' and b.netloc == 'example.com'
        and not r.scheme and r.netloc == 'other.example'
        and not r.query and not r.fragment
        and re.fullmatch(r'/[A-Za-z]+/\.\./[A-Za-z]+', r.path)):
    print('REFUTATION REJECTED: input is outside the stated valid RFC 3986 case')
else:
    # Independently remove dot segments from this absolute reference path.
    segments = []
    for segment in r.path.split('/')[1:]:
        if segment == '..':
            segments.pop()
        elif segment != '.':
            segments.append(segment)
    expected = b.scheme + '://' + r.netloc + '/' + '/'.join(segments)
    actual = u.urljoin(base, ref)
    if actual != expected:
        print('REFUTATION CONFIRMED:', (base, ref),
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED: actual equals the RFC 3986 expectation')