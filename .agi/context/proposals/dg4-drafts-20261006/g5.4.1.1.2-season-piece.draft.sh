#!/bin/sh
# season judge REPORT [--against PLAN] [--actor POST] [--session S]
# SoT: engine-post.md ### season -> /var/lib/agi/$P/bin/season (NOT extensions/agi/bin/season)
# exits 0 stamped+read-back lens non-empty · 1 [refused] · 2 usage
P=${AGI_POST:?}
T=${AGI_TRUNK:-HEAD}
refuse(){ echo "[refused] $*" >&2; exit 1; }
usage(){ echo "usage: season judge REPORT [--against PLAN] [--actor POST] [--session S]" >&2; exit 2; }
[ "$1" = judge ] || usage
shift
R=${1:?}; shift || true
A=; ACT=$P; SESS=
while [ $# -gt 0 ]; do
  case $1 in
    --against) A=${2:?}; shift 2;;
    --actor) ACT=${2:?}; shift 2;;
    --session) SESS=${2:?}; shift 2;;
    -h|--help) usage;;
    *) usage;;
  esac
done
[ "$ACT" = "$P" ] || refuse "actor $ACT != AGI_POST $P"
SEASON=$(git show "$T:.agi/nodes/.geometry/ladder.md" | sed -n "s/^current_season: //p" | head -1)
[ -n "$SEASON" ] || refuse "ladder current_season unreadable on $T"
RP=$(git grep -l --full-name "^id: ${R}$" "$T" -- .agi/nodes 2>/dev/null | head -1 | sed "s|^$T:||")
[ -n "$RP" ] || refuse "report $R not found on $T"
NODE=$(git show "$T:$RP")
TYPE=$(printf "%s\n" "$NODE" | sed -n "s/^type: //p" | head -1)
[ -n "$TYPE" ] || refuse "report $R has no type"
if [ -z "$A" ]; then
  A=$(printf "%s\n" "$NODE" | awk "/^parents:/{p=1;next} p&&/^  - /{gsub(/^  - /,\"\");print;exit} p&&/^[^ ]/{exit}")
  [ -n "$A" ] || refuse "no --against and no parents on $R"
fi
AP=$(git grep -l --full-name "^id: ${A}$" "$T" -- .agi/nodes 2>/dev/null | head -1 | sed "s|^$T:||")
[ -n "$AP" ] || refuse "against $A not found on $T"
LENS=$(git show "$T:$AP" | awk "/^parents:/{p=1;next} p&&/^  - /{gsub(/^  - /,\"\"); if(\$0~/^(goal|vision):/){print;exit}} p&&/^[^ ]/{exit}")
[ -n "$LENS" ] || refuse "empty lens — against $A has no goal/vision parent"
WARGS="--set judged_against=$A --set lens=$LENS --set season=$SEASON --actor $ACT"
[ -n "$SESS" ] && WARGS="$WARGS --session $SESS"
if command -v write.py >/dev/null 2>&1; then W=write.py
elif [ -x "${AGI_BIN:-/var/lib/agi/$P/bin}/write.py" ]; then W=${AGI_BIN:-/var/lib/agi/$P/bin}/write.py
else refuse "write.py not found"; fi
$W "$R" $WARGS || refuse "write failed for $R"
TIP=$(git rev-parse -q --verify HEAD 2>/dev/null || echo "$T")
RB=$(git show "$TIP:$RP" 2>/dev/null || git show "$T:$RP")
printf "%s\n" "$RB" | grep -q "^judged_against: ${A}$" || refuse "read-back judged_against mismatch"
printf "%s\n" "$RB" | grep -q "^lens: ${LENS}$" || refuse "read-back lens mismatch/empty"
printf "%s\n" "$RB" | grep -q "^season: ${SEASON}$" || refuse "read-back season mismatch"
echo "Judgment stamped on $R: judged_against=$A lens=$LENS season=$SEASON"
exit 0
