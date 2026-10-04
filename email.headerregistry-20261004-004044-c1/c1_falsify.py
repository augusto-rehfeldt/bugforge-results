import random
import time
from email.headerregistry import Address


def reference(s):
    """Parse the restricted, valid addr-spec grammar generated below."""
    assert s.startswith("user@")
    domain = s[5:]
    if not domain.startswith("["):
        assert domain == "example.com"
        return ("user", domain)

    assert domain.endswith("]")
    body = domain[1:-1]
    decoded = []
    i = 0
    while i < len(body):
        c = body[i]
        if c == "\\":
            i += 1
            assert i < len(body)
            assert 32 <= ord(body[i]) <= 126
            decoded.append(body[i])
        else:
            assert 33 <= ord(c) <= 90 or 94 <= ord(c) <= 126
            decoded.append(c)
        i += 1
    return ("user", "[" + "".join(decoded) + "]")


def evaluate(s):
    expected = reference(s)
    try:
        first = Address(addr_spec=s)
    except Exception:
        return None  # Only initially accepted inputs are relevant.

    rendered = first.addr_spec
    initial = (first.username, first.domain)
    try:
        second = Address(addr_spec=rendered)
        actual = (second.username, second.domain)
    except Exception as exc:
        actual = ("EXCEPTION", type(exc).__name__, str(exc))

    # Independently check the parsed meaning as well as round-trip preservation.
    failed = actual != expected and actual != initial
    return failed, {
        "initial": initial,
        "serialized": rendered,
        "reconstructed": actual,
    }, expected


def main():
    for s in ("user@example.com", "user@[abc]"):
        expected = reference(s)
        try:
            first = Address(addr_spec=s)
            second = Address(addr_spec=first.addr_spec)
            actual = (first.username, first.domain)
            reconstructed = (second.username, second.domain)
            ok = actual == reconstructed == expected
        except Exception as exc:
            actual = (type(exc).__name__, str(exc))
            ok = False
        print("SANITY:", repr(s), "actual:", repr(actual),
              "expected:", repr(expected), "OK" if ok else "FAILED")
        if not ok:
            print("SANITY FAILED")
            return

    rng = random.Random(5322)
    deadline = time.monotonic() + 175
    ordinary = "".join(chr(n) for n in range(33, 127)
                       if n not in (91, 92, 93))
    escaped = "".join(chr(n) for n in range(32, 127))
    handpicked = [
        'user@[a\\]b]',
        'user@[a\\\\b]',
        'user@[\\]]',
        'user@[\\\\]',
        'user@[a\\[b]',
        'user@[a\\ b]',
        'user@[a\\]\\]b]',
        'user@[a\\\\\\]b]',
        'user@[a\\(b\\)c]',
    ]
    tested = 0

    while time.monotonic() < deadline:
        if handpicked:
            s = handpicked.pop(0)
        else:
            pieces = []
            for _ in range(rng.randint(1, 60)):
                if rng.random() < 0.55:
                    c = rng.choice("]\\[" if rng.random() < 0.7 else escaped)
                    pieces.append("\\" + c)
                else:
                    pieces.append(rng.choice(ordinary))
            s = "user@[" + "".join(pieces) + "]"

        result = evaluate(s)
        if result is None:
            continue
        tested += 1
        if result[0]:
            repeated = evaluate(s)
            if repeated is not None and repeated[0] and repeated == result:
                print("COUNTEREXAMPLE:", repr(s))
                print("actual:", repr(repeated[1]))
                print("expected:", repr(repeated[2]))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()