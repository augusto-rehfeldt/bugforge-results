# bugforge: `difflib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: HtmlDiff silently removes literal SOH characters from unchanged text

Target: `difflib.HtmlDiff.make_table`

Property: For identical one-line inputs [s], where s is a nonempty string containing no tabs, newlines, carriage returns, or HTML metacharacters, make_table([s], [s]) must preserve s as the decoded text content of each corresponding source-text cell. In particular, embedded U+0001 characters must not disappear.

### Draft issue: difflib.HtmlDiff drops literal U+0001 characters from source lines

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

**Documented behaviour:** Python difflib documentation, HtmlDiff.make_table: "Returns a string which is a complete HTML table showing a side by side, line by line comparison of the lines with inter-line and intra-line changes highlighted." Showing the input lines requires preserving their text, apart from documented display transformations.

**Expected:** Both source-text cells decode to 'A\x01B'.

**Actual:** Both source-text cells decode to 'AB'.

**Reproducer:**

```python
import difflib
from html.parser import HTMLParser

s = 'A\x01B'

class Cells(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells, self.active = [], False
    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.active = any(k == 'nowrap' for k, v in attrs)
            if self.active:
                self.cells.append('')
    def handle_data(self, data):
        if self.active:
            self.cells[-1] += data
    def handle_endtag(self, tag):
        if tag == 'td':
            self.active = False

if not isinstance(s, str) or not s or any(c in s for c in '\t\n\r<>&"\''):
    print('REFUTATION REJECTED: input violates the stated restrictions')
else:
    p = Cells()
    p.feed(difflib.HtmlDiff().make_table([s], [s]))
    actual, expected = p.cells, [s, s]
    if len(actual) != 2:
        print('REFUTATION REJECTED: could not identify both source-text cells')
    elif actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', repr(actual),
              'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED: both cells preserve the input')
```

**Output:**

```
REFUTATION CONFIRMED: 'A\x01B' actual: ['AB', 'AB'] expected: ['A\x01B', 'A\x01B']
```

Judge: BUG (low) -- The reproducer supplies valid identical string inputs and correctly extracts both source-text cells. HtmlDiff uses U+0001 as an internal highlighting delimiter and replaces literal occurrences without distinguishing them from generated markers, silently losing input text. This contradicts the documented line-by-line display; no cited limitation excludes control characters. The listed encoding issue is unrelated.

