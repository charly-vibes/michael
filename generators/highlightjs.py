#!/usr/bin/env python3
"""Generate highlight.js theme CSS for both variants.

A highlight.js theme is pure CSS keyed on .hljs-* classes — a natural
extension of michael's grammar into the web world (blogs, docs sites).
Emits:
  out/highlightjs/michael-light.css / michael-dark.css   (standard, single-scope)
  site/assets/michael-hljs.css                            (both variants,
    scoped under [data-michael="light|dark"] for the showcase site)

Grammar mapping (tokens.json -> hljs classes):
  ink+bold     -> keywords            ink       -> types, tags
  strong+bold  -> function titles     strong    -> builtins
  fg           -> variables, attrs    fg+bold   -> numbers, literals
  muted        -> strings, subst      fg+italic -> parameters
  strong+italic-> meta/decorators     faint+italic -> comments
  faint        -> punctuation         muted     -> operators
"""
import json
import os

HLJS_MAP = {
    'keyword':        ('keyword', 'hljs-keyword, .hljs-selector-tag, .hljs-doctag'),
    'type':           ('type', '.hljs-type, .hljs-title.class_, .hljs-name, .hljs-tag'),
    'functionDef':    ('functionDef', '.hljs-title, .hljs-title.function_'),
    'functionCall':   ('functionCall', '.hljs-built_in, .hljs-title.class_.inherited__'),
    'variable':       ('variable', '.hljs-variable, .hljs-attr, .hljs-attribute, .hljs-property'),
    'parameter':      ('parameter', '.hljs-params, .hljs-symbol'),
    'decorator':      ('decorator', '.hljs-meta, .hljs-meta .hljs-keyword, .hljs-addition'),
    'number':         ('number', '.hljs-number, .hljs-literal, .hljs-selector-id, .hljs-template-variable'),
    'constant':       ('constant', '.hljs-constant'),
    'string':         ('string', '.hljs-string, .hljs-regexp, .hljs-subst'),
    'comment':        ('comment', '.hljs-comment, .hljs-quote, .hljs-deletion'),
    'operator':       ('operator', '.hljs-operator'),
    'punctuation':    ('punctuation', '.hljs-punctuation'),
}


def css_for(variant, v, scope=''):
    g = lambda role: v[role]['hex']
    rules = []

    def emit(sel, color, weight=None, style=None):
        props = [f'color: {color}']
        if weight: props.append(f'font-weight: {weight}')
        if style: props.append(f'font-style: {style}')
        selectors = [f'{scope} .{c.strip().lstrip(".")}' for c in sel.split(',')]
        joined = ', '.join(selectors)
        rules.append(f'{joined} {{ {"; ".join(props)}; }}')

    # base block: bg + default fg; display:block so the background fills the
    # panel even when .hljs sits on an inline <code> element inside <pre>
    base_sels = [f'{scope} .hljs'] if scope else ['.hljs']
    rules.append(
        f"{', '.join(base_sels)} {{ background: {g('bg')}; color: {g('fg')}; display: block; overflow-x: auto; }}"
    )
    for kind, sel in HLJS_MAP.values():
        tok = tok_by_key(kind)
        if tok:
            emit(sel, v[tok['level']]['hex'],
                 '700' if tok.get('weight') == 'bold' else None,
                 'italic' if tok.get('style') == 'italic' else None)
    # hljs's own emphasis classes follow the grammar
    rules.append(f"{scope} .hljs-emphasis {{ font-style: italic; color: {g('fg')}; }}".strip())
    rules.append(f"{scope} .hljs-strong {{ font-weight: 700; color: {g('ink')}; }}".strip())
    return '\n'.join(rules) + '\n'


_TOK = None
def tok_by_key(key):
    global _TOK
    if _TOK is None:
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, '..', 'tokens.json')) as fh:
            _TOK = json.load(fh)['code']
    return _TOK.get(key)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(here, '..')
    with open(os.path.join(root, 'ramp.json')) as fh:
        ramp = json.load(fh)
    out = os.path.join(root, 'out', 'highlightjs')
    os.makedirs(out, exist_ok=True)

    base_css = "/* michael — highlight.js theme. Generated; grammar in tokens.json. */\n"
    for name in ('light', 'dark'):
        body = css_for(name, ramp['variants'][name])
        path = os.path.join(out, f'michael-{name}.css')
        with open(path, 'w') as fh:
            fh.write(base_css + body + '\n')
        print(f"wrote {path}")

    # site bundle: both variants scoped by data-michael attribute
    dual = (
        base_css
        + css_for('light', ramp['variants']['light'], scope='[data-michael="light"]') + '\n\n'
        + css_for('dark', ramp['variants']['dark'], scope='[data-michael="dark"]') + '\n'
    )
    site_path = os.path.join(root, 'site', 'assets', 'michael-hljs.css')
    with open(site_path, 'w') as fh:
        fh.write(dual)
    print(f"wrote {site_path}")

    print("""
Usage (self-hosted):
  <link rel="stylesheet" href="michael-dark.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/default.min.css">
  <pre><code class="language-python">...</code></pre>
  <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
  (our CSS must load AFTER the default theme to win the cascade)
""")


if __name__ == '__main__':
    main()
