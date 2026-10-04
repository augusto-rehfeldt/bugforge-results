*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `struct`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Reinitializing a Struct may prevent its existing iterator from advancing

Target: `struct.Struct.iter_unpack`

Property: For S = struct.Struct('B') and a nonempty bytes buffer b, create it = S.iter_unpack(b), then call S.__init__('0s'). The iterator must still terminate after finitely many next() calls, rather than repeatedly yielding tuples without consuming the buffer. Test termination within len(b) + 1 calls.

### Draft issue: Struct reinitialization to a zero-sized format makes an existing iter_unpack iterator nonterminating

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

**Documented behaviour:** Python 3.14 Library Reference, struct.iter_unpack: “This function returns an iterator which will read equally-sized chunks from the buffer until all its contents have been consumed.” Struct.iter_unpack is documented as “Identical to the iter_unpack() function, using the compiled format.”

**Expected:** The iterator should consume the original one-byte buffer and terminate within two next() calls, or incompatible reinitialization should be rejected.

**Actual:** After reinitialization to '0s', both next() calls yield (b'',) without advancing, leaving the iterator nonterminating.

**Reproducer:**

```python
import struct

b = b'\x00'
try:
    S = struct.Struct('B')
    size = S.size
    if not size or not b or len(b) % size:
        print('REFUTATION REJECTED: invalid buffer or chunk size')
    else:
        limit = len(b) // size + 1
        expected = {'terminated': True, 'within_calls': limit}
        it = S.iter_unpack(b)
        S.__init__('0s')
        yielded = []
        terminated = False
        for calls in range(1, limit + 1):
            try:
                yielded.append(next(it))
            except StopIteration:
                terminated = True
                break
        actual = dict(terminated=terminated, calls=calls, yielded=yielded)
        if not terminated:
            print('REFUTATION CONFIRMED:', repr(b), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED: iterator terminated within', limit, 'calls')
except Exception as e:
    print('REFUTATION REJECTED:', type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: b'\x00' actual: {'terminated': False, 'calls': 2, 'yielded': [(b'',), (b'',)]} expected: {'terminated': True, 'within_calls': 2}
```

Judge: BUG (medium) -- The original format and buffer are valid, and reinitializing the Struct succeeds. The existing iterator then uses the new zero-sized format, yielding without consuming any bytes. This violates the documented consumption-and-termination behavior; no cited limitation excludes Struct reinitialization. The two-call bound is correct for the original one-byte chunk size.

