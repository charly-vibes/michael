# michael eval report — judge: google/gemini-2.5-flash-lite

| theme | separation | readability | samples |
|---|---|---|---|
| michael-light | 1.71 | 2.00 | 7 |
| solarized-dark | 1.71 | 2.00 | 7 |
| solarized-light | 1.71 | 1.86 | 7 |
| flexoki-dark | 1.57 | 2.29 | 7 |
| flexoki-light | 1.57 | 1.86 | 7 |
| michael-dark | 1.57 | 2.14 | 7 |

## michael-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| comments | 0.50 | BROKEN |
| dim_text | 0.00 | BROKEN |
| dirs | 2.00 | weak |
| executables | 0.00 | BROKEN |
| function_names | 1.00 | BROKEN |
| highlight | 3.00 | solid |
| keywords | 2.67 | solid |
| modified | 1.00 | BROKEN |
| numbers | 1.83 | weak |
| punctuation | 1.33 | BROKEN |
| removed | 2.00 | weak |
| strings | 1.50 | weak |
| types | 1.17 | BROKEN |
| untracked | 1.00 | BROKEN |

### Most-colliding pairs

- 3x: types vs function_names
- 1x: modified, untracked
- 1x: punctuation vs types
- 1x: strings vs comments
- 1x: function_names vs punctuation

### Judge root causes (verbatim)

- (console, 4bit) Lack of color distinction for modified, added, and untracked Git status indicators.
- (clojure, 4bit) punctuation and types blend with default text gray
- (csharp, 4bit) Types and function names are rendered identically.
- (julia, 4bit) Lack of distinct color for types, strings, and comments.
- (python, 4bit) comment gray too close to number gray
- (rust, 4bit) comment gray too close to punctuation gray
- (typescript, 4bit) function_names and punctuation lack distinct styling from general identifiers.

Worst language: **clojure** (sep 1.00)

## solarized-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| comments | 1.00 | BROKEN |
| dim_text | 0.00 | BROKEN |
| dirs | 1.00 | BROKEN |
| executables | 0.00 | BROKEN |
| function_names | 0.83 | BROKEN |
| highlight | 1.00 | BROKEN |
| keywords | 1.67 | weak |
| modified | 2.00 | weak |
| numbers | 1.00 | BROKEN |
| punctuation | 1.50 | weak |
| removed | 2.00 | weak |
| strings | 2.00 | weak |
| types | 1.17 | BROKEN |
| untracked | 0.00 | BROKEN |

### Most-colliding pairs

- 2x: keywords vs types
- 2x: strings vs numbers
- 1x: dirs, highlight
- 1x: types vs numbers
- 1x: function_names vs numbers

### Judge root causes (verbatim)

- (console, 4bit) Lack of distinct color for directories and grep highlights.
- (clojure, 4bit) Lack of distinct colors for core code elements like keywords, identifiers, literals, and punctuation.
- (csharp, 4bit) Lack of color differentiation between keywords, types, and numbers
- (julia, 4bit) function_names, numbers, and punctuation colors are identical to body text
- (python, 4bit) keyword gray too close to type gray and function_name gray
- (rust, 4bit) String content and number boldness too subtle, blending with other tokens.
- (typescript, 4bit) keywords, types, and function names are too similar in color and weight

Worst language: **clojure** (sep 1.00)

## solarized-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 3.00 | solid |
| comments | 1.17 | BROKEN |
| dim_text | 0.00 | BROKEN |
| dirs | 0.00 | BROKEN |
| executables | 2.00 | weak |
| function_names | 1.00 | BROKEN |
| highlight | 3.00 | solid |
| keywords | 2.00 | weak |
| modified | 3.00 | solid |
| numbers | 1.50 | weak |
| punctuation | 1.33 | BROKEN |
| removed | 0.00 | BROKEN |
| strings | 1.83 | weak |
| types | 0.83 | BROKEN |
| untracked | 3.00 | solid |

### Most-colliding pairs

- 3x: types vs function_names
- 1x: removed, dirs
- 1x: strings vs numbers
- 1x: strings vs comments
- 1x: keywords vs types

### Judge root causes (verbatim)

- (console, 4bit) Failure to render distinct colors for removed items, directories, and git diff indicators.
- (clojure, 4bit) comment gray too close to background
- (csharp, 4bit) Lack of distinct color and weight contrast for keywords, types, and function names.
- (julia, 4bit) body text color too uniform
- (python, 4bit) comment gray too low contrast
- (rust, 4bit) Keywords, types, function names, numbers, and punctuation lack sufficient visual distinction from each other.
- (typescript, 4bit) Type and function names share color and weight.

