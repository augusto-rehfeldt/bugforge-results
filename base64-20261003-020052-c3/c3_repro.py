import base64

b, wrapcol = b'', 1
if not isinstance(b, bytes) or not isinstance(wrapcol, int) or wrapcol <= 0:
    print("REFUTATION REJECTED: invalid input")
else:
    actual = base64.a85encode(b, wrapcol=wrapcol, adobe=True)
    raw = b'<~~>'  # Empty payload, independently framed with Adobe markers.
    expected = b'\n'.join(raw[i:i + wrapcol] for i in range(0, len(raw), wrapcol))
    if any(len(line) > wrapcol for line in actual.split(b'\n')):
        print("REFUTATION CONFIRMED:", (b, wrapcol), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: every line satisfies wrapcol")