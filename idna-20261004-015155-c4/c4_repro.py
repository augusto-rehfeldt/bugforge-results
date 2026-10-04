import unicodedata as u
try:
    import idna
    domain = "0.\u05d0"
    labels = domain.split(".")
    # Both labels satisfy non-Bidi IDNA requirements; test Bidi independently.
    if (u.normalize("NFC", domain) != domain or
        [u.category(c) for c in "0\u05d0"] != ["Nd", "Lo"] or
        [u.bidirectional(c) for c in "0\u05d0"] != ["EN", "R"]):
        raise ValueError("input validation failed")
    bidi_domain = any(u.bidirectional(c) in ("R", "AL", "AN") for c in domain)
    violates = bidi_domain and any(
        u.bidirectional(label[0]) not in ("L", "R", "AL") for label in labels
    )
    if not violates:
        raise ValueError("independent RFC 5893 check does not support the claim")
    expected = ("error", "IDNABidiError")
    try:
        actual = ("result", idna.encode(domain))
    except Exception as e:
        actual = ("error", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(domain), actual, expected)
    else:
        print("REFUTATION REJECTED: implementation raises the required IDNABidiError")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))