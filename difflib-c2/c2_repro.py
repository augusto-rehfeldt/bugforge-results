import difflib

class Predicate:
    def __call__(self, line):
        return line == "A\n"

    def __bool__(self):
        return False

a, b, p = ["A\n", "B\n"], ["B\n", "A\n"], Predicate()
data = {"a": a, "b": b,
        "p": {"junk_membership": ["A\n"], "__bool__": False}}

if not (callable(p) and all(
    isinstance(s, str) and type(p(s)) is bool and p(s) == p(s)
    for s in a + b
)):
    print("REFUTATION REJECTED: input violates the documented predicate contract")
else:
    actual = list(difflib.ndiff(a, b, linejunk=p))
    # Independent alignment: B is the sole nonjunk anchor; A moves past it.
    expected = ["- " + a[0], "  " + a[1], "+ " + b[1]]
    wrapped = list(difflib.ndiff(a, b, linejunk=lambda s: p(s)))
    if actual != expected and wrapped == expected:
        print("REFUTATION CONFIRMED:", data,
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: no independently verified wrapper discrepancy",
              data, "actual:", actual, "expected:", expected, "wrapped:", wrapped)