import quopri

s = b'A' * 74 + b' BB'
saved = quopri.b2a_qp
failure = None
try:
    if not isinstance(s, bytes) or b'\r' in s or b'\n' in s:
        reason = 'input is not bytes without CR/LF'
    else:
        reason = 'all physical lines are at most 76 bytes'
        for encoder in (saved, None):
            quopri.b2a_qp = encoder
            actual = quopri.encodestring(s, quotetabs=False, header=False)
            lengths = list(map(len, actual.splitlines()))
            if any(n > 76 for n in lengths):
                failure = (actual, lengths)
                break
finally:
    quopri.b2a_qp = saved

if failure:
    print('REFUTATION CONFIRMED:', 'input=', repr(s),
          'actual=', repr(failure[0]), 'line lengths=', failure[1],
          'expected=every physical line length <= 76 bytes')
else:
    print('REFUTATION REJECTED:', reason)