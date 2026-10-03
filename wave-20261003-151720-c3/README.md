*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wave`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Short reads cause the reader's frame position to undercount

Target: `wave.Wave_read.readframes`

Property: For a valid PCM WAVE containing N complete frames, read through a seekable binary in-memory stream whose read(size) can return fewer bytes than requested. After successive readframes(1) calls have returned all audio bytes, tell() must equal N, independently of how the underlying stream fragments reads.

### Draft issue: wave.Wave_read loses frame position when underlying reads split frames

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

**Documented behaviour:** The module's reading API documentation states: "tell() -- return the current position" and "The position returned by tell() and the position given to setpos() are compatible and have nothing to do with the actual position in the file."

**Expected:** After returning both bytes of the single audio frame, tell() returns 1.

**Actual:** Two readframes(1) calls return one byte each; tell() remains 0 even after EOF.

**Reproducer:**

```python
import io
import struct
import wave

payload = b"\x00\x01"
case = dict(channels=1, sample_width=2, frames=1,
            short_read_limit=1, audio_payload=payload)
wav = (b"RIFF" + struct.pack("<I", 36 + len(payload)) + b"WAVEfmt " +
       struct.pack("<IHHIIHH", 16, 1, 1, 8000, 16000, 2, 16) +
       b"data" + struct.pack("<I", len(payload)) + payload)

class Fragmented(io.BytesIO):
    def read(self, size=-1):
        if self.tell() >= 44 and size > 0:
            size = min(size, case["short_read_limit"])
        return super().read(size)

try:
    with wave.open(io.BytesIO(wav), "rb") as reference:
        valid = (reference.getparams() == (1, 2, 8000, 1, "NONE", "not compressed")
                 and reference.readframes(2) == payload
                 and len(payload) % 2 == 0)
    if not valid:
        print("REFUTATION REJECTED:", "input is not the reported complete PCM WAVE")
    else:
        expected = (payload, len(payload) // (case["channels"] * case["sample_width"]))
        with wave.open(Fragmented(wav), "rb") as reader:
            chunks = []
            while True:
                chunk = reader.readframes(1)
                if not chunk:
                    break
                chunks.append(chunk)
            actual = (b"".join(chunks), reader.tell())
        if actual[0] == payload and actual != expected:
            print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED:", "all-byte position mismatch not reproduced",
                  "actual:", actual, "expected:", expected)
except Exception as exc:
    print("REFUTATION REJECTED:", type(exc).__name__, str(exc))
```

**Output:**

```
REFUTATION CONFIRMED: {'channels': 1, 'sample_width': 2, 'frames': 1, 'short_read_limit': 1, 'audio_payload': b'\x00\x01'} actual: (b'\x00\x01', 0) expected: (b'\x00\x01', 1)
```

Judge: BUG (medium) -- The reproducer supplies a valid one-frame PCM WAVE and fragments only audio reads. Short reads are permitted for binary file-like streams. Both audio bytes are returned, but readframes counts complete frames separately for each returned fragment, losing the frame split across calls. Consequently tell() no longer represents the consumed audio-frame position compatible with setpos(). The supplied upstream diff does not fix this behavior, and no duplicate is listed.

