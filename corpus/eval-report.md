# michael eval report — judge: google/gemini-2.5-flash-lite

| theme | separation | readability | samples |
|---|---|---|---|
| michael-dark | 3.00 | 4.00 | 1 |
| flexoki-dark | 2.00 | 4.00 | 1 |
| michael-light | 2.00 | 2.00 | 1 |
| solarized-dark | 2.00 | 3.00 | 1 |
| solarized-light | 2.00 | 3.00 | 1 |
| flexoki-light | 1.00 | 2.00 | 1 |

## michael-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| dim_text | 0.00 | BROKEN |
| dirs | 2.00 | weak |
| executables | 2.00 | weak |
| highlight | 3.00 | solid |
| modified | 2.00 | weak |
| removed | 3.00 | solid |
| untracked | 2.00 | weak |

### Most-colliding pairs

- 1x: added, executables

### Judge root causes (verbatim)

- (console, 4bit) Limited color palette leads to state color overlap.

Worst language: **console** (sep 3.00)

## flexoki-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 3.00 | solid |
| dim_text | 2.00 | weak |
| dirs | 1.00 | BROKEN |
| executables | 0.00 | BROKEN |
| highlight | 3.00 | solid |
| modified | 3.00 | solid |
| removed | 2.00 | weak |
| untracked | 3.00 | solid |

### Most-colliding pairs

- 1x: modified, untracked

### Judge root causes (verbatim)

- (console, 4bit) Directory text is not visually distinct from regular files.

Worst language: **console** (sep 2.00)

## michael-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| dim_text | 0.00 | BROKEN |
| dirs | 2.00 | weak |
| executables | 0.00 | BROKEN |
| highlight | 3.00 | solid |
| modified | 1.00 | BROKEN |
| removed | 2.00 | weak |
| untracked | 1.00 | BROKEN |

### Most-colliding pairs

- 1x: modified, untracked

### Judge root causes (verbatim)

- (console, 4bit) Lack of color distinction for modified, added, and untracked Git status indicators.

Worst language: **console** (sep 2.00)

## solarized-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| dim_text | 0.00 | BROKEN |
| dirs | 1.00 | BROKEN |
| executables | 0.00 | BROKEN |
| highlight | 1.00 | BROKEN |
| modified | 2.00 | weak |
| removed | 2.00 | weak |
| untracked | 0.00 | BROKEN |

### Most-colliding pairs

- 1x: dirs, highlight

### Judge root causes (verbatim)

- (console, 4bit) Lack of distinct color for directories and grep highlights.

Worst language: **console** (sep 2.00)

## solarized-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 3.00 | solid |
| dim_text | 0.00 | BROKEN |
| dirs | 0.00 | BROKEN |
| executables | 2.00 | weak |
| highlight | 3.00 | solid |
| modified | 3.00 | solid |
| removed | 0.00 | BROKEN |
| untracked | 3.00 | solid |

### Most-colliding pairs

- 1x: removed, dirs

### Judge root causes (verbatim)

- (console, 4bit) Failure to render distinct colors for removed items, directories, and git diff indicators.

Worst language: **console** (sep 2.00)

## flexoki-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 1.00 | BROKEN |
| dim_text | 3.00 | solid |
| dirs | 0.00 | BROKEN |
| executables | 0.00 | BROKEN |
| highlight | 2.00 | weak |
| modified | 1.00 | BROKEN |
| removed | 2.00 | weak |
| untracked | 1.00 | BROKEN |

### Most-colliding pairs

- 1x: added, modified

### Judge root causes (verbatim)

- (console, 4bit) Git status indicators (M, A, ??) are not sufficiently distinct from filenames.

Worst language: **console** (sep 1.00)
