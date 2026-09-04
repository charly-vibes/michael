#!/usr/bin/env python3
"""Vision eval: pi judges rendered themes with per-class diagnostic detail.

For every theme x language x quantization image, a vision model (headless pi +
OpenRouter) grades each token class for distinctness and explains what is
wrong. Output: corpus/eval-results.json (raw verdicts) and
corpus/eval-report.md (per-theme diagnostics: weak classes, collision matrix,
judge's root-cause analysis).

Verdicts are cached: images already graded in eval-results.json are skipped
unless --no-cache.

Usage:
    uv run bench/eval.py [--model google/gemini-2.5-flash-lite] [--jobs 2]
        [--filter michael] [--quant full|4bit|both] [--no-cache]
"""
import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER_DIR = os.path.join(HERE, '..', 'corpus', 'render')
LANGS = ('console', 'typescript', 'clojure', 'python', 'julia', 'rust', 'csharp')
CLASSES = ('keywords', 'types', 'function_names', 'strings', 'numbers', 'comments', 'punctuation')

RUBRIC = f"""You are grading a code-editor theme rendered as a screenshot of source code. \
The image may be color or grayscale; grade ONLY what is visible in the image.

For EACH token class below, judge how visually distinct it is from the other \
classes in this exact screenshot:
{', '.join(CLASSES)}.

Score each class 0-3:
- 3 = instantly distinguishable from all other classes
- 2 = distinguishable with attention
- 1 = confusable with at least one other class (name the confusable partner in notes)
- 0 = indistinguishable from other text

Then:
- "closest_pair": the two classes that are MOST confusable with each other, \
e.g. "strings vs comments"
- "root_cause": the single most impactful change that would improve this render, \
e.g. "comment gray too close to string gray", "keyword bolding too subtle", \
"body text too low contrast"
- "separation": 0-5 overall separation score
- "readability": 0-5 comfort reading a full file (contrast, strain, noise)
- "notes": one short sentence, max 20 words

Answer with ONLY a JSON object, no markdown fences:
{{"classes": {{"keywords": {{"distinct": 0, "notes": "..."}}, ...}}, \
"closest_pair": "...", "root_cause": "...", "separation": 0, "readability": 0, "notes": "..."}}"""


def parse_theme_image(fname):
    """python-michael-dark-4bit.png -> ('python', 'michael-dark', '4bit').

    Also repairs legacy cache keys like 'python-michael-dark-full-full-full'.
    """
    stem = fname.removesuffix('.png')
    quant = 'full'
    if stem.endswith('-4bit'):
        stem = stem[:-len('-4bit')]
        quant = '4bit'
    while stem.endswith('-full'):  # legacy repeated suffixes
        stem = stem[:-len('-full')]
        if not fname.endswith('-4bit.png'):
            quant = 'full'
    for lang in LANGS:
        if stem.startswith(f'{lang}-'):
            theme = stem[len(lang) + 1:]
            if not theme.endswith('-4bit'):
                return lang, theme, quant
    return None


def run_pi(image_path: str, model: str) -> dict:
    """Ask headless pi to grade one image. Returns parsed verdict dict."""
    cmd = ['pi', '-p', '--no-session', '-nt',
           '--provider', 'openrouter', '--model', model,
           RUBRIC, f'@{image_path}']
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180, check=False)
        out = proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return {'error': 'timeout', 'classes': {}, 'closest_pair': '',
                'root_cause': '', 'separation': -1, 'readability': -1, 'notes': 'timeout'}
    if out.startswith('```'):
        out = out.strip('`').removeprefix('json').strip()
    try:
        start, end = out.find('{'), out.rfind('}')
        verdict = json.loads(out[start:end + 1])
    except (json.JSONDecodeError, ValueError):
        return {'error': (proc.stdout + proc.stderr)[:200], 'classes': {},
                'closest_pair': '', 'root_cause': '', 'separation': -1,
                'readability': -1, 'notes': 'unparseable'}
    verdict.setdefault('classes', {})
    verdict.setdefault('closest_pair', '')
    verdict.setdefault('root_cause', '')
    verdict.setdefault('separation', -1)
    verdict.setdefault('readability', -1)
    verdict.setdefault('notes', '')
    return verdict


def mean(xs):
    xs = [x for x in xs if x >= 0]
    return sum(xs) / len(xs) if xs else -1


