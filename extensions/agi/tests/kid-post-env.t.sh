#!/bin/sh
# kid-post-env.t.sh: goal:g7.16.1.11.24 falsifiers 1 + 2 (belam-s2-II 02:4xZ 10-10, the kid half): a post's hand `box` finds its post, and a KID's env resolves to the KID for every identity reader.
# sh + git + jq + ssh-keygen + python3 on a SCRATCH repo, throwaway keys, no real pane, no live ref. The envs are NEVER hand-written and this lane exports AGI_POST nowhere:
#   POST env = the words of the agi-post@.service `Environment=` line of engine-root.md (%i -> the post name), minus PATH   (UNITFILE=<file> reads another unit text)
#   KID env  = the words of agi-kid's own `exec pi` line that read AGI_*=$k ($k -> kid9), applied ON TOP of the post env   (AGIKID=<file> tests another agi-kid piece)
# `box n` = the REAL box piece of ROOT's engine*.md (BOX=<file> another). One ok/FAIL line per case; exit = FAIL count.
# Cases: f1a the unit line carries AGI_SEAT=<name> AND AGI_POST=<name> · f1b `env -i` with ONLY that line, `box n` has no 'parameter not set' and lists the sender of a SIGNED refs/box/belam/alive (rc 0) ·
#   f1c agi-kid's exec line carries AGI_POST=$k (non-vacuous: the kid words were found) · f1d the kid env: `box n` lists NOTHING (rc 0), `box read` advances no held ref of the parent · f1e send.py's resolved sender (AGI_AGENT_ID unset) is the post in the post env and the KID in the kid env ·
#   f2 every AGI_POST= value in engine-root.md is %i, and the rendered AGI_SEAT and AGI_POST differ for no name.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};GEO=$R0/.agi/nodes/.geometry;BIN=$R0/extensions/agi/bin
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -n "$BOX" ]||{ sect box>$T/box;BOX=$T/box;}
[ -n "$AGIKID" ]||{ sect agi-kid>$T/agi-kid;AGIKID=$T/agi-kid;}
[ -n "$UNITFILE" ]||UNITFILE=$GEO/engine-root.md
[ -s $BOX ]&&[ -s $AGIKID ]&&[ -s $UNITFILE ]||{ echo "FAIL extract: box $(wc -c<$BOX) agi-kid $(wc -c<$AGIKID) unit $(wc -c<$UNITFILE)";exit 99;}
unitenv(){ grep -m1 '^Environment=.*AGI_SEAT=%i' $UNITFILE|sed 's/^Environment=//'|tr ' ' '\n'|grep -v '^PATH='|sed "s/%i/$1/g";}
kidenv(){ grep 'exec pi' $AGIKID|tr ' ' '\n'|grep -E '^AGI_[A-Z_]+=\$k$'|sed "s/\\\$k/$1/";}
# fixture: belam <- council (inert) <- alive; signer keys; belam sends one signed message to alive (the setup sender, not the subject)
mkdir $T/k $T/c;: >$T/signers
for u in belam alive;do
 ssh-keygen -q -t ed25519 -N '' -f $T/k/$u -C $u>/dev/null;echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/$u.pub)">>$T/signers
 printf '[user]\n\tname=%s\n\temail=%s@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[gpg "ssh"]\n\tallowedSignersFile=%s\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $u $u $T/k/$u $T/signers>$T/c/$u
done
$G init -q $T/r;mkdir -p $T/r/.agi/nodes/.geometry
cat >$T/r/.agi/nodes/.geometry/posts.md<<'POSTS'
  - {"name":"belam","parent":"owner","harness":"claude"}
  - {"name":"council","parent":"belam","members":["alive"]}
  - {"name":"alive","parent":"council","harness":"claude"}
