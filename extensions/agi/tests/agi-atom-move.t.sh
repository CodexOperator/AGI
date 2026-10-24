#!/bin/sh
# agi-atom-move.t.sh [ROOT]: goal:g7.16.1.11.46.4 (M3) falsifier 1+2: `agi-atom move <a..> <flow>` on a scratch card + flow -- the open rows shrink by k, the flow's ARGS gain the same k slices byte-equal, the commit count is 1; the moved slices are in §7 NOWHERE (negative: grep -c of each = 0); mutant m (a move without the close) reads RED as "atom in both places".
# sh + awk + jq + git on a scratch repo; the commit step is a stub of agi-at (AGI_ATOM_COMMIT: ONE git commit of the paths it is given). ROOT = the tree whose engine-post.md carries the piece; PIECE=<file> tests a candidate. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf $D' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_ATOM_CARD AGI_ATOM_COMMIT
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
PC=${PIECE:-};[ -n "$PC" ]||{ awk '/^### agi-atom /{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/engine-post.md>$D/agi-atom;PC=$D/agi-atom;};[ -s "$PC" ]||{ echo "FAIL inputs: no agi-atom piece";exit 99;}
printf '#!/bin/sh\ncd "$AGI_T"&&git add -A -- "$@"&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm "stub agi-at: $*"\n' >$D/stub;chmod +x $D/stub
mk(){ T=$D/$1/t;rm -rf $D/$1;mkdir -p $T/.agi/nodes/goal $T/.agi/sessions/quorum;cd $T;git init -q .
 printf -- '---\nid: goal:g9\n---\n## OWNER 2026-10-23, verbatim\n> "Trajectory holds the momentum data"\nplain line two\nthird "quoted" slice & more\n\n## Other\nx\n' >.agi/nodes/goal/g9.md
 printf '# card\n\n## §0 x\nhi\n\n## §7 ATOMS\n\n| # | atom (owner ask, short) | state |\n|---|---|---|\n| 1.1 | button down | target:§0 |\n' >.agi/sessions/quorum/p.md;C=$T/.agi/sessions/quorum/p.md;AR=$T/.agi/sessions/quorum/fl.args.json
 A grandfather;for w in 'plain line two' 'Trajectory holds' 'third "quoted" slice & more' 'momentum data';do A add "$w" src:goal:g9#OWNER>/dev/null;done;git add -A;git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm base;}
A(){ (cd $T;env AGI_T=$T AGI_POST=p AGI_LAP=5 HOME=$D AGI_ATOM_COMMIT=$D/stub sh ${PIECE_RUN:-$PC} "$@") 2>$D/err;}
opens(){ grep -c '^| a[0-9]* | .* | target:' $C;}
nc(){ git -C $T rev-list --count HEAD;}
mk a;o0=$(opens);c0=$(nc);A move a1 a3 fl;rc=$?
ok "move-rc-0 the move answers 0 (rc $rc)" '[ $rc = 0 ]'
ok "move-open-rows-shrink-by-k the open atoms went $o0 -> $(opens) (want -2)" '[ $(opens) = $((o0-2)) ]'
ok "move-args-gain-the-slices-byte-equal ARGS atoms[].slice = the two slices, byte for byte, quotes and & kept" '[ "$(jq -r ".atoms[].slice" $AR)" = "plain line two
third \"quoted\" slice & more" ]'
ok "move-rows-close-as-moved-flow a1 and a3 read moved:fl, a2 is still open" '[ "$(grep -c "| moved:fl |" $C)" = 2 ]&&grep -q "^| a2 | .* | target:" $C'
ok "move-one-commit the whole move is ONE commit ($c0 -> $(nc)), the tree is clean" '[ $(nc) = $((c0+1)) ]&&[ -z "$(git -C $T status --porcelain)" ]'
ok "move-negative-slice-in-section-nowhere grep -c of each moved slice over §7 is 0 (got $(grep -cF "plain line two" $C)/$(grep -cF "third \"quoted\" slice" $C))" '[ "$(grep -cF "plain line two" $C)" = 0 ]&&[ "$(grep -cF "third \"quoted\" slice" $C)" = 0 ]'
ok "move-keeps-source-and-hash the closed row keeps src: and carries the slice hash in place of the slice" 'grep -q "^| a1 | \"sha:[0-9a-f]\{12\}\" | src:goal:g9#OWNER | moved:fl |" $C&&[ "$(jq -r ".atoms[0].sha" $AR)" = "$(printf %s "plain line two"|sha256sum|cut -c1-12)" ]'
A move a1 fl;rc=$?;ok "move-twice-REFUSED a row already moved does not move again (rc $rc)" '[ $rc != 0 ]&&[ "$(jq ".atoms|length" $AR)" = 2 ]'
mk b;c0=$(nc);A move 1.1 fl;rc=$?;ok "move-grandfathered-REFUSED a src:doc row is a paraphrase, not a slice: refused (rc $rc)" '[ $rc != 0 ]&&[ $(nc) = $c0 ]'
A move a9 fl;rc=$?;ok "move-absent-row-REFUSED (rc $rc)" '[ $rc != 0 ]&&[ $(nc) = $c0 ]'
A move a1 'Bad Flow';rc=$?;ok "move-bad-flow-name-REFUSED (rc $rc)" '[ $rc != 0 ]&&[ $(nc) = $c0 ]'
A move a1 fl ../x.json;rc=$?;ok "move-args-path-outside-t-REFUSED (rc $rc)" '[ $rc != 0 ]&&[ $(nc) = $c0 ]'
mk c;A move a1 fl .agi/sessions/quorum/other.args.json;ok "move-args-path-is-an-argument an explicit ARGS file under ~/t is used (atoms: $(jq ".atoms|length" $T/.agi/sessions/quorum/other.args.json))" '[ "$(jq ".atoms|length" $T/.agi/sessions/quorum/other.args.json)" = 1 ]'
mk d;printf '{"k":1,"atoms":[{"id":"x","src":"s","slice":"keep","sha":"h"}]}\n'>$AR;A move a1 fl;ok "move-appends-to-existing-ARGS an ARGS file with other keys and atoms keeps them (k + 2 atoms)" '[ "$(jq -r ".k" $AR)" = 1 ]&&[ "$(jq ".atoms|length" $AR)" = 2 ]'
# --- mutant m: a move that writes ARGS but does not close the rows leaves each atom in two places
M=$D/m;awk '/^move\)/{m=1}m&&/mv "\$A.n" "\$A";for i in/{sub(/;for i in \$a;do h=.*done$/,"")}1' $PC>$M;mk e;PIECE_RUN=$M A move a1 fl;n=$(opens)
ok "m-move-without-the-close-RED the mutant leaves a1 open AND in ARGS (open rows $n, want 4): the 'atom in both places' check catches it" '[ "$n" = 4 ]&&[ "$(jq ".atoms|length" $AR)" = 1 ]&&grep -qF "plain line two" $C'
echo "agi-atom-move.t.sh: $f FAIL";exit $f
