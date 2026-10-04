*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `markupsafe`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Empty-spec formatting re-escapes trusted __html__ output

Target: `markupsafe.EscapeFormatter.format_field`

Property: For any object x whose __html__ method returns a plain str h, EscapeFormatter(escape).format_field(x, '') should equal str(escape(x)): both should preserve h as the object's trusted HTML representation.

### Draft issue: EscapeFormatter re-escapes plain-str output from __html__

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

**Documented behaviour:** The escape documentation states: "If the object has an __html__ method, it is called and the return value is assumed to already be safe for HTML." Markup's class documentation also states that passing an object implementing __html__ will "wrap the output of that method, marking it safe."

**Expected:** <b>x</b>

**Actual:** &lt;b&gt;x&lt;/b&gt;

**Reproducer:**

```python
from markupsafe import EscapeFormatter, escape

class X:
    def __html__(self):
        return "<b>x</b>"

x = X()
expected = x.__html__()  # Documented trusted HTML, independently of escape.
if type(expected) is not str:
    print("REFUTATION REJECTED: __html__ did not return a plain str")
else:
    actual = EscapeFormatter(escape).format_field(x, "")
    if actual != expected:
        print(f"REFUTATION CONFIRMED: input={expected!r} actual={actual!r} expected={expected!r}")
    else:
        print("REFUTATION REJECTED: trusted HTML was preserved")
```

**Output:**

```
REFUTATION CONFIRMED: input='<b>x</b>' actual='&lt;b&gt;x&lt;/b&gt;' expected='<b>x</b>'
```

Judge: BUG (medium) -- The input is valid: __html__ returns a plain str representing trusted HTML. The formatter calls that method but then escapes its returned string, losing the trust associated with __html__. This contradicts the documented treatment of __html__ output as already safe. The expected value is independently obtained from __html__, not inferred from the failing formatter. No duplicate is listed.

