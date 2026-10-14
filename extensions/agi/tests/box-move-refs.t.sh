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
mkdir -p $T/host $T/us $T/ut;: >$T/host/box-carry;: >$T/host/agi-signers;: >$T/host/agi-signers-repoint;mkdir -p $T/host/rw;UNITS_S=$T/us;UNITS_T=$T/ut;export UNITS_S UNITS_T
printf '#!/bin/sh\n[ "$1" = -n ]&&echo ${SYSCTL_LIVE:-200}\n' >$B/sysctl
sysd(){ mkdir -p $1;printf '# the vfs cache stopgap\nvm.vfs_cache_pressure = 200\n' >$1/60-agi-vm.conf; }
chmod +x $B/*;: >$T/sshconf
cat >$T/node.md <<'XX'
# config:guard (fixture)
```sh move.exclude
refs/remotes  a remote-tracking ref is a copy of origin's; the target fetches its own
```
XX
printf '```sh move.unit-optional\nWorkingDirectory %s/hm/%%i  host-act move creates the post home after this check\nEnvironmentFile %s/hm/%%i.env  an env file a post may not have\n```\n' $T $T >>$T/node.md
# units: the SAME good unit on both boxes by default; a row edits ONE side (the target's: ut)
unitgood(){ printf '[Service]\nWorkingDirectory=%s/hm/%%i\nEnvironmentFile=-%s/hm/%%i.env\nExecStartPre=+/usr/bin/env -i PATH=/usr/bin:/bin %s/host/agi-signers %%i\nExecStartPre=-+%s/host/agi-signers-repoint %%i\nExecStart=sh -c x\nExecStopPost=sh -c agi-flush\nReadWritePaths=-%s/host/rw /run/agi-%%i\n' $T $T $T $T $T >$1/agi-post@p1.service;printf '[Service]\nExecStart=%s/host/box-carry\n' $T >$1/agi-carry@p1.service; }
unitgood $T/us;unitgood $T/ut
# fix: a fresh source (s) + origin (o, bare) + target (w, a clone of s before the move) in $T/f; the source's refs are listed in $T/f/pre (name sha) before the run
fix(){ rm -rf $T/f $T/sysd-s $T/sysd-t;mkdir -p $T/f;sysd $T/sysd-s;sysd $T/sysd-t;export SYSCTL_D=$T/sysd-s;unset SYSCTL_LIVE;: >$T/ctl.log;unitgood $T/us;unitgood $T/ut;cd $T/f;git init -q -b local-maxxing/season2/main s;git init -q --bare o
 ( cd s;mkdir -p .agi/nodes/.geometry extensions/agi/guard
  printf '%s\n' '  - {"name": "p1", "engine": {"v": 4}, "box": "local-town"}' '  - {"name": "p2", "engine": {"v": 4}, "box": "local-town"}' >.agi/nodes/.geometry/posts.md
  printf 'echo act\nexit 0\n' >extensions/agi/guard/host-act-encryption-town.sh;cp $UP extensions/agi/guard/unit-paths.sh;cp $SC extensions/agi/guard/sysctl-check.sh;git add .;git commit -q -m base;git remote add origin $T/f/o )
 git clone -q s w;git -C w remote remove origin
 ( cd s;t=$(git rev-parse HEAD^{tree});for r in heads/posts/p1 heads/dg4-x heads/other grid/n1/1 grid/n2/1 box/a/b/1 box/a/b/2 held/a/b/1 archive/p1/dir1 archive/p2/dir2 agi/x tags/v1 novel/q/r remotes/origin/main stash;do git update-ref refs/$r $(git commit-tree -m $r $t);done )
 git -C s for-each-ref --format='%(refname) %(objectname)' >$T/f/pre; }
# go NODE: run the move in the source; sets rc, $T/out, $T/err
go(){ mkdir -p $T/proc/vm;echo ${SYSCTL_LIVE:-200} >$T/proc/vm/vfs_cache_pressure;( cd $T/f/s&&PATH=$B:$PATH AGI_MOVE_SSH=$T/sshconf AGI_MOVE_EXCLUDE_NODE=${1:-$T/node.md} sh $SRC move $P >$T/out 2>$T/err );rc=$?; }
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
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\ngit for-each-ref --format="%%(refname)" refs/archive/|while read -r r;do git update-ref -d $r;done\n' >$T/f/w/.git/hooks/post-receive;chmod +x $T/f/w/.git/hooks/post-receive;go
ok "refs-short-namespace-refuses a target that ends with 0 of the 2 refs/archive/* refs ends rc != 0 (rc $rc), not 0" '[ $rc != 0 ]'
ok "refs-short-namespace-is-named stderr names '[refs-short] refs/archive before=2 after=0' ($(head -c 160 $T/err|tr '\n' ' '))" 'grep -q "^\[refs-short\] refs/archive before=2 after=0" $T/err'
ok "refs-short-namespace-never-starts-the-post agi-post@$P is NOT started on the target (ctl: $(tr '\n' '|' <$T/ctl.log))" '! started'
ok "refs-short-namespace-names-only-the-short-one refs/grid (not short) is not named in a [refs-short] line" '! grep -q "^\[refs-short\] refs/grid" $T/err'
# an EXCLUDED namespace that comes up short is not a refusal
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\ngit for-each-ref --format="%%(refname)" refs/remotes/|while read -r r;do git update-ref -d $r;done\n' >$T/f/w/.git/hooks/post-receive;chmod +x $T/f/w/.git/hooks/post-receive;go
ok "refs-an-excluded-namespace-may-be-short a target with 0 refs/remotes/* (excluded) still ends rc 0 and starts the post (rc $rc; started: $(started&&echo yes||echo no))" '[ $rc = 0 ]&&started'

# round 2 (e)-2: counts can hide a missing NAME (refs/heads gets carry/trunk on the target, so 5 >= 4 even with refs/heads/other gone)
fix;mkdir -p $T/f/w/.git/hooks;printf '#!/bin/sh\ngit update-ref -d refs/heads/other\n' >$T/f/w/.git/hooks/post-receive;chmod +x $T/f/w/.git/hooks/post-receive;go
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
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/remotes  a copy of origin\n```\n' >$T/node-noopt.md;fix;go $T/node-noopt.md
ok "refs-unit-paths-the-exemptions-are-the-cells-and-nothing-else with NO move.unit-optional block the target's home paths ($T/hm/p1) are not exempt: rc $rc (want 7), '[unit-path] ... WorkingDirectory $T/hm/p1 missing' ($(grep -c 'WorkingDirectory '$T'/hm/p1 missing' $T/err) line)" '[ $rc = 7 ]&&grep -q -F "WorkingDirectory $T/hm/p1 missing" $T/err'

# goal:g7.16.1.11.40.1.1 target 3a (DG1's guard/sysctl-check.sh) as an AFTER-check: the TARGET's /etc/sysctl.d/60-agi-vm.conf must be there and live. The SOURCE's stays good (a check that runs on the source passes wrongly).
fix;go
ok "refs-sysctl-check-good-target-completes the target has 60-agi-vm.conf and the kernel agrees: rc $rc (want 0), the post started ($(started&&echo yes||echo no)), stdout carries the check's 'ok vm.vfs_cache_pressure' ($(grep -c '^ok vm.vfs_cache_pressure' $T/out) line)" '[ $rc = 0 ]&&started&&grep -q "^ok vm.vfs_cache_pressure" $T/out'
fix;rm -f $T/sysd-t/60-agi-vm.conf;go
ok "refs-sysctl-check-a-dropped-conf-refuses the target LOST 60-agi-vm.conf (a box move or a reinstall drops it): rc $rc (want 8), '[sysctl-check]' on stderr ($(grep -c '^\[sysctl-check\]' $T/err) line), 'RED sysctl' on stdout, and agi-post@$P is NOT started on the target (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc = 8 ]&&grep -q "^\[sysctl-check\]" $T/err&&grep -q "^RED sysctl" $T/out&&! started'
fix;SYSCTL_LIVE=100;export SYSCTL_LIVE;go;unset SYSCTL_LIVE
ok "refs-sysctl-check-a-file-the-kernel-does-not-hold-refuses the conf says 200 but the kernel has 100 (sysctl --system not run): rc $rc (want 8), the post is NOT started" '[ $rc = 8 ]&&! started'

# the cell is the ONLY list
sed 's#^refs/remotes .*#&\nrefs/agi  scratch bookkeeping the target rebuilds#' $T/node.md >$T/node-add.md;fix;go $T/node-add.md
ok "refs-the-cell-is-the-only-list-add an entry added to the cell (refs/agi) is NOT carried: target refs/agi/*: $(cnt $T/f/w agi) (want 0), printed 'excluded: scratch bookkeeping' ($(grep -c 'refs refs/agi excluded: scratch bookkeeping' $T/out)), rc $rc" '[ $rc = 0 ]&&[ $(cnt $T/f/w agi) = 0 ]&&grep -q "refs refs/agi excluded: scratch bookkeeping" $T/out'
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/agi  scratch bookkeeping the target rebuilds\n```\n' >$T/node-sw.md;sed -n '/^```sh move.unit-optional/,/^```$/p' $T/node.md >>$T/node-sw.md;fix;go $T/node-sw.md
ok "refs-the-cell-is-the-only-list-remove refs/remotes taken OUT of the cell is carried: target refs/remotes/*: $(cnt $T/f/w remotes) (want >= 1), rc $rc" '[ $rc = 0 ]&&[ $(cnt $T/f/w remotes) -ge 1 ]'
# no cell, no move
fix;go $T/nonexistent.md;pre=$(git -C $T/f/o for-each-ref|wc -l|tr -d ' ')
ok "refs-no-cell-no-move a missing exclude node ends rc != 0 ($rc), says [refs-exclude] ($(head -c 100 $T/err|tr '\n' ' ')), never stops the post (ctl: $(tr '\n' '|' <$T/ctl.log)), pushes nothing (origin refs $pre, target archive $(cnt $T/f/w archive))" '[ $rc != 0 ]&&grep -q "^\[refs-exclude\]" $T/err&&! grep -q "^stop" $T/ctl.log&&[ $pre = 0 ]&&[ $(cnt $T/f/w archive) = 0 ]'
printf '# config:guard (fixture)\n```sh move.exclude\n```\n' >$T/node-empty.md;fix;go $T/node-empty.md
ok "refs-an-empty-cell-is-no-cell an exclude block with no entry ends rc != 0 ($rc) before the post is stopped (ctl: $(tr '\n' '|' <$T/ctl.log))" '[ $rc != 0 ]&&! grep -q "^stop" $T/ctl.log'

# the tree under test
n=$(grep -c -F '$E "cd /data/work/agi' $SRC)
ok "refs-the-host-act-line-stays-one $SRC holds $n line(s) with \$E \"cd /data/work/agi (want 1: box-move.t.sh extracts it)" '[ $n = 1 ]'
G=$R0/.agi/nodes/.geometry/guard.md;ent=$(sed -n '/^```sh move.exclude/,/^```$/p' $G 2>/dev/null|grep -E '^refs/[a-z0-9_-]+  *[^ ]');ne=$(echo "$ent"|grep -c .)
bad=$([ -n "$ent" ]&&echo "$ent"|awk '{n=$1;sub(/^[^ ]+ +/,"");if(length($0)<8)print n" (reason too short)"; if(n~/^refs\/(heads|grid|box|held|archive|agi)$/)print n" (must be carried)"}'|tr '\n' ' ')
ok "refs-the-real-cell-exists-and-excludes-nothing-that-must-move $G holds the move.exclude block with $ne entr(ies) (want >= 1), each with a reason of >= 8 chars, none of heads/grid/box/held/archive/agi: [${bad% }]" '[ $ne -ge 1 ]&&[ -z "$bad" ]'
uo=$(sed -n '/^```sh move.unit-optional/,/^```$/p' $G 2>/dev/null|grep -E '^(Exec[A-Za-z]*|WorkingDirectory|EnvironmentFile|ReadWritePaths|ReadOnlyPaths)  *[^ ]');nu=$(echo "$uo"|grep -c .)
ub=$(echo "$uo"|awk '{k=$1;p=$2;sub(/^[^ ]+ +[^ ]+ +/,"");if(length($0)<8)print k" "p" (reason too short)"; if(k ~ /^Exec/)print k" "p" (a command is never exempt)"; if(p ~ /signers|repoint|sbin|opt\/agi/)print k" "p" (a host tool is never exempt)"}'|tr '\n' ' ')
ok "refs-the-real-unit-optional-cell-exists-and-exempts-no-command $G holds the move.unit-optional block with $nu entr(ies) (want >= 1), each with a reason of >= 8 chars, none an Exec* key and none naming the signers / a host tool: [${ub% }]" '[ $nu -ge 1 ]&&[ -z "$ub" ]'
echo "box-move-refs: $f FAIL";exit $f
