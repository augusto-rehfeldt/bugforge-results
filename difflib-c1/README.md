# bugforge: `difflib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Equal-score matches require undocumented ordering of sequence elements

Target: `difflib.get_close_matches`

Property: For word and possibilities consisting of finite lists of complex numbers, positive integer n, and cutoff in [0, 1], get_close_matches must return the highest-scoring qualifying candidates, up to n, sorted by decreasing similarity, without raising TypeError. Ties may appear in any order.

### Draft issue: difflib.get_close_matches raises TypeError for tied matches containing non-orderable elements

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `difflib`

**Documented behaviour:** get_close_matches docstring: "word is a sequence for which close matches are desired (typically a string)." "possibilities is a list of sequences against which to match word (typically a list of strings)." "The best (no more than n) matches among the possibilities are returned in a list, sorted by similarity score, most similar first."

**Expected:** Return both candidates, in either order, since both score 0.5 and n is 3.

**Actual:** Raises TypeError: '<' not supported between instances of 'complex' and 'complex'.

**Reproducer:**

```python
import difflib
from collections import Counter

data = dict(word=[0j, 3j], possibilities=[[0j, 1j], [0j, 2j]], n=3, cutoff=0.5)
w, ps, n, cutoff = data.values()

def matches(a, b):
    best, i, j = 0, 0, 0
    for x in range(len(a)):
        for y in range(len(b)):
            k = 0
            while x+k < len(a) and y+k < len(b) and a[x+k] == b[y+k]:
                k += 1
            if k > best:
                best, i, j = k, x, y
    return (best + matches(a[:i], b[:j]) + matches(a[i+best:], b[j+best:])
            if best else 0)

def score(p):
    return 2 * matches(w, p) / (len(w) + len(p))

valid = (
    isinstance(ps, list)
    and all(isinstance(s, list) and all(isinstance(x, complex) for x in s)
            for s in [w] + ps)
    and isinstance(n, int) and n > 0 and 0 <= cutoff <= 1
)
if not valid:
    print("REFUTATION REJECTED:", "input violates documented requirements")
else:
    expected = sorted((p for p in ps if score(p) >= cutoff),
                      key=score, reverse=True)[:n]
    try:
        actual = difflib.get_close_matches(**data)
        # Both reported candidates tie, so accept either ordering.
        ok = (isinstance(actual, list)
              and Counter(map(tuple, actual)) == Counter(map(tuple, expected)))
    except Exception as e:
        actual = (type(e).__name__, str(e))
        ok = False
    if ok:
        print("REFUTATION REJECTED:", "actual matches the documented expectation")
    else:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'word': [0j, 3j], 'possibilities': [[0j, 1j], [0j, 2j]], 'n': 3, 'cutoff': 0.5} actual: ('TypeError', "'<' not supported between instances of 'complex' and 'complex'") expected: [[0j, 1j], [0j, 2j]]
```

Judge: BUG (medium) -- The documented sequence inputs are valid: complex elements are hashable and support equality, as required by SequenceMatcher. Both candidates have similarity 0.5 and qualify. get_close_matches ranks (score, candidate) tuples, so tied scores trigger ordering comparisons between candidates and ultimately complex elements, raising TypeError. No documented requirement makes sequence elements orderable, and arbitrary tie ordering does not permit an exception.

