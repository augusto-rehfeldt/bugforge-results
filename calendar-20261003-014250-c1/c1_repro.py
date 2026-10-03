import calendar
from html.parser import HTMLParser

data = dict(year=2024, width=3, encoding="utf-8", css="a&notin;.css")

class Links(HTMLParser):
    hrefs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "stylesheet":
            self.hrefs.append(a.get("href"))

if not (type(data["year"]) is int and 1 <= data["year"] <= 9999
        and isinstance(data["css"], str) and data["css"]
        and data["width"] == 3 and data["encoding"] == "utf-8"):
    print("REFUTATION REJECTED: invalid input")
else:
    parser = Links()
    parser.feed(calendar.HTMLCalendar().formatyearpage(
        data["year"], width=data["width"], encoding=data["encoding"],
        css=data["css"]).decode("utf-8"))
    parser.close()
    expected = data["css"]  # The documented stylesheet name, unchanged.
    if parser.hrefs != [expected]:
        actual = parser.hrefs[0] if len(parser.hrefs) == 1 else parser.hrefs
        print("REFUTATION CONFIRMED:", data, "actual =", repr(actual),
              "expected =", repr(expected))
    else:
        print("REFUTATION REJECTED: parsed href equals the stylesheet name")