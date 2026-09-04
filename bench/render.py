#!/usr/bin/env python3
"""Render michael AND baseline themes (Solarized, Flexoki) onto real code, as PNGs.

Pipeline: source -> pygments lex -> token map -> drawn with JetBrains Mono
(real bold/italic faces) -> PNG. All themes share corpus, font, weight and
style grammar; the only variable is lightness design.

Variants per theme: full-fidelity PNG + 4-bit (16-gray) quantization (e-ink
floor test). Baselines additionally emit a LUMINANCE-PRESERVING GRAYSCALE
conversion - what a grayscale-forced display does to a color theme: relative
luminance (and therefore WCAG contrast) is kept, hue is destroyed.

Usage: uv run bench/render.py   (writes to corpus/render/)
"""
import json
import os

from ansi import ansi16 as ramp_ansi16
from baselines import build_baselines
from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
FONT_DIR = '/usr/share/fonts/jetbrains-mono-fonts'
FONTS = {
    (False, False): 'JetBrainsMono-Regular.otf',
    (True, False):  'JetBrainsMono-Bold.otf',
    (False, True):  'JetBrainsMono-Italic.otf',
    (True, True):   'JetBrainsMono-BoldItalic.otf',
}

# ---------------------------------------------------------------- corpus ---
CORPUS = {
    'python.py': ('python', '''\
from dataclasses import dataclass, field
import re

MAX_RETRIES: int = 3

@dataclass(frozen=True)
class Fetcher:
    """Fetches pages with retries and backoff."""
    base_url: str
    timeout: float = 5.0
    headers: dict[str, str] = field(default_factory=dict)

    async def fetch(self, path: str, session) -> str:
        url = f"{self.base_url}/{path.lstrip('/')}"
        for attempt in range(MAX_RETRIES):
            try:
                resp = await session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.text
            except ConnectionError as err:
                if attempt == MAX_RETRIES - 1:
                    raise RuntimeError(f"failed: {url}") from err
        # unreachable when MAX_RETRIES > 0
        return ""
'''),
    'julia.jl': ('julia', '''\
module Optics

export lensmaker

"""Thin-lens focal length via the lensmaker equation."""
function lensmaker(n::Float64, r1::Float64, r2::Float64; thick=0.0)
    inv_f = (n - 1) * (1/r1 - 1/r2 + (n-1)*thick/(n*r1*r2))
    return 1 / inv_f
end

struct Surface
    radius::Float64
    convex::Bool
end

function power(surfaces::Vector{Surface}, n::Float64)
    mapreduce(s -> (n - 1) / s.radius, +, surfaces; init=0.0)
end

end # module
'''),
    'rust.rs': ('rust', '''\
use std::collections::HashMap;
use std::fmt;

#[derive(Debug, Clone)]
pub enum Node {
    Leaf { value: i64 },
    Branch(Box<Node>, Box<Node>),
}

impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Node::Leaf { value } => write!(f, "{}", value),
            Node::Branch(l, r) => write!(f, "({} {})", l, r),
        }
    }
}

fn walk(node: &Node, depth: usize, out: &mut HashMap<usize, usize>) {
    match node {
        Node::Leaf { .. } => *out.entry(depth).or_insert(0) += 1,
        Node::Branch(l, r) => { walk(l, depth + 1, out); walk(r, depth + 1, out); }
    }
}
'''),
    'typescript.ts': ('typescript', '''\
export interface Options {
  retries?: number;
  baseUrl: string;
}

type Handler = (req: Request) => Promise<Response>;

const DEFAULT_TIMEOUT = 5_000;

export class Router {
  private routes = new Map<string, Handler>();

  add(path: string, handler: Handler): this {
    if (this.routes.has(path)) {
      throw new Error(`duplicate route: ${path}`);
    }
    this.routes.set(path, handler);
    return this;
  }

  async handle(req: Request): Promise<Response> {
    const handler = this.routes.get(new URL(req.url).pathname)
      ?? (() => new Response("not found", { status: 404 }));
    return handler(req);
  }
}
'''),
    'clojure.clj': ('clojure', '''\
(ns shop.cart
  "Shopping cart with line-item totals."
  (:require [clojure.spec.alpha :as s]))

(defonce ^:private registry (atom {}))

(s/def ::price pos?)
(s/def ::qty nat-int?)
(s/def ::line (s/keys :req [::price ::qty]))

(defn total
  "Sum of price*qty over lines, rounded to cents."
  [lines]
  (->> lines
       (filter #(s/valid? ::line %))
       (map (fn [{:keys [::price ::qty]}] (* price qty)))
       (reduce + 0.0)
       (as-> v (Math/round (* 100 v)))))

(defn register! [id lines]
  (swap! registry assoc id {:lines lines :total (total lines)}))
'''),
    'csharp.cs': ('csharp', '''\
using System;
using System.Collections.Generic;
using System.Linq;

namespace Shop;

public record Line(decimal Price, int Qty);

public sealed class Cart
{
    private static readonly decimal TaxRate = 0.19m;
    private readonly List<Line> _lines = new();

    public decimal Net => _lines.Sum(l => l.Price * l.Qty);

    public void Add(Line line) =>
        _lines.Add(line ?? throw new ArgumentNullException(nameof(line)));

    public decimal Gross() => decimal.Round(Net * (1 + TaxRate), 2);
}
'''),
}

