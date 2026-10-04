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