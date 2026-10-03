import configparser as c
import io

a, b = "a", "b"
value = a + " # " + b
expected = ("InvalidWriteError or exact readback", value)

try:
    if not all(x and x.isascii() and x.isalpha() for x in (a, b)):
        raise ValueError("input is outside the claimed domain")
    p = c.RawConfigParser(inline_comment_prefixes=("#",))
    p.add_section("s")
    p.set("s", "key", value)  # Valid string section, option and raw value.
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        if isinstance(e, getattr(c, "InvalidWriteError", ())):
            print("REFUTATION REJECTED:", "write raised InvalidWriteError")
        else:
            print("REFUTATION REJECTED:", "unexpected write failure:", repr(e))
    else:
        q = c.RawConfigParser(inline_comment_prefixes=("#",))
        try:
            q.read_string(out.getvalue())
            actual = ("readback", q.get("s", "key", raw=True))
        except Exception as e:
            actual = ("read error", repr(e))
        if actual == ("readback", value):
            print("REFUTATION REJECTED:", "exact readback")
        else:
            print("REFUTATION CONFIRMED:", (a, b),
                  "actual:", actual, "expected:", expected)