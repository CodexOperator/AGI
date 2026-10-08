#!/bin/sh
# guard-env.t.sh: goal:g1.41 C (DG1 21:38Z; hypothesis:g141-c-guard-env-is-read-by-one-validating-parser-never-eval): the four guard scripts read config:guard's ```sh guard.env block through ONE validating loader, never eval.
# sh + bash + awk on SCRATCH nodes, no root, no mount, no systemd, no network, 0 USD. GUARD=<dir> is the guard dir under test (default: ROOT's extensions/agi/guard); the SAME file runs against the trunk's scripts (NEG) and the build. sudo / systemctl / mount / umount / runuser are STUBS on PATH that log argv. A non-root uid is required (guard-init dies for root BEFORE it reads the node).
# Contract the lane reads (c1): the loader is $GUARD/guard-env.sh, function guard_env_load <node>, it sets the GUARD_* variables in the caller; a refused line makes it return/exit non-zero with ONE message line that holds the node's file name AND the line number (of the node file, or of the block: both pass), before any stub call.
# Lanes: c1-* each hostile line (cmd subst, backtick, semicolon chain, function def, single-quoted subst, a second dollar var, a CONTROL variable GUARD_DIR pointing at decoy sibling scripts) in each of the four scripts: rc != 0, the marker file absent, the refusal names node + line, 0 stub argv. l-* the loader alone: a battery of refused shapes, the accepted shapes, c2 $HOME by string replacement (HOME=/x/y, a HOME holding a substitution, a HOME holding an ampersand), c3 the live values. s-* the scripts: a benign node passes the loader, c3 every live value through each script's cell(), no non-comment eval, one loader.
# Honest limits: NO real mount / unit write is run (that is the stubs + --dry-run), so "before any mount" is read off the stub log; guard-init's later layers and its legacy guard.env source are not covered; the ampersand row (l-home-ampersand) is beyond the brief: bash 5.2 expands & in ${v//pat/$HOME}.
# RC1 + RC2 INVENTORY (DG1 23:05Z): every cell the four scripts read, and where its text ends up. Validated whole-string before use (num_cell / size_cell in guard-init: digits, one dot, M or G; a bad one is refused by name): RESERVE DOCKER_BUDGET PSI_FULL OOMD_LIMIT USER_HIGH_PCT GRACE USER_SWAP_PCT USER_SWAP_CAP AGI_MAX_PCT AGI_HIGH_PCT ENGINE_HIGH_PCT WORK_HIGH_PCT AGI_OOMD_LIMIT OOMD_SWAP_USED_PCT OOMD_PRESSURE_PCT OOMD_PRESSURE_S SYSTEM_MIN SSH_MIN CLAUDE_LOW_DIV CLAUDE_LOW_CAP USER_MIN DOCKER_CAP_HEADROOM_PCT DEFER_PCT ENGINE_MAX ENGINE_SWAP_MAX RAMDISK_SWAP_MAX RAM_BUDGET.
# FREE STRINGS (the loader admits any text of its quoted set: spaces, =, >, %, comma): (1) PEERWATCH_CLAUDE -> guard-init :237 PEER_CLAUDE -> watch.env PEER_CLAUDE= (:658) which sanctuary-watch :22-24 DOT-SOURCES, so a second word RUNS: rows rc1-*. (2) GUARD_SANCTUARY (the environment, not a block cell) -> watch.env SANCTUARY= (:657, sourced) and every installed file header: rows rc2-sanctuary-*. (3) RAM_DIR -> guard-init :235 -> ramdisk.slice comment + Description= (:504-508, unit text): rows rc2-ram-dir-*; the same cell in ram-main.sh -> systemd-escape -p -> After= / Requires= of agi-ram-main.service: row rc2-ram-main-install-unit-text; session-sweep.sh -> df. (4) RAM_SYNC_MIN -> ram-main.sh timer OnUnitActiveSec=%smin: one line, a value like '5 x' writes a broken timer, never code: NOT pinned (banked). (5) RAM_MAIN TIER_HOT TIER_COLD TIER_DIRS SWEEP_PAIRS AGI_SESSIONS_ARCHIVE CLAUDE_PROJECTS_ARCHIVE SWEEP_*_MIN SWEEP_PRESSURE_PCT -> path ARGUMENTS of rsync / mv / mkdir / mount / df (quoted; TIER_DIRS and SWEEP_PAIRS are word-split on purpose): never sourced, never unit text, but a value starting with a dash is an OPTION to rsync: NOT pinned (banked, DG1 to rule: absolute-path-only?). (6) the legacy guard.env that guard-init :183 dot-sources is outside this lane.
# Rows: rc1-* PEERWATCH_CLAUDE (block and environment) refused naming the cell, the marker absent, no raw PEER_CLAUDE line in the dry-run watch.env AND the watch.env it would write sourced under sh leaves the marker absent; controls 0 / 1 / no cell / the flag / an inherited PEER_CLAUDE. EMPTY is pinned as either refused or the default 0 (the cells convention at guard-init :190 says an empty cell takes the default; DG1's list said refuse: both pass, a raw empty or a second word never). rc2-* refused-or-inert for sinks (2) (3); rc2-i = the inventory covers every cell name found by grep. v-* (DG1 23:11Z, DG5's sink shapes) a uint cell (RAM_SYNC_MIN SWEEP_IDLE_MIN SWEEP_PRESSURE_PCT SWEEP_PRESSURE_IDLE_MIN SWEEP_CLAUDE_IDLE_MIN), an absolute-path cell (RAM_MAIN RAM_DIR TIER_HOT TIER_COLD AGI_SESSIONS_ARCHIVE CLAUDE_PROJECTS_ARCHIVE; no %), TIER_DIRS words, SWEEP_PAIRS path=>path, each given a loader-accepted wrong shape: rc != 0, the cell named, the marker absent, 0 stub argv; v-control = the valid block names no cell. NOT covered: GUARD_RAM_WORKTREES and GUARD_RAM_WT_HOLD_PCT, which no guard script reads (dispatch.py and cli.py read them through locations.guard_cell, a second parser); GUARD_SANCTUARY is covered (rc2-sanctuary-*) though DG5's list does not name it.
# RC3 (DG1 23:59Z): uint = 0 or [1-9][0-9]{0,8} (a leading zero is OCTAL in session-sweep's $(( )): 09 010 00 007 refused naming the cell for each of the 6 uint cells; bounds RAM_SYNC_MIN >= 1, SWEEP_PRESSURE_PCT 1..100, the *_IDLE_MIN cells take 0; controls 1 10 100 1440); the path kind refuses a bare / and any .. component (/a/.. /../b /a/../b) for the 7 path cells and accepts a dotted name; rc3-i diffs this file's KINDED list with the real _GE_KIND table of guard-env.sh. RC3b (DG1 00:07Z): TIER_DIRS words and SWEEP_PAIRS sides take the same two rules (rows after the path loop).
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};G=${GUARD:-$R0/extensions/agi/guard};LIVE=$R0/.agi/nodes/.geometry/guard.md
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GUARD_BOX GUARD_ENV_NODE GUARD_DIR GUARD_SANCTUARY
[ "$(id -u)" != 0 ]||{ echo "FAIL needs a non-root uid";exit 99;}
[ -f $LIVE ]&&[ -f $G/ram-main.sh ]||{ echo "FAIL inputs: node $LIVE guard dir $G";exit 99;}
mkdir -p $T/fk $T/hm $T/nd;M=$T/marker;NODEF=$T/nd/gnode-zq.md;NB=gnode-zq.md
for c in sudo mount umount runuser;do printf '#!/bin/sh\necho "%s $*" >>%s/stub\nexit 0\n' $c $T >$T/fk/$c;done
printf '#!/bin/sh\necho "systemctl $*" >>%s/stub\n[ "$1" = --version ]&&echo "systemd 255 (255.4)"\nexit 0\n' $T >$T/fk/systemctl;chmod +x $T/fk/*
# mknode FILE LINE: 33 prose lines (line 3 holds substitutions that are only prose), the fence at line 34, block lines 1-6 filler (a comment holds a substitution), block line 7 = LINE (= file line 41), line 8 filler, the fence, then a hostile line AFTER the block
mknode(){ i=1;{ while [ $i -le 33 ];do if [ $i = 3 ];then echo "prose \$(touch $M) and \`touch $M\` stay prose";else echo "prose $i";fi;i=$((i+1));done
 echo '```sh guard.env';echo '# scratch block';echo;echo 'GUARD_RAM_MAIN_local_town=';echo 'GUARD_TIER_HOT_local_town=';echo "# a comment holding \$(touch $M) and ; | & is only a comment";echo 'GUARD_SWEEP_IDLE_MIN_local_town=120';printf '%s\n' "$2";echo 'GUARD_ENGINE_MAX_local_town=3G';echo '```';echo "touch $M";} >$1;}
# runs SCRIPT ARGS: the real script under env -i, non-root, stubs first on PATH -> rc, stubn, mk (marker), the output in $T/out $T/err
runs(){ s=$1;shift;rm -f $M;: >$T/stub;(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME="${HM:-$T/hm}" GUARD_BOX=local-town GUARD_ENV_NODE=$NODEF timeout 60 bash $G/$s "$@" >$T/out 2>$T/err);rc=$?;stubn=$(wc -l <$T/stub|tr -d ' ');mk=0;[ -e $M ]&&mk=1;}
# named: ONE message line holds the node's file name and a number that is the file line (41) or the block line (7), whole number, once the path is cut out
named(){ cat $T/err $T/out 2>/dev/null|grep -F "$NB"|sed "s#$NODEF##g;s#$NB##g"|grep -Eq '(^|[^0-9])(41|7)([^0-9]|$)';}
# load NODE VAR...: the loader alone, in bash, HOME=${HM} -> lrc (91 = no guard-env.sh, 92 = guard_env_load refused), values in $T/lo, the message in $T/le
load(){ n=$1;shift;rm -f $M;(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME="${HM:-$T/hm}" bash -c '. "$1/guard-env.sh" || exit 91; guard_env_load "$2" || exit 92; shift 2; for v; do printf "%s=%s\n" "$v" "${!v-<unset>}"; done' x "$G" "$n" "$@" >$T/lo 2>$T/le);lrc=$?;mk=0;[ -e $M ]&&mk=1;}
lnamed(){ cat $T/le $T/lo 2>/dev/null|grep -F "$NB"|sed "s#$NODEF##g;s#$NB##g"|grep -Eq '(^|[^0-9])(41|7)([^0-9]|$)';}
# the six hostile lines; case 5 needs a cell the script really reads (the trunk's cell() evals it only then)
H(){ case $1 in 1)printf '%s' "GUARD_RAM_DIR_local_town=\$(touch $M)";;2)printf '%s' "GUARD_RAM_DIR_local_town=\`touch $M\`";;3)printf '%s' "GUARD_X=1; touch $M";;4)printf '%s' "printf() { touch $M; command printf \"\$@\"; }";;5)printf '%s' "GUARD_$2_local_town='\$(touch $M)'";;6)printf '%s' "GUARD_RAM_DIR_local_town='\$HOME/\$USER'";;7)printf '%s' "GUARD_DIR=$T/decoy";;esac;}
mkdir -p $T/decoy;for d in sanctuary-health sanctuary-watch;do printf '#!/bin/sh\ntouch %s\n' $M >$T/decoy/$d;chmod +x $T/decoy/$d;done   # R1: a block line that points guard-init's GUARD_DIR at decoy sibling scripts (guard-init RUNS them, even in a dry run)
SCR="ram-main.sh:status:RAM_DIR ram-tier.sh:sync:TIER_HOT session-sweep.sh:--dry-run:RAM_DIR guard-init.sh:--dry-run:RAM_DIR"
for hc in 1:command-substitution 2:backtick 3:semicolon-chain 4:function-definition 5:single-quoted-substitution 6:second-dollar-var 7:control-variable-guard-dir;do cn=${hc%%:*};cl=${hc#*:}
 for sc in $SCR;do s=${sc%%:*};r=${sc#*:};a=${r%%:*};v=${r#*:};mknode $NODEF "$(H $cn $v)";runs $s $a;nm=0;named&&nm=1
  ok "c1-$cl-${s%.sh} $s $a with the hostile node line: rc $rc (want != 0), marker $mk (want 0 = nothing ran), $stubn stub argv (want 0 = refused before any mount/sudo/systemctl), the refusal names node + line: $nm (want 1)" '[ $rc != 0 ]&&[ $mk = 0 ]&&[ $stubn = 0 ]&&[ $nm = 1 ]';done;done
# l: the loader alone
ok "l-loader-file-defines-guard_env_load $G/guard-env.sh exists and defines guard_env_load" '[ -f $G/guard-env.sh ]&&grep -Eq "^[[:space:]]*(function[[:space:]]+)?guard_env_load[[:space:]]*(\(\))?[[:space:]]*\{?" $G/guard-env.sh'
bad(){ nm=$1;mknode $NODEF "$2";load $NODEF;ln=0;lnamed&&ln=1;ok "l-refuses-$nm the line [$2] in a block: rc $lrc (want != 0 and not 91/the missing file), marker $mk (want 0), the refusal names node + line: $ln (want 1)" '[ $lrc != 0 ]&&[ $lrc != 91 ]&&[ $mk = 0 ]&&[ $ln = 1 ]';}
# badn NAME LINE VAR: a refused CONTROL name; the refusal names node + line AND the variable was never assigned in the caller (a rule applied after the assignment leaves it set)
badn(){ nm=$1;mknode $NODEF "$2";rm -f $M;(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME="$T/hm" bash -c '. "$1/guard-env.sh" || exit 91; guard_env_load "$2"; r=$?; shift 2; for v; do printf "%s=%s\n" "$v" "${!v-<unset>}"; done; exit $((r?92:0))' x "$G" "$NODEF" $3 >$T/lo 2>$T/le);lrc=$?;mk=0;[ -e $M ]&&mk=1;ln=0;lnamed&&ln=1;vs=$(sed "s/^$3=//" $T/lo)
 ok "l-refuses-the-control-name-$nm the line [$2]: rc $lrc (want 92 = refused, not 91/0), marker $mk (want 0), the refusal names node + line: $ln (want 1), $3 after the refusal [$vs] (want <unset>)" '[ $lrc = 92 ]&&[ $mk = 0 ]&&[ $ln = 1 ]&&[ "$vs" = "<unset>" ]';}
badn guard-dir 'GUARD_DIR=/x' GUARD_DIR
badn env-node 'GUARD_ENV_NODE=/x' GUARD_ENV_NODE
badn env-from 'GUARD_ENV_FROM=x' GUARD_ENV_FROM
badn env-n 'GUARD_ENV_N=1' GUARD_ENV_N
badn env-text 'GUARD_ENV_TEXT=x' GUARD_ENV_TEXT
badn box 'GUARD_BOX=x' GUARD_BOX
badn sanctuary 'GUARD_SANCTUARY=/x' GUARD_SANCTUARY
badn ram-dir-no-box-suffix 'GUARD_RAM_DIR=/x' GUARD_RAM_DIR
badn lowercase-name 'GUARD_x=1' GUARD_x
badn uppercase-suffix 'GUARD_RAM_DIR_LOCAL=/x' GUARD_RAM_DIR_LOCAL
badn leading-lowercase 'GUARD_aB_local_town=1' GUARD_aB_local_town
badn empty-name-part 'GUARD__local_town=1' GUARD__local_town
badn guard-dir-single-quoted "GUARD_DIR='/x'" GUARD_DIR
badn box-single-quoted "GUARD_BOX='x'" GUARD_BOX
bad pipe 'GUARD_RAM_DIR_local_town=a|b'
bad ampersand 'GUARD_RAM_DIR_local_town=a&b'
bad less-than 'GUARD_RAM_DIR_local_town=a<b'
bad greater-than-bare 'GUARD_RAM_DIR_local_town=a>b'
bad parenthesis 'GUARD_RAM_DIR_local_town=(a)'
bad backslash 'GUARD_RAM_DIR_local_town=a\b'
bad double-quote 'GUARD_RAM_DIR_local_town="a"'
bad double-quote-inside-single "GUARD_RAM_DIR_local_town='a\"b'"
bad single-quoted-other-dollar "GUARD_RAM_DIR_local_town='\$X'"
bad single-quoted-braced-home "GUARD_RAM_DIR_local_town='\${HOME}'"
bad single-quoted-subst "GUARD_RAM_DIR_local_town='\$(true)'"
bad single-quoted-backtick "GUARD_RAM_DIR_local_town='\`true\`'"
bad bare-dollar-home 'GUARD_RAM_DIR_local_town=$HOME'
bad unclosed-quote "GUARD_RAM_DIR_local_town='a"
bad glob 'GUARD_RAM_DIR_local_town=a*'
bad tilde 'GUARD_RAM_DIR_local_town=~/x'
bad brace 'GUARD_RAM_DIR_local_town=a{b,c}'
bad hash-in-value 'GUARD_RAM_DIR_local_town=a#b'
bad name-not-guard 'X=1'
bad bare-command-substitution 'GUARD_RAM_DIR_local_town=$(true)'
bad bare-backtick 'GUARD_RAM_DIR_local_town=`true`'
bad name-not-guard-single-quoted "X='1'"
bad export-prefix 'export GUARD_RAM_DIR_local_town=1'
bad spaces-around-equals 'GUARD_RAM_DIR_local_town = 1'
bad append-assignment 'GUARD_RAM_DIR_local_town+=1'
bad assignment-then-command "GUARD_RAM_DIR_local_town=1 touch $M"
bad bare-command "touch $M"
bad source-line '. /dev/null'
# accepted shapes + c2 + c3
EXP=$T/exp;HM=/x/y
mknode $NODEF 'GUARD_RAM_DIR_local_town=/a/B-c_d.e:f@g%h+i,j';load $NODEF GUARD_RAM_DIR_local_town GUARD_SWEEP_IDLE_MIN_local_town GUARD_RAM_MAIN_local_town GUARD_ENGINE_MAX_local_town
printf 'GUARD_RAM_DIR_local_town=/a/B-c_d.e:f@g%%h+i,j\nGUARD_SWEEP_IDLE_MIN_local_town=120\nGUARD_RAM_MAIN_local_town=\nGUARD_ENGINE_MAX_local_town=3G\n' >$EXP
ok "l-accepts-the-bare-class the whole bare class [A-Za-z0-9._:/@%+,-], an EMPTY value, blanks and comments (one holding a substitution) and the lines around: rc $lrc (want 0), marker $mk (want 0), values read back exactly" '[ $lrc = 0 ]&&[ $mk = 0 ]&&cmp -s $T/lo $EXP'
mknode $NODEF "GUARD_TIER_DIRS_local_town='\$HOME/.claude \$HOME/.pi'";load $NODEF GUARD_TIER_DIRS_local_town
ok "l-c2-home-by-string-replacement HOME=/x/y: the single-quoted \$HOME value loads as [$(cat $T/lo)] (want GUARD_TIER_DIRS_local_town=/x/y/.claude /x/y/.pi)" '[ $lrc = 0 ]&&[ "$(cat $T/lo)" = "GUARD_TIER_DIRS_local_town=/x/y/.claude /x/y/.pi" ]'
mknode $NODEF "GUARD_RAM_DIR_local_town='a b=c>d \$HOME/x \$HOME'";load $NODEF GUARD_RAM_DIR_local_town
ok "l-accepts-the-single-quoted-class a single-quoted value with a space, = and >, and two \$HOME tokens: [$(cat $T/lo)] (want a b=c>d /x/y/x /x/y)" '[ $lrc = 0 ]&&[ "$(cat $T/lo)" = "GUARD_RAM_DIR_local_town=a b=c>d /x/y/x /x/y" ]'
mknode $NODEF "GUARD_RAM_DIR_local_town=1
GUARD_RAM_DIR_local_town=2";load $NODEF GUARD_RAM_DIR_local_town
ok "l-last-assignment-wins as the old eval did: [$(cat $T/lo)] (want 2)" '[ $lrc = 0 ]&&[ "$(cat $T/lo)" = "GUARD_RAM_DIR_local_town=2" ]'
HM='/x/$(touch '$M')';mknode $NODEF "GUARD_RAM_DIR_local_town='\$HOME/q'";load $NODEF GUARD_RAM_DIR_local_town
ok "l-c2-a-home-holding-a-substitution-is-data HOME holds a command substitution: marker $mk (want 0), the value is that text verbatim" '[ $lrc = 0 ]&&[ $mk = 0 ]&&[ "$(cat $T/lo)" = "GUARD_RAM_DIR_local_town=$HM/q" ]'
HM='/x/a&b';mknode $NODEF "GUARD_RAM_DIR_local_town='\$HOME/q'";load $NODEF GUARD_RAM_DIR_local_town
ok "l-home-ampersand (beyond the brief) HOME=/x/a&b: the value is [$(cat $T/lo)] (want /x/a&b/q; bash 5.2 expands & in a bare \${v//pat/\$HOME})" '[ $lrc = 0 ]&&[ "$(cat $T/lo)" = "GUARD_RAM_DIR_local_town=/x/a&b/q" ]'
HM=/x/y
# c3: the live block, every GUARD_ assignment, the expected value computed here from the block text alone
awk '/^```sh guard.env$/{f=1;next} f&&/^```$/{exit} f' $LIVE|grep '^GUARD_' >$T/live
: >$EXP;: >$T/names;while IFS== read -r n b;do case $b in \'*) b=${b#\'};b=${b%\'};; esac;printf '%s=%s\n' "$n" "$(printf '%s' "$b"|sed 's#\$HOME#/x/y#g')" >>$EXP;echo $n >>$T/names;done <$T/live
nl=$(wc -l <$T/live|tr -d ' ')
load $LIVE $(cat $T/names)
ok "l-c3-the-live-values the $nl live assignments of the trunk guard.md (want >= 20) load to the value computed from the block text, HOME=/x/y: rc $lrc (want 0), $(diff $EXP $T/lo 2>&1|grep -c '^[<>]') differing line(s) (want 0)" '[ $lrc = 0 ]&&[ $nl -ge 20 ]&&cmp -s $T/lo $EXP'
shp=$(grep -cvE '^GUARD_[A-Z][A-Z0-9_]*_[a-z0-9][a-z0-9_]*$' $T/names)
ok "l-live-names-match-the-name-shape $shp of the $nl live names miss ^GUARD_[A-Z][A-Z0-9_]*_[a-z0-9][a-z0-9_]*\$ (want 0: the rule must never refuse the live block)" '[ $shp = 0 ]'
# s: the scripts
mknode $NODEF '';: >$T/benign
for sc in $SCR;do s=${sc%%:*};r=${sc#*:};a=${r%%:*};runs $s $a;rf=$(grep -ci 'refus' $T/err $T/out|awk -F: '{n+=$2}END{print n+0}')
 case $s in guard-init.sh)ok "s-benign-node-passes-the-loader-${s%.sh} $s $a on a benign node: marker $mk (want 0), $stubn stub argv (want >= 1: it went on to systemctl past the loader), $rf refusal line(s) (want 0)" '[ $mk = 0 ]&&[ $stubn -ge 1 ]&&[ $rf = 0 ]';;
 *)ok "s-benign-node-passes-the-loader-${s%.sh} $s $a on a benign node (empty cells, so the script says it is off): rc $rc (want 0), marker $mk (want 0), $stubn stub argv (want 0), $rf refusal line(s) (want 0)" '[ $rc = 0 ]&&[ $mk = 0 ]&&[ $stubn = 0 ]&&[ $rf = 0 ]';;esac;done
# DG1 21:46Z addendum: a block of comments + blanks only (zero assignments) is ACCEPTED (every cell() answers its default); a block with NO lines at all is the only one guard-init dies on
{ i=1;while [ $i -le 33 ];do echo "prose $i";i=$((i+1));done;echo '```sh guard.env';echo '# only a comment';echo;echo '   ';echo '# GUARD_RAM_DIR_local_town=/never';echo '```';} >$T/nd/comments.md;{ i=1;while [ $i -le 33 ];do echo "prose $i";i=$((i+1));done;echo '```sh guard.env';echo '```';} >$T/nd/nolines.md
load $T/nd/comments.md GUARD_RAM_DIR_local_town GUARD_TIER_DIRS_local_town
ok "l-comments-and-blanks-only-block-is-accepted the loader on a block of comments and blanks (one a commented-out assignment): rc $lrc (want 0), nothing set: [$(tr '\n' ' ' <$T/lo)] (want both <unset>)" '[ $lrc = 0 ]&&[ "$(cat $T/lo)" = "GUARD_RAM_DIR_local_town=<unset>
GUARD_TIER_DIRS_local_town=<unset>" ]'
for s in ram-main.sh ram-tier.sh session-sweep.sh;do pre=$(sed '/\$(cell /,$d' $G/$s);got=$(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME=/x/y GUARD_BOX=local-town GUARD_ENV_NODE=$T/nd/comments.md timeout 30 bash -c "$pre
printf '%s|%s' \"\$(cell RAM_DIR /mnt/agi-ram)\" \"\$(cell TIER_DIRS)\"" "$G/$s" 2>&1)
 ok "s-comments-only-block-answers-defaults-${s%.sh} $s on a comments-only block: cell RAM_DIR /mnt/agi-ram | cell TIER_DIRS = [$got] (want /mnt/agi-ram| )" '[ "$got" = "/mnt/agi-ram|" ]';done
NODEF=$T/nd/comments.md;runs guard-init.sh --dry-run;rf=$(grep -ci 'no .*block' $T/err|tr -d ' ')
ok "s-guard-init-accepts-a-comments-only-block guard-init.sh --dry-run: $stubn stub argv (want >= 1: past the loader), 'no block' message lines: $rf (want 0)" '[ $stubn -ge 1 ]&&[ $rf = 0 ]'
NODEF=$T/nd/nolines.md;runs guard-init.sh --dry-run;rf=$(grep -ci 'no .*block' $T/err|tr -d ' ')
ok "s-guard-init-dies-on-a-block-with-no-lines guard-init.sh --dry-run on an empty block: rc $rc (want != 0), a 'no ... block' message: $rf (want 1), $stubn stub argv (want 0)" '[ $rc != 0 ]&&[ $rf = 1 ]&&[ $stubn = 0 ]'
NODEF=$T/nd/gnode-zq.md
# c3 through each script's cell(): the prelude (up to the first use of cell) of the REAL script, then cell NAME for every live assignment
for s in ram-main.sh ram-tier.sh session-sweep.sh;do pre=$(sed '/\$(cell /,$d' $G/$s);: >$T/got;bd=0
 while IFS== read -r n b;do case $n in GUARD_*_local_town)k=local_town;;GUARD_*_encryption_town)k=encryption_town;;*)k=?;;esac;N=${n#GUARD_};N=${N%_$k};want=$(grep "^$n=" $EXP|sed "s/^$n=//")
  got=$(cd $T&&env -i PATH=$T/fk:/usr/bin:/bin HOME=/x/y GUARD_BOX=$(echo $k|tr _ -) GUARD_ENV_NODE=$LIVE timeout 30 bash -c "$pre
printf '%s' \"\$(cell $N)\"" "$G/$s" 2>/dev/null)
  [ "$got" = "$want" ]||{ bd=$((bd+1));echo "  $s cell $N: [$got] want [$want]";};done <$T/live
 ok "s-c3-the-live-values-through-cell-${s%.sh} the $nl live assignments read through $s's own cell() under HOME=/x/y: $bd differ (want 0)" '[ $bd = 0 ]&&[ $nl -ge 20 ]';done
ev=$(grep -nE '\beval\b' $G/*.sh|grep -vE ':[0-9]+:[[:space:]]*#'|wc -l|tr -d ' ')
ok "s-no-eval $ev non-comment eval line(s) in $G/*.sh (want 0; the trunk has 7)" '[ $ev = 0 ]'
ld=$(grep -lE '^[[:space:]]*(function[[:space:]]+)?guard_env_load[[:space:]]*\(\)' $G/*.sh 2>/dev/null|xargs -n1 basename 2>/dev/null|tr '\n' ' ');us=$(grep -lE 'guard_env_load[[:space:]]+"?\$' $G/guard-init.sh $G/ram-main.sh $G/ram-tier.sh $G/session-sweep.sh 2>/dev/null|wc -l|tr -d ' ')
ok "s-one-loader guard_env_load is defined in [$ld] (want exactly guard-env.sh) and CALLED by $us of the four scripts (want 4)" '[ "$ld" = "guard-env.sh " ]&&[ $us = 4 ]'
# --- RC1 + RC2 (DG1 23:05Z; SM returned lane C): a cell the loader ACCEPTS must not reach a sink that is sourced or becomes unit text as code ---
mkdir -p $T/fk2 $T/fk3 $T/th;NBX=rc.md
printf '#!/bin/sh\n[ "$1" = passwd ]&&echo "$2:x:1000:1000::%s/th:/bin/sh"\n' $T >$T/fk2/getent
printf '#!/bin/sh\necho "sudo $*" >>%s/stub\ncase $1 in tee)cat >%s/tee.out;; esac\nexit 0\n' $T $T >$T/fk3/sudo;chmod +x $T/fk2/getent $T/fk3/sudo
gnode(){ printf 'prose\n```sh guard.env\n%s\n```\n' "$1" >$T/nd/$NBX;}
wsect(){ awk -v f="$1" '$0 ~ "would (write|install) +.*"f"$"{p=1;next} p&&/^        /{sub(/^        /,"");print;next} p{exit}' $T/out;}
# gi ENV=val...: the real guard-init --dry-run (GA = other args) with getent faked to a scratch home; sets rc mk (marker after the run) w.env slice raw (PEER_CLAUDE lines other than 0 or 1) mk2 (marker after sourcing the watch.env it would write under sh) nmd (stderr names the cell or the node)
gi(){ rm -f $M $T/out $T/err;: >$T/stub;(cd $T&&env -i PATH=$T/fk2:$T/fk:/usr/bin:/bin HOME=$T/hm GUARD_BOX=local-town GUARD_ENV_NODE=$T/nd/$NBX "$@" timeout 60 bash $G/guard-init.sh ${GA:---dry-run} >$T/out 2>$T/err);rc=$?;mk=0;[ -e $M ]&&mk=1;wsect watch.env >$T/w.env;wsect ramdisk.slice >$T/slice
 raw=$(grep -E '^PEER_CLAUDE=' $T/w.env|grep -vcxE 'PEER_CLAUDE=[01]'||true);mk2=0;if [ -s $T/w.env ];then rm -f $M;(cd $T/th&&env -i PATH=/usr/bin:/bin HOME=$T/hm sh -c '. "$1"' x $T/w.env >/dev/null 2>&1);[ -e $M ]&&mk2=1;fi;nmd=0;grep -qE "PEERWATCH_CLAUDE|GUARD_SANCTUARY|SANCTUARY|RAM_DIR|$NBX" $T/err&&nmd=1;true;}
# pw NAME VALUE [ENV=val...]: PEERWATCH_CLAUDE as a block line (VALUE verbatim after the =)
pw(){ nm=$1;v=$2;shift 2;gnode "GUARD_PEERWATCH_CLAUDE_local_town=$v";gi "$@";}
bad(){ ok "rc1-$nm PEERWATCH_CLAUDE=[$v]: rc $rc (want != 0: refused), the cell or node named: $nmd (want 1), marker $mk after the run and $mk2 after sourcing the watch.env (want 0 and 0), $raw raw PEER_CLAUDE line(s) written (want 0)" '[ $rc != 0 ]&&[ $nmd = 1 ]&&[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ $raw = 0 ]';}
pw cmd-after-a-one "'1 touch $M'";bad
pw semicolon-chain "'1;touch $M'";bad
pw command-substitution "'\$(touch $M)'";bad
pw two 2;bad
pw word-yes yes;bad
pw leading-space "' 1'";bad
pw trailing-space "'1 '";bad
pw leading-zero 01;bad
pw word-true true;bad
pw two-digits "'1 2'";bad
pw empty "";ok "rc1-empty PEERWATCH_CLAUDE=[]: either refused naming the cell (rc $rc != 0, named $nmd) or taken as the default 0 like every other empty cell (rc $rc = 0, PEER_CLAUDE=0 written: $(grep -cx 'PEER_CLAUDE=0' $T/w.env)); never the raw text, marker $mk/$mk2 (want 0/0), $raw raw line(s) (want 0)" '{ [ $rc != 0 ]&&[ $nmd = 1 ]||{ [ $rc = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=0" $T/w.env)" = 1 ];};}&&[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ $raw = 0 ]'
# the same cell supplied as a raw environment variable (no block line): a newline and a substitution the loader would refuse reach hostvar directly
nl=$(printf '\n.');nl=${nl%.}
gnode "GUARD_X_local_town=1";gi "GUARD_PEERWATCH_CLAUDE_local_town=1${nl}touch $M"
ok "rc1-env-newline GUARD_PEERWATCH_CLAUDE_local_town in the environment = 1, newline, touch: rc $rc (want != 0), the cell named: $nmd (want 1), marker $mk/$mk2 (want 0/0), $raw raw line(s) (want 0)" '[ $rc != 0 ]&&[ $nmd = 1 ]&&[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ $raw = 0 ]'
gnode "GUARD_X_local_town=1";gi "GUARD_PEERWATCH_CLAUDE_local_town=\$(touch $M)"
ok "rc1-env-command-substitution the same cell in the environment = a command substitution: rc $rc (want != 0), marker $mk/$mk2 (want 0/0), $raw raw line(s) (want 0)" '[ $rc != 0 ]&&[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ $raw = 0 ]'
# controls: 0 and 1 boot, a missing cell is 0, the --peerwatch-claude flag is 1, an inherited PEER_CLAUDE variable is not read
pw zero 0;ok "rc1-control-zero PEERWATCH_CLAUDE=0: rc $rc (want 0), PEER_CLAUDE=0 written: $(grep -cx 'PEER_CLAUDE=0' $T/w.env) (want 1), raw $raw (want 0)" '[ $rc = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=0" $T/w.env)" = 1 ]&&[ $raw = 0 ]'
pw one 1;ok "rc1-control-one PEERWATCH_CLAUDE=1: rc $rc (want 0), PEER_CLAUDE=1 written: $(grep -cx 'PEER_CLAUDE=1' $T/w.env) (want 1), raw $raw (want 0)" '[ $rc = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=1" $T/w.env)" = 1 ]&&[ $raw = 0 ]'
gnode "GUARD_X_local_town=1";gi;ok "rc1-control-no-cell no PEERWATCH_CLAUDE line: rc $rc (want 0), PEER_CLAUDE=0 written: $(grep -cx 'PEER_CLAUDE=0' $T/w.env) (want 1)" '[ $rc = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=0" $T/w.env)" = 1 ]'
GA="--dry-run --peerwatch-claude";gi;GA=;ok "rc1-control-the-flag --peerwatch-claude with no cell: rc $rc (want 0), PEER_CLAUDE=1 written: $(grep -cx 'PEER_CLAUDE=1' $T/w.env) (want 1)" '[ $rc = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=1" $T/w.env)" = 1 ]'
gi "PEER_CLAUDE=1 touch $M";ok "rc1-an-inherited-PEER_CLAUDE-is-not-read PEER_CLAUDE='1 touch ..' in the environment, no cell: rc $rc (want 0), marker $mk/$mk2 (want 0/0), PEER_CLAUDE=0 written: $(grep -cx 'PEER_CLAUDE=0' $T/w.env) (want 1)" '[ $rc = 0 ]&&[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ "$(grep -cx "PEER_CLAUDE=0" $T/w.env)" = 1 ]'
# RC2: the other sinks. Each row is "refused, or reaches the sink inert"
# GUARD_SANCTUARY (the environment; guard-init writes it raw into watch.env, which sanctuary-watch dot-sources, and into every installed file header)
inert(){ ok "rc2-$nm $dsc: rc $rc, marker $mk after the run / $mk2 after sourcing the watch.env (want 0/0), refused-or-inert: $ri (want 1)" '[ $mk = 0 ]&&[ $mk2 = 0 ]&&[ $ri = 1 ]';}
gnode "GUARD_X_local_town=1";gi "GUARD_SANCTUARY=/x touch $M";nm=sanctuary-second-word;dsc="GUARD_SANCTUARY='/x touch ..' -> watch.env SANCTUARY=";ri=0;{ [ $rc != 0 ]||[ "$(grep -c '^SANCTUARY=.* ' $T/w.env)" = 0 ];}&&ri=1;inert
gnode "GUARD_X_local_town=1";gi "GUARD_SANCTUARY=\$(touch $M)";nm=sanctuary-command-substitution;dsc="GUARD_SANCTUARY=a command substitution -> watch.env SANCTUARY=";ri=1;inert
gnode "GUARD_X_local_town=1";gi "GUARD_SANCTUARY=/x${nl}ExecStart=touch $M";nm=sanctuary-newline;dsc="GUARD_SANCTUARY=/x, newline, ExecStart=.. -> every installed file";ri=0;{ [ $rc != 0 ]||[ "$(grep -c '^ *ExecStart=touch' $T/out)" = 0 ];}&&ri=1;inert
# RAM_DIR into ramdisk.slice (a comment and Description=): the block value and the environment value
RB='GUARD_RAM_BUDGET_local_town=64M'
gnode "$RB
GUARD_RAM_DIR_local_town='/x Requires=y.target'";gi;nm=ram-dir-second-word;dsc="GUARD_RAM_DIR='/x Requires=y.target' -> ramdisk.slice";ri=0;{ [ $rc != 0 ]||{ [ -s $T/slice ]&&[ "$(grep -c '^ *Requires=' $T/slice)" = 0 ]&&[ "$(grep -c '^ *\[' $T/slice)" = 2 ];};}&&ri=1;inert
gnode "$RB";gi "GUARD_RAM_DIR_local_town=/x${nl}ExecStart=touch $M";nm=ram-dir-env-newline;dsc="GUARD_RAM_DIR in the environment = /x, newline, ExecStart=.. -> ramdisk.slice";ri=0;{ [ $rc != 0 ]||{ [ -s $T/slice ]&&[ "$(grep -c '^ *ExecStart=' $T/slice)" = 0 ];};}&&ri=1;inert
gnode "$RB";gi "GUARD_RAM_DIR_local_town=\$(touch $M)";nm=ram-dir-env-command-substitution;dsc="GUARD_RAM_DIR in the environment = a command substitution -> ramdisk.slice";ri=1;inert
# RAM_DIR into ram-main.sh install (After=/Requires= through systemd-escape): the unit text goes through sudo tee (a stub that keeps stdin)
gnode "GUARD_RAM_MAIN_local_town=/x/main
GUARD_RAM_DIR_local_town='/x Requires=y.target'";rm -f $T/tee.out $M;: >$T/stub;(cd $T&&env -i PATH=$T/fk3:$T/fk:/usr/bin:/bin HOME=$T/hm GUARD_BOX=local-town GUARD_ENV_NODE=$T/nd/$NBX timeout 60 bash $G/ram-main.sh install >$T/out 2>$T/err);rc=$?;mk=0;[ -e $M ]&&mk=1;rq=$(grep -c '^Requires=' $T/tee.out 2>/dev/null);hq=$(grep -c 'Requires=y' $T/tee.out 2>/dev/null)
ok "rc2-ram-main-install-unit-text GUARD_RAM_DIR='/x Requires=y.target' -> agi-ram-main.service from ram-main.sh install: rc $rc (refused when != 0, else:), marker $mk (want 0), $rq line(s) starting Requires= (want 1: the escaped mount unit only), $hq raw 'Requires=y' (want 0)" '[ $mk = 0 ]&&{ [ $rc != 0 ]||{ [ "$rq" = 1 ]&&[ "$hq" = 0 ];};}'
# v: DG5's sink-shape classes (DG1 23:11Z) -- a uint cell, an absolute-path cell, TIER_DIRS paths, SWEEP_PAIRS path=>path: a loader-accepted value of the wrong shape is refused naming the cell, before any stub call and with the marker absent. Valid siblings are in the block so no script exits early as "off".
BASEB="GUARD_RAM_MAIN_local_town=/x/main
GUARD_RAM_DIR_local_town=/x/ram
GUARD_TIER_HOT_local_town=/x/hot
GUARD_TIER_COLD_local_town=/x/cold
GUARD_TIER_DIRS_local_town='/x/d1 /x/d2'
GUARD_AGI_SESSIONS_ARCHIVE_local_town=/x/a
GUARD_CLAUDE_PROJECTS_ARCHIVE_local_town=/x/c
GUARD_SWEEP_PAIRS_local_town='/x/s=>/x/t'"
# vrow CELL SCRIPT ACTION NAME VALUE: BASEB with CELL overridden by the last line
vrow(){ gnode "$BASEB
GUARD_$1_local_town=$5";NODEF=$T/nd/$NBX;runs $2 $3;vn=0;grep -q "$1" $T/err $T/out&&vn=1
 ok "v-$4-$1-in-${2%.sh} GUARD_$1_local_town=[$5] read by $2 $3: rc $rc (want != 0), the cell named: $vn (want 1), marker $mk (want 0), $stubn stub argv (want 0: refused before any side effect)" '[ $rc != 0 ]&&[ $vn = 1 ]&&[ $mk = 0 ]&&[ $stubn = 0 ]';}
for pc in RAM_MAIN:ram-main.sh:status RAM_DIR:ram-main.sh:status RAM_DIR:session-sweep.sh:--dry-run TIER_HOT:ram-tier.sh:status TIER_COLD:ram-tier.sh:status AGI_SESSIONS_ARCHIVE:session-sweep.sh:--dry-run CLAUDE_PROJECTS_ARCHIVE:session-sweep.sh:--dry-run;do c=${pc%%:*};r=${pc#*:};s=${r%%:*};a=${r#*:}
 vrow $c $s $a relative rel/path;vrow $c $s $a leading-dash "'--log-file=/x'";vrow $c $s $a percent '/x/%n';vrow $c $s $a second-word "'/x /y'";vrow $c $s $a redirect "'/x>/y'";done
for u in RAM_SYNC_MIN:ram-main.sh:status SWEEP_IDLE_MIN:session-sweep.sh:--dry-run SWEEP_PRESSURE_PCT:session-sweep.sh:--dry-run SWEEP_PRESSURE_IDLE_MIN:session-sweep.sh:--dry-run SWEEP_CLAUDE_IDLE_MIN:session-sweep.sh:--dry-run;do c=${u%%:*};r=${u#*:};s=${r%%:*};a=${r#*:}
 vrow $c $s $a second-word "'5 x'";vrow $c $s $a negative -1;vrow $c $s $a letters x;vrow $c $s $a decimal 5.5;vrow $c $s $a hex 0x10;vrow $c $s $a two-numbers "'1 2'";done
vrow TIER_DIRS ram-tier.sh status relative-word "'/x/d1 rel'";vrow TIER_DIRS ram-tier.sh status dash-word "'/x/d1 --log-file=/x'";vrow TIER_DIRS ram-tier.sh status percent-word "'/x/d1 /x/%n'"
vrow SWEEP_PAIRS session-sweep.sh --dry-run no-arrow /x/a;vrow SWEEP_PAIRS session-sweep.sh --dry-run empty-dest "'/x/a=>'";vrow SWEEP_PAIRS session-sweep.sh --dry-run empty-source "'=>/x/b'";vrow SWEEP_PAIRS session-sweep.sh --dry-run relative-source "'rel=>/x/b'";vrow SWEEP_PAIRS session-sweep.sh --dry-run relative-dest "'/x/a=>rel'";vrow SWEEP_PAIRS session-sweep.sh --dry-run second-pair-bad "'/x/a=>/x/b rel=>/x/c'"
# controls: the valid block names no cell on stderr in any script (a validator that refuses a good value is as wrong as one that accepts a bad one)
for sc in ram-main.sh:status ram-tier.sh:status session-sweep.sh:--dry-run;do s=${sc%%:*};a=${sc#*:};gnode "$BASEB
GUARD_SWEEP_PAIRS_local_town='/x/s=>/x/t /x/u=>/x/v'";NODEF=$T/nd/$NBX;runs $s $a;vn=$(grep -cE 'GUARD_[A-Z_]+_local_town|RAM_MAIN|RAM_DIR|TIER_|ARCHIVE|SWEEP_|SYNC_MIN' $T/err||true)
 ok "v-control-the-valid-block-in-${s%.sh} the valid block (absolute paths, two SWEEP_PAIRS, TIER_DIRS with two words) read by $s $a: marker $mk (want 0), $vn stderr line(s) naming a cell (want 0: nothing refused)" '[ $mk = 0 ]&&[ $vn = 0 ]';done
# RC3 (DG1 23:59Z; union3 returned lane C): a uint is 0 or [1-9][0-9]{0,8} (a leading zero is OCTAL to session-sweep.sh's $(( )): SWEEP_PRESSURE_PCT=09 dies "value too great for base" exactly under pressure, 010 makes stop_at=-2 and the early stop never fires); bounds RAM_SYNC_MIN >= 1 (a 0-minute timer period is degenerate), SWEEP_PRESSURE_PCT 1..100, the *_IDLE_MIN cells and RAM_WT_HOLD_PCT take 0; the path kind refuses a bare / and any .. component (a hostile node write could aim RAM_DIR at / or /a/../b in a mount argv)
# vok CELL SCRIPT ACTION NAME VALUE: the value is NOT refused: the cell is not named on stderr (rc is free: the fixture has no mounts)
vok(){ gnode "$BASEB
GUARD_$1_local_town=$5";NODEF=$T/nd/$NBX;runs $2 $3;vn=0;grep -q "GUARD_$1_local_town" $T/err&&vn=1
 ok "rc3-$4-$1-in-${2%.sh} GUARD_$1_local_town=[$5] read by $2 $3: the cell named on stderr: $vn (want 0: accepted), marker $mk (want 0)" '[ $vn = 0 ]&&[ $mk = 0 ]';}
UCELLS="RAM_SYNC_MIN:ram-main.sh:status SWEEP_IDLE_MIN:session-sweep.sh:--dry-run SWEEP_PRESSURE_PCT:session-sweep.sh:--dry-run SWEEP_PRESSURE_IDLE_MIN:session-sweep.sh:--dry-run SWEEP_CLAUDE_IDLE_MIN:session-sweep.sh:--dry-run RAM_WT_HOLD_PCT:ram-main.sh:status"
for u in $UCELLS;do c=${u%%:*};r=${u#*:};s=${r%%:*};a=${r#*:}
 for z in 09 010 00 007;do vrow $c $s $a leading-zero-$z "'$z'";done
 case $c in SWEEP_PRESSURE_PCT|RAM_WT_HOLD_PCT)vs="1 10 100";; *)vs="1 10 100 1440";; esac;for v in $vs;do vok $c $s $a control-$v "'$v'";done;done
vrow RAM_SYNC_MIN ram-main.sh status zero "'0'";vrow SWEEP_PRESSURE_PCT session-sweep.sh --dry-run zero "'0'";vrow SWEEP_PRESSURE_PCT session-sweep.sh --dry-run above-100 "'101'"
for c in SWEEP_IDLE_MIN SWEEP_PRESSURE_IDLE_MIN SWEEP_CLAUDE_IDLE_MIN;do vok $c session-sweep.sh --dry-run zero-is-allowed "'0'";done
for pc in RAM_MAIN:ram-main.sh:status RAM_DIR:ram-main.sh:status RAM_DIR:session-sweep.sh:--dry-run RAM_WORKTREES:ram-main.sh:status TIER_HOT:ram-tier.sh:status TIER_COLD:ram-tier.sh:status AGI_SESSIONS_ARCHIVE:session-sweep.sh:--dry-run CLAUDE_PROJECTS_ARCHIVE:session-sweep.sh:--dry-run;do c=${pc%%:*};r=${pc#*:};s=${r%%:*};a=${r#*:}
 vrow $c $s $a bare-slash "'/'";vrow $c $s $a dotdot-last '/a/..';vrow $c $s $a dotdot-first '/../b';vrow $c $s $a dotdot-middle '/a/../b';vok $c $s $a control-a-dotted-name '/a/b..c/d.e';done
# RC3b (DG1 00:07Z): the same two rules on the words of TIER_DIRS and the sides of SWEEP_PAIRS (a bare / and any .. component); controls: the loader-expanded $HOME forms and a dotted name
vrow TIER_DIRS ram-tier.sh status bare-slash "'/'";vrow TIER_DIRS ram-tier.sh status bare-slash-second-word "'/a /'";vrow TIER_DIRS ram-tier.sh status dotdot-first-word "'/a/.. /b'";vrow TIER_DIRS ram-tier.sh status dotdot-last-word "'/b /a/..'";vrow TIER_DIRS ram-tier.sh status dotdot-middle "'/a/../b /c'"
vrow SWEEP_PAIRS session-sweep.sh --dry-run dotdot-source "'/a/..=>/b'";vrow SWEEP_PAIRS session-sweep.sh --dry-run bare-slash-dest "'/a=>/'";vrow SWEEP_PAIRS session-sweep.sh --dry-run bare-slash-source "'/=>/b'";vrow SWEEP_PAIRS session-sweep.sh --dry-run dotdot-dest "'/a=>/b/..'";vrow SWEEP_PAIRS session-sweep.sh --dry-run dotdot-second-pair "'/a=>/b /c=>/d/../e'"
vok TIER_DIRS ram-tier.sh status control-home-words "'\$HOME/x \$HOME/y'";vok TIER_DIRS ram-tier.sh status control-dotted-names "'/a/b..c /d/.e'";vok TIER_DIRS ram-tier.sh status control-trailing-slash "'/a/ /b/'"
vok SWEEP_PAIRS session-sweep.sh --dry-run control-home-pair "'\$HOME/a=>\$HOME/b'";vok SWEEP_PAIRS session-sweep.sh --dry-run control-dotted-pairs "'/a/b..c=>/d/.e /f=>/g/h..'";vok SWEEP_PAIRS session-sweep.sh --dry-run control-trailing-slash-pair "'/a/=>/b/'"
# the kind table the scripts really use (source guard-env.sh, declare -p _GE_KIND) against the cells and kinds the rows above drive
KINDED=" PEERWATCH_CLAUDE:bool RAM_SYNC_MIN:uint SWEEP_IDLE_MIN:uint SWEEP_PRESSURE_PCT:uint SWEEP_PRESSURE_IDLE_MIN:uint SWEEP_CLAUDE_IDLE_MIN:uint RAM_WT_HOLD_PCT:uint RAM_MAIN:path RAM_DIR:path RAM_WORKTREES:path TIER_HOT:path TIER_COLD:path AGI_SESSIONS_ARCHIVE:path CLAUDE_PROJECTS_ARCHIVE:path TIER_DIRS:paths SWEEP_PAIRS:pairs "
real=$(bash -c '. "$1/guard-env.sh" && for c in "${!_GE_KIND[@]}";do echo "$c:${_GE_KIND[$c]}";done' x "$G" 2>/dev/null|sort|tr '\n' ' ');mine=$(for k in $KINDED;do echo $k;done|sort|tr '\n' ' ')
ok "rc3-i-the-kind-table-is-the-one-the-rows-drive guard-env.sh's _GE_KIND has $(echo $real|wc -w|tr -d ' ') cell(s); this file drives $(echo $mine|wc -w|tr -d ' '); the table and the rows differ by [$(for k in $real;do case "$KINDED" in *" $k "*);;*)echo -n "+$k ";; esac;done;for k in $mine;do case " $real" in *" $k "*);;*)echo -n "-$k ";; esac;done)] (want none: add a kinded cell to KINDED with its rows, or remove it from both)" '[ -n "$real" ]&&[ "$real" = "$mine" ]'
# i: the inventory (header) names every cell the four scripts read, so a new free-string cell cannot arrive unlisted
INV=" AGI_HIGH_PCT AGI_MAX_PCT AGI_OOMD_LIMIT AGI_SESSIONS_ARCHIVE CLAUDE_LOW_CAP CLAUDE_LOW_DIV CLAUDE_PROJECTS_ARCHIVE DEFER_PCT DOCKER_BUDGET DOCKER_CAP_HEADROOM_PCT ENGINE_HIGH_PCT ENGINE_MAX ENGINE_SWAP_MAX GRACE OOMD_LIMIT OOMD_PRESSURE_PCT OOMD_PRESSURE_S OOMD_SWAP_USED_PCT PEERWATCH_CLAUDE PSI_FULL RAM_BUDGET RAM_DIR RAMDISK_SWAP_MAX RAM_MAIN RAM_SYNC_MIN RESERVE SSH_MIN SWEEP_CLAUDE_IDLE_MIN SWEEP_IDLE_MIN SWEEP_PAIRS SWEEP_PRESSURE_IDLE_MIN SWEEP_PRESSURE_PCT SYSTEM_MIN TIER_COLD TIER_DIRS TIER_HOT USER_HIGH_PCT USER_MIN USER_SWAP_CAP USER_SWAP_PCT WORK_HIGH_PCT "
seen=$({ grep -ohE '\b(hostvar|cell) [A-Z][A-Z0-9_]*' $G/*.sh|awk '{print $2}';grep -ohE '\b(num|size)_cell [A-Za-z_]+ [A-Z][A-Z0-9_]*' $G/*.sh|awk '{print $3}';}|sort -u);un=;for c in $seen;do case "$INV" in *" $c "*);;*)un="$un $c";; esac;done
ok "rc2-i-the-inventory-names-every-cell the cells the four scripts read through hostvar / cell / num_cell / size_cell: $(echo $seen|wc -w|tr -d ' ') (want >= 38), not in this file's inventory:$un (want none: classify the new cell in the header, then add it to INV)" '[ -z "$un" ]&&[ $(echo $seen|wc -w) -ge 38 ]'
echo "guard-env: $f FAIL"
exit $f
