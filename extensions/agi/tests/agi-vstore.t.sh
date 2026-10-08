#!/bin/sh
# agi-vstore.t.sh [ROOT]: goal:g1.41 A1b (DG1 03:53Z; hypothesis:g141-a1b-root-reads-the-pinned-trunk-only-through-a-store-it-verified-...; belam [rule] 03:44Z: alive's agi-vstore, NOT the digest): root reads the pinned trunk ONLY through a store it verified. The piece `### agi-vstore` (alive's 856 B script, sha256 f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc, byte-identical) FETCHES the pin over file:// into a root-owned bare store; git index-pack re-hashes every object it receives, so a forged object makes the fetch fail; every later root read goes to that store through GIT_DIR.
# sh + git + jq + python3 (zlib, to forge loose objects) on SCRATCH repos, unprivileged, no systemd, no /etc, no network, 0 USD. The piece comes from `sect agi-vstore` of the .geometry/engine*.md of ROOT (default the working tree); VSTORE=<file> tests a candidate piece (alive's file taken from the node). The unit texts (agi-boot.service, the baked agi-project.service / .path) come from the same ROOT; the baked pair is produced by one real boot. RED today: the section is absent, every row that needs the piece fails (a stub that exits 127; a refusal row also requires the clean row to have passed, so an always-failing verifier proves nothing).
# Lanes: c1 the piece: p0 clean (rc 0, store mode 700, the store holds EXACTLY the pin commit + its trees + the blobs under .agi/nodes/.geometry and .agi/config.json, an unrelated blob NOT readable; the pin is NOT a ref tip, so the --upload-pack flags matter) · p1 a forged .geometry blob · p2 a forged config.json blob · p3 a forged TREE · p4 a forged COMMIT · p5 an objects/info/alternates dir serving a forged blob (MAIN's own copy removed) · p6 a replace ref in MAIN (the store holds the ORIGINAL bytes) · p7 repo config uploadpack.packObjectsHook (a marker file must not appear) · p8 the pin unset / HEAD / a ref name / 39, 41 hex / uppercase / absent from MAIN · p9 the store path pre-planted as a symlink (its target is kept) · p10 a STALE store holding a forged blob is not trusted · p11 GIT_DIR set in the environment (the unit sets it for the store) · p0o the unit's own Environment (safe.directory) lets it read a repo owned by ANOTHER uid (GIT_TEST_ASSUME_DIFFERENT_OWNER=1, empty global config) while the same seam without it is refused. Every forged object is a REAL loose object written under its own sha path with zlib, never a stub.
# c2 agi-boot.service: ExecStartPre=/usr/local/libexec/agi-vstore BEFORE ExecStart, Environment=GIT_DIR=/run/agi-v.git; the boot ExecStart (the unit's Environment words, GIT_DIR rewritten to the scratch store, cwd NOT a repo) after the piece: a clean MAIN starts both boot rows; a MAIN whose pinned engine-root.md / posts.md / config.json object is FORGED refuses (piece rc != 0 AND, the ExecStart run anyway as a belt, rc != 0, 0 setfacl, 0 start, 0 unit file, the hostile script never ran). c3 the baked agi-project.service / .path: EnvironmentFile=/etc/agi/carry.env, its OWN store path (not agi-boot's), ExecStartPre, the literal $AGI_TRUNK, 0 occurrences of the pinned sha and of rev-parse, PathChanged=/etc/agi/carry.env; its ExecStart over a clean store regrows the units, over a forged pinned engine.md refuses. c4 carry.env gains no cell.
# Honest limits: the text and env of the units, not systemd (the ExecStartPre order is read off the line order; EnvironmentFile loading is modelled as AGI_TRUNK set; Environment= is read as space-separated KEY=VAL words); the piece runs as the test's uid, so root's own safe.directory on MAIN is exercised only through the seam; `rm -rf $V` on a path that is a MOUNT is not modelled.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};MARK=$T/marker
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_VSTORE AGI_MAIN AGI_SEAT AGI_POST AGI_RAM AGI_BOOT_OUT GIT_NO_REPLACE_OBJECTS GIT_NO_LAZY_FETCH
[ "$(id -u)" != 0 ]||{ echo "FAIL needs a non-root uid";exit 99;}
export GIT_NO_LAZY_FETCH=1   # P0 sets it ITSELF (DG1 05:09Z): the store keeps a promisor remote to MAIN, so every read this test makes of it must not fetch; the piece's own runs are env -i and set it themselves
mkdir -p $T/fk $T/hm $T/cwd
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
# the piece under test: VSTORE=<file> | sect agi-vstore of ROOT | a stub that exits 127 (so no refusal row can pass on an absent verifier)
VP=$T/agi-vstore;if [ -n "$VSTORE" ];then cp $VSTORE $VP;else sect agi-vstore >$VP;fi;have=1;[ -s $VP ]||{ have=0;printf '#!/bin/sh\nexit 127\n' >$VP;}
printf '#!/bin/sh\necho "setfacl $*">>%s/log\n' $T >$T/fk/setfacl
printf '#!/bin/sh\necho "systemctl $*">>%s/log\n[ "$1" = start ]&&echo "b $2">>%s/log\nexit 0\n' $T $T >$T/fk/systemctl
printf '#!/bin/sh\necho "sysusers $*">>%s/log\nexit 0\n' $T >$T/fk/systemd-sysusers
chmod +x $T/fk/*
echo "0.50 0.5 0.5 1/1 1" >$T/la;printf 'some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/io
row(){ printf '  - {"name": "%s", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' $1;}
# --- the fixture MAIN: the real engine*.md of ROOT, boot rows a b, a config.json with a fast gate, an unrelated blob, GOOD (the pin, NOT a ref tip) then a LATER commit on main
mkm(){ rm -rf $T/m $T/alt $T/vs $T/vp $MARK;D=$T/m/.agi/nodes/.geometry;mkdir -p $D $T/m/.agi/nodes/goal
 cp $R0/.agi/nodes/.geometry/engine*.md $D/;{ printf -- '---\nposts:\n';row a;row b;} >$D/posts.md
 jq '.values.local_maxxing.agi_boot={"poll_s":0.1,"wait_max_s":1,"space_s":0.2}' $R0/.agi/config.json >$T/m/.agi/config.json
 echo "unrelated secret" >$T/m/secret.txt;echo "unrelated node" >$T/m/.agi/nodes/goal/x.md
 $G init -q $T/m;$G -C $T/m add -A;$G -C $T/m commit -qm good;PIN=$($G -C $T/m rev-parse HEAD)
 echo later >$T/m/later.txt;$G -C $T/m add -A;$G -C $T/m commit -qm later
 B_ER=$($G -C $T/m rev-parse $PIN:.agi/nodes/.geometry/engine-root.md);B_EN=$($G -C $T/m rev-parse $PIN:.agi/nodes/.geometry/engine.md);B_P=$($G -C $T/m rev-parse $PIN:.agi/nodes/.geometry/posts.md);B_C=$($G -C $T/m rev-parse $PIN:.agi/config.json);B_S=$($G -C $T/m rev-parse $PIN:secret.txt);B_X=$($G -C $T/m rev-parse $PIN:.agi/nodes/goal/x.md);TG=$($G -C $T/m rev-parse $PIN:.agi/nodes/.geometry);TR=$($G -C $T/m rev-parse $PIN^{tree})
 TIP=$($G -C $T/m rev-parse HEAD);[ "$PIN" != "$TIP" ]||echo "FAIL fixture: the pin is the ref tip";}
# forge OID TYPE SRCFILE [GITDIR]: a REAL loose object under its own sha path (the original removed), content = SRCFILE, zlib'd with the header
forge(){ python3 -c "
import os,sys,zlib
oid,typ,src,gd=sys.argv[1:5]
data=open(src,'rb').read();raw=('%s %d\0'%(typ,len(data))).encode()+data
p=os.path.join(gd,'objects',oid[:2],oid[2:]);os.makedirs(os.path.dirname(p),exist_ok=True)
if os.path.exists(p): os.chmod(p,0o644);os.unlink(p)
open(p,'wb').write(zlib.compress(raw))" "$1" "$2" "$3" "${4:-$T/m/.git}";}
# rawf OID: the raw bytes of an object, from the original MAIN
# OWN = P10 REAL OWNERSHIP, the DEFAULT env of every row (DG1 04:44Z, belam 04:4xZ): env -i, an empty global config, no system config, git's different-owner seam (MAIN counts as owned by ANOTHER uid), and ONLY the fetching store ($V.n) trusted, through the env pair (what the unit's Environment= gives root, narrowed): MAIN is trusted by the piece alone
OWN="GIT_CONFIG_NOSYSTEM=1 GIT_TEST_ASSUME_DIFFERENT_OWNER=1"
# vrun [PIN]: the piece as an unprivileged user under OWN; MAINP overrides MAIN (the bare row); rc in $vrc, stderr $T/v.err
# HOST MODEL (DG1 06:11Z): carry.env's GIT_CONFIG_VALUE_0 is the PATH of AGI_REPO (measured 10-08: /data/work/agi), applied over the unit's inline `*`; root OWNS its own $V and $V.n on the host, so they need no grant there. The seam would make them foreign, so they are granted by the global file $T/own.cfg (not by the env pair as before: that was the seam over-modelling), and the env pair carries the MAIN path.
printf '[safe]\n\tdirectory=%s\n\tdirectory=%s\n' $T/vs $T/vs.n >$T/own.cfg
vrun(){ rm -f $T/v.out $T/v.err;(cd $T/cwd&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/own.cfg GIT_CONFIG_SYSTEM=/dev/null $OWN GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=${CV0:-${MAINP:-$T/m}} ${VENV} AGI_VSTORE=$T/vs AGI_MAIN=${MAINP:-$T/m} ${1-AGI_TRUNK=$PIN} timeout 60 sh $VP >$T/v.out 2>$T/v.err);vrc=$?;}
# inst OID: the object is IN the store (a listing of its own objects: no lazy fetch can make an absent object appear); seen OID WORD: lines of the stored object holding WORD
inst(){ id=$($G -C $T/vs rev-parse --verify -q "$1" 2>/dev/null)||return 1;$G -C $T/vs cat-file --batch-all-objects --batch-check='%(objectname)' 2>/dev/null|grep -qx "$id";}
seen(){ GIT_NO_LAZY_FETCH=1 $G -C $T/vs cat-file -p "$1" 2>/dev/null|grep -c "$2"||true;}
# --- p12 (the digest row, apart from the behaviour rows): the piece is the ruled 856 B file (alive 04:45Z; it REPLACES the 756 B 3be9e024...)
dg=$(sha256sum <$VP|cut -c1-64);sz=$(wc -c <$VP|tr -d ' ')
ok "p12-the-piece-is-alive-s-856-bytes-and-its-sha256 the ### agi-vstore piece: present $have (want 1), $sz bytes (want 856), sha256 $(echo $dg|cut -c1-16)... (want f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc)" '[ $have = 1 ]&&[ $sz = 856 ]&&[ $dg = f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc ]'
# p12 (node): the re-cut brief node carries the piece WHOLE in a fenced block under `## agi-vstore (the piece`; the sha256 of that fenced body is the ruled digest AND it is the piece this lane tests
NODE=$(ls $R0/.agi/nodes/hypothesis/g141-a1b-*.md 2>/dev/null|head -1);: >$T/node.piece;[ -z "$NODE" ]||sed -n '/^## agi-vstore (the piece/,/^## /{/^~~~/,/^~~~/{//!p}}' $NODE >$T/node.piece
nsz=$(wc -c <$T/node.piece|tr -d ' ');ndg=$(sha256sum <$T/node.piece|cut -c1-64)
ok "p12-the-nodes-fenced-piece-is-the-tested-piece the hypothesis node $([ -n "$NODE" ]&&echo found||echo NOT FOUND): its fenced piece is $nsz bytes (want 856), sha256 $(echo $ndg|cut -c1-16)... (want f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc), byte-identical to the piece under test: $(cmp -s $T/node.piece $VP&&echo yes||echo NO) (want yes)" '[ -n "$NODE" ]&&[ "$nsz" = 856 ]&&[ "$ndg" = f60191fd12942280569156cc2308e3ab4ec0c82cbb366676d50e77717b2d1fcc ]&&cmp -s $T/node.piece $VP'
# --- p0 clean
mkm;vrun;mode=$(stat -c %a $T/vs 2>/dev/null);exp=$({ echo $PIN;$G -C $T/m rev-parse $PIN^{tree};$G -C $T/m ls-tree -r -t --format='%(objectname)' $PIN|while read -r id;do [ "$($G -C $T/m cat-file -t $id)" = tree ]&&echo $id;done;echo $B_ER;echo $B_EN;echo $B_P;echo $B_C;$G -C $T/m ls-tree -r --format='%(objectname)' $PIN -- .agi/nodes/.geometry .agi/config.json;}|sort -u|tr '\n' ' ');got=$($G -C $T/vs cat-file --batch-all-objects --batch-check='%(objectname)' 2>/dev/null|sort -u|tr '\n' ' ')
LIVE=0;[ $vrc = 0 ]&&LIVE=1
ok "p0-clean-fetch rc $vrc (want 0), store mode $mode (want 700), the commit present: $(inst $PIN^{commit}&&echo yes||echo NO), the engine-root / posts / config blobs present: $(inst $B_ER&&inst $B_P&&inst $B_C&&echo yes||echo NO), the pin is not a ref tip, stderr $(wc -c <$T/v.err|tr -d ' ') byte(s)" '[ $vrc = 0 ]&&[ "$mode" = 700 ]&&inst $PIN^{commit}&&inst $B_ER&&inst $B_P&&inst $B_C'
ok "p0-the-store-holds-exactly-the-pin-its-trees-and-the-geometry-and-config-blobs the objects in the store equal {commit, every tree, the blobs under .agi/nodes/.geometry and .agi/config.json}: $(echo $got|wc -w|tr -d ' ') in the store, $(echo $exp|wc -w|tr -d ' ') expected, identical: $([ "$got" = "$exp" ]&&echo yes||echo NO)" '[ $LIVE = 1 ]&&[ "$got" = "$exp" ]'
ok "p0-an-unrelated-blob-is-not-readable the unrelated blobs (secret.txt, a goal node, the later commit) are NOT readable from the store: secret $(inst $B_S&&echo READABLE||echo absent), goal node $(inst $B_X&&echo READABLE||echo absent), later commit $(inst $TIP&&echo READABLE||echo absent)" '[ $LIVE = 1 ]&&! inst $B_S&&! inst $B_X&&! inst $TIP'
# --- p1 / p2 forged blobs
printf 'EVIL posts\n' >$T/evil;mkm;forge $B_P blob $T/evil;vrun
ok "p1-a-forged-geometry-blob a loose posts.md blob forged under its own sha path: rc $vrc (want 1, not 127), forged bytes readable from the store: $(seen $B_P EVIL) (want 0)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&[ "$(seen $B_P EVIL)" = 0 ]'
printf '{"EVIL":1}\n' >$T/evil;mkm;forge $B_C blob $T/evil;vrun
ok "p2-a-forged-config-json-blob a loose .agi/config.json blob forged under its own sha path: rc $vrc (want 1, not 127), forged bytes readable: $(seen $B_C EVIL) (want 0)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&[ "$(seen $B_C EVIL)" = 0 ]'
# --- p3 a forged tree (the .geometry tree with posts.md pointing at the unrelated blob), p4 a forged commit
mkm;python3 -c "
import subprocess,sys
g=sys.argv[1];tg=sys.argv[2];bp=sys.argv[3];bs=sys.argv[4]
raw=subprocess.run(['git','-C',g,'cat-file','tree',tg],capture_output=True).stdout
a=bytes.fromhex(bp);b=bytes.fromhex(bs);assert a in raw
open(sys.argv[5],'wb').write(raw.replace(a,b))" $T/m $TG $B_P $B_S $T/evil.tree;forge $TG tree $T/evil.tree;vrun
ok "p3-a-forged-tree the .agi/nodes/.geometry tree forged under its own sha path (posts.md pointed at another blob): rc $vrc (want 1, not 127)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]'
mkm;$G -C $T/m cat-file commit $PIN|sed 's/^good$/forged/' >$T/evil.commit;forge $PIN commit $T/evil.commit;vrun
ok "p4-a-forged-commit the pin commit forged under its own sha path (a different message): rc $vrc (want 1, not 127), the forged commit readable from the store: $(inst $PIN&&echo yes||echo no) (want no)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&! inst $PIN'
# --- p5 an alternates dir serves a forged blob; MAIN'"'"'s own copy is removed
printf 'EVIL via alternates\n' >$T/evil;mkm;rm -f $T/m/.git/objects/$(echo $B_P|cut -c1-2)/$(echo $B_P|cut -c3-);mkdir -p $T/alt;forge $B_P blob $T/evil $T/alt;echo $T/alt/objects >$T/m/.git/objects/info/alternates;vrun
ok "p5-an-alternate-serves-a-forged-blob MAIN's posts.md blob exists only as a forged object in objects/info/alternates: rc $vrc (want 1, not 127), forged bytes readable from the store: $(seen $B_P EVIL) (want 0)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&[ "$(seen $B_P EVIL)" = 0 ]'
# --- p6 a replace ref in MAIN: the store holds the ORIGINAL bytes
mkm;printf 'EVIL replacement\n' >$T/evil;NB=$($G -C $T/m hash-object -w $T/evil);$G -C $T/m replace $B_P $NB;orig=$(GIT_NO_REPLACE_OBJECTS=1 $G -C $T/m cat-file blob $B_P|sha256sum|cut -c1-16);vrun;st=$(GIT_NO_LAZY_FETCH=1 $G -C $T/vs cat-file blob $B_P 2>/dev/null|sha256sum|cut -c1-16)
ok "p6-a-replace-ref-changes-nothing MAIN has refs/replace/<posts.md blob> -> another blob: rc $vrc (want 0), the store's posts.md bytes are the ORIGINAL ($st vs $orig), the replacement not readable from the store: $(inst $NB&&echo READABLE||echo absent)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ "$st" = "$orig" ]&&! inst $NB'
# --- p7 repo config packObjectsHook (honoured only from protected config)
mkm;printf '#!/bin/sh\necho hook >>%s/hookmark\nexec "$@"\n' $T >$T/hook.sh;chmod +x $T/hook.sh;$G -C $T/m config uploadpack.packObjectsHook $T/hook.sh;rm -f $T/hookmark;vrun
ok "p7-a-repo-config-hook-does-not-run MAIN's .git/config sets uploadpack.packObjectsHook to a script that writes a marker: rc $vrc (want 0), marker $([ -e $T/hookmark ]&&echo APPEARED||echo absent) (want absent)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ ! -e $T/hookmark ]'
# --- p8 pins that are not a clean 40-hex commit of MAIN
mkm;$G -C $T/m branch gggggggggggggggggggggggggggggggggggggggg $PIN
for pair in "unset:" "empty:AGI_TRUNK=" "HEAD:AGI_TRUNK=HEAD" "ref-name:AGI_TRUNK=main" "nonhex-40-branch:AGI_TRUNK=gggggggggggggggggggggggggggggggggggggggg" "hex39:AGI_TRUNK=$(printf %s $PIN|cut -c1-39)" "hex41:AGI_TRUNK=${PIN}0" "uppercase:AGI_TRUNK=$(printf %s $PIN|tr a-f A-F)" "absent-from-main:AGI_TRUNK=1234567890abcdef1234567890abcdef12345678";do nm=${pair%%:*};arg=${pair#*:};vrun "$arg"
 ok "p8-pin-$nm the pin is $nm: rc $vrc (want != 0, not 127)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]';done
# --- p9 the store path pre-planted as a symlink: its target is kept
mkm;mkdir -p $T/target;echo keep >$T/target/sentinel;ln -s $T/target $T/vs;vrun
ok "p9-a-symlink-at-the-store-path-keeps-its-target AGI_VSTORE is a symlink to a directory holding a sentinel: rc $vrc (want 0), the target and its sentinel kept: $([ -f $T/target/sentinel ]&&echo yes||echo NO) (want yes), the store path is now a real directory: $([ -d $T/vs ]&&[ ! -L $T/vs ]&&echo yes||echo NO) (want yes), the target holds no repo: $([ ! -e $T/target/HEAD ]&&echo yes||echo NO)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ -f $T/target/sentinel ]&&[ -d $T/vs ]&&[ ! -L $T/vs ]&&[ ! -e $T/target/HEAD ]'
rm -rf $T/target
# --- p9b a STALE store holding a forged blob is not trusted
mkm;$G init -q --bare $T/vs;printf 'EVIL stale\n' >$T/evil;forge $B_P blob $T/evil $T/vs;vrun;st=$(GIT_NO_LAZY_FETCH=1 $G -C $T/vs cat-file blob $B_P 2>/dev/null|sha256sum|cut -c1-16);orig=$($G -C $T/m cat-file blob $B_P|sha256sum|cut -c1-16)
ok "p9b-a-stale-store-is-not-trusted the store path already holds a bare repo with a forged posts.md blob; MAIN is clean: rc $vrc (want 0), the store's posts.md bytes are MAIN's ORIGINAL ($st vs $orig), forged bytes readable: $(seen $B_P EVIL) (want 0)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ "$st" = "$orig" ]&&[ "$(seen $B_P EVIL)" = 0 ]'
# --- p9c GIT_DIR in the environment (the unit sets GIT_DIR for the store): the fetch still lands in the store, the decoy is untouched
mkm;$G init -q --bare $T/decoy;VENV="GIT_DIR=$T/decoy" vrun;VENV=
ok "p9c-a-git-dir-in-the-environment-is-ignored GIT_DIR is set to a decoy bare repo: rc $vrc (want 0), the store holds the pin commit: $(inst $PIN^{commit}&&echo yes||echo NO) (want yes), the decoy holds $($G -C $T/decoy cat-file --batch-all-objects --batch-check 2>/dev/null|wc -l|tr -d ' ') object(s) (want 0)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&inst $PIN^{commit}&&[ "$($G -C $T/decoy cat-file --batch-all-objects --batch-check 2>/dev/null|wc -l|tr -d " ")" = 0 ]'
# --- P10 REAL OWNERSHIP: every row above already ran under OWN. The seam row first (a plain git on MAIN is refused as dubious ownership: the seam bites, so the rows below prove something), then the env pair alone does NOT reach the child upload-pack (the reason the piece carries its own -c), then non-bare and bare MAIN
sect agi-boot.service >$T/unit.txt;UE=$(sed -n 's/^Environment=//p' $T/unit.txt|tr ' ' '\n');UCMD=$(sed -n 's/^ExecStart=//p' $T/unit.txt)
mkm;sn=$(cd $T/cwd&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $OWN git -C $T/m rev-parse HEAD 2>&1|grep -c 'dubious ownership')
ok "p10-the-seam-bites a plain git -C MAIN under OWN (empty config, GIT_TEST_ASSUME_DIFFERENT_OWNER=1) is refused: $sn dubious-ownership line(s) (want 1; 0 = the seam does not bite and every P10 row proves nothing)" '[ "$sn" = 1 ]'
mkm;rm -rf $T/probe;$G init -q --bare $T/probe;(cd $T/cwd&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $OWN GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' git -C $T/probe fetch -q file://$T/m/.git HEAD >/dev/null 2>$T/probe.err);prc2=$?
ok "p10-the-env-pair-does-not-reach-the-child a plain file:// fetch of MAIN under the unit's own env pair (safe.directory=*): rc $prc2 (want != 0), the refusal says dubious ownership: $(grep -c 'dubious ownership' $T/probe.err) line(s) (want >= 1): this is WHY the piece carries -c safe.directory= on the child" '[ $prc2 != 0 ]&&[ "$(grep -c "dubious ownership" $T/probe.err)" -ge 1 ]'
mkm;vrun;nbmode=$(stat -c %a $T/vs 2>/dev/null)
ok "p10-non-bare-main MAIN is a non-bare repo owned by ANOTHER uid (the seam), no safe.directory but the piece's own: rc $vrc (want 0, not 127), store mode $nbmode (want 700), the commit present: $(inst $PIN^{commit}&&echo yes||echo NO), the geometry and config blobs present: $(inst $B_ER&&inst $B_P&&inst $B_C&&echo yes||echo NO), stderr $(wc -c <$T/v.err|tr -d ' ') byte(s)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ "$nbmode" = 700 ]&&inst $PIN^{commit}&&inst $B_ER&&inst $B_P&&inst $B_C'
mkm;rm -rf $T/mb;$G clone -q --bare $T/m $T/mb;MAINP=$T/mb vrun;bmode=$(stat -c %a $T/vs 2>/dev/null)
ok "p10-bare-main MAIN is a BARE repo owned by ANOTHER uid (the gitdir form is chosen by [ -d MAIN/.git ]): rc $vrc (want 0, not 127), store mode $bmode (want 700), the commit present: $(inst $PIN^{commit}&&echo yes||echo NO), the config blob present: $(inst $B_C&&echo yes||echo NO)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ "$bmode" = 700 ]&&inst $PIN^{commit}&&inst $B_C'
rm -rf $T/mb
# --- p0o the piece TEXT: the child carries a narrowed safe.directory, never *
nsd=$(grep -c -e '-c safe\.directory=' $VP||true);nstar=$(grep -c -e 'safe\.directory=\*' -e 'safe\.directory=\\\*' -e "safe\.directory='\*'" $VP||true)
ok "p0o-the-child-carries-a-narrowed-safe-directory the piece text carries -c safe.directory= on $nsd line(s) (want >= 1) and safe.directory=* / =\\* on $nstar line(s) (want 0)" '[ $have = 1 ]&&[ "$nsd" -ge 1 ]&&[ "$nstar" = 0 ]'
# --- B5 MECHANISM (SM mur, DG1 05:09Z; p0o above is only a cheap pre-check: ='*', ="*", =$X evade a substring test and the P10 behaviour rows pass under a wildcard too): a fixture `git` first on PATH logs every argv; the child upload-pack string handed to `fetch --upload-pack` must carry exactly ONE `-c safe.directory=<V>` with V == MAIN's gitdir path EXACTLY (MAIN/.git non-bare, MAIN bare) and no other safe.directory word
mkdir -p $T/shim;cat >$T/shim/git<<'XX'
#!/bin/sh
printf ARGV >>"$GITLOG";for a in "$@";do printf '\t%s' "$a" >>"$GITLOG";done;echo >>"$GITLOG"
exec /usr/bin/git "$@"
XX
chmod +x $T/shim/git
shimrun(){ rm -rf $T/vs $T/vs.n;: >$T/git.log;(cd $T/cwd&&env -i PATH=$T/shim:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/own.cfg GIT_CONFIG_SYSTEM=/dev/null $OWN GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=${CV0:-$1} GITLOG=$T/git.log AGI_VSTORE=$T/vs AGI_MAIN=$1 AGI_TRUNK=$PIN timeout 60 sh $VP >/dev/null 2>$T/v.err);vrc=$?
 awk -F'\t' '{for(i=1;i<=NF;i++)if(index($i,"--upload-pack=")==1)print substr($i,15)}' $T/git.log >$T/ups;nups=$(grep -c . $T/ups||true);bad=0;got=
 while IFS= read -r s;do n1=$(printf '%s' "$s"|grep -o 'safe\.directory'|wc -l|tr -d ' ');x=$(printf '%s' "$s"|sed -n 's/^git -c safe\.directory=\([^ ]*\) .*/\1/p');got="$got [$x]";[ "$n1" = 1 ]&&[ "$x" = "$2" ]||bad=$((bad+1));done <$T/ups;}
