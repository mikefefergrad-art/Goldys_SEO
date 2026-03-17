#!/bin/bash
set -euo pipefail

# Only run in Claude Code remote environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

REPO_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"

echo "Installing Python dependencies for Claude SEO..."

# Install pip dependencies from requirements.txt
pip install -q -r "$REPO_DIR/claude-seo/requirements.txt"

echo "Dependencies installed successfully."
