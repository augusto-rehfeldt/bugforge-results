try:
    import markupsafe as m

    spec, html = "link", "<em>hello</em>"

    class X:
        def __html_format__(self, spec):
            if spec != "link":
                raise ValueError("unsupported spec")
            return html

    x = X()
    expected = x.__html_format__(spec)
    if not spec or hasattr(x, "__html__") or type(expected) is not str or expected != html:
        print("REFUTATION REJECTED: invalid input")
    else:
        actual = m.EscapeFormatter(m.escape).format_field(x, spec)
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"spec": spec, "html": html},
                  "actual:", repr(actual), "expected:", repr(expected))
        else:
            print("REFUTATION REJECTED: actual matches documented expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))