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