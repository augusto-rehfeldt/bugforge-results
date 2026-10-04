*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `idna`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Valid Unicode 17 labels rejected using older host Unicode bidi data

Target: `idna.check_label`

Property: For every single-character label consisting of an IDNA2008 PVALID, NFC-stable Unicode 17 lowercase letter with Bidi_Class L, check_label must return None rather than raise IDNABidiError. Such labels satisfy the character, normalization, hyphen, initial-combiner, context, and bidi requirements.

### Draft issue: check_label rejects valid Unicode 17 Beria Erfe letters with unknown directionality

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `idna` 3.20

**Documented behaviour:** Public API documentation for check_label: "Run the full set of IDNA 2008 validity checks on a single label." Public API documentation for check_bidi identifies the bidi requirements as RFC 5893.

**Expected:** idna.check_label(chr(0x16EBB)) returns None.

**Actual:** Raises IDNABidiError: Unknown directionality in label '\U00016ebb' at position 1.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: '\U00016ebb' actual: ('raise', 'IDNABidiError', "Unknown directionality in label '\\U00016ebb' at position 1") expected: ('return', None)
```

Judge: BUG (medium) -- U+16EBB is a Unicode 17 PVALID, NFC-stable lowercase letter with bidi class L; a single-character label therefore satisfies the cited validity requirements. The output shows check_label rejecting it because directionality is unknown, consistent with using Python's older Unicode database for bidi checks alongside newer IDNA validity tables. The reproducer hard-codes the Unicode facts, but those facts and the expected result are correct. Neither listed issue covers this failure.

