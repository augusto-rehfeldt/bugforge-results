import difflib
import random
import sys
import time

LIMIT = sys.getrecursionlimit()
DEADLINE = time.monotonic() + 175
EXPECTED = "HTML table string (no exception)"


def reference(s):
    # The documented contract applies to every nonempty ASCII-letter string.
    assert s and all("a" <= c <= "z" or "A" <= c <= "Z" for c in s)
    return EXPECTED


def evaluate(s):
    try:
        result = difflib.HtmlDiff(wrapcolumn=1).make_table([s], [s])
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"
    valid = (
        isinstance(result, str)
        and result.lstrip().startswith("<table")
        and result.rstrip().endswith("</table>")
    )
    return valid, EXPECTED if valid else repr(result)


for s in ("a", "aaa"):
    expected = reference(s)
    ok, actual = evaluate(s)
    print(f"SANITY {s!r}: actual={actual!r}, expected={expected!r}", flush=True)
    if not ok or actual != expected:
        print("SANITY FAILED")
        sys.exit(0)

tested = 0


def check(length):
    global tested
    s = "a" * length
    expected = reference(s)
    ok, actual = evaluate(s)
    tested += 1
    if not ok:
        confirmed, repeated_actual = evaluate(s)
        if not confirmed:
            print("COUNTEREXAMPLE:")
            print(repr(s))
            print("actual:", repr(repeated_actual))
            print("expected:", repr(expected))
            sys.exit(0)


edges = (
    1, 2, 10,
    max(1, LIMIT - 10),
    max(1, LIMIT - 1),
    LIMIT,
    LIMIT + 1,
    2 * LIMIT,
    2 * LIMIT + 1,
)
for length in dict.fromkeys(edges):
    if time.monotonic() >= DEADLINE:
        break
    check(length)

rng = random.Random(20250308)
while time.monotonic() < DEADLINE:
    if rng.randrange(2):
        length = max(1, LIMIT + rng.randint(-100, 100))
    else:
        length = rng.randint(1, 3 * LIMIT)
    check(length)

print("NO COUNTEREXAMPLE", tested)