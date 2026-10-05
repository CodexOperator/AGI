#!/bin/sh
# agi-wt-archive.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_agi_wt_archive.py
# Isolated: each case is a subshell with its own HOME. Never writes the caller's tree.
# One ok/FAIL line per named case; exit = FAIL count. sh + git; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
GEO=$R0/.agi/nodes/.geometry
sect(){ cat "$R0"/.agi/nodes/.geometry/engine*.md | sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }
MAIL='a@t.invalid'
NODE='---
id: doc:t1
mint_id: m1
---
body
'

# f3 / r2: read-only, no process
u=$(cat "$GEO/engine-root.md")
ok "f3_unit_keeps_runtime_dir_across_restart" 'printf %s "$u" | grep -q "RuntimeDirectory=agi-%i" && printf %s "$u" | grep -q "RuntimeDirectoryPreserve=restart"'
ns=$(sed -n 's/^SWEEP_ARCHIVE_NS = "\([^"]*\)".*/\1/p' "$R0/extensions/agi/bin/heal.py" | head -1)
wt=$(sect agi-wt)
ok "r2_one_namespace_with_heal" '[ -n "$ns" ] && printf %s "$wt" | grep -q "update-ref ${ns}\$s@"'

BASE=$(mktemp -d)
trap 'rm -rf "$BASE"' 0

# one isolated tree: prints the pulled dir on stdout; env lives in the subshell
case_env(){
  # $1 = case dir under BASE
  base=$1
  home=$base/home; rt=$base/rt; bin=$base/bin
  mkdir -p "$home/t/.agi/nodes" "$rt" "$bin"
  for n in agi-wt agi-flush agi-turn agi-link; do
    sect "$n" >"$bin/$n"; chmod +x "$bin/$n"
  done
  HOME=$home RUNTIME_DIRECTORY=$rt AGI_WT_HOLD=101 USER=u1
  PATH="$bin:$PATH"
  GIT_AUTHOR_NAME=a GIT_AUTHOR_EMAIL=$MAIL GIT_COMMITTER_NAME=a GIT_COMMITTER_EMAIL=$MAIL
  GIT_CONFIG_GLOBAL=/dev/null
  export HOME RUNTIME_DIRECTORY AGI_WT_HOLD USER PATH GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_CONFIG_GLOBAL
  [ -n "$AGI_POST" ] && export AGI_POST
  [ -n "$AGI_SEAT" ] && export AGI_SEAT
  t=$home/t
  git -C "$t" init -q
  printf '%s\n' "$NODE" >"$t/.agi/nodes/n.md"
  git -C "$t" add -A
  git -C "$t" commit -qm base
  agi-wt pull doc:t1
}

# f1
(
  AGI_SEAT=p1; unset AGI_POST
  d=$(case_env "$BASE/f1")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  out=$(agi-wt drop doc:t1); rc=$?
  echo "$rc" >"$BASE/f1.rc"
  printf '%s\n' "$out" >"$BASE/f1.out"
  git -C "$HOME/t" show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"$BASE/f1.show" 2>"$BASE/f1.err"
  git -C "$HOME/t" status --porcelain -- .agi >"$BASE/f1.porc"
  rm -rf "$RUNTIME_DIRECTORY"
  git -C "$HOME/t" show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"$BASE/f1.after"
)
ok "f1_drop_rc4_moved" '[ "$(cat "$BASE/f1.rc")" = 4 ] && grep -q moved "$BASE/f1.out"'
ok "f1_archive_has_edit" 'grep -q edited "$BASE/f1.show"'
ok "f1_porcelain_clean" '[ ! -s "$BASE/f1.porc" ]'
ok "f1_survives_stop" 'grep -q edited "$BASE/f1.after"'

