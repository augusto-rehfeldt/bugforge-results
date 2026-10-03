# bugforge: `calendar`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `calendar`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: HTML calendar does not preserve stylesheet filenames containing HTML-sensitive characters

Target: `calendar.HTMLCalendar.formatyearpage`

Property: For a valid integer year (1–9999) and a nonempty stylesheet filename css, decoding the returned UTF-8 page and parsing its stylesheet link as HTML must yield an href attribute equal to css. Include filenames containing ampersands and double quotes, which are valid Windows filename characters.

### Draft issue: Escape the stylesheet href in calendar.HTMLCalendar.formatyearpage

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `calendar`

**Documented behaviour:** Python calendar documentation, HTMLCalendar.formatyearpage: “css is the name of the cascading style sheet to be used.”

**Expected:** The parsed stylesheet href is a&notin;.css; the HTML source should escape its ampersand.

**Actual:** The parsed stylesheet href is a∉.css.

**Reproducer:**

```python
import calendar
from html.parser import HTMLParser

data = dict(year=2024, width=3, encoding="utf-8", css="a&notin;.css")

class Links(HTMLParser):
    hrefs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "stylesheet":
            self.hrefs.append(a.get("href"))

if not (type(data["year"]) is int and 1 <= data["year"] <= 9999
        and isinstance(data["css"], str) and data["css"]
        and data["width"] == 3 and data["encoding"] == "utf-8"):
    print("REFUTATION REJECTED: invalid input")
else:
    parser = Links()
    parser.feed(calendar.HTMLCalendar().formatyearpage(
        data["year"], width=data["width"], encoding=data["encoding"],
        css=data["css"]).decode("utf-8"))
    parser.close()
    expected = data["css"]  # The documented stylesheet name, unchanged.
    if parser.hrefs != [expected]:
        actual = parser.hrefs[0] if len(parser.hrefs) == 1 else parser.hrefs
        print("REFUTATION CONFIRMED:", data, "actual =", repr(actual),
              "expected =", repr(expected))
    else:
        print("REFUTATION REJECTED: parsed href equals the stylesheet name")
```

**Output:**

```
REFUTATION CONFIRMED: {'year': 2024, 'width': 3, 'encoding': 'utf-8', 'css': 'a&notin;.css'} actual = 'a∉.css' expected = 'a&notin;.css'
```

Judge: BUG (low) -- The documented css argument names the stylesheet to use. The valid filename a&notin;.css is emitted without HTML attribute escaping, so parsing resolves &notin; to ∉ and selects a different stylesheet. The reproducer correctly compares the parsed href with the supplied name. Double quotes are not valid Windows filename characters, but that does not invalidate the ampersand example. No duplicates were listed.

