import plistlib
from io import BytesIO
from collections import UserDict

data = {'a': 'b'}
try:
    if not data or not all(isinstance(k, str) and isinstance(v, str)
                           for k, v in data.items()):
        raise ValueError("input is not a nonempty string-to-string dictionary")
    xml = plistlib.dumps(data, fmt=plistlib.FMT_XML)
    if plistlib.load(BytesIO(xml)) != data:
        raise ValueError("XML does not represent the reported input")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    expected = UserDict(data)
    try:
        actual = plistlib.load(BytesIO(xml), dict_type=UserDict)
        broken = not isinstance(actual, UserDict) or actual != expected
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", "input:", data,
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED:", "returned the expected UserDict")