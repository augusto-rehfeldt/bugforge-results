import math
import random
import statistics
import time


def reference(data, h, x):
    # Stable logistic CDF, averaged over the sample kernels.
    probabilities = []
    for datum in data:
        z = (x - datum) / h
        if z >= 0.0:
            probabilities.append(1.0 / (1.0 + math.exp(-z)))
        else:
            e = math.exp(z)
            probabilities.append(e / (1.0 + e))
    return math.fsum(probabilities) / len(data)


def actual(data, h, x):
    try:
        result = statistics.kde(
            data, h, kernel="logistic", cumulative=True
        )(x)
        return ("result", result)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def valid(data, h, x):
    return (
        bool(data)
        and all(math.isfinite(d) for d in data)
        and math.isfinite(h)
        and h > 0.0
        and math.isfinite(x)
        and all(math.isfinite((x - d) / h) for d in data)
    )


def failed(outcome):
    if outcome[0] == "exception":
        return True
    value = outcome[1]
    try:
        return not (math.isfinite(value) and 0.0 <= value <= 1.0)
    except (TypeError, ValueError):
        return True


def main():
    deadline = time.monotonic() + 175.0
    for data, h, x in [
        ([0.0], 1.0, 0.0),
        ([-1.0, 0.0, 2.0], 0.75, 0.5),
    ]:
        expected = reference(data, h, x)
        observed = actual(data, h, x)
        print("SANITY:", repr((data, h, x)), repr(observed),
              "expected:", repr(expected))
        if (
            observed[0] != "result"
            or not math.isclose(
                observed[1], expected, rel_tol=1e-12, abs_tol=1e-14
            )
        ):
            print("SANITY FAILED")
            return

    cases = 0

    def check(data, h, x):
        nonlocal cases
        if not valid(data, h, x):
            return False
        cases += 1
        observed = actual(data, h, x)
        if failed(observed):
            repeated = actual(data, h, x)
            if failed(repeated):
                expected = reference(data, h, x)
                print(
                    "COUNTEREXAMPLE:",
                    repr({"data": data, "h": h,
                          "kernel": "logistic", "cumulative": True, "x": x}),
                    "actual:", repr(repeated),
                    "expected:", repr(expected),
                )
                return True
        return False

    hand_picked = [
        ([0.0], 1.0, 710.0),
        ([0.0], 1.0, 1000.0),
        ([0.0], 1.0, 1e6),
        ([0.0], 1.0, 709.0),
        ([-2.0, 0.0, 3.0], 1.0, 1000.0),
        ([0.0, 1.0], 0.001, 1.0),
        ([0.0], 1e-300, 1e-294),
        ([0.0], 1.0, 1e308),
    ]
    for data, h, x in hand_picked:
        if check(data, h, x):
            return

    rng = random.Random(20260317)
    while time.monotonic() < deadline:
        h = 10.0 ** rng.uniform(-200.0, 200.0)
        data = [rng.uniform(-10.0, 10.0) * h
                for _ in range(rng.randint(1, 8))]
        z = rng.choice([
            rng.uniform(700.0, 750.0),
            rng.uniform(750.0, 1e6),
            10.0 ** rng.uniform(3.0, 100.0),
            rng.uniform(-1000.0, 1000.0),
        ])
        x = z * h
        if check(data, h, x):
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()