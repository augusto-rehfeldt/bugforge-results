# bugforge: `difflib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: ndiff ignores a junk predicate when the callable itself is falsey

Target: `difflib.ndiff`

Property: For lists of strings a and b and a deterministic callable predicate p, list(ndiff(a, b, linejunk=p)) must equal list(ndiff(a, b, linejunk=lambda line: p(line))). Wrapping a predicate without changing its results must not change which lines are treated as junk, including when bool(p) is False.

### Draft issue: difflib ignores falsey callable linejunk predicates

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

**Documented behaviour:** The Python library documentation for difflib.ndiff describes linejunk as: "A function that accepts a single string argument, and returns true if the string is junk, or false if not."

**Expected:** ['- A\n', '  B\n', '+ A\n'] with either the predicate or its result-preserving wrapper

**Actual:** Direct predicate: ['+ B\n', '  A\n', '- B\n']; wrapped predicate: ['- A\n', '  B\n', '+ A\n']

**Reproducer:**

```python
import difflib

class Predicate:
    def __call__(self, line):
        return line == "A\n"

    def __bool__(self):
        return False

a, b, p = ["A\n", "B\n"], ["B\n", "A\n"], Predicate()
data = {"a": a, "b": b,
        "p": {"junk_membership": ["A\n"], "__bool__": False}}

if not (callable(p) and all(
    isinstance(s, str) and type(p(s)) is bool and p(s) == p(s)
    for s in a + b
)):
    print("REFUTATION REJECTED: input violates the documented predicate contract")
else:
    actual = list(difflib.ndiff(a, b, linejunk=p))
    # Independent alignment: B is the sole nonjunk anchor; A moves past it.
    expected = ["- " + a[0], "  " + a[1], "+ " + b[1]]
    wrapped = list(difflib.ndiff(a, b, linejunk=lambda s: p(s)))
    if actual != expected and wrapped == expected:
        print("REFUTATION CONFIRMED:", data,
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: no independently verified wrapper discrepancy",
              data, "actual:", actual, "expected:", expected, "wrapped:", wrapped)
```

WARNING: the tracker search was incomplete (ndiff linejunk predicate bool False: HTTPError: HTTP Error 403: rate limit exceeded; difflib linejunk wrapper changes output: HTTPError: HTTP Error 403: rate limit exceeded); search it by hand before filing.

**Output:**

```
REFUTATION CONFIRMED: {'a': ['A\n', 'B\n'], 'b': ['B\n', 'A\n'], 'p': {'junk_membership': ['A\n'], '__bool__': False}} actual: ['+ B\n', '  A\n', '- B\n'] expected: ['- A\n', '  B\n', '+ A\n']
```

Judge: BUG (low) -- The callable is deterministic and returns actual booleans, satisfying the documented linejunk contract. Its own truth value does not change whether a line is junk. The reproducer correctly identifies B as the nonjunk anchor, and the wrapper produces that alignment. Passing the falsey callable directly instead anchors on junk line A, demonstrating that predicate truthiness incorrectly disables junk filtering. No duplicates were found, but the tracker was not fully checked because both searches failed with HTTP 403 rate-limit errors.

