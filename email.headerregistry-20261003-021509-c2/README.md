*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Unstructured headers discard encoded-word parsing defects

Target: `email.headerregistry.UnstructuredHeader`

Property: For an unfolded ASCII header value containing an RFC 2047 encoded-word whose Base64 payload has invalid padding, if UnstructuredHeader.value_parser(value).all_defects contains InvalidBase64PaddingDefect, then HeaderRegistry()('Subject', value).defects must also contain an InvalidBase64PaddingDefect.

### Draft issue: UnstructuredHeader drops encoded-word Base64 padding defects

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** BaseHeader documentation in email.headerregistry: "Defects should be added to the list instead. The standard header parsers register defects for RFC compliance issues, for obsolete RFC syntax, and for unrecoverable parsing errors."

**Expected:** The Subject header's defects includes InvalidBase64PaddingDefect.

**Actual:** The parser's all_defects includes InvalidBase64PaddingDefect, but the Subject header's defects does not.

**Reproducer:**

```python
from email.headerregistry import HeaderRegistry, UnstructuredHeader
from email.errors import InvalidBase64PaddingDefect

value = '=?utf-8?b?YQ?='
if not value.isascii() or '\r' in value or '\n' in value:
    print('REFUTATION REJECTED: input is not unfolded ASCII')
else:
    expected = any(isinstance(d, InvalidBase64PaddingDefect)
                   for d in UnstructuredHeader.value_parser(value).all_defects)
    actual = any(isinstance(d, InvalidBase64PaddingDefect)
                 for d in HeaderRegistry()('Subject', value).defects)
    if expected and not actual:
        print('REFUTATION CONFIRMED:', repr(value),
              'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: parser prerequisite absent or defect preserved',
              repr(value), 'actual:', actual, 'expected:', expected)
```

**Output:**

```
REFUTATION CONFIRMED: '=?utf-8?b?YQ?=' actual: False expected: True
```

Judge: BUG (low) -- The reproducer correctly checks the same defect type on the same unfolded ASCII value. Although the encoded-word is malformed, defect reporting explicitly covers RFC compliance errors; malformed padding is therefore not grounds to reject this test. The parser detects InvalidBase64PaddingDefect, but the public header object's defects omit it, contrary to the documented defect-reporting contract. No matching issue or fix was supplied, and the upstream changes shown are unrelated.

