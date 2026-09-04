# michael

Grayscale-only theme for grayscale-forced displays.
**Priority: terminal/console/editors** (GNOME Terminal, Doom Emacs, VS Code)
on 8-bit grayscale-forced screens, desktop + mobile. E-ink is secondary —
the 4-bit quantization gate is kept as a robustness floor, not the target.

Philosophy: Solarized's lightness-relationship discipline + Flexoki's
off-polar endpoints and step-count restraint. No hue anywhere; meaning is
carried by **lightness × weight × style × overlay**, never by hue.

## Layout

- `ramp.json` — single source of truth: 8 roles per variant, OKLCH L + hex, gate-derived
- `tokens.json` — semantic map: token → (level, weight, style, overlay)
- `bench/check.py` — acceptance gates (run via `just check`)
- `generators/` — emit GNOME Terminal dconf, Doom Emacs deftheme, VS Code JSON
- `out/` — generated artifacts (do not edit)

## Semantic grammar

| Channel | Values | Meaning |
|---|---|---|
| level | ink/strong/fg/muted/faint | importance |
| weight | regular/bold | binding (definitions, bound keywords) |
| style | none/italic | kind (metadata: comments, parameters) |
| underline | solid/wavy/dotted | diagnostics only (error/warning/info) |
| overlay | bgFill/outline/inverse | selection, brace match, current search |

Bold is also the terminal's ANSI-bright flag (`bold-is-bright=true`),
multiplexing weight into the 16-slot palette.

## Benchmarks (acceptance gates)

1. WCAG vs bg: ink/strong ≥ 10:1, fg ≥ 7:1, muted ≥ 4.5:1, faint ≥ 3:1
2. ΔL ≥ 0.10 OKLCH between adjacent text levels
3. Text-on-overlay: ink/strong/fg ≥ 4.5:1, muted ≥ 3:1 vs selection fill
4. 4-bit (16-gray) quantization survival — simulates e-ink dithering
5. Selection fill visible at 4-bit

All gates must pass for **both** variants before any output ships.
`just check` is the gate runner.

## Commands

Environment is managed with **uv** (`uv sync` after clone).

```sh
uv sync            # set up .venv (pillow, pygments, ruff)
just build         # regenerate out/
just check         # build + run all gates + render corpus PNGs
just lint          # ruff
just install-gnome # dconf profiles
just install-doom  # copy themes to ~/.doom.d/themes/
just install-vscode
```

## Corpus rendering + vision eval

`bench/render.py` renders a six-language code corpus (Python, Julia, Rust,
TypeScript, Clojure, C#) through the token grammar using Pygments +
JetBrains Mono, PLUS a synthetic console session (git status/ls/grep/diff
with real SGR sequences, honoring bold-is-bright) — for michael AND for
Solarized/Flexoki baselines.
Baselines go through a luminance-preserving grayscale conversion: exactly
what a grayscale-forced display does to a color theme (WCAG ratios kept,
hue destroyed). Each render gets a full PNG + a 4-bit quantized version
(e-ink floor test).

`bench/eval.py` has a vision model (headless `pi` + OpenRouter, default
`google/gemini-2.5-flash-lite`) grade every image blind on a rubric
(token-class separation, readability, collisions) and ranks the themes:

```sh
just eval-quick   # ~6 images: python corpus, 4-bit, michael vs solarized-light
just eval         # full matrix: 6 themes x 6 languages x 2 quantizations
uv run bench/eval.py --langs python,rust --themes michael   # custom subset
uv run bench/eval.py --model google/gemma-4-31b-it:free     # free model
```

Iteration pattern: `just eval-quick` while tuning the ramp (verdicts are
cached and resume across runs), `just eval` for a release-grade pass.

Results land in `corpus/eval-results.json`. The final check is still a
real e-ink/grayscale screen — the judge is a proxy.
