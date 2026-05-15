#!/usr/bin/env bash
set -euo pipefail
VERB="${1:?usage: delegate.sh <verb>}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF="$SKILL_DIR/lib/impeccable/reference/$VERB.md"
if [ -f "$REF" ]; then
  echo "$REF"
else
  echo "ERROR: no reference for verb '$VERB' at $REF" >&2
  exit 1
fi
