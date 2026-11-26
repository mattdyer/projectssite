# Music Visualizer — Issues

**Status: ALL FIXED** (2026-11-26)

## 0. ✅ Syntax error in template literal (HIGH)
`infoEl.textContent = `${mode} · ${Math.round(sensitivity*10)/10}× sens · ${(Math.round(t/1000)}s`;` — the `(` in `${(Math.round(t/1000)}` is never closed. This is a pre-existing syntax error that prevents the entire script from running.

## 1. ✅ `getVolume()` returns wrong scale (HIGH)
`avg(dataArray) / 255` — time-domain data is centered around 128, so this returns ~0.5 always. Volume bar always shows ~50%+ height. Should be `(avg(dataArray) - 128) / 128` clamped to [0, 1].

## 2. ✅ `getFreqRange()` calls `getByteFrequencyData` on every invocation (HIGH)
`getFreqRange` calls `analyser.getByteFrequencyData(freqData)` every time it's called. In `drawWaves`, it's called once per pixel column (W times per frame). Should fetch frequency data once per frame and slice from it.

## 3. ✅ `drawWaves` calls `getFreqRange` inside the x loop (HIGH)
`const freq = getFreqRange(x / W, (x + 2) / W) * sensitivity;` — called for every pixel column. Should be hoisted out of the loop or replaced with a direct slice of pre-fetched data.

## 4. ✅ `avg()` returns NaN for empty arrays (MEDIUM)
`arr.reduce((a,b)=>a+b,0)/arr.length` — if `slice` is empty (e.g. `getFreqRange(0.99, 1.0)`), returns NaN. Should return 0 for empty arrays.

## 5. ✅ `hexToRgb()` doesn't handle invalid hex (LOW)
`parseInt(hex.slice(1,3),16)` returns NaN for invalid hex. Should validate and return [0,0,0] or similar.

## 6. ✅ Dead code: unused `bass`, `vol`, `[r,g,b]` in draw functions (LOW)
`drawBars` computes `bass`, `vol`, `[r,g,b]` but never uses them. `drawCircles` computes `[r,g,b]` but never uses it. `drawRays` computes `[r,g,b]` but never uses it. `drawParticles` computes `[r,g,b]` but never uses it. `drawWaves` computes `vol` and `[r,g,b]` but never uses them.

## 7. ✅ `initStars()` re-randomizes stars on every resize (LOW)
`resize()` calls `initStars()` which re-creates all stars with new random positions. Stars jump on every resize. Should preserve stars or only init once.

## 8. ✅ `getVolume()` called redundantly in `loop()` and `drawWaves` (LOW)
`loop()` calls `getVolume()` for the volume bar, and `drawWaves` also calls `getVolume()`. Both call `analyser.getByteTimeDomainData(dataArray)`. Should fetch once per frame.

## 9. ✅ `drawWaves` calls `getByteTimeDomainData` twice (LOW)
`drawWaves` calls `analyser.getByteTimeDomainData(dataArray)` at the start, then `getVolume()` calls it again. Should fetch once.

## 10. ✅ `getFreqRange` slices `freqData` but `freqData` is a Uint8Array (LOW)
`freqData.slice(...)` on a Uint8Array returns a Uint8Array, which is fine, but `avg()` iterates it — this is correct but the slice is created every call. Should slice from a pre-fetched array.

## 11. ✅ `particles` not cleared when switching away from particles mode (LOW)
`particles` is cleared when switching TO particles mode, but not when switching away. Not a bug per se (only used in drawParticles), but wasteful.

## 12. ✅ `resize()` doesn't handle zero-size canvas (LOW)
`resize()` sets `W = canvas.width = window.innerWidth` — if the window is minimized, W could be 0. Should guard against zero-size.
