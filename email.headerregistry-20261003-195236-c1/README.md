*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: RFC 2231 continuations should join across parameter-name casing

Target: `email.headerregistry.ContentDispositionHeader`

Property: For nonempty ASCII alphabetic strings a and b, HeaderRegistry()('Content-Disposition', "attachment; filename*0*=us-ascii''" + a + '; FILENAME*1*=' + b).params['filename'] must equal a + b: MIME parameter names are case-insensitive, so these are two sections of the same RFC 2231 parameter.

### Draft issue: email.headerregistry fails to combine RFC 2231 continuations with mixed-case parameter names

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** The email.headerregistry documentation, under ParameterizedMIMEHeader.params, states: “Parameter names are always mapped to lower case” and “Parameter values are decoded if necessary according to RFC 2231.” RFC 2231 continuation decoding applies to the case-insensitive MIME parameter names.

**Expected:** params['filename'] == 'helloworld'

**Actual:** params['filename'] == 'world'

**Reproducer:**

```python
from email.headerregistry import HeaderRegistry

a, b = "hello", "world"
parts = [("filename*0*", "us-ascii''" + a), ("FILENAME*1*", b)]
value = "attachment; " + "; ".join(k + "=" + v for k, v in parts)
valid = all(s and s.isascii() and s.isalpha() for s in (a, b))
valid &= [k.lower() for k, _ in parts] == ["filename*0*", "filename*1*"]
if not valid:
    print("REFUTATION REJECTED: invalid RFC 2231 continuation input")
else:
    expected = a + b
    actual = HeaderRegistry()("Content-Disposition", value).params.get("filename")
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(value), "actual =", repr(actual),
              "expected =", repr(expected))
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: "attachment; filename*0*=us-ascii''hello; FILENAME*1*=world" actual = 'world' expected = 'helloworld'
```

Judge: BUG (medium) -- The reproducer supplies valid RFC 2231 continuation sections with consecutive indices. MIME parameter names are case-insensitive, so filename*0* and FILENAME*1* belong to the same parameter. The documented lowercase mapping and RFC 2231 decoding require concatenating these sections, not treating them separately and overwriting the result. No duplicate is listed, and the upstream diff does not address decoding.

