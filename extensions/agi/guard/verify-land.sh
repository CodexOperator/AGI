#!/bin/sh
# verify-land.sh N LANDSHA BASE GATETIP -- held, wrap, tree, parents, G, D, anonymize, home, gpu, cite, r-land, ran as, self; one reading per line, then ONE verdict line:
# `verify-land: OK` rc 0, or `verify-land: HOLD (<checks>)` rc 1 (rc 2 = no work tree). Box-local and unreviewed until VL (council 3/3, alive 21:31:33Z 10-25):
# commit 1 was the ~/tools bytes every land L1..L132 ran; this commit gives each check its HOLD. Installed from the pin at /opt/agi/bin/verify-land (the host-act path).
# VL_T (work tree), VL_MAIN (the held refs), VL_OUT (diff + msg), VL_ANON, VL_CARRY (the pin), VL_INSTALLED, VL_TOOLS, VL_RING (r-land's ring), VL_RLAND_SINCE (L140), VL_WRAP_SIGNER + VL_LAND_SIGNER (R3's
# principals): the lane's knobs; defaults are the live box. `verify-land.sh wrap N L BASE GATETIP` = the WRAP step (below): prints `land: plain <L>` or makes
# W and prints `land: wrap <W> over <L> (<why>)`; it moves no ref (the CAS to that sha stays belam's step), then verify-land runs on that sha.
N=$1 L=$2 B=$3 G=$4;T=${VL_T:-$HOME/t};MAIN=${VL_MAIN:-/data/work/agi};S=${VL_OUT:-$HOME/.verify-land};A=${VL_ANON:-$T/extensions/agi/bin/anonymize.py}
mkdir -p "$S"&&cd "$T"||exit 2
h=;hold(){ h="$h $1";}
# WRAP (owner ruling (1) 05:0xZ 10-26 "Yeah you can land"; council 3/3 alive 05:18:24Z + [correction] 05:19:08Z; THE list 06:06:56Z): a RULES land moves the
# trunk to W = commit-tree L^{tree} -p BASE -p L -S (belam-signed, adds no change), never to L: the first-parent lander is belam (written_by), SM's signed L
# stays W's 2nd parent. L1 RULES = `git diff --name-only BASE L -- <specs>` non-empty, specs = BASE's .agi/config.json land.rules_paths (never TIP's);
# L4 the cell absent, unparsable, not a list of strings or EMPTY = RULES (`rules_paths unread ...: wrapped`); R1's guard route: BASE's r-land printed a
# `config:` line on the range, or r-land was unread there. R2 `config: lander not provable` HOLDS; R3 a wrap's tree, parent order and two signers HOLD.
rp(){ git cat-file blob $1:.agi/config.json 2>/dev/null|python3 -I -c 'import json,sys
try: v=json.load(sys.stdin)["land"]["rules_paths"]
except Exception: sys.exit(1)
ok=isinstance(v,list) and v and all(isinstance(x,str) and x for x in v)
print("\n".join(v)) if ok else sys.exit(1)';}
# P1 (council 07:01:14Z): every git call that takes the specs runs with the pathspec env CLEARED: an inherited GIT_LITERAL_PATHSPECS=1 makes the :(glob) specs
# match nothing (a .gitattributes-only RULES land would land plain); P2 (07:01:25Z + 07:01:37Z): `rules: N of M specs match nothing at BASE (...)`, a reading
gs(){ env -u GIT_LITERAL_PATHSPECS -u GIT_NOGLOB_PATHSPECS -u GIT_GLOB_PATHSPECS -u GIT_ICASE_PATHSPECS git "$@";}
rnone(){ sp=$(rp $1)||{ echo "rules: specs unread at BASE $(echo $1|cut -c1-10)";return;};e=$(git hash-object -t tree /dev/null)
  printf '%s\n' "$sp"|{ m=0;n=0;z=;while IFS= read -r x;do m=$((m+1));[ -n "$(gs diff --name-only $e $1 -- "$x" 2>/dev/null|head -1)" ]||{ n=$((n+1));z="$z${z:+ }$x";};done
  printf 'rules: %s of %s specs match nothing at BASE (%s)\n' $n $m "$z";};}
rules(){ sp=$(rp $1)||{ echo "rules_paths unread at BASE $(echo $1|cut -c1-10): wrapped";return 0;}   # rc 0 = RULES (prints why), rc 1 = not by the list
  f=$(printf '%s\n' "$sp"|tr '\n' '\0'|xargs -0 env -u GIT_LITERAL_PATHSPECS -u GIT_NOGLOB_PATHSPECS -u GIT_GLOB_PATHSPECS -u GIT_ICASE_PATHSPECS git diff --name-only $1 $2 -- 2>/dev/null)||{ echo "rules: diff unread: wrapped";return 0;}
  [ -n "$f" ]&&{ echo "rules: $(echo $f|cut -c1-160)";return 0;};return 1;}
# r-land (council 3/3, alive 02:11:54Z 10-26, R4 site 2): the SAME call as SM's gate and the reference-transaction piece: BASE's guard/r-land blob on
# BASE..LAND (a range never brings its own judge), ring from VL_RING. Its lines print as they are (report mode: `would refuse` lines at rc 0 are readings
# for the [landed]); rc != 0 (an enforce refusal or unread, a BASE/TIP that does not rev-parse) HOLDS. GATE272 (council 03:49-03:5xZ 10-26): V1 no tmpfile
# HOLDS; V3 an ancestry read that errors (an unresolvable BASE) HOLDS; fail open (the hook's reading) ONLY for a BASE that does not descend L140
# (VL_RLAND_SINCE); V2' at a post-L140 BASE an ABSENT or EMPTY judge is replaced by the LAST non-empty r-land blob in BASE's history (never none, never the
# range's own: a HOLD there would lock out the restoring land, the GATE264 shape; the walk is --first-parent, or a land merge that deletes r-land,
# TREESAME to its 2nd parent, leads the walk off the trunk into the range's own history); HOLD only for what a retry clears: a read error on a present blob, a
# failed history search, no prior judge. NAMED LIMIT: a land that makes r-land a BROKEN script locks out its own repair (BASE's judge runs); the repair path
# is the stated override: the hook's hooksPath bypass (R5), and belam lifting this HOLD with the reason in the [landed].
rjudge(){ B=$1;RX=$2;RP=extensions/agi/guard/r-land;RS=${VL_RLAND_SINCE:-20e4947d3a0dc641340df3d07449bed0ab205325};b=$(echo $B|cut -c1-10);j=;ra=9;rr=;s=$(mktemp 2>/dev/null)||s=
if [ -z "$s" ];then echo "r-land: unread (tmpfile)";ra=9
else git merge-base --is-ancestor $RS $B 2>/dev/null;d=$?
  if [ $d != 0 ]&&[ $d != 1 ];then echo "r-land: unread (BASE $b)";ra=9
  elif git cat-file -e $B:$RP 2>/dev/null&&! git cat-file blob $B:$RP >$s 2>/dev/null;then echo "r-land: unread (unreadable at BASE $b)";ra=9
  elif [ -s $s ];then j=$B
  elif [ $d = 1 ];then echo "r-land: none at BASE $b (a pre-L140 BASE: fail open, as the hook)";ra=0
  elif ! hs=$(git log --first-parent --format=%H $B -- $RP 2>/dev/null);then echo "r-land: unread (history search at BASE $b)";ra=9
  else w=$(echo "$hs"|head -1);git cat-file -e $w:$RP 2>/dev/null&&k=emptied||k=deleted
    for c in $hs;do git cat-file -e $c:$RP 2>/dev/null||continue;git cat-file blob $c:$RP >$s 2>/dev/null||{ j=x;break;};[ -s $s ]&&{ j=$c;break;};done
    [ -n "$w" ]||k=absent;case $j in x)j=;echo "r-land: unread (unreadable prior judge at $(echo $c|cut -c1-10))";ra=9;;
      "")echo "r-land: unread (no prior judge at BASE $b)";ra=9;;
      *)echo "r-land: judge from $(echo $j|cut -c1-10) ($k at $(echo $w|cut -c1-10))";;esac;fi
  [ -z "$j" ]||{ rr=$(AGI_RING=${VL_RING:-/var/lib/agi/allowed_signers} sh $s $B $RX 2>&1);ra=$?;printf '%s\n' "$rr";echo "r-land=$ra";};rm -f $s;fi;}
