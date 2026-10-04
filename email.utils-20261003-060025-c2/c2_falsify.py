import random
import time
from email.utils import decode_params


def reference(params):
    """Reference for contiguous continuations with an unencoded first segment."""
    parts = []
    any_encoded = False
    for index, (name, value) in enumerate(params[1:]):
        encoded = name.endswith("*")
        assert name == "filename*{}".format(index) + ("*" if encoded else "")
        assert index != 0 or not encoded
        any_encoded |= encoded
        if encoded:
            decoded = bytearray()
            position = 0
            while position < len(value):
                if value[position] == "%":
                    decoded.append(int(value[position + 1:position + 3], 16))
                    position += 3
                else:
                    decoded.append(ord(value[position]))
                    position += 1
            parts.append(decoded.decode("ascii"))
        else:
            parts.append(value)

    value = "".join(parts)
    quoted = '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    # Charset and language can only be declared in an encoded initial segment.
    result = (None, None, quoted) if any_encoded else quoted
    return [params[0], ("filename", result)]


def observe(params):
    try:
        return decode_params(params[:])
    except Exception as error:
        return ("EXCEPTION", type(error).__name__, str(error))


def main():
    sanity_cases = [
        [("text/plain", ""), ("filename*0", "ab"), ("filename*1", "c")],
        [("text/plain", ""), ("filename*0", "ab"), ("filename*1*", "%63")],
    ]
    for index, params in enumerate(sanity_cases, 1):
        expected = reference(params)
        actual = observe(params)
        print("SANITY {}: actual={!r}, expected={!r}".format(index, actual, expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0

    def check(params):
        nonlocal tested
        expected = reference(params)
        actual = observe(params)
        tested += 1
        if actual != expected:
            repeated = observe(params)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr(params))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    hand_picked = [
        [("text/plain", ""), ("filename*0", "a'b'"), ("filename*1*", "%63")],
        [("text/plain", ""), ("filename*0", "''"), ("filename*1*", "%41")],
        [("text/plain", ""), ("filename*0", "'a'"), ("filename*1*", "%27")],
        [
            ("text/plain", ""),
            ("filename*0", "x'y'z"),
            ("filename*1", "tail"),
            ("filename*2*", "%20%63"),
        ],
    ]
    for params in hand_picked:
        if check(params):
            return

    rng = random.Random(2231)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ._-"
    while time.monotonic() - start < 175:
        chunks = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(12)))
            for _ in range(3)
        ]
        initial = chunks[0] + "'" + chunks[1] + "'" + chunks[2]
        params = [("text/plain", ""), ("filename*0", initial)]
        count = rng.randint(1, 6)
        mandatory_encoded = rng.randint(1, count)
        for index in range(1, count + 1):
            value = "".join(
                rng.choice(alphabet + "'") for _ in range(rng.randint(1, 15))
            )
            encoded = index == mandatory_encoded or rng.choice([False, True])
            if encoded:
                value = "".join("%{:02X}".format(ord(char)) for char in value)
            params.append(("filename*{}".format(index) + ("*" if encoded else ""), value))
        if check(params):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()