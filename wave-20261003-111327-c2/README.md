*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wave`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Writer tell() counts frames that a short write did not actually write

Target: `wave.Wave_write.tell`

Property: For a writer backed by a seekable in-memory binary stream whose write() may return a positive short count, configured with valid PCM parameters, tell() after writeframesraw(data) must equal the number of complete audio frames actually written. Generate data consisting entirely of complete frames, and restrict short writes to the audio payload so the WAV header is written completely.

### Draft issue: wave: handle short payload writes before advancing Wave_write frame position

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

**Documented behaviour:** The wave documentation for Wave_write.tell() says: "Return current position in the file, with the same disclaimer for Wave_read.tell()." Wave_read.tell() specifies: "Return current file pointer position, in audio frames."

**Expected:** tell() returns 2 for the two complete audio frames actually written, or writeframesraw() completes the remaining writes before reporting 4.

**Actual:** tell() returns 4 although only 2 audio frames were written.

**Reproducer:**

```python
import io
import wave

class ShortWrite(io.BytesIO):
    def write(self, data):
        return super().write(data[:2] if self.tell() == 44 else data)

case = dict(channels=1, sample_width=1, rate=8000,
            data=b'\x00\x01\x02\x03', accepted_frames=2)
try:
    frame_size = case["channels"] * case["sample_width"]
    if not (case["channels"] > 0 and 1 <= case["sample_width"] <= 4
            and case["rate"] > 0 and len(case["data"]) % frame_size == 0):
        raise ValueError("invalid PCM input")
    stream = ShortWrite()
    if not stream.seekable():
        raise ValueError("stream is not seekable")
    writer = wave.open(stream, "wb")
    writer.setparams((1, 1, 8000, 0, "NONE", "not compressed"))
    writer.writeframesraw(case["data"])
    actual = writer.tell()
    raw = stream.getvalue()
    if raw[:4] != b"RIFF" or raw[8:12] != b"WAVE" or raw[36:40] != b"data":
        raise ValueError("header was not written completely")
    expected = len(raw[44:]) // frame_size
    writer.close()
    if actual != expected:
        print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "tell() matches actual complete frames")
except Exception as exc:
    print("REFUTATION REJECTED:", str(exc))
```

**Output:**

```
REFUTATION CONFIRMED: {'channels': 1, 'sample_width': 1, 'rate': 8000, 'data': b'\x00\x01\x02\x03', 'accepted_frames': 2} actual: 4 expected: 2
```

Judge: BUG (medium) -- The reproducer uses valid PCM parameters and complete frames. Its stream writes the entire header but accepts only two of the four payload bytes, returning 2. Wave_write ignores that return count and advances its frame counter by the requested payload length, so tell() contradicts the documented position in audio frames. The supplied upstream diff does not fix this, and no duplicate is listed.

