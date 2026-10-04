*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Symmetric beta distribution collapses to zero for large finite shape parameters

Target: `random.Random.betavariate`

Property: For equal finite positive shape parameters alpha = beta, the generated beta distribution must have expected value 0.5. In particular, alpha = beta = 9e307 must not produce a distribution concentrated entirely at zero.

### Draft issue: random.betavariate hangs for very large finite positive shape parameters

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.betavariate docstring: "Conditions on the parameters are alpha > 0 and beta > 0." and "E[X] = alpha / (alpha + beta)". Mathematically, equal positive parameters give an expected value of 0.5.

**Expected:** Sampling terminates and returns beta-distributed values concentrated near 0.5.

**Actual:** The subprocess timed out after one second; no samples or sample mean were obtained.

**Reproducer:**

```python
import random, math, subprocess, sys, json

a = b = 9e307
seed, n = 0, 128
inp = dict(alpha=a, beta=b, seed=seed, samples=n)
if not (math.isfinite(a) and math.isfinite(b) and a > 0 and b > 0):
    print("REFUTATION REJECTED:", inp, "invalid parameters")
else:
    expected = 1 / (1 + b / a)  # Avoid overflow in alpha + beta.
    code = (
        f"import random,json; r=random.Random({seed}); "
        f"print(json.dumps([r.betavariate({a!r},{b!r}) for _ in range({n})]))"
    )
    try:
        p = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=1
        )
        if p.returncode:
            print("REFUTATION REJECTED:", inp, "test failed:", p.stderr.strip())
        else:
            xs = json.loads(p.stdout)
            actual = dict(mean=math.fsum(xs) / n, all_zero=all(x == 0 for x in xs))
            broken = actual["all_zero"] or any(not 0 <= x <= 1 for x in xs)
            print("REFUTATION CONFIRMED:" if broken else "REFUTATION REJECTED:",
                  inp, "actual:", actual, "expected:", expected,
                  *([] if broken else ["no demonstrated violation"]))
    except subprocess.TimeoutExpired:
        print("REFUTATION CONFIRMED:", inp,
              "actual:", {"timeout_seconds": 1}, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'alpha': 9e+307, 'beta': 9e+307, 'seed': 0, 'samples': 128} actual: {'timeout_seconds': 1} expected: 0.5
```

Judge: BUG (medium) -- Both parameters are finite and positive, and the correct mathematical expectation is 0.5. The output demonstrates a timeout, not an all-zero distribution. There is nevertheless a concrete overflow-induced nontermination defect: gammavariate's calculation of 2 * alpha - 1 overflows, leading to infinity and NaN in its rejection test, so candidates are never accepted. The listed issues concern different behavior, and the upstream changes do not address this path.

