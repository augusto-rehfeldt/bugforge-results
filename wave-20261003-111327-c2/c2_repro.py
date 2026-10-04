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