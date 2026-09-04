#!/usr/bin/env python3
"""Shared ANSI 16-slot role map for michael + console-session rendering.

Slot design for grayscale console work (bold-is-bright doubles each slot):
normal slots carry "at rest" levels; bright slots pop. Hue families that
co-occur in real console output land on DIFFERENT levels:

  git status:  modified(yellow=3 muted) vs deleted(red=1 strong) vs staged(green=2 fg)
  ls -l:       dirs(blue=4 strong, bold->12 ink) vs executables(green=2 fg bold->10 ink)
  grep match:  bold red 1 -> bright 9 ink (hard pop)
  diff:        removed(red=1) vs added(green=2)  -- distinct
  dim text:    0/8 faint (whitespace, comments in vim, progress bars)

Known trade-off: red(1) and blue(4) share the strong level; they rarely carry
adjacent semantics in the same listing (errors vs dirs), but ls archives(red)
vs dirs(blue) do co-occur — disambiguated by suffix/name in practice.
"""

# (normal role, bright role) per hue family 0-7
SLOT_MAP = [
    ('faint',  'faint'),   # 0/8  black
    ('strong', 'ink'),     # 1/9  red:    errors, removed, grep matches
    ('fg',     'ink'),     # 2/10 green:  success, added, executables
    ('muted',  'strong'),  # 3/11 yellow: warnings, modified
    ('strong', 'ink'),     # 4/12 blue:   dirs, links, info
    ('muted',  'strong'),  # 5/13 magenta: branches, special
    ('fg',     'muted'),   # 6/14 cyan:   paths, code
    ('fg',     'ink'),     # 7/15 white:  near-default text
]


def ansi16(ramp_variant):
    """michael ramp variant dict -> 16 hex colors in slot order."""
    g = lambda role: ramp_variant[role]['hex']
    return [g(normal) for normal, _ in SLOT_MAP] + \
           [g(bright) for _, bright in SLOT_MAP]
