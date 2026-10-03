import configparser

section, b, v = "s", "original", "override"
options = {"x": "${y}", "y": "${z}", "z": b}
overrides = {"z": v}
data = {"section": section, "b": b, "v": v, "vars": overrides}

p = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
if section == p.default_section or not isinstance(overrides, dict) or any(
    not isinstance(s, str) or "$" in s for s in (b, v)
):
    print("REFUTATION REJECTED:", "invalid input")
else:
    p.read_dict({section: options})
    actual = p.get(section, "x", vars=overrides)
    substitutions = dict(options, **overrides)
    expected = substitutions["x"]
    while expected.startswith("${") and expected.endswith("}"):
        expected = substitutions[expected[2:-1]]
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual =", repr(actual),
              "expected =", repr(expected))
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")