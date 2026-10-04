*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `shlex`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `shlex`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Pushed source is prefixed by punctuation buffered from its parent

Target: `shlex.push_source`

Property: For nonempty ASCII alphabetic strings p and c, construct L = shlex.shlex(p + ';tail', posix=True, punctuation_chars=';') and consume p using get_token(). After L.push_source(c + ' '), the next token must be c, not punctuation belonging to the suspended parent stream.

### Draft issue: shlex.push_source leaks buffered parent punctuation into pushed source

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `shlex`

**Documented behaviour:** The shlex documentation, under shlex.push_source(), states: "Push an input source stream onto the input stack." The source attribute documentation describes stacked input processing: "When the end of that file is reached, files are popped off the stack until the original input stream is resumed." Together these require the pushed source to be processed before resuming its parent.

**Expected:** The next token after push_source('b ') is 'b'; the parent's ';' is returned only after the pushed source ends.

**Actual:** The next token is ';', punctuation from the suspended parent stream.

**Reproducer:**

```python
import shlex

p, c = 'a', 'b'
if not all(s and s.isascii() and s.isalpha() for s in (p, c)):
    print('REFUTATION REJECTED: invalid input')
else:
    L = shlex.shlex(p + ';tail', posix=True, punctuation_chars=';')
    if L.get_token() != p:
        print('REFUTATION REJECTED: parent token was not consumed as required')
    else:
        L.push_source(c + ' ')
        actual, expected = L.get_token(), c
        if actual != expected:
            print('REFUTATION CONFIRMED:', (p, c),
                  'actual:', repr(actual), 'expected:', repr(expected))
        else:
            print('REFUTATION REJECTED: pushed source was processed first')
```

**Output:**

```
REFUTATION CONFIRMED: ('a', 'b') actual: ';' expected: 'b'
```

Judge: BUG (medium) -- The reproducer uses valid inputs and correctly consumes the parent token before pushing a new source. The documented source-stack ordering requires reading the pushed source before resuming the parent. Instead, punctuation buffered while reading the parent token leaks into the pushed source's tokenization. The upstream changes shown do not address this behavior, and no duplicate was found.

