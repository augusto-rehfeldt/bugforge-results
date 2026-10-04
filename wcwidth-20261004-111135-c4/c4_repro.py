import unicodedata
from wcwidth import grapheme_boundary_before

text = ''.join(chr(c) for c in range(0x1F1FF, 0x1F1E5, -1)) * 2
pos = 51
if not (0 < pos < len(text) and pos % 2 and len(text) % 2 == 0
        and all(unicodedata.name(c).startswith('REGIONAL INDICATOR SYMBOL LETTER ') for c in text)):
    print('REFUTATION REJECTED:', 'invalid input')
else:
    # Unicode grapheme rule GB12/GB13 pairs consecutive regional indicators.
    expected = max(range(0, pos, 2))
    try:
        actual = grapheme_boundary_before(text, pos)
    except Exception as e:
        print('REFUTATION REJECTED:', 'reported result not reproduced:', repr(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr((text, pos)), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED:', 'actual matches expected:', actual)