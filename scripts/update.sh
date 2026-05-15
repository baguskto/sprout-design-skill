#!/usr/bin/env bash
set -euo pipefail
cd "$HOME/.claude/skills/sprout-design"
git pull --ff-only
chmod +x scripts/*.sh scripts/*.py 2>/dev/null || true
echo "sprout-design updated to $(git rev-parse --short HEAD)"
