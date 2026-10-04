import random
import time
from wcwidth import iter_graphemes

VIRAMA = "\u094d"
KA = "\u0915"


def reference(s):
    # Independent reference for the tested alphabet and patterns:
    # GB9 attaches each virama (Extend) to the preceding cluster.
    # A leading run has no initial InCB=Consonant, so GB9c cannot
    # suppress the boundary between that run and the final KA.
    clusters = []
    for char in s:
        if char == VIRAMA and clusters:
            clusters[-1] += char
        else:
            clusters.append(char)
    return clusters


def main():
    deadline = time.monotonic() + 170.0

    sanity_failed = False
    for s in ("abc", KA + VIRAMA):
        expected = reference(s)
        actual = list(iter_graphemes(s))
        print("SANITY:", repr(s), repr(actual), repr(expected))
        if actual != expected:
            sanity_failed = True
    if sanity_failed:
        print("SANITY FAILED")
        return

    tested = 0

    def check(k):
        nonlocal tested
        s = VIRAMA * k + KA
        # Exact reference for this restricted input family.
        expected = [VIRAMA * k, KA]
        actual = list(iter_graphemes(s))
        tested += 1
        if actual != expected:
            repeated = list(iter_graphemes(s))
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr(s))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    edges = (
        1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64,
        127, 128, 255, 256, 1023, 1024, 4096, 16384,
        65536, 262144,
    )
    for k in edges:
        if time.monotonic() >= deadline:
            break
        if check(k):
            return

    rng = random.Random(0x094D0915)
    while time.monotonic() < deadline:
        mode = rng.randrange(4)
        if mode == 0:
            k = rng.randint(1, 8)
        elif mode == 1:
            k = rng.randint(1, 1024)
        elif mode == 2:
            k = rng.randint(1025, 262144)
        else:
            k = max(1, (1 << rng.randrange(19)) + rng.randint(-2, 2))
        if check(k):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()