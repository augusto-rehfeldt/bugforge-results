import math
import random
import statistics
import time

TOL = 1e-15


def reference_cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def main():
    for z in (0.0, 2.0):
        expected = reference_cdf(z)
        actual = statistics.NormalDist(0.0, 1.0).cdf(z)
        print("SANITY:", repr(z), "actual:", repr(actual),
              "expected:", repr(expected))
        if not math.isfinite(actual) or abs(actual - expected) > TOL:
            print("SANITY FAILED")
            return

    expected = reference_cdf(2.0)
    deadline = time.monotonic() + 175.0
    tested = 0

    def evaluate(a):
        try:
            return statistics.NormalDist(-a, a).cdf(a)
        except Exception as exc:
            return exc

    def fails(result):
        return (
            isinstance(result, Exception)
            or not math.isfinite(result)
            or abs(result - expected) > TOL
        )

    def check(a):
        nonlocal tested
        assert math.isfinite(a) and 0.0 < a <= 1.2e308
        tested += 1
        actual = evaluate(a)
        if fails(actual):
            repeated = evaluate(a)
            if fails(repeated):
                displayed = (
                    repr(repeated)
                    if isinstance(repeated, Exception)
                    else repeated
                )
                print("COUNTEREXAMPLE:", repr(a),
                      "actual:", displayed, "expected:", repr(expected))
                return True
        return False

    boundary = float.fromhex("0x1.fffffffffffffp+1022")
    edges = [
        1e308,
        9e307,
        1.2e308,
        math.nextafter(1e308, 0.0),
        math.nextafter(1e308, math.inf),
        boundary,
        math.nextafter(boundary, 0.0),
        math.nextafter(boundary, math.inf),
        1.0,
        1e-300,
        math.ulp(0.0),
    ]

    for a in edges:
        if check(a):
            return

    rng = random.Random(20260719)
    while time.monotonic() < deadline:
        if rng.randrange(4):
            a = 9e307 + rng.random() * 3e307
        else:
            a = math.ldexp(1.0 + rng.random(), rng.randint(-1074, 1023))
            if not math.isfinite(a) or not 0.0 < a <= 1.2e308:
                continue
        if check(a):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()