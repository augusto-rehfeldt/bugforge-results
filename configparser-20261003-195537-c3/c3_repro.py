import configparser as c
import io

data = {"section": "s", "option": "key", "value": "a\n#b"}
p = c.RawConfigParser()
try:
    # Documented input types: string section, option and value.
    p.add_section(data["section"])
    p.set(data["section"], data["option"], data["value"])
except (TypeError, ValueError, c.Error) as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        print("REFUTATION REJECTED:", "write raised", type(e).__name__)
    else:
        text = out.getvalue()
        q = c.RawConfigParser()
        q.read_string(text)
        restored = q.get(data["section"], data["option"])
        actual = ("write succeeded", text, restored)
        # Independently test the documented round-trip promise.
        if restored != data["value"]:
            print("REFUTATION CONFIRMED:", data, "actual:", actual,
                  "expected:", ("exception", "InvalidWriteError"))
        else:
            print("REFUTATION REJECTED:", "round trip preserved the value")