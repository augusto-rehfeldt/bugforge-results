*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.utils`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Three-digit obsolete years are interpreted without the required 1900 offset

Target: `email.utils.parsedate_tz`

Property: For every integer y from 100 through 999, parsedate_tz('01 Jan ' + str(y) + ' 12:00:00 +0000') must return a non-None tuple whose year component is y + 1900, as required by RFC 2822's obsolete three-digit year interpretation.

### Draft issue: email.utils.parsedate_tz misinterprets obsolete RFC 2822 three-digit years

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.utils`

**Documented behaviour:** The email.utils documentation describes parsedate_tz as performing “the same function as parsedate()” with an additional timezone element. The parsedate() documentation says: “Attempts to parse a date according to the rules in RFC 2822.” RFC 2822 §4.3 specifies: “If a three digit year is encountered, the year is interpreted by adding 1900 to the year.”

**Expected:** A non-None tuple with year component 2000.

**Actual:** (100, 1, 1, 12, 0, 0, 0, 1, -1, 0)

**Reproducer:**

```python
import email.utils
import re

s = '01 Jan ' + str(100) + ' 12:00:00 +0000'
if not re.fullmatch(r'01 Jan [1-9][0-9]{2} 12:00:00 \+0000', s):
    print('REFUTATION REJECTED: input is not a valid obsolete RFC 2822 date')
else:
    expected = int(s.split()[2]) + 1900  # RFC 2822 §4.3
    actual = email.utils.parsedate_tz(s)
    if actual is None or actual[0] != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual=', actual,
              'expected_year=', expected)
    else:
        print('REFUTATION REJECTED: actual year matches RFC 2822 §4.3')
```

**Output:**

```
REFUTATION CONFIRMED: '01 Jan 100 12:00:00 +0000' actual= (100, 1, 1, 12, 0, 0, 0, 1, -1, 0) expected_year= 2000
```

Judge: BUG (medium) -- The reproducer supplies a valid obsolete RFC 2822 date. Section 4.3 explicitly requires adding 1900 to a three-digit year, so 100 means 2000. parsedate_tz instead returns year 100, contradicting its documented RFC 2822 parsing behavior. None of the listed issues or pull requests covers this year interpretation. The supplied email.utils diff does not show a fix, though it does not establish the state of the underlying parser on main.

