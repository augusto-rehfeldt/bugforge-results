import heapq

class Item:
    def __init__(self, name, priority):
        self.name, self.priority = name, priority
    def __lt__(self, other):
        return self.priority < other.priority

data = [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 0)]
xs = [Item(*pair) for pair in data]
n = 4

if not (type(n) is int and 0 < n < len(xs)
        and all(type(x.priority) is int for x in xs)
        and all((x == y) == (x is y)
                and (x < y) == (x.priority < y.priority)
                for x in xs for y in xs)):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = heapq.nsmallest(n, xs)
    expected = sorted(xs)[:n]
    if len(actual) != len(expected) or any(
            a is not e for a, e in zip(actual, expected)):
        print("REFUTATION CONFIRMED:",
              {'n': n, 'xs': data},
              "actual:", [x.name for x in actual],
              "expected:", [x.name for x in expected])
    else:
        print("REFUTATION REJECTED: actual matches sorted(xs)[:n] by identity and order")