import shlex

P, C = 'a', 'b'
if not all(s and s.isascii() and s.isalpha() for s in (P, C)):
    print('REFUTATION REJECTED: input must be nonempty ASCII letters')
else:
    expected = list(shlex.shlex(P + ' ', posix=True, punctuation_chars=';'))
    lexer = shlex.shlex(P + ' ', posix=True, punctuation_chars=';')
    lexer.push_source(C + ';tail')
    token = lexer.get_token()
    if token != C:
        print('REFUTATION REJECTED: pushed token was', repr(token))
    else:
        lexer.pop_source()
        actual = list(lexer)
        if actual != expected:
            print('REFUTATION CONFIRMED:', (P, C), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED: restored source matches independent reference')