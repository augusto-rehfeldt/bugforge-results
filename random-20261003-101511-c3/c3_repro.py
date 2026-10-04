import random
import math

args = (1e308, 1e-308, 0)
alpha, beta, seed = args
if not (math.isfinite(alpha) and alpha > 0 and
        math.isfinite(beta) and beta > 0 and
        math.isfinite(alpha * beta)):
    print("REFUTATION REJECTED:", "invalid input", args)
else:
    class DrawLimit(Exception):
        pass

    class BoundedRandom(random.Random):
        draws = 0

        def random(self):
            self.draws += 1
            if self.draws > 512:
                raise DrawLimit
            return super().random()

    # Distribution moments, not a seed-dependent reference implementation.
    expected = dict(behavior="terminate with a gamma sample",
                    mean=alpha * beta,
                    standard_deviation=math.sqrt(alpha) * beta)
    try:
        actual = BoundedRandom(seed).gammavariate(alpha, beta)
    except DrawLimit as exc:
        tb = exc.__traceback__
        while tb and tb.tb_frame.f_code.co_name != "gammavariate":
            tb = tb.tb_next
        state = tb.tb_frame.f_locals if tb else {}
        # These loop invariants force r = bbb + ccc*v - x to NaN
        # on every eligible draw, so neither acceptance test can pass.
        trapped = (state.get("ainv") == math.inf and
                   state.get("ccc") == math.inf and
                   state.get("v") == 0 and
                   state.get("x") == alpha and
                   math.isnan(state.get("r", 0)))
        if trapped:
            print("REFUTATION CONFIRMED:", args,
                  "actual =", "nontermination: invariant NaN acceptance value",
                  "expected =", expected)
        else:
            print("REFUTATION REJECTED:", "draw limit alone is inconclusive", args)
    except Exception as exc:
        print("REFUTATION CONFIRMED:", args,
              "actual =", repr(exc), "expected =", expected)
    else:
        print("REFUTATION REJECTED:", args, "returned", actual,
              "; one sample cannot establish a distributional defect")