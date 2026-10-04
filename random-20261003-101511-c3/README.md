*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Gamma sampling can loop forever for large finite shape parameters

Target: `random.Random.gammavariate`

Property: For finite floats alpha > 0 and beta > 0 with finite alpha * beta, Random(seed).gammavariate(alpha, beta) must terminate and return a gamma-distribution sample for every integer seed.

### Draft issue: random.Random.gammavariate loops indefinitely for large finite alpha

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.gammavariate docstring: "Gamma distribution. Not the gamma function!" and "Conditions on the parameters are alpha > 0 and beta > 0."

**Expected:** Terminate and return a gamma-distribution sample for these valid finite parameters.

**Actual:** Loops indefinitely for alpha=1e308 and beta=1e-308 because overflow creates a NaN acceptance value.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: (1e+308, 1e-308, 0) actual = nontermination: invariant NaN acceptance value expected = {'behavior': 'terminate with a gamma sample', 'mean': 0.9999999999999999, 'standard_deviation': 1e-154}
```

Judge: BUG (medium) -- The inputs satisfy the documented positive-parameter conditions and have a finite product. In the alpha > 1 algorithm, 2*alpha overflows, making ainv and ccc infinite. Every eligible draw then produces v = 0 and x = alpha, while ccc*v makes r NaN. Both acceptance tests consequently fail forever. The reproducer checks this deterministic trap rather than inferring nontermination solely from its draw limit. The upstream changes do not address it, and no duplicate is listed.

