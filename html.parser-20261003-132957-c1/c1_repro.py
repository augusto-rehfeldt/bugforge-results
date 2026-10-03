import html.parser
import re
import sys

if not hasattr(sys, "set_int_max_str_digits"):
    print("REFUTATION REJECTED: integer-string conversion limit unavailable")
else:
    sys.set_int_max_str_digits(4300)
    text = '<div title="&#' + '0' * 4300 + '65;">'
    match = re.fullmatch(r'<div title="&#([0-9]+);">', text)
    if not match or match[1].lstrip("0") != "65":
        print("REFUTATION REJECTED: input is not a valid decimal reference to U+0041")
    else:
        expected = ("OK", [("div", [("title", chr(65))])])
        events = []

        class Parser(html.parser.HTMLParser):
            def handle_starttag(self, tag, attrs):
                events.append((tag, attrs))

        try:
            Parser(convert_charrefs=True).feed(text)
            actual = ("OK", events)
        except Exception as e:
            actual = ("EXCEPTION", type(e).__name__, str(e))

        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(text),
                  "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: actual matches documented expectation")