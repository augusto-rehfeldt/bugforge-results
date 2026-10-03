import configparser
import io
import random
import string
import time


def reference(name):
    # Default comment prefixes are '#' and ';'. An option line beginning
    # with either is a comment, so reading it back omits the option.
    return {
        "must_raise_InvalidWriteError": name.startswith(("#", ";")),
        "original_items": [(name.lower(), "v")],
        "readback_items": [] if name.startswith(("#", ";")) else [(name.lower(), "v")],
    }


def observe(name):
    parser = configparser.RawConfigParser()
    parser.add_section("s")
    parser.set("s", name, "v")
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        return {
            "status": "raised",
            "exception": type(exc).__name__,
            "is_InvalidWriteError": (
                getattr(configparser, "InvalidWriteError", None) is not None
                and isinstance(exc, configparser.InvalidWriteError)
            ),
        }

    text = output.getvalue()
    fresh = configparser.RawConfigParser()
    try:
        fresh.read_string(text)
        items = list(fresh.items("s", raw=True))
    except Exception as exc:
        return {
            "status": "readback_error",
            "output": text,
            "exception": type(exc).__name__,
        }
    return {"status": "written", "output": text, "readback_items": items}


def violates(actual, expected):
    return expected["must_raise_InvalidWriteError"] and not (
        actual["status"] == "raised" and actual["is_InvalidWriteError"]
    )


def main():
    deadline = time.monotonic() + 175
    for name in ("alpha", "MixedCase"):
        expected = reference(name)
        actual = observe(name)
        agrees = (
            actual["status"] == "written"
            and actual["readback_items"] == expected["readback_items"]
        )
        print("SANITY:", repr(name), "PASS" if agrees else "FAIL")
        if not agrees:
            print("SANITY FAILED")
            return

    rng = random.Random(20260719)
    edges = [
        "#a", ";a", "#A", ";A", "#abc", ";abc",
        "#MixedCase", ";MixedCase", "#" + "a" * 4096, ";" + "Z" * 4096,
    ]
    tested = 0
    index = 0
    while time.monotonic() < deadline:
        if index < len(edges):
            name = edges[index]
            index += 1
        else:
            length = rng.choice((1, 2, 3, 8, 32, 128, 1024))
            name = rng.choice("#;") + "".join(
                rng.choice(string.ascii_letters) for _ in range(length)
            )
        expected = reference(name)
        actual = observe(name)
        tested += 1
        if violates(actual, expected):
            confirmation = observe(name)
            if confirmation == actual and violates(confirmation, expected):
                print("COUNTEREXAMPLE:")
                print(repr(name))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()