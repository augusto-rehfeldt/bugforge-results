import unicodedata as ud

u = ud.ucd_3_2_0
x, y = '\u1ab0', '\u0316'
s = 'a' + x + y
if not (u.category(x) == 'Cn' and u.combining(x) == 0
        and u.decomposition(x) == '' and u.combining(y) > 0
        and u.decomposition(y) == '' and u.decomposition('a') == ''
        and u.combining('a') == 0):
    print('REFUTATION REJECTED: input does not satisfy the premises')
else:
    ref = []
    for c in s:
        ref.append(c)
        i = len(ref) - 1
        while i and 0 < u.combining(ref[i]) < u.combining(ref[i - 1]):
            ref[i - 1], ref[i] = ref[i], ref[i - 1]
            i -= 1
    expected = ''.join(ref)
    actual = u.normalize('NFD', s)
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual),
              'expected =', repr(expected))
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')