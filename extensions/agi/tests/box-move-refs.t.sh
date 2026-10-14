#!/bin/sh
# box-move-refs.t.sh: goal:g7.16.1.11.39 (council 0a8aa43672 remark 3 + 5a6f6ce9a6; DG2): a box move carries EVERY ref namespace except a NAMED exclude list, counts each namespace before and after, REFUSES when a carried namespace comes up short, and routes the box-local namespaces box-to-box only, never through origin. sh + git, scratch repos only, no network, no root, no sudo, 0 USD.
# It runs the REAL `sh guard/box-move.sh move p1` (SRC = ROOT's, a mutation = SRC=<edited copy>) in a scratch SOURCE repo with refs in many namespaces (heads/posts/other branches, grid, box, held, archive 2 deep, agi, tags, remotes, and `refs/novel/q/r` that NO script names), against a scratch ORIGIN (bare) and a scratch TARGET (a clone, reached through an ssh STUB that runs the remote command locally with /data/work/agi remapped), with stubs for sudo + systemctl (the box-move.t.sh ones). The post under test is p1.
# THE CONTRACT (the builder cuts to it):
#   exclude cell = the fenced block opened by the line ```` ```sh move.exclude ```` in the config:guard node (.agi/nodes/.geometry/guard.md), closed by a bare fence; one entry per line, `refs/<namespace>  <reason>` (namespace = the first two path parts; the reason is free text, one per entry). AGI_MOVE_EXCLUDE_NODE=<path> points the carrier at another copy of that node (guard-init.sh's GUARD_ENV_NODE precedent). The list lives ONLY there: the script holds no namespace names.
#   no cell found (node missing, or the block empty) = rc != 0 BEFORE anything is done ([refs-exclude], the post is not stopped, nothing is pushed).
#   `move` pushes every namespace of the source that is not excluded to the TARGET (never the target's checked-out trunk branch by name: that one goes through carry/trunk + ff, as now), and prints, to stdout, one line per carried namespace `refs <ns> before=<n> after=<m>` (n = the SOURCE count before the first push, m = the TARGET count after the last) and one `refs <ns> excluded: <reason>` per excluded entry.
#   a carried namespace with m < n = `[refs-short] <ns> before=<n> after=<m>` on stderr, rc != 0, and the post is NOT started on the target (the ff + host-act line is never reached). An excluded namespace may come up short without a refusal.
#   origin (public) gets exactly what it gets today: HEAD to refs/heads/local-maxxing/season2/main, no other ref.
#   (goal:g7.16.1.11.39 round 2, council 16:21Z) PREFLIGHT: BEFORE `systemctl stop` and BEFORE the posts-row edit, `git push --dry-run --porcelain` of the SAME refspecs; any '!' line = `[refs-reject] <ref> ...` on stderr, rc 6, nothing touched (the post still runs, the row is unmoved, origin and target are written nothing). A TWO-PART ref (refs/stash) cannot be pushed at all (git receive-pack refuses a 'funny ref'): it is not counted, and each one is REPORTED on stdout as `refs <ref> skipped: ...`, never lost silently (the alternative the council named: exclude it with its reason). The after-check is an IDENTITY check of ref NAMES (a carried namespace with m >= n but one source ref name absent on the target = `[refs-short] <ns> before=<n> after=<m> missing=<k> first=<ref>`); a ref present at another sha is a live writer's race and is not refused (the limit, named).
#   (goal:g7.16.1.11.39.1) UNIT PATHS: BEFORE the stop and the row edit, extensions/agi/guard/unit-paths.sh runs ON THE TARGET (ssh `sh -s POST Key=path...` < the script, AGI_BOX=<target>) and reads the units as RENDERED there (`systemctl cat agi-post@POST.service`, agi-boxwake@POST.service): every host path they name must exist: the command word of each Exec* line (past the - @ + ! : prefixes, and past `env` options / VAR=val), WorkingDirectory, EnvironmentFile, ReadWritePaths, ReadOnlyPaths. A leading '-' is NOT a pass. A missing one = `[unit-path] <unit> <Key> <path> missing on <box>` on stderr, rc 7, nothing touched; agi-post@ unreadable = `[unit-path] <unit> unreadable on <box>`, rc 7. The NAMED exemptions (a path host-act creates after the check, one a post may lack) are the fenced block ```sh move.unit-optional``` of the same config:guard node, `Key path  reason`. /run /proc /dev /sys, non-absolute words and $-words are not checked (the script header says so). It only READS.
#   (goal:g7.16.1.11.40.1.1 target 3a) SYSCTL AFTER-CHECK (the kernel is faked TWICE, a stub `sysctl` on PATH AND a proc dir PROC_SYS=$T/proc, both answering ${SYSCTL_LIVE:-200}, so the lane is green with the sysctl-reading script and with the /proc/sys-reading one): after the refs after-check and BEFORE the post starts, guard/sysctl-check.sh runs ON THE TARGET (`ssh sh -s` < the script): its /etc/sysctl.d/60-agi-vm.conf must be there and agree with the live kernel; else `[sysctl-check]` on stderr, rc 8, the post not started.
#   (goal:g7.16.1.11.39.3) TARGET FIT: BEFORE the stop and the row edit, in the SAME ssh as unit-paths.sh (target-fit.sh is streamed first), the target must have the free space under /data/work/agi that the `sh move.target-fit` cell names (data-free-min-kb) AND a probe file must be creatable and removable in its .git/refs/heads as the pushing uid; else `[target-unfit] <box> df|refs-write <reading>`, rc 9, nothing touched. No cell = rc 5 before anything. A pre-receive hook's verdict and a ref that advances between the dry run and the push are NOT caught (named in the script).
#   (goal:g7.16.1.11.39.4) UNIT REQUIRED: the paths a unit uses INSIDE sh -c strings (invisible to the Exec check; carry.env first) are the fenced block ```sh move.unit-required``` of the same node, `path  reason`, `%i` = the post; each must exist on the target, else `[unit-path] required <path> missing on <box>`, rc 7, nothing touched (same ssh, same refusal shape).
#   (goal:g7.16.1.11.44.7) CAPSULE FLOW: the move CALLS the capsule piece (pack / out / verify / in; no move verb): a DRY pack in a job-owned repo + verify + in in a scratch on the target that mirrors its refs, BEFORE the stop (a non-ff line = `[refs-reject] <ref> ...`, rc 6: doc row 5c, the GATE; the refs-write probe lives here, `[target-unfit] <box> refs-write`, rc 9); after the stop the trunk goes as carry/trunk and the REAL pack / out / one file / in carries the rest; a refused real `in` = `[move-in-failed]`, rc 10, the row reverted, the post started on FROM (RECOVERY). The lane needs ssh-keygen (a throwaway signer) and signs with a per-run gitconfig.
#   box-move.t.sh stays green: the file keeps exactly ONE line holding `$E "cd /data/work/agi`.
# One ok/FAIL line per case; exit = number of FAILs.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};SRC=${SRC:-$R0/extensions/agi/guard/box-move.sh}
SRC=$(cd "$(dirname "$SRC")"&&pwd)/$(basename "$SRC")
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
P=p1;B=$T/bin;mkdir -p $B;TGT=$T/f/w;export TGT
printf '#!/bin/sh\nwhile [ "$1" = -n ];do shift;done\ncase "$1 $2 $3" in "test -f "*/h.conf)exit 1;;esac\nexec "$@"\n' >$B/sudo
printf '#!/bin/sh\ncase "$1" in cat)d=$UNITS_S;[ -n "$ON_TARGET" ]&&d=$UNITS_T;[ -f "$d/$2" ]&&exec cat "$d/$2";exit 1;; esac\necho "$*" >>%s/ctl.log\ncase "$1" in is-active)exit 1;; show)echo "running 0";; esac\nexit 0\n' $T >$B/systemctl
printf '#!/bin/sh\nwhile :;do case "$1" in -F|-o)shift 2;; -*)shift;; *)break;;esac;done\nshift\nexec env ON_TARGET=1 SYSCTL_D=%s/sysd-t PROC_SYS=%s/proc sh -c "$(printf %%s "$*"|sed "s#/data/work/agi#$TGT#g")"\n' $T $T >$B/ssh
case $T in /dev/*|/run/*|/proc/*|/sys/*)echo "FAIL tmp: TMPDIR $T is under /dev /run /proc /sys, which the unit-path check does not read (a vacuous pass): use a disk dir";exit 99;; esac
UP=${UP:-$(dirname $SRC)/unit-paths.sh};[ -s $UP ]||UP=$R0/extensions/agi/guard/unit-paths.sh
SC=${SC:-$(dirname $SRC)/sysctl-check.sh};[ -s $SC ]||SC=$R0/extensions/agi/guard/sysctl-check.sh
TF=${TF:-$(dirname $SRC)/target-fit.sh};[ -s $TF ]||TF=$R0/extensions/agi/guard/target-fit.sh
mkdir -p $T/host $T/us $T/ut;: >$T/host/box-carry;: >$T/host/agi-signers;: >$T/host/agi-signers-repoint;mkdir -p $T/host/rw;UNITS_S=$T/us;UNITS_T=$T/ut;export UNITS_S UNITS_T
printf '#!/bin/sh\n[ "$1" = -n ]&&echo ${SYSCTL_LIVE:-200}\n' >$B/sysctl
printf '#!/bin/sh\necho "Filesystem 1024-blocks Used Available Capacity Mounted on"\necho "fake 99999999 1 ${DF_FREE_KB:-99999999} 1%% /"\n' >$B/df
sysd(){ mkdir -p $1;printf '# the vfs cache stopgap\nvm.vfs_cache_pressure = 200\n' >$1/60-agi-vm.conf; }
chmod +x $B/*;: >$T/sshconf
# the capsule pack is signed: a throwaway key, the ring file, a per-run gitconfig (the move runs with it, never the lane's /dev/null one)
mkdir -p $T/k;ssh-keygen -q -t ed25519 -N '' -f $T/k/prime -C prime >/dev/null;echo "prime@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/prime.pub)" >$T/allowed
printf '[user]\n\tname=prime\n\temail=prime@agi\n\tsigningkey=%s\n[gpg]\n\tformat=ssh\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' $T/k/prime >$T/gc
ENG=${ENG:-$R0/.agi/nodes/.geometry/engine-capsule.md};[ -s $ENG ]||{ echo "FAIL extract: no $ENG";exit 99;}
cat >$T/node.md <<'XX'
# config:guard (fixture)
```sh move.exclude
refs/remotes  a remote-tracking ref is a copy of origin's; the target fetches its own
```
XX
mkdir -p $T/etc;: >$T/etc/carry.env;: >$T/etc/p1.pin
printf '```sh move.unit-required\n%s/etc/carry.env  the fixture unit reads it in an sh -c string\n%s/etc/%%i.pin  a per-post required path (tests %%i)\n```\n' $T $T >>$T/node.md
printf '```sh move.target-fit\ndata-free-min-kb 1000  the fixture floor\n```\n' >>$T/node.md
printf '```sh move.unit-optional\nWorkingDirectory %s/hm/%%i  host-act move creates the post home after this check\nEnvironmentFile %s/hm/%%i.env  an env file a post may not have\n```\n' $T $T >>$T/node.md
# units: the SAME good unit on both boxes by default; a row edits ONE side (the target's: ut)
unitgood(){ printf '[Service]\nWorkingDirectory=%s/hm/%%i\nEnvironmentFile=-%s/hm/%%i.env\nExecStartPre=+/usr/bin/env -i PATH=/usr/bin:/bin %s/host/agi-signers %%i\nExecStartPre=-+%s/host/agi-signers-repoint %%i\nExecStart=sh -c x\nExecStopPost=sh -c agi-flush\nReadWritePaths=-%s/host/rw /run/agi-%%i\n' $T $T $T $T $T >$1/agi-post@p1.service;printf '[Service]\nExecStart=%s/host/box-carry\n' $T >$1/agi-carry@p1.service; }
unitgood $T/us;unitgood $T/ut
# fix: a fresh source (s) + origin (o, bare) + target (w, a clone of s before the move) in $T/f; the source's refs are listed in $T/f/pre (name sha) before the run
fix(){ chmod -R u+w $T/f 2>/dev/null;unset DF_FREE_KB;rm -rf $T/f $T/sysd-s $T/sysd-t;mkdir -p $T/f;sysd $T/sysd-s;sysd $T/sysd-t;export SYSCTL_D=$T/sysd-s;unset SYSCTL_LIVE;: >$T/ctl.log;unitgood $T/us;unitgood $T/ut;cd $T/f;git init -q -b local-maxxing/season2/main s;git init -q --bare o
 ( cd s;mkdir -p .agi/nodes/.geometry extensions/agi/guard
  printf '%s\n' '  - {"name": "p1", "engine": {"v": 4}, "box": "local-town"}' '  - {"name": "p2", "engine": {"v": 4}, "box": "local-town"}' >.agi/nodes/.geometry/posts.md
  printf 'echo act\nexit 0\n' >extensions/agi/guard/host-act-encryption-town.sh;mkdir -p .agi/nodes/doc;printf -- '---\nid: doc:card-p1\nmint_id: 0123456789abcdef0123456789abcdef\ntype: doc\nparents: []\n---\ncard\n' >.agi/nodes/doc/card-p1.md;cp $ENG .agi/nodes/.geometry/engine-capsule.md;cp $UP extensions/agi/guard/unit-paths.sh;cp $SC extensions/agi/guard/sysctl-check.sh;cp $TF extensions/agi/guard/target-fit.sh;git add .;git commit -q -m base;git remote add origin $T/f/o )
 git clone -q s w;git -C w remote remove origin
 ( cd s;t=$(git rev-parse HEAD^{tree});for r in heads/posts/p1 heads/dg4-x heads/other grid/n1/1 grid/n2/1 box/a/b/1 box/a/b/2 held/a/b/1 archive/p1/dir1 archive/p2/dir2 agi/x tags/v1 novel/q/r remotes/origin/main stash;do git update-ref refs/$r $(git commit-tree -m $r $t);done )
 git -C s for-each-ref --format='%(refname) %(objectname)' >$T/f/pre; }
# go NODE: run the move in the source; sets rc, $T/out, $T/err
go(){ mkdir -p $T/proc/vm;echo ${SYSCTL_LIVE:-200} >$T/proc/vm/vfs_cache_pressure;( cd $T/f/s&&env -u AGI_TRUNK GIT_CONFIG_GLOBAL=$T/gc AGI_POST=prime AGI_ALLOWED=$T/allowed PATH=$B:$PATH AGI_MOVE_SSH=$T/sshconf AGI_MOVE_EXCLUDE_NODE=${1:-$T/node.md} sh $SRC move $P >$T/out 2>$T/err );rc=$?; }
# cnt REPO NS: how many refs of REPO sit under refs/<NS>/
cnt(){ git -C $1 for-each-ref --format='%(refname)' refs/$2/|wc -l|tr -d ' '; }
started(){ grep -q "^start agi-post@$P" $T/ctl.log; }
line(){ grep -F '$E "cd /data/work/agi' "$SRC";}
[ -s $SRC ]||{ echo "FAIL extract: no $SRC";exit 99;}

fix;go;ns="heads grid box held archive agi tags novel";nd="";for n in $ns;do a=$(cnt $T/f/w $n);b=$(cnt $T/f/s $n);[ $n = heads ]&&b=$(git -C $T/f/s for-each-ref --format='%(refname)' refs/heads/|grep -c -v carry/trunk);[ "$a" -ge "$b" ]||nd="$nd $n($a/$b)";done
miss=$(while read -r r s;do case $r in refs/remotes/*|refs/heads/local-maxxing/season2/main|refs/stash)continue;; esac;[ "$(git -C $T/f/w rev-parse -q --verify $r 2>/dev/null)" = "$s" ]||echo $r;done <$T/f/pre|tr '\n' ' ')
ok "refs-the-move-succeeds-and-starts-the-post a move with every namespace present ends rc 0 and starts agi-post@$P (rc $rc; ctl: $(tr '\n' '|' <$T/ctl.log); err: $(head -c 200 $T/err|tr '\n' ' '))" '[ $rc = 0 ]&&started'
ok "refs-every-named-ref-arrives-with-its-sha $(echo $miss|wc -w|tr -d ' ') source ref(s) missing or at another sha on the target (want 0): [${miss% }]" '[ -z "$miss" ]'
ok "refs-trunk-still-ffs-on-the-target the target's trunk is the source's moved trunk ($(git -C $T/f/w rev-parse --short HEAD) vs $(git -C $T/f/s rev-parse --short HEAD))" '[ "$(git -C $T/f/w rev-parse HEAD)" = "$(git -C $T/f/s rev-parse HEAD)" ]'
for n in $ns;do ok "refs-namespace-$n-arrives the target holds $(cnt $T/f/w $n) refs/$n/* refs, the source $(cnt $T/f/s $n) (want target >= source)" "[ $(cnt $T/f/w $n) -ge $(cnt $T/f/s $n) ]";done
ok "refs-an-unnamed-namespace-is-carried refs/novel/q/r (named by NO script) is on the target: a carrier that lists what to keep loses it" 'git -C $T/f/w rev-parse -q --verify refs/novel/q/r >/dev/null'
ok "refs-the-excluded-namespace-stays-home refs/remotes/* on the target: $(cnt $T/f/w remotes) (want 0: the cell names it)" '[ $(cnt $T/f/w remotes) = 0 ]'
pr=$(for n in $ns;do b=$(git -C $T/f/s for-each-ref --format='%(refname)' refs/$n/|grep -c -v 'carry/trunk');grep -q -x "refs refs/$n before=$b after=[0-9]*" $T/out||printf '%s ' $n;done)
ok "refs-both-counts-are-printed one 'refs refs/<ns> before=<n> after=<m>' line per carried namespace, n the source's count: wrong or absent for [${pr% }] (want none)" '[ -z "$pr" ]'
ok "refs-the-excluded-entry-is-printed-with-its-reason 'refs refs/remotes excluded: <the cell's reason>' is on stdout ($(grep 'excluded' $T/out|head -c 120))" 'grep -q -F "refs refs/remotes excluded: a remote-tracking ref is a copy of origin" $T/out'
ok "refs-after-counts-are-the-targets every printed after=<m> equals the target's own count of that namespace (a made-up m is RED): bad [$(for n in $ns;do m=$(sed -n "s#^refs refs/$n before=[0-9]* after=\([0-9]*\)\$#\1#p" $T/out);[ "$m" = "$(cnt $T/f/w $n)" ]||printf '%s(%s/%s) ' $n "$m" "$(cnt $T/f/w $n)";done)]" '[ -z "$(for n in $ns;do m=$(sed -n "s#^refs refs/$n before=[0-9]* after=\([0-9]*\)\$#\1#p" $T/out);[ "$m" = "$(cnt $T/f/w $n)" ]||printf x;done)" ]'
o=$(git -C $T/f/o for-each-ref --format='%(refname)'|tr '\n' ' ')
ok "refs-origin-gets-only-the-trunk origin holds [${o% }] (want exactly refs/heads/local-maxxing/season2/main: the box-local namespaces go box-to-box, never through the public origin)" '[ "${o% }" = refs/heads/local-maxxing/season2/main ]'

# a target that loses a carried namespace on receive: refuse, name it, never start the post
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\n[ "$1" = committed ]&&[ -z "$LOOP" ]||exit 0\nexport LOOP=1\ngit for-each-ref --format="%%(refname)" refs/archive/|while read -r r;do git update-ref -d $r;done\n' >$T/f/w/.git/hooks/reference-transaction;chmod +x $T/f/w/.git/hooks/reference-transaction;go
ok "refs-short-namespace-refuses a target that ends with 0 of the 2 refs/archive/* refs ends rc != 0 (rc $rc), not 0" '[ $rc != 0 ]'
ok "refs-short-namespace-is-named stderr names '[refs-short] refs/archive before=2 after=0' ($(head -c 160 $T/err|tr '\n' ' '))" 'grep -q "^\[refs-short\] refs/archive before=2 after=0" $T/err'
ok "refs-short-namespace-never-starts-the-post agi-post@$P is NOT started on the target (ctl: $(tr '\n' '|' <$T/ctl.log))" '! started'
ok "refs-short-namespace-names-only-the-short-one refs/grid (not short) is not named in a [refs-short] line" '! grep -q "^\[refs-short\] refs/grid" $T/err'
# an EXCLUDED namespace that comes up short is not a refusal
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\n[ "$1" = committed ]&&[ -z "$LOOP" ]||exit 0\nexport LOOP=1\ngit for-each-ref --format="%%(refname)" refs/remotes/|while read -r r;do git update-ref -d $r;done\n' >$T/f/w/.git/hooks/reference-transaction;chmod +x $T/f/w/.git/hooks/reference-transaction;go
ok "refs-an-excluded-namespace-may-be-short a target with 0 refs/remotes/* (excluded) still ends rc 0 and starts the post (rc $rc; started: $(started&&echo yes||echo no))" '[ $rc = 0 ]&&started'

# round 2 (e)-2: counts can hide a missing NAME (refs/heads gets carry/trunk on the target, so 5 >= 4 even with refs/heads/other gone)
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\n[ "$1" = committed ]&&[ -z "$LOOP" ]||exit 0\nexport LOOP=1\ngit update-ref -d refs/heads/other\n' >$T/f/w/.git/hooks/reference-transaction;chmod +x $T/f/w/.git/hooks/reference-transaction;go
ok "refs-the-after-check-is-an-identity-check one NAME (refs/heads/other) gone on the target while the refs/heads COUNT stays >= the source's ends rc != 0 ($rc) with '[refs-short] refs/heads ... missing=1 first=refs/heads/other' ($(head -c 200 $T/err|tr '\n' ' ')) and the post is not started" '[ $rc != 0 ]&&grep -q "^\[refs-short\] refs/heads before=[0-9]* after=[0-9]* missing=1 first=refs/heads/other" $T/err&&! started'
# round 2 (e)-1: a two-part ref cannot be pushed: it is reported, not counted, and the move does not refuse after the stop
fix;go
ok "refs-a-two-part-ref-is-reported-not-lost refs/stash (two path parts: git refuses to push a 'funny ref') ends rc $rc (want 0, no [refs-short]: $(head -c 100 $T/err|tr '\n' ' ')) and stdout says 'refs refs/stash skipped: ...' ($(grep -c '^refs refs/stash skipped: ' $T/out) line, want 1)" '[ $rc = 0 ]&&! grep -q refs-short $T/err&&[ $(grep -c "^refs refs/stash skipped: " $T/out) = 1 ]'
# round 2: THE PREFLIGHT. The target holds refs/archive/p1/dir1 one commit AHEAD of the source's: a non-force push of it is rejected. Nothing may be touched.
fix;git -C $T/f/w fetch -q $T/f/s refs/archive/p1/dir1:refs/archive/p1/dir1;git -C $T/f/w update-ref refs/archive/p1/dir1 $(git -C $T/f/w commit-tree -m ahead -p refs/archive/p1/dir1 $(git -C $T/f/w rev-parse refs/archive/p1/dir1^{tree})) ;h0=$(git -C $T/f/s rev-parse HEAD);go
ok "refs-preflight-rejects-and-names-the-ref a target ref AHEAD of the source's (refs/archive/p1/dir1) ends rc 6 ($rc) with '[refs-reject] refs/archive/p1/dir1' on stderr ($(head -c 200 $T/err|tr '\n' ' '))" '[ $rc = 6 ]&&grep -q "^\[refs-reject\] refs/archive/p1/dir1" $T/err'
ok "refs-preflight-runs-before-the-stop the post is NOT stopped and NOT started (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ ! -s $T/ctl.log ]'
ok "refs-preflight-runs-before-the-row-edit the source repo is untouched: HEAD $(git -C $T/f/s rev-parse --short HEAD) (want $(echo $h0|cut -c1-7)), posts.md clean ($(git -C $T/f/s status --short|wc -l|tr -d ' ') change(s), want 0), the row still says local-town ($(grep -c local-town $T/f/s/.agi/nodes/.geometry/posts.md) line(s), want 2)" '[ "$(git -C $T/f/s rev-parse HEAD)" = "$h0" ]&&[ -z "$(git -C $T/f/s status --short)" ]&&[ $(grep -c local-town $T/f/s/.agi/nodes/.geometry/posts.md) = 2 ]'
ok "refs-preflight-writes-nothing origin holds $(git -C $T/f/o for-each-ref|wc -l|tr -d ' ') ref(s) and the target $(cnt $T/f/w grid) refs/grid + $(cnt $T/f/w box) refs/box refs (want 0 0 0: the dry run carried nothing, the OTHER refs did not go ahead of the rejected one)" '[ $(git -C $T/f/o for-each-ref|wc -l|tr -d " ") = 0 ]&&[ $(cnt $T/f/w grid) = 0 ]&&[ $(cnt $T/f/w box) = 0 ]'

# goal:g7.16.1.11.39.1: THE TARGET'S RENDERED UNITS NAME ONLY PATHS THAT EXIST. Each row edits the TARGET's unit (ut); the SOURCE's (us) stays good, so a check that reads the source's units passes wrongly.
fix;go
ok "refs-unit-paths-every-path-present-the-move-completes the good unit (a '-' EnvironmentFile and a '-+' ExecStartPre that exist, /run/agi-p1 unchecked, the home paths exempted by the cell): rc $rc (want 0), the post started ($(started&&echo yes||echo no)), no [unit-path] line ($(grep -c '^\[unit-path\]' $T/err))" '[ $rc = 0 ]&&started&&! grep -q "^\[unit-path\]" $T/err'
ut1(){ fix;sed "$1" $T/ut/agi-post@p1.service >$T/ut/x&&mv $T/ut/x $T/ut/agi-post@p1.service;h0=$(git -C $T/f/s rev-parse HEAD);go; }
untouched(){ [ ! -s $T/ctl.log ]&&[ "$(git -C $T/f/s rev-parse HEAD)" = "$h0" ]&&[ -z "$(git -C $T/f/s status --short)" ]&&[ $(git -C $T/f/o for-each-ref|wc -l|tr -d ' ') = 0 ]&&[ $(cnt $T/f/w archive) = 0 ]; }
ut1 "s#^ExecStartPre=-+$T/host/agi-signers-repoint#ExecStartPre=-+$T/host/gone-repoint#"
ok "refs-unit-paths-a-dash-prefixed-path-is-checked-like-any-other the target's ExecStartPre=-+<path>/gone-repoint (the agi-signers-repoint shape: systemd would skip it silently) ends rc 7 ($rc) with '[unit-path] agi-post@p1.service ExecStartPre $T/host/gone-repoint missing on encryption-town' ($(grep '^\[unit-path\]' $T/err|head -c 220))" '[ $rc = 7 ]&&grep -q -F "[unit-path] agi-post@p1.service ExecStartPre $T/host/gone-repoint missing on encryption-town" $T/err'
ok "refs-unit-paths-refusal-touches-nothing the post is not stopped or started (ctl: $(tr '\n' '|' <$T/ctl.log)), the source HEAD and posts.md are unmoved, origin holds $(git -C $T/f/o for-each-ref|wc -l|tr -d ' ') refs, the target $(cnt $T/f/w archive) refs/archive, and the missing path is still missing: the check only READS ($([ -e $T/host/gone-repoint ]&&echo CREATED||echo still-absent))" 'untouched&&[ ! -e $T/host/gone-repoint ]'
ok "refs-unit-paths-reads-the-targets-units the SOURCE's unit is complete and the TARGET's is not: the move still refuses (rc $rc, want 7): a check that reads the source's own units passes wrongly" '[ $rc = 7 ]'
ut1 "s#$T/host/agi-signers %i#$T/host/gone-signers %i#"
ok "refs-unit-paths-an-env-wrapped-command-is-checked ExecStartPre=+/usr/bin/env -i PATH=.. <path>/gone-signers %i: the command behind env is named missing ($(grep '^\[unit-path\]' $T/err|head -c 200)), rc $rc (want 7)" '[ $rc = 7 ]&&grep -q -F "ExecStartPre $T/host/gone-signers missing" $T/err'
ut1 "s#^ReadWritePaths=-$T/host/rw #ReadWritePaths=-$T/host/gone-rw #"
ok "refs-unit-paths-read-write-paths-are-checked a missing ReadWritePaths entry behind '-' ends rc $rc (want 7) naming $T/host/gone-rw ($(grep -c 'gone-rw missing' $T/err) line)" '[ $rc = 7 ]&&grep -q -F "ReadWritePaths $T/host/gone-rw missing" $T/err'
ut2(){ fix;sed "$1" $T/ut/agi-carry@p1.service >$T/ut/x&&mv $T/ut/x $T/ut/agi-carry@p1.service;h0=$(git -C $T/f/s rev-parse HEAD);go; }
ut2 "s#$T/host/box-carry#$T/host/gone-carry#"
ok "refs-unit-paths-the-carry-unit-is-checked-too (goal:g7.16.1.11.39.2) the target's rendered agi-carry@p1.service names a missing ExecStart path: rc $rc (want 7) with '[unit-path] agi-carry@p1.service ExecStart $T/host/gone-carry missing on encryption-town' ($(grep -c 'agi-carry@p1.service ExecStart '$T'/host/gone-carry missing on encryption-town' $T/err) line), the post not stopped or started, the row unmoved" '[ $rc = 7 ]&&grep -q -F "[unit-path] agi-carry@p1.service ExecStart $T/host/gone-carry missing on encryption-town" $T/err&&untouched'
fix;rm -f $T/ut/agi-post@p1.service;go
ok "refs-unit-paths-an-unreadable-unit-refuses the target has no agi-post@p1.service to read: rc $rc (want 7), '[unit-path] agi-post@p1.service unreadable on encryption-town' ($(grep '^\[unit-path\]' $T/err|head -c 160)), nothing touched" '[ $rc = 7 ]&&grep -q -F "[unit-path] agi-post@p1.service unreadable on encryption-town" $T/err&&[ ! -s $T/ctl.log ]'
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/remotes  a copy of origin\n```\n' >$T/node-noopt.md;sed -n '/^```sh move.target-fit/,/^```$/p' $T/node.md >>$T/node-noopt.md;fix;go $T/node-noopt.md
ok "refs-unit-paths-the-exemptions-are-the-cells-and-nothing-else with NO move.unit-optional block the target's home paths ($T/hm/p1) are not exempt: rc $rc (want 7), '[unit-path] ... WorkingDirectory $T/hm/p1 missing' ($(grep -c 'WorkingDirectory '$T'/hm/p1 missing' $T/err) line)" '[ $rc = 7 ]&&grep -q -F "WorkingDirectory $T/hm/p1 missing" $T/err'

# goal:g7.16.1.11.40.1.1 target 3a (DG1's guard/sysctl-check.sh) as an AFTER-check: the TARGET's /etc/sysctl.d/60-agi-vm.conf must be there and live. The SOURCE's stays good (a check that runs on the source passes wrongly).
fix;go
ok "refs-sysctl-check-good-target-completes the target has 60-agi-vm.conf and the kernel agrees: rc $rc (want 0), the post started ($(started&&echo yes||echo no)), stdout carries the check's 'ok vm.vfs_cache_pressure' ($(grep -c '^ok vm.vfs_cache_pressure' $T/out) line)" '[ $rc = 0 ]&&started&&grep -q "^ok vm.vfs_cache_pressure" $T/out'
fix;rm -f $T/sysd-t/60-agi-vm.conf;go
ok "refs-sysctl-check-a-dropped-conf-refuses the target LOST 60-agi-vm.conf (a box move or a reinstall drops it): rc $rc (want 8), '[sysctl-check]' on stderr ($(grep -c '^\[sysctl-check\]' $T/err) line), 'RED sysctl' on stdout, and agi-post@$P is NOT started on the target (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc = 8 ]&&grep -q "^\[sysctl-check\]" $T/err&&grep -q "^RED sysctl" $T/out&&! started'
fix;SYSCTL_LIVE=100;export SYSCTL_LIVE;go;unset SYSCTL_LIVE
ok "refs-sysctl-check-a-file-the-kernel-does-not-hold-refuses the conf says 200 but the kernel has 100 (sysctl --system not run): rc $rc (want 8), the post is NOT started" '[ $rc = 8 ]&&! started'

# goal:g7.16.1.11.39.3: THE TARGET MUST FIT THE CARRY, checked before anything is touched.
fix;go
ok "refs-target-fit-fine-target-completes enough free space and a writable refs dir: rc $rc (want 0), the post started ($(started&&echo yes||echo no)), no probe file left on the target ($(ls -A $TGT/.git/refs/heads|grep -c unfit-probe) left, want 0)" '[ $rc = 0 ]&&started&&[ $(ls -A $TGT/.git/refs/heads|grep -c unfit-probe) = 0 ]'
fix;DF_FREE_KB=500;export DF_FREE_KB;h0=$(git -C $T/f/s rev-parse HEAD);go;unset DF_FREE_KB
ok "refs-target-fit-a-full-disk-refuses-before-the-stop the target has 500 KB free, the floor is 1000: rc $rc (want 9), '[target-unfit] encryption-town df 500 KB free' ($(grep -c 'target-unfit\] encryption-town df 500 KB free' $T/err) line), nothing touched" '[ $rc = 9 ]&&grep -q "\[target-unfit\] encryption-town df 500 KB free" $T/err&&untouched'
fix;chmod a-w $TGT/.git/refs/heads;h0=$(git -C $T/f/s rev-parse HEAD);go;chmod u+w $TGT/.git/refs/heads
if [ "$(id -u)" = 0 ];then ok "refs-target-fit-a-read-only-refs-dir-refuses (SKIPPED as root: root writes anywhere)" 'true'
else ok "refs-target-fit-a-read-only-refs-dir-refuses the target's .git/refs/heads is read-only for the pushing uid: rc $rc (want 9), '[target-unfit] encryption-town refs-write' ($(grep -c 'target-unfit\] encryption-town refs-write' $T/err) line), nothing touched" '[ $rc = 9 ]&&grep -q "\[target-unfit\] encryption-town refs-write" $T/err&&untouched';fi
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/remotes  a copy of origin\n```\n' >$T/node-nofit.md;sed -n '/^```sh move.unit-optional/,/^```$/p' $T/node.md >>$T/node-nofit.md;fix;h0=$(git -C $T/f/s rev-parse HEAD);go $T/node-nofit.md
ok "refs-target-fit-no-cell-no-move with no move.target-fit block: rc $rc (want 5), '[target-unfit] no data-free-min-kb' ($(grep -c 'no data-free-min-kb' $T/err) line), nothing touched" '[ $rc = 5 ]&&grep -q "no data-free-min-kb" $T/err&&untouched'
fix;rm -f $T/f/s/extensions/agi/guard/target-fit.sh;h0=$(git -C $T/f/s rev-parse HEAD);go
ok "refs-target-fit-a-missing-script-fails-closed the source has no extensions/agi/guard/target-fit.sh: rc $rc (want 5), '[target-unfit] ... is missing here' ($(grep -c 'target-fit.sh is missing here' $T/err) line), the check does NOT silently vanish, nothing touched (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc = 5 ]&&grep -q "target-fit.sh is missing here" $T/err&&[ ! -s $T/ctl.log ]'

# goal:g7.16.1.11.39.4: paths used INSIDE sh -c strings are required by the move.unit-required cell.
fix;go
ok "refs-unit-required-present-the-move-completes carry.env and the per-post pin exist: rc $rc (want 0), the post started ($(started&&echo yes||echo no)), no '[unit-path] required' line ($(grep -c 'unit-path\] required' $T/err))" '[ $rc = 0 ]&&started&&! grep -q "unit-path\] required" $T/err'
fix;rm -f $T/etc/carry.env;h0=$(git -C $T/f/s rev-parse HEAD);go
ok "refs-unit-required-a-missing-carry-env-refuses a target without carry.env (the post would start with AGI_BOX EMPTY): rc $rc (want 7), '[unit-path] required $T/etc/carry.env missing on encryption-town' ($(grep -c 'unit-path\] required '$T'/etc/carry.env missing on encryption-town' $T/err) line), nothing touched" '[ $rc = 7 ]&&grep -q -F "[unit-path] required $T/etc/carry.env missing on encryption-town" $T/err&&untouched'
fix;rm -f $T/etc/p1.pin;h0=$(git -C $T/f/s rev-parse HEAD);go
ok "refs-unit-required-%i-is-the-post a required path with %i (…/etc/%i.pin) missing: rc $rc (want 7), the line names $T/etc/p1.pin ($(grep -c 'required '$T'/etc/p1.pin missing' $T/err) line)" '[ $rc = 7 ]&&grep -q -F "[unit-path] required $T/etc/p1.pin missing on" $T/err&&untouched'
: >$T/etc/p1.pin;: >$T/etc/carry.env

# the cell is the ONLY list
sed 's#^refs/remotes .*#&\nrefs/agi  scratch bookkeeping the target rebuilds#' $T/node.md >$T/node-add.md;fix;go $T/node-add.md
ok "refs-the-cell-is-the-only-list-add an entry added to the cell (refs/agi) is NOT carried: target refs/agi/*: $(cnt $T/f/w agi) (want 0), printed 'excluded: scratch bookkeeping' ($(grep -c 'refs refs/agi excluded: scratch bookkeeping' $T/out)), rc $rc" '[ $rc = 0 ]&&[ $(cnt $T/f/w agi) = 0 ]&&grep -q "refs refs/agi excluded: scratch bookkeeping" $T/out'
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/agi  scratch bookkeeping the target rebuilds\n```\n' >$T/node-sw.md;sed -n '/^```sh move.unit-optional/,/^```$/p;/^```sh move.target-fit/,/^```$/p' $T/node.md >>$T/node-sw.md;fix;go $T/node-sw.md
ok "refs-the-cell-is-the-only-list-remove refs/remotes taken OUT of the cell is carried: target refs/remotes/*: $(cnt $T/f/w remotes) (want >= 1), rc $rc" '[ $rc = 0 ]&&[ $(cnt $T/f/w remotes) -ge 1 ]'
# no cell, no move
fix;go $T/nonexistent.md;pre=$(git -C $T/f/o for-each-ref|wc -l|tr -d ' ')
ok "refs-no-cell-no-move a missing exclude node ends rc != 0 ($rc), says [refs-exclude] ($(head -c 100 $T/err|tr '\n' ' ')), never stops the post (ctl: $(tr '\n' '|' <$T/ctl.log)), pushes nothing (origin refs $pre, target archive $(cnt $T/f/w archive))" '[ $rc != 0 ]&&grep -q "^\[refs-exclude\]" $T/err&&! grep -q "^stop" $T/ctl.log&&[ $pre = 0 ]&&[ $(cnt $T/f/w archive) = 0 ]'
printf '# config:guard (fixture)\n```sh move.exclude\n```\n' >$T/node-empty.md;fix;go $T/node-empty.md
ok "refs-an-empty-cell-is-no-cell an exclude block with no entry ends rc != 0 ($rc) before the post is stopped (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc != 0 ]&&! grep -q "^stop" $T/ctl.log'

# goal:g7.16.1.11.44.7: THE BOX MOVE CALLS THE CAPSULE VERBS (doc:g716111-44-capsule-pack section 6): pack / out / verify / in, no `move` verb. A MUTANT row edits a copy of box-move.sh with ONE sed and passes only when the clean row's condition is FALSE for it.
mutgo(){ mkdir -p $T/m;sed "$1" $SRC >$T/m/box-move.sh;if cmp -s $SRC $T/m/box-move.sh;then echo "FAIL mutant $2 changed nothing";f=$((f+1));return 1;fi;S0=$SRC;SRC=$T/m/box-move.sh;go;SRC=$S0; }
refs_other(){ git -C $1 for-each-ref --format='%(refname) %(objectname)'|grep -v -e ' refs/capsule/' -e '^refs/capsule/' -e '^refs/heads/local-maxxing/season2/main ' -e '^refs/remotes/'; }
fix;go;CS=$(git -C $T/f/s for-each-ref --format='%(refname) %(objectname)' refs/capsule/);CT=$(git -C $T/f/w for-each-ref --format='%(refname) %(objectname)' refs/capsule/)
ok "capsule-the-real-pack-lands-one-signed-ref-on-both-boxes after a good move MAIN holds $(cnt $T/f/s capsule) refs/capsule/* ref (want 1: the REAL pack; the dry run's is in a job-owned repo) and the target holds the SAME ref+sha ([$CT] vs [$CS])" '[ $rc = 0 ]&&[ $(cnt $T/f/s capsule) = 1 ]&&[ -n "$CS" ]&&[ "$CS" = "$CT" ]'
ok "capsule-the-move-calls-the-four-verbs-and-no-move-verb box-move.sh runs the piece's pack, out, verify and in, and pushes ONLY the trunk branch to the target ($(grep -c 'git push -q ssh://' $SRC) push, want 1)" 'grep -q "cap pack" $SRC&&grep -q "cap out" $SRC&&grep -q "TI verify" $SRC&&grep -q "TI in " $SRC&&grep -q "D/cap in" $SRC&&[ $(grep -c "git push -q ssh://" $SRC) = 1 ]&&! grep -q -E "cap move" $SRC'
# the dry run is job-owned: a refused move leaves MAIN's refs/capsule/* count unchanged (the design's PRE-STOP row)
pre_ahead(){ fix;git -C $T/f/w fetch -q $T/f/s refs/archive/p1/dir1:refs/archive/p1/dir1;git -C $T/f/w update-ref refs/archive/p1/dir1 $(git -C $T/f/w commit-tree -m ahead -p refs/archive/p1/dir1 $(git -C $T/f/w rev-parse refs/archive/p1/dir1^{tree}));git -C $T/f/s for-each-ref --format='%(refname) %(objectname)' >$T/pre2; }
pre_ahead;go
ok "capsule-a-dry-run-leaves-mains-capsule-refs-unchanged a refused move (rc $rc, want 6) leaves MAIN with $(cnt $T/f/s capsule) refs/capsule/* (want 0)" '[ $rc = 6 ]&&[ $(cnt $T/f/s capsule) = 0 ]'
pre_ahead;mutgo 's#CD=\$(cd \$J/dry&&#CD=$(#;s#(cd \$J/dry&&AGI_TRUNK#(AGI_TRUNK#' dry-in-main
ok "capsule-mutant-the-dry-pack-in-MAIN-is-RED the dry pack run in MAIN leaves $(cnt $T/f/s capsule) refs/capsule/* after a refused move (the clean row wants 0: this one must NOT be 0)" '[ $(cnt $T/f/s capsule) != 0 ]'
# GATE (doc row 5c, council 3/3 06:38Z 10-14): the target's refs/grid has a ref the source line is NOT a fast-forward of -> the PRE-STOP, which mirrors MAIN's refs/grid in a scratch on the target, exits rc 6 NAMED, the post still on FROM, FROM's refs unchanged
grid_div(){ fix;git -C $T/f/w update-ref refs/grid/n1/1 $(git -C $T/f/w commit-tree -m diverged $(git -C $T/f/w rev-parse 'HEAD^{tree}'));gw=$(git -C $T/f/w rev-parse refs/grid/n1/1);refs_other $T/f/s >$T/pre5;h0=$(git -C $T/f/s rev-parse HEAD); }
grid_div;go
ok "capsule-gate-5c-a-non-ff-grid-line-refuses-before-the-stop the target's refs/grid/n1/1 is a commit the source's line is not a fast-forward of: rc $rc (want 6), '[refs-reject] refs/grid/n1/1' on stderr ($(grep -c '^\[refs-reject\] refs/grid/n1/1' $T/err) line), nothing stopped or started (ctl: $(tr '\n' '|' <$T/ctl.log)), the target's line unmoved" '[ $rc = 6 ]&&grep -q "^\[refs-reject\] refs/grid/n1/1" $T/err&&[ ! -s $T/ctl.log ]&&[ "$(git -C $T/f/w rev-parse refs/grid/n1/1)" = "$gw" ]'
ok "capsule-gate-5c-from-is-untouched FROM's refs are the same set+shas as before (diff: $(refs_other $T/f/s|diff $T/pre5 - |wc -l|tr -d ' ') line(s), want 0), its HEAD $(git -C $T/f/s rev-parse --short HEAD) = $(echo $h0|cut -c1-7), posts.md clean, origin holds $(git -C $T/f/o for-each-ref|wc -l|tr -d ' ') refs (want 0)" 'refs_other $T/f/s|cmp -s $T/pre5 -&&[ "$(git -C $T/f/s rev-parse HEAD)" = $h0 ]&&[ -z "$(git -C $T/f/s status --short)" ]&&[ $(git -C $T/f/o for-each-ref|wc -l|tr -d " ") = 0 ]'
grid_div;mutgo "s#'+refs/\*:refs/\*'&&cd s#'+refs/heads/*:refs/heads/*'\&\&cd s#" plain-clone-scratch
ok "capsule-gate-5c-mutant-a-scratch-without-the-grid-mirror-is-RED a PRE-STOP scratch that mirrors only the heads (a plain clone) lets the non-ff grid line through: rc $rc (the clean row wants 6: this one must NOT be 6)" '[ $rc != 6 ]'
grid_div;mutgo 's#&&\$TI in \.\./b##' verify-only
ok "capsule-gate-5c-mutant-no-dry-in-is-RED a PRE-STOP that only VERIFIES (never runs the scratch in) lets the non-ff grid line through: rc $rc (the clean row wants 6: this one must NOT be 6)" '[ $rc != 6 ]'
# RECOVERY (section 6, sA2): the REAL `in` refused after the stop -> [move-in-failed], the row reverted by a second commit, the post started on FROM, FROM's refs unchanged, the target gained nothing
recov_fix(){ fix;mkdir -p $TGT/.git/refs/archive/p1;: >$TGT/.git/refs/archive/p1/dir1.lock;refs_other $T/f/s >$T/pre6; }
recov_fix;go
ok "capsule-recovery-a-refused-real-in-reverts-the-row-and-restarts-from the target's refs/archive/p1/dir1 is locked (the scratch cannot see a lock held in MAIN): rc $rc (want 10), '[move-in-failed]' on stderr ($(grep -c '^\[move-in-failed\]' $T/err) line), agi-post@$P started on FROM after the stop (ctl: $(tr '\n' '|' <$T/ctl.log)), the row at HEAD says local-town ($(git -C $T/f/s show HEAD:.agi/nodes/.geometry/posts.md|grep -c '"box": "local-town"') of 2), posts.md clean" '[ $rc = 10 ]&&grep -q "^\[move-in-failed\]" $T/err&&grep -q "^stop agi-post@$P" $T/ctl.log&&grep -q "^start agi-post@$P" $T/ctl.log&&[ $(git -C $T/f/s show HEAD:.agi/nodes/.geometry/posts.md|grep -c "\"box\": \"local-town\"") = 2 ]&&[ -z "$(git -C $T/f/s status --short)" ]'
ok "capsule-recovery-is-lossless FROM's refs apart from the trunk branch and refs/capsule are the same set+shas as before (diff: $(refs_other $T/f/s|diff $T/pre6 - |wc -l|tr -d ' ') line(s), want 0), the target holds $(cnt $T/f/w grid) refs/grid + $(cnt $T/f/w box) refs/box (want 0 0), origin's row says local-town ($(git -C $T/f/o show refs/heads/local-maxxing/season2/main:.agi/nodes/.geometry/posts.md|grep -c '"box": "local-town"') of 2)" 'refs_other $T/f/s|cmp -s $T/pre6 -&&[ $(cnt $T/f/w grid) = 0 ]&&[ $(cnt $T/f/w box) = 0 ]&&[ $(git -C $T/f/o show refs/heads/local-maxxing/season2/main:.agi/nodes/.geometry/posts.md|grep -c "\"box\": \"local-town\"") = 2 ]'
recov_fix;mutgo 's#git revert --no-edit HEAD >/dev/null&&##' no-revert
ok "capsule-recovery-mutant-no-revert-is-RED a RECOVERY that never reverts the row leaves HEAD's row at encryption-town ($(git -C $T/f/s show HEAD:.agi/nodes/.geometry/posts.md|grep -c '"box": "local-town"') of 2 local-town; the clean row wants 2: this one must NOT be 2)" '[ $(git -C $T/f/s show HEAD:.agi/nodes/.geometry/posts.md|grep -c "\"box\": \"local-town\"") != 2 ]'
recov_fix;mutgo 's#;sudo -n systemctl start agi-post@\$P;exit 10#;exit 10#' no-restart
ok "capsule-recovery-mutant-no-restart-is-RED a RECOVERY that never starts the post on FROM: start logged ($(grep -c '^start agi-post@'$P $T/ctl.log)); the clean row wants 1: this one must NOT log one" '! grep -q "^start agi-post@$P" $T/ctl.log'
ok "capsule-the-probe-left-target-fit-and-lives-in-the-prestop-step target-fit.sh holds $(grep -c unfit-probe $TF) probe line(s) (want 0, the df floor stays: $(grep -c 'df -Pk' $TF)), box-move.sh holds $(grep -c 'unfit-probe' $SRC) (want 1)" '[ $(grep -c unfit-probe $TF) = 0 ]&&[ $(grep -c "df -Pk" $TF) -ge 1 ]&&[ $(grep -c unfit-probe $SRC) = 1 ]'

# SSH'S OWN rc 255 (council, L14 residue): ssh that cannot reach the target is not a unit-path refusal; it is named [ssh] rc 255, nothing touched
sshdown(){ fix;cp $B/ssh $T/ssh.real;printf '#!/bin/sh\nexit 255\n' >$B/ssh;h0=$(git -C $T/f/s rev-parse HEAD);go; }
sshup(){ cp $T/ssh.real $B/ssh;chmod +x $B/ssh; }
sshdown;r1=$rc;e1=$(grep -c '^\[ssh\] rc 255' $T/err);u1=$(grep -c '^\[unit-path\]' $T/err);sshup
ok "ssh-an-unreachable-target-is-named-ssh-rc-255-not-a-unit-path ssh exits 255: rc $r1 (want 255), '[ssh] rc 255' on stderr ($e1 line, want 1), no '[unit-path]' line ($u1, want 0), the post not stopped or started, the row unmoved" '[ $r1 = 255 ]&&[ $e1 = 1 ]&&[ $u1 = 0 ]&&untouched'
sshdown;mutgo 's#\[ \$r != 255 \]||{ echo "\[ssh\][^;]*;exit 255;};##' no-ssh-branch;sshup
ok "ssh-mutant-the-255-branch-dropped-is-RED a box-move.sh that never names ssh's own rc ends rc $rc and prints $(grep -c '^\[unit-path\]' $T/err) '[unit-path]' line(s) for an unreachable target (the clean row wants rc 255 and 0: this one must NOT be rc 255)" '[ $rc != 255 ]'
# the tree under test
n=$(grep -c -F '$E "cd /data/work/agi' $SRC)
ok "refs-the-host-act-line-stays-one $SRC holds $n line(s) with \$E \"cd /data/work/agi (want 1: box-move.t.sh extracts it)" '[ $n = 1 ]'
G=$R0/.agi/nodes/.geometry/guard.md;ent=$(sed -n '/^```sh move.exclude/,/^```$/p' $G 2>/dev/null|grep -E '^refs/[a-z0-9_-]+  *[^ ]');ne=$(echo "$ent"|grep -c .)
bad=$([ -n "$ent" ]&&echo "$ent"|awk '{n=$1;sub(/^[^ ]+ +/,"");if(length($0)<8)print n" (reason too short)"; if(n~/^refs\/(heads|grid|box|held|archive|agi)$/)print n" (must be carried)"}'|tr '\n' ' ')
ok "refs-the-real-cell-exists-and-excludes-nothing-that-must-move $G holds the move.exclude block with $ne entr(ies) (want >= 1), each with a reason of >= 8 chars, none of heads/grid/box/held/archive/agi: [${bad% }]" '[ $ne -ge 1 ]&&[ -z "$bad" ]'
uo=$(sed -n '/^```sh move.unit-optional/,/^```$/p' $G 2>/dev/null|grep -E '^(Exec[A-Za-z]*|WorkingDirectory|EnvironmentFile|ReadWritePaths|ReadOnlyPaths)  *[^ ]');nu=$(echo "$uo"|grep -c .)
ub=$(echo "$uo"|awk '{k=$1;p=$2;sub(/^[^ ]+ +[^ ]+ +/,"");if(length($0)<8)print k" "p" (reason too short)"; if(k ~ /^Exec/)print k" "p" (a command is never exempt)"; if(p ~ /signers|repoint|sbin|opt\/agi/)print k" "p" (a host tool is never exempt)"}'|tr '\n' ' ')
ok "refs-the-real-unit-optional-cell-exists-and-exempts-no-command $G holds the move.unit-optional block with $nu entr(ies) (want >= 1), each with a reason of >= 8 chars, none an Exec* key and none naming the signers / a host tool: [${ub% }]" '[ $nu -ge 1 ]&&[ -z "$ub" ]'
tf=$(sed -n '/^```sh move.target-fit/,/^```$/p' $G 2>/dev/null|awk '$1=="data-free-min-kb"{print $2}');tr_=$(sed -n '/^```sh move.target-fit/,/^```$/p' $G 2>/dev/null|grep -c 'measured')
ok "refs-the-real-target-fit-cell-exists-with-a-measured-floor $G holds move.target-fit with data-free-min-kb=[$tf] (want a number >= 1048576) and a reason naming the measured size ($tr_ line with 'measured', want >= 1)" 'case $tf in ""|*[!0-9]*)false;; *)[ $tf -ge 1048576 ];; esac&&[ $tr_ -ge 1 ]'
ur=$(sed -n '/^```sh move.unit-required/,/^```$/p' $G 2>/dev/null|grep -E '^/[^ ]+  *[^ ]');ur1=$(echo "$ur"|head -1|awk '{print $1}');urr=$(echo "$ur"|head -1|sed 's/^[^ ]* *//'|wc -c)
ok "refs-the-real-unit-required-cell-names-carry-env-first $G holds move.unit-required whose first entry is [$ur1] (want /etc/agi/carry.env) with a reason of $urr chars (want >= 12)" '[ "$ur1" = /etc/agi/carry.env ]&&[ $urr -ge 12 ]'
echo "box-move-refs: $f FAIL";exit $f
