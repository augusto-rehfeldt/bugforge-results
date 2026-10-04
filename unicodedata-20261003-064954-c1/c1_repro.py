import unicodedata as ud

u = ud.ucd_3_2_0
m = '\u1ab0'
s = 'A\u0315' + m

if not (u.category(m) == 'Cn' and u.combining(m) == 0
        and ud.combining(m) > 0):
    print('REFUTATION REJECTED: input does not meet the stated premises')
else:
    # These characters are not Hangul syllables. NFD requires no canonical
    # decompositions and nondecreasing combining classes between class-zero boundaries.
    classes = [u.combining(c) for c in s]
    decomps = [u.decomposition(c) for c in s]
    expected = (
        all(not d or d.startswith('<') for d in decomps)
        and all(b == 0 or a <= b for a, b in zip(classes, classes[1:]))
    )
    actual = u.is_normalized('NFD', s)
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), actual, expected)
    else:
        print('REFUTATION REJECTED: actual agrees with independent Unicode 3.2 NFD check')