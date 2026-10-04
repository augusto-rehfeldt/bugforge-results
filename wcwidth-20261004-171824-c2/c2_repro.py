from wcwidth import iter_graphemes

s = '\u094d' + '\u0915'
if not isinstance(s, str) or any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print('REFUTATION REJECTED: input is not a Unicode scalar string')
else:
    # U+094D: Extend, InCB=Linker; U+0915: InCB=Consonant.
    # GB9c cannot apply without an earlier consonant; GB999 splits.
    expected = ['\u094d', '\u0915']
    try:
        actual = list(iter_graphemes(s))
    except Exception as e:
        print('REFUTATION REJECTED: no cluster result:', repr(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
        else:
            print('REFUTATION REJECTED: result matches Unicode grapheme rules')