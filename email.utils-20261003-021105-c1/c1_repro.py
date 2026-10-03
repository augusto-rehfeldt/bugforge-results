import email.utils as e
import re

pair = ('Alice', '"a[b"@example.com')
name, address = pair
# RFC 2822 quoted-string qtext permits "["; example.com is a valid domain.
if not (re.fullmatch(r'[A-Za-z]+', name) and
        re.fullmatch(r'"[\x21\x23-\x5b\x5d-\x7e]+"@example\.com', address)):
    print('REFUTATION REJECTED: input validity not established')
else:
    expected = (name, address)  # Independently derived from the inverse promise.
    actual = e.parseaddr(e.formataddr(pair))
    if actual != expected:
        print('REFUTATION CONFIRMED:', pair, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: documented round trip succeeds')