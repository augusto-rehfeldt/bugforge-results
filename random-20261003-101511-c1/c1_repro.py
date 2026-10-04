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