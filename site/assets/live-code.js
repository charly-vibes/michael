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
};

function setLang(lang) {
  const target = document.getElementById('codeTarget');
  target.className = 'hljs language-' + lang;
  target.textContent = CODE[lang];
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
