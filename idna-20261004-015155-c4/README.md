*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `idna`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Encoding a Bidi domain must validate its ASCII-only labels too

Target: `idna.encode`

Property: For a domain consisting of an ASCII digit-only label followed by a valid Hebrew RTL label, encode(domain) must raise IDNABidiError: the RTL label makes this a Bidi domain, and the digit-only label violates RFC 5893's requirement that each label begin with L, R, or AL.

### Draft issue: Enforce domain-wide Bidi rules for ASCII labels in RTL domains

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

**Documented behaviour:** The project README promises: "Support for the Internationalised Domain Names in Applications (IDNA) protocol as specified in RFC 5891." RFC 5891 incorporates the RFC 5893 Bidi Rule; RFC 5893 §2 requires: "The first character must be a character with Bidi property L, R, or AL." Its Bidi-domain requirements apply to every label, including ASCII-only labels.

**Expected:** Raise IDNABidiError for idna.encode('0.א').

**Actual:** Returns b'0.xn--4db'.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: '0.א' ('result', b'0.xn--4db') ('error', 'IDNABidiError')
```

Judge: BUG (medium) -- The reproducer correctly identifies a Bidi domain: the Hebrew label contains an R character. RFC 5893 requires every label in that domain, including ASCII-only labels, to satisfy the Bidi Rule. The label '0' starts with EN, not L, R, or AL, so accepting the domain violates the cited IDNA conformance promise. No duplicate is listed.

