import textwrap

case = dict(width=1, text="a", initial_indent=" ", subsequent_indent="")
w, text = case["width"], case["text"]
valid = (
    type(w) is int and w > 0
    and isinstance(text, str)
    and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in text)
    and all(isinstance(case[k], str) and not case[k].strip(" ")
            for k in ("initial_indent", "subsequent_indent"))
)
if not valid:
    print("REFUTATION REJECTED:", "input is outside the documented domain")
else:
    wrapper = textwrap.TextWrapper(
        width=w, initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"], break_long_words=True)
    actual = wrapper.wrap(text)
    expected = f"Every returned line has length <= {w}"
    if any(len(line) > w for line in actual):
        print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "all returned lines satisfy", expected)