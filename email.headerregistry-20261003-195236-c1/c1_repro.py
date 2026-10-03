from email.headerregistry import HeaderRegistry

a, b = "hello", "world"
parts = [("filename*0*", "us-ascii''" + a), ("FILENAME*1*", b)]
value = "attachment; " + "; ".join(k + "=" + v for k, v in parts)
valid = all(s and s.isascii() and s.isalpha() for s in (a, b))
valid &= [k.lower() for k, _ in parts] == ["filename*0*", "filename*1*"]
if not valid:
    print("REFUTATION REJECTED: invalid RFC 2231 continuation input")
else:
    expected = a + b
    actual = HeaderRegistry()("Content-Disposition", value).params.get("filename")
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(value), "actual =", repr(actual),
              "expected =", repr(expected))
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")