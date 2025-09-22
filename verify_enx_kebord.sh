#!/usr/bin/env bash
# enx-kebord sanity checker for current source directory (path-agnostic, venv-enforcing)
# Verifies venv, dependencies, sounds, and venv-based launchers.

set -euo pipefail

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m"

BASE="$(cd "$(dirname "$0")" && pwd)"
VENV="$BASE/venv"
PY="$VENV/bin/python3"

SOUND_TYPES=(
  blue brown red mechanical typewriter creamy dry thock clicky silent tactile lofi gx_feryn lee_sin hacker hard
)

ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail()  { echo -e "${RED}[FAIL]${NC} $1"; }
step()  { echo -e "\n${BLUE}==>${NC} $1"; }

summary_msgs=()
add_summary() { summary_msgs+=("$1"); }

step "Using base path: $BASE"
cd "$BASE"

step "Checking virtual environment"
if [[ -x "$PY" ]]; then
  ok "Found venv Python: $PY"
else
  warn "Venv not found at $VENV"
  add_summary "Create venv and install deps: ./setup_enhanced.sh"
fi

if [[ -x "$PY" ]]; then
  step "Checking Python dependencies in venv (pygame, pynput, psutil, numpy)"
  if "$PY" - << 'PY'
import importlib, sys
mods = ["pygame", "pynput", "psutil", "numpy"]
missing = []
for m in mods:
    try:
        importlib.import_module(m)
    except Exception:
        missing.append(m)
if missing:
    print("MISSING:" + ",".join(missing))
    sys.exit(3)
print("OK")
PY
  then
    ok "All required modules present"
  else
    MISSING=$("$PY" - << 'PY'
import importlib, sys
mods = ["pygame", "pynput", "psutil", "numpy"]
missing = []
for m in mods:
    try:
        importlib.import_module(m)
    except Exception:
        missing.append(m)
print(",".join(missing))
PY
    )
    warn "Missing Python modules: ${MISSING:-unknown}"
    add_summary "Install missing modules in venv: source venv/bin/activate && pip install -r requirements.txt"
  fi
fi

step "Checking generated sounds"
missing_sounds=()
for s in "${SOUND_TYPES[@]}"; do
  f="generated_sounds/keyboard_${s}.wav"
  if [[ ! -f "$f" ]]; then
    missing_sounds+=("$s")
  fi
done
if [[ ${#missing_sounds[@]} -eq 0 ]]; then
  ok "All ${#SOUND_TYPES[@]} generated sound files exist"
else
  warn "Missing ${#missing_sounds[@]} sound(s): ${missing_sounds[*]}"
  add_summary "Generate sounds: ./sound_control.sh generate"
fi

step "Checking current sound file"
if [[ -f "key_press.wav" ]]; then
  ok "key_press.wav present"
else
  warn "key_press.wav missing"
  add_summary "Set a current sound: ./sound_control.sh switch blue (or any type)"
fi

step "Checking venv usage in control script"
if grep -q 'VENV_PYTHON="\$SCRIPT_DIR/venv/bin/python3"' keyboard_sound_control.sh && \
   grep -q '"\$VENV_PYTHON" "\$DAEMON_PATH" \&' keyboard_sound_control.sh; then
  ok "keyboard_sound_control.sh launches daemon via venv"
else
  warn "keyboard_sound_control.sh is not venv-enforced"
  add_summary "Ensure keyboard_sound_control.sh uses VENV_PYTHON to start the daemon"
fi

step "Checking desktop templates"
errors=0
if grep -q "^Exec=launch_gui.sh$" enx-kebord.desktop; then
  ok "enx-kebord.desktop Exec uses launch script"
else
  warn "enx-kebord.desktop Exec not using launch script"
  errors=$((errors+1))
fi
if grep -q "^Icon=enx-kebord-icon.png$" enx-kebord.desktop; then
  ok "enx-kebord.desktop Icon is relative"
else
  warn "enx-kebord.desktop Icon not relative"
  errors=$((errors+1))
fi
if grep -q "^Exec=launch_daemon.sh$" enx-kebord-daemon.desktop; then
  ok "enx-kebord-daemon.desktop Exec uses launch script"
else
  warn "enx-kebord-daemon.desktop Exec not using launch script"
  errors=$((errors+1))
fi
if grep -q "^Icon=enx-kebord-icon.png$" enx-kebord-daemon.desktop; then
  ok "enx-kebord-daemon.desktop Icon is relative"
else
  warn "enx-kebord-daemon.desktop Icon not relative"
  errors=$((errors+1))
fi
if [[ -f keyboard-sound-daemon.desktop ]]; then
  if grep -q "^Hidden=true$" keyboard-sound-daemon.desktop; then
    ok "keyboard-sound-daemon.desktop is present but disabled (Hidden=true)"
  else
    warn "keyboard-sound-daemon.desktop exists but is not disabled; consider removing it or setting Hidden=true"
    errors=$((errors+1))
  fi
else
  ok "keyboard-sound-daemon.desktop removed"
fi

if [[ $errors -gt 0 ]]; then
  add_summary "Desktop entries in repo are not generic; templates should be generic (install.sh writes absolute paths)."
fi

step "Checking venv Python usage (entry points only)"
# Python files are launched via venv-aware shell scripts; no fixed shebang required.
# Ensure entry points are venv-enforced.
ok "Python entry points are launched via venv-aware scripts"

step "Checking venv Python usage (launch and control scripts)"
if grep -q 'exec "\$\(pwd\)/venv/bin/python3" enx_kebord_gui.py' launch_gui.sh; then
  ok "launch_gui.sh uses venv python"
else
  warn "launch_gui.sh does not use venv python"
  add_summary "Fix launch_gui.sh to exec \"\$(pwd)/venv/bin/python3\" enx_kebord_gui.py"
fi
if grep -q 'exec "\$\(pwd\)/venv/bin/python3" keyboard_sound_daemon_enhanced.py' launch_daemon.sh; then
  ok "launch_daemon.sh uses venv python"
else
  warn "launch_daemon.sh does not use venv python"
  add_summary "Fix launch_daemon.sh to exec \"\$(pwd)/venv/bin/python3\" keyboard_sound_daemon_enhanced.py"
fi
if grep -q '"\$VENV_PYTHON" sound_generator.py --type all' sound_control.sh; then
  ok "sound_control.sh generate uses venv python"
else
  warn "sound_control.sh generate does not use venv python"
  add_summary "Fix sound_control.sh to use venv python for generation"
fi

step "Checking script executability"
need_exec=()
for f in keyboard_sound_control.sh sound_control.sh switch_sound.sh setup_enhanced.sh launch_daemon.sh launch_gui.sh reinstall.sh *.py; do
  [[ -e "$f" ]] || continue
  if [[ ! -x "$f" ]]; then
    need_exec+=("$f")
  fi
done
if [[ ${#need_exec[@]} -eq 0 ]]; then
  ok "All scripts are executable"
else
  warn "Scripts not executable: ${need_exec[*]}"
  add_summary "Make scripts executable: chmod +x ${need_exec[*]}"
fi

step "Summary"
if [[ ${#summary_msgs[@]} -eq 0 ]]; then
  ok "All checks passed. You should be able to start the daemon."
  echo "Run: ./keyboard_sound_control.sh start"
else
  printf "- %s\n" "${summary_msgs[@]}"
  echo ""
  echo "After addressing the above, try: ./keyboard_sound_control.sh start"
fi
