default: check

# Generate all theme outputs into out/
build:
    uv run generators/gnome_terminal.py
    uv run generators/doom_emacs.py
    uv run generators/vscode.py
    uv run generators/ghostty.py
    uv run generators/windows_terminal.py
    uv run generators/highlightjs.py

# Run benchmark gates + render corpus PNGs (full and 4-bit e-ink simulation)
check: build
    uv run bench/check.py
    uv run bench/render.py

# Vision eval: pi grades rendered themes (needs OPENROUTER credit)
eval: build
    uv run bench/render.py
    uv run bench/eval.py --jobs 2

# Light eval: python corpus only, 4-bit, michael vs winning baseline (~6 images)
eval-quick: build
    uv run bench/eval.py --jobs 3 --quant 4bit --langs python \
        --themes "michael,solarized-light"

# Lint Python sources
lint:
    uv run ruff check bench generators

# Install: GNOME Terminal profiles via dconf
install-gnome: build
    dconf load /org/gnome/terminal/legacy/profiles:/ < out/gnome-terminal/michael-light.dconf
    dconf load /org/gnome/terminal/legacy/profiles:/ < out/gnome-terminal/michael-dark.dconf
    @echo "Set default profile in GNOME Terminal preferences."

# Install: Doom Emacs theme
install-doom: build
    mkdir -p ~/.doom.d/themes
    cp -f out/doom-emacs/doom-michael-*.el ~/.doom.d/themes/
    @echo "Add to ~/.doom.d/config.el: (custom-set-variables '(doom-theme 'doom-michael-dark))"

# Install: VS Code theme
install-vscode: build
    mkdir -p ~/.config/Code/User
    cp -f out/vscode/michael-*-color-theme.json ~/.config/Code/User/
    @echo "Select 'michael light' / 'michael dark' via Preferences: Color Theme."

# Render corpus + publish gallery assets (images + manifest) to site/
gallery: build
    uv run bench/render.py
    mkdir -p site/assets/gallery
    cp -f corpus/render/*.png site/assets/gallery/
    for f in corpus/render-color/*.png; do cp -f "$f" "site/assets/gallery/color-$(basename $f)"; done
    cp -f corpus/render/manifest.json site/assets/gallery/

clean:
    rm -rf out corpus/render
