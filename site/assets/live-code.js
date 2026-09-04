// michael — live highlighted code samples (same corpus as bench/render.py)
const CODE = {
  python: `from dataclasses import dataclass
import re

MAX_RETRIES: int = 3

@dataclass(frozen=True)
class Fetcher:
    """Fetches pages with retries and backoff."""
    base_url: str
    timeout: float = 5.0

    async def fetch(self, path: str, session) -> str:
        url = f"{self.base_url}/{path.lstrip('/')}"
        for attempt in range(MAX_RETRIES):
            try:
                resp = await session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.text
            except ConnectionError as err:
                if attempt == MAX_RETRIES - 1:
                    raise RuntimeError(f"failed: {url}") from err`,
  julia: `module Optics

export lensmaker

"""Thin-lens focal length via the lensmaker equation."""
function lensmaker(n::Float64, r1::Float64, r2::Float64; thick=0.0)
    inv_f = (n - 1) * (1/r1 - 1/r2 + (n-1)*thick/(n*r1*r2))
    return 1 / inv_f
end

struct Surface
    radius::Float64
    convex::Bool
end`,
  rust: `use std::collections::HashMap;

#[derive(Debug, Clone)]
pub enum Node {
    Leaf { value: i64 },
    Branch(Box<Node>, Box<Node>),
}

fn walk(node: &Node, depth: usize, out: &mut HashMap<usize, usize>) {
    match node {
        Node::Leaf { .. } => *out.entry(depth).or_insert(0) += 1,
        Node::Branch(l, r) => { walk(l, depth + 1, out); walk(r, depth + 1, out); }
    }
}`,
  typescript: `export interface Options {
  retries?: number;
  baseUrl: string;
}

const DEFAULT_TIMEOUT = 5_000;

export class Router {
  private routes = new Map<string, () => Promise<Response>>();

  async handle(req: Request): Promise<Response> {
    const path = new URL(req.url).pathname;
    const handler = this.routes.get(path);
    if (!handler) throw new Error(\`no route: \${path}\`);
    return handler(req);
  }
}`,
  clojure: `(ns shop.cart
  "Shopping cart with line-item totals."
  (:require [clojure.spec.alpha :as s]))

(defn total
  "Sum of price*qty over lines, rounded to cents."
  [lines]
  (->> lines
       (filter #(s/valid? ::line %))
       (map (fn [{:keys [::price ::qty]}] (* price qty)))
       (reduce + 0.0)))

(defn register! [id lines]
  (swap! registry assoc id {:lines lines :total (total lines)}))`,
  csharp: `using System.Linq;

namespace Shop;

public record Line(decimal Price, int Qty);

public sealed class Cart
{
    private static readonly decimal TaxRate = 0.19m;
    private readonly List<Line> _lines = new();

    public decimal Net => _lines.Sum(l => l.Price * l.Qty);
    public decimal Gross() => decimal.Round(Net * (1 + TaxRate), 2);
}`,
  css: `/* panel chrome — muted comment */
.panel {
  display: flex;
  gap: 0.5rem;
  border: 1px solid var(--sel);
  opacity: 0.96;
}
.panel:focus { outline: 1px dotted; }`,
  html: `<!DOCTYPE html>
<html lang="en">
  <!-- inspector shell — faint comment -->
  <head>
    <meta charset="utf-8">
    <title>michael</title>
  </head>
  <body class="grayscale">
    <input type="url" spellcheck="false">
  </body>
</html>`,
  xml: `<?xml version="1.0" encoding="UTF-8"?>
<!-- profile: michael-dark -->
<theme name="michael" variant="dark">
  <color role="ink" hex="#F5F5F5" />
  <color role="muted" hex="#7A7A7A" />
</theme>`,
  json: `{"name": "michael",
 "levels": ["ink", "strong", "fg", "muted", "faint"],
 "gates": {"contrast": 10.0, "spacing": 0.10},
 "eink_floor": true,
 "notes": null}`,
  yaml: `# eval: median-of-3 grading
theme: michael
variants:
  light: {bg: "#F5F5F5", fg: "#505050"}
  dark:  {bg: "#070707", fg: "#9B9B9B"}
gates:
  contrast_min: 7.0
  eink: 4-bit quantization`,
  toml: `# ghostty config — michael dark
theme = "michael-dark"

[window]
opacity = 0.96
padding-x = 8

[cursor]
style = "block"
blink = false`,
};

function setLang(lang) {
  const target = document.getElementById('codeTarget');
  target.className = 'hljs language-' + lang;
  target.textContent = CODE[lang];
  // hljs 11 marks elements with data-highlighted and skips re-highlighting
  target.removeAttribute('data-highlighted');
  target.removeAttribute('data-hljs');
  hljs.highlightElement(target);
  document.querySelectorAll('#langPills .pill').forEach(p =>
    p.classList.toggle('on', p.dataset.lang === lang));
}

function codeVariant(v) {
  document.getElementById('codeBox').dataset.michael = v;
  document.getElementById('codeLight').classList.toggle('on', v === 'light');
  document.getElementById('codeDark').classList.toggle('on', v === 'dark');
}

(function initCode() {
  const pills = document.getElementById('langPills');
  for (const lang of Object.keys(CODE)) {
    const b = document.createElement('button');
    b.className = 'pill' + (lang === 'python' ? ' on' : '');
    b.dataset.lang = lang;
    b.textContent = lang;
    b.onclick = () => setLang(lang);
    pills.appendChild(b);
  }
  setLang('python');
})();
