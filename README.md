# bugforge results

Behaviour of Python libraries that breaks their documentation, found by [bugforge](https://github.com/augusto-rehfeldt/bugforge): one language model proposes a documented property, another searches for a failing input, a third writes a minimal standalone reproducer, which is run, and a judge reads the reproducer, the documentation and the project's issue tracker. Every folder holds the reproducer and its output on the Python version named. No person reviewed these before publication; upstream reports are filed by hand, and a result is linked to its issue once filed.

42 result(s).

| Date | Target | Verdict | Title | Python | Upstream |
| --- | --- | --- | --- | --- | --- |
| 2026-10-03 | `urllib.parse.urljoin` | bug | [urllib.parse.urljoin incorrectly collapses repeated slashes in relative paths](urllib.parse-20261003-015128-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `urllib.parse.urlsplit` | bug | [urllib.parse.urlsplit rejects documented bytearray inputs as unhashable](urllib.parse-20261003-015128-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `textwrap.TextWrapper.fill` | doc-bug | [Clarify TextWrapper width guarantees when indentation leaves no room for text](textwrap-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `textwrap.TextWrapper.wrap` | doc-bug | [Clarify TextWrapper width guarantees when indentation consumes the available width](textwrap-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `struct.pack_into` | bug | [struct.pack_into corrupts an 's' value when source and destination are the same bytearray](struct-20261003-122508-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `string.capwords` | bug | [string.capwords ignores falsey nonempty str subclasses when joining](string-20261003-020655-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.kde` | bug | [statistics.kde logistic CDF overflows for large finite arguments](statistics-c1/) | 3.14.6 | [cpython#158631](https://github.com/python/cpython/issues/158631) (open, 4 comment(s)) |
| 2026-10-03 | `statistics.NormalDist.overlap` | bug | [statistics.NormalDist.overlap returns incorrect coefficient for large finite standard deviations](statistics-20261003-124541-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.NormalDist.inv_cdf` | bug | [NormalDist.inv_cdf returns infinity from intermediate overflow for a finite quantile](statistics-20261003-124541-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.fmean` | bug | [statistics.fmean raises OverflowError for finite inputs with a representable mean](statistics-20261003-124541-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `shlex.pop_source` | bug | [shlex.pop_source() leaks punctuation buffered from the popped source](shlex-20261003-015527-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `random.binomialvariate` | bug | [random.binomialvariate returns deterministic zero for small positive p with n*p=1](random-20261003-142339-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `random.Random.binomialvariate` | bug | [random.binomialvariate returns only zero for large n and tiny p with n*p = 1](random-20261003-142339-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `json.dumps` | bug | [json.JSONEncoder.iterencode drops entries from dict subclasses with false truthiness](json-20261003-130022-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `json.dump` | bug | [json.dump silently drops entries from dict subclasses with false truthiness](json-20261003-130022-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv4Network.supernet` | bug | [IPv4Network.supernet skips new_prefix validation for /0 networks](ipaddress-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv6Address.exploded` | bug | [IPv6Address.exploded raises AddressValueError for valid scoped addresses](ipaddress-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv6Address.__add__` | bug | [ipaddress: IPv6Address integer addition discards scope ID](ipaddress-20261003-125643-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `html.parser.HTMLParser.parse_starttag` | bug | [HTMLParser raises ValueError for numeric character references with many leading zeros](html.parser-20261003-132957-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `html.unescape` | bug | [html.unescape raises ValueError for decimal character references exceeding the integer conversion digit limit](html-20261003-020338-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `heapq.merge` | bug | [heapq.merge fails for valid iterators whose __next__ has no __self__](heapq-20261003-022813-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.getaddresses` | bug | [email.utils.getaddresses rejects valid domain-literal addresses in strict mode](email.utils-20261003-134022-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.encode_rfc2231` | doc-bug | [Clarify encode_rfc2231 docstring: values are quoted even without charset or language](email.utils-20261003-021105-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.format_datetime` | bug | [email.utils.format_datetime rejects custom zero-offset tzinfo with usegmt=True](email.utils-20261003-021105-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.formataddr` | bug | [email.utils.parseaddr rejects a valid quoted local part containing '\['](email.utils-20261003-021105-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `email.headerregistry.MIMEVersionHeader` | bug | [MIMEVersionHeader raises ValueError on non-decimal Unicode digits](email.headerregistry-20261003-134457-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `email.headerregistry.UnstructuredHeader` | bug | [UnstructuredHeader drops encoded-word Base64 padding defects](email.headerregistry-20261003-021509-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `email.headerregistry.Address` | bug | [email.headerregistry.Address fails to quote usernames with leading dots](email.headerregistry-20261003-021509-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.HtmlDiff.make_table` | bug | [difflib.HtmlDiff drops literal U+0001 characters from source lines](difflib-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.get_close_matches` | bug | [difflib.get_close_matches raises TypeError for tied matches containing non-orderable elements](difflib-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.ndiff` | bug | [difflib ignores falsey callable junk predicates](difflib-20261003-011733-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `datetime.datetime.fromisoformat` | bug | [datetime.fromisoformat loses fractional UTC offsets smaller than one second](datetime-20261003-014717-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `datetime.time.fromisoformat` | bug | [datetime.time.fromisoformat loses subsecond-only UTC offsets](datetime-20261003-014717-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `datetime.date` | bug | [datetime.date raises OverflowError instead of documented ValueError for very large integer years](datetime-20261003-014717-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `csv.Sniffer.has_header` | bug | [csv.Sniffer.has_header raises csv.Error for valid CR-terminated CSV](csv-20261003-135109-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `csv.DictReader` | bug | [csv.DictReader.line_num is stale after skipping trailing blank lines](csv-20261003-022404-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `csv.DictWriter.writeheader` | bug | [csv.DictWriter.writeheader loses field-name representations for equal keys](csv-20261003-022404-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `configparser.RawConfigParser.write` | bug | [configparser.write fails to reject comment-prefixed option names](configparser-20261003-021945-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `configparser.RawConfigParser.get` | bug | [ExtendedInterpolation drops get() vars overrides during recursive interpolation](configparser-20261003-021945-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `calendar.HTMLCalendar.formatyearpage` | bug | [Escape the stylesheet href in calendar.HTMLCalendar.formatyearpage](calendar-20261003-014250-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `base64.a85encode` | doc-bug | [Document minimum wrapcol of 2 for a85encode with adobe=True](base64-20261003-020052-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `base64.encode` | bug | [base64.encode silently truncates output when the binary stream performs short writes](base64-20261003-020052-c1/) | 3.14.6 | not filed |
