#!/usr/bin/env python3
"""Generate GNOME Terminal profile (dconf) for both variants."""
import json
import os


def load():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, '..', 'ramp.json')) as fh:
        ramp = json.load(fh)
    with open(os.path.join(here, '..', 'tokens.json')) as fh:
        tokens = json.load(fh)
    return ramp, tokens

# ANSI slot assignment: 16 slots from the ramp + weight multiplexing via bright.
# ramp-level mapping, shared by both variants (roles flip polarity):
#   black=b(faint), red=muted, green=fg, yellow=muted(bold-slot), blue=fg(bold-slot),
#   magenta=strong, cyan=muted(bold-slot), white=ink,
#   bright* = one tier stronger equivalents
def palette(v):
    g = lambda role: v[role]['hex']
    return [
        g('faint'),   # 0 black (punctuation/linenumbers)
        g('muted'),   # 1 red  -> used sparingly (diff signs)
        g('fg'),      # 2 green -> variables
        g('muted'),   # 3 yellow -> strings (bold flag distinguishes)
        g('fg'),      # 4 blue  -> function calls (bold flag -> strong)
        g('strong'),  # 5 magenta -> types/keywords
        g('muted'),   # 6 cyan  -> paths/dirs
        g('ink'),     # 7 white -> default text
        g('faint'),   # 8 bright black -> faint bg-ish text (bold suppresses)
        g('muted'),   # 9 bright red
        g('strong'),  # 10 bright green -> function defs (bold flag)
        g('muted'),   # 11 bright yellow
        g('strong'),  # 12 bright blue
        g('strong'),  # 13 bright magenta
        g('fg'),      # 14 bright cyan
        g('ink'),     # 15 bright white
    ]

def emit(variant_name, v):
    bg, fg = v['bg']['hex'], v['ink']['hex']
    pal = palette(v)
    lines = [
        f"# michael ({variant_name}) — generated, do not edit",
        "# Usage: dconf load /org/gnome/terminal/legacy/profiles:/ < this file",
        f"[profiles:/:michael-{variant_name}]",
        f"visible-name='michael {variant_name}'",
        f"background-color='{bg}'",
        f"foreground-color='{fg}'",
        "use-theme-colors=false",
        f"cursor-background-color='{fg}'",
        f"cursor-foreground-color='{bg}'",
        "cursor-blink-mode='off'",      # e-ink ghosting
        "cursor-shape='ibeam'",          # bar cursor, not block
        "bold-is-bright=true",           # weight channel doubles as level channel
        "scrollbar-policy='never'",
        "palette=[" + ", ".join(f"'{c}'" for c in pal) + "]",
    ]
    return "\n".join(lines) + "\n"

if __name__ == '__main__':
    ramp, _ = load()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'gnome-terminal')
    os.makedirs(out, exist_ok=True)
    for name in ('light', 'dark'):
        path = os.path.join(out, f'michael-{name}.dconf')
        with open(path, 'w') as fh:
            fh.write(emit(name, ramp['variants'][name]))
        print(f"wrote {path}")
