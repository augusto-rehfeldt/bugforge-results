import email.utils

s = "a b"
if not s.isascii():
    print("REFUTATION REJECTED: input is not ASCII")
else:
    actual = email.utils.encode_rfc2231(s, charset=None, language=None)
    expected = s  # Documented return when neither argument is given.
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), repr(actual), repr(expected))
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")