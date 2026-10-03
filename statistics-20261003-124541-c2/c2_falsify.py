import math
import random
import statistics
import time


def standard_quantile(p):
    # Invert Phi(z) = (1 + erf(z / sqrt(2))) / 2 independently.
    lo, hi = -12.0, 12.0
    target = 2.0 * p - 1.0
    for _ in range(100):
        mid = lo + (hi - lo) / 2.0
        if math.erf(mid / math.sqrt(2.0)) < target:
            lo = mid
        else:
            hi = mid
    return lo + (hi - lo) / 2.0


def evaluate(mu, sigma, p):
    try:
        return statistics.NormalDist(mu, sigma).inv_cdf(p)
    except Exception as exc:
        return "{}: {}".format(type(exc).__name__, exc)


def agrees(actual, expected):
    return (
        isinstance(actual, (int, float))
        and math.isfinite(actual)
        and math.isclose(actual, expected, rel_tol=1e-14, abs_tol=0.0)
    )


def main():
    p = 0.975
    z = standard_quantile(p)

    sanity_ok = True
    for mu, sigma in ((0.0, 1.0), (2.0, 3.0)):
        expected = mu + sigma * z
        actual = evaluate(mu, sigma, p)
        ok = agrees(actual, expected)
        print("SANITY:", repr((mu, sigma, p)),
              "actual =", repr(actual), "expected =", repr(expected),
              "PASS" if ok else "FAIL")
        sanity_ok = sanity_ok and ok

    if not sanity_ok:
        print("SANITY FAILED")
        return

    low, high = 9.5e307, 1e308
    edges = [
        low,
        high,
        math.nextafter(low, high),
        math.nextafter(high, low),
        low + (high - low) / 2.0,
    ]
    rng = random.Random(20250308)
    deadline = time.monotonic() + 175.0
    tested = 0

    def inputs():
        yield from edges
        while time.monotonic() < deadline:
            yield low + (high - low) * rng.random()

    for a in inputs():
        expected = a * (z - 1.0)
        actual = evaluate(-a, a, p)
        tested += 1
        if not agrees(actual, expected):
            repeated = evaluate(-a, a, p)
            if not agrees(repeated, expected):
                print("COUNTEREXAMPLE:",
                      repr({"a": a, "mu": -a, "sigma": a, "p": p}),
                      "actual =", repr(repeated),
                      "expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()