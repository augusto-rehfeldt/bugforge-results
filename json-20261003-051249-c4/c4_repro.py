import json, math, re

class FalseBool:
    def __init__(self):
        self.calls = []
    def __bool__(self):
        return False
    def __call__(self, text):
        self.calls.append(text)
        return "<sentinel>"

document, hook = "1.5", FalseBool()
if not (re.fullmatch(r"-?(?:0|[1-9][0-9]*)\.[0-9]+", document)
        and math.isfinite(float(document)) and callable(hook) and not bool(hook)):
    print("REFUTATION REJECTED:", "invalid input or hook")
else:
    expected = {"result": "<sentinel>", "calls": [document]}
    try:
        result = json.loads(document, parse_float=hook)
        actual = {"result": result, "calls": hook.calls}
    except Exception as error:
        actual = {"exception": repr(error), "calls": hook.calls}
    if actual != expected:
        print("REFUTATION CONFIRMED:",
              {"document": document, "parse_float": "FalseBool"},
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")