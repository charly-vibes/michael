#!/usr/bin/env python3
"""Generate Ghostty theme files for both variants.

Emits out/ghostty/michael-light and out/ghostty/michael-dark — drop them in
~/.config/ghostty/themes/ and set:

    theme = light:michael-light,dark:michael-dark

(plus the recommended cursor lines from the printed snippet).
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'bench'))


def theme_file(variant_name, v):
    g = lambda role: v[role]['hex']
    lines = [
        f"palette = {g('faint')}",    # 0  black
        f"palette = {g('strong')}",   # 1  red
        f"palette = {g('fg')}",       # 2  green
        f"palette = {g('muted')}",    # 3  yellow
        f"palette = {g('strong')}",   # 4  blue
        f"palette = {g('muted')}",    # 5  magenta
        f"palette = {g('fg')}",       # 6  cyan
        f"palette = {g('ink')}",      # 7  white
        f"palette = {g('faint')}",    # 8  bright black
        f"palette = {g('ink')}",      # 9  bright red
        f"palette = {g('ink')}",      # 10 bright green
        f"palette = {g('strong')}",   # 11 bright yellow
        f"palette = {g('ink')}",      # 12 bright blue
        f"palette = {g('strong')}",   # 13 bright magenta
        f"palette = {g('muted')}",    # 14 bright cyan
        f"palette = {g('ink')}",      # 15 bright white
        '',
        f'background = {g("bg")}',
        f'foreground = {g("fg")}',
        f'cursor-color = {g("ink")}',
        f'selection-background = {g("selectionFill")}',
        f'selection-foreground = {g("ink")}',
    ]
    return '\n'.join(lines) + '\n'


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '..', 'ramp.json')) as fh:
        ramp = json.load(fh)
    out = os.path.join(here, '..', 'out', 'ghostty')
    os.makedirs(out, exist_ok=True)

    for name in ('light', 'dark'):
        path = os.path.join(out, f'michael-{name}')
        with open(path, 'w') as fh:
            fh.write(theme_file(name, ramp['variants'][name]))
        print(f"wrote {path}")

    print("""
Install:
  mkdir -p ~/.config/ghostty/themes
  cp out/ghostty/michael-* ~/.config/ghostty/themes/

Config (~/.config/ghostty/config):
  theme = light:michael-light,dark:michael-dark
  cursor-style = bar
  cursor-style-blink = false
""")


if __name__ == '__main__':
    main()
