import email.utils
import re

field = "alice@example.com" + " (team, west)"
# This RFC 2822 subset has a dot-atom addr-spec and balanced ASCII comment.
m = re.fullmatch(r"([A-Za-z]+(?:\.[A-Za-z]+)*@[A-Za-z]+(?:\.[A-Za-z]+)+) \(([A-Za-z ,]*)\)", field)
if not m:
    print("REFUTATION REJECTED: input not independently validated")
else:
    expected = [(m[2], m[1])]
    try:
        actual = email.utils.getaddresses([field], strict=True)
    except Exception as e:
        print("REFUTATION REJECTED:", type(e).__name__, str(e))
    else:
        if len(actual) != 1 or actual[0][1] != m[1]:
            print("REFUTATION CONFIRMED:", repr(field), actual, expected)
        else:
            print("REFUTATION REJECTED: one address with the expected addr-spec")