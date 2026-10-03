*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wave`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Sequential WAV reading incorrectly requires seek when tell is available

Target: `wave.open`

Property: For a complete valid PCM WAV supplied through a binary file-like object implementing read(), tell(), and close(), but not seek(), wave.open(stream, 'rb') must succeed and permit sequential reading of all audio frames without using setpos() or rewind().

### Draft issue: wave.open fails on non-seekable input streams that implement tell()

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

**Documented behaviour:** The wave module's opening documentation states: "When the setpos() and rewind() methods are not used, the seek() method is not necessary."

**Expected:** Opening succeeds; sequential reads return (b'', b'\xce', b'$', b'', b'').

**Actual:** AttributeError: 'Stream' object has no attribute 'seek'

**Reproducer:**

```python
import struct
import wave

wav = b'RIFF&\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x02\x00\x00\x00\xce$'
requests = (0, 1, 2, 3, 1)

class Stream:
    def __init__(self):
        self.pos = 0
    def read(self, n=-1):
        end = len(wav) if n < 0 else min(len(wav), self.pos + n)
        data = wav[self.pos:end]
        self.pos = end
        return data
    def tell(self):
        return self.pos
    def close(self):
        pass

def main():
    try:
        fields = struct.unpack('<4sI4s4sIHHIIHH4sI2s', wav)
        valid = fields == (
            b'RIFF', len(wav) - 8, b'WAVE', b'fmt ', 16,
            1, 1, 8000, 8000, 1, 8, b'data', 2, b'\xce$'
        )
    except struct.error:
        valid = False
    if not valid:
        print('REFUTATION REJECTED:', 'input is not the complete PCM WAV claimed')
        return

    audio = fields[-1]
    pos = 0
    chunks = []
    for n in requests:
        chunks.append(audio[pos:pos + n])
        pos = min(len(audio), pos + n)
    expected = ('ok', (1, 1, 8000, len(audio), 'NONE', 'not compressed'),
                tuple(chunks))
    try:
        with wave.open(Stream(), 'rb') as reader:
            actual = ('ok', tuple(reader.getparams()),
                      tuple(reader.readframes(n) for n in requests))
    except Exception as exc:
        actual = ('exception', type(exc).__name__, str(exc))

    if actual != expected:
        print('REFUTATION CONFIRMED:',
              {'wav': wav, 'read_requests': requests},
              'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'sequential reading matches the documented expectation')

main()
```

**Output:**

```
REFUTATION CONFIRMED: {'wav': b'RIFF&\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x02\x00\x00\x00\xce$', 'read_requests': (0, 1, 2, 3, 1)} actual: ('exception', 'AttributeError', "'Stream' object has no attribute 'seek'") expected: ('ok', (1, 1, 8000, 2, 'NONE', 'not compressed'), (b'', b'\xce', b'$', b'', b''))
```

Judge: BUG (medium) -- The reproducer supplies a complete, valid 46-byte PCM WAV with correct RIFF and chunk lengths. Its expected parameters and sequential frame results are correct, and it never calls setpos() or rewind(). Requiring seek() therefore violates the explicit documented promise. Successful tell() causes the internal chunk reader to assume seeking is available; skipping the consumed fmt chunk then attempts the missing seek(). The supplied upstream diff leaves this path unchanged, and the listed Unicode issue is unrelated.

