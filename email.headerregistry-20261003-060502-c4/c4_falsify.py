import random
import sys
import time
from email.headerregistry import HeaderRegistry

deadline = time.monotonic() + 175
registry = HeaderRegistry()
rng = random.Random(314159)
tested = 0


def reference(value):
    # Independently implement the documented grammar for this input space.
    parts = value.split(".")
    return (
        len(parts) == 2
        and all(parts)
        and all("0" <= char <= "9" for part in parts for char in part)
    )


def actual(value):
    try:
        registry("MIME-Version", value)
        return True, "constructed without exception"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


for value in ("1.0", "12.34"):
    expected = reference(value)
    observed, detail = actual(value)
    tested += 1
    print(f"SANITY {value!r}: actual={observed}, expected={expected}")
    if observed != expected:
        print("SANITY FAILED")
        sys.exit(0)


def check(value):
    global tested
    expected = reference(value)
    assert expected, "Test generator produced invalid input"
    observed, detail = actual(value)
    tested += 1
    if observed != expected:
        confirmed, confirmed_detail = actual(value)
        tested += 1
        if confirmed != expected:
            print("COUNTEREXAMPLE:", repr(value))
            print("actual:", confirmed_detail)
            print("expected: constructed without exception")
            sys.exit(0)


limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
anchor = limit if limit else 4300

# Hand-picked boundaries, testing both integer components independently.
sizes = sorted({
    1, 2, 10,
    max(1, anchor - 1),
    anchor,
    anchor + 1,
    anchor + 2,
    anchor * 2,
})
for n in sizes:
    for value in ("1." + "1" * n, "1" * n + ".0"):
        if time.monotonic() >= deadline:
            print("NO COUNTEREXAMPLE", tested)
            sys.exit(0)
        check(value)

# Fixed-seed sampling mixes short controls with near-limit and above-limit cases.
for _ in range(10000):
    if time.monotonic() >= deadline:
        break
    mode = rng.randrange(3)
    if mode == 0:
        n = rng.randint(1, 100)
    elif mode == 1:
        n = max(1, anchor + rng.randint(-32, 128))
    else:
        n = rng.randint(anchor + 1, anchor * 2 + 100)
    value = "1." + "1" * n if rng.randrange(2) else "1" * n + ".0"
    check(value)

print("NO COUNTEREXAMPLE", tested)