*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wave`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Empty audio writes do not lock channel parameters

Target: `wave.Wave_write.setnchannels`

Property: For a writer backed by io.BytesIO with valid PCM parameters, after a successful writeframes(b'') or writeframesraw(b''), calling setnchannels with a different valid channel count must raise wave.Error.

### Draft issue: wave: Reject parameter changes after empty frame writes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `wave`

**Documented behaviour:** The wave documentation, under Wave_write objects, states: "Note that it is invalid to set any parameters after calling writeframes() or writeframesraw(), and any attempt to do so will raise wave.Error."

**Expected:** setnchannels(2) raises wave.Error after a successful writeframes(b'') or writeframesraw(b'').

**Actual:** After writeframes(b''), setnchannels(2) succeeds without an exception.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'channels': 1, 'sample_width': 1, 'frame_rate': 8000, 'method': 'writeframes', 'data': b'', 'new_channels': 2} actual: no exception expected: raises wave.Error
```

Judge: BUG (medium) -- The reproducer uses valid PCM parameters and successfully calls writeframes(b''). The documentation explicitly prohibits parameter changes after either write method, without excluding empty writes. Empty writes emit the header but leave _datawritten at zero, so setnchannels permits changes that can disagree with the already-written header. The upstream diff does not fix this guard, and the listed issue is unrelated.

