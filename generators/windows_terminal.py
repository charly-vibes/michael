#!/usr/bin/env python3
"""Generate Windows Terminal color schemes (JSON fragments) for both variants.

Emission: out/windows-terminal/michael-schemes.json — an array of two scheme
objects. Users paste the objects into the "schemes" array of their
settings.json and reference them by name in a profile.

Windows Terminal has no per-profile bold-is-bright swap: the 16 slots stand
alone. We map the same console roles as bench/ansi.py, using bright slots
for emphasis so critical output stays distinguishable.
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'bench'))
from ansi import SLOT_MAP as PALETTE_MAP

WT_KEYS = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white',
           'brightBlack', 'brightRed', 'brightGreen', 'brightYellow',
           'brightBlue', 'brightPurple', 'brightCyan', 'brightWhite']


def scheme(variant_name, v):
    g = lambda role: v[role]['hex']
    colors = {}
    for i, key in enumerate(WT_KEYS):
        normal, bright = PALETTE_MAP[i % 8]
        colors[key] = g(bright if i >= 8 else normal)
    return {
        'name': f'michael {variant_name}',
        'background': g('bg'),
        'foreground': g('fg'),
        'cursorColor': g('ink'),
        'selectionBackground': g('selectionFill'),
        'selectionForeground': g('ink'),
        **colors,
    }


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '..', 'ramp.json')) as fh:
        ramp = json.load(fh)
    out = os.path.join(here, '..', 'out', 'windows-terminal')
    os.makedirs(out, exist_ok=True)

    schemes = [scheme('dark', ramp['variants']['dark']),
               scheme('light', ramp['variants']['light'])]
    path = os.path.join(out, 'michael-schemes.json')
    with open(path, 'w') as fh:
        json.dump(schemes, fh, indent=2)
        fh.write('\n')
    print(f"wrote {path}")

    snippet = {
        'name': 'michael dark',
        'colorScheme': 'michael dark',
        'cursorShape': 'bar',
        'cursorBlinkingEnabled': False,
    }
    print('\nProfile snippet (merge into settings.json -> profiles -> list):')
    print(json.dumps(snippet, indent=2))
    print('\nThen set "defaults": { "colorScheme": "michael dark" } or pick the scheme per profile.')


if __name__ == '__main__':
    main()
