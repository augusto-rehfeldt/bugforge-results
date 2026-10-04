# Unicode 17.0.0 UCD facts for U+16EBB (Beria Erfe):
# General_Category=Ll, Bidi_Class=L, Decomposition_Mapping=<none>.
# It is not an RFC 5892 exception, ignorable, or excluded character;
# therefore RFC 5892's LetterDigits rule makes it PVALID.
# A single undecomposable scalar is NFC; it is neither a hyphen nor
# a combining mark and needs no contextual check. RFC 5893 permits
# a single L character (including as both first and last character).
s = chr(0x16EBB)
category, bidi, decomposition = "Ll", "L", ()
pvalid = category == "Ll"
valid = pvalid and not decomposition and bidi == "L"
expected = ("return", None) if valid else ("invalid",)

try:
    import idna
except Exception as e:
    print("REFUTATION REJECTED:", "cannot import idna:", str(e))
else:
    try:
        actual = ("return", idna.check_label(s))
    except Exception as e:
        actual = ("raise", type(e).__name__, str(e))
    if valid and actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no documented violation;",
              repr(s), "actual:", actual, "expected:", expected)