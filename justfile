default: check

# Generate all theme outputs into out/
build:
    python3 generators/gnome_terminal.py
    python3 generators/doom_emacs.py
    python3 generators/vscode.py

# Run benchmark gates against ramp.json (contrast, dL, 4-bit survival)
check: build
    python3 bench/check.py

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

clean:
    rm -rf out
