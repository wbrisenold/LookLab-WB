#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/dctl/LookLab-WB-v3.1.dctl"
DEST="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Support/LUT/Luma Color System/LookLab WB"
mkdir -p "$DEST"
cp "$SRC" "$DEST/"
echo "Installed LookLab WB to: $DEST"
