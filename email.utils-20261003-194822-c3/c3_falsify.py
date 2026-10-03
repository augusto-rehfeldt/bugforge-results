import email.utils
import random
import re
import string
import time

LETTERS = string.ascii_letters
deadline = time.monotonic() + 175.0
rng = random.Random(472901)
tested = 0

# Independent reference for the restricted, bare addr-spec input space.
label = r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
domain_pattern = re.compile(rf"{label}(?:\.{label})*\Z", re.ASCII)
local_pattern = re.compile(r"[A-Za-z]+(?:\.[A-Za-z]+)*\Z", re.ASCII)


def reference(address):
    parts = address.split("@")
    if len(parts) != 2:
        return ("", "")
    local, domain = parts
    if not domain_pattern.fullmatch(domain):
        return ("", "")
    if not local_pattern.fullmatch(local):
        return ("", "")
    return ("", address)


for address in ("alice@example.com", "Alice.Bob@mail.example.org"):
    expected = reference(address)
    try:
        actual = email.utils.parseaddr(address, strict=True)
    except Exception as exc:
        print("SANITY CHECK:", repr(address), type(exc).__name__, repr(expected))
        print("SANITY FAILED")
        raise SystemExit(0)
    print("SANITY CHECK:", repr(address), repr(actual), repr(expected))
    if actual != expected:
        print("SANITY FAILED")
        raise SystemExit(0)


def check(address):
    global tested
    expected = reference(address)
    tested += 1
    try:
        actual = email.utils.parseaddr(address, strict=True)
    except Exception:
        # Exceptions on malformed addresses are not counterexamples.
        return
    if actual == expected:
        return
    try:
        repeated = email.utils.parseaddr(address, strict=True)
    except Exception:
        return
    if repeated == actual:
        print("COUNTEREXAMPLE:", repr(address), repr(actual), repr(expected))
        raise SystemExit(0)


edges = [
    "a..b@example.com",
    "a...b@example.com",
    "a....b@example.com",
    "A..Z@EXAMPLE.COM",
    "ab..cd@x.org",
    "a..b@a-b.example",
]
for length in (1, 2, 63, 64, 127, 256, 1024):
    for dots in (2, 3, 4, 8, 32, 128):
        edges.append("a" * length + "." * dots + "b@example.com")
        edges.append("a" + "." * dots + "b" * length + "@example.com")

for address in edges:
    if time.monotonic() >= deadline:
        break
    check(address)


def letters(length):
    return "".join(rng.choices(LETTERS, k=length))


def random_domain():
    labels = []
    for _ in range(rng.randint(1, 4)):
        length = rng.randint(1, 30)
        if length == 1:
            labels.append(rng.choice(LETTERS))
        else:
            labels.append(
                rng.choice(LETTERS)
                + "".join(rng.choices(LETTERS + string.digits + "-", k=length - 2))
                + rng.choice(LETTERS + string.digits)
            )
    return ".".join(labels + [rng.choice(("com", "org", "net", "example"))])


while time.monotonic() < deadline:
    a = letters(rng.randint(1, 256))
    b = letters(rng.randint(1, 256))
    dots = rng.choice((2, 2, 2, 3, 4, 5, 8, 16, 32, 64))
    check(a + "." * dots + b + "@" + random_domain())

print("NO COUNTEREXAMPLE", tested)