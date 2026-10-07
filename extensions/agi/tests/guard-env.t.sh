#!/bin/sh
# guard-env.t.sh: goal:g1.41 C (DG1 21:38Z; hypothesis:g141-c-guard-env-is-read-by-one-validating-parser-never-eval): the four guard scripts read config:guard's ```sh guard.env block through ONE validating loader, never eval.
# sh + bash + awk on SCRATCH nodes, no root, no mount, no systemd, no network, 0 USD. GUARD=<dir> is the guard dir under test (default: ROOT's extensions/agi/guard); the SAME file runs against the trunk's scripts (NEG) and the build. sudo / systemctl / mount / umount / runuser are STUBS on PATH that log argv. A non-root uid is required (guard-init dies for root BEFORE it reads the node).
# Contract the lane reads (c1): the loader is $GUARD/guard-env.sh, function guard_env_load <node>, it sets the GUARD_* variables in the caller; a refused line makes it return/exit non-zero with ONE message line that holds the node's file name AND the line number (of the node file, or of the block: both pass), before any stub call.
# Lanes: c1-* each hostile line (cmd subst, backtick, semicolon chain, function def, single-quoted subst, a second dollar var, a CONTROL variable GUARD_DIR pointing at decoy sibling scripts) in each of the four scripts: rc != 0, the marker file absent, the refusal names node + line, 0 stub argv. l-* the loader alone: a battery of refused shapes, the accepted shapes, c2 $HOME by string replacement (HOME=/x/y, a HOME holding a substitution, a HOME holding an ampersand), c3 the live values. s-* the scripts: a benign node passes the loader, c3 every live value through each script's cell(), no non-comment eval, one loader.
# Honest limits: NO real mount / unit write is run (that is the stubs + --dry-run), so "before any mount" is read off the stub log; guard-init's later layers and its legacy guard.env source are not covered; the ampersand row (l-home-ampersand) is beyond the brief: bash 5.2 expands & in ${v//pat/$HOME}.
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
echo "guard-env: $f FAIL"
exit $f
