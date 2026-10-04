*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `markupsafe`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: HTML-format protocol output is escaped instead of trusted

Target: `markupsafe.EscapeFormatter.format_field`

Property: For any object x implementing __html_format__(spec) but not __html__, where that method returns a plain string h representing safe HTML, and any nonempty format specification spec accepted by that method, EscapeFormatter(escape).format_field(x, spec) must equal h.

### Draft issue: EscapeFormatter escapes safe plain-string results from __html_format__

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

**Documented behaviour:** MarkupSafe's String Formatting documentation states: “If an object has an __html_format__ method, it is called instead of __format__. It is passed the format specifier and must return a string that is already safe for HTML.”

**Expected:** <em>hello</em>

**Actual:** &lt;em&gt;hello&lt;/em&gt;

**Reproducer:**

```python
try:
    import markupsafe as m

    spec, html = "link", "<em>hello</em>"

    class X:
        def __html_format__(self, spec):
            if spec != "link":
                raise ValueError("unsupported spec")
            return html

    x = X()
    expected = x.__html_format__(spec)
    if not spec or hasattr(x, "__html__") or type(expected) is not str or expected != html:
        print("REFUTATION REJECTED: invalid input")
    else:
        actual = m.EscapeFormatter(m.escape).format_field(x, spec)
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"spec": spec, "html": html},
                  "actual:", repr(actual), "expected:", repr(expected))
        else:
            print("REFUTATION REJECTED: actual matches documented expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'spec': 'link', 'html': '<em>hello</em>'} actual: '&lt;em&gt;hello&lt;/em&gt;' expected: '<em>hello</em>'
```

Judge: BUG (medium) -- The input satisfies the documented __html_format__ contract: the method accepts the nonempty specifier and returns a string containing safe HTML. The expected value is correctly computed. Escaping that result contradicts the promise that it is already safe for HTML. No duplicate was identified.

