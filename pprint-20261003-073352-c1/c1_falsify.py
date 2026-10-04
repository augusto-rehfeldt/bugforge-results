import pprint
import random
import time


class Key(list):
    __hash__ = object.__hash__


def reference(obj, active=None):
    """Independent recursion-aware representation; never compares list keys."""
    if active is None:
        active = set()

    if isinstance(obj, (dict, list, tuple)):
        oid = id(obj)
        if oid in active:
            return "<Recursion on {} with id={}>".format(type(obj).__name__, oid)

        active.add(oid)
        try:
            if isinstance(obj, dict):
                items = list(obj.items())
                if all(type(k) is int for k, _ in items):
                    items.sort(key=lambda item: item[0])
                return "{" + ", ".join(
                    reference(k, active) + ": " + reference(v, active)
                    for k, v in items
                ) + "}"

            parts = [reference(value, active) for value in obj]
            if isinstance(obj, list):
                return "[" + ", ".join(parts) + "]"
            return "(" + ", ".join(parts) + ("," if len(parts) == 1 else "") + ")"
        finally:
            active.remove(oid)

    return repr(obj)


def make_input(depths):
    result = {}
    for index, depth in enumerate(depths, 1):
        key = Key()
        current = key
        for _ in range(depth):
            child = []
            current.append(child)
            current = child
        current.append(key)
        result[key] = index
    return result


def actual_result(obj):
    try:
        result = pprint.saferepr(obj)
        return isinstance(result, str), result
    except Exception as exc:
        return False, "{}: {}".format(type(exc).__name__, exc)


def main():
    for ordinary in ([1, [2, 3]], {2: (4,), 1: [3]}):
        expected = reference(ordinary)
        actual = pprint.saferepr(ordinary)
        print("SANITY:", repr(ordinary), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    rng = random.Random(20260710)
    tested = 0
    handpicked = [
        [0],
        [0, 0],
        [1, 1],
        [2, 2],
        [0, 1],
        [1, 0],
        [0, 0, 0],
        [5, 5],
        [20, 20],
    ]

    while time.monotonic() - start < 175:
        if handpicked:
            depths = handpicked.pop(0)
        else:
            count = rng.randint(1, 12)
            if rng.randrange(2):
                depths = [rng.randint(0, 25)] * count
            else:
                depths = [rng.randint(0, 25) for _ in range(count)]

        obj = make_input(depths)
        expected = reference(obj)
        tested += 1
        passed, actual = actual_result(obj)

        if not passed:
            confirmed_passed, confirmed_actual = actual_result(obj)
            if confirmed_passed:
                continue
            print("COUNTEREXAMPLE:")
            print(repr(obj))
            print("actual:", repr(confirmed_actual))
            print("expected: a string without an exception;", repr(expected))
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()