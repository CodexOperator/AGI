#!/bin/sh
# box-move-refs.t.sh: goal:g7.16.1.11.39 (council 0a8aa43672 remark 3 + 5a6f6ce9a6; DG2): a box move carries EVERY ref namespace except a NAMED exclude list, counts each namespace before and after, REFUSES when a carried namespace comes up short, and routes the box-local namespaces box-to-box only, never through origin. sh + git, scratch repos only, no network, no root, no sudo, 0 USD.
# It runs the REAL `sh guard/box-move.sh move p1` (SRC = ROOT's, a mutation = SRC=<edited copy>) in a scratch SOURCE repo with refs in many namespaces (heads/posts/other branches, grid, box, held, archive 2 deep, agi, tags, remotes, and `refs/novel/q/r` that NO script names), against a scratch ORIGIN (bare) and a scratch TARGET (a clone, reached through an ssh STUB that runs the remote command locally with /data/work/agi remapped), with stubs for sudo + systemctl (the box-move.t.sh ones). The post under test is p1.
# THE CONTRACT (the builder cuts to it):
#   exclude cell = the fenced block opened by the line ```` ```sh move.exclude ```` in the config:guard node (.agi/nodes/.geometry/guard.md), closed by a bare fence; one entry per line, `refs/<namespace>  <reason>` (namespace = the first two path parts; the reason is free text, one per entry). AGI_MOVE_EXCLUDE_NODE=<path> points the carrier at another copy of that node (guard-init.sh's GUARD_ENV_NODE precedent). The list lives ONLY there: the script holds no namespace names.
#   no cell found (node missing, or the block empty) = rc != 0 BEFORE anything is done ([refs-exclude], the post is not stopped, nothing is pushed).
#   `move` pushes every namespace of the source that is not excluded to the TARGET (never the target's checked-out trunk branch by name: that one goes through carry/trunk + ff, as now), and prints, to stdout, one line per carried namespace `refs <ns> before=<n> after=<m>` (n = the SOURCE count before the first push, m = the TARGET count after the last) and one `refs <ns> excluded: <reason>` per excluded entry.
#   a carried namespace with m < n = `[refs-short] <ns> before=<n> after=<m>` on stderr, rc != 0, and the post is NOT started on the target (the ff + host-act line is never reached). An excluded namespace may come up short without a refusal.
#   origin (public) gets exactly what it gets today: HEAD to refs/heads/local-maxxing/season2/main, no other ref.
#   box-move.t.sh stays green: the file keeps exactly ONE line holding `$E "cd /data/work/agi`.
# One ok/FAIL line per case; exit = number of FAILs.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};SRC=${SRC:-$R0/extensions/agi/guard/box-move.sh}
SRC=$(cd "$(dirname "$SRC")"&&pwd)/$(basename "$SRC")
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
P=p1;B=$T/bin;mkdir -p $B;TGT=$T/f/w;export TGT
printf '#!/bin/sh\nwhile [ "$1" = -n ];do shift;done\ncase "$1 $2 $3" in "test -f "*/h.conf)exit 1;;esac\nexec "$@"\n' >$B/sudo
printf '#!/bin/sh\necho "$*" >>%s/ctl.log\ncase "$1" in is-active)exit 1;; show)echo "running 0";; esac\nexit 0\n' $T >$B/systemctl
printf '#!/bin/sh\nwhile :;do case "$1" in -F|-o)shift 2;; -*)shift;; *)break;;esac;done\nshift\nexec sh -c "$(printf %%s "$*"|sed "s#/data/work/agi#$TGT#g")"\n' >$B/ssh
chmod +x $B/*;: >$T/sshconf
cat >$T/node.md <<'XX'
# config:guard (fixture)
```sh move.exclude
refs/remotes  a remote-tracking ref is a copy of origin's; the target fetches its own
```
XX
# fix: a fresh source (s) + origin (o, bare) + target (w, a clone of s before the move) in $T/f; the source's refs are listed in $T/f/pre (name sha) before the run
fix(){ rm -rf $T/f;mkdir -p $T/f;: >$T/ctl.log;cd $T/f;git init -q -b local-maxxing/season2/main s;git init -q --bare o
 ( cd s;mkdir -p .agi/nodes/.geometry extensions/agi/guard
  printf '%s\n' '  - {"name": "p1", "engine": {"v": 4}, "box": "local-town"}' '  - {"name": "p2", "engine": {"v": 4}, "box": "local-town"}' >.agi/nodes/.geometry/posts.md
  printf 'echo act\nexit 0\n' >extensions/agi/guard/host-act-encryption-town.sh;git add .;git commit -q -m base;git remote add origin $T/f/o )
 git clone -q s w;git -C w remote remove origin
 ( cd s;t=$(git rev-parse HEAD^{tree});for r in heads/posts/p1 heads/dg4-x heads/other grid/n1/1 grid/n2/1 box/a/b/1 box/a/b/2 held/a/b/1 archive/p1/dir1 archive/p2/dir2 agi/x tags/v1 novel/q/r remotes/origin/main;do git update-ref refs/$r $(git commit-tree -m $r $t);done )
 git -C s for-each-ref --format='%(refname) %(objectname)' >$T/f/pre; }
# go NODE: run the move in the source; sets rc, $T/out, $T/err
go(){ ( cd $T/f/s&&PATH=$B:$PATH AGI_MOVE_SSH=$T/sshconf AGI_MOVE_EXCLUDE_NODE=${1:-$T/node.md} sh $SRC move $P >$T/out 2>$T/err );rc=$?; }
# cnt REPO NS: how many refs of REPO sit under refs/<NS>/
cnt(){ git -C $1 for-each-ref --format='%(refname)' refs/$2/|wc -l|tr -d ' '; }
started(){ grep -q "^start agi-post@$P" $T/ctl.log; }
line(){ grep -F '$E "cd /data/work/agi' "$SRC";}
[ -s $SRC ]||{ echo "FAIL extract: no $SRC";exit 99;}

fix;go;ns="heads grid box held archive agi tags novel";nd="";for n in $ns;do a=$(cnt $T/f/w $n);b=$(cnt $T/f/s $n);[ $n = heads ]&&b=$(git -C $T/f/s for-each-ref --format='%(refname)' refs/heads/|grep -c -v carry/trunk);[ "$a" -ge "$b" ]||nd="$nd $n($a/$b)";done
miss=$(while read -r r s;do case $r in refs/remotes/*|refs/heads/local-maxxing/season2/main)continue;; esac;[ "$(git -C $T/f/w rev-parse -q --verify $r 2>/dev/null)" = "$s" ]||echo $r;done <$T/f/pre|tr '\n' ' ')
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

# the cell is the ONLY list
sed 's#^refs/remotes .*#&\nrefs/agi  scratch bookkeeping the target rebuilds#' $T/node.md >$T/node-add.md;fix;go $T/node-add.md
ok "refs-the-cell-is-the-only-list-add an entry added to the cell (refs/agi) is NOT carried: target refs/agi/*: $(cnt $T/f/w agi) (want 0), printed 'excluded: scratch bookkeeping' ($(grep -c 'refs refs/agi excluded: scratch bookkeeping' $T/out)), rc $rc" '[ $rc = 0 ]&&[ $(cnt $T/f/w agi) = 0 ]&&grep -q "refs refs/agi excluded: scratch bookkeeping" $T/out'
printf '# config:guard (fixture)\n```sh move.exclude\nrefs/agi  scratch bookkeeping the target rebuilds\n```\n' >$T/node-sw.md;fix;go $T/node-sw.md
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
echo "box-move-refs: $f FAIL";exit $f
