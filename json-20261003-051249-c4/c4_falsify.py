import json
import random
import re
import time

TOKEN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)")
WHITESPACE = " \t\r\n"


class Sentinel:
    def __repr__(self):
        return "<sentinel>"


class Callback:
    def __init__(self):
        self.calls = []
        self.sentinel = Sentinel()

    def __call__(self, text):
        self.calls.append(text)
        return self.sentinel


class FalseBool(Callback):
    def __bool__(self):
        return False


class ZeroLen(Callback):
    def __len__(self):
        return 0


def reference(document):
    token = document.strip(WHITESPACE)
    if TOKEN.fullmatch(token) is None:
        raise AssertionError("Generator produced an invalid floating-point document")
    return {"result": "<sentinel>", "calls": [token]}


def observe(document, callback_type):
    callback = callback_type()
    try:
        result = json.loads(document, parse_float=callback)
        description = (
            "<sentinel>" if result is callback.sentinel
            else type(result).__name__ + ": " + repr(result)
        )
        return {"result": description, "calls": callback.calls}
    except Exception as exc:
        return {
            "exception": type(exc).__name__ + ": " + str(exc),
            "calls": callback.calls,
        }


def main():
    started = time.monotonic()
    for document in ("1.5", " \t-2E-10\r\n"):
        expected = reference(document)
        actual = observe(document, Callback)
        print("SANITY:", repr(document), "actual:", actual, "expected:", expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(document, callback_type):
        nonlocal tested
        expected = reference(document)
        actual = observe(document, callback_type)
        tested += 1
        if actual != expected:
            repeated = observe(document, callback_type)
            if repeated != expected:
                failing_input = {
                    "document": document,
                    "parse_float": callback_type.__name__,
                }
                print(
                    "COUNTEREXAMPLE:", repr(failing_input),
                    "actual:", repr(repeated),
                    "expected:", repr(expected),
                )
                return True
        return False

    edge_tokens = (
        "1.5", "-0.0", "1e0", "2E-10", "0.0", "0e0",
        "-0E+00", "1.00000000000000000001", "9e100", "1e-100",
    )
    padding = (("", ""), (" ", " "), ("\t\r\n", "\n\t "))
    for token in edge_tokens:
        for left, right in padding:
            for callback_type in (FalseBool, ZeroLen):
                if check(left + token + right, callback_type):
                    return

    rng = random.Random(731904)
    for _ in range(100000):
        if time.monotonic() - started >= 175:
            break
        integer = str(rng.randrange(10**18))
        token = ("-" if rng.randrange(2) else "") + integer
        if rng.randrange(2):
            token += "." + "".join(
                str(rng.randrange(10)) for _ in range(rng.randrange(1, 40))
            )
        else:
            token += rng.choice("eE")
            token += rng.choice(("", "+", "-"))
            token += "0" * rng.randrange(4) + str(rng.randrange(101))
        if "." in token and rng.randrange(2):
            token += rng.choice("eE") + rng.choice(("", "+", "-"))
            token += str(rng.randrange(101))
        left = "".join(rng.choice(WHITESPACE) for _ in range(rng.randrange(5)))
        right = "".join(rng.choice(WHITESPACE) for _ in range(rng.randrange(5)))
        if check(left + token + right, rng.choice((FalseBool, ZeroLen))):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()