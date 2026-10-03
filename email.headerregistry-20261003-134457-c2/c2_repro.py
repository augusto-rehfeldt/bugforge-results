from email.headerregistry import HeaderRegistry

value = chr(0xB2) + ".0"
parts = value.split(".")
domain_ok = len(parts) == 2 and all(
    p and all(c in "0123456789" or (c.isdigit() and not c.isdecimal()) for c in p)
    for p in parts
)
if not domain_ok:
    print("REFUTATION REJECTED: input is outside the claimed domain")
else:
    # Invalid MIME grammar is parser input, not grounds for raising:
    # BaseHeader requires reporting defects instead, insofar as practical.
    grammar_ok = all(all(c in "0123456789" for c in p) for p in parts)
    expected = {"returned_header": True, "has_defects": not grammar_ok}
    try:
        h = HeaderRegistry()("MIME-Version", value)
        actual = {"returned_header": True, "has_defects": bool(h.defects)}
    except Exception as e:
        actual = {"returned_header": False, "exception": type(e).__name__,
                  "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(value), "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED: behavior matches the documented expectation")