*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `markupsafe`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: translate marks unescaped replacement text as HTML-safe

Target: `markupsafe.Markup.translate`

Property: For any single ASCII letter c and plain string replacement r, Markup(c).translate({ord(c): r}) must equal Markup.escape(r) and return a Markup instance, since r is newly inserted text rather than trusted markup.

### Draft issue: Escape plain-string replacements in Markup.translate

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `markupsafe` 3.0.4

**Documented behaviour:** Markup class documentation: "This is a subclass of :class:`str`. It has the same methods, but escapes their arguments and returns a ``Markup`` instance."

**Expected:** Markup('&amp;')

**Actual:** Markup('&')

**Reproducer:**

```python
import html
import markupsafe

c, r = "a", "&"
table = {ord(c): r}
if not (len(c) == 1 and c.isascii() and c.isalpha() and type(r) is str):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        actual = markupsafe.Markup(c).translate(table)
        expected = html.escape(r, quote=True).replace("&#x27;", "&#39;")
        if actual != expected or not isinstance(actual, markupsafe.Markup):
            print(f"REFUTATION CONFIRMED: input={(c, table)!r}, actual={actual!r}, expected={expected!r}")
        else:
            print("REFUTATION REJECTED: documented escaping and return type hold")
    except Exception as e:
        print(f"REFUTATION REJECTED: could not reproduce: {e}")
```

**Output:**

```
REFUTATION CONFIRMED: input=('a', {97: '&'}), actual=Markup('&'), expected='&amp;'
```

Judge: BUG (medium) -- The input is valid, and the expected escaping of '&' to '&amp;' is correct. translate inserts a plain string from the translation table without escaping it, contrary to the documented promise that Markup methods escape their arguments. Returning a Markup instance then marks that unescaped replacement as safe. No duplicate is listed.

