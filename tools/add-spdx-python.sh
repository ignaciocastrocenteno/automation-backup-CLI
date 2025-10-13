#!/usr/bin/env bash
set -euo pipefail

# === Configurable ===
LICENSE_ID="GPL-3.0-or-later"
YEAR="$(date +%Y)"
HOLDER="Ignacio Castro Centeno"
# ====================

COPYRIGHT_LINE="# Copyright (c) ${YEAR} ${HOLDER}"
SPDX_LINE="# SPDX-License-Identifier: ${LICENSE_ID}"

export LC_ALL=C

find . -type f -name "*.py" -not -path "*/.venv/*" -print0 |
while IFS= read -r -d '' f; do
  if ! grep -q "SPDX-License-Identifier" "$f"; then
    # If there's no SPDX notice → prepend (respecting 'shebang' if exists)
    tmp="${f}.tmp.$$"
    read -r firstline < "$f" || true
    if [[ "${firstline:-}" =~ ^#! ]]; then
      {
        echo "$firstline"
        echo "$SPDX_LINE"
        echo "$COPYRIGHT_LINE"
        tail -n +2 "$f"
      } > "$tmp"
    else
      {
        echo "$SPDX_LINE"
        echo "$COPYRIGHT_LINE"
        cat "$f"
      } > "$tmp"
    fi
    mv "$tmp" "$f"
    echo "Added SPDX + copyright to: $f"
  else
    # If there's a SPDX notice → ensure copyright immediately after the first SPDX line (if missing)
    if ! grep -qE '^[#]\s*Copyright\s+\(c\)\s+[0-9]{4}\s+.+$' "$f"; then
      tmp="${f}.tmp.$$"
      awk -v spdx_re="SPDX-License-Identifier" -v cpr="$COPYRIGHT_LINE" '
        !done && $0 ~ spdx_re {
          print
          print cpr
          done=1
          next
        }
        { print }
      ' "$f" > "$tmp"
      mv "$tmp" "$f"
      echo "Inserted copyright after SPDX in: $f"
    fi
  fi
done
