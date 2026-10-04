from dateutil.relativedelta import relativedelta, TU

offsets = {}
w = TU(1)
data = {"offsets": offsets, "left_weekday": ("TU", TU.n),
        "right_weekday": ("TU", w.n)}
if TU.weekday != 1 or TU.n is not None or w.weekday != 1 or w.n != 1:
    print("REFUTATION REJECTED: input is not the documented Tuesday/default/+1 case")
else:
    a = relativedelta(weekday=TU, **offsets)
    b = relativedelta(weekday=w, **offsets)
    actual = (a == b, hash(a) == hash(b))
    # Empty offsets are valid; documented default +1 makes both specifications
    # equivalent, and equal hashable objects must have equal hashes.
    expected = (True, True)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: equality and hashes match the documented expectation")