import html

d = '9' * 4301
s = '&#' + d + ';'
n = d.lstrip('0') or '0'
if not d or any(c not in '0123456789' for c in d):
    print('REFUTATION REJECTED: invalid decimal reference')
elif (len(n), n) <= (7, '1114111'):
    print('REFUTATION REJECTED: value is not above 0x10FFFF')
else:
    expected = '\uFFFD'
    try:
        actual = html.unescape(s)
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual),
              'expected =', repr(expected))
    else:
        print('REFUTATION REJECTED: result matches HTML5')