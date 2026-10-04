import binascii, io, quopri

s = b'A' * 74 + b'\xff'
if not isinstance(s, bytes) or b'\r' in s or b'\n' in s:
    print('REFUTATION REJECTED:', 'input is not a newline-free bytes payload')
else:
    quopri.b2a_qp = None
    out = io.BytesIO()
    quopri.encode(io.BytesIO(s), out, quotetabs=True, header=False)
    encoded = out.getvalue()
    actual = binascii.a2b_qp(encoded)
    expected = s
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, (encoded, actual), expected)
    else:
        print('REFUTATION REJECTED:', 'independent decoding recovers the input')