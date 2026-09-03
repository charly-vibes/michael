#!/usr/bin/env python3
"""Generate VS Code JSON themes (light/dark) for michael."""
import json, os

def load():
    here = os.path.dirname(os.path.abspath(__file__))
    ramp = json.load(open(os.path.join(here, '..', 'ramp.json')))
    tokens = json.load(open(os.path.join(here, '..', 'tokens.json')))
    return ramp, tokens

def to_scope_entry(tok, v):
    """tokens entry -> {foreground, fontStyle}"""
    fg = v[tok['level']]['hex']
    styles = []
    if tok.get('weight') == 'bold': styles.append('bold')
    if tok.get('style') == 'italic': styles.append('italic')
    return {'foreground': fg, 'fontStyle': ' '.join(styles)}

SCOPES = {
    'keyword':      ['keyword.control', 'keyword.operator.new', 'storage.type', 'storage.modifier', 'keyword'],
    'type':         ['entity.name.type', 'entity.name.class', 'support.type', 'support.class'],
    'functionDef':  ['entity.name.function.definition'],
    'functionCall': ['entity.name.function', 'support.function', 'meta.function-call'],
    'variable':     ['variable', 'variable.other'],
    'parameter':    ['variable.parameter'],
    'decorator':    ['meta.decorator', 'entity.other.attribute-name', 'meta.attribute'],
    'number':       ['constant.numeric'],
    'constant':     ['constant.language'],
    'string':       ['string'],
    'stringEscape': ['constant.character.escape'],
    'docComment':   ['comment.block.documentation'],
    'comment':      ['comment'],
    'operator':     ['keyword.operator'],
    'punctuation':  ['punctuation', 'meta.brace'],
}

def emit(variant, v, tokens):
    g = lambda role: v[role]['hex']
    bg, bgAlt, sel = g('bg'), g('bgAlt'), g('selectionFill')
    ink, strong, fg, muted, faint = (g('ink'), g('strong'), g('fg'), g('muted'), g('faint'))
    theme = {
        'name': f'michael {variant}',
        'type': variant,
        'colors': {
            'editor.background': bg,
            'editor.foreground': fg,
            'editor.lineHighlightBackground': bgAlt,
            'editor.selectionBackground': sel,
            'editorCursor.foreground': ink,
            'editorLineNumber.foreground': faint,
            'editorLineNumber.activeForeground': muted,
            'editorIndentGuide.background1': faint,
            'editorIndentGuide.activeBackground1': muted,
            'editorBracketMatch.border': fg,      # outline-only brace match
            'editorBracketMatch.background': bg,  # no fill behind glyphs
            'editorWidget.background': bgAlt,
            'statusBar.background': bgAlt,
            'statusBar.foreground': fg,
            # diff: direction carried by gutter signs; faint fill secondary
            'diffEditor.insertedLineBackground': bgAlt,
            'diffEditor.removedLineBackground': bgAlt,
            'editorGutter.addedBackground': muted,
            'editorGutter.deletedBackground': muted,
            'editorGutter.modifiedBackground': muted,
            # bracket nesting = depth-mapped lightness, not hue cycling
            'editorBracketHighlight.foreground1': faint,
            'editorBracketHighlight.foreground2': fg,
            'editorBracketHighlight.foreground3': strong,
            'editorBracketHighlight.foreground4': faint,
            'editorBracketHighlight.foreground5': fg,
            'editorBracketHighlight.foreground6': strong,
            # diagnostics: underline pattern colors
            'editorError.foreground': ink,
            'editorWarning.foreground': strong,
            'editorInfo.foreground': muted,
        },
        'tokenColors': [
            {'scope': scopes, 'settings': to_scope_entry(tokens['code'][key], v)}
            for key, scopes in SCOPES.items()
        ],
    }
    return json.dumps(theme, indent=2) + '\n'

if __name__ == '__main__':
    ramp, tokens = load()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'vscode')
    os.makedirs(out, exist_ok=True)
    for name in ('light', 'dark'):
        path = os.path.join(out, f'michael-{name}-color-theme.json')
        open(path, 'w').write(emit(name, ramp['variants'][name], tokens))
        print(f"wrote {path}")
