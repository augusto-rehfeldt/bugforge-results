from sortedcontainers import SortedDict

case = {'initial_keys': [0], 'absent_key': 1, 'value': 'value'}
failing = False

def key(k):
    if failing and k == case['absent_key']:
        raise RuntimeError('key evaluation failed')
    return k

d = SortedDict(key, {k: None for k in case['initial_keys']})
if (not all(type(k) is int for k in case['initial_keys'] + [case['absent_key']])
        or case['absent_key'] in d
        or list(d.keys()) != sorted(dict.keys(d), key=key)):
    print('REFUTATION REJECTED: invalid input or initial ordering')
else:
    failing = True
    raised = False
    try:
        d.setdefault(case['absent_key'], case['value'])
    except RuntimeError:
        raised = True
    finally:
        failing = False
    actual = list(d.keys())
    expected = sorted(dict.keys(d), key=key)
    if raised and actual != expected:
        print('REFUTATION CONFIRMED:', case, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'no key-function exception' if not raised
              else 'dictionary and sorted keys remain consistent')