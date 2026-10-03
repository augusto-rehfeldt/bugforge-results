import email.utils
import re

a, b, d = 'a', 'b', 'example.com'
s = a + '..' + b + '@' + d
atom = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
domain = r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)+'

if not (re.fullmatch('[A-Za-z]+', a + b) and re.fullmatch(domain, d)):
    print('REFUTATION REJECTED:', 'invalid test parameters')
else:
    # Malformed strings are in scope: strict=True promises to reject them.
    expected = ('', s) if re.fullmatch(atom + r'(?:\.' + atom + r')*@' + domain, s) else ('', '')
    try:
        actual = email.utils.parseaddr(s, strict=True)
    except Exception as e:
        print('REFUTATION REJECTED:', type(e).__name__, str(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
        else:
            print('REFUTATION REJECTED:', 'result matches expectation')