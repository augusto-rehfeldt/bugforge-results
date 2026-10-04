import re
import sys
import email.headerregistry as hr

limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
value = "1" * (limit + 1 if limit else 4301) + ".0"
expected = "constructed without exception" if re.fullmatch(r"[0-9]+\.[0-9]+", value) else None

if expected is None:
    print("REFUTATION REJECTED: input does not match the documented grammar")
else:
    try:
        hr.HeaderRegistry()("MIME-Version", value)
    except Exception as e:
        print(f"REFUTATION CONFIRMED: input={value!r}\nactual: {type(e).__name__}: {e}\nexpected: {expected}")
    else:
        print("REFUTATION REJECTED: constructed without exception")