mkm;shimrun $T/m $T/m/.git
ok "b5-the-child-upload-pack-carries-exactly-the-gitdir-non-bare MAIN non-bare: rc $vrc (want 0), $nups --upload-pack string(s) handed to fetch (want 2: the commit fetch and the blob fetch), safe.directory values [$got ] (want each exactly $T/m/.git, ONE safe.directory word each), strings off: $bad (want 0)" '[ $vrc = 0 ]&&[ "$nups" = 2 ]&&[ "$bad" = 0 ]'
mkm;rm -rf $T/mb;$G clone -q --bare $T/m $T/mb;shimrun $T/mb $T/mb
ok "b5-the-child-upload-pack-carries-exactly-the-gitdir-bare MAIN bare: rc $vrc (want 0), $nups --upload-pack string(s) (want 2), safe.directory values [$got ] (want each exactly $T/mb, ONE safe.directory word each), strings off: $bad (want 0)" '[ $vrc = 0 ]&&[ "$nups" = 2 ]&&[ "$bad" = 0 ]'
rm -rf $T/mb
# --- P11 ATOMIC: the store is built at $V.n and renamed to $V only after BOTH fetches succeeded. A failure at the SECOND fetch (a geometry blob MAIN does not hold, so the blob:none first fetch succeeds and the blob fetch cannot) leaves neither $V nor $V.n and REMOVES a pre-planted $V; a failure at the FIRST fetch (the pin is absent) leaves neither either
mkm;rm -f $T/m/.git/objects/$(echo $B_C|cut -c1-2)/$(echo $B_C|cut -c3-);mkdir -p $T/vs;echo stale >$T/vs/stale;vrun
ok "p11-a-failure-at-the-second-fetch-leaves-neither-store MAIN lacks the .agi/config.json blob (pre-planted stale store at the path): rc $vrc (want != 0, not 127), the store path exists: $([ -e $T/vs ]&&echo YES||echo no) (want no), $T/vs.n exists: $([ -e $T/vs.n ]&&echo YES||echo no) (want no)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&[ ! -e $T/vs ]&&[ ! -e $T/vs.n ]'
mkm;mkdir -p $T/vs;echo stale >$T/vs/stale;vrun "AGI_TRUNK=1234567890abcdef1234567890abcdef12345678"
ok "p11-a-failure-at-the-first-fetch-leaves-neither-store the pin is absent from MAIN (pre-planted stale store at the path): rc $vrc (want != 0, not 127), the store path exists: $([ -e $T/vs ]&&echo YES||echo no) (want no), $T/vs.n exists: $([ -e $T/vs.n ]&&echo YES||echo no) (want no)" '[ $LIVE = 1 ]&&[ $vrc != 0 ]&&[ $vrc != 127 ]&&[ ! -e $T/vs ]&&[ ! -e $T/vs.n ]'
mkm;vrun
ok "p11-a-success-leaves-only-the-store after a clean run the store path exists and $T/vs.n does not: $([ -d $T/vs ]&&echo yes||echo NO) / $([ -e $T/vs.n ]&&echo YES||echo no) (want yes / no)" '[ $LIVE = 1 ]&&[ $vrc = 0 ]&&[ -d $T/vs ]&&[ ! -e $T/vs.n ]'
# --- c2: agi-boot.service text
pre=$(grep -n '^ExecStartPre=/usr/local/libexec/agi-vstore$' $T/unit.txt|cut -d: -f1);npre=$(grep -c '^ExecStartPre=' $T/unit.txt);xs=$(grep -n '^ExecStart=' $T/unit.txt|cut -d: -f1);gd=$(printf '%s\n' "$UE"|grep -cx 'GIT_DIR=/run/agi-v.git');ec=$(grep -c '^EnvironmentFile=/etc/agi/carry.env$' $T/unit.txt)
ok "c2-boot-unit-runs-the-verifier-before-execstart agi-boot.service: ExecStartPre=/usr/local/libexec/agi-vstore on line ${pre:-none}, ExecStart on line ${xs:-none} (want the Pre first), $npre ExecStartPre line(s) (want 1), Environment GIT_DIR=/run/agi-v.git: $gd (want 1), EnvironmentFile carry.env: $ec (want 1)" '[ -n "$pre" ]&&[ -n "$xs" ]&&[ "$pre" -lt "$xs" ]&&[ "$npre" = 1 ]&&[ "$gd" = 1 ]&&[ "$ec" = 1 ]'
UER=$(printf '%s\n' "$UE"|sed "s#GIT_DIR=/run/agi-v.git#GIT_DIR=$T/vs#");gdw=$(printf '%s\n' "$UER"|grep -c "^GIT_DIR=$T/vs\$")
counts(){ sf=$(grep -c '^setfacl' $T/log||true);st=$(grep -c '^b ' $T/log||true);uf=$(ls $T/out 2>/dev/null|wc -l|tr -d ' ');mk=untouched;[ -e $MARK ]&&mk="TOUCHED($(tr '\n' ' ' <$MARK))";true;}
# B2 COMPOSED CHAIN (SM mur, DG1 05:09Z). The unit runs ExecStartPre then ExecStart with WorkingDirectory=/data/work/agi = MAIN, so START runs with cwd = MAIN (a START that loses its GIT_DIR reads MAIN: that is what row (ii) catches). comp ENVWORDS START runs `sh -c 'PRE && START'` in ONE shell: START only on PRE rc 0, never a START fragment on an absent store; ran = START was reached. The unit's Environment words, GIT_DIR rewritten to the scratch store PRE built.
comp(){ rm -f $T/startran;(set -f;cd $T/m&&env -i $1 timeout 90 sh -c 'sh "$0"&&{ : >"$2";sh -c "$1";}' $VP "$2" $T/startran >$T/x.out 2>$T/err);crc=$?;[ -e $T/startran ]&&ran=1||ran=0;counts;}
pre_only(){ (set -f;cd $T/m&&env -i $1 timeout 60 sh $VP >$T/pre.out 2>$T/pre.err);prc=$?;}
start_only(){ rm -f $T/startran;(set -f;cd $T/m&&env -i $1 timeout 60 sh -c "$2" >$T/x.out 2>$T/err);brc=$?;counts;}
bw(){ echo "PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $OWN AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io $UER AGI_VSTORE=$T/vs AGI_MAIN=$T/m AGI_TRUNK=$PIN";}   # a function: mkm mints a NEW MAIN (a new pin) every time
breset(){ rm -rf $T/vs $T/out $T/ram $MARK;: >$T/log;}
mkm;breset;comp "$(bw)" "$UCMD"
ok "c2-clean-main-boots-through-the-store the composed chain sh -c 'PRE && START' (cwd MAIN, GIT_DIR=$T/vs from the unit) on a clean MAIN: rc $crc (want 0), START reached: $ran (want 1), $st start(s) (want 2), $uf unit file(s) written (want > 0), the unit's GIT_DIR word present: $gdw (want 1)" '[ $LIVE = 1 ]&&[ $gdw = 1 ]&&[ $crc = 0 ]&&[ $ran = 1 ]&&[ $st = 2 ]&&[ $uf -gt 0 ]'
CLEANOK=0;[ $LIVE = 1 ]&&[ $gdw = 1 ]&&[ $crc = 0 ]&&[ $ran = 1 ]&&[ $st = 2 ]&&CLEANOK=1;mkdir -p $T/baked;cp -a $T/out/. $T/baked/ 2>/dev/null;PINBAKE=$PIN
forgeboot(){ nm=$1;oid=$2;src=$3
 mkm;forge $oid blob $src;breset;comp "$(bw)" "$UCMD"
 ok "c2-forged-$nm-refuses-before-the-verifier (i) MAIN's pinned $nm blob is FORGED before PRE: the composed chain rc $crc (want != 0, not 127), START reached: $ran (want 0), MARK $mk (want untouched), $sf setfacl (want 0), $st start (want 0), $uf unit file(s) (want 0)" '[ $CLEANOK = 1 ]&&[ $crc != 0 ]&&[ $crc != 127 ]&&[ $ran = 0 ]&&[ "$mk" = untouched ]&&[ $sf = 0 ]&&[ $st = 0 ]&&[ $uf = 0 ]'
 mkm;breset;pre_only "$(bw)";p0=$prc;forge $oid blob $src;: >$T/log;start_only "$(bw)" "$UCMD";ev=$(grep -c evil $T/log $T/err 2>/dev/null|awk -F: '{n+=$2} END{print n+0}');evu=$(ls $T/out 2>/dev/null|grep -c evil||true)
 ok "c2-forged-$nm-after-the-fetch-reads-the-store (ii) PRE && forge && START: a GOOD store exists (PRE rc $p0, want 0) and MAIN's $nm blob is forged AFTER the fetch: START reads the store and runs the ORIGINAL bytes: rc $brc (want 0), $st start(s) (want 2), $uf unit file(s) (want > 0), MARK $mk (want untouched), the forged row evil started or projected: $ev + $evu (want 0)" '[ $CLEANOK = 1 ]&&[ $p0 = 0 ]&&[ $brc = 0 ]&&[ $st = 2 ]&&[ $uf -gt 0 ]&&[ "$mk" = untouched ]&&[ "$ev" = 0 ]&&[ "$evu" = 0 ]'
 mkm;forge $oid blob $src;breset;start_only "$(bw)" "$UCMD"
 ok "c2-forged-$nm-no-store-nothing-runs (iii) NO store at all (the verifier never ran) and MAIN's $nm blob forged: START alone with GIT_DIR=$T/vs: rc $brc (want != 0), MARK $mk (want untouched), $sf setfacl (want 0), $st start (want 0), $uf unit file(s) (want 0) -- a fail-closed observation, NOT a forgery proof (rows (i) and (ii) are)" '[ $CLEANOK = 1 ]&&[ $brc != 0 ]&&[ "$mk" = untouched ]&&[ $sf = 0 ]&&[ $st = 0 ]&&[ $uf = 0 ]';}
