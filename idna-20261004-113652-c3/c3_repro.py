import idna

s = 'xn--tdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
try:
    u = s[4:].encode('ascii').decode('punycode')
    # Repeated ü is NFC and IDNA-valid; verify canonical Punycode.
    if not u or set(u) != {'ü'} or 'xn--' + u.encode('punycode').decode('ascii') != s:
        raise ValueError('input is not canonical Punycode for a valid U-label')
    expected = ('error', 'IDNAError') if len(s.encode('ascii')) > 63 else ('unicode', u)
    try:
        actual = ('unicode', idna.decode(s))
    except idna.IDNAError:
        actual = ('error', 'IDNAError')
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
except Exception as e:
    print('REFUTATION REJECTED:', type(e).__name__, str(e))