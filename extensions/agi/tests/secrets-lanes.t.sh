#!/bin/sh
# secrets-lanes.t.sh: goal:g7.16.1.11.46.7 (C2) falsifier 1: the three Console lane cells of config:secrets parse, a malformed cell is refused, and a Console
# key string planted in a cell is RED. sh + python3 (envfile.py itself) on a SCRATCH project built from the tree's own secrets.md; no network, no root, 0 USD. One ok/FAIL line
# per case; exit = number of FAILs. ROOT=<tree> (default: the tree this file sits in). A mutant is one edit of the scratch copy (mut); the clean row passes only when the check
# reads the real cells and the mutant row passes only when the check refuses it.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};EF=$R0/extensions/agi/bin/envfile.py;N=${SL_NODE:-$R0/.agi/nodes/.geometry/secrets.md}
[ -f $EF ]&&[ -f $N ]||{ echo "FAIL inputs: $EF $N";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
KP=sk-an;KP=${KP}t   # the key prefix is never spelled out in a file the negative grep reads
proj(){ rm -rf $T/p;mkdir -p $T/p/.agi/nodes/.geometry;echo '{"metric_primary":"outcome_coverage"}'>$T/p/.agi/config.json;cat>$T/p/.agi/nodes/.geometry/secrets.md;}
chk(){ python3 $EF --lanes $T/p >$T/o 2>$T/e;rc=$?;}
# the mutants edit a BASE copy whose three workspace cells are the EMPTY literal, whatever the live node holds (filled or empty); fail closed when the base lacks them or a mut changes 0 bytes
sed -e '/^  agi-batch:/s/"workspace": "[^"]*"/"workspace": ""/' -e '/^  agi-kids:/s/"workspace": "[^"]*"/"workspace": ""/' -e '/^  agi-council:/s/"workspace": "[^"]*"/"workspace": ""/' $N>$T/base.md
nb=$(grep -c '"workspace": ""' $T/base.md);[ "$nb" = 3 ]||{ echo "FAIL fixture: the base copy holds $nb of 3 empty workspace cells";exit 99;}
mut(){ A=$1 B=$2 awk '{o="";r=$0;while((i=index(r,ENVIRON["A"]))>0){o=o substr(r,1,i-1) ENVIRON["B"];r=substr(r,i+length(ENVIRON["A"]))}print o r}' $T/base.md|proj;cmp -s $T/base.md $T/p/.agi/nodes/.geometry/secrets.md&&{ echo "FAIL fixture: mut matched nothing [$1]";exit 99;};}
# --- the real node
proj <$N;chk
ok "lanes-a-the-real-three-cells-parse rc $rc: $(cat $T/o|cut -c1-90)" '[ $rc = 0 ]&&grep -q "^\[lanes\] ok: agi-batch, agi-kids, agi-council" $T/o'
ok "lanes-a-the-real-node-names-no-console-key grep -c = $(grep -c "$KP" $N) (want 0)" '[ "$(grep -c "$KP" $N)" = 0 ]'
# --- a good id, option B, and an empty cell all parse
mut '{"workspace": "", "unit": "agi-batch.service"}' '{"workspace": "wrkspc_01AbC9", "unit": "agi-batch.service"}';chk
ok "lanes-b-a-wrkspc-id-parses rc $rc" '[ $rc = 0 ]'
mut '{"workspace": "", "unit": "agi-kids.service"}' '{"scoped_key": "claude-kids", "unit": "agi-kids.service"}';chk
ok "lanes-b-option-b-scoped-key-parses rc $rc" '[ $rc = 0 ]'
# --- refusals: each names the lane and the key, rc 1
mut '{"workspace": "", "unit": "agi-batch.service"}' '{"workspace": "wrkspc-bad id", "unit": "agi-batch.service"}';chk
ok "lanes-c-a-malformed-workspace-id-is-refused rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "lane agi-batch: .workspace. is not" $T/e'
mut '{"workspace": "", "unit": "agi-council.service"}' '{"workspace": "", "scoped_key": "x", "unit": "agi-council.service"}';chk
ok "lanes-c-both-workspace-and-scoped-key-is-refused rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "lane agi-council: exactly one of" $T/e'
mut '{"workspace": "", "unit": "agi-kids.service"}' '{"workspace": "", "unit": "agi-kids"}';chk
ok "lanes-c-a-unit-without-dot-service-is-refused rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "lane agi-kids: .unit. is not" $T/e'
mut '  agi-council: {"workspace": "", "unit": "agi-council.service"}' '';chk
ok "lanes-c-a-missing-lane-is-refused rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "lane agi-council: no cell" $T/e'
# --- the mutant: a Console key string planted in a cell (the check must go RED = rc 1 naming the line, never the line)
K="${KP}-api03-CANARYCANARYCANARY"
mut '{"workspace": "", "unit": "agi-batch.service"}' "{\"workspace\": \"$K\", \"unit\": \"agi-batch.service\"}";chk
ok "lanes-d-MUTANT-a-key-planted-in-a-cell-is-RED rc $rc: $(sed -n 1p $T/e|cut -c1-90)" '[ $rc = 1 ]&&grep -q "hold a Console key string (line" $T/e'
ok "lanes-d-the-refusal-never-prints-the-key canary in stdout/stderr: $(cat $T/o $T/e|grep -c CANARY) (want 0)" '[ "$(cat $T/o $T/e|grep -c CANARY)" = 0 ]'
# the same string in the PROSE of the node (not a cell) is just as red
{ cat $N;echo "a note: $K";}|proj;chk
ok "lanes-d-a-key-in-the-prose-is-RED rc $rc" '[ $rc = 1 ]&&grep -q "hold a Console key string" $T/e'
if [ -z "$SL_INNER" ];then
# --- the fixture is INDEPENDENT of the live cells (SM finding 10-26: with the cells filled every mut matched nothing and five rows read rc 0). Rows run COPIES of this file on SCRATCH nodes holding DECOY ids
# (SL_NODE; the live file is never read), in seconds.
FR=$T/fr.md;FE=$T/fe.md;SELF=$R0/extensions/agi/tests/secrets-lanes.t.sh
sed -e '/^  agi-batch:/s/"workspace": "[^"]*"/"workspace": "wrkspc_LIVEDECOY1"/' -e '/^  agi-kids:/s/"workspace": "[^"]*"/"workspace": "wrkspc_LIVEDECOY2"/' -e '/^  agi-council:/s/"workspace": "[^"]*"/"workspace": "wrkspc_LIVEDECOY3"/' $N>$FR
cp $T/base.md $FE
slcopy(){ python3 - "$SELF" "$@" <<'P'
import sys
s=open(sys.argv[1]).read();out=sys.argv[2];pr=sys.argv[3:]
for x,y in zip(pr[0::2],pr[1::2]):
    assert x in s,"mutant target absent: "+x[:40]; s=s.replace(x,y,1)
open(out,"w").write(s)
P
}
slrun(){ ROOT=$R0 SL_INNER=1 SL_NODE=$1 sh $2 >$T/sl.out 2>&1;slrc=$?;slfail=$(grep -c '^FAIL' $T/sl.out);slok=$(grep -c '^ok' $T/sl.out);}
slrun $FR $SELF
ok "h-a-live-cells-FILLED: every row passes rc $slrc, ok $slok, FAIL lines $slfail (want 0)" '[ $slrc = 0 ]&&[ $slfail = 0 ]&&[ $slok -ge 11 ]'
slrun $FE $SELF
ok "h-a-live-cells-EMPTY: the same rows pass rc $slrc, ok $slok, FAIL lines $slfail (want 0)" '[ $slrc = 0 ]&&[ $slfail = 0 ]&&[ $slok -ge 11 ]'
slcopy $T/sl.m1.sh '$N>$T/base.md
' '$N>$T/base.md;cp $N $T/base.md
'
slrun $FR $T/sl.m1.sh
ok "h-b-the-empty-only-base-with-the-guard-stops-at-the-fixture rc $slrc (want 99): $(grep -m1 '^FAIL fixture' $T/sl.out|cut -c1-60)" '[ $slrc = 99 ]&&grep -q "^FAIL fixture: the base copy holds 0 of 3" $T/sl.out'
slcopy $T/sl.m2.sh '$N>$T/base.md
' '$N>$T/base.md;cp $N $T/base.md
' '[ "$nb" = 3 ]||' 'true||' 'cmp -s $T/base.md $T/p/' 'false $T/base.md $T/p/'
slrun $FR $T/sl.m2.sh
ok "h-c-MUTANT-empty-only-base-and-no-guards-reads-RED rc $slrc (want >0, not 99), FAIL lines $slfail: $(grep -c 'is-refused\|MUTANT' $T/sl.out) refusal rows seen" '[ $slrc -ge 1 ]&&[ $slrc != 99 ]&&grep -q "^FAIL lanes-d-MUTANT-a-key-planted-in-a-cell-is-RED" $T/sl.out'
slcopy $T/sl.m3.sh "mut '{\"workspace\": \"\", \"unit\": \"agi-batch.service\"}' '{\"workspace\": \"wrkspc_01AbC9\"" "mut '{\"workspace\": \"ZZ\", \"unit\": \"agi-batch.service\"}' '{\"workspace\": \"wrkspc_01AbC9\""
slrun $FR $T/sl.m3.sh
ok "h-d-a-mut-that-matches-nothing-stops-at-the-fixture rc $slrc (want 99): $(grep -m1 '^FAIL fixture' $T/sl.out|cut -c1-60)" '[ $slrc = 99 ]&&grep -q "^FAIL fixture: mut matched nothing" $T/sl.out'
fi
echo "secrets-lanes: $f FAIL";exit $f