POSTS
(cd $T/r&&$G add -A&&$G -c user.name=t -c user.email=t@t commit -q -m fixture)
BASE="HOME=$T PATH=/usr/bin:/bin:/usr/local/bin AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/alive GIT_CONFIG_SYSTEM=/dev/null"
(cd $T/r&&printf 'hello\n'|env -i HOME=$T PATH=/usr/bin:/bin:/usr/local/bin AGI_TRUNK=HEAD GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=$T/c/belam GIT_CONFIG_SYSTEM=/dev/null AGI_POST=belam sh $BOX send alive)
[ -n "$($G -C $T/r for-each-ref refs/box/belam/alive)" ]||{ echo "FAIL fixture: no signed refs/box/belam/alive";exit 99;}
as(){ w=$1;shift;(cd $T/r&&env -i $BASE $(unitenv alive) "$@" sh -c 'exec "$0" "$@"' sh $BOX "$w" 2>$T/err);}   # as VERB [kid words..]: the post env, then any kid words on top, then box VERB
UE=$(unitenv alive)
ok "f1a-unit-line-carries-both the agi-post@.service Environment= line renders AGI_SEAT=alive AND AGI_POST=alive: [$(echo $UE)]" 'echo "$UE"|grep -qx AGI_SEAT=alive&&echo "$UE"|grep -qx AGI_POST=alive'
o=$(as n);rc=$?
ok "f1b-hand-box-finds-its-post env -i with ONLY the unit line: box n exits $rc (want 0), says 'parameter not set' $(grep -c 'parameter not set' $T/err) time(s) (want 0), and lists belam (the signed sender): [$o]" '[ $rc = 0 ]&&! grep -q "parameter not set" $T/err&&[ "$o" = belam ]'
KW=$(kidenv kid9)
ok "f1c-agi-kid-exec-line-carries-AGI_POST agi-kid's own exec line reads [$(echo $KW)] (want AGI_SEAT=kid9 AGI_POST=kid9): the kid words were found and carry AGI_POST" 'echo "$KW"|grep -qx AGI_POST=kid9&&echo "$KW"|grep -qx AGI_SEAT=kid9'
ko=$(as n $KW);krc=$?
ok "f1d-kid-box-n-lists-nothing the kid env (the post env, then agi-kid's words on top): box n lists [$ko] (want nothing) rc $krc (want 0), where the parent's env lists belam" '[ $krc = 0 ]&&[ -z "$ko" ]'
as read $KW >/dev/null;kh=$($G -C $T/r for-each-ref refs/held|wc -l|tr -d ' ')
ok "f1d-kid-box-read-advances-no-parent-ref the kid's box read leaves $kh held ref(s) (want 0): it did not act as alive" '[ "$kh" = 0 ]'
as read >/dev/null;ph=$($G -C $T/r for-each-ref refs/held|wc -l|tr -d ' ');$G -C $T/r for-each-ref --format='%(refname)' refs/held|while read r;do $G -C $T/r update-ref -d $r;done
ok "f1d-witness-the-parent-read-advances the SAME box read in the parent's own env leaves $ph held ref (want 1), so the kid row above can fail" '[ "$ph" = 1 ]'
py(){ env -i $BASE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$BIN $(unitenv alive) "$@" python3 -c 'import send;print(send._detect_sender(None))' 2>/dev/null;}
ps=$(py);pk=$(py $KW)
ok "f1e-send-py-sender-is-the-kid send.py's resolved sender (AGI_AGENT_ID unset): the post env says [$ps] (want alive), the kid env says [$pk] (want kid9)" '[ "$ps" = alive ]&&[ "$pk" = kid9 ]'
bad=$(grep -o 'AGI_POST=[^ ]*' $UNITFILE|grep -v '^AGI_POST=%i$'|sort -u|tr '\n' ' ')
ok "f2-only-%i-in-engine-root every AGI_POST= value in engine-root.md is %i: [${bad% }] (want none)" '[ -z "$bad" ]'
d=;for n in alive dg1 belam sm all-is-one;do u=$(unitenv $n);[ "$(echo "$u"|grep '^AGI_SEAT='|cut -d= -f2)" = "$(echo "$u"|grep '^AGI_POST='|cut -d= -f2)" ]&&[ -n "$(echo "$u"|grep '^AGI_POST=')" ]||d="$d $n";done
ok "f2-seat-equals-post the rendered AGI_SEAT and AGI_POST are both present and differ for no instance name: differing [${d# }] (want none)" '[ -z "$d" ]'
echo "kid-post-env: $f FAIL";exit $f
