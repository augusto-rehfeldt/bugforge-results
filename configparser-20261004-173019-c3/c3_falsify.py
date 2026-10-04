import configparser
import io
import random
import string
import time


def reference_names(option):
    # Default option normalization is lowercase; parsing removes surrounding
    # ASCII whitespace from these restricted option names.
    stored = option.lower()
    return stored, stored.strip(" \t")


def observe(option):
    parser = configparser.RawConfigParser()
    parser.add_section("s")
    parser.set("s", option, "value")
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        return ("raised", type(exc).__name__)

    text = output.getvalue()
    fresh = configparser.RawConfigParser()
    try:
        fresh.read_string(text)
        names = tuple(fresh.options("s"))
    except Exception as exc:
        return ("write succeeded; read raised", type(exc).__name__, text)
    return ("write succeeded", names, text)


def main():
    started = time.monotonic()

    for option in ("alpha", "MiXeD"):
        stored, reread = reference_names(option)
        result = observe(option)
        agrees = (
            stored == reread
            and result[0] == "write succeeded"
            and result[1] == (reread,)
        )
        print("SANITY:", repr(option), "PASS" if agrees else "FAIL")
        if not agrees:
            print("SANITY FAILED")
            return

    expected = ("raised", "InvalidWriteError")
    tested = 0

    def check(w, k):
        nonlocal tested
        option = w + k
        stored, reread = reference_names(option)
        assert stored != reread
        result = observe(option)
        tested += 1
        if result != expected:
            repeated = observe(option)
            if repeated == result:
                case = {"W": w, "K": k, "option": option, "value": "value"}
                print(
                    "COUNTEREXAMPLE:",
                    repr(case),
                    "actual=" + repr(result),
                    "expected=" + repr(expected),
                )
                return True
        return False

    whitespace_cases = (
        " ", "\t", "  ", " \t", "\t ", "\t\t",
        " \t ", "\t \t", " " * 64, "\t" * 64,
    )
    letter_cases = ("a", "A", "Z", "abc", "MiXeD", string.ascii_letters)

    for w in whitespace_cases:
        for k in letter_cases:
            if check(w, k):
                return

    rng = random.Random(20260417)
    while tested < 200000 and time.monotonic() - started < 170:
        w = "".join(rng.choice(" \t") for _ in range(rng.randint(1, 128)))
        k = "".join(
            rng.choice(string.ascii_letters) for _ in range(rng.randint(1, 128))
        )
        if check(w, k):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()