mkm;printf '### agi-boot (1 B)\n~~~sh\n#!/bin/sh\necho boot >>%s\n~~~\n' $MARK >$T/evil.er;forgeboot engine-root.md $B_ER $T/evil.er
mkm;{ printf -- '---\nposts:\n';row a;row b;row evil;} >$T/evil.posts;forgeboot posts.md $B_P $T/evil.posts
mkm;jq '.values.local_maxxing.agi_boot={"poll_s":0.1,"wait_max_s":0,"space_s":0}|.values.local_maxxing.de_live_parents.ceiling_if.loadavg1_lt=0.1' $R0/.agi/config.json >$T/evil.cfg;forgeboot config.json $B_C $T/evil.cfg   # RA15: the forged gate cell NEVER opens (the fixture load is 0.50, the line 0.1) with wait_max_s 0: a START that reads MAIN's forged config.json starts 0 posts and exits != 0; the store's original config (line 16) starts 2
# --- c3: the baked agi-project.service / .path of the clean boot
BS=$T/baked/agi-project.service;BP=$T/baked/agi-project.path;[ -f $BS ]||: >$BS;[ -f $BP ]||: >$BP
bec=$(grep -c '^EnvironmentFile=/etc/agi/carry.env$' $BS);bpre=$(grep -n '^ExecStartPre=/usr/local/libexec/agi-vstore$' $BS|cut -d: -f1);bxs=$(grep -n '^ExecStart=' $BS|cut -d: -f1);bgd=$(sed -n 's/^Environment=//p' $BS|tr ' ' '\n'|sed -n 's/^GIT_DIR=//p');bvs=$(sed -n 's/^Environment=//p' $BS|tr ' ' '\n'|sed -n 's/^AGI_VSTORE=//p')
ok "c3-baked-unit-has-its-own-verified-store the baked agi-project.service: EnvironmentFile carry.env $bec (want 1), ExecStartPre=agi-vstore on line ${bpre:-none} before ExecStart on line ${bxs:-none}, GIT_DIR [$bgd] = AGI_VSTORE [$bvs] (want equal, under /run), and NOT agi-boot's /run/agi-v.git" '[ "$bec" = 1 ]&&[ -n "$bpre" ]&&[ -n "$bxs" ]&&[ "$bpre" -lt "$bxs" ]&&[ -n "$bgd" ]&&[ "$bgd" = "$bvs" ]&&case $bgd in /run/*);;*)false;;esac&&[ "$bgd" != /run/agi-v.git ]'
npin=$(cat $BS $BP|grep -c "$PINBAKE"||true);nrp=$(cat $BS $BP|grep -c 'rev-parse'||true);lit=$(grep '^ExecStart=' $BS|grep -c '\$AGI_TRUNK')
ok "c3-baked-unit-reads-the-pin-at-run-time the baked pair names the pin $npin time(s) (want 0), rev-parse $nrp time(s) (want 0), and the ExecStart carries the literal \$AGI_TRUNK: $lit (want >= 1)" '[ -s $BS ]&&[ "$npin" = 0 ]&&[ "$nrp" = 0 ]&&[ "$lit" -ge 1 ]'
pc=$(grep -c '^PathChanged=/etc/agi/carry.env$' $BP);pn=$(grep -c -E '^Path[A-Za-z]*=' $BP);pg=$(grep -c -E 'logs/|refs/|\.git' $BP)
ok "c3-path-unit-watches-the-pin-file agi-project.path: PathChanged=/etc/agi/carry.env $pc (want 1), $pn Path* line(s) (want 1), lines naming logs/ refs/ or .git: $pg (want 0)" '[ -s $BP ]&&[ "$pc" = 1 ]&&[ "$pn" = 1 ]&&[ "$pg" = 0 ]'
UB=$(sed -n 's/^ExecStart=//p' $BS);BE=$(sed -n 's/^Environment=//p' $BS|tr ' ' '\n'|sed "s#GIT_DIR=$bgd#GIT_DIR=$T/vp#;s#AGI_VSTORE=$bgd#AGI_VSTORE=$T/vp#")
# B2 for the baked unit: WorkingDirectory=%s is $PWD at bake time = MAIN; the same composed chain, the baked unit's own Environment words (GIT_DIR rewritten to the scratch store) + ONLY the pin from carry.env
bcounts(){ hc=$(ls $T/out/agi-post@*.service.d/h.conf 2>/dev/null|wc -l|tr -d ' ');su=$(grep -c '^sysusers' $T/log||true);}
bwb(){ echo "PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $OWN $BE AGI_MAIN=$T/m AGI_TRUNK=$PIN";}
bareset(){ rm -rf $T/vp $T/out $MARK;: >$T/log;}
mkm;bareset;comp "$(bwb)" "$UB";bcounts;BAKEOK=0;[ $LIVE = 1 ]&&[ -n "$UB" ]&&[ $crc = 0 ]&&[ $ran = 1 ]&&[ $hc -gt 0 ]&&[ $su = 1 ]&&BAKEOK=1
ok "c3-baked-execstart-regrows-through-its-store the composed chain sh -c 'PRE && START' of the baked unit (cwd MAIN), clean MAIN, only AGI_TRUNK from carry.env: rc $crc (want 0), START reached: $ran (want 1), $hc post unit drop-in(s) regrown (want > 0), sysusers called $su time(s) (want 1)" '[ $LIVE = 1 ]&&[ -n "$UB" ]&&[ $crc = 0 ]&&[ $ran = 1 ]&&[ $hc -gt 0 ]&&[ $su = 1 ]'
forgeen(){ mkm;awk -v m="echo project >>$MARK" '/^### agi-project /{h=1} {print} h&&!d&&/^#!\/bin\/sh/{print m;d=1}' $T/m/.agi/nodes/.geometry/engine.md >$T/evil.en;forge $B_EN blob $T/evil.en;}
forgeen;bareset;comp "$(bwb)" "$UB";bcounts
ok "c3-forged-pinned-engine-md-refuses-before-the-verifier (i) MAIN's pinned engine.md blob is FORGED before PRE (its agi-project piece would write MARK): the composed chain rc $crc (want != 0, not 127), START reached: $ran (want 0), MARK $mk (want untouched), $hc drop-in(s) regrown (want 0), sysusers $su (want 0)" '[ $BAKEOK = 1 ]&&[ $crc != 0 ]&&[ $crc != 127 ]&&[ $ran = 0 ]&&[ "$mk" = untouched ]&&[ $hc = 0 ]&&[ $su = 0 ]'
mkm;bareset;pre_only "$(bwb)";p0=$prc;awk -v m="echo project >>$MARK" '/^### agi-project /{h=1} {print} h&&!d&&/^#!\/bin\/sh/{print m;d=1}' $T/m/.agi/nodes/.geometry/engine.md >$T/evil.en;forge $B_EN blob $T/evil.en;: >$T/log;start_only "$(bwb)" "$UB";bcounts
ok "c3-forged-pinned-engine-md-after-the-fetch-reads-the-store (ii) PRE && forge && START: a GOOD store exists (PRE rc $p0, want 0) and MAIN's engine.md blob is forged AFTER the fetch: the baked START reads the store and regrows the ORIGINAL: rc $brc (want 0), $hc drop-in(s) regrown (want > 0), sysusers $su (want 1), MARK $mk (want untouched)" '[ $BAKEOK = 1 ]&&[ $p0 = 0 ]&&[ $brc = 0 ]&&[ $hc -gt 0 ]&&[ $su = 1 ]&&[ "$mk" = untouched ]'
forgeen;bareset;start_only "$(bwb)" "$UB";bcounts
ok "c3-forged-pinned-engine-md-no-store-nothing-runs (iii) NO store (the verifier never ran) and MAIN's engine.md forged: the baked START alone with GIT_DIR=$T/vp: rc $brc (want != 0), MARK $mk (want untouched), $hc drop-in(s) regrown (want 0), sysusers $su (want 0) -- a fail-closed observation, NOT a forgery proof (rows (i) and (ii) are)" '[ $BAKEOK = 1 ]&&[ $brc != 0 ]&&[ "$mk" = untouched ]&&[ $hc = 0 ]&&[ $su = 0 ]'
# --- c6 (B6, SM mur, DG1 05:44Z): under the store's bare GIT_DIR the agi-project section's `O=` (`git rev-parse --show-toplevel`) is EMPTY, so every projected h.conf carries `O=` with nothing and the posts' worktree base is lost. START runs with cwd = MAIN, so the value is MAIN's toplevel (`$PWD`). Both composed chains (boot unit, baked unit), clean MAIN, GIT_DIR rewritten to the scratch store: at least one h.conf is projected and EVERY one carries O=<MAIN's physical toplevel> exactly (not empty, not the store path). The mutant is `$(git rev-parse --show-toplevel)` back on engine.md line 90 (RED on both chains).
ohc(){ MT=$(cd $T/m&&pwd -P);nh=0;nbo=0;for hf in $T/out/agi-post@*.service.d/h.conf;do [ -f "$hf" ]||continue;nh=$((nh+1));ov=$(sed -n 's/.* O=\([^ ]*\) .*/\1/p' "$hf");[ "$ov" = "$MT" ]||nbo=$((nbo+1));done;}
mkm;breset;comp "$(bw)" "$UCMD";ohc;crc6=$crc
ok "c6-boot-chain-projects-O-as-MAINs-toplevel the composed boot chain 'PRE && START' (cwd MAIN) on a clean MAIN: rc $crc6 (want 0), $nh h.conf projected (want > 0), $nbo of them with O= other than [$MT] (want 0)" '[ $LIVE = 1 ]&&[ $crc6 = 0 ]&&[ $nh -gt 0 ]&&[ $nbo = 0 ]'
mkm;bareset;comp "$(bwb)" "$UB";ohc;crc6=$crc
ok "c6-baked-chain-projects-O-as-MAINs-toplevel the composed baked chain 'PRE && START' (cwd MAIN) on a clean MAIN: rc $crc6 (want 0), $nh h.conf projected (want > 0), $nbo of them with O= other than [$MT] (want 0)" '[ $LIVE = 1 ]&&[ -n "$UB" ]&&[ $crc6 = 0 ]&&[ $nh -gt 0 ]&&[ $nbo = 0 ]'
nwt=$( { sect agi-project;sect agi-boot;} |grep -cE -e '--show-toplevel|--show-prefix|ls-files|git( -[^ ]+)* (status|worktree)|worktree'||true)
ok "c6-projected-sections-need-no-work-tree the agi-project and agi-boot sections run under a bare GIT_DIR: lines naming --show-toplevel / --show-prefix / ls-files / git status / worktree: $nwt (want 0)" '[ -n "$(sect agi-project)" ]&&[ -n "$(sect agi-boot)" ]&&[ "$nwt" = 0 ]'
# --- c5 (B1): agi-gate (agi-land calls `agi-gate $n` WITHOUT exporting AGI_TRUNK). The verdict must depend only on the candidate: AGI_TRUNK UNSET and a STALE AGI_TRUNK (another valid commit of MAIN with different posts) give the same verdict. This row must NOT set AGI_TRUNK itself (test_agi_boot's run.env does, which is why it stays green today); a replay without AGI_TRUNK=$1 -> empty or stale
sect sect >$T/fk/sect;sect agi-gate >$T/fk/agi-gate;chmod +x $T/fk/sect $T/fk/agi-gate;hg=0;[ -s $T/fk/agi-gate ]&&[ -s $T/fk/sect ]&&hg=1
mkm;sed 's|\\047/^### agi-project /|\\047/^### agi-projectX /|' $T/m/.agi/nodes/.geometry/engine.md >$T/bad.engine;nbad=$(grep -c 'agi-projectX' $T/bad.engine||true)
GOODC=$PIN;cp $T/bad.engine $T/m/.agi/nodes/.geometry/engine.md;$G -C $T/m add -A;$G -C $T/m commit -qm "bad candidate";BADC=$($G -C $T/m rev-parse HEAD)
printf -- '---\nposts:\n' >$T/old.posts;row zold >>$T/old.posts;ob=$($G -C $T/m hash-object -w $T/old.posts);rm -f $T/idx;GIT_INDEX_FILE=$T/idx $G -C $T/m read-tree $GOODC;GIT_INDEX_FILE=$T/idx $G -C $T/m update-index --cacheinfo 100644,$ob,.agi/nodes/.geometry/posts.md;STALE=$(GIT_INDEX_FILE=$T/idx $G -C $T/m commit-tree -m stale $(GIT_INDEX_FILE=$T/idx $G -C $T/m write-tree))
gate(){ (cd $T/m&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null $OWN GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' $1 timeout 60 sh $T/fk/agi-gate $2 >$T/g.out 2>$T/g.err);grc=$?;}
gate "" $GOODC;g1=$grc;gate "" $BADC;g2=$grc;gate "AGI_TRUNK=$STALE" $GOODC;g3=$grc;gate "AGI_TRUNK=$STALE" $BADC;g4=$grc
ok "c5-agi-gate-accepts-a-good-candidate-whatever-AGI_TRUNK the gate piece present: $hg (want 1); a GOOD candidate with AGI_TRUNK UNSET: rc $g1 (want 0); with a STALE AGI_TRUNK=<another commit, different posts> in the env: rc $g3 (want 0)" '[ $hg = 1 ]&&[ $LIVE = 1 ]&&[ "$g1" = 0 ]&&[ "$g3" = 0 ]'
ok "c5-agi-gate-refuses-a-candidate-whose-agi-project-would-not-regrow-whatever-AGI_TRUNK a BAD candidate (its baked ExecStart extracts a section that does not exist: $nbad edit): AGI_TRUNK UNSET rc $g2, STALE AGI_TRUNK rc $g4 (want both != 0 and != 127, identical verdicts)" '[ $hg = 1 ]&&[ "$nbad" = 1 ]&&[ "$g2" != 0 ]&&[ "$g2" != 127 ]&&[ "$g4" != 0 ]&&[ "$g4" != 127 ]'
# --- c4: carry.env gains no cell (the host installer writes the key set; the unit texts use no other cell)
INS=$R0/.agi/context/local-maxxing/aa1m/aa1m-install.sh;keys=$(grep -o "printf 'AGI_BOX=%s[^']*'" $INS 2>/dev/null|head -1|grep -o '[A-Z_0-9]*=%s'|sed 's/=%s//'|sort|tr '\n' ' ')
ok "c4-carry-env-gains-no-cell the installer writes the cells [${keys% }] (want exactly AGI_BOX AGI_HUB AGI_REPO AGI_TRUNK GIT_CONFIG_VALUE_0)" '[ "${keys% }" = "AGI_BOX AGI_HUB AGI_REPO AGI_TRUNK GIT_CONFIG_VALUE_0" ]'
used=$(cat $T/unit.txt $BS|grep -o '\$AGI_[A-Z_]*'|sort -u|tr -d '$'|tr '\n' ' ')
ok "c4-the-units-read-only-existing-cells the \$AGI_* names the two units expand: [${used% }] (want a subset of AGI_BOX AGI_HUB AGI_REPO AGI_TRUNK)" 'for u in $used;do case $u in AGI_BOX|AGI_HUB|AGI_REPO|AGI_TRUNK);;*)false;break;;esac;done'
echo "agi-vstore: $f FAIL";exit $f
