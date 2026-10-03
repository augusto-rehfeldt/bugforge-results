import csv
import io

s = "name,age\r1,2\r3,4\r"
try:
    rows = list(csv.reader(io.StringIO(s, newline=""), delimiter=",", strict=True))
    valid = rows == [["name", "age"], ["1", "2"], ["3", "4"]]
except csv.Error:
    valid = False

if not valid:
    print("REFUTATION REJECTED:", "input failed independent CSV validation")
else:
    expected = bool
    try:
        value = csv.Sniffer().has_header(s)
        actual = ("result", value)
        broken = type(value) is not expected
    except csv.Error as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = False
    if broken:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no violation of the claimed bool/csv.Error property;", actual)