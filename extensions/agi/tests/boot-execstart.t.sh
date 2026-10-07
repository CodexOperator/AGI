#!/bin/sh
# boot-execstart.t.sh: goal:g1.41 A1 return RA1-RA4 (DG1 22:35Z; SM mur on 3209c6a32e accept_with_residue, upheld 4): the agi-boot.service ExecStart line and the baked agi-project.service ExecStart line, run for real under sh in a SCRATCH repo, fail closed. RA1 the 40-hex gate sits inside the fetched blob, so it cannot guard its own fetch: an absent or empty AGI_TRUNK makes `echo :path|git cat-file --batch` read the INDEX, `HEAD:` or a branch name reads an agi-writable ref, and root runs it ungated. RA2 refs/replace redirects a pinned sha read (GIT_NO_REPLACE_OBJECTS=1 must be in the unit Environment= and in the baked unit). RA3 a pin that fetches no script exits 0 silently. RA4 no lane drove the ExecStart itself.
# sh + git + jq on a SCRATCH repo, no systemd, no root, no /etc, no network, 0 USD. The ExecStart text and the Environment= words come from `sect agi-boot.service` of the .geometry/engine*.md of ROOT (default the working tree); the baked unit is produced by one real pinned boot and read back from its AGI_BOOT_OUT. Each line runs under env -i with ONLY what its unit supplies: the unit's Environment= words, AGI_TRUNK as /etc/agi/carry.env would set it (absent, empty or a value; agi-boot.service only), PATH to the fakes (setfacl, systemctl, systemd-sysusers log), an empty HOME, no global or system gitconfig, plus the path knobs AGI_RAM / AGI_BOOT_OUT / AGI_LOADAVG / AGI_PSI_IO the script already reads. The repo carries a HOSTILE commit: its engine-root.md `### agi-boot` and its engine.md `### agi-project` (as its first command) append a line to MARK, HEAD and the index are that commit, a branch `evil` and a 40-char non-hex branch name point at it.
# Lanes: k controls (a good 40-hex pin boots both posts; the baked line replays and regrows the units) · a-* nine bad pins (absent, empty, HEAD, a branch name, the hostile sha cut to 39 hex, 41 hex, uppercase hex, `a b`, a 40-char non-hex branch name): rc != 0, MARK absent, 0 setfacl, 0 start, 0 unit files · c-* a well-formed pin naming no commit / 40 zeros / a commit with no `### agi-boot` / a commit with no engine-root.md: rc != 0 AND a message on stderr, MARK absent, 0 start · b-* `git replace GOOD HOSTILE`: the pinned boot line runs the clean script (rc 0, both posts started, MARK absent) and the baked agi-project line regrows the clean units (MARK absent, units written, sysusers called).
# Honest limits: the text and env of the units, not systemd (EnvironmentFile loading is modelled as AGI_TRUNK set or not; Environment= is read as space-separated KEY=VAL words, no quoting; systemd's own $VAR substitution is not modelled, sh expands it); the repo is owned by the running user, so the ownership refusal on a root unit over an agi-owned repo is not modelled (the unit's own safe.directory word is applied but nothing needs it); a pin that is a real 40-hex commit of the attacker's choosing is out of scope (root trusts its own carry.env); the exit code of a refusal is only asserted != 0 (the unset code is 2, not 1).
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
 (set -f;cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io $UE ${pin:+"$pin"} timeout 60 sh -c "$UCMD" >$T/x.out 2>$T/err);brc=$?;counts;}
counts(){ sf=$(grep -c '^setfacl' $T/log||true);st=$(grep -c '^b ' $T/log||true);uf=$(ls $T/out 2>/dev/null|wc -l|tr -d ' ');mk=untouched;[ -e $MARK ]&&mk="TOUCHED($(tr '\n' ' ' <$MARK))";true;}
# brun: the baked agi-project.service ExecStart under env -i with the baked unit's own Environment= words (the output dir is emptied first, so a regrow is visible)
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
echo "boot-execstart: $f FAIL"
exit $f
