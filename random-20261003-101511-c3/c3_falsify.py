import math
import random
import sys
import time

# Independent implementation of the alpha > 1 rejection sampler.
# Unlike the overflowing expression sqrt(2*alpha - 1), this computes
# its scale safely for very large finite alpha.
def reference(alpha, beta, seed):
    rng = random.Random(seed)
    if alpha > sys.float_info.max / 2:
        scale = math.sqrt(alpha) * math.sqrt(2.0 - 1.0 / alpha)
    else:
        scale = math.sqrt(2.0 * alpha - 1.0)
    offset = alpha - math.log(4.0)
    coefficient = alpha + scale
    for _ in range(10000):
        u = rng.random()
        if not 1e-7 < u < 0.9999999:
            continue
        w = 1.0 - rng.random()
        v = math.log(u / (1.0 - u)) / scale
        x = alpha * math.exp(v)
        z = u * u * w
        r = offset + coefficient * v - x
        if r + 1.0 + math.log(4.5) - 4.5 * z >= 0.0:
            return x * beta
        if r >= math.log(z):
            return x * beta
    raise AssertionError("Reference unexpectedly exhausted its bound")


for case in ((2.0, 3.0, 0), (5.0, 0.5, 42)):
    alpha, beta, seed = case
    expected = reference(alpha, beta, seed)
    actual = random.Random(seed).gammavariate(alpha, beta)
    print("SANITY:", repr(case), repr(actual), repr(expected))
    if actual != expected:
        print("SANITY FAILED")
        sys.exit(0)


class DrawLimit(Exception):
    pass


class BoundedRandom(random.Random):
    def __init__(self, seed):
        super().__init__(seed)
        self.draws = 0

    def random(self):
        if self.draws >= 512:
            raise DrawLimit()
        self.draws += 1
        return super().random()


def probe(case):
    alpha, beta, seed = case
    rng = BoundedRandom(seed)
    evidence = {"nan_rejection_states": 0}
    code = random.Random.gammavariate.__code__

    def trace(frame, event, arg):
        if frame.f_code is code and event == "line":
            loc = frame.f_locals
            if all(name in loc for name in ("ainv", "ccc", "r")):
                if (math.isinf(loc["ainv"])
                        and math.isinf(loc["ccc"])
                        and math.isnan(loc["r"])):
                    evidence["nan_rejection_states"] += 1
        return trace

    previous = sys.gettrace()
    sys.settrace(trace)
    try:
        result = rng.gammavariate(alpha, beta)
        return ("returned", result)
    except DrawLimit:
        return ("draw limit reached", rng.draws,
                evidence["nan_rejection_states"])
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))
    finally:
        sys.settrace(previous)


def rejection_proof(alpha):
    # For every eligible u, log(u/(1-u)) is finite. Division by
    # infinite ainv gives signed zero, so ccc*v is NaN. Both
    # acceptance comparisons with r are consequently false.
    ainv = math.sqrt(2.0 * alpha - 1.0)
    ccc = alpha + ainv
    v = math.log(0.25 / 0.75) / ainv
    r = alpha - math.log(4.0) + ccc * v - alpha * math.exp(v)
    return math.isinf(ainv) and math.isinf(ccc) and math.isnan(r)


start = time.monotonic()
chooser = random.Random(8675309)
handpicked = [
    (1e308, 1e-308, 0),
    (9e307, 1e-307, 1),
    (1.7e308, 1e-308, -1),
]
tested = 0

while time.monotonic() - start < 170:
    if tested < len(handpicked):
        case = handpicked[tested]
    else:
        case = (
            chooser.uniform(9e307, 1.7e308),
            chooser.uniform(1e-308, 1e-307),
            chooser.randrange(-(1 << 63), 1 << 63),
        )
    alpha, beta, seed = case
    assert (math.isfinite(alpha) and alpha > 0
            and math.isfinite(beta) and beta > 0
            and math.isfinite(alpha * beta))

    tested += 1
    expected_sample = reference(alpha, beta, seed)
    actual = probe(case)
    proven = rejection_proof(alpha)
    failed = (
        actual[0] == "exception"
        or (actual[0] == "draw limit reached"
            and actual[2] > 0 and proven)
        or (actual[0] == "returned"
            and (not math.isfinite(actual[1]) or actual[1] < 0))
    )
    if failed:
        replay = probe(case)
        if replay == actual:
            expected = {
                "behavior": "terminate with a finite gamma sample",
                "stable_reference_sample": expected_sample,
            }
            if actual[0] == "draw limit reached":
                actual = {
                    "behavior": "nontermination: NaN makes both acceptance tests false",
                    "bounded_observation": actual,
                    "replay": replay,
                }
            print("COUNTEREXAMPLE:", repr(case),
                  "actual =", repr(actual),
                  "expected =", repr(expected))
            sys.exit(0)

print("NO COUNTEREXAMPLE", tested)