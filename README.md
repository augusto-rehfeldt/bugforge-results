# bugforge results

Behaviour of Python libraries that breaks their documentation, found by [bugforge](https://github.com/augusto-rehfeldt/bugforge): one language model proposes a documented property, another searches for a failing input, a third writes a minimal standalone reproducer, which is run, and a judge reads the reproducer, the documentation and the project's issue tracker. Every folder holds the reproducer and its output on the Python version named. No person reviewed these before publication; upstream reports are filed by hand, and a result is linked to its issue once filed.

5 result(s).

| Date | Target | Verdict | Title | Python | Upstream |
| --- | --- | --- | --- | --- | --- |
| 2026-10-03 | `ipaddress.IPv4Network.supernet` | bug | [IPv4Network.supernet skips new_prefix validation for /0 networks](ipaddress-c4/) | 3.14.6 | not filed |
| 2026-10-03 | `ipaddress.IPv6Address.exploded` | bug | [IPv6Address.exploded raises AddressValueError for valid scoped addresses](ipaddress-c1/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.HtmlDiff.make_table` | bug | [difflib.HtmlDiff drops literal U+0001 characters from source lines](difflib-c3/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.ndiff` | bug | [difflib ignores falsey callable linejunk predicates](difflib-c2/) | 3.14.6 | not filed |
| 2026-10-03 | `difflib.get_close_matches` | bug | [difflib.get_close_matches raises TypeError for tied matches containing non-orderable elements](difflib-c1/) | 3.14.6 | not filed |