# ------------------------------------------------- pygments -> michael map ---
def token_kind(ttype, value):
    """Map a pygments token type to a tokens.json code key (or None = variable)."""
    if ttype in Token.Literal.String.Doc:
        return 'docComment'
    if ttype in Token.Comment:
        return 'docComment' if 'Documentation' in str(ttype) else 'comment'
    if ttype in Token.Literal.String.Escape:
        return 'stringEscape'
    if ttype in Token.Literal.String.Interpol:
        return 'stringEscape'
    if ttype in Token.Literal.String:
        return 'string'
    if ttype in Token.Literal.Number:
        return 'number'
    if ttype in Token.Keyword.Constant or ttype in Token.Name.Constant or ttype in Token.Name.Builtin.Pseudo:
        return 'constant'
    if ttype in Token.Keyword or ttype in Token.Storage:
        return 'keyword'
    if ttype in Token.Name.Decorator or ttype in Token.Name.Attribute:
        return 'decorator'
    if ttype in Token.Name.Function or ttype in Token.Name.Function.Magic:
        return 'functionDef'
    if ttype in Token.Name.Class:
        return 'type'
    if ttype in Token.Name.Builtin or ttype in Token.Name.Function.Builtin:
        return 'functionCall'
    if ttype in Token.Name.Exception or ttype in Token.Name.Namespace:
        return 'type'
    if ttype in Token.Operator:
        return 'operator'
    if ttype in Token.Punctuation or ttype in Token.Text or ttype in Token.Whitespace:
        return 'punctuation'
    if ttype in Token.Name.Tag:
        return 'decorator'
    return None  # plain names -> variable (unstyled fallback)


