import random
import time
from fractions import Fraction

POPULATION = ['a', 'b']
K = 100000


def reference(weights, k, seed):
    """Exact relative-weight selection using an independent implementation."""
    cumulative = []
    total = Fraction(0)
    for weight in weights:
        total += Fraction.from_float(weight)
        cumulative.append(total)

    rng = random.Random(seed)
    counts = dict.fromkeys(POPULATION, 0)
    for _ in range(k):
        position = Fraction.from_float(rng.random()) * total
        for item, boundary in zip(POPULATION, cumulative):
            if position < boundary:
                counts[item] += 1
                break
    return counts


def actual(weights, k, seed):
    sample = random.Random(seed).choices(
        POPULATION, weights=weights, k=k
    )
    return {item: sample.count(item) for item in POPULATION}


def main():
    start = time.monotonic()

    for weights in ([1.0, 1.0], [1.0, 3.0]):
        expected = reference(weights, 2000, 0)
        observed = actual(weights, 2000, 0)
        print("SANITY:", repr(weights), "actual:", observed,
              "reference:", expected)
        if observed != expected:
            print("SANITY FAILED")
            return

    generator = random.Random(73921)
    w = float.fromhex('0x0.0000000000001p-1022')
    hand_picked = [
        w,
        2 * w,
        float.fromhex('0x1.0000000000000p-1022'),
        1.0,
    ]
    cases = 0

    while time.monotonic() - start < 170:
        if cases < len(hand_picked):
            weight = hand_picked[cases]
        else:
            # All generated weights are finite, positive, and have finite sums.
            weight = float.fromhex(
                '0x1.%013xp%+d' %
                (generator.getrandbits(52), generator.randint(-1074, 1022))
            )
            if weight == 0.0:
                continue

        weights = [weight, weight]
        input_literal = {
            'population': POPULATION,
            'weights': weights,
            'k': K,
            'seed': 0,
        }
        expected_counts = reference(weights, K, 0)
        observed = actual(weights, K, 0)
        cases += 1

        # A generous ten-standard-deviation bound for Binomial(K, 1/2).
        # Exact deterministic reference counts are also reported for diagnosis.
        tolerance = 10 * (K / 4) ** 0.5
        if any(abs(observed[item] - K / 2) > tolerance
               for item in POPULATION):
            repeated = actual(weights, K, 0)
            if repeated != observed:
                continue

            ordinary = actual([1.0, 1.0], K, 0)
            print("COUNTEREXAMPLE:")
            print(repr(input_literal))
            print("actual:", repr({
                'counts': observed,
                'rerun_counts': repeated,
                'weights_1_1_counts': ordinary,
            }))
            print("expected:", repr({
                'probabilities': {'a': '1/2', 'b': '1/2'},
                'mean_counts': {'a': K / 2, 'b': K / 2},
                'exact_reference_counts': expected_counts,
                'count_tolerance': tolerance,
            }))
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == '__main__':
    main()