# f2
(
  AGI_SEAT=p1; unset AGI_POST
  d=$(case_env "$BASE/f2")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  out=$(agi-wt drop doc:t1); rc=$?
  echo "$rc" >"$BASE/f2.rc"
  [ -d "$d" ] && echo yes >"$BASE/f2.exists" || echo no >"$BASE/f2.exists"
  git -C "$HOME/t" show HEAD:.agi/nodes/n.md >"$BASE/f2.head"
  git -C "$HOME/t" for-each-ref refs/archive >"$BASE/f2.refs"
)
ok "f2_clean_tree_drops_as_today" '[ "$(cat "$BASE/f2.rc")" = 0 ] && [ "$(cat "$BASE/f2.exists")" = no ] && grep -q edited "$BASE/f2.head" && [ ! -s "$BASE/f2.refs" ]'

# r1
(
  AGI_SEAT=p1; unset AGI_POST
  d=$(case_env "$BASE/r1")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  mkdir -p "$HOME/t/.git/refs/archive/worktrees"
  : >"$HOME/t/.git/refs/archive/worktrees/p1@m1.lock"
  out=$(agi-wt drop doc:t1 2>"$BASE/r1.err"); rc=$?
  echo "$rc" >"$BASE/r1.rc"
  printf '%s\n' "$out" >"$BASE/r1.out"
)
ok "r1_failed_archive_is_loud_and_not_4" '[ "$(cat "$BASE/r1.rc")" = 5 ] && grep -q "agi-wt: archive of doc:t1 failed" "$BASE/r1.err" && ! grep -q moved "$BASE/r1.out"'

# m1 post wins
(
  AGI_POST=p2; unset AGI_SEAT
  d=$(case_env "$BASE/m1a")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  out=$(agi-wt drop doc:t1); rc=$?
  echo "$rc" >"$BASE/m1a.rc"
  git -C "$HOME/t" for-each-ref --format='%(refname)' refs/archive >"$BASE/m1a.ref"
)
ok "m1_identity_post_wins" '[ "$(cat "$BASE/m1a.rc")" = 4 ] && [ "$(cat "$BASE/m1a.ref")" = refs/archive/worktrees/p2@m1 ]'

# m1 none refuses
(
  unset AGI_SEAT AGI_POST
  d=$(case_env "$BASE/m1b")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  out=$(agi-wt drop doc:t1 2>"$BASE/m1b.err"); rc=$?
  echo "$rc" >"$BASE/m1b.rc"
  git -C "$HOME/t" for-each-ref refs/archive >"$BASE/m1b.refs"
)
ok "m1_none_refuses" '[ "$(cat "$BASE/m1b.rc")" = 5 ] && grep -q "no AGI_POST/AGI_SEAT" "$BASE/m1b.err" && [ ! -s "$BASE/m1b.refs" ]'

# m3 flush archives
(
  AGI_SEAT=p1; unset AGI_POST
  d=$(case_env "$BASE/m3")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  out=$(agi-flush); rc=$?
  echo "$rc" >"$BASE/m3.rc"
  git -C "$HOME/t" show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"$BASE/m3.show"
)
ok "m3_agi_flush_archives_moved_tree_end_to_end" '[ "$(cat "$BASE/m3.rc")" = 0 ] && grep -q edited "$BASE/m3.show"'

# g83 flush exits 5
(
  AGI_SEAT=p1; unset AGI_POST
  d=$(case_env "$BASE/g83")
  printf '%s\nedited\n' "$NODE" >"$d/.agi/nodes/n.md"
  printf '%s\ntrunk\n' "$NODE" >"$HOME/t/.agi/nodes/n.md"
  git -C "$HOME/t" commit -qam move
  mkdir -p "$HOME/t/.git/refs/archive/worktrees"
  : >"$HOME/t/.git/refs/archive/worktrees/p1@m1.lock"
  out=$(agi-flush 2>"$BASE/g83.err"); rc=$?
  echo "$rc" >"$BASE/g83.rc"
  [ -d "$d" ] && echo yes >"$BASE/g83.exists" || echo no >"$BASE/g83.exists"
)
ok "g83_agi_flush_exits_5_when_a_drop_exits_5" '[ "$(cat "$BASE/g83.rc")" = 5 ] && grep -q "agi-wt: archive of m1 failed" "$BASE/g83.err" && [ "$(cat "$BASE/g83.exists")" = yes ]'
exit $f
