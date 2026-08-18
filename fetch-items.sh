#!/usr/bin/env bash
# Downloads every item image ETC needs into ./items/
#
# Run this once from the root of your repo, then commit the items/ folder.
# After that the calculator serves the art from your own site and never
# depends on anyone else's server staying up.
#
#   bash fetch-items.sh
#
# Source: warerastats.io. Worth a word of thanks to them.

set -u
SRC="https://warerastats.io/items"
OUT="items"
mkdir -p "$OUT"

SLOTS="helmet chest boots gloves pants"
WEAPONS="gun sniper tank knife"

ok=0
missing=""

grab() {
  local code="$1"
  local url="$SRC/$code.png"
  if curl -fsSL -o "$OUT/$code.png" "$url"; then
    printf '  %-12s ok\n' "$code"
    ok=$((ok + 1))
  else
    printf '  %-12s NOT FOUND\n' "$code"
    rm -f "$OUT/$code.png"
    missing="$missing $code"
  fi
}

echo "Equipment (six tiers each)"
for slot in $SLOTS; do
  for tier in 1 2 3 4 5 6; do
    grab "$slot$tier"
  done
done

echo
echo "Weapons"
for w in $WEAPONS; do
  grab "$w"
done

echo
echo "Downloaded $ok files into $OUT/"
if [ -n "$missing" ]; then
  echo "Missing:$missing"
  echo "Those codes may not exist, or may be named differently."
else
  echo "Everything found."
fi
echo
echo "Now: git add items && git commit -m 'Add item art' && git push"
