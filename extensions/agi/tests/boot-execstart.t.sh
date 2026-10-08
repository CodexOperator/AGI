#!/bin/sh
# boot-execstart.t.sh: goal:g1.41 A1 return RA1-RA4 (DG1 22:35Z; SM mur on 3209c6a32e accept_with_residue, upheld 4): the agi-boot.service ExecStart line and the baked agi-project.service ExecStart line, run for real under sh in a SCRATCH repo, fail closed. RA1 the 40-hex gate sits inside the fetched blob, so it cannot guard its own fetch: an absent or empty AGI_TRUNK makes `echo :path|git cat-file --batch` read the INDEX, `HEAD:` or a branch name reads an agi-writable ref, and root runs it ungated. RA2 refs/replace redirects a pinned sha read (GIT_NO_REPLACE_OBJECTS=1 must be in the unit Environment= and in the baked unit). RA3 a pin that fetches no script exits 0 silently. RA4 no lane drove the ExecStart itself.
# sh + git + jq on a SCRATCH repo, no systemd, no root, no /etc, no network, 0 USD. The ExecStart text and the Environment= words come from `sect agi-boot.service` of the .geometry/engine*.md of ROOT (default the working tree); the baked unit is produced by one real pinned boot and read back from its AGI_BOOT_OUT. Each line runs under env -i with ONLY what its unit supplies: the unit's Environment= words, AGI_TRUNK as /etc/agi/carry.env would set it (absent, empty or a value; agi-boot.service only), PATH to the fakes (setfacl, systemctl, systemd-sysusers log), an empty HOME, no global or system gitconfig, plus the path knobs AGI_RAM / AGI_BOOT_OUT / AGI_LOADAVG / AGI_PSI_IO the script already reads. The repo carries a HOSTILE commit: its engine-root.md `### agi-boot` and its engine.md `### agi-project` (as its first command) append a line to MARK, HEAD and the index are that commit, a branch `evil` and a 40-char non-hex branch name point at it.
# Lanes: k controls (a good 40-hex pin boots both posts; the baked line replays and regrows the units) · a-* nine bad pins (absent, empty, HEAD, a branch name, the hostile sha cut to 39 hex, 41 hex, uppercase hex, `a b`, a 40-char non-hex branch name): rc != 0, MARK absent, 0 setfacl, 0 start, 0 unit files · c-* a well-formed pin naming no commit / 40 zeros / a commit with no `### agi-boot` / a commit with no engine-root.md: rc != 0 AND a message on stderr, MARK absent, 0 start · b-* `git replace GOOD HOSTILE`: the pinned boot line runs the clean script (rc 0, both posts started, MARK absent) and the baked agi-project line regrows the clean units (MARK absent, units written, sysusers called).
# RA5 + RA6 + RA7 (DG1 23:32Z, SM demoted c34db81a66): ra5-* every `sh` in the new rows is a wrapper that execs the real dash and keeps a copy of what `sh -s` is handed: the PSI file ABOVE the cell and the load ABOVE the cell close the gate (rc != 0, 0 starts), the open side still boots, the first script handed to sh -s equals the pinned agi-boot byte for byte (cmp) and so does the one agi-boot hands on, a pinned script holding the literal a\1b\nc\\d runs as written, and so does the baked line's fetched agi-project; ra6-* a scratch repo with a promisor remote and a core.sshCommand that touches a marker, the pin names a commit whose blob is MISSING: the boot ExecStart (unit Environment= words), the agi-boot script's own export and the baked unit's Environment= must each keep the marker absent; ra6-k proves the trap is live (a plain read runs the sshCommand, GIT_NO_LAZY_FETCH=1 does not). `printf '%s' "$s"` (no trailing newline) fails the byte compare although the script behaves the same: the compare is the stricter reading DG1 asked for.
# Honest limits: the text and env of the units, not systemd (EnvironmentFile loading is modelled as AGI_TRUNK set or not; Environment= is read as space-separated KEY=VAL words, no quoting; systemd's own $VAR substitution is not modelled, sh expands it); the repo is owned by the running user, so the ownership refusal on a root unit over an agi-owned repo is modelled with git's GIT_TEST_ASSUME_DIFFERENT_OWNER=1 seam, and each run is granted only what its unit grants (the Environment= GIT_CONFIG_COUNT/KEY_0/VALUE_0 words; the ra6 agi-boot-export row hardcodes those three words from engine-root.md, carry.env is not read); the baked-unit run (brun) is NOT under the seam, so its rows do not see the refusal (see the comment at brun); a pin that is a real 40-hex commit of the attacker's choosing is out of scope (root trusts its own carry.env); the exit code of a refusal is only asserted != 0 (the unset code is 2, not 1). RA8 + RA9 (DG1 00:33Z, comment only, no row changed): (1) WRITABLE OBJECTS: the lane never forges an object under its own sha path, and none of its rows could fail on one. git does not re-hash an object on read: SM's verifier forged one and `cat-file --batch` and `git show` both served it, only `fsck` noticed. So a writer of the repo's objects directory can forge the script root runs; the pin roots the REF, not the BYTES; the closure is banked in the node, not pinned here. (2) THE f-TWICE CONSEQUENCE: the line reads the script twice, `[ -n "$(f)" ]` and then `f|sh -s`; a racing store writer can empty the second read and the unit exits 0 silently (RA3's silent-success shape, but through a race). No row pins it, and it needs the same privilege as forging an object.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};MARK=$T/marker
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST AGI_RAM AGI_BOOT_OUT GIT_NO_REPLACE_OBJECTS
sect agi-boot.service >$T/unit.txt;UCMD=$(sed -n 's/^ExecStart=//p' $T/unit.txt);UE=$(sed -n 's/^Environment=//p' $T/unit.txt|tr ' ' '\n')
[ -n "$UCMD" ]&&[ -s $R0/.agi/config.json ]||{ echo "FAIL extract: no ExecStart line in agi-boot.service, or no config.json in ROOT";exit 99;}
mkdir -p $T/fk $T/hm
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n' >$T/gitconfig
printf '#!/bin/sh\necho "setfacl $*">>%s/log\n' $T >$T/fk/setfacl
printf '#!/bin/sh\necho "systemctl $*">>%s/log\n[ "$1" = start ]&&echo "b $2">>%s/log\nexit 0\n' $T $T >$T/fk/systemctl
printf '#!/bin/sh\necho "sysusers $*">>%s/log\nexit 0\n' $T >$T/fk/systemd-sysusers
chmod +x $T/fk/*
echo "0.50 0.5 0.5 1/1 1" >$T/la;printf 'some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/io
row(){ printf '  - {"name": "%s", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' $1;}
# the scratch repo: GOOD (the real engine*.md of ROOT, boot rows a b); evil = HOSTILE (engine-root.md and the agi-project piece append to MARK); nb = no `### agi-boot`; nf = no engine-root.md
rm -rf $T/r;mkdir -p $T/r/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine*.md $T/r/.agi/nodes/.geometry/
{ printf -- '---\nposts:\n';row a;row b;} >$T/r/.agi/nodes/.geometry/posts.md
jq '.values.local_maxxing.agi_boot={"poll_s":0.1,"wait_max_s":1,"space_s":0.2}' $R0/.agi/config.json >$T/r/.agi/config.json
export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
GD=$T/r/.agi/nodes/.geometry;$G init -q $T/r;$G -C $T/r add -A;$G -C $T/r commit -qm good;GOOD=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -b evil;cp $GD/engine.md $T/engine.good
awk -v m="echo project >>$MARK" '/^### agi-project /{h=1} {print} h&&!d&&/^#!\/bin\/sh/{print m;d=1}' $T/engine.good >$GD/engine.md
printf '### agi-boot (1 B)\n~~~sh\n#!/bin/sh\necho boot >>%s\n~~~\n' $MARK >$GD/engine-root.md
$G -C $T/r add -A;$G -C $T/r commit -qm hostile;EVIL=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -b nb $GOOD;printf '### other (1 B)\n~~~sh\n:\n~~~\n' >$GD/engine-root.md;$G -C $T/r commit -qam noboot;NB=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -b nf $GOOD;$G -C $T/r rm -q $GD/engine-root.md;$G -C $T/r commit -qm nofile;NF=$($G -C $T/r rev-parse HEAD)
G40=gggggggggggggggggggggggggggggggggggggggg;$G -C $T/r branch $G40 $EVIL;$G -C $T/r checkout -q -B main $EVIL
[ "$GOOD" != "$EVIL" ]&&[ "$GOOD" != "$NB" ]&&[ "$GOOD" != "$NF" ]&&[ ${#G40} = 40 ]||echo "FAIL fixture: the commits are not distinct"
# xrun PIN|-: the agi-boot.service ExecStart under env -i with the unit's Environment= words; - = AGI_TRUNK absent. rc in $brc, MARK in $mk, counts in $sf $st $uf, stderr in $T/err
xrun(){ rm -rf $T/out $T/ram $MARK;: >$T/log;pin=;[ "$1" = - ]||pin="AGI_TRUNK=$1"
 (set -f;cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out AGI_LOADAVG=${LAF:-$T/la} AGI_PSI_IO=${IOF:-$T/io} $UE ${pin:+"$pin"} timeout 60 sh -c "$UCMD" >$T/x.out 2>$T/err);brc=$?;counts;}
counts(){ sf=$(grep -c '^setfacl' $T/log||true);st=$(grep -c '^b ' $T/log||true);uf=$(ls $T/out 2>/dev/null|wc -l|tr -d ' ');mk=untouched;[ -e $MARK ]&&mk="TOUCHED($(tr '\n' ' ' <$MARK))";true;}
# brun: the baked agi-project.service ExecStart under env -i with the baked unit's own Environment= words (the output dir is emptied first, so a regrow is visible)
# brun is deliberately NOT under GIT_TEST_ASSUME_DIFFERENT_OWNER=1: the baked unit's GIT_CONFIG_VALUE_0 comes from /etc/agi/carry.env, which this lane does not read, so under the seam its 3 baked rows (k-the-baked-execstart, b-replace-the-baked, ra5-the-baked-line) FAIL on the trunk (measured); the baked rows under the seam arrive with the A1b boot-lane re-cut
brun(){ rm -rf $T/out $MARK;: >$T/log
 (set -f;cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $BE timeout 60 sh -c "$UB" >$T/b.out 2>$T/err);brc=$?;counts;hc=$(ls $T/out/agi-post@*.service.d/h.conf 2>/dev/null|wc -l|tr -d ' ');su=$(grep -c '^sysusers' $T/log||true);}
# k: controls first, so a broken fixture shows before the lanes. HEAD and the index are the hostile commit; the pin is GOOD
xrun $GOOD;ok "k-a-good-pin-boots-both-posts the ExecStart with AGI_TRUNK=<GOOD> while HEAD is the hostile commit: rc $brc (want 0), MARK $mk (want untouched), $st start(s) (want 2), $uf unit file(s) written (want > 0)" '[ $brc = 0 ]&&[ "$mk" = untouched ]&&[ $st = 2 ]&&[ $uf -gt 0 ]'
cp -a $T/out $T/baked;UB=$(sed -n 's/^ExecStart=//p' $T/baked/agi-project.service);BE=$(sed -n 's/^Environment=//p' $T/baked/agi-project.service|tr ' ' '\n')
[ -n "$UB" ]||echo "FAIL extract: no ExecStart line in the baked agi-project.service"
brun;ok "k-the-baked-execstart-regrows-the-units the baked agi-project.service ExecStart, no replace ref: rc $brc (want 0), MARK $mk (want untouched), $hc post unit drop-in(s) regrown (want > 0), sysusers called $su time(s) (want 1)" '[ $brc = 0 ]&&[ "$mk" = untouched ]&&[ $hc -gt 0 ]&&[ $su = 1 ]'
# a (RA1): a bad pin fails before the candidate runs, with a HOSTILE index entry and a HOSTILE HEAD
bad(){ nm=$1;xrun "$2";ok "a-pin-$nm-never-runs-the-candidate AGI_TRUNK $nm: rc $brc (want != 0), MARK $mk (want untouched), $sf setfacl (want 0), $st start (want 0), $uf unit file(s) written (want 0)" '[ $brc != 0 ]&&[ "$mk" = untouched ]&&[ $sf = 0 ]&&[ $st = 0 ]&&[ $uf = 0 ]';}
bad absent -
bad empty ""
bad head HEAD
bad branch-name evil
bad hex39 "$(printf %s $EVIL|cut -c1-39)"
bad hex41 "${EVIL}0"
bad uppercase-hex "$(printf %s $EVIL|tr a-f A-F)"
bad two-words "a b"
bad nonhex-40-chars $G40
# c (RA3): a well-formed pin that fetches no script fails loud
loud(){ nm=$1;xrun "$2";ok "c-pin-$nm-fails-loud a well-formed pin, $nm: rc $brc (want != 0), $(wc -c <$T/err|tr -d ' ') byte(s) on stderr (want > 0), MARK $mk (want untouched), $sf setfacl (want 0), $st start (want 0)" '[ $brc != 0 ]&&[ -s $T/err ]&&[ "$mk" = untouched ]&&[ $sf = 0 ]&&[ $st = 0 ]';}
loud names-no-commit 1234567890abcdef1234567890abcdef12345678
loud forty-zeros 0000000000000000000000000000000000000000
loud commit-with-no-agi-boot-piece $NB
loud commit-with-no-engine-root $NF
# b (RA2): refs/replace redirects GOOD to the hostile commit; both lines must still read GOOD's own bytes
$G -C $T/r replace $GOOD $EVIL;rp=$($G -C $T/r for-each-ref refs/replace|wc -l|tr -d ' ')
xrun $GOOD;ok "b-replace-the-boot-unit-reads-the-pinned-bytes refs/replace redirects the pin GOOD to the hostile commit ($rp replace ref): the agi-boot.service ExecStart: rc $brc (want 0), MARK $mk (want untouched), $st start(s) (want 2: the clean script ran), $uf unit file(s) written (want > 0)" '[ $rp = 1 ]&&[ $brc = 0 ]&&[ "$mk" = untouched ]&&[ $st = 2 ]&&[ $uf -gt 0 ]'
brun;ok "b-replace-the-baked-execstart-reads-the-pinned-bytes the same replace ref: the baked agi-project.service ExecStart: rc $brc (want 0), MARK $mk (want untouched), $hc post unit drop-in(s) regrown (want > 0: the clean genome ran), sysusers called $su time(s) (want 1)" '[ $brc = 0 ]&&[ "$mk" = untouched ]&&[ $hc -gt 0 ]&&[ $su = 1 ]'
# --- RA5 + RA6 + RA7 (DG1 23:32Z; SM mur on c34db81a66 DEMOTE): the bytes the shell receives, the closed side of the gate, and the lazy fetch ---
# RA5: /bin/sh is DASH on the box and the unit's fetched script reached `sh -s` through `echo "$s"`: dash's echo rewrites backslash escapes (the pinned agi-boot's sed \1 became byte 0x01, so the PSI reading was garbage and the IO half of the gate OPENED at any pressure). Every `sh` in these rows is a wrapper that execs the real dash and, for `sh -s`, keeps a copy of the script it was handed. RA7: the rows above pinned PSI at 1.00 and asserted starts and rc only; these close the gate (PSI or load above the cell) and read the closed side.
[ -x /usr/bin/dash ]||{ echo "FAIL needs /usr/bin/dash";exit 99;}
RECV=$T/recv;mkdir -p $RECV
printf '#!/usr/bin/dash\nif [ "$1" = -s ];then n=$(ls %s|wc -l);cat >%s/r$n;exec /usr/bin/dash -s "$@" <%s/r$n;fi\nexec /usr/bin/dash "$@"\n' $RECV $RECV $RECV >$T/fk/sh;chmod +x $T/fk/sh
printf 'some avg10=0.00 avg60=99.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/io99;echo "99.00 0.5 0.5 1/1 1" >$T/la99
CL=$(jq -r '.values.local_maxxing.de_live_parents.ceiling_if.loadavg1_lt' $R0/.agi/config.json);CP=$(jq -r '.values.local_maxxing.de_live_parents.ceiling_if.io_psi_some_avg60_lt' $R0/.agi/config.json)
awk -v l=$CL -v p=$CP 'BEGIN{exit !(l<99&&p<99&&l>0.5&&p>1)}'||echo "FAIL fixture: the live cells ($CL / $CP) are not between the open and the closed readings"
LIT='a\1b\nc\\d'
$G -C $T/r replace -d $GOOD >/dev/null 2>&1   # the b rows left refs/replace GOOD -> HOSTILE in place: every read of GOOD below must be the real one
# probe commits (cut from GOOD): BS = an agi-boot piece that writes LIT to a file; BS2 = an agi-project piece that does it as its first command
$G -C $T/r checkout -q -b bs $GOOD;python3 - $GD $T "$LIT" <<'PY'
import sys,re
g,t,lit=sys.argv[1:4]
s=open(g+'/engine-root.md').read()
n=re.sub(r'(### agi-boot \(\d+ B\)\n~~~sh\n).*?(\n~~~\n)',lambda x:x.group(1)+"#!/bin/sh\nprintf '%s\\n' '"+lit+"' >"+t+"/probe.boot"+x.group(2),s,count=1,flags=re.S)
assert n!=s;open(g+'/engine-root.md','w').write(n)
PY
$G -C $T/r commit -qam probe-boot;BS=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -b bs2 $GOOD;python3 - $GD $T "$LIT" <<'PY'
import sys,re
g,t,lit=sys.argv[1:4]
e=open(g+'/engine.md').read()
n=re.sub(r'(### agi-project \(\d+ B\)\n~~~sh\n#!/bin/sh\n)',lambda x:x.group(1)+"printf '%s\\n' '"+lit+"' >"+t+"/probe.proj\n",e,count=1)
assert n!=e;open(g+'/engine.md','w').write(n)
PY
$G -C $T/r commit -qam probe-proj;BS2=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -B main $EVIL
printf '%s\n' "$LIT" >$T/lit.exp
# ra5-k: the gate's closed side. PSI file above the cell, then load above the cell; the open side (1.00) is the control above
IOF=$T/io99;xrun $GOOD;IOF=
ok "ra5-psi-above-the-cell-closes-the-gate the REAL ExecStart under dash, PSI avg60 99.00 (cell $CP): rc $brc (want != 0: the gate stayed closed), $st start(s) (want 0), MARK $mk (want untouched)" '[ $brc != 0 ]&&[ $st = 0 ]&&[ "$mk" = untouched ]'
LAF=$T/la99;xrun $GOOD;LAF=
ok "ra5-load-above-the-cell-closes-the-gate the same, load 99.00 (cell $CL): rc $brc (want != 0), $st start(s) (want 0), MARK $mk (want untouched)" '[ $brc != 0 ]&&[ $st = 0 ]&&[ "$mk" = untouched ]'
xrun $GOOD;ok "ra5-k-the-open-side-still-boots PSI 1.00 and load 0.50: rc $brc (want 0), $st start(s) (want 2)" '[ $brc = 0 ]&&[ $st = 2 ]'
# ra5: the bytes the shell receives. The first `sh -s` of the boot line is the fetched agi-boot, the second (inside it) the fetched agi-project; compare each with the blob read the plain way
rm -rf $RECV/*;xrun $GOOD
$G -C $T/r show $GOOD:.agi/nodes/.geometry/engine-root.md|sed -n '/^### agi-boot /,/^##/{/^~~~/,/^~~~/{//!p}}' >$T/exp.boot
$G -C $T/r show $GOOD:.agi/nodes/.geometry/engine.md|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}' >$T/exp.proj
cb=1;cmp -s $RECV/r0 $T/exp.boot&&cb=0;cp=1;cmp -s $RECV/r1 $T/exp.proj&&cp=0
ok "ra5-the-shell-receives-the-pinned-agi-boot-byte-for-byte the first script handed to sh -s by the boot ExecStart (backslashes in it: $(grep -c '\\' $T/exp.boot) line(s)) vs the pinned blob: cmp rc $cb (want 0), $(wc -c <$RECV/r0 2>/dev/null) vs $(wc -c <$T/exp.boot) bytes" '[ $cb = 0 ]'
ok "ra5-the-shell-receives-the-pinned-agi-project-byte-for-byte the script agi-boot hands to sh -s: cmp rc $cp (want 0), $(wc -c <$RECV/r1 2>/dev/null) vs $(wc -c <$T/exp.proj) bytes" '[ $cp = 0 ]'
rm -f $T/probe.boot;xrun $BS;pr=1;cmp -s $T/probe.boot $T/lit.exp&&pr=0
ok "ra5-a-script-with-backslash-sequences-runs-as-written the pin names a commit whose agi-boot writes the literal [$LIT] to a file: rc $brc (want 0), the file is that literal, cmp rc $pr (want 0)" '[ $brc = 0 ]&&[ $pr = 0 ]'
# the baked line: bake at BS2, empty the output, replay; the probe in the fetched agi-project must read as written
rm -f $T/probe.proj;xrun $BS2;cp -a $T/out $T/baked2;UB=$(sed -n 's/^ExecStart=//p' $T/baked2/agi-project.service);BE=$(sed -n 's/^Environment=//p' $T/baked2/agi-project.service|tr ' ' '\n')
rm -f $T/probe.proj;brun;pj=1;cmp -s $T/probe.proj $T/lit.exp&&pj=0
ok "ra5-the-baked-line-runs-the-fetched-agi-project-as-written the baked agi-project.service ExecStart (bake at a commit whose agi-project writes [$LIT]): rc $brc (want 0), the file is that literal, cmp rc $pj (want 0)" '[ $brc = 0 ]&&[ $pj = 0 ]'
# RA6: a lazy fetch of a missing pinned object runs the repo's core.sshCommand (agi-writable .git/config). Three carriers must stop it: the unit Environment= words, the agi-boot export, the baked unit's Environment=
LZ=$T/lazy;printf '#!/bin/sh\ntouch %s\nexit 1\n' $LZ >$T/fakessh;chmod +x $T/fakessh
# MB: engine-root.md blob unique and then DELETED; PC: config.json blob unique and deleted; PD: engine.md blob unique, baked first, then deleted
$G -C $T/r checkout -q -b mb $GOOD;printf '### zzz-mb (1 B)\n~~~sh\n:\n~~~\n' >>$GD/engine-root.md;$G -C $T/r commit -qam mb;MB=$($G -C $T/r rev-parse HEAD);MBB=$($G -C $T/r rev-parse $MB:.agi/nodes/.geometry/engine-root.md)
$G -C $T/r checkout -q -b pc $GOOD;jq '.zz_pc=1' $T/r/.agi/config.json >$T/c.json;cp $T/c.json $T/r/.agi/config.json;$G -C $T/r commit -qam pc;PC=$($G -C $T/r rev-parse HEAD);PCB=$($G -C $T/r rev-parse $PC:.agi/config.json)
$G -C $T/r checkout -q -b pd $GOOD;printf '\nprose line pd\n' >>$GD/engine.md;$G -C $T/r commit -qam pd;PD=$($G -C $T/r rev-parse HEAD);PDB=$($G -C $T/r rev-parse $PD:.agi/nodes/.geometry/engine.md)
$G -C $T/r checkout -q -B main $EVIL
xrun $PD;cp -a $T/out $T/bakedpd;UB=$(sed -n 's/^ExecStart=//p' $T/bakedpd/agi-project.service);BE=$(sed -n 's/^Environment=//p' $T/bakedpd/agi-project.service|tr ' ' '\n')
$G -C $T/r config core.repositoryformatversion 1;$G -C $T/r config extensions.partialClone origin;$G -C $T/r config remote.origin.url ssh://nowhere.invalid/p;$G -C $T/r config remote.origin.promisor true;$G -C $T/r config core.sshCommand $T/fakessh
for b in $MBB $PCB $PDB;do rm -f $T/r/.git/objects/${b%${b#??}}/${b#??};done
# the trap is live: a plain git read of a missing blob runs the sshCommand; with GIT_NO_LAZY_FETCH=1 it does not
rm -f $LZ;(cd $T/r&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null git cat-file -p $MBB >/dev/null 2>&1);t1=0;[ -e $LZ ]&&t1=1
rm -f $LZ;(cd $T/r&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_NO_LAZY_FETCH=1 git cat-file -p $MBB >/dev/null 2>&1);t2=0;[ -e $LZ ]&&t2=1
ok "ra6-k-the-trap-is-live a plain git read of a missing blob in a promisor repo runs core.sshCommand: marker $t1 (want 1); with GIT_NO_LAZY_FETCH=1: marker $t2 (want 0)" '[ $t1 = 1 ]&&[ $t2 = 0 ]'
rm -f $LZ;xrun $MB;l1=0;[ -e $LZ ]&&l1=1
ok "ra6-the-unit-environment-stops-the-lazy-fetch the boot ExecStart, the pin names a commit whose engine-root.md blob is missing: rc $brc (want != 0: loud), the sshCommand ran: $l1 (want 0), $st start(s) (want 0)" '[ $brc != 0 ]&&[ $l1 = 0 ]&&[ $st = 0 ]'
sect agi-boot >$T/agiboot.sh;rm -f $LZ
(cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out2 AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io AGI_TRUNK=$PC timeout 60 sh -s <$T/agiboot.sh >$T/s.out 2>$T/s.err);l2=0;[ -e $LZ ]&&l2=1
ok "ra6-the-agi-boot-export-stops-the-lazy-fetch the agi-boot script run WITHOUT the unit's environment (the export is its own), the pin names a commit whose config.json blob is missing: the sshCommand ran: $l2 (want 0)" '[ $l2 = 0 ]'
rm -f $LZ;brun;l3=0;[ -e $LZ ]&&l3=1
ok "ra6-the-baked-environment-stops-the-lazy-fetch the baked agi-project ExecStart, its engine.md blob missing: rc $brc (want != 0), the sshCommand ran: $l3 (want 0)" '[ $brc != 0 ]&&[ $l3 = 0 ]'
echo "boot-execstart: $f FAIL"
exit $f
