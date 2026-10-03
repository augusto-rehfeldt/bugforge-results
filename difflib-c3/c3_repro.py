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