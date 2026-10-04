*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: SortedDict.update may ignore mapping entries when a dict subclass overrides iteration

Target: `sortedcontainers.SortedDict.update`

Property: For a nonempty SortedDict d with integer keys and values, and a dict subclass m whose keys() and __getitem__ expose its stored entries but whose __iter__ yields no keys, d.update(m) must produce the same key-value mapping as ordinary dict.update applied to the same initial mapping and m.

### Draft issue: SortedDict.update skips dict-subclass entries when __iter__ differs from keys()

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** "Update sorted dict with items from `args` and `kwargs`." — SortedDict.update documentation. The documented dict-like update operation consumes a mapping's entries.

**Expected:** The original 100 entries plus 100: 1000.

**Actual:** Only the original 100 entries remain; 100: 1000 is missing.

**Reproducer:**

```python
try:
    from sortedcontainers import SortedDict

    class M(dict):
        def __iter__(self):
            return iter(())

    initial = {i: -i for i in range(100)}
    m = M({100: 1000})
    entries = {k: m[k] for k in m.keys()}
    d = SortedDict(initial)
    if not d or entries != {100: 1000} or list(m) or not all(
        type(k) is type(v) is int for k, v in initial.items()
    ):
        print("REFUTATION REJECTED: invalid input")
    else:
        expected = initial.copy()
        expected.update(m)
        d.update(m)
        actual = dict(d.items())
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"initial": initial, "M_entries": entries},
                  "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: actual matches dict.update")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
 -33, 34: -34, 35: -35, 36: -36, 37: -37, 38: -38, 39: -39, 40: -40, 41: -41, 42: -42, 43: -43, 44: -44, 45: -45, 46: -46, 47: -47, 48: -48, 49: -49, 50: -50, 51: -51, 52: -52, 53: -53, 54: -54, 55: -55, 56: -56, 57: -57, 58: -58, 59: -59, 60: -60, 61: -61, 62: -62, 63: -63, 64: -64, 65: -65, 66: -66, 67: -67, 68: -68, 69: -69, 70: -70, 71: -71, 72: -72, 73: -73, 74: -74, 75: -75, 76: -76, 77: -77, 78: -78, 79: -79, 80: -80, 81: -81, 82: -82, 83: -83, 84: -84, 85: -85, 86: -86, 87: -87, 88: -88, 89: -89, 90: -90, 91: -91, 92: -92, 93: -93, 94: -94, 95: -95, 96: -96, 97: -97, 98: -98, 99: -99} expected: {0: 0, 1: -1, 2: -2, 3: -3, 4: -4, 5: -5, 6: -6, 7: -7, 8: -8, 9: -9, 10: -10, 11: -11, 12: -12, 13: -13, 14: -14, 15: -15, 16: -16, 17: -17, 18: -18, 19: -19, 20: -20, 21: -21, 22: -22, 23: -23, 24: -24, 25: -25, 26: -26, 27: -27, 28: -28, 29: -29, 30: -30, 31: -31, 32: -32, 33: -33, 34: -34, 35: -35, 36: -36, 37: -37, 38: -38, 39: -39, 40: -40, 41: -41, 42: -42, 43: -43, 44: -44, 45: -45, 46: -46, 47: -47, 48: -48, 49: -49, 50: -50, 51: -51, 52: -52, 53: -53, 54: -54, 55: -55, 56: -56, 57: -57, 58: -58, 59: -59, 60: -60, 61: -61, 62: -62, 63: -63, 64: -64, 65: -65, 66: -66, 67: -67, 68: -68, 69: -69, 70: -70, 71: -71, 72: -72, 73: -73, 74: -74, 75: -75, 76: -76, 77: -77, 78: -78, 79: -79, 80: -80, 81: -81, 82: -82, 83: -83, 84: -84, 85: -85, 86: -86, 87: -87, 88: -88, 89: -89, 90: -90, 91: -91, 92: -92, 93: -93, 94: -94, 95: -95, 96: -96, 97: -97, 98: -98, 99: -99, 100: 1000}
```

Judge: BUG (medium) -- The input is a valid dict subclass whose keys() and __getitem__ expose {100: 1000}. Mapping-style update consumes those entries, not the subclass's overridden __iter__; the ordinary dict.update baseline correctly adds them. SortedDict.update silently skips the entry, violating its documented dict-like update behavior. No duplicate was found, though the development branch was not compared.

