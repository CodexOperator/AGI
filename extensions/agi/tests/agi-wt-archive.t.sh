#!/bin/sh
# agi-wt-archive.t.sh: T1 of goal:g7.16.1.11.16 — shell twin of test_agi_wt_archive.py
# Each process case is env -i + its own HOME. Never writes the caller's tree.
# One ok/FAIL line per named case; exit = FAIL count. sh + git; no python.
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
GEO=$R0/.agi/nodes/.geometry
sect(){ cat "$R0"/.agi/nodes/.geometry/engine*.md | sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"; }

# f3 / r2: read-only
u=$(cat "$GEO/engine-root.md")
ok "f3_unit_keeps_runtime_dir_across_restart" 'printf %s "$u" | grep -q "RuntimeDirectory=agi-%i" && printf %s "$u" | grep -q "RuntimeDirectoryPreserve=restart"'
ns=$(sed -n 's/^SWEEP_ARCHIVE_NS = "\([^"]*\)".*/\1/p' "$R0/extensions/agi/bin/heal.py" | head -1)
wt=$(sect agi-wt)
ok "r2_one_namespace_with_heal" '[ -n "$ns" ] && printf %s "$wt" | grep -q "update-ref ${ns}\$s@"'

BASE=$(mktemp -d)
trap 'rm -rf "$BASE"' 0
BIN=$BASE/bin
mkdir -p "$BIN"
for n in agi-wt agi-flush agi-turn agi-link; do
  sect "$n" >"$BIN/$n"; chmod +x "$BIN/$n"
done

# env -i runner: $1 = case name, remaining env KEY=val, stdin = script
runiso(){
  name=$1; shift
  home=$BASE/$name/home; rt=$BASE/$name/rt
  mkdir -p "$home/t/.agi/nodes" "$rt"
  env -i HOME="$home" RUNTIME_DIRECTORY="$rt" AGI_WT_HOLD=101 USER=u1 \
    PATH="$BIN:/usr/bin:/bin" \
    GIT_AUTHOR_NAME=a GIT_AUTHOR_EMAIL=a@t.invalid \
    GIT_COMMITTER_NAME=a GIT_COMMITTER_EMAIL=a@t.invalid \
    GIT_CONFIG_GLOBAL=/dev/null \
    "$@" \
    /bin/sh
}

NODE='---
id: doc:t1
mint_id: m1
---
body
'

# shared prelude written into each case
PRE='
set -e
cd "$HOME/t"
git init -q
printf "%s\n" '"'$NODE'"' >.agi/nodes/n.md
git add -A
git commit -qm base
d=$(agi-wt pull doc:t1)
'

runiso f1 AGI_SEAT=p1 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
set +e
out=\$(agi-wt drop doc:t1); rc=\$?
set -e
echo \$rc >"\$RUNTIME_DIRECTORY/../rc"
printf '%s\n' "\$out" >"\$RUNTIME_DIRECTORY/../out"
git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"\$RUNTIME_DIRECTORY/../show"
git status --porcelain -- .agi >"\$RUNTIME_DIRECTORY/../porc"
rm -rf "\$RUNTIME_DIRECTORY"
git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"\$HOME/../after"
EOS
ok "f1_drop_rc4_moved" '[ "$(cat "$BASE/f1/rc")" = 4 ] && grep -q moved "$BASE/f1/out"'
ok "f1_archive_has_edit" 'grep -q edited "$BASE/f1/show"'
ok "f1_porcelain_clean" '[ ! -s "$BASE/f1/porc" ]'
ok "f1_survives_stop" 'grep -q edited "$BASE/f1/after"'

runiso f2 AGI_SEAT=p1 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
set +e
out=\$(agi-wt drop doc:t1); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
[ -d "\$d" ] && echo yes >"\$HOME/../exists" || echo no >"\$HOME/../exists"
git show HEAD:.agi/nodes/n.md >"\$HOME/../head"
git for-each-ref refs/archive >"\$HOME/../refs"
EOS
ok "f2_clean_tree_drops_as_today" '[ "$(cat "$BASE/f2/rc")" = 0 ] && [ "$(cat "$BASE/f2/exists")" = no ] && grep -q edited "$BASE/f2/head" && [ ! -s "$BASE/f2/refs" ]'

runiso r1 AGI_SEAT=p1 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
mkdir -p .git/refs/archive/worktrees
: >.git/refs/archive/worktrees/p1@m1.lock
set +e
out=\$(agi-wt drop doc:t1 2>"\$HOME/../err"); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
printf '%s\n' "\$out" >"\$HOME/../out"
EOS
ok "r1_failed_archive_is_loud_and_not_4" '[ "$(cat "$BASE/r1/rc")" = 5 ] && grep -q "agi-wt: archive of doc:t1 failed" "$BASE/r1/err" && ! grep -q moved "$BASE/r1/out"'

runiso m1a AGI_POST=p2 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
set +e
out=\$(agi-wt drop doc:t1); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
git for-each-ref --format='%(refname)' refs/archive >"\$HOME/../ref"
EOS
ok "m1_identity_post_wins" '[ "$(cat "$BASE/m1a/rc")" = 4 ] && [ "$(cat "$BASE/m1a/ref")" = refs/archive/worktrees/p2@m1 ]'

runiso m1b <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
set +e
out=\$(agi-wt drop doc:t1 2>"\$HOME/../err"); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
git for-each-ref refs/archive >"\$HOME/../refs"
EOS
ok "m1_none_refuses" '[ "$(cat "$BASE/m1b/rc")" = 5 ] && grep -q "no AGI_POST/AGI_SEAT" "$BASE/m1b/err" && [ ! -s "$BASE/m1b/refs" ]'

runiso m3 AGI_SEAT=p1 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
set +e
out=\$(agi-flush); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
git show refs/archive/worktrees/p1@m1:.agi/nodes/n.md >"\$HOME/../show"
EOS
ok "m3_agi_flush_archives_moved_tree_end_to_end" '[ "$(cat "$BASE/m3/rc")" = 0 ] && grep -q edited "$BASE/m3/show"'

runiso g83 AGI_SEAT=p1 <<EOS
$PRE
printf '%s\nedited\n' '$NODE' >"\$d/.agi/nodes/n.md"
printf '%s\ntrunk\n' '$NODE' >.agi/nodes/n.md
git commit -qam move
mkdir -p .git/refs/archive/worktrees
: >.git/refs/archive/worktrees/p1@m1.lock
set +e
out=\$(agi-flush 2>"\$HOME/../err"); rc=\$?
set -e
echo \$rc >"\$HOME/../rc"
[ -d "\$d" ] && echo yes >"\$HOME/../exists" || echo no >"\$HOME/../exists"
EOS
ok "g83_agi_flush_exits_5_when_a_drop_exits_5" '[ "$(cat "$BASE/g83/rc")" = 5 ] && grep -q "agi-wt: archive of m1 failed" "$BASE/g83/err" && [ "$(cat "$BASE/g83/exists")" = yes ]'
exit $f