# ------------------------------------------------------- theme construction ---
def _rel_lum(h):
    v = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    v = [u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4 for u in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def gray_keep_lum(h):
    """Grayscale a hex color preserving relative luminance (hence WCAG ratio).

    This is what a grayscale-forced display does: destroys hue, keeps lightness.
    """
    L = _rel_lum(h)
    u = 12.92 * L if L <= 0.0031308 else 1.055 * L ** (1 / 2.4) - 0.055
    g = round(max(0, min(1, u)) * 255)
    return f'#{g:02X}{g:02X}{g:02X}'


def michael_styles(vname, ramp, tokens_map):
    """michael variant -> theme dict (authored gray, no conversion)."""
    v = ramp['variants'][vname]
    tokens = {}
    for kind, spec in tokens_map['code'].items():
        tokens[kind] = (
            v[spec['level']]['hex'],
            spec.get('weight') == 'bold',
            spec.get('style') == 'italic',
        )
    return {'name': f'michael-{vname}', 'bg': v['bg']['hex'],
            'gutter': v['faint']['hex'], 'default': v['fg']['hex'],
            'tokens': tokens, 'grayscale': False}


def render_theme(theme, corpus, out_dir, scale=2):
    """Render one theme dict over the corpus. Returns list of output paths."""
    fonts = {}

    def font(bold, italic):
        key = (bold, italic)
        if key not in fonts:
            fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[key]), 14 * scale)
        return fonts[key]

    def fg(kind):
        if kind is not None and kind in theme['tokens']:
            c, bold, italic = theme['tokens'][kind]
        else:
            c, bold, italic = theme['default'], False, False
        return (gray_keep_lum(c) if theme['grayscale'] else c, bold, italic)

    def conv(c):
        return gray_keep_lum(c) if theme['grayscale'] else c

    paths = []
    for fname, (lang, code) in corpus.items():
        lexer = get_lexer_by_name(lang)
        lines = code.rstrip('\n').split('\n')
        probe = font(False, False)
        ch_w = probe.getbbox('M')[2] - probe.getbbox('M')[0]
        line_h = int(14 * scale * 1.55)
        pad = 12 * scale
        w = pad * 2 + ch_w * (max(len(l) for l in lines) + 4)
        h = pad * 2 + line_h * len(lines)
        img = Image.new('RGB', (w, h), conv(theme['bg']))
        draw = ImageDraw.Draw(img)

        for lineno, line in enumerate(lines):
            y = pad + lineno * line_h
            draw.text((pad, y), str(lineno + 1).rjust(3), font=font(False, False),
                      fill=conv(theme['gutter']))
            x = pad + ch_w * 4
            for ttype, value in lex(line, lexer):
                color, bold, italic = fg(token_kind(ttype, value))
                draw.text((x, y), value, font=font(bold, italic), fill=color)
                x += ch_w * len(value)

        base = os.path.join(out_dir, f"{os.path.splitext(fname)[0]}-{theme['name']}")
        img.save(base + '.png')
        img.quantize(colors=16, dither=Image.Dither.NONE).save(base + '-4bit.png')
        paths.extend([base + '.png', base + '-4bit.png'])
    return paths


# --------------------------------------------- console session (ANSI/SGR) ---
def _sgr(*params):
    return f'\x1b[{";".join(map(str, params))}m'


def _console_lines():
    """Realistic console session with embedded SGR sequences (slot-level truth)."""
    s = _sgr
    reset = s(0)
    return [
        '$ git status',
        s(32) + 'On branch main' + reset,
        s(33) + 'Your branch is ahead of origin/main by 2 commits.' + reset,
        '',
        '$ git status --short',
        s(31) + 'M  ' + reset + 'src/theme.py',
        s(32) + 'A  ' + reset + 'tests/test_palette.py',
        s(90) + '?? notes.org' + reset,
        '',
        '$ ls -la',
        s(1, 34) + 'corpus/' + reset,
        '-rw-r--r--  ramp.json',
        s(1, 32) + 'build.sh' + reset,
        s(31) + 'backup.tar.gz' + reset,
        '',
        '$ grep -n faint ramp.py',
        s(1, 31) + '42' + reset + ':    faint:   ' + s(1, 31) + '"#8D8D8D"' + reset,
        '',
        '$ git diff',
        s(31) + '- "level": 0.80,' + reset,
        s(32) + '+ "level": 0.82,' + reset,
        s(90) + '  # 4-bit survival re-checked' + reset,
    ]


