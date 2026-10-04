import tabulate

case = dict(rows=[["abc"]], tablefmt="asciidoc",
            disable_numparse=True, stralign=None)
rows = case["rows"]
valid = bool(rows) and bool(rows[0]) and all(
    len(row) == len(rows[0]) and all(
        isinstance(cell, str) and bool(cell) and cell.isascii()
        for cell in row
    ) for row in rows
)
# Documented alignment disabling applies to these text-only cells.
expected = "a table string without raising an exception" if valid else None

if not valid:
    print("REFUTATION REJECTED:", "invalid input")
else:
    try:
        result = tabulate.tabulate(
            rows, **{k: v for k, v in case.items() if k != "rows"}
        )
        actual = ("result", result)
        broken = not isinstance(result, str)
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", case, "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "returned a table string", actual)