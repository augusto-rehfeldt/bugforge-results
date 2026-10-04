import re
from email.headerregistry import Address

s = r'user@[a\]b]'
# RFC 5322: domain-literal = "[" *(dtext / quoted-pair) "]".
valid = re.fullmatch(r'user@\[(?:[\x21-\x5a\x5e-\x7e]|\\[\x09\x20-\x7e])*\]', s)
if not valid:
    print("REFUTATION REJECTED:", "input is not an RFC 5322 domain literal")
else:
    expected = ('user', re.sub(r'\\(.)', r'\1', s[5:]))
    try:
        a = Address(addr_spec=s)
    except Exception as e:
        print("REFUTATION REJECTED:", "initial construction failed:", repr(e))
    else:
        actual = {'initial': (a.username, a.domain), 'serialized': a.addr_spec}
        try:
            b = Address(addr_spec=a.addr_spec)
            result = (b.username, b.domain)
        except Exception as e:
            result = ('EXCEPTION', type(e).__name__, str(e))
        actual['reconstructed'] = result
        if actual['initial'] == expected and result != expected:
            print("REFUTATION CONFIRMED:", repr(s), actual, expected)
        else:
            print("REFUTATION REJECTED:", "reported failure not reproduced",
                  repr(s), actual, expected)