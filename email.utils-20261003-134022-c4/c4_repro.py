import email.utils
import re

mailbox = "alice@" + "[127.0.0.1]"
m = re.fullmatch(r"[A-Za-z]+(?:\.[A-Za-z]+)*@\[(\d+\.\d+\.\d+\.\d+)\]", mailbox, re.ASCII)
if not m or not all(0 <= int(n) <= 255 for n in m[1].split(".")):
    print("REFUTATION REJECTED:", "input is not the claimed RFC 2822 mailbox")
else:
    expected = [("", mailbox)]
    try:
        actual = email.utils.getaddresses([mailbox], strict=True)
    except Exception as exc:
        print("REFUTATION REJECTED:", "call did not return:", repr(exc))
    else:
        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(mailbox), "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED:", "actual matches documented expectation")