*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wave`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: writeframesraw silently loses audio on short writes

Target: `wave.Wave_write.writeframesraw`

Property: For a writable, seekable in-memory binary stream whose write() may legally return a positive count smaller than the supplied buffer length, writing complete PCM frames with writeframesraw() and closing must produce a WAV whose readframes(-1) equals the supplied audio bytes.

### Draft issue: wave.Wave_write silently loses audio data on short writes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

**Documented behaviour:** The module docstring, under 'Writing WAVE files', says: 'The open file pointer must have methods write(), tell(), seek(), and close().' It describes writeframesraw(data) as 'write audio frames without patching up the file header'. Binary raw streams may return short write counts.

**Expected:** readframes(-1) returns b'\x13\\'.

**Actual:** readframes(-1) returns b'\x13'; the WAV header declares two audio bytes although only one was written.

**Reproducer:**

```python
import io
import wave

case = {'payload': b'\x13\\', 'cap': 1, 'rate': 8000}

class ShortStream(io.BytesIO):
    def write(self, data):
        return super().write(data[:case['cap']] if self.tell() >= 44 else data)

stream = ShortStream()
payload = case['payload']
if not (stream.writable() and stream.seekable()
        and all(callable(getattr(stream, m, None))
                for m in ('write', 'tell', 'seek', 'close'))
        and case['rate'] > 0 and 0 < case['cap'] < len(payload)):
    print('REFUTATION REJECTED:', 'invalid input')
else:
    expected = bytes(payload)  # Mono, 8-bit PCM: every byte is a complete frame.
    try:
        writer = wave.open(stream, 'wb')
        writer.setparams((1, 1, case['rate'], 0, 'NONE', 'not compressed'))
        writer.writeframesraw(payload)
        writer.close()
        stream.seek(0)
        with wave.open(stream, 'rb') as reader:
            actual = reader.readframes(-1)
    except Exception as error:
        actual = repr(error)
    if actual != expected:
        print('REFUTATION CONFIRMED:', case, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'audio matches expected bytes')
```

**Output:**

```
REFUTATION CONFIRMED: {'payload': b'\x13\\', 'cap': 1, 'rate': 8000} actual: b'\x13' expected: b'\x13\\'
```

Judge: BUG (medium) -- The stream satisfies the documented file-object requirements, and both payload bytes are complete mono 8-bit PCM frames. writeframesraw() ignores the positive short-write count and accounts for both bytes as written, silently losing the second byte. Closing cannot repair this because the recorded byte count already matches the declared data length. The supplied upstream diff does not fix short writes, and the listed issues concern read-side memory allocation, not this behaviour.

