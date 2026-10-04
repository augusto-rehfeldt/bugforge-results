import urllib.parse as u

base, p = 'file://server/share/base', 'a'
ref = 'file:///' + p
b, r = u.urlsplit(base), u.urlsplit(ref)
if not (p.isascii() and p.isalpha()
        and b.scheme == 'file' and b.netloc == 'server'
        and r.scheme == 'file' and ref[5:7] == '//'
        and r.netloc == '' and r.path == '/' + p):
    print('REFUTATION REJECTED:', 'input is not the documented absolute file URL')
else:
    # RFC 3986 §5.2.2: explicit scheme and authority (even empty) replace base.
    expected = 'file://' + '/' + p
    actual = u.urljoin(base, ref)
    if actual != expected:
        print('REFUTATION CONFIRMED:', (base, ref), repr(actual), repr(expected))
    else:
        print('REFUTATION REJECTED:', 'actual equals documented expectation')