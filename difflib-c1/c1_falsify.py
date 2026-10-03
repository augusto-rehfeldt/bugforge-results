import difflib
import random
import time
from fractions import Fraction


def reference_ratio(a, b):
    # Independent implementation of recursive longest-contiguous-block matching.
    # All generated sequences are shorter than the autojunk threshold.
    def matched(alo, ahi, blo, bhi):
        best_i, best_j, best_size = alo, blo, 0
        for i in range(alo, ahi):
            for j in range(blo, bhi):
                size = 0
                while (i + size < ahi and j + size < bhi
                       and a[i + size] == b[j + size]):
                    size += 1
                if size > best_size:
                    best_i, best_j, best_size = i, j, size
        if not best_size:
            return 0
        total = best_size
        if alo < best_i and blo < best_j:
            total += matched(alo, best_i, blo, best_j)
        if best_i + best_size < ahi and best_j + best_size < bhi:
            total += matched(best_i + best_size, ahi,
                             best_j + best_size, bhi)
        return total

    length = len(a) + len(b)
    return Fraction(2 * matched(0, len(a), 0, len(b)), length) if length else Fraction(1)


def expected_result(word, possibilities, n, cutoff):
    threshold = Fraction(cutoff)
    ranked = [(reference_ratio(candidate, word), index, candidate)
              for index, candidate in enumerate(possibilities)]
    ranked = [item for item in ranked if item[0] >= threshold]
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in ranked[:n]]


def acceptable(actual, expected, word, possibilities):
    if not isinstance(actual, list) or len(actual) != len(expected):
        return False
    remaining = list(possibilities)
    for candidate in actual:
        try:
            remaining.remove(candidate)
        except ValueError:
            return False
    return ([reference_ratio(candidate, word) for candidate in actual]
            == [reference_ratio(candidate, word) for candidate in expected])


def invoke(word, possibilities, n, cutoff):
    try:
        return True, difflib.get_close_matches(word, possibilities, n, cutoff)
    except Exception as exc:
        return False, (type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    for word, possibilities, n, cutoff in [
        ("appel", ["apple", "ape", "banana"], 2, 0.6),
        ("abcd", ["abcd", "abce", "xyz"], 3, 0.5),
    ]:
        expected = expected_result(word, possibilities, n, cutoff)
        ok, actual = invoke(word, possibilities, n, cutoff)
        agrees = ok and acceptable(actual, expected, word, possibilities)
        print("SANITY:", repr(actual), repr(expected), agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    tested = 0

    def check(case):
        nonlocal tested
        word, possibilities, n, cutoff = case
        expected = expected_result(word, possibilities, n, cutoff)
        tested += 1
        ok, actual = invoke(word, possibilities, n, cutoff)
        if ok and acceptable(actual, expected, word, possibilities):
            return False
        # Repeat the identical input before reporting.
        ok2, actual2 = invoke(word, possibilities, n, cutoff)
        if ok2 and acceptable(actual2, expected, word, possibilities):
            return False
        print("COUNTEREXAMPLE:")
        print(repr({
            "word": word,
            "possibilities": possibilities,
            "n": n,
            "cutoff": cutoff,
        }))
        print("actual:", repr(actual2) if ok2 else "exception " + repr(actual2))
        print("expected:", repr(expected))
        return True

    edge_cases = [
        ([0j, 3j], [[0j, 1j], [0j, 2j]], 3, 0.5),
    ]
    for candidates in ([[0j, 1j], [0j, 2j]],
                       [[0j, 2j], [0j, 1j]]):
        for n in (1, 2, 3):
            for cutoff in (0.0, 0.5, 0.5000000000000001, 1.0):
                edge_cases.append(([0j, 3j], candidates, n, cutoff))
    edge_cases.extend([
        ([], [], 1, 0.0),
        ([], [[], [1j], [2j]], 3, 0.0),
        ([3j], [[1j], [2j]], 2, 0.0),
    ])
    for case in edge_cases:
        if check(case):
            return

    rng = random.Random(20260317)
    alphabet = [complex(real, imag) for real in range(3) for imag in range(4)]
    while time.monotonic() - start < 175:
        word = [rng.choice(alphabet) for _ in range(rng.randrange(13))]
        possibilities = [
            [rng.choice(alphabet) for _ in range(rng.randrange(13))]
            for _ in range(rng.randrange(10))
        ]
        cutoff = rng.choice([0.0, 0.25, 0.5, 0.75, 1.0])
        if possibilities and rng.randrange(2):
            cutoff = float(reference_ratio(rng.choice(possibilities), word))
        if check((word, possibilities, rng.randrange(1, 12), cutoff)):
            return
    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()