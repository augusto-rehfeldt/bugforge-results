import struct, subprocess, sys

case = {'initial': 'B', 'replacement': '0s', 'buffer': b'', 'token': None}
if sys.version_info < (3, 12):
    print('REFUTATION REJECTED:', 'Python 3.12+ is required for __buffer__')
else:
    size = struct.calcsize(case['initial'])
    valid = size > 0 and len(case['buffer']) % size == 0
    expected = 'raises struct.error' if struct.calcsize(case['replacement']) == 0 else None
    if not valid or expected is None:
        print('REFUTATION REJECTED:', 'input or zero-sized-format premise is invalid')
    else:
        code = """
import struct
S = struct.Struct('B')
class Exporter:
    def __buffer__(self, flags):
        S.__init__('0s')
        return memoryview(b'')
try:
    S.iter_unpack(Exporter())
except struct.error:
    print('raises struct.error')
except BaseException as e:
    print(type(e).__name__, str(e))
else:
    print('returned iterator')
"""
        p = subprocess.run([sys.executable, '-I', '-c', code],
                           capture_output=True, text=True)
        actual = p.stdout.strip() if p.returncode == 0 else ('process exited', p.returncode)
        if actual != expected:
            print('REFUTATION CONFIRMED:', case, 'actual =', actual, 'expected =', expected)
        else:
            print('REFUTATION REJECTED:', 'the call raised struct.error as expected')