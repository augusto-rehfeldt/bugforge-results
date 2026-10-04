import random
import time
import unicodedata

# Embedded Unicode 3.2 reference excerpt.
# Numeric entries come from Unicode 3.2 Unihan numeric properties.
# U+4EAC..U+4EAF are assigned Han characters in UnicodeData-3.2.0;
# none has a numeric entry in that version's Unihan data.
REFERENCE_NUMERIC = {
    "\u4e00": 1,       # 一
    "\u4e8c": 2,       # 二
    "\u4e09": 3,       # 三
    "\u5341": 10,      # 十
    "\u767e": 100,     # 百
    "\u5343": 1000,    # 千
    "\u4e07": 10000,   # 万
}
REFERENCE_NONNUMERIC = {
    "\u4eac": None,    # 京
    "\u4ead": None,    # 亭
    "\u4eae": None,    # 亮
    "\u4eaf": None,    # 亯
}

u = unicodedata.ucd_3_2_0
sentinel = object()
deadline = time.monotonic() + 175.0


def observe(character):
    try:
        value = u.numeric(character)
        omitted = ("returned", value)
    except ValueError:
        omitted = ("raised", "ValueError")
    except Exception as exc:
        omitted = ("raised", type(exc).__name__)

    try:
        value = u.numeric(character, sentinel)
        supplied = (
            ("returned", "sentinel by identity")
            if value is sentinel
            else ("returned", value)
        )
    except Exception as exc:
        supplied = ("raised", type(exc).__name__)

    return omitted, supplied


expected = (
    ("raised", "ValueError"),
    ("returned", "sentinel by identity"),
)

# Two independent reference sanity checks.
try:
    actual_one = u.numeric("\u4e00")
except Exception as exc:
    actual_one = type(exc).__name__
print("SANITY:", repr("\u4e00"), actual_one, "expected", REFERENCE_NUMERIC["\u4e00"])
sanity_one = actual_one == REFERENCE_NUMERIC["\u4e00"]

actual_two = observe("\u4ead")
print("SANITY:", repr("\u4ead"), repr(actual_two), "expected", repr(expected))
sanity_two = actual_two == expected

if not (sanity_one and sanity_two):
    print("SANITY FAILED")
    raise SystemExit(0)

cases = 0


def check(character):
    global cases
    cases += 1
    actual = observe(character)
    if actual != expected:
        repeated = observe(character)
        if repeated != expected:
            print(
                "COUNTEREXAMPLE:",
                repr(character),
                "actual:",
                repr(repeated),
                "expected:",
                repr(expected),
            )
            raise SystemExit(0)


# Hand-picked edge cases first, with 京 explicitly first.
for character in ("\u4eac", "\u4eaf", "\u4eae", "\u4ead"):
    if time.monotonic() >= deadline:
        break
    check(character)

# Enumerate the assigned Han characters covered by the embedded excerpt.
# The current database is used only to prioritize inputs, never as an oracle.
candidates = list(REFERENCE_NONNUMERIC)


def currently_numeric(character):
    try:
        unicodedata.numeric(character)
        return True
    except ValueError:
        return False


candidates.sort(key=lambda character: (not currently_numeric(character), ord(character)))
for character in candidates:
    if time.monotonic() >= deadline:
        break
    check(character)

rng = random.Random(320032)
for _ in range(100000):
    if time.monotonic() >= deadline:
        break
    check(rng.choice(candidates))

print("NO COUNTEREXAMPLE", cases)