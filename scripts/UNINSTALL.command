#!/usr/bin/env bash
set -euo pipefail
DEST="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Support/LUT/Luma Color System/LookLab WB"
rm -rf "$DEST"
echo "Removed: $DEST"
