*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Malformed Unicode MIME-Version digits should produce defects, not crash

Target: `email.headerregistry.MIMEVersionHeader`

Property: For values of the form a + '.' + b, where a and b are nonempty strings drawn from ASCII decimal digits and Unicode characters that satisfy str.isdigit() but not str.isdecimal(), HeaderRegistry()('MIME-Version', value) must return a header rather than raise ValueError; values containing those non-ASCII characters must report parsing defects.

### Draft issue: MIMEVersionHeader raises ValueError on non-decimal Unicode digits

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** BaseHeader's subclass parsing contract states: "The parser should not, insofar as practical, raise any errors. Defects should be added to the list instead." MIMEVersionHeader.value_parser documents the grammar as "mime-version = [CFWS] 1*digit [CFWS] \".\" [CFWS] 1*digit [CFWS]".

**Expected:** Return a MIMEVersionHeader with parsing defects for '².0'.

**Actual:** Raises ValueError: invalid literal for int() with base 10: '²'.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: '².0' actual: {'returned_header': False, 'exception': 'ValueError', 'message': "invalid literal for int() with base 10: '²'"} expected: {'returned_header': True, 'has_defects': True}
```

Judge: BUG (medium) -- The reproducer correctly includes '².0' in its domain and identifies it as invalid MIME grammar. Malformed header text is nevertheless legitimate input to this defect-reporting parser. Rejecting this character without raising is practical and covered by the documented parsing contract. The ValueError indicates that a character accepted as a digit reaches int() even though it cannot be converted. No listed issue duplicates this, and the upstream diff does not address it.

