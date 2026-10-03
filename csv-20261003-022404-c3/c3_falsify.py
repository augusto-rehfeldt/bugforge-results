import csv
import random
import time


def expected(lines):
    # Each input string is exactly one newline-terminated physical line.
    return len(lines)


def actual(lines):
    reader = csv.DictReader(iter(lines))
    list(reader)
    return reader.line_num


def main():
    sanity_inputs = [
        ["name\n", "Alice\n"],
        ["name,age\n", "Alice,30\n", "Bob,25\n"],
    ]
    for i, lines in enumerate(sanity_inputs, 1):
        got = actual(lines)
        want = expected(lines)
        print(f"SANITY {i}: actual={got}, expected={want}")
        if got != want:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0

    def check(lines):
        nonlocal tested
        tested += 1
        got = actual(lines)
        want = expected(lines)
        if got != want:
            repeated = actual(lines)
            if repeated == got and repeated != want:
                print("COUNTEREXAMPLE:")
                print(repr(lines))
                print(f"actual: {got}")
                print(f"expected: {want}")
                return True
        return False

    edge_cases = [
        ["name\n", "\n", "\n"],
        ["name\n", "\n"],
        ["name\n", "Alice\n", "\n"],
        ["name,age\n", "Alice,30\n", "\n", "\n"],
        ["name\r\n", "\r\n", "\r\n"],
        ["name\n"] + ["\n"] * 100,
    ]
    for lines in edge_cases:
        if check(lines):
            return

    rng = random.Random(20250308)
    while time.monotonic() - start < 175:
        newline = rng.choice(["\n", "\r\n"])
        width = rng.randint(1, 5)
        lines = [",".join(f"field{i}" for i in range(width)) + newline]
        for _ in range(rng.randint(0, 40)):
            lines.append(
                ",".join(str(rng.randint(-1000, 1000)) for _ in range(width))
                + newline
            )
        lines.extend([newline] * rng.randint(1, 30))
        if check(lines):
            return

    print(f"NO COUNTEREXAMPLE {tested}")


if __name__ == "__main__":
    main()