# michael eval report — judge: google/gemini-2.5-flash-lite

| theme | separation | readability | samples |
|---|---|---|---|
| michael-light | 1.83 | 2.00 | 6 |
| flexoki-light | 1.62 | 2.08 | 13 |
| solarized-dark | 1.54 | 2.08 | 13 |
| flexoki-dark | 1.54 | 2.00 | 13 |
| michael-dark | 1.50 | 2.00 | 6 |
| solarized-light | 1.15 | 1.77 | 13 |

## michael-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 3.00 | solid |
| types | 0.83 | BROKEN |
| function_names | 0.83 | BROKEN |
| strings | 1.83 | weak |
| numbers | 1.17 | BROKEN |
| comments | 1.17 | BROKEN |
| punctuation | 1.00 | BROKEN |

### Most-colliding pairs

- 4x: types vs function_names
- 1x: strings vs comments
- 1x: numbers vs punctuation

### Judge root causes (verbatim)

- (clojure, 4bit) type gray too close to number gray
- (julia, 4bit) Lack of distinct hue or weight for types, function_names, numbers, and punctuation.
- (python, 4bit) body text too low contrast
- (typescript, 4bit) type and function name gray value too close to general text gray value
- (csharp, 4bit) Type and function_name colors are identical.
- (console, 4bit) body text color is too close to numbers and punctuation

Worst language: **clojure** (sep 1.00)

## flexoki-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.54 | solid |
| types | 1.08 | BROKEN |
| function_names | 1.00 | BROKEN |
| strings | 2.00 | weak |
| numbers | 0.85 | BROKEN |
| comments | 1.62 | weak |
| punctuation | 1.00 | BROKEN |

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

## solarized-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 1.54 | weak |
| types | 1.00 | BROKEN |
| function_names | 1.23 | BROKEN |
| strings | 1.92 | weak |
| numbers | 1.38 | BROKEN |
| comments | 0.62 | BROKEN |
| punctuation | 1.15 | BROKEN |

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

## flexoki-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 1.92 | weak |
| types | 0.77 | BROKEN |
| function_names | 0.85 | BROKEN |
| strings | 1.83 | weak |
| numbers | 1.00 | BROKEN |
| comments | 0.50 | BROKEN |
| punctuation | 1.38 | BROKEN |

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

## michael-dark

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.50 | solid |
| types | 0.67 | BROKEN |
| function_names | 1.33 | BROKEN |
| strings | 1.33 | BROKEN |
| numbers | 0.50 | BROKEN |
| comments | 0.17 | BROKEN |
| punctuation | 0.67 | BROKEN |

### Most-colliding pairs

- 1x: function_names vs types
- 1x: types vs function_names
- 1x: types vs numbers
- 1x: types vs strings
- 1x: numbers vs punctuation

### Judge root causes (verbatim)

- (clojure, 4bit) Lack of distinct color for types, numbers, function names, and punctuation.
- (csharp, 4bit) Lack of visual distinction between types, function_names, numbers, and punctuation.
- (python, 4bit) type, number, and comment colors are too similar and lack contrast.
- (rust, 4bit) Non-bold text lacks distinct styling for types, strings, and punctuation.
- (typescript, 4bit) Numbers and punctuation share the same color, making them indistinguishable.
- (console, 4bit) Lack of color and weight differentiation between token classes.

Worst language: **console** (sep 0.00)

## solarized-light

### Class distinctness (mean 0-3)

| class | distinct | verdict |
|---|---|---|
| keywords | 2.23 | weak |
| types | 0.77 | BROKEN |
| function_names | 0.77 | BROKEN |
| strings | 0.92 | BROKEN |
| numbers | 0.77 | BROKEN |
| comments | 0.85 | BROKEN |
| punctuation | 0.92 | BROKEN |

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

Worst language: **console** (sep 0.00)
