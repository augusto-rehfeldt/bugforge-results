# bugforge results

Behaviour of Python libraries that breaks their documentation, found by [bugforge](https://github.com/augusto-rehfeldt/bugforge): one language model proposes a documented property, another searches for a failing input, a third writes a minimal standalone reproducer, which is run, and a judge reads the reproducer, the documentation and the project's issue tracker. Every folder holds the reproducer and its output on the Python version named. No person reviewed these before publication; upstream reports are filed by hand, and a result is linked to its issue once filed.

116 result(s).

| Date | Target | Verdict | Title | Python | Upstream |
| --- | --- | --- | --- | --- | --- |
| 2026-10-04 | `zlib.decompressobj` | bug | [zlib.decompressobj fails after documented-safe zdict mutation with a partial initial header](zlib-20261003-065622-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `wave.Wave_write.writeframesraw` | bug | [wave.Wave_write silently loses audio data on short writes](wave-20261003-111327-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `wave.Wave_write.tell` | bug | [wave: handle short payload writes before advancing Wave_write frame position](wave-20261003-111327-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `wave.Wave_write.setnchannels` | bug | [wave: Reject parameter changes after empty frame writes](wave-20261003-042850-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `urllib.parse.urljoin` | bug | [urllib.parse.urljoin skips dot-segment removal for network-path references](urllib.parse-20261003-090106-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `urllib.parse.urljoin` | bug | [urljoin incorrectly inherits base authority for absolute file URLs with empty authority](urllib.parse-20261003-053113-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `unicodedata.UCD.numeric` | bug | [unicodedata.ucd_3_2_0.numeric returns newer numeric value for U+4EAC](unicodedata-20261003-064954-c4/) | 3.14.6 | not filed |
| 2026-10-04 | `unicodedata.UCD.normalize` | bug | [unicodedata.ucd_3_2_0.normalize incorrectly reorders marks across Unicode 3.2 unassigned characters](unicodedata-20261003-064954-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `unicodedata.UCD.is_normalized` | bug | [unicodedata.ucd_3_2_0.is_normalized incorrectly rejects NFD with a character unassigned in Unicode 3.2](unicodedata-20261003-064954-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `struct.Struct.iter_unpack` | bug | [Struct reinitialization to a zero-sized format makes an existing iter_unpack iterator nonterminating](struct-20261003-075217-c4/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.harmonic_mean` | bug | [statistics.harmonic_mean returns zero for identical positive subnormal floats](statistics-20261003-081656-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.pstdev` | bug | [statistics.pstdev overflows for large finite values when given the correct mean](statistics-20261003-081656-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.median` | bug | [statistics.median overflows for large finite middle values](statistics-20261003-045701-c4/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.correlation` | bug | [statistics.correlation misclassifies tiny nonconstant inputs as constant](statistics-20261003-045701-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.linear_regression` | bug | [statistics.linear_regression misclassifies small nonconstant inputs as constant due to underflow](statistics-20261003-045701-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `statistics.NormalDist.cdf` | bug | [statistics.NormalDist.cdf returns incorrect probability when x - mu overflows](statistics-20261003-045701-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `shlex.push_source` | bug | [shlex.push_source leaks buffered parent punctuation into pushed source](shlex-20261003-090557-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `random.Random.gammavariate` | bug | [random.Random.gammavariate loops indefinitely for large finite alpha](random-20261003-101511-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `random.Random.betavariate` | bug | [random.betavariate hangs for very large finite positive shape parameters](random-20261003-101511-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `random.triangular` | bug | [random.triangular returns infinity for finite bounds when their difference overflows](random-20261003-034345-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `random.Random.vonmisesvariate` | bug | [random.vonmisesvariate raises ZeroDivisionError for large finite kappa](random-20261003-034345-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `quopri.decode` | bug | [quopri.decode silently truncates output on short writes](quopri-20261003-110848-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `quopri.encode` | bug | [quopri.encode silently truncates output on short writes](quopri-20261003-110848-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `quopri.encodestring` | bug | [quopri pure-Python fallback exceeds quoted-printable line length limit at a space boundary](quopri-20261003-074352-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `quopri.encodestring` | bug | [quopri pure-Python encoder splits hexadecimal escapes at line boundaries](quopri-20261003-042505-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `quopri.encode` | bug | [quopri.encode pure-Python fallback splits hexadecimal escapes at line boundaries](quopri-20261003-042505-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `pprint.saferepr` | bug | [pprint.saferepr raises RecursionError when sorting self-referential list-subclass dictionary keys](pprint-20261003-073352-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `plistlib.loads` | bug | [plistlib binary serialization conflates aware datetimes with different fold-dependent UTC offsets](plistlib-20261003-073911-c4/) | 3.14.6 | not filed |
| 2026-10-04 | `plistlib.dump` | bug | [plistlib binary writer conflates fold-distinct aware datetimes before UTC conversion](plistlib-20261003-073911-c3/) | 3.14.6 | not filed |
| 2026-10-04 | `plistlib.load` | bug | [plistlib binary writer conflates fold-distinct aware datetimes](plistlib-20261003-073911-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `plistlib.load` | bug | [plistlib.load rejects XML dictionary keys when dict_type is collections.UserDict](plistlib-20261003-042133-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `operator.iconcat` | bug | [operator.iconcat ignores list subclass __iadd__ override](operator-20261003-044103-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `json.JSONEncoder.iterencode` | bug | [json.JSONEncoder.iterencode allows NaN float subclasses with allow_nan=False](json-20261003-083804-c4/) | 3.14.6 | [cpython#158730](https://github.com/python/cpython/issues/158730) |
| 2026-10-04 | `json.loads` | bug | [json.loads ignores explicitly supplied false-valued parse_float callables](json-20261003-051249-c4/) | 3.14.6 | [cpython#158729](https://github.com/python/cpython/issues/158729) |
| 2026-10-04 | `ipaddress.IPv6Interface.ip` | bug | [ipaddress.IPv6Interface.ip drops the IPv6 scope ID](ipaddress-20261003-050858-c2/) | 3.14.6 | [cpython#158723](https://github.com/python/cpython/issues/158723) |
| 2026-10-04 | `html.parser.HTMLParser.handle_decl` | bug | [HTMLParser truncates DOCTYPE declarations at '>' inside quoted system identifiers](html.parser-20261003-091556-c3/) | 3.14.6 | [cpython#158720](https://github.com/python/cpython/issues/158720) |
| 2026-10-04 | `heapq.nsmallest` | bug | [heapq.nsmallest violates sorted equivalence for ordering-equivalent objects with identity equality](heapq-20261003-061723-c4/) | 3.14.6 | [cpython#158718](https://github.com/python/cpython/issues/158718) |
| 2026-10-04 | `heapq.merge` | bug | [heapq.merge silently drops an input stream when key raises StopIteration](heapq-20261003-061723-c1/) | 3.14.6 | [cpython#158717](https://github.com/python/cpython/issues/158717) |
| 2026-10-04 | `email.utils.parsedate_tz` | bug | [email.utils.parsedate_tz misinterprets obsolete RFC 2822 three-digit years](email.utils-20261004-003800-c1/) | 3.14.6 | [cpython#158715](https://github.com/python/cpython/issues/158715) |
| 2026-10-04 | `email.utils.parseaddr` | bug | [email.utils.parseaddr(strict=True) accepts angle address without closing '>'](email.utils-20261003-092603-c3/) | 3.14.6 | [cpython#158714](https://github.com/python/cpython/issues/158714) |
| 2026-10-04 | `email.utils.decode_params` | bug | [email.utils.decode_params fails to combine RFC 2231 continuations with mixed-case attribute names](email.utils-20261003-092603-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `email.utils.getaddresses` | bug | [email.utils.getaddresses(strict=True) rejects valid mailboxes with commas in trailing comments](email.utils-20261003-060025-c4/) | 3.14.6 | [cpython#158713](https://github.com/python/cpython/issues/158713) |
| 2026-10-04 | `email.utils.decode_params` | bug | [email.utils.decode_params misinterprets apostrophes in unencoded RFC 2231 initial segments](email.utils-20261003-060025-c2/) | 3.14.6 | [cpython#158712](https://github.com/python/cpython/issues/158712) |
| 2026-10-04 | `email.headerregistry.Address` | bug | [email.headerregistry.Address fails to escape closing brackets in domain literals](email.headerregistry-20261004-004044-c1/) | 3.14.6 | not filed |
| 2026-10-04 | `email.headerregistry.MIMEVersionHeader.parse` | bug | [MIME-Version header parsing leaks ValueError for oversized numeric components](email.headerregistry-20261003-060502-c4/) | 3.14.6 | [cpython#158707](https://github.com/python/cpython/issues/158707) |
| 2026-10-04 | `difflib.HtmlDiff.make_table` | bug | [HtmlDiff.make_table raises RecursionError when wrapping long lines at column 1](difflib-20261003-082046-c2/) | 3.14.6 | [cpython#158704](https://github.com/python/cpython/issues/158704) |
| 2026-10-04 | `configparser.RawConfigParser.write` | bug | [configparser.write silently loses surrounding value whitespace instead of raising InvalidWriteError](configparser-20261003-093513-c2/) | 3.14.6 | not filed |
| 2026-10-04 | `cmath.isclose` | bug | [cmath.isclose incorrectly returns True for large finite opposite complex values](cmath-20261003-033712-c2/) | 3.14.6 | [cpython#158697](https://github.com/python/cpython/issues/158697) (open, 0 comment(s)) |
| 2026-10-04 | `base64.encode` | bug | [base64.encode silently treats non-blocking read returning None as EOF](base64-20261004-002157-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `wave.open` | bug | [wave.open fails on non-seekable input streams that implement tell()](wave-20261003-182548-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `wave.Wave_read.readframes` | bug | [wave.Wave_read loses frame position when underlying reads split frames](wave-20261003-151720-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `urllib.parse.urljoin` | bug | [urllib.parse.urljoin incorrectly collapses repeated slashes in relative paths](urllib.parse-20261003-015128-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `urllib.parse.urlsplit` | bug | [urllib.parse.urlsplit rejects documented bytearray inputs as unhashable](urllib.parse-20261003-015128-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `textwrap.TextWrapper.fill` | doc-bug | [Clarify TextWrapper width guarantees when indentation leaves no room for text](textwrap-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `textwrap.TextWrapper.wrap` | doc-bug | [Clarify TextWrapper width guarantees when indentation consumes the available width](textwrap-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `struct.Struct.iter_unpack` | bug | [struct.Struct.iter_unpack crashes when __buffer__ reinitializes the Struct to a zero-sized format](struct-20261003-232219-c4/) | 3.14.6 | [cpython#158695](https://github.com/python/cpython/issues/158695) (open, 0 comment(s)) |
| 2026-10-03 | `struct.Struct.pack_into` | bug | [struct.Struct.pack_into with '0p' modifies a byte outside its zero-sized representation](struct-20261003-182950-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `struct.pack_into` | bug | [struct.pack_into corrupts an 's' value when source and destination are the same bytearray](struct-20261003-122508-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `string.capwords` | bug | [string.capwords ignores falsey nonempty str subclasses when joining](string-20261003-020655-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.kde` | bug | [statistics.kde logistic CDF overflows for large finite arguments](statistics-c1/) | 3.14.6 | [cpython#158631](https://github.com/python/cpython/issues/158631) (open, 4 comment(s)) |
| 2026-10-03 | `statistics.kde` | bug | [statistics.kde sigmoid PDF raises OverflowError for finite tail inputs](statistics-20261003-234100-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.harmonic_mean` | bug | [statistics.harmonic_mean raises for positive finite inputs when weighted reciprocals underflow](statistics-20261003-234100-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.covariance` | bug | [statistics.covariance overflows when the final covariance is representable](statistics-20261003-185112-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.correlation` | bug | [statistics.correlation misclassifies distinct large integers as constant input](statistics-20261003-185112-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.fmean` | bug | [statistics.fmean returns zero for a singleton with a tiny positive weight](statistics-20261003-185112-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.quantiles` | bug | [statistics.quantiles produces infinite cut points from finite inputs with representable results](statistics-20261003-154526-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.NormalDist.overlap` | bug | [statistics.NormalDist.overlap returns incorrect coefficient for large finite standard deviations](statistics-20261003-124541-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.NormalDist.inv_cdf` | bug | [NormalDist.inv_cdf returns infinity from intermediate overflow for a finite quantile](statistics-20261003-124541-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `statistics.fmean` | bug | [statistics.fmean raises OverflowError for finite inputs with a representable mean](statistics-20261003-124541-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `shlex.pop_source` | bug | [shlex.pop_source() leaks punctuation buffered from the popped source](shlex-20261003-015527-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `random.Random.choices` | bug | [random.choices produces strongly biased results for equal subnormal weights](random-20261003-202849-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `random.Random.betavariate` | bug | [random.betavariate produces biased samples for small positive shape parameters](random-20261003-174041-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `random.binomialvariate` | bug | [random.binomialvariate returns deterministic zero for small positive p with n*p=1](random-20261003-142339-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `random.Random.binomialvariate` | bug | [random.binomialvariate returns only zero for large n and tiny p with n*p = 1](random-20261003-142339-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `plistlib.dump` | bug | [plistlib.dump fails on non-seekable writable streams with FMT_BINARY](plistlib-20261003-211350-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `plistlib.dumps` | bug | [plistlib XML serialization normalizes carriage returns in keys, causing silent data loss](plistlib-20261003-150942-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `json.dumps` | bug | [json.JSONEncoder.iterencode drops entries from dict subclasses with false truthiness](json-20261003-130022-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `json.dump` | bug | [json.dump silently drops entries from dict subclasses with false truthiness](json-20261003-130022-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv4Network.supernet` | bug | [IPv4Network.supernet skips new_prefix validation for /0 networks](ipaddress-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv6Address.exploded` | bug | [IPv6Address.exploded raises AddressValueError for valid scoped addresses](ipaddress-c1/) | 3.14.6 | [cpython#158728](https://github.com/python/cpython/issues/158728) |
| 2026-10-03 | `ipaddress.IPv6Network.address_exclude` | bug | [IPv6Network.address_exclude raises AssertionError for contained scoped IPv6 networks](ipaddress-20261003-235502-c3/) | 3.14.6 | [cpython#158727](https://github.com/python/cpython/issues/158727) |
| 2026-10-03 | `ipaddress.IPv6Network.is_global` | bug | [ipaddress: IPv6Network.is_global violates documented endpoint classification rule](ipaddress-20261003-190337-c3/) | 3.14.6 | [cpython#158726](https://github.com/python/cpython/issues/158726) |
| 2026-10-03 | `ipaddress.IPv6Interface.with_prefixlen` | bug | [ipaddress.IPv6Interface.with_prefixlen drops IPv6 scope IDs](ipaddress-20261003-155745-c2/) | 3.14.6 | [cpython#158725](https://github.com/python/cpython/issues/158725) |
| 2026-10-03 | `ipaddress.IPv6Address.__add__` | bug | [ipaddress: IPv6Address integer addition discards scope ID](ipaddress-20261003-125643-c1/) | 3.14.6 | [cpython#158724](https://github.com/python/cpython/issues/158724) |
| 2026-10-03 | `html.parser.HTMLParser.goahead` | bug | [HTMLParser raises ValueError for oversized decimal character references](html.parser-20261003-193928-c4/) | 3.14.6 | [cpython#158722](https://github.com/python/cpython/issues/158722) |
| 2026-10-03 | `html.parser.HTMLParser.parse_starttag` | bug | [HTMLParser raises ValueError for numeric character references with many leading zeros](html.parser-20261003-132957-c1/) | 3.14.6 | [cpython#158721](https://github.com/python/cpython/issues/158721) |
| 2026-10-03 | `html.unescape` | bug | [html.unescape raises ValueError for decimal character references exceeding the integer conversion digit limit](html-20261003-020338-c2/) | 3.14.6 | [cpython#158719](https://github.com/python/cpython/issues/158719) |
| 2026-10-03 | `heapq.merge` | bug | [heapq.merge fails for valid iterators whose __next__ has no __self__](heapq-20261003-022813-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `fractions.Fraction.__format__` | bug | [Fraction scientific formatting fails for near-unit values with large numerators and denominators](fractions-20261003-233134-c1/) | 3.14.6 | [cpython#158716](https://github.com/python/cpython/issues/158716) |
| 2026-10-03 | `email.utils.parseaddr` | bug | [email.utils.parseaddr(strict=True) accepts consecutive dots in an unquoted local part](email.utils-20261003-194822-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.getaddresses` | bug | [email.utils.getaddresses rejects valid domain-literal addresses in strict mode](email.utils-20261003-134022-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.encode_rfc2231` | doc-bug | [Clarify encode_rfc2231 docstring: values are quoted even without charset or language](email.utils-20261003-021105-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.format_datetime` | bug | [email.utils.format_datetime rejects custom zero-offset tzinfo with usegmt=True](email.utils-20261003-021105-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `email.utils.formataddr` | bug | [email.utils.parseaddr rejects a valid quoted local part containing '\['](email.utils-20261003-021105-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `email.headerregistry.ParameterizedMIMEHeader` | bug | [email: Match RFC 2231 continuation parameter names case-insensitively](email.headerregistry-20261003-195236-c3/) | 3.14.6 | [cpython#158710](https://github.com/python/cpython/issues/158710) |
| 2026-10-03 | `email.headerregistry.ContentDispositionHeader` | bug | [email.headerregistry fails to combine RFC 2231 continuations with mixed-case parameter names](email.headerregistry-20261003-195236-c1/) | 3.14.6 | [cpython#158709](https://github.com/python/cpython/issues/158709) |
| 2026-10-03 | `email.headerregistry.MIMEVersionHeader` | bug | [MIMEVersionHeader raises ValueError on non-decimal Unicode digits](email.headerregistry-20261003-134457-c2/) | 3.14.6 | [cpython#158708](https://github.com/python/cpython/issues/158708) |
| 2026-10-03 | `email.headerregistry.UnstructuredHeader` | bug | [UnstructuredHeader drops encoded-word Base64 padding defects](email.headerregistry-20261003-021509-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `email.headerregistry.Address` | bug | [email.headerregistry.Address fails to quote usernames with leading dots](email.headerregistry-20261003-021509-c1/) | 3.14.6 | [cpython#158706](https://github.com/python/cpython/issues/158706) |
| 2026-10-03 | `difflib.HtmlDiff.make_table` | bug | [difflib.HtmlDiff drops literal U+0001 characters from source lines](difflib-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.get_close_matches` | bug | [difflib.get_close_matches raises TypeError for tied matches containing non-orderable elements](difflib-c1/) | 3.14.6 | [cpython#158705](https://github.com/python/cpython/issues/158705) |
| 2026-10-03 | `difflib.ndiff` | bug | [difflib ignores falsey callable junk predicates](difflib-20261003-011733-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `datetime.datetime.fromisoformat` | bug | [datetime.fromisoformat loses fractional UTC offsets smaller than one second](datetime-20261003-014717-c4/) | 3.14.6 | [cpython#158703](https://github.com/python/cpython/issues/158703) |
| 2026-10-03 | `datetime.time.fromisoformat` | bug | [datetime.time.fromisoformat loses subsecond-only UTC offsets](datetime-20261003-014717-c2/) | 3.14.6 | [cpython#158702](https://github.com/python/cpython/issues/158702) |
| 2026-10-03 | `datetime.date` | bug | [datetime.date raises OverflowError instead of documented ValueError for very large integer years](datetime-20261003-014717-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `csv.Sniffer.has_header` | bug | [csv.Sniffer.has_header raises csv.Error for valid CR-terminated CSV](csv-20261003-135109-c1/) | 3.14.6 | [cpython#158701](https://github.com/python/cpython/issues/158701) |
| 2026-10-03 | `csv.DictReader` | bug | [csv.DictReader.line_num is stale after skipping trailing blank lines](csv-20261003-022404-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `csv.DictWriter.writeheader` | bug | [csv.DictWriter.writeheader loses field-name representations for equal keys](csv-20261003-022404-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `configparser.InvalidWriteError` | bug | [configparser fails to reject comment-prefixed multiline values that cannot round-trip](configparser-20261003-195537-c3/) | 3.14.6 | [cpython#158700](https://github.com/python/cpython/issues/158700) |
| 2026-10-03 | `configparser.RawConfigParser.write` | bug | [configparser.write() fails to reject values truncated by inline comments](configparser-20261003-195537-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `configparser.RawConfigParser.write` | bug | [configparser.write() fails to reject blank lines in values when empty_lines_in_values=False](configparser-20261003-170729-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `configparser.RawConfigParser.write` | bug | [configparser.write fails to reject comment-prefixed option names](configparser-20261003-021945-c2/) | 3.14.6 | [cpython#158699](https://github.com/python/cpython/issues/158699) |
| 2026-10-03 | `configparser.RawConfigParser.get` | bug | [ExtendedInterpolation drops get() vars overrides during recursive interpolation](configparser-20261003-021945-c1/) | 3.14.6 | [cpython#158698](https://github.com/python/cpython/issues/158698) |
| 2026-10-03 | `calendar.HTMLCalendar.formatyearpage` | bug | [Escape the stylesheet href in calendar.HTMLCalendar.formatyearpage](calendar-20261003-014250-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `base64.a85encode` | doc-bug | [Document minimum wrapcol of 2 for a85encode with adobe=True](base64-20261003-020052-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `base64.encode` | bug | [base64.encode silently truncates output when the binary stream performs short writes](base64-20261003-020052-c1/) | 3.14.6 | [cpython#158696](https://github.com/python/cpython/issues/158696) (open, 0 comment(s)) |
