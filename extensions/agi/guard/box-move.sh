#!/bin/sh
# box-move.sh: move ONE v5 post from this box to another, and relay its first-run login (belam, 10-08: the local-town -> encryption-town
# move, proved on 10 posts; owner 23:3xZ: "add the box move script to the graph directly"). Runs on the SOURCE box, from MAIN, as the Prime.
#   sh box-move.sh move POST                 flip the row's box (one cell) · stop on this box (agi-flush lands the last turn) · trunk to origin
#                                            + the target · the post's branches to the target (no force) · ff + host-act move on the target
#   printf %s CODE | sh box-move.sh login POST   the code on STDIN, never argv: type it into the post's fifo, step Enter / Security notes,
#                                            answer the workspace-trust prompt Yes (Down + Enter), stop on anything unknown
#   sh box-move.sh url POST                  step the theme / login-method screens and print the login URL for the owner
# After the refs check, BEFORE the post starts, guard/sysctl-check.sh runs ON THE TARGET (ssh `sh -s`): its /etc/sysctl.d/60-agi-vm.conf must be there and live; else `[sysctl-check]`, rc 8, post not started (goal:g7.16.1.11.40.1.1 target 3a).
# BEFORE the stop, in the SAME ssh as unit-paths.sh, guard/target-fit.sh reads the target: free space under /data/work/agi >= the `sh move.target-fit` cell of config:guard, and a probe file can be created and removed in its .git/refs/heads; else `[target-unfit]`, rc 9, nothing touched (goal:g7.16.1.11.39.3; no cell = rc 5).
# Refs (goal:g7.16.1.11.39): `move` carries EVERY ref namespace (refs/<ns>/*, the first two path parts) to the target except those the exclude cell names (the fenced block `sh move.exclude` of config:guard, .agi/nodes/.geometry/guard.md; AGI_MOVE_EXCLUDE_NODE=<path> = another copy; no cell = rc 5 before the post is stopped), never a list of what to keep; it prints `refs <ns> before=<n> after=<m>` (source before, target after) per carried namespace and `refs <ns> excluded: <reason>` per entry, and a carried namespace with m < n, or with ANY source ref NAME absent on the target, = `[refs-short]`, rc 4, the post never started (the check is the set of ref NAMES; a ref present at another sha is a live writer's race, not refused). BEFORE the stop and the row edit the target's RENDERED units are read (extensions/agi/guard/unit-paths.sh through ssh, goal:g7.16.1.11.39.1: every host path they name must exist, a missing one = `[unit-path] <unit> <Key> <path> missing on <box>`, rc 7; the named exemptions are the `sh move.unit-optional` block of the same node) and a PREFLIGHT (the same refspecs pushed with --dry-run --porcelain): any `!` line = `[refs-reject] <ref>`, rc 6, nothing touched. Origin (public) still gets the trunk branch only: refs/archive, refs/box, refs/held and the grid go box-to-box.
# Cells (env): AGI_MOVE_TO (default encryption-town) · AGI_MOVE_FROM (default local-town) · AGI_MOVE_SSH (the ssh config holding the target
# host; default the sanctuary mesh config) · AGI_MOVE_EXTRA (more branch globs for the post, e.g. 'dg4-*').
# Requires on the target (the gaps the pilot found, G1-G5): the host act (host-act-<box>.sh act) carries ALL of them: group agi + user belam
# ACLs (+ defaults) on MAIN .git/{objects,refs,logs,worktrees} (G2) and .agi/comms (G4, recursive), group agi (+ default) on .agi/sessions
# (G5: grid.py commit --all needs sessions/.grid.lock) and .agi/sessions/inbox (G3) · AGI_BOX=<target> in any shell there running send.py.
P=$2;TO=${AGI_MOVE_TO:-encryption-town};FROM=${AGI_MOVE_FROM:-local-town}
case $P in ""|*[!a-z0-9-]*)echo "usage: move|login|url POST">&2;exit 1;;esac
C=${AGI_MOVE_SSH:-$(ls -d /home/*/work/.sanctuary/ssh/config 2>/dev/null|head -1)};[ -f "$C" ]||{ echo "no ssh config (AGI_MOVE_SSH)">&2;exit 1;}
E="ssh -F $C -o BatchMode=yes $TO"
N=${AGI_MOVE_EXCLUDE_NODE:-$(git rev-parse --show-toplevel 2>/dev/null)/.agi/nodes/.geometry/guard.md}
cnt(){ echo "$1"|awk -F/ 'NF>=3{c[$1"/"$2]++} END{for(k in c)print k,c[k]}'|sort;}
SCR='f=/var/lib/agi/'$P'/o;k(){ sudo -n sh -c "printf \"$1\" > /run/agi-'$P'/i";};scr(){ sudo -n tail -c ${1:-4000} $f|tr -d "\r\n"|sed -E "s/\x1b\[[0-9;?]*[a-zA-Z]//g;s/\x1b\][^\a]*\a//g;s/\x1b[()][0-9A-Za-z]//g";}'
case $1 in
move)
set -e;X=$(sed -n '/^```sh move.exclude/,/^```$/p' "$N" 2>/dev/null|grep -E '^refs/[a-z0-9_-]+  *[^ ]'||true);[ -n "$X" ]||{ echo "[refs-exclude] no move.exclude cell in $N: nothing moved">&2;exit 5;}
NS=$(cnt "$(git for-each-ref --format='%(refname)')"|awk -v X="$X" 'BEGIN{n=split(X,xl,"\n");for(i=1;i<=n;i++){split(xl[i],t," ");e[t[1]]=1}} !($1 in e)')
SR=$(git for-each-ref --format='%(refname)'|awk -F/ -v X="$X" 'BEGIN{n=split(X,xl,"\n");for(i=1;i<=n;i++){split(xl[i],t," ");e[t[1]]=1}} NF>=3&&!(($1"/"$2) in e)&&$0!="refs/heads/local-maxxing/season2/main"')
RS=$(echo "$NS"|awk '{print $1"/*:"$1"/*"}')
x=;for g in $AGI_MOVE_EXTRA;do x="$x refs/heads/$g:refs/heads/$g";done
cd "$(git rev-parse --show-toplevel)";[ "$(git branch --show-current)" = local-maxxing/season2/main ];git diff --quiet -- .agi/nodes/.geometry/posts.md
UO=$(sed -n '/^```sh move.unit-optional/,/^```$/p' "$N" 2>/dev/null|grep -E '^(Exec[A-Za-z]*|WorkingDirectory|EnvironmentFile|ReadWritePaths|ReadOnlyPaths)  *[^ ]'|awk '{print $1"="$2}'|tr '\n' ' ')
FIT=$(sed -n '/^```sh move.target-fit/,/^```$/p' "$N" 2>/dev/null|awk '$1=="data-free-min-kb"{print $2}');case $FIT in ""|*[!0-9]*)echo "[target-unfit] no data-free-min-kb in the move.target-fit cell of $N: nothing moved">&2;exit 5;;esac
[ -s extensions/agi/guard/target-fit.sh ]||{ echo "[target-unfit] extensions/agi/guard/target-fit.sh is missing here: nothing moved">&2;exit 5;}
{ cat extensions/agi/guard/target-fit.sh extensions/agi/guard/unit-paths.sh|$E "AGI_BOX=$TO TF_REPO=/data/work/agi TF_MIN_KB=$FIT sh -s $P $UO";}||{ r=$?;[ $r != 9 ]||{ echo "[target-unfit] nothing touched: the post still runs on $FROM, the row is unmoved (rc 9)">&2;exit 9;};echo "[unit-path] nothing touched: the post still runs on $FROM, the row is unmoved (rc 7)">&2;exit 7;}
pf=$(GIT_SSH_COMMAND="ssh -F $C -o BatchMode=yes" git push --dry-run --porcelain ssh://$TO/data/work/agi "$(git rev-parse HEAD):refs/heads/carry/trunk" "refs/heads/posts/$P:refs/heads/posts/$P" $x $RS ^refs/heads/local-maxxing/season2/main 2>&1) && prc=0 || prc=$?
if [ $prc != 0 ] || echo "$pf"|grep -q '^!';then { echo "$pf"|sed -n 's/^!\t\([^\t]*\)\t/[refs-reject] \1 /p';echo "$pf"|grep -q '^!'||echo "[refs-reject] preflight failed (rc $prc): $(echo "$pf"|tail -1)"; echo "[refs-reject] nothing touched: the post still runs, the row is unmoved">&2; } >&2;exit 6;fi
python3 - "$P" "$FROM" "$TO" <<'PY'
import sys,json;P,F,T=sys.argv[1:];f='.agi/nodes/.geometry/posts.md';L=open(f).read().split('\n')
h=[i for i,l in enumerate(L) if l.startswith('  - {"name": "%s"'%P)];assert len(h)==1,h
o=json.loads(L[h[0]][4:]);assert o.get('engine',{}).get('v')==4 and o['box']==F,(o.get('engine'),o['box'])
n=dict(o);n['box']=T;L[h[0]]='  - '+json.dumps(n,ensure_ascii=False);open(f,'w').write('\n'.join(L))
PY
[ "$(git diff -U0 -- .agi/nodes/.geometry/posts.md|grep -c '^[-+] ')" = 2 ]
git add .agi/nodes/.geometry/posts.md;git commit -q -m "belam: posts row $P box $FROM -> $TO (box-move.sh; one cell)"
sudo -n systemctl stop agi-post@$P;echo "$FROM stop: $(systemctl show agi-post@$P -p Result --value)"
git push -q origin HEAD:local-maxxing/season2/main
GIT_SSH_COMMAND="ssh -F $C -o BatchMode=yes" git push -q ssh://$TO/data/work/agi "$(git rev-parse HEAD):refs/heads/carry/trunk" "refs/heads/posts/$P:refs/heads/posts/$P" $x
GIT_SSH_COMMAND="ssh -F $C -o BatchMode=yes" git push -q ssh://$TO/data/work/agi $RS ^refs/heads/local-maxxing/season2/main
AL=$($E "git -C /data/work/agi for-each-ref --format='%(refname)'")
A=$(cnt "$AL")
MS=$(echo "$SR"|awk -v A="$AL" 'BEGIN{n=split(A,a,"\n");for(i=1;i<=n;i++)h[a[i]]=1} NF&&!($0 in h)')
echo "$X"|awk '{n=$1;sub(/^[^ ]+ +/,"");print "refs " n " excluded: " $0}'
git for-each-ref --format='%(refname)'|awk -F/ -v X="$X" 'BEGIN{n=split(X,xl,"\n");for(i=1;i<=n;i++){split(xl[i],t," ");e[t[1]]=1}} NF==2&&!(($1"/"$2) in e){print "refs " $0 " skipped: a two-part ref cannot be pushed (git refuses a funny ref), so it stays on this box"}'
R=$(awk -v A="$A" -v B="$NS" -v M="$MS" 'BEGIN{n=split(M,ml,"\n");for(i=1;i<=n;i++){if(ml[i]=="")continue;split(ml[i],q,"/");k=q[1]"/"q[2];mc[k]++;if(!mf[k])mf[k]=ml[i]} n=split(A,al,"\n");for(i=1;i<=n;i++){split(al[i],t," ");a[t[1]]=t[2]+0} n=split(B,bl,"\n");for(i=1;i<=n;i++){split(bl[i],t," ");af=a[t[1]]+0;print "refs " t[1] " before=" t[2] " after=" af;if((af<t[2]||mc[t[1]])&&!s)s="[refs-short] " t[1] " before=" t[2] " after=" af (mc[t[1]]?" missing=" mc[t[1]] " first=" mf[t[1]]:"") ": move refused, post not started"} if(s)print s}')
echo "$R"|grep -v '^\[refs-short\]'
! echo "$R"|grep '^\[refs-short\]'>&2||:
echo "$R"|grep -q '^\[refs-short\]'&&exit 4
$E "sh -s" <extensions/agi/guard/sysctl-check.sh||{ echo "[sysctl-check] the target's /etc/sysctl.d/60-agi-vm.conf is missing or not live (guard/sysctl-check.sh, goal:g7.16.1.11.40.1.1): move refused, post not started" >&2;exit 8;}
echo "trunk $(git rev-parse --short HEAD) · posts/$P $(git rev-parse --short posts/$P)"
$E "cd /data/work/agi&&git merge -q --ff-only carry/trunk&&{ o=\$(mktemp);sudo -n env PIN=\$(git rev-parse HEAD) sh extensions/agi/guard/host-act-$TO.sh move $P >\$o 2>&1;r=\$?;tail -2 \$o;rm -f \$o;[ \$r = 0 ]||{ echo host-act move failed rc=\$r: post not started >&2;exit \$r;};}&&{ sudo -n test -f /run/systemd/system/agi-post@$P.service.d/h.conf&&sudo -n systemctl enable --now agi-carry@$P.path&&sudo -n systemctl reset-failed agi-post@$P 2>/dev/null;sudo -n systemctl is-active -q agi-post@$P||sudo -n systemctl start agi-post@$P;systemctl show agi-post@$P -p SubState -p NRestarts --value|tr '\n' ' ';}";;
url)
timeout 90 $E "$SCR"';sleep 6;for i in 1 2 3 4 5;do s=$(scr 600|tr -d " ");case "$s" in *OAutherror*|*"OAuth error"*)k "\r";sleep 6;;*Pastecode*|*"Paste code"*)break;;*Selectloginmethod*|*"Select login method"*|*Syntaxtheme*|*"Syntax theme"*|*"text style"*)k "\r";sleep 6;;*)sleep 4;;esac;done;scr|grep -o -E "https://claude\.com/cai/oauth/authorize[^ ]*"|tail -1|sed "s/Pastecodehereifprompted>.*//"';;
login)
timeout 30 $E "sudo -n sh -c 'cat > /run/agi-$P/i'"||{ echo "code write failed">&2;exit 1;}
timeout 150 $E "$SCR"';sleep 2;k "\r";sleep 8
for i in 1 2 3 4 5;do t=$(scr 1500|tr -d " ");case "$t" in
 *trustthisfolder*|*"trust this folder"*)echo "trust prompt -> Yes";k "\033[B";sleep 2;k "\r";sleep 12;break;;
 *Invalid*|*invalid*|*rror*)echo "STOP: $(echo "$t"|tail -c 160)";exit 2;;
 *PressEnter*|*"Press Enter"*|*Securitynotes*|*"Security notes"*)echo "step $i: enter";k "\r";sleep 7;;
 *)echo "step $i: unknown screen, stop";echo "$t"|tail -c 200;exit 3;;esac;done
echo "unit: $(systemctl show agi-post@'$P' -p SubState -p NRestarts --value|tr "\n" " ")";scr 600|grep -q -E "[✻✶✽✢]"&&echo "working (spinner)"||echo "no spinner yet"';;
*)echo "usage: move|login|url POST">&2;exit 1;;
esac
