#!/usr/bin/env python3
"""Generate GNOME Terminal profile (dconf) for both variants."""
import json, os

def load():
    here = os.path.dirname(os.path.abspath(__file__))
    ramp = json.load(open(os.path.join(here, '..', 'ramp.json')))
    tokens = json.load(open(os.path.join(here, '..', 'tokens.json')))
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
        "[profiles:/:michael-%s]" % variant_name,
        "visible-name='michael %s'" % variant_name,
        "background-color='%s'" % bg,
        "foreground-color='%s'" % fg,
        "use-theme-colors=false",
        "cursor-background-color='%s'" % fg,
        "cursor-foreground-color='%s'" % bg,
        "cursor-blink-mode='off'",      # e-ink ghosting
        "cursor-shape='ibeam'",          # bar cursor, not block
        "bold-is-bright=true",           # weight channel doubles as level channel
        "scrollbar-policy='never'",
        "palette=[%s]" % ", ".join(f"'{c}'" for c in pal),
    ]
    return "\n".join(lines) + "\n"

if __name__ == '__main__':
    ramp, _ = load()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'gnome-terminal')
    os.makedirs(out, exist_ok=True)
    for name in ('light', 'dark'):
        path = os.path.join(out, f'michael-{name}.dconf')
        open(path, 'w').write(emit(name, ramp['variants'][name]))
        print(f"wrote {path}")
