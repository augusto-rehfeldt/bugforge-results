import random
import shlex
import string
import time


def reference(P):
    # A nonempty ASCII-letter word followed by whitespace is one token.
    return [P]


def check(P, C):
    try:
        lexer = shlex.shlex(P + " ", posix=True, punctuation_chars=";")
        lexer.push_source(C + ";tail")
        first = lexer.get_token()
        if first != C:
            return ("unexpected child token", first)
        lexer.pop_source()
        return list(lexer)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    for word in ("a", "OrdinaryWord"):
        expected = reference(word)
        actual = list(shlex.shlex(
            word + " ", posix=True, punctuation_chars=";"
        ))
        print("SANITY:", repr(word), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    rng = random.Random(20260301)
    letters = string.ascii_letters
    edges = [
        ("a", "b"),
        ("A", "Z"),
        ("hello", "child"),
        ("a", "C" * 4096),
        ("P" * 4096, "c"),
        ("Ab" * 4096, "Cd" * 4096),
    ]
    tested = 0

    while time.monotonic() < deadline:
        if tested < len(edges):
            P, C = edges[tested]
        else:
            lengths = (1, 2, 3, 16, 127, 1024, 4096)
            P = "".join(rng.choices(letters, k=rng.choice(lengths)))
            C = "".join(rng.choices(letters, k=rng.choice(lengths)))

        expected = reference(P)
        actual = check(P, C)
        tested += 1

        if actual != expected:
            repeated = check(P, C)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr((P, C)),
                      "actual:", repr(actual), "expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()