from email.headerregistry import HeaderRegistry, UnstructuredHeader
from email.errors import InvalidBase64PaddingDefect

value = '=?utf-8?b?YQ?='
if not value.isascii() or '\r' in value or '\n' in value:
    print('REFUTATION REJECTED: input is not unfolded ASCII')
else:
    expected = any(isinstance(d, InvalidBase64PaddingDefect)
                   for d in UnstructuredHeader.value_parser(value).all_defects)
    actual = any(isinstance(d, InvalidBase64PaddingDefect)
                 for d in HeaderRegistry()('Subject', value).defects)
    if expected and not actual:
        print('REFUTATION CONFIRMED:', repr(value),
              'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: parser prerequisite absent or defect preserved',
              repr(value), 'actual:', actual, 'expected:', expected)