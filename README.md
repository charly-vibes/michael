# michael

Grayscale-only color theme for grayscale-forced displays.
**Priority: terminal/console/editors** — GNOME Terminal, Doom Emacs, VS Code.
Light + dark variants. E-ink is secondary: the 4-bit quantization gate stays
as a robustness floor, not the design target.

**Live docs & showcase:** <https://charly-vibes.github.io/michael/>

## Why

On a grayscale-forced screen (desktop or mobile), color themes lose their hue
and their token distinctions collapse to whatever lightness accidents remain.
michael is authored grayscale from the start: meaning is carried by
**lightness × weight × style × overlay** — never by hue. Evaluated against
Solarized and Flexoki converted the same way your screens convert them.

## The grammar

| Channel | Values | Meaning |
|---|---|---|
| level | ink / strong / fg / muted / faint | importance |
| weight | regular / bold | binding (definitions, keywords) |
| style | none / italic | kind (comments, parameters, metadata) |
| underline | solid / wavy / dotted | diagnostics only (error / warning / info) |
| overlay | bgFill / outline / inverse | selection, brace match, search |

Bold is also the terminal's ANSI-bright flag (`bold-is-bright=true`), so the
weight channel doubles as a brightness escape hatch in the 16-slot palette.

## Benchmarks (acceptance gates)

`just check` runs gates against both variants and fails on violation:

1. WCAG contrast vs bg: ink/strong ≥ 10:1, fg ≥ 7:1, muted ≥ 4.5:1, faint ≥ 3:1
2. ΔL ≥ 0.10 OKLCH between adjacent text levels
3. Text-on-overlay: ink/strong/fg ≥ 4.5:1, muted ≥ 3:1 vs selection fill
4. 4-bit (16-gray) quantization survival — robustness floor, e-ink included
5. Selection fill must be visible after quantization

## Vision eval (pi + OpenRouter)

`bench/eval.py` has a vision model grade rendered themes **blind** (median of
repeats), producing per-class diagnostics: which token classes collide, worst
pairs, and a root-cause statement per render. Baselines are Solarized and
Flexoki, luminance-preserving grayscaled — exactly what your displays do to
color themes. Headline results live in `corpus/eval-report.md`;
`notes/eval-experiments.org` is the full experiment log.

## Install

Installing needs **nothing but Python 3** — the generators are stdlib-only.
`uv`/`just` are only needed for the eval pipeline and gate checks.

```sh
git clone https://github.com/charly-vibes/michael.git
cd michael
./install.sh                    # everything except Windows Terminal
```

Or pick targets explicitly:

```sh
./install.sh gnome doom vscode ghostty
./install.sh windows            # prints merge instructions for settings.json
```

| target | activate |
|---|---|
| GNOME Terminal | Preferences → Profiles → *michael light/dark* (cursor bar, blink off, bold-is-bright preset) |
| Doom Emacs | `(custom-set-variables '(doom-theme 'doom-michael-dark))` |
| VS Code | Preferences: Color Theme → *michael light/dark* |
| Ghostty | add `theme = light:michael-light,dark:michael-dark` to `~/.config/ghostty/config` |
| Windows Terminal | merge `out/windows-terminal/michael-schemes.json` into `settings.json` → `schemes`, set `"colorScheme": "michael dark"` |

On Windows without a shell: `python generators/windows_terminal.py` works
with plain CPython, then merge the emitted JSON.

### Dev tooling (optional)

```sh
uv sync               # .venv: pillow, pygments, ruff (eval pipeline only)
just build            # regenerate out/
just check            # build + gates + render corpus
just eval-quick       # light vision eval
just lint             # ruff
```

## Terminal palette design

The 16 ANSI slots are assigned for real console semantics, not hue parity:
git-status trio (modified/deleted/staged) lands on three distinct grays;
bold-red grep matches pop to ink via bold-is-bright; dirs and executables
escape to brighter slots when bolded. See `bench/ansi.py` (single source of
truth, shared with the eval's console-session renderer).

## Repo layout

| path | what |
|---|---|
| `ramp.json` | 8 roles × 2 variants, OKLCH L + hex, gate-derived |
| `tokens.json` | semantic map: token → (level, weight, style, overlay) |
| `bench/check.py` | acceptance gates |
| `bench/render.py` | corpus renderer (code + console sessions, all themes) |
| `bench/eval.py` | blind vision eval via headless pi + OpenRouter |
| `bench/ansi.py` | ANSI slot map (single source of truth) |
| `bench/baselines.py` | Solarized / Flexoki baselines + canonical ANSI palettes |
| `generators/` | GNOME Terminal dconf, Ghostty, Windows Terminal schemes, Doom deftheme, VS Code JSON |
| `install.sh` | dependency-free installer (stdlib-only generators) |
| `notes/eval-experiments.org` | experiment log |
| `site/` | GitHub Pages showcase |

## License

See [LICENSE](LICENSE).
