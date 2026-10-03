import random
import time
from fractions import Fraction

DEADLINE = time.monotonic() + 170
BATCH_SIZE = 256
cases_tested = 0


def reference_mean(n, p):
    # Exact arithmetic on the supplied floating-point probability.
    numerator, denominator = p.as_integer_ratio()
    return n * Fraction(numerator, denominator)


def sample_batch(n, p, seeds):
    results = []
    for seed in seeds:
        try:
            results.append(random.Random(seed).binomialvariate(n, p))
        except Exception as exc:
            return {"exception": type(exc).__name__, "message": str(exc)}
    return results


def report(n, p, actual, expected):
    print("COUNTEREXAMPLE:", repr((n, p)),
          "actual =", repr(actual), "expected =", repr(expected))


def main():
    global cases_tested

    # Ordinary, nondegenerate inputs. These are statistical sanity checks,
    # with deliberately generous tolerances rather than exact sample equality.
    for n, p in ((10, 0.5), (20, 0.25)):
        expected = reference_mean(n, p)
        actual = sample_batch(n, p, range(4096))
        if isinstance(actual, dict):
            print("SANITY:", repr((n, p)), repr(actual),
                  "reference mean =", float(expected))
            print("SANITY FAILED")
            return
        observed = Fraction(sum(actual), len(actual))
        print("SANITY:", repr((n, p)), "observed mean =", float(observed),
              "reference mean =", float(expected))
        if (any(not isinstance(x, int) or not 0 <= x <= n for x in actual)
                or abs(observed - expected) > Fraction(1, 4)):
            print("SANITY FAILED")
            return

    chooser = random.Random(8675309)

    def check(j):
        global cases_tested
        n, p = 2 ** j, 2.0 ** (-j)
        expected = reference_mean(n, p)
        assert expected == 1

        seeds = [chooser.getrandbits(128) for _ in range(BATCH_SIZE)]
        actual = sample_batch(n, p, seeds)
        cases_tested += 1

        suspicious = isinstance(actual, dict) or all(x == 0 for x in actual)
        if not suspicious:
            return False

        # Re-test the same parameters using a fresh, independent seed batch.
        repeat_seeds = [chooser.getrandbits(128) for _ in range(BATCH_SIZE)]
        repeated = sample_batch(n, p, repeat_seeds)

        if isinstance(actual, dict):
            if repeated == actual:
                report(n, p, actual,
                       {"distribution": "binomial", "mean": int(expected),
                        "exception": None})
                return True
            return False

        if isinstance(repeated, list) and all(x == 0 for x in repeated):
            # Independently derived:
            # P(X=0)=(1-p)^n <= 1/(1+n*p)=1/2.
            # Thus 512 consecutive zeros have probability <= 2**-512
            # under independent documented binomial draws. This is statistical
            # evidence, not a claim that a finite sample proves the expectation.
            report(
                n, p,
                {"draws": 2 * BATCH_SIZE, "all_zero": True, "sample_mean": 0},
                {"distribution_mean": int(expected),
                 "all_zero_probability_upper_bound":
                     str(Fraction(1, 2 ** (2 * BATCH_SIZE)))},
            )
            return True
        return False

    # Hand-picked edges first, including the specifically requested input.
    for j in [55, 54] + list(range(56, 101)):
        if time.monotonic() >= DEADLINE:
            break
        if check(j):
            return

    # Then randomized valid inputs, selected reproducibly.
    while time.monotonic() < DEADLINE:
        if check(chooser.randint(54, 100)):
            return

    print("NO COUNTEREXAMPLE", cases_tested)


if __name__ == "__main__":
    main()