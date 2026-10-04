import unicodedata as ud

c = chr(0x4EAC)
u = ud.ucd_3_2_0
sentinel = object()

# Independent reference: U+4EAC has no numeric field in Unicode 3.2's
# UnicodeData.txt or numeric entry in its Unihan data.
reference = {0x4EAC: None}

def call(*args):
    try:
        value = u.numeric(*args)
        return ("returned", "sentinel by identity" if value is sentinel else value)
    except Exception as e:
        return ("raised", type(e).__name__)

if u.unidata_version != "3.2.0" or len(c) != 1 or u.category(c) == "Cn":
    print("REFUTATION REJECTED:", "input is not an assigned Unicode 3.2 character")
elif reference[ord(c)] is not None:
    print("REFUTATION REJECTED:", "reference defines a numeric value")
else:
    expected = (("raised", "ValueError"), ("returned", "sentinel by identity"))
    actual = (call(c), call(c, sentinel))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(c), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "documented behavior holds for", repr(c))