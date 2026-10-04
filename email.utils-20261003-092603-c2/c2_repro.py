import email.utils, re

p = [('text/plain', ''), ('filename*0', 'report'), ('FILENAME*1', '.txt')]
s = [(re.fullmatch(r'([A-Za-z]+)\*(0|[1-9][0-9]*)', k), v) for k, v in p[1:]]
# These names and values are valid RFC 2045 tokens; attributes ignore case.
if (not all(m and re.fullmatch(r'[A-Za-z.]+', v) for m, v in s)
    or len({m[1].lower() for m, v in s}) != 1
    or sorted(int(m[2]) for m, v in s) != list(range(len(s)))):
    print('REFUTATION REJECTED: invalid continuation input')
else:
    expected = [p[0], (s[0][0][1].lower(),
                       '"' + ''.join(v for m, v in sorted(s, key=lambda x: int(x[0][2]))) + '"')]
    actual = email.utils.decode_params(p)
    if actual != expected:
        print('REFUTATION CONFIRMED:', 'input:', p, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')