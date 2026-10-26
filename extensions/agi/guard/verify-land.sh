#!/bin/sh
# verify-land.sh N LANDSHA BASE GATETIP -- held, tree, parents, G, D, anonymize, home, gpu, cite, r-land, ran as, self; one reading per line, then ONE verdict line:
# `verify-land: OK` rc 0, or `verify-land: HOLD (<checks>)` rc 1 (rc 2 = no work tree). Box-local and unreviewed until VL (council 3/3, alive 21:31:33Z 10-25):
# commit 1 was the ~/tools bytes every land L1..L132 ran; this commit gives each check its HOLD. Installed from the pin at /opt/agi/bin/verify-land (the host-act path).
# VL_T (work tree), VL_MAIN (the held refs), VL_OUT (diff + msg), VL_ANON, VL_CARRY (the pin), VL_INSTALLED, VL_TOOLS, VL_RING (r-land's ring), VL_RLAND_SINCE (L140): the lane's knobs; defaults are the live box.
N=$1 L=$2 B=$3 G=$4;T=${VL_T:-$HOME/t};MAIN=${VL_MAIN:-/data/work/agi};S=${VL_OUT:-$HOME/.verify-land};A=${VL_ANON:-$T/extensions/agi/bin/anonymize.py}
mkdir -p "$S"&&cd "$T"||exit 2
h=;hold(){ h="$h $1";}
git fetch -q origin 2>/dev/null
H=$(git -C "$MAIN" rev-parse -q --verify refs/held/sanctuary-master/$N 2>/dev/null || git rev-parse -q --verify refs/held/sanctuary-master/$N)
L=$(git rev-parse -q --verify "$L^{commit}")||{ echo "verify-land: HOLD (land unread)";exit 1;}
echo "held=$(echo $H|cut -c1-10) land=$(echo $L|cut -c1-10) $( [ "$H" = "$L" ] && echo OK || echo MISMATCH)";[ "$H" = "$L" ]||hold held
P=$(git log -1 --format=%P $L);W="$(git rev-parse -q --verify "$B^{commit}") $(git rev-parse -q --verify "$G^{commit}")"
echo "parents: $(echo $P | awk '{print substr($1,1,10), substr($2,1,10)}') want $(echo $W | awk '{print substr($1,1,10), substr($2,1,10)}')";[ "$P" = "$W" ]||hold parents
t1=$(git rev-parse $L^{tree});t2=$(git merge-tree --write-tree $B $G 2>/dev/null | head -1)
echo "tree $(echo $t1|cut -c1-10) merge-tree $(echo $t2|cut -c1-10)";[ -n "$t2" ]&&[ "$t1" = "$t2" ]||hold tree
echo "sigs: $(git log --format=%G? $B..$L | sort | uniq -c | tr '\n' ' ')";[ -z "$(git log --format=%G? $B..$L | grep -vx G)" ]||hold sigs
nd=$(git diff --name-status $B $L | grep -c '^D');echo "D: $nd  files: $(git diff --name-status $B $L | tr '\t\n' ' ')";[ "$nd" = 0 ]||hold D
git diff $B $L > "$S/$N.diff"; git log --format=%B $B..$L > "$S/$N.msg"
python3 "$A" check --diff-file "$S/$N.diff"; a=$?;echo "anon-diff=$a";[ $a = 0 ]||hold anon-diff
python3 "$A" check --text "$(grep -v -x -E 'Co-Authored-By: Claude (Opus|Sonnet|Haiku|Fable) [0-9]+\.[0-9]+ <noreply@anthropic\.com>' "$S/$N.msg")" >/dev/null; a=$?;em=$(grep -o -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$S/$N.msg" | sort -u | tr '\n' ' ')
echo "anon-msg=$a emails: $em";[ $a = 0 ]||hold anon-msg   # C4 (council 22:05:25Z) + C5 (22:16:14Z): the message minus EXACTLY the co-author trailer (model family + N.N only, so no ip hides in it) must anonymize clean
[ -z "$(printf '%s\n' $em | grep -vx 'noreply@''anthropic.com')" ]||hold msg-email   # the co-author line is the one address a land message carries
python3 -I - "$S/$N.diff" "$S/$N.msg" <<'P' || hold home
import pwd,sys
homes={p.pw_dir for p in pwd.getpwall() if len(p.pw_dir)>5 and p.pw_dir not in ('/nonexistent','/var/empty','/usr/sbin')}
hits=[h for f in sys.argv[1:] for h in homes if h+'/' in open(f,errors='replace').read()]
print('home hits', hits);sys.exit(1 if hits else 0)
P
echo "gpu: $(grep -c -i -E 'nvidia|cuda|gpu' "$S/$N.diff")"   # a reading, not a hold (as before VL)
# cite (council 3/3, alive 21:31:33Z 10-25, M10 row b): a land that changes a node file holding a `## OWNER` block (at BASE or LAND; broader than a changed
# heading, so a body edit that drops a cited chunk id is caught) runs agi-mem cite on the LAND tree; rc != 0 (a violation or unread) holds the land
o=$(for x in $(git diff --name-only $B $L -- .agi/nodes);do { git show $L:$x 2>/dev/null;git show $B:$x 2>/dev/null;}|grep -q '^## OWNER'&&echo $x;done)
if [ -n "$o" ];then w=$(mktemp -d)/land;if git worktree add -q --detach $w $L 2>/dev/null;then r=$(AGI_ENGINE=$w AGI_POST=belam agi-mem cite 2>&1);a=$?;git worktree remove --force $w
  printf '%s\n' "$r";echo "cite=$a ($(echo $o|wc -w) OWNER file(s))";[ $a = 0 ]||hold cite;else echo "cite: unread (no land worktree)";hold cite;fi
else echo "cite: n/a (no OWNER file changed)";fi
# r-land (council 3/3, alive 02:11:54Z 10-26, R4 site 2): the SAME call as SM's gate and the reference-transaction piece: BASE's guard/r-land blob on
# BASE..LAND (a range never brings its own judge), ring from VL_RING. Its lines print as they are (report mode: `would refuse` lines at rc 0 are readings
# for the [landed]); rc != 0 (an enforce refusal or unread, a BASE/TIP that does not rev-parse) HOLDS. GATE272 (council 03:49-03:5xZ 10-26): V1 no tmpfile
# HOLDS; V3 an ancestry read that errors (an unresolvable BASE) HOLDS; fail open (the hook's reading) ONLY for a BASE that does not descend L140
# (VL_RLAND_SINCE); V2' at a post-L140 BASE an ABSENT or EMPTY judge is replaced by the LAST non-empty r-land blob in BASE's history (never none, never the
# range's own: a HOLD there would lock out the restoring land, the GATE264 shape; the walk is --first-parent, or a land merge that deletes r-land,
# TREESAME to its 2nd parent, leads the walk off the trunk into the range's own history); HOLD only for what a retry clears: a read error on a present blob, a
# failed history search, no prior judge. NAMED LIMIT: a land that makes r-land a BROKEN script locks out its own repair (BASE's judge runs); the repair path
# is the stated override: the hook's hooksPath bypass (R5), and belam lifting this HOLD with the reason in the [landed].
RP=extensions/agi/guard/r-land;RS=${VL_RLAND_SINCE:-20e4947d3a0dc641340df3d07449bed0ab205325};b=$(echo $B|cut -c1-10);j=;s=$(mktemp 2>/dev/null)||s=
if [ -z "$s" ];then echo "r-land: unread (tmpfile)";hold r-land
else git merge-base --is-ancestor $RS $B 2>/dev/null;d=$?
  if [ $d != 0 ]&&[ $d != 1 ];then echo "r-land: unread (BASE $b)";hold r-land
  elif git cat-file -e $B:$RP 2>/dev/null&&! git cat-file blob $B:$RP >$s 2>/dev/null;then echo "r-land: unread (unreadable at BASE $b)";hold r-land
  elif [ -s $s ];then j=$B
  elif [ $d = 1 ];then echo "r-land: none at BASE $b (a pre-L140 BASE: fail open, as the hook)"
  elif ! hs=$(git log --first-parent --format=%H $B -- $RP 2>/dev/null);then echo "r-land: unread (history search at BASE $b)";hold r-land
  else w=$(echo "$hs"|head -1);git cat-file -e $w:$RP 2>/dev/null&&k=emptied||k=deleted
    for c in $hs;do git cat-file -e $c:$RP 2>/dev/null||continue;git cat-file blob $c:$RP >$s 2>/dev/null||{ j=x;break;};[ -s $s ]&&{ j=$c;break;};done
    [ -n "$w" ]||k=absent;case $j in x)j=;echo "r-land: unread (unreadable prior judge at $(echo $c|cut -c1-10))";hold r-land;;
      "")echo "r-land: unread (no prior judge at BASE $b)";hold r-land;;
      *)echo "r-land: judge from $(echo $j|cut -c1-10) ($k at $(echo $w|cut -c1-10))";;esac;fi
  [ -z "$j" ]||{ r=$(AGI_RING=${VL_RING:-/var/lib/agi/allowed_signers} sh $s $B $L 2>&1);a=$?;printf '%s\n' "$r";echo "r-land=$a";[ $a = 0 ]||hold r-land;};rm -f $s;fi
