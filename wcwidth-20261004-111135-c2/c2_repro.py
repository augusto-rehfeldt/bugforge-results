from wcwidth import iter_graphemes, iter_graphemes_reverse

s = "\r\n" + "".join(chr(0x1F1E6 + i % 26) for i in range(31)) + "\u200d"
if any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print("REFUTATION REJECTED: input contains non-scalar values")
else:
    actual = list(iter_graphemes(s))
    expected = list(reversed(list(iter_graphemes_reverse(s))))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), actual, expected)
    else:
        print("REFUTATION REJECTED: forward and reversed reverse traversal agree")