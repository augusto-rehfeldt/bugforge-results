import random
import string
import time
from email.headerregistry import Address

DOMAIN = "example.com"
DEADLINE = time.monotonic() + 170.0


def reference(username):
    # RFC 5322 dot-atom: nonempty atext runs separated by single dots.
    # All non-dot characters in our input alphabet are ASCII letters (atext).
    is_dot_atom = all(part for part in username.split("."))
    local = username if is_dot_atom else '"' + username + '"'
    return (local + "@" + DOMAIN, username, DOMAIN)


def actual(username):
    try:
        addr_spec = Address(username=username, domain=DOMAIN).addr_spec
    except Exception as exc:
        return ("construction error", type(exc).__name__, str(exc))
    try:
        parsed = Address(addr_spec=addr_spec)
        return (addr_spec, parsed.username, parsed.domain)
    except Exception as exc:
        return (addr_spec, "parse error", type(exc).__name__, str(exc))


for username in ("alice", "a.b"):
    expected = reference(username)
    result = actual(username)
    print("SANITY:", repr(username), "actual:", repr(result),
          "expected:", repr(expected))
    if result != expected:
        print("SANITY FAILED")
        raise SystemExit(0)

tested = 0


def check(username):
    global tested
    expected = reference(username)
    result = actual(username)
    tested += 1
    if result != expected:
        repeated = actual(username)
        if repeated != expected:
            print("COUNTEREXAMPLE:", repr(username),
                  "actual:", repr(repeated), "expected:", repr(expected))
            raise SystemExit(0)


for username in (
    ".a", "a.", "a..b", ".", "..", "...", ".a.", "..a",
    "a..", "a...b", ".A.B.", "a.b", "Alice", "A.b.C",
):
    check(username)

rng = random.Random(20260217)
alphabet = string.ascii_letters + "."
for _ in range(200000):
    if time.monotonic() >= DEADLINE:
        break
    length = rng.randint(1, 80)
    username = "".join(rng.choice(alphabet) for _ in range(length))
    mode = rng.randrange(6)
    if mode == 0:
        username = "." + username
    elif mode == 1:
        username += "."
    elif mode == 2:
        pos = rng.randrange(len(username) + 1)
        username = username[:pos] + ".." + username[pos:]
    elif mode == 3:
        username = "." * rng.randint(1, 20)
    check(username)

print("NO COUNTEREXAMPLE", tested)