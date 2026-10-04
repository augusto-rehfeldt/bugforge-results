from html.parser import HTMLParser
from xml.parsers.expat import ParserCreate

s = '<!DOCTYPE html SYSTEM "' + 'a>b' + '">'
actual, declarations = [], []

try:
    validator = ParserCreate()
    validator.StartDoctypeDeclHandler = lambda *args: declarations.append(args)
    validator.Parse(s + '<html/>', True)
    if declarations != [('html', 'a>b', None, 0)]:
        raise ValueError('system identifier was not preserved')
except Exception as e:
    print('REFUTATION REJECTED:', 'invalid declaration:', str(e))
else:
    parser = HTMLParser()
    parser.handle_decl = actual.append
    parser.feed(s)
    parser.close()
    expected = [s[2:-1]]
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'actual matches documented expectation')