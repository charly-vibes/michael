# michael eval report — judge: google/gemini-2.5-flash-lite

| theme | separation | readability | samples |
|---|---|---|---|
| flexoki-light | 1.67 | 2.08 | 12 |
| michael-dark | 1.58 | 2.08 | 12 |
| michael-light | 1.58 | 2.00 | 12 |
| flexoki-dark | 1.58 | 2.00 | 12 |
| solarized-dark | 1.50 | 2.08 | 12 |
| solarized-light | 1.25 | 1.92 | 12 |

## flexoki-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.75 | solid |
| types | 1.17 | BROKEN |
| function_names | 1.08 | BROKEN |
| strings | 2.00 | weak |
| numbers | 0.92 | BROKEN |
| comments | 1.50 | weak |
| punctuation | 1.08 | BROKEN |

### Most-colliding pairs

- 2x: numbers vs punctuation
- 2x: types vs numbers
- 2x: types vs function_names
- 1x: function_names vs types
- 1x: function_names vs punctuation

### Judge root causes (verbatim)

- (clojure, full) function names, numbers, and punctuation share identical styling
- (csharp, full) uniform styling for types, numbers, punctuation, and function names
- (python, full) comment gray too close to background
- (rust, full) type gray too close to comment gray
- (typescript, full) Keyword color too close to type/number color
- (clojure, 4bit) body text too low contrast
- (julia, 4bit) Function names, numbers, and punctuation are rendered identically, offering no visual distinction.
- (julia, full) String content color is identical to base code text.

Worst language: **csharp** (sep 1.00)

## michael-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.17 | weak |
| types | 1.25 | BROKEN |
| function_names | 1.00 | BROKEN |
| strings | 1.50 | weak |
| numbers | 1.33 | BROKEN |
| comments | 0.67 | BROKEN |
| punctuation | 1.17 | BROKEN |

### Most-colliding pairs

- 3x: keywords vs types
- 2x: types vs function_names
- 2x: function_names vs punctuation
- 1x: keywords vs strings
- 1x: types vs punctuation

### Judge root causes (verbatim)

- (python, full) Keywords, types, and function names have identical styling.
- (clojure, full) Extreme lack of color differentiation for most token types.
- (csharp, full) Types, function_names, numbers, and punctuation share the same color and weight, making them indistinguishable from each other.
- (julia, full) Gray elements (strings, comments, punctuation, and 0.0) are visually indistinguishable from each other.
- (rust, full) Lack of visual differentiation for types, function_names, and literal numbers.
- (typescript, full) function name color indistinguishable from type color
- (clojure, 4bit) light gray elements lack distinct styling
- (csharp, 4bit) Lack of semantic coloring/styling for all token types.

Worst language: **csharp** (sep 0.50)

## michael-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.58 | solid |
| types | 0.67 | BROKEN |
| function_names | 0.75 | BROKEN |
| strings | 2.00 | weak |
| numbers | 1.17 | BROKEN |
| comments | 0.91 | BROKEN |
| punctuation | 0.83 | BROKEN |

### Most-colliding pairs

- 2x: types vs function_names
- 2x: strings vs comments
- 1x: types vs punctuation
- 1x: numbers vs strings
- 1x: keywords vs numbers

### Judge root causes (verbatim)

- (python, full) types, function names, and numbers are indistinguishable from punctuation
- (clojure, full) string and number gray too close to code text gray
- (csharp, full) Types, function names, and numbers use colors too close to each other.
- (julia, full) keyword gray too close to number gray
- (rust, full) function names identical to keywords
- (typescript, full) body text contrast too low for types and function names
- (clojure, 4bit) Numbers and strings share the same color, and types/function names lack distinct styling.
- (csharp, 4bit) Body text color is too uniform and lacks contrast with background.

Worst language: **python** (sep 1.50)

## flexoki-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.08 | weak |
| types | 0.83 | BROKEN |
| function_names | 0.92 | BROKEN |
| strings | 2.00 | weak |
| numbers | 1.08 | BROKEN |
| comments | 0.45 | BROKEN |
| punctuation | 1.42 | BROKEN |

### Most-colliding pairs

- 3x: types vs function_names
- 2x: keywords vs types
- 1x: keywords vs function_names
- 1x: function_names vs types
- 1x: strings vs numbers

### Judge root causes (verbatim)

- (clojure, full) lack of contrast between keywords, function names, and punctuation
- (julia, full) body text too low contrast
- (python, full) body text too low contrast
- (rust, full) types, function_names, and numbers are indistinguishable from body text.
- (typescript, full) keyword/type/function_name gray too close to background
- (clojure, 4bit) Keyword color is too similar to function name and general code text.
- (csharp, 4bit) lack of differentiation between types and function names
- (csharp, full) Uniform color for keywords, types, function_names, and numbers.

Worst language: **clojure** (sep 1.00)

## solarized-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 1.42 | BROKEN |
| types | 1.08 | BROKEN |
| function_names | 1.25 | BROKEN |
| strings | 1.83 | weak |
| numbers | 1.42 | BROKEN |
| comments | 0.67 | BROKEN |
| punctuation | 1.17 | BROKEN |

### Most-colliding pairs

- 6x: keywords vs types
- 2x: keywords vs function_names
- 2x: types vs punctuation
- 1x: comments vs punctuation
- 1x: types vs numbers

### Judge root causes (verbatim)

- (clojure, full) keyword light gray too close to function name light gray
- (csharp, full) keywords, types, and punctuation have insufficient color differentiation.
- (julia, full) gray text elements for types, function names, comments, and punctuation are too similar
- (python, full) Keywords, types, function names, numbers, and punctuation share the same color, lacking visual differentiation.
- (rust, full) keyword gray too close to type gray
- (typescript, full) keywords and types are rendered identically
- (clojure, 4bit) lack of distinction between keywords, types, and function names
- (julia, 4bit) comment color too close to punctuation color

Worst language: **rust** (sep 0.50)

## solarized-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.42 | weak |
| types | 0.83 | BROKEN |
| function_names | 0.83 | BROKEN |
| strings | 1.00 | BROKEN |
| numbers | 0.83 | BROKEN |
| comments | 0.83 | BROKEN |
| punctuation | 1.00 | BROKEN |

### Most-colliding pairs

- 3x: types vs function_names
- 2x: keywords vs types
- 1x: punctuation vs types
- 1x: types vs comments
- 1x: types vs numbers

### Judge root causes (verbatim)

- (clojure, full) Medium gray is used for too many token classes, making them indistinguishable.
- (csharp, full) types gray too close to function_names gray
- (julia, full) Insufficient distinction between punctuation, types, and function names; same for strings, numbers, and comments.
- (python, full) function names, numbers, and punctuation share the same color as base text.
- (rust, full) Lack of distinct styling for types, numbers, punctuation, and strings.
- (typescript, full) Lack of any color or weight differentiation for token classes.
- (csharp, 4bit) color of types too close to color of keywords
- (julia, 4bit) white/very light gray text color for strings/numbers/punctuation has no contrast against the background

Worst language: **csharp** (sep 1.00)