echo "ran as: $(id -un 2>/dev/null||echo unread) uid $(id -u)"   # M2 (council 3/3, alive 02:53:20Z 10-26): a reading, never a verdict input
# self (council VL): this copy must be the pin's repo blob, and the one on PATH; the ~/tools copy is retired
pin=$(sed -n 's/^AGI_TRUNK=//p' "${VL_CARRY:-/etc/agi/carry.env}" 2>/dev/null|tail -1);rb=$(git -C "$MAIN" show "$pin:extensions/agi/guard/verify-land.sh" 2>/dev/null|sha256sum|cut -c1-64);me=$(sha256sum <"$0"|cut -c1-64)
if [ -n "$pin" ]&&[ "$rb" = "$me" ];then echo "self: = the pin's blob ($(echo $me|cut -c1-12))";else echo "verify-land: unread (installed != repo at pin ${pin:-<none>})";hold self;fi
I=${VL_INSTALLED:-/opt/agi/bin/verify-land};c=$(command -v verify-land 2>/dev/null)
[ "$c" = "$I" ]||{ echo "verify-land: RED PATH resolves verify-land to '${c:-nothing}', not $I";hold path;}
[ ! -e "${VL_TOOLS:-$HOME/tools/verify-land.sh}" ]||{ echo "verify-land: RED the box-local copy ${VL_TOOLS:-~/tools/verify-land.sh} still exists (retire it)";hold tools-copy;}
[ -z "$h" ]&&{ echo "verify-land: OK";exit 0;};echo "verify-land: HOLD ($(echo $h))";exit 1