def write_report(results, model):
    """Per-theme diagnostic markdown: weak classes, collision matrix, root causes."""
    themes = {}
    for (lang, theme, quant), v in results.items():
        if v['separation'] < 0:
            continue
        t = themes.setdefault(theme, {'sep': [], 'read': [], 'classes': {c: [] for c in CLASSES},
                                      'pairs': Counter(), 'roots': [], 'langs': {}})
        t['sep'].append(v['separation'])
        t['read'].append(v['readability'])
        for c in CLASSES:
            entry = v['classes'].get(c)
            if entry and 'distinct' in entry:
                t['classes'][c].append(entry['distinct'])
        if v.get('closest_pair'):
            t['pairs'][v['closest_pair']] += 1
        if v.get('root_cause'):
            t['roots'].append(f"- ({lang}, {quant}) {v['root_cause']}")
        t['langs'].setdefault(lang, []).append(v['separation'])

    lines = [f'# michael eval report — judge: {model}\n']
    lines.append('| theme | separation | readability | samples |')
    lines.append('|---|---|---|---|')
    for theme, t in sorted(themes.items(), key=lambda kv: -mean(kv[1]['sep'])):
        lines.append(f"| {theme} | {mean(t['sep']):.2f} | {mean(t['read']):.2f} | {len(t['sep'])} |")

    for theme, t in sorted(themes.items(), key=lambda kv: -mean(kv[1]['sep'])):
        lines.append(f'\n## {theme}\n')
        lines.append('### Class distinctness (mean 0-3)\n')
        lines.append('| class | distinct | verdict |')
        lines.append('|---|---|---|')
        for c in CLASSES:
            m = mean(t['classes'][c])
            verdict = ('solid' if m >= 2.5 else 'weak' if m >= 1.5 else 'BROKEN') if m >= 0 else '?'
            lines.append(f'| {c} | {m:.2f} | {verdict} |')
        lines.append('\n### Most-colliding pairs\n')
        for pair, n in t['pairs'].most_common(5):
            lines.append(f'- {n}x: {pair}')
        lines.append('\n### Judge root causes (verbatim)\n')
        lines.extend(t['roots'][:8])
        worst_lang = min(t['langs'], key=lambda l: mean(t['langs'][l]))
        lines.append(f'\nWorst language: **{worst_lang}** (sep {mean(t["langs"][worst_lang]):.2f})')

    out = os.path.join(HERE, '..', 'corpus', 'eval-report.md')
    with open(out, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'report: {out}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='google/gemini-2.5-flash-lite')
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--filter', default='')
    ap.add_argument('--quant', choices=['full', '4bit', 'both'], default='both')
    ap.add_argument('--no-cache', action='store_true')
    ap.add_argument('--repeats', type=int, default=1,
                    help='grades per image; median is kept (judge noise is +-0.5 at n=1)')
    ap.add_argument('--langs', default='',
                    help='comma-separated subset, e.g. "python,rust" (default: all)')
    ap.add_argument('--themes', default='',
                    help='comma-separated substrings, e.g. "michael-light,solarized-light"')
    args = ap.parse_args()

    lang_set = tuple(s.strip() for s in args.langs.split(',') if s.strip()) or LANGS
    theme_subs = tuple(s.strip() for s in args.themes.split(',') if s.strip())
    images = sorted(
        os.path.join(RENDER_DIR, f) for f in os.listdir(RENDER_DIR)
        if f.endswith('.png') and args.filter in f
        and (args.quant == 'both'
             or (args.quant == '4bit') == f.endswith('-4bit.png'))
        and any(f.startswith(f'{lang}-') for lang in lang_set)
        and (not theme_subs or any(sub in f for sub in theme_subs)))
    if not images:
        sys.exit(f'no images matching filter={args.filter!r}')

    cache_path = os.path.join(HERE, '..', 'corpus', 'eval-results.json')
    results = {}
    if not args.no_cache and os.path.exists(cache_path):
        with open(cache_path) as f:
            cached = json.load(f).get('results', {})
        for fname, v in cached.items():
            key = parse_theme_image(fname)
            if key and v.get('separation', -1) >= 0 and v.get('classes'):
                results[key] = v
    todo = [img for img in images
            if parse_theme_image(os.path.basename(img)) not in results]
    print(f'{len(images)} images, {len(results)} cached, {len(todo)} to grade '
          f'with {args.model}, {args.jobs} at a time\n')

    def grade(img):
        verdicts = [run_pi(img, args.model) for _ in range(args.repeats)]
        valid = sorted((v for v in verdicts if v['separation'] >= 0),
                       key=lambda v: v['separation'])
        if not valid:
            return img, verdicts[0]
        med = valid[len(valid) // 2]  # the median-run verdict, unmodified
        med['repeats'] = [v['separation'] for v in verdicts]
        return img, med

    cache_file = cache_path

    def save():
        tmp = cache_file + '.tmp'
        with open(tmp, 'w') as f:  # atomic: crash mid-dump can't corrupt cache
            json.dump({'model': args.model,
                       'results': {f'{l}-{t}-{q}': v
                                   for (l, t, q), v in results.items()}},
                      f, indent=2)
        os.replace(tmp, cache_file)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for done, (img, v) in enumerate(pool.map(grade, todo), 1):
            results[parse_theme_image(os.path.basename(img))] = v
            save()  # incremental: a timeout keeps completed verdicts
            print(f"[{done:2d}/{len(todo)}] {os.path.basename(img):42s} "
                  f"sep={v['separation']} read={v['readability']} "
                  f"worst={v.get('closest_pair', '')[:40]}", flush=True)

    save()

    # console summary: per-theme weak classes
    print('\n=== PER-CLASS DIAGNOSTICS (theme means, 0-3) ===')
    by_theme = {}
    for (lang, theme, quant), v in results.items():
        if v['separation'] < 0:
            continue
        t = by_theme.setdefault(theme, {c: [] for c in CLASSES})
        for c in CLASSES:
            entry = v['classes'].get(c)
            if entry and 'distinct' in entry:
                t[c].append(entry['distinct'])
    for theme, t in sorted(by_theme.items()):
        cells = ' '.join(f'{c[:4]}={mean(t[c]):.1f}' for c in CLASSES)
        print(f'{theme:24s} {cells}')

    write_report(results, args.model)


if __name__ == '__main__':
    main()
