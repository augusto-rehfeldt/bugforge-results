*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `struct`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Reentrant buffer acquisition must not bypass the zero-size iterator check

Target: `struct.Struct.iter_unpack`

Property: For a Struct S initially equal to Struct('B'), let exporter be a Python buffer exporter whose __buffer__ method calls S.__init__('0s') and returns memoryview(b''). S.iter_unpack(exporter) must raise struct.error for the resulting zero-sized format, rather than performing division by zero or crashing.

### Draft issue: struct.Struct.iter_unpack crashes when __buffer__ reinitializes the Struct to a zero-sized format

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

**Documented behaviour:** The struct documentation, under struct.iter_unpack, states: “The buffer’s size in bytes must be a multiple of the size required by the format.” A zero-sized format cannot define the fixed-size chunks described there: “This function returns an iterator which will read equally-sized chunks from the buffer until all its contents have been consumed.”

**Expected:** Raise struct.error after detecting the zero-sized format, without crashing.

**Actual:** The subprocess exits with status 3221225620 (0xC0000094, integer division by zero).

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'initial': 'B', 'replacement': '0s', 'buffer': b'', 'token': None} actual = ('process exited', 3221225620) expected = raises struct.error
```

Judge: BUG (high) -- The valid Python buffer exporter reinitializes the Struct during buffer acquisition, exposing a reentrancy hole in size validation. The process exits with Windows status 0xC0000094 (integer division by zero), rather than raising a Python exception. Even though the quoted documentation does not explicitly specify zero-size exception handling, this callback must not cause an interpreter crash. None of the listed issues addresses this behaviour.

