import string

class FalseySep(str):
    def __bool__(self):
        return False

s, sep = 'a|b', FalseySep('|')
if not (isinstance(s, str) and isinstance(sep, str) and len(sep) > 0):
    print('REFUTATION REJECTED:', 'invalid input')
else:
    actual = string.capwords(s, sep)
    expected = str.join(sep, map(str.capitalize, str.split(s, sep)))
    if actual != expected:
        print('REFUTATION CONFIRMED:', {'s': s, 'sep': sep, 'sep_class': type(sep).__name__},
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED:', 'actual matches documented expectation')