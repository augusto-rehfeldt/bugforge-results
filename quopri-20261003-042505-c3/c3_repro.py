import quopri

s = b'A' * 74 + b'\xffB'
if not isinstance(s, bytes):
    print('REFUTATION REJECTED: input is not bytes')
else:
    lines, line = [], b''
    for c in s:
        token = bytes([c]) if 33 <= c <= 126 and c != 61 else ('=%02X' % c).encode()
        if len(line + token) > 75:
            lines.append(line + b'=\n')
            line = b''
        line += token
    expected = b''.join(lines) + line
    quopri.b2a_qp = None  # Exercise the supported pure-Python fallback.
    actual = quopri.encodestring(s, quotetabs=True, header=False)
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, actual, expected)
    else:
        print('REFUTATION REJECTED: output matches independently encoded expectation')