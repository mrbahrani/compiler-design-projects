#!/usr/bin/env bash
# End-to-end: expr.txt -> LLVM IR -> object -> native binary -> run
# Usage: ./build_expr.sh [path/to/expr.txt] [--keep]
set -euo pipefail

EXPR_FILE="${1:-expr.txt}"
KEEP="${2:-}"
PY=python3
TINY=./tiny_compiler.py

# ---- checks ----
for tool in "$PY" llc clang; do
  command -v "$tool" >/dev/null 2>&1 || { echo "error: '$tool' not found in PATH" >&2; exit 1; }
done
[ -f "$TINY" ] || { echo "error: $TINY not found (put tiny_compiler.py next to this script)"; exit 1; }
[ -f "$EXPR_FILE" ] || { echo "error: expression file '$EXPR_FILE' not found"; exit 1; }

# ---- paths ----
base="$(basename "$EXPR_FILE" .txt)"
build_dir=".build_${base}"
mkdir -p "$build_dir"
IR="$build_dir/${base}.ll"
OBJ="$build_dir/${base}.o"
EXE="$build_dir/${base}"

# ---- compile to LLVM IR ----
echo "[1/4] Generating LLVM IR -> $IR"
$PY "$TINY" "$EXPR_FILE" -o "$IR"

# ---- object (PIC) ----
echo "[2/4] Assembling with llc (PIC) -> $OBJ"
llc -filetype=obj -relocation-model=pic "$IR" -o "$OBJ"

# ---- link (PIE by default) ----
echo "[3/4] Linking with clang -> $EXE"
clang "$OBJ" -o "$EXE"

# ---- run ----
echo "[4/4] Running $EXE"
"$EXE"

# ---- cleanup ----
if [ "$KEEP" != "--keep" ]; then
  # keep the binary, remove intermediates
  rm -f "$OBJ" "$IR"
  rmdir "$build_dir" 2>/dev/null || true
fi
