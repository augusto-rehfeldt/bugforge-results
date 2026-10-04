import configparser as c
import io

data = {"L": " ", "R": ""}
value = data["L"] + "value" + data["R"]
p = c.RawConfigParser()
try:
    # Documented inputs: a non-DEFAULT section and string option/value.
    p.add_section("s")
    p.set("s", "key", value)
    if p.get("s", "key") != value:
        print("REFUTATION REJECTED:", "input was not stored unchanged")
    else:
        out = io.StringIO()
        try:
            p.write(out)
        except getattr(c, "InvalidWriteError", ()):
            print("REFUTATION REJECTED:", "InvalidWriteError raised as permitted")
        else:
            q = c.RawConfigParser()
            try:
                q.read_string(out.getvalue())
                actual = q.get("s", "key")
            except c.Error as e:
                actual = (type(e).__name__, str(e))
            if actual != value:
                print("REFUTATION CONFIRMED:", data,
                      "actual:", (actual, out.getvalue()),
                      "expected:", (value, "or InvalidWriteError"))
            else:
                print("REFUTATION REJECTED:", "exact value preserved")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))