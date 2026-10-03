# bugforge: `shlex`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `shlex`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Popping a source leaks its buffered punctuation into the restored source

Target: `shlex.pop_source`

Property: For nonempty strings P and C containing only ASCII letters, construct shlex(P + ' ', posix=True, punctuation_chars=';'), push_source(C + ';tail'), consume the token C, then call pop_source(). Iterating the restored lexer must yield exactly [P], with no characters from the popped source.

### Draft issue: shlex.pop_source() leaks punctuation buffered from the popped source

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `shlex`

**Documented behaviour:** Python standard-library documentation, shlex.pop_source(): "Pop the last-pushed input source from the input stack." Together with shlex.push_source(): "Push an input source stream onto the input stack."

**Expected:** ['a']

**Actual:** [';', 'a']

**Reproducer:**

```python
import shlex

P, C = 'a', 'b'
if not all(s and s.isascii() and s.isalpha() for s in (P, C)):
    print('REFUTATION REJECTED: input must be nonempty ASCII letters')
else:
    expected = list(shlex.shlex(P + ' ', posix=True, punctuation_chars=';'))
    lexer = shlex.shlex(P + ' ', posix=True, punctuation_chars=';')
    lexer.push_source(C + ';tail')
    token = lexer.get_token()
    if token != C:
        print('REFUTATION REJECTED: pushed token was', repr(token))
    else:
        lexer.pop_source()
        actual = list(lexer)
        if actual != expected:
            print('REFUTATION CONFIRMED:', (P, C), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED: restored source matches independent reference')
```

**Output:**

```
REFUTATION CONFIRMED: ('a', 'b') actual: [';', 'a'] expected: ['a']
```

Judge: BUG (low) -- The reproducer uses valid inputs and computes the reference correctly. Reading 'b' buffers the following ';' from the pushed source. pop_source() restores the original stream but leaves that buffered character available, so subsequent tokenization leaks content from the popped source. This violates the documented source-stack behavior, not a documented limitation. No matching issue or pull request was provided.

