import io, wave

p = dict(channels=1, sample_width=1, frame_rate=8000,
         method="writeframes", data=b"", new_channels=2)
try:
    if not (p["channels"] > 0 and 1 <= p["sample_width"] <= 4
            and p["frame_rate"] > 0 and p["new_channels"] > 0
            and p["new_channels"] != p["channels"]
            and isinstance(p["data"], bytes)):
        raise ValueError("invalid PCM input")
    w = wave.open(io.BytesIO(), "wb")
    w.setparams((p["channels"], p["sample_width"], p["frame_rate"],
                 0, "NONE", "not compressed"))
    getattr(w, p["method"])(p["data"])
    expected = "raises wave.Error"  # Documentation forbids changes after either write.
    try:
        w.setnchannels(p["new_channels"])
        actual = "no exception"
    except wave.Error:
        actual = "raises wave.Error"
    if actual != expected:
        print("REFUTATION CONFIRMED:", p, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: documented wave.Error was raised")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))