Worst language: **clojure** (sep 1.00)

## flexoki-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 3.00 | solid |
| comments | 0.40 | BROKEN |
| dim_text | 2.00 | weak |
| dirs | 1.00 | BROKEN |
| executables | 0.00 | BROKEN |
| function_names | 0.67 | BROKEN |
| highlight | 3.00 | solid |
| keywords | 0.83 | BROKEN |
| modified | 3.00 | solid |
| numbers | 1.00 | BROKEN |
| punctuation | 0.83 | BROKEN |
| removed | 2.00 | weak |
| strings | 1.83 | weak |
| types | 0.67 | BROKEN |
| untracked | 3.00 | solid |

### Most-colliding pairs

- 3x: keywords vs types
- 1x: modified, untracked
- 1x: strings vs numbers
- 1x: types vs comments
- 1x: strings vs comments

### Judge root causes (verbatim)

- (console, 4bit) Directory text is not visually distinct from regular files.
- (clojure, 4bit) Numbers and strings have identical colors, lacking distinction.
- (csharp, 4bit) Color palette lacks sufficient distinction between key token types.
- (julia, 4bit) lack of distinct colors for keywords, function names, and strings
- (python, 4bit) keyword bolding too subtle
- (rust, 4bit) Keyword, type, function, and number colors are identical to body text.
- (typescript, 4bit) The identical white coloring for keywords, types, and function names makes them indistinguishable.

Worst language: **julia** (sep 1.00)

## flexoki-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 1.00 | BROKEN |
| comments | 0.50 | BROKEN |
| dim_text | 3.00 | solid |
| dirs | 0.00 | BROKEN |
| executables | 0.00 | BROKEN |
| function_names | 1.00 | BROKEN |
| highlight | 2.00 | weak |
| keywords | 1.83 | weak |
| modified | 1.00 | BROKEN |
| numbers | 1.00 | BROKEN |
| punctuation | 1.00 | BROKEN |
| removed | 2.00 | weak |
| strings | 1.67 | weak |
| types | 0.83 | BROKEN |
| untracked | 1.00 | BROKEN |

### Most-colliding pairs

- 2x: types vs punctuation
- 1x: added, modified
- 1x: punctuation vs. numbers
- 1x: keywords vs types
- 1x: types vs function_names

### Judge root causes (verbatim)

- (console, 4bit) Git status indicators (M, A, ??) are not sufficiently distinct from filenames.
- (clojure, 4bit) The neutral gray color for punctuation, numbers, types, and function names is too similar to the base text.
- (csharp, 4bit) type and punctuation color too close to background
- (julia, 4bit) Body text colors and styling lack sufficient contrast and differentiation.
- (python, 4bit) The gray for types, numbers, punctuation, and function names is identical to the base text gray.
- (rust, 4bit) Overall low contrast in the grayscale palette
- (typescript, 4bit) Keywords, types, and function names share identical styling; strings and numbers share identical styling.

Worst language: **console** (sep 1.00)

## michael-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| added | 2.00 | weak |
| comments | 1.17 | BROKEN |
| dim_text | 0.00 | BROKEN |
| dirs | 2.00 | weak |
| executables | 2.00 | weak |
| function_names | 0.67 | BROKEN |
| highlight | 3.00 | solid |
| keywords | 1.33 | BROKEN |
| modified | 2.00 | weak |
| numbers | 1.33 | BROKEN |
| punctuation | 0.83 | BROKEN |
| removed | 3.00 | solid |
| strings | 1.50 | weak |
| types | 1.33 | BROKEN |
| untracked | 2.00 | weak |

### Most-colliding pairs

- 2x: keywords vs function_names
- 1x: added, executables
- 1x: strings vs comments
- 1x: function_names vs comments
- 1x: keywords vs types

### Judge root causes (verbatim)

- (console, 4bit) Limited color palette leads to state color overlap.
- (clojure, 4bit) Lack of color or weight differentiation for all non-keyword tokens.
- (csharp, 4bit) Keywords/functions share identical bold white styling; types/numbers/punctuation share identical regular white styling.
- (julia, 4bit) lack of distinct styles for most token classes, leading to visual monotony
- (python, 4bit) keywords, types, and function_names share the same style (bold white), leading to indistinguishability.
- (typescript, 4bit) body text too low contrast
- (rust, 4bit) keyword and function_names share identical styling

Worst language: **clojure** (sep 1.00)
