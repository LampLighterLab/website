#!/bin/sh
set -eu
cd "$(git rev-parse --show-toplevel)"
existing_hooks=$(git config --get core.hooksPath || true)
if [ -n "$existing_hooks" ] && [ "$existing_hooks" != .githooks ]; then
  echo "Existing hooks path: $existing_hooks. Integrate .githooks/pre-commit with your hooks before changing it." >&2
  exit 1
fi
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Python 3.11 or newer is required.")'
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
git config core.hooksPath .githooks
echo "Installed: staged portraits will be prepared automatically on commit; files over 1 MiB will be rejected."
