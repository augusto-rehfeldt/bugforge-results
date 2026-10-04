from markupsafe import EscapeFormatter, escape

class X:
    def __html__(self):
        return "<b>x</b>"

x = X()
expected = x.__html__()  # Documented trusted HTML, independently of escape.
if type(expected) is not str:
    print("REFUTATION REJECTED: __html__ did not return a plain str")
else:
    actual = EscapeFormatter(escape).format_field(x, "")
    if actual != expected:
        print(f"REFUTATION CONFIRMED: input={expected!r} actual={actual!r} expected={expected!r}")
    else:
        print("REFUTATION REJECTED: trusted HTML was preserved")