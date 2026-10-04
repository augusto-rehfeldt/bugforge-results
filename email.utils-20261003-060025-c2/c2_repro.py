import email.utils as u
import re
from urllib.parse import unquote

p = [('text/plain', ''), ('filename*0', "a'b'"), ('filename*1*', '%63')]
# RFC 2231: contiguous segments; only the starred segment is encoded.
valid = (p[0] == ('text/plain', '') and
         [k for k, v in p[1:]] == ['filename*0', 'filename*1*'] and
         re.fullmatch(r"[A-Za-z0-9']+", p[1][1]) and
         re.fullmatch(r"(?:%[0-9a-fA-F]{2})+", p[2][1]))
if not valid:
    print('REFUTATION REJECTED: invalid RFC 2231 input')
else:
    value = p[1][1] + unquote(p[2][1])
    quoted = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    expected = [p[0], ('filename', (None, None, quoted))]
    actual = u.decode_params(p.copy())
    if actual != expected:
        print('REFUTATION CONFIRMED:', 'input=', repr(p),
              'actual=', repr(actual), 'expected=', repr(expected))
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')