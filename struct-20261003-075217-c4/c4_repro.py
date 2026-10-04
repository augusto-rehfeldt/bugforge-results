import struct

b = b'\x00'
try:
    S = struct.Struct('B')
    size = S.size
    if not size or not b or len(b) % size:
        print('REFUTATION REJECTED: invalid buffer or chunk size')
    else:
        limit = len(b) // size + 1
        expected = {'terminated': True, 'within_calls': limit}
        it = S.iter_unpack(b)
        S.__init__('0s')
        yielded = []
        terminated = False
        for calls in range(1, limit + 1):
            try:
                yielded.append(next(it))
            except StopIteration:
                terminated = True
                break
        actual = dict(terminated=terminated, calls=calls, yielded=yielded)
        if not terminated:
            print('REFUTATION CONFIRMED:', repr(b), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED: iterator terminated within', limit, 'calls')
except Exception as e:
    print('REFUTATION REJECTED:', type(e).__name__, str(e))