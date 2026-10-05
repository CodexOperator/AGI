#!/bin/sh
# project-agi-box.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_project_agi_box.py
# (drop-in carries AGI_BOX=<row box>; old agi-project bytes lack it).
# One ok/FAIL line per pytest case; exit = FAIL count. sh + git + jq + sed; 0 python.
# ROOT = working tree; OLD = tip whose engine.md agi-project lacks AGI_BOX= in the drop-in.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
OLD=${OLD:-6b536b730}
GEO=.agi/nodes/.geometry
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
command -v jq >/dev/null || { echo "FAIL jq-absent"; exit 99; }
# project BOX [ENGINE.md]: scratch repo of current engine*.md + one claude-code v4 row; run ### agi-project; print h.conf
project(){
  box=$1; eng=$2
  d=$(mktemp -d)
  mkdir -p "$d/repo/$GEO" "$d/out"
  cp "$R0/$GEO"/engine*.md "$d/repo/$GEO/"
  [ -n "$eng" ] && cp "$eng" "$d/repo/$GEO/engine.md"
  printf -- '---\nposts:\n  - {"name": "t1", "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "harness": "claude-code", "box": "%s"}\n' "$box" >"$d/repo/$GEO/posts.md"
  git -C "$d/repo" init -q
  git -C "$d/repo" add -A
  git -C "$d/repo" -c user.name=t -c user.email=t.invalid commit -qm x
  sect=$(sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}' "$d/repo/$GEO/engine.md")
  printf '%s\n' "$sect" | (cd "$d/repo" && env PATH=/usr/bin:/bin AGI_BOX="$box" sh -s "$d/out" HEAD)
  rc=$?
  if [ $rc -ne 0 ]; then echo "PROJECT_RC=$rc" >&2; rm -rf "$d"; return 1; fi
  cat "$d/out/agi-post@t1.service.d/h.conf"
  rm -rf "$d"
}
for box in local-town other-town; do
  conf=$(project "$box") || conf=
  ok "dropin_carries_agi_box $box" 'printf %s "$conf" | grep -q "AGI_BOX=$box" && printf %s "$conf" | grep -q "AGI_ROLE=director" && printf %s "$conf" | grep -q "AGI_LADDER_TIER=1"'
done
oldf=$(mktemp)
if git -C "$R0" show "$OLD:$GEO/engine.md" >"$oldf" 2>/dev/null && [ -s "$oldf" ]; then
  conf=$(project local-town "$oldf") || conf=
  ok "old_bytes_lack_agi_box" '! printf %s "$conf" | grep -q AGI_BOX'
else
  echo "FAIL old_bytes_lack_agi_box missing-tip $OLD"
  f=$((f+1))
fi
rm -f "$oldf"
exit $f
