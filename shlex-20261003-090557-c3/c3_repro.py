import shlex

p, c = 'a', 'b'
if not all(s and s.isascii() and s.isalpha() for s in (p, c)):
    print('REFUTATION REJECTED: invalid input')
else:
    L = shlex.shlex(p + ';tail', posix=True, punctuation_chars=';')
    if L.get_token() != p:
        print('REFUTATION REJECTED: parent token was not consumed as required')
    else:
        L.push_source(c + ' ')
        actual, expected = L.get_token(), c
        if actual != expected:
            print('REFUTATION CONFIRMED:', (p, c),
                  'actual:', repr(actual), 'expected:', repr(expected))
        else:
            print('REFUTATION REJECTED: pushed source was processed first')