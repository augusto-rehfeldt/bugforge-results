import random
import time
import zlib


def compress(dictionary, payload):
    compressor = zlib.compressobj(wbits=15, zdict=bytes(dictionary))
    return compressor.compress(payload) + compressor.flush()


def check(dictionary, payload):
    dictionary = bytearray(dictionary)
    stream = compress(dictionary, payload)
    try:
        decompressor = zlib.decompressobj(wbits=15, zdict=dictionary)
        output = decompressor.decompress(stream[:1])
        dictionary[:] = bytes(value ^ 255 for value in dictionary)
        output += decompressor.decompress(stream[1:])
        output += decompressor.flush()
        return output
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    deadline = start + 175
    rng = random.Random(0xD1C710)

    # The expected bytes are the original, explicitly constructed payloads,
    # not the result of any decompression operation.
    sanity_cases = [
        (b"A", b"A" * 100),
        (bytes(range(256)), bytes(range(256)) * 8 + b"ordinary input"),
    ]
    sanity_ok = True
    for index, (dictionary, expected) in enumerate(sanity_cases, 1):
        try:
            stream = compress(dictionary, expected)
            decompressor = zlib.decompressobj(wbits=15, zdict=dictionary)
            actual = decompressor.decompress(stream[:1])
            actual += decompressor.decompress(stream[1:])
            actual += decompressor.flush()
            agrees = actual == expected
        except Exception:
            agrees = False
        print("SANITY {}: {}".format(index, "PASS" if agrees else "FAIL"))
        sanity_ok = sanity_ok and agrees
    if not sanity_ok:
        print("SANITY FAILED")
        return

    tested = 0

    def test(dictionary, payload):
        nonlocal tested
        dictionary = bytes(dictionary)
        payload = bytes(payload)
        actual = check(dictionary, payload)
        tested += 1
        if actual != payload:
            confirmed = check(dictionary, payload)
            if confirmed == actual:
                print("COUNTEREXAMPLE:")
                print(repr({
                    "dictionary": bytearray(dictionary),
                    "payload": payload,
                    "mutation": "replace each byte b with b ^ 255",
                    "first_chunk_length": 1,
                    "wbits": 15,
                }))
                print("actual:", repr(confirmed))
                print("expected:", repr(payload))
                return True
        return False

    edge_dictionaries = [
        b"\x00",
        b"A",
        b"\xff",
        bytes(range(256)),
        b"\x00" * 256,
        bytes(range(255, -1, -1)),
        bytes(range(256)) * 128,
        b"A" * 32768,
        bytes(rng.randrange(256) for _ in range(32768)),
    ]
    for dictionary in edge_dictionaries:
        payloads = [
            dictionary * 4,
            dictionary[-min(512, len(dictionary)):] * 32,
            b"prefix:" + dictionary * 2 + b":suffix",
        ]
        for payload in payloads:
            if test(dictionary, payload):
                return

    while time.monotonic() < deadline:
        length = rng.choice([1, 256, 32768, rng.randint(1, 32768)])
        if rng.randrange(3) == 0:
            pattern = bytes(rng.randrange(256) for _ in range(rng.randint(1, 32)))
            dictionary = (pattern * ((length + len(pattern) - 1) // len(pattern)))[:length]
        else:
            dictionary = bytes(rng.randrange(256) for _ in range(length))

        offset = rng.randrange(length)
        size = rng.randint(1, min(4096, length - offset))
        substring = dictionary[offset:offset + size]
        prefix = bytes(rng.randrange(256) for _ in range(rng.randrange(33)))
        suffix = bytes(rng.randrange(256) for _ in range(rng.randrange(33)))
        payload = prefix + substring * rng.randint(2, 32) + suffix
        if test(dictionary, payload):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()