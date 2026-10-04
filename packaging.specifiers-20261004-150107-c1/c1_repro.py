from packaging.specifiers import Specifier, InvalidSpecifier

text = "==1.2.3"  # Documented valid string-equality example.
try:
    s = Specifier(text)
except InvalidSpecifier:
    print("REFUTATION REJECTED: invalid input", repr(text))
else:
    if s != text:
        print("REFUTATION REJECTED: objects do not compare equal")
    else:
        actual, expected = hash(s), hash(text)
        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(text), "actual =", actual, "expected =", expected)
        else:
            print("REFUTATION REJECTED: equal objects have equal hashes")