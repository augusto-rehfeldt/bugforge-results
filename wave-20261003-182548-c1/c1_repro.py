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