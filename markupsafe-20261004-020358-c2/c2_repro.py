import html
import markupsafe

c, r = "a", "&"
table = {ord(c): r}
if not (len(c) == 1 and c.isascii() and c.isalpha() and type(r) is str):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        actual = markupsafe.Markup(c).translate(table)
        expected = html.escape(r, quote=True).replace("&#x27;", "&#39;")
        if actual != expected or not isinstance(actual, markupsafe.Markup):
            print(f"REFUTATION CONFIRMED: input={(c, table)!r}, actual={actual!r}, expected={expected!r}")
        else:
            print("REFUTATION REJECTED: documented escaping and return type hold")
    except Exception as e:
        print(f"REFUTATION REJECTED: could not reproduce: {e}")