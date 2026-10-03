import textwrap

case = dict(width=1, initial_indent=" ", subsequent_indent="", text="a")
text = case["text"]
if not (type(case["width"]) is int and case["width"] > 0
        and text and text.isascii() and text.isalpha()
        and all(isinstance(case[k], str) for k in ("initial_indent", "subsequent_indent"))):
    print("REFUTATION REJECTED:", "invalid input")
else:
    # The documentation places no upper bound on indent length.
    wrapper = textwrap.TextWrapper(
        width=case["width"], initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"], break_long_words=True)
    actual = wrapper.fill(text)
    expected = {"every_line_length_at_most": case["width"]}
    if any(len(line) > case["width"] for line in actual.split("\n")):
        print("REFUTATION CONFIRMED:", case, "actual:", repr(actual), "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "every line fits the documented width")