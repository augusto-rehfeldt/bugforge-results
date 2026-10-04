import random
import time
from wcwidth import grapheme_boundary_before

def main():
    deadline = time.monotonic() + 175
    rng = random.Random(0x524547494F4E414C)
    alphabet = [chr(cp) for cp in range(0x1F1E6, 0x1F200)]
    cases = 0

    def reference(text, pos):
        # A run of regional indicators clusters into pairs from its start.
        assert len(text) % 2 == 0
        assert all(0x1F1E6 <= ord(ch) <= 0x1F1FF for ch in text)
        assert 1 <= pos < len(text) and pos % 2 == 1
        return pos - 1

    def actual(text, pos):
        try:
            return grapheme_boundary_before(text, pos)
        except Exception as exc:
            return ("EXCEPTION", type(exc).__name__, str(exc))

    for text, pos in [
        ("\U0001F1FA\U0001F1F8", 1),
        ("\U0001F1FA\U0001F1F8\U0001F1E8\U0001F1E6", 3),
    ]:
        expected = reference(text, pos)
        result = actual(text, pos)
        print("SANITY:", repr(text), pos, result, expected)
        if result != expected:
            print("SANITY FAILED")
            return

    def check(text):
        nonlocal cases
        # Check the end first, then every remaining odd position.
        positions = (len(text) - 1,)
        for pos in positions:
            if not check_position(text, pos):
                return False
        for pos in range(1, len(text) - 1, 2):
            if not check_position(text, pos):
                return False
        return True

    def check_position(text, pos):
        nonlocal cases
        if time.monotonic() >= deadline:
            return False
        expected = pos - 1
        result = actual(text, pos)
        cases += 1
        if result != expected:
            repeated = actual(text, pos)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr((text, pos)))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return False
        return True

    hand_picked = [
        alphabet[0] * 2,
        alphabet[-1] * 4,
        "".join(alphabet[:6]),
        "".join(alphabet),
        "".join(reversed(alphabet)) * 2,
    ]
    for length in (6, 8, 16, 32, 64, 128, 256, 512,
                   1024, 4096, 16384, 65536):
        hand_picked.append(alphabet[0] * length)
        hand_picked.append((alphabet[0] + alphabet[-1]) * (length // 2))

    for text in hand_picked:
        if not check(text):
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", cases)
            return

    while time.monotonic() < deadline:
        length = 2 * rng.choice([
            rng.randint(1, 128),
            rng.randint(129, 2048),
            rng.randint(2049, 16384),
        ])
        if rng.randrange(3) == 0:
            text = rng.choice(alphabet) * length
        else:
            text = "".join(rng.choices(alphabet, k=length))
        if not check(text):
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", cases)
            return

    print("NO COUNTEREXAMPLE", cases)

if __name__ == "__main__":
    main()