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