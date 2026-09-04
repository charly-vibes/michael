#!/usr/bin/env python3
"""Benchmark baselines: Solarized and Flexoki with conventional token mappings.

These are rendered through the same corpus, font, and weight/style grammar as
michael, so the only variable is lightness design. For baselines we emit the
AUTHENTIC color render plus a LUMINANCE-PRESERVING GRAYSCALE conversion —
which is exactly what a grayscale-forced display does to a color theme
(relative luminance, hence WCAG contrast, is preserved; hue is destroyed).

Token mappings follow each theme's canonical editor-theme conventions.
Weight/style match michael's grammar (keyword bold, comments italic) so the
comparison isolates lightness design as the only variable.
"""

# -- palette definitions -------------------------------------------------------

SOLARIZED = {
    'base03': '#002b36', 'base02': '#073642', 'base01': '#586e75',
    'base00': '#657b83', 'base0': '#839496', 'base1': '#93a1a1',
    'base2': '#eee8d5', 'base3': '#fdf6e3',
    'yellow': '#b58900', 'orange': '#cb4b16', 'red': '#dc322f',
    'magenta': '#d33682', 'violet': '#6c71c4', 'blue': '#268bd2',
    'cyan': '#2aa198', 'green': '#859900',
}

FLEXOKI = {
    # grays
    'black': '#100f0f', 'near-black': '#343331', 'gray-2': '#6f6e69',
    'gray-1': '#9c9c97', 'paper-1': '#cecdc3', 'white': '#fffcf0',
    # accents: (light, dark)
    'red': ('#af3029', '#d14d41'), 'orange': ('#bc5215', '#da702c'),
    'yellow': ('#ad8301', '#d0a215'), 'green': ('#66800b', '#879a39'),
    'cyan': ('#24837b', '#3aa99f'), 'blue': ('#205ea6', '#4385be'),
    'purple': ('#5e409d', '#8b7ec8'), 'magenta': ('#a02f6f', '#d5477e'),
}

def _fk(name, variant):
    """Flexoki accent by name and variant."""
    return FLEXOKI[name][0 if variant == 'light' else 1]

# token kind -> (fg, bold, italic). kind None (plain names/variables) = 'default'.

SOLARIZED_MAP = {
    'keyword':      ('blue', True, False),
    'type':         ('yellow', False, False),
    'functionDef':  ('blue', False, False),
    'functionCall': ('blue', False, False),
    'variable':     ('base0', False, False),
    'parameter':    ('base0', False, True),
    'decorator':    ('orange', False, False),
    'number':       ('cyan', False, False),
    'constant':     ('orange', False, False),
    'string':       ('cyan', False, False),
    'stringEscape': ('cyan', False, False),
    'docComment':   ('base01', False, True),
    'comment':      ('base01', False, True),
    'operator':     ('base0', False, False),
    'punctuation':  ('base01', False, False),
}

FLEXOKI_MAP = {
    'keyword':      ('red', True, False),
    'type':         ('blue', False, False),
    'functionDef':  ('orange', False, False),
    'functionCall': ('orange', False, False),
    'variable':     ('near-black', False, False),   # (light) / gray handled below
    'parameter':    ('near-black', False, True),
    'decorator':    ('purple', False, False),
    'number':       ('purple', False, False),
    'constant':     ('purple', False, False),
    'string':       ('green', False, False),
    'stringEscape': ('green', False, False),
    'docComment':   ('gray-2', False, True),
    'comment':      ('gray-2', False, True),
    'operator':     ('near-black', False, False),
    'punctuation':  ('gray-2', False, False),
}


def build_baselines():
    """Return {name: {bg, gutter, default, tokens, ansi16, grayscale}}.

    ansi16 = canonical terminal palette (used by the console-session corpus).
    For Solarized these are the official X-resource values; Flexoki's spec maps
    accents to both normal and bright slots (bold carries the emphasis).
    Colors are NOT pre-grayscaled here; render.py applies luminance-preserving
    grayscale to baseline themes (flag) to simulate the user's forced displays.
    """
    themes = {}

    def mk(name, bg, gutter, default, token_map, palette, variant):
        tokens = {}
        for kind, (key, bold, italic) in token_map.items():
            c = palette[key]
            if isinstance(c, tuple):  # flexoki accents
                c = c[0 if variant == 'light' else 1]
            tokens[kind] = (c, bold, italic)
        return {'name': name, 'bg': bg, 'gutter': gutter, 'default': default,
                'tokens': tokens, 'ansi16': ANSI16[name], 'grayscale': True}

    # Solarized: light bg=base3 fg=base00; dark bg=base03 fg=base0
    themes['solarized-light'] = mk(
        'solarized-light', SOLARIZED['base3'], SOLARIZED['base1'],
        SOLARIZED['base00'], SOLARIZED_MAP, SOLARIZED, 'light')
    themes['solarized-dark'] = mk(
        'solarized-dark', SOLARIZED['base03'], SOLARIZED['base01'],
        SOLARIZED['base0'], SOLARIZED_MAP, SOLARIZED, 'dark')

    # Flexoki: light bg=white fg=black; dark bg=black fg=paper-1
    themes['flexoki-light'] = mk(
        'flexoki-light', FLEXOKI['white'], FLEXOKI['gray-1'],
        FLEXOKI['black'], FLEXOKI_MAP, FLEXOKI, 'light')
    themes['flexoki-dark'] = mk(
        'flexoki-dark', FLEXOKI['black'], FLEXOKI['gray-2'],
        FLEXOKI['paper-1'], FLEXOKI_MAP, FLEXOKI, 'dark')

    return themes


# Canonical ANSI-16 palettes (console-session corpus). Solarized = official
# X-resource values. Flexoki = accents for both normal and bright (the spec
# relies on bold for emphasis); grays for black/white.
_ANSI = lambda slots: [c for c in slots]
SOLARIZED_ANSI = {
    'light': _ANSI(['#073642', '#dc322f', '#859900', '#b58900',
                    '#268bd2', '#d33682', '#2aa198', '#eee8d5',
                    '#002b36', '#cb4b16', '#586e75', '#657b83',
                    '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']),
    'dark': _ANSI(['#073642', '#dc322f', '#859900', '#b58900',
                   '#268bd2', '#d33682', '#2aa198', '#eee8d5',
                   '#002b36', '#cb4b16', '#586e75', '#657b83',
                   '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']),
}
_FLEXOKI_ACCENTS = ['#d14d41', '#879a39', '#d0a215', '#4385be', '#d5477e', '#3aa99f']
FLEXOKI_ANSI = {
    'dark': _ANSI(['#100f0f', *_FLEXOKI_ACCENTS, '#cecdc3',
                   '#343331', *_FLEXOKI_ACCENTS, '#cecdc3']),
    'light': _ANSI(['#100f0f', '#af3029', '#66800b', '#ad8301', '#205ea6', '#a02f6f', '#24837b', '#cecdc3',
                    '#343331', '#af3029', '#66800b', '#ad8301', '#205ea6', '#a02f6f', '#24837b', '#100f0f']),
}
ANSI16 = {
    'solarized-light': SOLARIZED_ANSI['light'],
    'solarized-dark': SOLARIZED_ANSI['dark'],
    'flexoki-light': FLEXOKI_ANSI['light'],
    'flexoki-dark': FLEXOKI_ANSI['dark'],
}
