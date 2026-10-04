*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `idna`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: decode accepts oversized A-labels

Target: `idna.decode`

Property: For every ASCII string consisting of a single syntactically valid xn-- label whose Punycode payload decodes to an otherwise valid IDNA U-label, decode must raise IDNAError if the ASCII label exceeds 63 octets: such a label is not a valid A-label.

### Draft issue: decode accepts Punycode A-labels exceeding the 63-octet limit

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

**Documented behaviour:** The supplied public API documents decode as “Decode an A-label-encoded domain name back to Unicode.” RFC 5890 §2.3.2.1 defines A-labels and explicitly requires: “The A-label must also conform to the DNS length restrictions.”

**Expected:** Raise idna.IDNAError for the ASCII label exceeding 63 octets.

**Actual:** Returns the decoded string of repeated ü characters.

**Reproducer:**

```python
import idna

s = 'xn--tdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
try:
    u = s[4:].encode('ascii').decode('punycode')
    # Repeated ü is NFC and IDNA-valid; verify canonical Punycode.
    if not u or set(u) != {'ü'} or 'xn--' + u.encode('punycode').decode('ascii') != s:
        raise ValueError('input is not canonical Punycode for a valid U-label')
    expected = ('error', 'IDNAError') if len(s.encode('ascii')) > 63 else ('unicode', u)
    try:
        actual = ('unicode', idna.decode(s))
    except idna.IDNAError:
        actual = ('error', 'IDNAError')
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
except Exception as e:
    print('REFUTATION REJECTED:', type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: 'xn--tdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' actual: ('unicode', 'üüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüüü') expected: ('error', 'IDNAError')
```

Judge: BUG (medium) -- The reproducer verifies canonical Punycode for an otherwise valid U-label and checks the ASCII octet length directly. decode accepts the overlength xn-- label despite the documented A-label contract and RFC 5890's DNS length requirement. Invalid encoded labels should be rejected, not silently decoded. The listed Unicode-data PR is unrelated; development-branch status remains unverified.

