import decimal
import math
import random
import time


class ScriptedRandom(random.Random):
    def __init__(self, values):
        super().__init__(0)
        self.values = tuple(values)
        self.index = 0

    def random(self):
        if self.index < len(self.values):
            value = self.values[self.index]
            self.index += 1
            return value
        return 0.5


def reference(mu, kappa, values):
    """Evaluate the rejection sampler using high-precision real arithmetic."""
    rng = ScriptedRandom(values)
    if kappa <= 1e-6:
        return math.tau * rng.random()

    with decimal.localcontext() as ctx:
        ctx.prec = 700
        D = decimal.Decimal
        one = D(1)
        s = D("0.5") / D.from_float(kappa)
        r = s + (one + s * s).sqrt()

        while True:
            z = D.from_float(math.cos(math.pi * rng.random()))
            d = z / (r + z)
            u = D.from_float(rng.random())
            if u < one - d * d:
                break
            # For d < -1000, the second acceptance probability is
            # smaller than every positive binary64 random() value.
            if d < -1000:
                if u == 0:
                    break
            elif u <= (one - d) * d.exp():
                break

        f = (one + r * z) / (r + z)
        f = max(-1.0, min(1.0, float(f)))
        angle = math.acos(f)
        if rng.random() > 0.5:
            return (mu + angle) % math.tau
        return (mu - angle) % math.tau


def actual(case):
    try:
        return ScriptedRandom(case["random_values"]).vonmisesvariate(
            case["mu"], case["kappa"]
        )
    except Exception as exc:
        return (type(exc).__name__, str(exc))


def valid_sample(result):
    return isinstance(result, float) and math.isfinite(result) and 0 <= result <= math.tau


def main():
    start = time.monotonic()
    for mu, kappa in [(0.3, 1.0), (2.0, 4.0)]:
        case = {
            "mu": mu,
            "kappa": kappa,
            "random_values": (0.25, 0.1, 0.75),
        }
        expected = reference(mu, kappa, case["random_values"])
        observed = actual(case)
        agrees = valid_sample(observed) and math.isclose(
            observed, expected, rel_tol=1e-12, abs_tol=1e-12
        )
        print("SANITY:", repr(case), repr(observed), repr(expected), agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    edge = 1.0 - 2**-53
    concentrations = [
        1e20, 1e16, math.nextafter(1e16, 0.0),
        math.nextafter(1e16, math.inf), 1e17, 1e18,
        1e100, 1e200, 1e308,
    ]
    cases = (
        {"mu": mu, "kappa": k, "random_values": (edge, 0.5, 0.5, 0.5)}
        for k in concentrations
        for mu in (0.0, math.pi, math.tau)
    )
    seed = random.Random(872341)
    tested = 0

    while time.monotonic() - start < 175:
        try:
            case = next(cases)
        except StopIteration:
            case = {
                "mu": seed.uniform(0.0, math.tau),
                "kappa": 10.0 ** seed.uniform(16.0, 308.0),
                "random_values": (edge, 0.5, 0.5, 0.5),
            }

        expected = reference(case["mu"], case["kappa"], case["random_values"])
        observed = actual(case)
        tested += 1
        if not valid_sample(observed):
            repeated = actual(case)
            if repeated == observed:
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("actual:", repr(observed))
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()