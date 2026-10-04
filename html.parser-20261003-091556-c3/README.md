*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `html.parser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: DOCTYPE declarations are truncated at greater-than signs inside quoted identifiers

Target: `html.parser.HTMLParser.handle_decl`

Property: For every declaration s = '<!DOCTYPE html SYSTEM "' + identifier + '">', where identifier contains no double quote and is a valid system identifier, feeding s and calling close() must invoke handle_decl exactly once with s[2:-1], including any '>' characters inside identifier.

### Draft issue: HTMLParser truncates DOCTYPE declarations at '>' inside quoted system identifiers

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

**Documented behaviour:** Python Library Reference, html.parser, HTMLParser.handle_decl: "The decl parameter will be the entire contents of the declaration inside the <! ... > markup (e.g. 'DOCTYPE html')."

**Expected:** handle_decl called exactly once with 'DOCTYPE html SYSTEM "a>b"'.

**Actual:** handle_decl called with the truncated string 'DOCTYPE html SYSTEM "a'.

**Reproducer:**

```python
from html.parser import HTMLParser
from xml.parsers.expat import ParserCreate

s = '<!DOCTYPE html SYSTEM "' + 'a>b' + '">'
actual, declarations = [], []

try:
    validator = ParserCreate()
    validator.StartDoctypeDeclHandler = lambda *args: declarations.append(args)
    validator.Parse(s + '<html/>', True)
    if declarations != [('html', 'a>b', None, 0)]:
        raise ValueError('system identifier was not preserved')
except Exception as e:
    print('REFUTATION REJECTED:', 'invalid declaration:', str(e))
else:
    parser = HTMLParser()
    parser.handle_decl = actual.append
    parser.feed(s)
    parser.close()
    expected = [s[2:-1]]
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'actual matches documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: '<!DOCTYPE html SYSTEM "a>b">' actual: ['DOCTYPE html SYSTEM "a'] expected: ['DOCTYPE html SYSTEM "a>b"']
```

Judge: BUG (medium) -- The declaration is valid: '>' is permitted within a quoted system identifier, and the reproducer independently confirms its preservation with Expat. The documented promise to pass the entire declaration contents is violated by terminating at the quoted '>'. The expected slice is correct. No listed issue or pull request duplicates this behaviour, and the supplied upstream changes do not fix declaration parsing.

