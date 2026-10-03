import configparser
import random
import time


def evaluate(section, b, v):
    parser = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation()
    )
    parser.read_dict({section: {"x": "${y}", "y": "${z}", "z": b}})
    try:
        return ("result", parser.get(section, "x", vars={"z": v}))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def reference(b, v):
    # With no dollar signs in either literal, the documented override
    # makes z equal to v throughout the x -> y -> z substitution chain.
    return v


def main():
    start = time.monotonic()
    deadline = start + 175.0

    # Ordinary inputs where the override and stored value agree.
    for section, literal in [("ordinary", "hello"), ("unicode", "世界")]:
        actual = evaluate(section, literal, literal)
        expected = ("result", reference(literal, literal))
        print("SANITY:", repr((section, literal)), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(section, b, v):
        nonlocal tested
        case = {"section": section, "b": b, "v": v, "vars": {"z": v}}
        expected = ("result", reference(b, v))
        actual = evaluate(section, b, v)
        tested += 1
        if actual != expected:
            repeated = evaluate(section, b, v)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(case),
                      "actual =", repr(actual),
                      "expected =", repr(expected))
                return True
        return False

    edges = [
        ("s", "original", "override"),
        ("s", "", "override"),
        ("s", "original", ""),
        ("s", "", ""),
        ("節", "雪", "火"),
        (" section ", " \t\n", "\n\t "),
        ("DEFAULT ordinary", "a", "b"),
        ("s", "${".replace("$", ""), "}\n:="),
        ("s", "\x00", "\x00different"),
        ("s", "é", "e\u0301"),
    ]
    for case in edges:
        if check(*case):
            return

    rng = random.Random(1729)
    alphabet = "abcXYZ019 \t\n\r:=[]{}#;%éΩ雪🙂\x00"

    def literal(max_length):
        return "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(max_length + 1))
        )

    while time.monotonic() < deadline:
        section = "section_" + literal(20)
        b = literal(80)
        v = literal(80)
        if rng.randrange(4) == 0:
            v = b + "distinct"
        if check(section, b, v):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()