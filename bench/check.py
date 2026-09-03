#!/usr/bin/env python3
"""michael benchmark gates. Fails (exit 1) on any violation.

Gates:
  1. WCAG contrast floors vs bg:  ink>=10, strong>=10, fg>=7, muted>=4.5, faint>=3
  2. dL >= 0.10 OKLCH between adjacent text levels
  3. Text-on-overlay: ink/strong/fg vs selectionFill >= 4.5, muted >= 3.0
  4. 4-bit (16-gray) quantization survival: text levels stay pairwise distinct,
     bg stays distinct from every text level and from selectionFill
  5. Selection fill must be visible: distinct from bg after quantization
"""
import json, sys, os

def lum(h):
    v = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    v = [u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4 for u in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]

def cr(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def quant4(h):  # simulate 4-bit e-ink: 16 evenly spaced grays
    return '#%02X%02X%02X' % tuple(round(int(h[i:i+2], 16) / 17) * 17 for i in (1, 3, 5))

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ramp = json.load(open(os.path.join(here, '..', 'ramp.json')))
    failures = []

    floors = {'ink': 10, 'strong': 10, 'fg': 7, 'muted': 4.5, 'faint': 3}
    overlay_floors = {'ink': 4.5, 'strong': 4.5, 'fg': 4.5, 'muted': 3.0}
    levels = ['ink', 'strong', 'fg', 'muted', 'faint']

    for vname, v in ramp['variants'].items():
        bg, sel = v['bg']['hex'], v['selectionFill']['hex']
        text = {k: v[k]['hex'] for k in levels}

        # Gate 1: contrast floors
        for k, need in floors.items():
            r = cr(text[k], bg)
            status = 'OK' if r >= floors[k] else 'FAIL'
            print(f"[{vname}] {k:6s} {text[k]} vs bg {bg}: {r:5.2f}:1 (need {floors[k]}) {status}")
            if r < floors[k]:
                failures.append(f"{vname}: {k} contrast {r:.2f} < {floors[k]}")

        # Gate 2: dL between adjacent text levels
        Ls = sorted(v[k]['L'] for k in levels)
        gaps = [b - a for a, b in zip(Ls, Ls[1:])]
        status = 'OK' if min(gaps) >= 0.10 - 1e-9 else 'FAIL'
        print(f"[{vname}] dL gaps: {['%.3f' % g for g in gaps]} {status}")
        if min(gaps) < 0.10 - 1e-9:
            failures.append(f"{vname}: dL gap {min(gaps):.3f} < 0.10")

        # Gate 3: text on selection
        for k, need in overlay_floors.items():
            r = cr(text[k], sel)
            status = 'OK' if r >= need else 'FAIL'
            print(f"[{vname}] {k:6s} on selection {r:5.2f}:1 (need {need}) {status}")
            if r < need:
                failures.append(f"{vname}: {k} on selection {r:.2f} < {need}")

        # Gate 4+5: 4-bit quantization survival
        qt = {k: quant4(text[k]) for k in levels}
        if len(set(qt.values())) != 5:
            failures.append(f"{vname}: text levels collide after 4-bit quantization")
        for k in levels:
            if qt[k] == quant4(bg):
                failures.append(f"{vname}: {k} indistinguishable from bg at 4-bit")
        if quant4(sel) == quant4(bg):
            failures.append(f"{vname}: selection fill invisible at 4-bit")
        print(f"[{vname}] 4-bit: bg={quant4(bg)} sel={quant4(sel)} text={[qt[k] for k in levels]} "
              f"{'OK' if not any('4-bit' in f or 'invisible' in f for f in failures) else 'FAIL'}")

    print()
    if failures:
        print(f"GATES FAILED ({len(failures)}):")
        for f in failures: print(f"  - {f}")
        sys.exit(1)
    print("ALL GATES PASSED")

if __name__ == '__main__':
    main()
