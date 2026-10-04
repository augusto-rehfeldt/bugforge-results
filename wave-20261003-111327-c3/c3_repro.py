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