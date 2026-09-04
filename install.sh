#!/bin/sh
# michael installer — no uv, no just, stdlib-only generators.
# Usage: ./install.sh [targets...]     targets: gnome doom vscode ghostty windows
#        ./install.sh                  (auto: everything except windows)
set -eu
cd "$(dirname "$0")"

Targets="${*:-gnome doom vscode ghostty}"

# generate all outputs once (plain python3, no dependencies)
python3 generators/gnome_terminal.py    > /dev/null
python3 generators/doom_emacs.py        > /dev/null
python3 generators/vscode.py            > /dev/null
python3 generators/ghostty.py           > /dev/null
python3 generators/windows_terminal.py  > /dev/null

for t in $Targets; do
  case "$t" in
    gnome)
      if ! command -v dconf >/dev/null 2>&1; then
        echo "gnome: dconf not found — skipping (outputs are in out/gnome-terminal/)"
        continue
      fi
      dconf load /org/gnome/terminal/legacy/profiles:/ < out/gnome-terminal/michael-light.dconf
      dconf load /org/gnome/terminal/legacy/profiles:/ < out/gnome-terminal/michael-dark.dconf
      sh out/gnome-terminal/register.sh
      echo "gnome: installed — pick 'michael light/dark' in Terminal preferences"
      ;;
    doom)
      mkdir -p ~/.doom.d/themes
      cp -f out/doom-emacs/doom-michael-*.el ~/.doom.d/themes/
      echo "doom: installed — add to ~/.doom.d/config.el:"
      echo "      (custom-set-variables '(doom-theme 'doom-michael-dark))"
      ;;
    vscode)
      mkdir -p ~/.config/Code/User
      cp -f out/vscode/michael-*-color-theme.json ~/.config/Code/User/
      echo "vscode: installed — 'michael light/dark' in Preferences: Color Theme"
      ;;
    ghostty)
      mkdir -p ~/.config/ghostty/themes
      cp -f out/ghostty/michael-* ~/.config/ghostty/themes/
      echo "ghostty: installed — add to ~/.config/ghostty/config:"
      echo "  theme = light:michael-light,dark:michael-dark"
      echo "  cursor-style = bar"
      echo "  cursor-style-blink = false"
      ;;
    windows)
      echo "windows: schemes written to out/windows-terminal/michael-schemes.json"
      echo "  1. open Windows Terminal settings.json"
      echo "  2. merge the two objects into \"schemes\": [ ... ]"
      echo "  3. set \"colorScheme\": \"michael dark\" in your profile (or defaults)"
      echo "  4. recommended per-profile: \"cursorShape\": \"bar\", \"cursorBlinkingEnabled\": false"
      ;;
    *)
      echo "unknown target: $t (use: gnome doom vscode ghostty windows)" >&2
      exit 1
      ;;
  esac
done
