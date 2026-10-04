try:
    import wcwidth

    scale, k, W, p = 2, 1, 2, 1
    sized = f'\x1b]66;s={scale};{"x" * k}\x07'
    text = 'a' * p + ' ' + sized
    case = dict(text=text, width=W, break_long_words=True)

    if not (scale >= 2 and k >= 1 and W >= scale * k and 0 <= p < W):
        raise ValueError("input violates the stated validity constraints")

    lines = wcwidth.wrap(**case)
    widths = []
    for line in lines:
        plain = line.replace(sized, '')
        if any(c not in 'a ' for c in plain):
            raise ValueError("output contains characters this independent oracle cannot measure")
        widths.append(len(plain) + line.count(sized) * scale * k)

    if any(n > W for n in widths):
        print("REFUTATION CONFIRMED:", case,
              {"lines": lines, "reference_widths": widths},
              {"every_line_width_at_most": W})
    else:
        print("REFUTATION REJECTED: every returned line fits", widths)
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))