*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `zlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `zlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Preset dictionary remains dependent on mutable input after the first decompress call

Target: `zlib.decompressobj`

Property: For a nonempty bytearray dictionary D and payload P compressed using an immutable snapshot of D, construct decompressobj(zdict=D), then call decompress() with only the first byte of the compressed stream. Modifying D afterward, without changing its length, must not prevent subsequent decompress() calls and flush() from recovering P: the documented interval during which dictionary mutation is prohibited has ended.

### Draft issue: zlib.decompressobj fails after documented-safe zdict mutation with a partial initial header

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `zlib`

**Documented behaviour:** Python Library Reference, zlib.decompressobj(): “If zdict is a mutable object (such as a bytearray), you must not modify its contents between the call to decompressobj() and the first call to the decompressor’s decompress() method.”

**Expected:** Subsequent decompress() calls and flush() recover b'\x00\x00\x00\x00' using the original dictionary contents.

**Actual:** The subsequent decompress() call raises zlib.error: Error -3 while setting zdict: invalid input data.

**Reproducer:**

```python
import zlib

D = bytearray(b"\0")
P = b"\0" * 4
case = dict(dictionary=D[:], payload=P, mutation="replace each byte b with b ^ 255",
            first_chunk_length=1, wbits=15)
try:
    snapshot = bytes(D)
    c = zlib.compressobj(wbits=15, zdict=snapshot)
    stream = c.compress(P) + c.flush()
    reference = zlib.decompressobj(wbits=15, zdict=snapshot)
    expected = reference.decompress(stream) + reference.flush()
    if not D or expected != P or not reference.eof:
        print("REFUTATION REJECTED:", "input failed immutable-dictionary validation")
    else:
        try:
            d = zlib.decompressobj(wbits=15, zdict=D)
            actual = d.decompress(stream[:1])
            # Mutation occurs after the first decompress() call, as documented.
            D[:] = bytes(b ^ 255 for b in D)
            actual += d.decompress(stream[1:]) + d.flush()
        except Exception as e:
            actual = ("EXCEPTION", type(e).__name__, str(e))
        if actual != expected:
            print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED:", "documented expectation was recovered")
except Exception as e:
    print("REFUTATION REJECTED:", "validation/setup failed:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'dictionary': bytearray(b'\x00'), 'payload': b'\x00\x00\x00\x00', 'mutation': 'replace each byte b with b ^ 255', 'first_chunk_length': 1, 'wbits': 15} actual: ('EXCEPTION', 'error', 'Error -3 while setting zdict: invalid input data') expected: b'\x00\x00\x00\x00'
```

Judge: BUG (medium) -- The reproducer uses a valid stream verified with an immutable dictionary snapshot. It mutates the bytearray only after the first decompress() call, outside the documented prohibited interval. A one-byte initial chunk apparently delays dictionary installation, allowing the later mutation to cause failure despite compliance with the documented contract. Neither listed issue identifies this mutation-timing defect.

