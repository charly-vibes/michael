#!/usr/bin/env python3
"""Vision eval: pi judges rendered themes for clean token separation.

For every theme x language x quantization image, a vision model (via headless
pi + OpenRouter) grades the render against a rubric and reports structured
verdicts. Aggregate results rank michael against the Solarized/Flexoki
baselines AFTER luminance-preserving grayscale conversion — i.e., what the
user's grayscale-forced displays actually show.

Usage:
    uv run bench/eval.py [--model google/gemini-2.5-flash-lite] [--jobs 4]
        [--filter michael]     # subset by substring
        [--quant full|4bit|both]
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER_DIR = os.path.join(HERE, '..', 'corpus', 'render')

RUBRIC = """You are grading a code-editor color theme rendered as a screenshot. \
The screenshot may be in color or grayscale; grade ONLY what is visible.

Rate the following on integer scales:
- "separation": 0-5, how cleanly distinct the token classes are \
(keywords, types, function names, strings, numbers, comments, punctuation). \
5 = every class instantly distinguishable; 0 = wall of uniform text.
- "readability": 0-5, comfort for reading a full file of this code \
(contrast of body text, harshness, visual noise).
- "collisions": list any pairs of token classes that are hard to tell apart, \
e.g. ["strings vs comments", "types vs function names"]. Empty list if none.
- "notes": one short sentence, max 20 words.

Answer with ONLY a JSON object, no markdown fences:
{"separation": <int>, "readability": <int>, "collisions": ["..."], "notes": "..."}"""


def run_pi(image_path: str, model: str) -> dict:
    """Ask headless pi to grade one image. Returns parsed verdict dict."""
    cmd = ['pi', '-p', '--no-session', '-nt',
           '--provider', 'openrouter', '--model', model,
           RUBRIC, f'@{image_path}']
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180, check=False)
        out = proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return {'error': 'timeout', 'separation': -1, 'readability': -1,
                'collisions': [], 'notes': 'timeout'}
    # strip accidental fences
    if out.startswith('```'):
        out = out.strip('`').removeprefix('json').strip()
    try:
        start, end = out.find('{'), out.rfind('}')
        verdict = json.loads(out[start:end + 1])
    except (json.JSONDecodeError, ValueError):
        return {'error': proc.stdout[:200] + proc.stderr[:200],
                'separation': -1, 'readability': -1, 'collisions': [],
                'notes': 'unparseable'}
    verdict.setdefault('separation', -1)
    verdict.setdefault('readability', -1)
    verdict.setdefault('collisions', [])
    verdict.setdefault('notes', '')
    return verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='google/gemini-2.5-flash-lite')
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--filter', default='')
    ap.add_argument('--quant', choices=['full', '4bit', 'both'], default='both')
    args = ap.parse_args()

    images = sorted(
        os.path.join(RENDER_DIR, f) for f in os.listdir(RENDER_DIR)
        if f.endswith('.png') and args.filter in f
        and (args.quant == 'both'
             or (args.quant == '4bit') == f.endswith('-4bit.png')))
    if not images:
        sys.exit(f'no images matching filter={args.filter!r} in {RENDER_DIR}')

    print(f'evaluating {len(images)} images with {args.model}, {args.jobs} at a time\n')
    results = {}
    with cf_pool(args.jobs) as pool:
        futures = {pool.submit(run_pi, img, args.model): img for img in images}
        for done, fut in enumerate(cf.as_completed(futures), 1):
            img = futures[fut]
            v = fut.result()
            results[img] = v
            print(f"[{done:2d}/{len(images)}] {os.path.basename(img):45s} "
                  f"sep={v['separation']} read={v['readability']} "
                  f"collisions={len(v['collisions'])}")

    # aggregate by theme
    print('\n=== AGGREGATE (by theme) ===')
    langs = ('typescript', 'clojure', 'python', 'julia', 'rust', 'csharp')
    themes = {}
    for img, v in results.items():
        stem = os.path.basename(img).removesuffix('.png').removesuffix('-4bit')
        theme = stem
        for lang in langs:  # filenames are <lang>-<theme>[-4bit].png
            if stem.startswith(f'{lang}-'):
                theme = stem[len(lang) + 1:]
                break
        t = themes.setdefault(theme, {'sep': [], 'read': [], 'coll': 0, 'n': 0})
        if v['separation'] >= 0:
            t['sep'].append(v['separation'])
            t['read'].append(v['readability'])
            t['coll'] += len(v['collisions'])
            t['n'] += 1

    rows = []
    for theme, t in themes.items():
        sep = sum(t['sep']) / len(t['sep']) if t['sep'] else -1
        read = sum(t['read']) / len(t['read']) if t['read'] else -1
        rows.append((sep, read, t['coll'], t['n'], theme))
    rows.sort(reverse=True)
    print(f"{'theme':30s} {'sep':>5s} {'read':>5s} {'coll':>4s} {'n':>3s}")
    for sep, read, coll, n, theme in rows:
        print(f'{theme:30s} {sep:5.2f} {read:5.2f} {coll:4d} {n:3d}')

    out = os.path.join(HERE, '..', 'corpus', 'eval-results.json')
    with open(out, 'w') as f:
        json.dump({'model': args.model, 'results': {os.path.basename(k): v for k, v in results.items()}}, f, indent=2)
    print(f'\nfull verdicts: {out}')


def cf_pool(jobs):
    """ThreadPoolExecutor helper (named for readability)."""
    return ThreadPoolExecutor(max_workers=jobs)

if __name__ == '__main__':
    main()
