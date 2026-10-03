import html.parser
import re

s = '&#' + '9' * 4301 + ';'
digits = s[2:-1]
if not re.fullmatch(r'&#[0-9]+;', s):
    print('REFUTATION REJECTED: invalid decimal character reference')
else:
    d = digits.lstrip('0') or '0'
    expected = ('data', '\ufffd' if (len(d), d) > (7, '1114111') else chr(int(d)))

    class Parser(html.parser.HTMLParser):
        def handle_data(self, data):
            chunks.append(data)

    chunks = []
    try:
        p = Parser(convert_charrefs=True)
        p.feed(s)
        p.close()
        actual = ('data', ''.join(chunks))
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))

    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')