# Fractal Explorer — Issues

**Status: ALL FIXED** (2026-11-25)

Review of `docs/fractal-explorer/index.html` (643 lines).

## 1. ✅ Race condition: canvas can go stale (HIGH)

`renderFractal()` early-returns when `rendering` is true (line 277), leaving `needsRender` true but no rAF pending.

Trace:
- `scheduleRender()` sets `needsRender = true` and schedules rAF#1.
- rAF#1 fires → `renderFractal()` → `rendering = true`, `needsRender = false`, computes, `createImageBitmap` starts (async).
- User drags → `scheduleRender()` → `needsRender = true`, rAF#2 scheduled.
- rAF#2 fires → `renderFractal()` → `rendering` is true → **return early**. `needsRender` stays true.
- `bitmap.then` fires → `rendering = false`; `needsRender` is true → `scheduleRender()` → `needsRender` is already true → **does nothing**.
- Result: no render happens; canvas is stale.

Fix: in the early return, set `needsRender = true` (or don't early-return). Also make `scheduleRender()` re-schedule even when `needsRender` is true but no rAF is pending.

## 2. ✅ Smooth coloring formula is wrong (MEDIUM)

Line 350 / 380:
```js
const smoothIter = iter + 1 - Math.log(Math.log(Math.sqrt(zr*zr + zi*zi))) / Math.log(2);
```
`Math.sqrt(zr*zr + zi*zi)` is `|z|`, so `Math.log(Math.sqrt(|z|^2))` = `0.5 * Math.log(|z|^2)`. The standard formula is `Math.log(Math.log(zr*zr + zi*zi))`. The current formula is off by a constant and can produce negative/NaN `smoothIter` for points near the boundary, yielding black pixels.

Fix:
```js
const smoothIter = iter + 1 - Math.log(Math.log(zr*zr + zi*zi)) / Math.log(2);
```

## 3. ✅ `pi` can be negative or out of range (MEDIUM)

Line 352 / 382:
```js
const pi = Math.floor(t * mi) % mi;
```
`t = smoothIter / mi`, so `t * mi = smoothIter`. If `smoothIter` is negative (possible for Julia points with `|z|^2` close to 1), `pi` is negative → `paletteLUT[negative]` is `undefined` → `data[idx] = undefined` → 0 (black).

Fix: clamp `pi` to `[0, mi-1]`:
```js
const pi = Math.max(0, Math.min(mi - 1, Math.floor(smoothIter) % mi));
```

## 4. ✅ Zoom slider range is wrong (LOW)

Line 170: `<input type="range" id="zoomDisplay" min="0" max="8" value="0" step="0.01">`.

`view.zoom` can be < 1 (e.g., 0.5 → `log10(0.5)` = -0.3, below min 0). The slider clamps to 0, so the displayed value doesn't match the actual zoom.

Fix: set `min="-2"` (or `-1`) and `max="10"`, or clamp `updateZoomDisplay()` to the slider range.

## 5. ✅ `updateZoomDisplay()` doesn't clamp (LOW)

Line 443: `zoomDisplay.value = Math.log10(view.zoom);` — if `view.zoom` is < 1, `log10` is negative, slider clamps to 0, but `view.zoom` stays. The slider and view get out of sync.

Fix: clamp the value to the slider's min/max, or set the slider min to a negative value.

## 6. ✅ Touch double-tap zoom doesn't keep the tap point fixed (LOW)

Line 578-582: double-tap zooms in by 2 but doesn't update `cx`/`cy` to keep the tap point fixed. The view jumps.

Fix: compute the complex point under the tap and adjust `cx`/`cy` like the wheel handler does.

## 7. ✅ `lastTap` is set even on single taps (LOW)

Line 583: `lastTap = now;` is set unconditionally, so a third tap within 300ms of a double-tap triggers another zoom. Minor.

Fix: only set `lastTap` when the double-tap check fails, or reset it after a double-tap.

## 8. ✅ `screenshotBtn` uses `canvas.toDataURL` which can fail (LOW)

Line 633: `canvas.toDataURL('image/png')` — if the canvas is tainted (e.g., by an external image), this throws. Currently the canvas is only drawn from `ImageData`, so it's safe, but the error is unhandled.

Fix: wrap in try/catch and show an error message.

## 9. ✅ `resize()` doesn't re-render on DPR change (LOW)

Line 268-274: `resize()` sets canvas dimensions and calls `scheduleRender()`. But `window.resize` doesn't fire on DPR change (e.g., moving between monitors). Minor.

Fix: also listen to `matchMedia('(resolution: ...)')` or `ResizeObserver`.

## 10. ✅ `hslToRgb` can produce out-of-range values (LOW)

Line 248-265: `hslToRgb` can produce values outside [0, 255] for some `h` values. The `hue2rgb` function doesn't clamp.

Fix: clamp the output to [0, 255].

## 11. ✅ `palettes.electric` can produce out-of-range values (LOW)

Line 213-218: `Math.sin(t * 0.4 + 0.0) * 0.5 + 0.5` can be slightly negative or > 1 due to floating point, producing values outside [0, 255].

Fix: clamp the output to [0, 255].

## 12. ✅ `palettes.neon` can produce out-of-range values (LOW)

Line 236-241: `Math.sin(t * 3.0) * 127 + 128` can be slightly negative or > 255 due to floating point.

Fix: clamp the output to [0, 255].
