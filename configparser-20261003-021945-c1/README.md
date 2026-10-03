*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Extended interpolation must preserve vars overrides through nested substitutions

Target: `configparser.RawConfigParser.get`

Property: For a ConfigParser using ExtendedInterpolation, with one ordinary section containing x='${y}', y='${z}', and z=b, get(section, 'x', vars={'z': v}) must return v for all strings b and v containing no '$'. The vars override must apply even when its referenced option is reached through another substitution.

### Draft issue: ExtendedInterpolation drops get() vars overrides during recursive interpolation

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** RawConfigParser.get documentation in the module docstring: "Additional substitutions may be provided using the `vars` argument, which must be a dictionary whose contents override any pre-existing defaults."

**Expected:** override

**Actual:** original

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'section': 's', 'b': 'original', 'v': 'override', 'vars': {'z': 'override'}} actual = 'original' expected = 'override'
```

Judge: BUG (medium) -- The input is valid and the expected-value calculation correctly resolves x → y → z using the supplied override. ExtendedInterpolation loses the vars mapping during recursive substitution, so the override works for direct references but not nested ones. This violates the documented substitution override behavior. The listed PR concerns items() including vars keys, not recursive interpolation, and the upstream differences do not fix this behavior.

