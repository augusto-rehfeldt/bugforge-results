import difflib

s = "a" * 999
expected = "HTML table string (no exception)"
if not (s and s.isascii() and s.isalpha()):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        result = difflib.HtmlDiff(wrapcolumn=1).make_table([s], [s])
        valid = isinstance(result, str) and "<table" in result and "</table>" in result
        actual = expected if valid else repr(result)
    except Exception as e:
        valid = False
        actual = f"{type(e).__name__}: {e}"
    if valid:
        print("REFUTATION REJECTED: documented HTML table returned")
    else:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)