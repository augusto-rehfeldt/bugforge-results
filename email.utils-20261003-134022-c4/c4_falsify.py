import email.utils
import random
import string
import time


def reference(mailbox):
    local, domain = mailbox.split("@")
    assert local and all(
        atom and all(c in string.ascii_letters for c in atom)
        for atom in local.split(".")
    )
    assert domain.startswith("[") and domain.endswith("]")
    octets = domain[1:-1].split(".")
    assert len(octets) == 4
    assert all(
        octet and all(c in string.digits for c in octet)
        and 0 <= int(octet) <= 255
        for octet in octets
    )
    return [("", mailbox)]


def call(mailbox):
    try:
        return ("result", email.utils.getaddresses([mailbox], strict=True))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175
    for mailbox in ("alice@example.com", "Bob.Smith@example.org"):
        expected = [("", mailbox)]
        actual = call(mailbox)
        print("SANITY:", repr(mailbox), repr(actual), repr(expected))
        if actual != ("result", expected):
            print("SANITY FAILED")
            return

    tested = 0

    def check(mailbox):
        nonlocal tested
        expected = reference(mailbox)
        actual = call(mailbox)
        tested += 1
        if actual == ("result", expected):
            return False
        repeated = call(mailbox)
        if repeated == ("result", expected):
            return False
        displayed = repeated[1] if repeated[0] == "result" else repeated
        print("COUNTEREXAMPLE:", repr(mailbox),
              "actual:", repr(displayed), "expected:", repr(expected))
        return True

    edges = [
        "alice@[127.0.0.1]",
        "a@[0.0.0.0]",
        "Z@[255.255.255.255]",
        "Alice.Bob@[0.255.0.255]",
        "x@[255.0.255.0]",
        "A.B.C@[1.2.3.4]",
        "abcdefghijklmnopqrstuvwxyz@[254.255.0.1]",
    ]
    for mailbox in edges:
        if check(mailbox):
            return

    rng = random.Random(2822)
    while time.monotonic() < deadline:
        local = ".".join(
            "".join(rng.choice(string.ascii_letters)
                    for _ in range(rng.randint(1, 24)))
            for _ in range(rng.randint(1, 5))
        )
        octets = [rng.randrange(256) for _ in range(4)]
        mailbox = local + "@[" + ".".join(map(str, octets)) + "]"
        if check(mailbox):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()