if [ "${1:-}" = wrap ];then N=$2 L=$3 B=$4 G=$5;T=${VL_T:-$HOME/t};MAIN=${VL_MAIN:-/data/work/agi};cd "$T"||exit 2
  H=$(git -C "$MAIN" rev-parse -q --verify refs/held/sanctuary-master/$N 2>/dev/null || git rev-parse -q --verify refs/held/sanctuary-master/$N)
  L=$(git rev-parse -q --verify "$L^{commit}")&&[ "$L" = "$H" ]||{ echo "wrap: refused ($N: the land is not the held refs/held/sanctuary-master/$N)";exit 1;}
  B=$(git rev-parse -q --verify "$B^{commit}")||{ echo "wrap: refused (BASE unread)";exit 1;};rnone $B
  y=$(rules $B $L)||{ rjudge $B $L >/dev/null;case $rr in *"
config: "*|"config: "*)y="r-land judged a config change";;esac;[ $ra = 9 ]&&y="r-land unread on the route question";}
  [ -n "$y" ]||{ echo "land: plain $L";exit 0;}
  W=$(git commit-tree "$L^{tree}" -p $B -p $L -S -m "belam: wrap of $N (gate $L)")||{ echo "wrap: refused (commit-tree -S failed)";exit 1;}
  echo "land: wrap $W over $L ($y)";exit 0;fi
git fetch -q origin 2>/dev/null
H=$(git -C "$MAIN" rev-parse -q --verify refs/held/sanctuary-master/$N 2>/dev/null || git rev-parse -q --verify refs/held/sanctuary-master/$N)
L=$(git rev-parse -q --verify "$L^{commit}")||{ echo "verify-land: HOLD (land unread)";exit 1;}
X=;[ -n "$H" ]&&[ "$L" != "$H" ]&&[ "$(git rev-parse -q --verify $L^2 2>/dev/null)" = "$H" ]&&X=1   # LAND = a WRAP W whose 2nd parent is the held L
echo "held=$(echo $H|cut -c1-10) land=$(echo $L|cut -c1-10) $( [ "$H" = "$L" ] && echo OK || { [ -n "$X" ] && echo "WRAP over held" || echo MISMATCH; })";[ "$H" = "$L" ]||[ -n "$X" ]||hold held
K=$L;[ -z "$X" ]||K=$H   # the land SM gated: its parents are [BASE, GATETIP]
P=$(git log -1 --format=%P $K);W="$(git rev-parse -q --verify "$B^{commit}") $(git rev-parse -q --verify "$G^{commit}")"
echo "parents: $(echo $P | awk '{print substr($1,1,10), substr($2,1,10)}') want $(echo $W | awk '{print substr($1,1,10), substr($2,1,10)}')";[ "$P" = "$W" ]||hold parents
if [ -n "$X" ];then P2=$(git log -1 --format=%P $L);echo "R3 wrap parents: $(echo $P2 | awk '{print substr($1,1,10), substr($2,1,10)}') want $(echo $B|cut -c1-10) $(echo $H|cut -c1-10)"
  [ "$P2" = "$(git rev-parse -q --verify "$B^{commit}") $H" ]||hold r3-parents
  [ "$(git rev-parse $L^{tree})" = "$(git rev-parse $H^{tree})" ]&&echo "R3 wrap tree = land tree"||{ echo "R3 wrap tree != land tree";hold r3-tree;}
  ws=$(git log -1 --format='%G? %GS' $L);ls=$(git log -1 --format='%G? %GS' $H);echo "R3 signers: wrap [$ws] land [$ls]"
  [ "$ws" = "G ${VL_WRAP_SIGNER:-belam@agi}" ]&&[ "$ls" = "G ${VL_LAND_SIGNER:-sanctuary-master@agi}" ]||hold r3-signer;fi
t1=$(git rev-parse $L^{tree});t2=$(git merge-tree --write-tree $B $G 2>/dev/null | head -1)
echo "tree $(echo $t1|cut -c1-10) merge-tree $(echo $t2|cut -c1-10)";[ -n "$t2" ]&&[ "$t1" = "$t2" ]||hold tree
echo "sigs: $(git log --format=%G? $B..$L | sort | uniq -c | tr '\n' ' ')";[ -z "$(git log --format=%G? $B..$L | grep -vx G)" ]||hold sigs
# D (goal:g7.16.1.11.46.23.1, council 3/3 alive 09:55:09Z 10-26 (c)): renames PINNED (`-M`: the D set never depends on diff.renames, L154 read D 1 by default and
# D 4 with diff.renames=false); a D is admitted ONLY by its exact path from BASE's .agi/config.json land.deletes_admitted [{path, ruling}] (never TIP's: a range
# cannot admit its own delete), sets not counts (a listed dir/ covers nothing below it), a D under .agi/nodes/ never (a retire is an R into deprecated/).
# The cell absent = [] (nothing admitted); unreadable or malformed = `deletes_admitted unread ...` and nothing admitted. Each entry is removed after its land.
da(){ git cat-file blob $1:.agi/config.json 2>/dev/null|python3 -I -c 'import json,sys
try: v=json.load(sys.stdin).get("land",{}).get("deletes_admitted",[])
except Exception: sys.exit(1)
ok=isinstance(v,list) and all(isinstance(e,dict) and isinstance(e.get(k),str) and e[k] and "\t" not in e[k] and "\n" not in e[k] for e in v for k in ("path","ruling"))
print("".join(e["path"]+"\t"+e["ruling"]+"\n" for e in v),end="") if ok else sys.exit(1)';}
ns=$(git diff -M --name-status $B $L);nd=$(printf '%s\n' "$ns"|grep -c '^D');echo "D: $nd  files: $(printf '%s\n' "$ns"|tr '\t\n' ' ')"
ad=$(da $B)||{ echo "deletes_admitted unread at BASE $(echo $B|cut -c1-10): nothing admitted";ad=;}
dl=$(printf '%s\n' "$ns"|sed -n 's/^D\t//p');du=0
while IFS= read -r p;do [ -n "$p" ]||continue;r=$(printf '%s\n' "$ad"|awk -F'\t' -v p="$p" '$1==p{print $2;exit}')
  case $p in .agi/nodes/*) echo "D not admitted: $p (a node: retire, never delete)";du=1;continue;;esac
  [ -n "$r" ]&&echo "D admitted: $p ($r)"||{ echo "D not admitted: $p";du=1;};done <<EOD
$dl
EOD
printf '%s\n' "$ad"|cut -f1|while IFS= read -r p;do [ -z "$p" ]||printf '%s\n' "$dl"|grep -qxF -- "$p"||echo "admitted but not deleted: $p";done
[ "$du" = 0 ]||hold D
git diff $B $L > "$S/$N.diff"; git log --format=%B $B..$L > "$S/$N.msg"
# FIXTURE CLASS (c) (council 3/3 alive 18:25:50Z 10-26; belam's [hold] 18:15Z on L177+L178): a PINNED fixture user's `/home/<name>` in an ADDED line of a file under
# extensions/agi/tests/ is ONE named WARN, not a HOLD. The class is decided by the diff's `+++ b/` PATH, never by the line's content; the allowlist is BASE's
# `.agi/config.json` anonymize.fixture_homes (a RULES path; never TIP's, so a land cannot add its own name); every other hit -- an unpinned /home/<x>, passwd or not,
# a real passwd home, anything outside tests/ -- stays for `anonymize.py check` and HOLDs. FAIL CLOSED: an unreadable / empty / malformed cell, or a passwd read that
# errors or is empty, pins NOTHING (every hit HOLDs); a pinned name that is ALSO a passwd home of this box is dropped (HOLD). The substitution runs on a COPY of the diff.
# The tokens are paths.py's HOME_RE, the ONE home-path regex literal (config:census home-path-code-literal-regex; never a second one, split or not): ONLY a token
# `/home/<pinned>` with no word character after it becomes the placeholder (the count is of substitutions, never of tokens); every other token stays.
# The step failing (paths unimportable, any crash) = the unfiltered diff + ONE named `unread` line: nothing is pinned, every hit HOLDs.
git show "$B:.agi/config.json" > "$S/$N.cfg" 2>/dev/null
python3 -I - "$S/$N.diff" "$S/$N.cfg" "$S/$N.anon.diff" "$A" <<'P' || { echo "anon-diff fixture class: unread (the step failed): nothing pinned, every hit HOLDs";cp "$S/$N.diff" "$S/$N.anon.diff";}
import json,os,pwd,re,sys
diff,cfg,out,anon=sys.argv[1:5]
sys.path.insert(0,os.path.dirname(os.path.abspath(anon)))    # paths.py sits beside the anonymize.py that judges this diff
import paths
def pinned():
    try:
        names=json.load(open(cfg)).get('anonymize',{}).get('fixture_homes')
        names=[n for n in names if isinstance(n,str) and re.fullmatch(r'[A-Za-z0-9_-]+',n)] if isinstance(names,list) else []
        if os.environ.get('VL_PASSWD'):    # the lane's seam: a passwd-format file standing in for this box's
            dirs={l.split(':')[5] for l in open(os.environ['VL_PASSWD']) if l.count(':')>=5}
        else:
            dirs={p.pw_dir for p in pwd.getpwall()}
        if not names or not dirs: return []
        return [n for n in names if '/home/'+n not in dirs]
    except Exception: return []
names=pinned()
text=open(diff,errors='replace').read().split('\n')
cur,hits,res=None,{},[]
def fixture(m):     # one paths.HOME_RE token (also ~/, $HOME, expanduser: those stay)
    t=m.group(0)
    if t[:6]!='/home/' or t[6:] not in names or re.match(r'\w',m.string[m.end():]): return t
    hits[cur]=hits.get(cur,0)+1;return '<fixture-home>'
for l in text:
    if l.startswith('diff --git '): cur=None
    elif l.startswith('+++ '): cur=l[6:] if l.startswith('+++ b/') else None
    elif names and cur and cur.startswith('extensions/agi/tests/') and l.startswith('+') and not l.startswith('+++'):
        l=paths.HOME_RE.sub(fixture,l)
    res.append(l)
open(out,'w').write('\n'.join(res))
for f,k in sorted(hits.items()): print('anon-diff WARN (fixture class): pinned /home/<'+'|'.join(names)+'> x%d in %s'%(k,f))
P
python3 "$A" check --diff-file "$S/$N.anon.diff"; a=$?;echo "anon-diff=$a";[ $a = 0 ]||hold anon-diff
python3 "$A" check --text "$(grep -v -x -E 'Co-Authored-By: Claude (Opus|Sonnet|Haiku|Fable) [0-9]+\.[0-9]+ <noreply@anthropic\.com>' "$S/$N.msg")" >/dev/null; a=$?;em=$(grep -o -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$S/$N.msg" | sort -u | tr '\n' ' ')
echo "anon-msg=$a emails: $em";[ $a = 0 ]||hold anon-msg   # C4 (council 22:05:25Z) + C5 (22:16:14Z): the message minus EXACTLY the co-author trailer (model family + N.N only, so no ip hides in it) must anonymize clean
[ -z "$(printf '%s\n' $em | grep -vx 'noreply@''anthropic.com')" ]||hold msg-email   # the co-author line is the one address a land message carries
python3 -I - "$S/$N.diff" "$S/$N.msg" <<'P' || hold home
import pwd,sys
homes={p.pw_dir for p in pwd.getpwall() if len(p.pw_dir)>5 and p.pw_dir not in ('/nonexistent','/var/empty','/usr/sbin')}
hits=[h for f in sys.argv[1:] for h in homes if h+'/' in open(f,errors='replace').read()]
print('home hits', hits);sys.exit(1 if hits else 0)
P
gp=$(python3 -I - "$A" "$S/$N.diff" "$T" <<'P'
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(sys.argv[1])))
try:
    import anonymize as a
    fr=[v for c,v in a.box_tokens(sys.argv[3],secrets=False) if c=="hardware" and len(v)>=a.MIN_TOKEN]
    print(0 if not fr else sum(1 for l in open(sys.argv[2],errors="replace") if a._hw_frag_re(fr).search(l)))
except Exception: print("unread")
P
);echo "gpu: $gp (lines naming a box device, anonymize's hardware list; never the bare word)"   # a reading, not a hold (council 06:06:56Z: device names, its own file not excluded)
# cite (council 3/3, alive 21:31:33Z 10-25, M10 row b): a land that changes a node file holding a `## OWNER` block (at BASE or LAND; broader than a changed
# heading, so a body edit that drops a cited chunk id is caught) runs agi-mem cite on the LAND tree; rc != 0 (a violation or unread) holds the land
o=$(for x in $(git diff --name-only $B $L -- .agi/nodes);do { git show $L:$x 2>/dev/null;git show $B:$x 2>/dev/null;}|grep -q '^## OWNER'&&echo $x;done)
if [ -n "$o" ];then w=$(mktemp -d)/land;if git worktree add -q --detach $w $L 2>/dev/null;then r=$(AGI_ENGINE=$w AGI_POST=belam agi-mem cite 2>&1);a=$?;git worktree remove --force $w
  printf '%s\n' "$r";echo "cite=$a ($(echo $o|wc -w) OWNER file(s))";[ $a = 0 ]||hold cite;else echo "cite: unread (no land worktree)";hold cite;fi
else echo "cite: n/a (no OWNER file changed)";fi
rjudge $B $L;[ $ra = 0 ]||hold r-land   # the r-land block (council 02:11:54Z R4 site 2 + GATE272), as the function above
case $rr in *"config: lander not provable"*)echo "R2: config lander not provable on this land";hold lander-unprovable;;esac
rnone $B
if [ -n "$X" ];then echo "wrap: $(echo $L|cut -c1-10) over $(echo $H|cut -c1-10) ($(rules $B $H||echo needless: the range is not RULES))"
else y=$(rules $B $H)||{ case $rr in *"
config: "*|"config: "*)y="r-land judged a config change";;esac;};[ -z "$y" ]||{ echo "wrap: MISSING, landed plain ($y)";hold wrap-missing;};fi
echo "ran as: $(id -un 2>/dev/null||echo unread) uid $(id -u)"   # M2 (council 3/3, alive 02:53:20Z 10-26): a reading, never a verdict input
# self (council VL): this copy must be the pin's repo blob, and the one on PATH; the ~/tools copy is retired
pin=$(sed -n 's/^AGI_TRUNK=//p' "${VL_CARRY:-/etc/agi/carry.env}" 2>/dev/null|tail -1);rb=$(git -C "$MAIN" show "$pin:extensions/agi/guard/verify-land.sh" 2>/dev/null|sha256sum|cut -c1-64);me=$(sha256sum <"$0"|cut -c1-64)
if [ -n "$pin" ]&&[ "$rb" = "$me" ];then echo "self: = the pin's blob ($(echo $me|cut -c1-12))";else echo "verify-land: unread (installed != repo at pin ${pin:-<none>})";hold self;fi
I=${VL_INSTALLED:-/opt/agi/bin/verify-land};c=$(command -v verify-land 2>/dev/null)
[ "$c" = "$I" ]||{ echo "verify-land: RED PATH resolves verify-land to '${c:-nothing}', not $I";hold path;}
[ ! -e "${VL_TOOLS:-$HOME/tools/verify-land.sh}" ]||{ echo "verify-land: RED the box-local copy ${VL_TOOLS:-~/tools/verify-land.sh} still exists (retire it)";hold tools-copy;}
[ -z "$h" ]&&{ echo "verify-land: OK";exit 0;};echo "verify-land: HOLD ($(echo $h))";exit 1
