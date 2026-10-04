import configparser as c
import io

data = {"W": " ", "K": "a", "option": " a", "value": "value"}
p = c.RawConfigParser()
try:
    p.add_section("s")
    p.set("s", data["option"], data["value"])
    if tuple(p.options("s")) != (data["option"],):
        raise ValueError("reported option was not stored unchanged")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    # Independently check how the default serialization would be read.
    reference = c.RawConfigParser()
    reference.read_string("[s]\n a = value\n\n")
    expected = ("raised", "InvalidWriteError") if tuple(reference.options("s")) != tuple(p.options("s")) else ("write succeeded",)
    out = io.StringIO()
    try:
        p.write(out)
        reread = c.RawConfigParser()
        reread.read_string(out.getvalue())
        actual = ("write succeeded", tuple(reread.options("s")), out.getvalue())
    except Exception as e:
        actual = ("raised", type(e).__name__)
    if expected == ("raised", "InvalidWriteError") and actual[0] == "write succeeded" and actual[1] != tuple(p.options("s")):
        print("REFUTATION CONFIRMED:", data, "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED:", "no demonstrated promise violation", data, "actual=", actual, "expected=", expected)