def render_console(theme, ansi_palette, out_dir, scale=2):
    """Render an SGR-tokenized console session. ANSI codes are the tokenizer:
    no pygments here. Simulates bold-is-bright (bold + slot 0-7 -> slot + 8)."""
    fonts = {}

    def font(bold, italic):
        key = (bold, italic)
        if key not in fonts:
            fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[key]), 14 * scale)
        return fonts[key]

    def col(c):
        return gray_keep_lum(c) if theme['grayscale'] else c

    lines = _console_lines()
    probe = font(False, False)
    ch_w = probe.getbbox('M')[2] - probe.getbbox('M')[0]
    line_h = int(14 * scale * 1.55)
    pad = 12 * scale
    w = pad * 2 + ch_w * 72
    h = pad * 2 + line_h * len(lines)
    img = Image.new('RGB', (w, h), col(theme['bg']))
    draw = ImageDraw.Draw(img)

    for lineno, line in enumerate(lines):
        y = pad + lineno * line_h
        x = pad
        slot, bold = None, False
        i = 0
        while i < len(line):
            if line[i] == '\x1b' and i + 1 < len(line) and line[i + 1] == '[':
                end = line.find('m', i)
                if end != -1:
                    for p in line[i + 2:end].split(';'):
                        p = int(p) if p else 0
                        if p == 0:
                            slot, bold = None, False
                        elif p == 1:
                            bold = True
                        elif 30 <= p <= 37:
                            slot = p - 30
                        elif 90 <= p <= 97:
                            slot = p - 90 + 8
                    i = end + 1
                    continue
            j = i
            while j < len(line) and line[j] != '\x1b':
                j += 1
            text = line[i:j]
            use_slot = slot + 8 if (bold and slot is not None and slot < 8) else slot
            color = theme['default'] if use_slot is None else ansi_palette[use_slot]
            draw.text((x, y), text, font=font(bold, False), fill=col(color))
            x += ch_w * len(text)
            i = j

    base = os.path.join(out_dir, f"console-{theme['name']}")
    img.save(base + '.png')
    img.quantize(colors=16, dither=Image.Dither.NONE).save(base + '-4bit.png')
    return [base + '.png', base + '-4bit.png']


if __name__ == '__main__':
    with open(os.path.join(ROOT, 'ramp.json')) as fh:
        ramp = json.load(fh)
    with open(os.path.join(ROOT, 'tokens.json')) as fh:
        tokens_map = json.load(fh)
    out_dir = os.path.join(ROOT, 'corpus', 'render')
    os.makedirs(out_dir, exist_ok=True)
    # clean stale renders from older naming schemes
    for stale in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, stale))

    total = 0
    for vname in ramp['variants']:
        paths = render_theme(michael_styles(vname, ramp, tokens_map), CORPUS, out_dir)
        paths += render_console({'name': f'michael-{vname}', 'bg': ramp['variants'][vname]['bg']['hex'],
                                 'default': ramp['variants'][vname]['fg']['hex'],
                                 'grayscale': False},
                                ramp_ansi16(ramp['variants'][vname]), out_dir)
        total += len(paths)
        print(f"rendered michael-{vname}: {len(CORPUS)} code files + console session")
    for name, theme in build_baselines().items():
        paths = render_theme(theme, CORPUS, out_dir)
        paths += render_console(theme, theme['ansi16'], out_dir)
        total += len(paths)
        print(f"rendered {name}: {len(CORPUS)} code files + console session")
    print(f"total images: {total}")

    # manifest for the site gallery: filename -> structured metadata
    import re
    entries = []
    for fname in sorted(os.listdir(out_dir)):
        m = re.match(r'^(console|typescript|clojure|python|julia|rust|csharp)-(.+?)(?:-(4bit))?\.png$', fname)
        if not m:
            continue
        entries.append({
            'file': fname,
            'lang': m.group(1),
            'theme': m.group(2),
            'quant': '4bit' if m.group(3) else 'full',
        })
    with open(os.path.join(out_dir, 'manifest.json'), 'w') as fh:
        json.dump(entries, fh, indent=2)
    print(f"manifest: {len(entries)} entries")
