import configparser as c
import io

a, b = "a", "b"
value = a + "\n\n" + b
p = c.RawConfigParser(empty_lines_in_values=False)
p.add_section("s")
try:
    if not all(x and x.isascii() and x.isalpha() for x in (a, b)):
        raise ValueError("invalid claimed input")
    p.set("s", "key", value)  # RawConfigParser accepts string values.
    if p.get("s", "key") != value:
        raise ValueError("input was not stored unchanged")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        print("REFUTATION REJECTED:", "write raised", type(e).__name__, str(e))
    else:
        text = out.getvalue()
        q = c.RawConfigParser(empty_lines_in_values=False)
        try:
            q.read_string(text)
            recovered = q.get("s", "key")
            accurate = recovered == value
            actual = ("write succeeded; roundtrip", recovered, text)
        except Exception as e:
            accurate = False
            actual = ("write succeeded; read raised", type(e).__name__, str(e), text)
        if accurate:
            print("REFUTATION REJECTED:", "output accurately round-trips", repr(value))
        else:
            print("REFUTATION CONFIRMED:", (a, b), "actual:", actual,
                  "expected:", ("write raised", "InvalidWriteError"))