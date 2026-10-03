import configparser as c
import io

inp = {"section": "s", "option": "#a", "value": "v"}
try:
    # Documented API: string section/option/value; no forbidden option names.
    p = c.RawConfigParser()
    p.add_section(inp["section"])
    p.set(inp["section"], inp["option"], inp["value"])
    original = p.items("s", raw=True)
    if original != [("#a", "v")]:
        raise ValueError("input was not stored as reported")

    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        if isinstance(e, getattr(c, "InvalidWriteError", ())):
            print("REFUTATION REJECTED:", "write raised InvalidWriteError")
        else:
            print("REFUTATION REJECTED:", repr(e))
    else:
        q = c.RawConfigParser()
        q.read_string(out.getvalue())
        readback = q.items("s", raw=True) if q.has_section("s") else []
        actual = {
            "status": "written",
            "output": out.getvalue(),
            "readback_items": readback,
        }
        expected = {
            "must_raise_InvalidWriteError": readback != original,
            "original_items": original,
            "readback_items": readback,
        }
        if expected["must_raise_InvalidWriteError"]:
            print("REFUTATION CONFIRMED:", inp, actual, expected)
        else:
            print("REFUTATION REJECTED:", "output preserves the input", actual)
except Exception as e:
    print("REFUTATION REJECTED:", "validation/readback failed:", repr(e))