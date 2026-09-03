# michael

Grayscale-only theme for grayscale-forced displays and e-ink panels.
Light + dark variants. Targets: GNOME Terminal, Doom Emacs, VS Code.

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

## Corpus rendering

`bench/render.py` renders the six-language corpus (Python, Julia, Rust,
TypeScript, Clojure, C#) through the actual token grammar using Pygments +
JetBrains Mono, in both variants, into `corpus/render/`:

- `<lang>-light.png` / `<lang>-dark.png` — full-fidelity render
- `<lang>-*-4bit.png` — quantized to 16 grays (e-ink simulation)

Inspect the 4-bit PNGs to confirm every token state survives the panel;
the final check is still a real e-ink/grayscale screen.
