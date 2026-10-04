import random
import time
from urllib.parse import unquote_to_bytes
from yarl import URL


def reference(query, removed):
    result = {}
    for field in query.split("&"):
        key, value = field.split("=", 1)
        if key != removed:
            result[key] = unquote_to_bytes(value)
    return result


def evaluate(url_text, removed):
    query = url_text.split("?", 1)[1]
    expected = reference(query, removed)
    try:
        result = URL(url_text, encoded=True).without_query_params(removed)
        actual = {}
        if result.raw_query_string:
            for field in result.raw_query_string.split("&"):
                key, separator, value = field.partition("=")
                actual[key] = unquote_to_bytes(value)
        return actual, expected
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc)), expected


def main():
    for query in (
        "keep=%41%42%43&drop=%31",
        "first=%00%7F&drop=%32&second=%C3%A9",
    ):
        text = "https://example.com/?" + query
        actual, expected = evaluate(text, "drop")
        print("SANITY:", repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    deadline = started + 175
    rng = random.Random(735192)
    tested = 0
    edges = [
        b"\xff",
        b"\x80",
        b"\xc2",
        b"\xe2\x82",
        b"\xf0\x9f\x92",
        b"\xfe\xff",
        b"\xc0\xaf",
        b"\xed\xa0\x80",
        b"\xf4\x90\x80\x80",
        bytes(range(256)),
        b"\x00&=+%#?\xff",
        b"valid\xc3\xa9",
    ]

    def encode(value):
        return "".join("%%%02X" % octet for octet in value)

    def check(query):
        nonlocal tested
        text = "https://example.com/?" + query
        actual, expected = evaluate(text, "drop")
        tested += 1
        if actual != expected:
            repeated_actual, repeated_expected = evaluate(text, "drop")
            if repeated_actual == actual and repeated_expected == expected:
                print("COUNTEREXAMPLE:")
                print(repr((text, "drop")))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    for value in edges:
        for query in (
            "keep=" + encode(value) + "&drop=1",
            "drop=1&keep=" + encode(value),
            "first=%41&keep=" + encode(value) + "&drop=1&last=%00",
        ):
            if check(query):
                return

    while time.monotonic() < deadline:
        fields = []
        for index in range(rng.randint(1, 5)):
            value = bytes(rng.randrange(256) for _ in range(rng.randint(1, 64)))
            fields.append("keep%d=%s" % (index, encode(value)))
        fields.insert(rng.randrange(len(fields) + 1), "drop=%31")
        if check("&".join(fields)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()