import difflib
import random
import time


class FalseyJunk:
    def __init__(self, junk):
        self.junk = frozenset(junk)

    def __call__(self, line):
        return line in self.junk

    def __bool__(self):
        return False


def reference_ndiff(a, b, junk):
    """Independent reference for the single-character lines used below."""
    assert all(len(s) == 2 and s.endswith("\n") for s in a + b)

    def longest(alo, ahi, blo, bhi):
        best_i, best_j, best_size = alo, blo, 0
        previous = {}
        for i in range(alo, ahi):
            current = {}
            for j in range(blo, bhi):
                if b[j] not in junk and a[i] == b[j]:
                    size = previous.get(j - 1, 0) + 1
                    current[j] = size
                    if size > best_size:
                        best_i, best_j, best_size = i - size + 1, j - size + 1, size
            previous = current

        while (best_i > alo and best_j > blo
               and b[best_j - 1] not in junk
               and a[best_i - 1] == b[best_j - 1]):
            best_i -= 1
            best_j -= 1
            best_size += 1
        while (best_i + best_size < ahi and best_j + best_size < bhi
               and b[best_j + best_size] not in junk
               and a[best_i + best_size] == b[best_j + best_size]):
            best_size += 1
        while (best_i > alo and best_j > blo
               and b[best_j - 1] in junk
               and a[best_i - 1] == b[best_j - 1]):
            best_i -= 1
            best_j -= 1
            best_size += 1
        while (best_i + best_size < ahi and best_j + best_size < bhi
               and b[best_j + best_size] in junk
               and a[best_i + best_size] == b[best_j + best_size]):
            best_size += 1
        return best_i, best_j, best_size

    pending = [(0, len(a), 0, len(b))]
    blocks = []
    while pending:
        alo, ahi, blo, bhi = pending.pop()
        i, j, size = longest(alo, ahi, blo, bhi)
        if size:
            blocks.append((i, j, size))
            if alo < i and blo < j:
                pending.append((alo, i, blo, j))
            if i + size < ahi and j + size < bhi:
                pending.append((i + size, ahi, j + size, bhi))

    merged = []
    for i, j, size in sorted(blocks):
        if merged and merged[-1][0] + merged[-1][2] == i and merged[-1][1] + merged[-1][2] == j:
            pi, pj, ps = merged[-1]
            merged[-1] = pi, pj, ps + size
        else:
            merged.append((i, j, size))
    merged.append((len(a), len(b), 0))

    output = []

    def replace(alo, ahi, blo, bhi):
        # Different single-character lines have character similarity 1/2,
        # below Differ's 3/4 synchronization threshold. Only exact lines
        # can synchronize a replacement.
        for j in range(blo, bhi):
            for i in range(alo, ahi):
                if a[i] == b[j]:
                    replace(alo, i, blo, j)
                    output.append("  " + a[i])
                    replace(i + 1, ahi, j + 1, bhi)
                    return
        deleted = ["- " + s for s in a[alo:ahi]]
        inserted = ["+ " + s for s in b[blo:bhi]]
        if bhi - blo < ahi - alo:
            output.extend(inserted + deleted)
        else:
            output.extend(deleted + inserted)

    ai = bj = 0
    for i, j, size in merged:
        replace(ai, i, bj, j)
        output.extend("  " + s for s in a[i:i + size])
        ai, bj = i + size, j + size
    return output


def main():
    sanity = [
        (["A\n", "B\n"], ["A\n", "C\n"], frozenset()),
        (["A\n", "B\n"], ["B\n", "A\n"], frozenset({"A\n"})),
    ]
    for number, (a, b, junk) in enumerate(sanity, 1):
        expected = reference_ndiff(a, b, junk)
        actual = list(difflib.ndiff(a, b, linejunk=lambda line: line in junk))
        print("SANITY", number, actual == expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    rng = random.Random(741093)
    alphabet = ["A\n", "B\n", "C\n", "D\n"]
    edges = [
        (["A\n", "B\n"], ["B\n", "A\n"], {"A\n"}),
        (["A\n", "A\n", "B\n"], ["B\n", "A\n", "A\n"], {"A\n"}),
        ([], [], {"A\n"}),
        ([], ["A\n", "A\n"], {"A\n"}),
        (["A\n", "A\n"], [], {"A\n"}),
        (["A\n"], ["A\n"], {"A\n"}),
    ]
    count = 0
    while time.monotonic() - start < 170:
        if count < len(edges):
            a, b, junk = edges[count]
        else:
            a = [rng.choice(alphabet) for _ in range(rng.randrange(13))]
            b = [rng.choice(alphabet) for _ in range(rng.randrange(13))]
            junk = {s for s in alphabet if rng.randrange(2)}
        count += 1
        p = FalseyJunk(junk)
        expected = reference_ndiff(a, b, p.junk)
        actual = list(difflib.ndiff(a, b, linejunk=p))
        if actual != expected:
            again = list(difflib.ndiff(a, b, linejunk=FalseyJunk(junk)))
            expected_again = reference_ndiff(a, b, frozenset(junk))
            if again == actual and expected_again == expected:
                print("COUNTEREXAMPLE:")
                print(repr({
                    "a": a,
                    "b": b,
                    "p": {"junk_membership": sorted(junk), "__bool__": False},
                }))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return
    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()