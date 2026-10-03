import csv

lines = ['name\n', '\n', '\n']
if list(csv.reader(lines)) != [['name'], [], []]:
    print('REFUTATION REJECTED: input is not a header followed by valid blank CSV lines')
else:
    consumed = []
    reader = csv.DictReader(consumed.append(line) or line for line in lines)
    list(reader)
    actual, expected = reader.line_num, len(consumed)
    if actual != expected:
        print('REFUTATION CONFIRMED:', lines, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: line_num equals the number of source lines consumed')