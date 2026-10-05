#!/bin/sh
# agi-wt-archive.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_agi_wt_archive.py
# (moved claimed tree archived to refs/archive/worktrees/<post>@<mint> before drop exits 4).
# One ok/FAIL line per named case; exit = FAIL count. sh + git; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
GEO=$R0/.agi/nodes/.geometry
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
MAIL='a@t.invalid'
NODE='---
id: doc:t1
mint_id: m1
---
body
'
# setup DIR: writes pieces into DIR/bin, inits DIR/home/t, pulls doc:t1; prints g-env via files
setup(){
  base=$1
  home=$base/home; rt=$base/rt; bin=$base/bin
  mkdir -p "$home/t/.agi/nodes" "$rt" "$bin"
  for n in agi-wt agi-flush agi-turn agi-link; do
    sect "$n" >"$bin/$n"; chmod +x "$bin/$n"
  done
  export HOME=$home RUNTIME_DIRECTORY=$rt AGI_SEAT=p1 AGI_WT_HOLD=101 USER=u1
  export PATH="$bin:$PATH"
  export GIT_AUTHOR_NAME=a GIT_AUTHOR_EMAIL=$MAIL GIT_COMMITTER_NAME=a GIT_COMMITTER_EMAIL=$MAIL
  export GIT_CONFIG_GLOBAL=/dev/null
  t=$home/t
  git -C "$t" init -q
  printf '%s\n' "$NODE" >"$t/.agi/nodes/n.md"
  git -C "$t" add -A
  git -C "$t" commit -qm base
  d=$(agi-wt pull doc:t1)
  echo "$d"
}
g(){ (cd "$HOME/t" && "$@"); }
move(){
  d=$1
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  g git commit -qam move
}

# f3: unit text, no process
u=$(cat "$GEO/engine-root.md")
ok "f3_unit_keeps_runtime_dir_across_restart" 'printf %s "$u" | grep -q "RuntimeDirectory=agi-%i" && printf %s "$u" | grep -q "RuntimeDirectoryPreserve=restart"'

# r2: one namespace with heal
ns=$(sed -n 's/^SWEEP_ARCHIVE_NS = "\([^"]*\)".*/\1/p' "$R0/extensions/agi/bin/heal.py" | head -1)
wt=$(sect agi-wt)
ok "r2_one_namespace_with_heal" '[ -n "$ns" ] && printf %s "$wt" | grep -q "update-ref ${ns}\$s@"'

BASE=$(mktemp -d)
trap 'rm -rf "$BASE"' 0

# f1
d=$(setup "$BASE/f1")
move "$d"
r=$(g agi-wt drop doc:t1); rc=$?
out=$r
ok "f1_drop_rc4_moved" '[ $rc -eq 4 ] && printf %s "$out" | grep -q moved'
ok "f1_archive_has_edit" 'g git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md | grep -q edited'
ok "f1_porcelain_clean" '[ -z "$(g git status --porcelain -- .agi)" ]'
rm -rf "$RUNTIME_DIRECTORY"
ok "f1_survives_stop" 'g git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md | grep -q edited'

# f2
unset AGI_POST
export AGI_SEAT=p1
d=$(setup "$BASE/f2")
printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
r=$(g agi-wt drop doc:t1); rc=$?
ok "f2_clean_tree_drops_as_today" '[ $rc -eq 0 ] && [ ! -d "$d" ] && g git show HEAD:.agi/nodes/n.md | grep -q edited && [ -z "$(g git for-each-ref refs/archive)" ]'

# r1
d=$(setup "$BASE/r1")
move "$d"
mkdir -p "$HOME/t/.git/refs/archive/worktrees"
: >"$HOME/t/.git/refs/archive/worktrees/p1@m1.lock"
r=$(g agi-wt drop doc:t1 2>"$BASE/r1.err"); rc=$?
ok "r1_failed_archive_is_loud_and_not_4" '[ $rc -eq 5 ] && grep -q "agi-wt: archive of doc:t1 failed" "$BASE/r1.err" && ! printf %s "$r" | grep -q moved'

# m1 identity post wins
unset AGI_SEAT
export AGI_POST=p2
d=$(setup "$BASE/m1a")
move "$d"
r=$(g agi-wt drop doc:t1); rc=$?
ref=$(g git for-each-ref --format='%(refname)' refs/archive)
ok "m1_identity_post_wins" '[ $rc -eq 4 ] && [ "$ref" = refs/archive/worktrees/p2@m1 ]'

unset AGI_SEAT AGI_POST
d=$(setup "$BASE/m1b")
move "$d"
r=$(g agi-wt drop doc:t1 2>"$BASE/m1b.err"); rc=$?
ok "m1_none_refuses" '[ $rc -eq 5 ] && grep -q "no AGI_POST/AGI_SEAT" "$BASE/m1b.err" && [ -z "$(g git for-each-ref refs/archive)" ]'

# m3 flush archives
export AGI_SEAT=p1
unset AGI_POST
d=$(setup "$BASE/m3")
move "$d"
r=$(g agi-flush); rc=$?
ok "m3_agi_flush_archives_moved_tree_end_to_end" '[ $rc -eq 0 ] && g git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md | grep -q edited'

# g83 flush exits 5
d=$(setup "$BASE/g83")
move "$d"
mkdir -p "$HOME/t/.git/refs/archive/worktrees"
: >"$HOME/t/.git/refs/archive/worktrees/p1@m1.lock"
r=$(g agi-flush 2>"$BASE/g83.err"); rc=$?
ok "g83_agi_flush_exits_5_when_a_drop_exits_5" '[ $rc -eq 5 ] && grep -q "agi-wt: archive of m1 failed" "$BASE/g83.err" && [ -d "$d" ]'
exit $f
