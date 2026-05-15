#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="sprout-design"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
REPO_URL="https://github.com/baguskto/sprout-design-skill.git"

command -v git >/dev/null || { echo "git required"; exit 1; }

if [ -d "$SKILL_DIR" ]; then
  BACKUP_DIR="$HOME/.claude/skills-backups"
  mkdir -p "$BACKUP_DIR"
  BACKUP="$BACKUP_DIR/$SKILL_NAME.backup-$(date +%Y%m%d_%H%M%S)"
  echo "Existing install found, backing up to $BACKUP"
  mv "$SKILL_DIR" "$BACKUP"
fi

git clone --depth 1 "$REPO_URL" "$SKILL_DIR"

chmod +x "$SKILL_DIR/scripts/"*.sh "$SKILL_DIR/scripts/"*.py 2>/dev/null || true

echo ""
echo "=== API Key Setup ==="
echo "sprout-design uses GPT Image 2 (text-heavy assets) and Gemini Nano Banana (photos)."
echo ""

if [ ! -f "$HOME/.gpt-image/config.json" ]; then
  read -p "Set up OpenAI API key now? (y/N): " setup_openai
  if [ "${setup_openai:-N}" = "y" ] || [ "${setup_openai:-N}" = "Y" ]; then
    python3 "$SKILL_DIR/lib/gpt-image/scripts/setup.py"
  else
    echo "Skipped. Run later: python3 $SKILL_DIR/lib/gpt-image/scripts/setup.py"
  fi
fi

if [ -z "${GOOGLE_AI_API_KEY:-}" ]; then
  read -p "Set up Gemini API key now? (y/N): " setup_gemini
  if [ "${setup_gemini:-N}" = "y" ] || [ "${setup_gemini:-N}" = "Y" ]; then
    python3 "$SKILL_DIR/lib/banana/scripts/setup_mcp.py"
  else
    echo "Skipped. Run later: python3 $SKILL_DIR/lib/banana/scripts/setup_mcp.py"
  fi
fi

echo ""
echo "Installed: $SKILL_DIR"
echo "Try: /sprout-design teach (in a project root)"
