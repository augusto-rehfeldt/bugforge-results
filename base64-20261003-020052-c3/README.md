*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `base64`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `doc-bug`: Ascii85 wrapping exceeds the requested column limit with Adobe framing

Target: `base64.a85encode`

Property: For every bytes input b and positive integer wrapcol, each newline-delimited line returned by a85encode(b, wrapcol=wrapcol, adobe=True) has length at most wrapcol.

### Draft issue: Document minimum wrapcol of 2 for a85encode with adobe=True

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

**Documented behaviour:** The a85encode docstring states: "If wrapcol is non-zero, insert a newline (b'\n') character after at most every wrapcol characters."

**Expected:** Document that adobe=True uses an effective wrapcol of at least 2; retain intact Adobe delimiters.

**Actual:** b'<~\n~>' has two lines of length 2 despite wrapcol=1.

**Reproducer:**

```python
import base64

b, wrapcol = b'', 1
if not isinstance(b, bytes) or not isinstance(wrapcol, int) or wrapcol <= 0:
    print("REFUTATION REJECTED: invalid input")
else:
    actual = base64.a85encode(b, wrapcol=wrapcol, adobe=True)
    raw = b'<~~>'  # Empty payload, independently framed with Adobe markers.
    expected = b'\n'.join(raw[i:i + wrapcol] for i in range(0, len(raw), wrapcol))
    if any(len(line) > wrapcol for line in actual.split(b'\n')):
        print("REFUTATION CONFIRMED:", (b, wrapcol), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: every line satisfies wrapcol")
```

**Output:**

```
REFUTATION CONFIRMED: (b'', 1) actual: b'<~\n~>' expected: b'<\n~\n~\n>'
```

Judge: DOC_BUG (low) -- The output does exceed the literal documented limit, but the implementation deliberately clamps wrapcol to at least 2 when adobe=True to preserve the two-character Adobe delimiters. The reproducer's expected output splits those delimiters and is not valid Adobe framing. This is a documentation omission, not an encoding bug. None of the listed issues specifically covers this minimum width.

