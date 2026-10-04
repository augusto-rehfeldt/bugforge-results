import wcwidth

r = ''.join(chr(0x1F1E6 + i % 26) for i in range(31))
s = '\r\n' + r + '\u0301'
if not isinstance(s, str) or any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print('REFUTATION REJECTED: input is not a Unicode scalar string')
else:
    # CRLF is one cluster; regional indicators pair from the left;
    # the combining acute joins the final cluster.
    clusters = ['\r\n'] + [r[i:i+2] for i in range(0, len(r), 2)]
    clusters[-1] += '\u0301'
    expected = clusters[::-1]
    try:
        actual = list(wcwidth.iter_graphemes_reverse(s))
    except Exception as e:
        actual = f'{type(e).__name__}: {e}'
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
    else:
        print('REFUTATION REJECTED: reverse iteration matches independent grapheme segmentation')