#!/bin/sh
# box-move.sh: move ONE v5 post from this box to another, and relay its first-run login (belam, 10-08: the local-town -> encryption-town
# move, proved on 10 posts; owner 23:3xZ: "add the box move script to the graph directly"). Runs on the SOURCE box, from MAIN, as the Prime.
#   sh box-move.sh move POST                 flip the row's box (one cell) · stop on this box (agi-flush lands the last turn) · trunk to origin
#                                            + the target · the post's branches to the target (no force) · ff + host-act move on the target
#   printf %s CODE | sh box-move.sh login POST   the code on STDIN, never argv: type it into the post's fifo, step Enter / Security notes,
#                                            answer the workspace-trust prompt Yes (Down + Enter), stop on anything unknown
#   sh box-move.sh url POST                  step the theme / login-method screens and print the login URL for the owner
# Cells (env): AGI_MOVE_TO (default encryption-town) · AGI_MOVE_FROM (default local-town) · AGI_MOVE_SSH (the ssh config holding the target
# host; default the sanctuary mesh config) · AGI_MOVE_EXTRA (more branch globs for the post, e.g. 'dg4-*').
# Requires on the target (the gaps the pilot found, G1-G3): the host act (host-act-<box>.sh act) · group agi + user belam ACLs on
# MAIN .git/{objects,refs,logs,worktrees} and .agi/sessions/inbox, mirrored from the source · AGI_BOX=<target> in any shell there running send.py.
P=$2;TO=${AGI_MOVE_TO:-encryption-town};FROM=${AGI_MOVE_FROM:-local-town}
case $P in ""|*[!a-z0-9-]*)echo "usage: move|login|url POST">&2;exit 1;;esac
C=${AGI_MOVE_SSH:-$(ls -d /home/*/work/.sanctuary/ssh/config 2>/dev/null|head -1)};[ -f "$C" ]||{ echo "no ssh config (AGI_MOVE_SSH)">&2;exit 1;}
E="ssh -F $C -o BatchMode=yes $TO"
SCR='f=/var/lib/agi/'$P'/o;k(){ sudo -n sh -c "printf \"$1\" > /run/agi-'$P'/i";};scr(){ sudo -n tail -c ${1:-4000} $f|tr -d "\r\n"|sed -E "s/\x1b\[[0-9;?]*[a-zA-Z]//g;s/\x1b\][^\a]*\a//g;s/\x1b[()][0-9A-Za-z]//g";}'
case $1 in
move)
set -e;cd "$(git rev-parse --show-toplevel)";[ "$(git branch --show-current)" = local-maxxing/season2/main ];git diff --quiet -- .agi/nodes/.geometry/posts.md
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
x=;for g in $AGI_MOVE_EXTRA;do x="$x refs/heads/$g:refs/heads/$g";done
GIT_SSH_COMMAND="ssh -F $C -o BatchMode=yes" git push -q ssh://$TO/data/work/agi "$(git rev-parse HEAD):refs/heads/carry/trunk" "refs/heads/posts/$P:refs/heads/posts/$P" $x
echo "trunk $(git rev-parse --short HEAD) · posts/$P $(git rev-parse --short posts/$P)"
$E "cd /data/work/agi&&git merge -q --ff-only carry/trunk&&sudo -n env PIN=\$(git rev-parse HEAD) sh extensions/agi/guard/host-act-$TO.sh move $P 2>&1|tail -2;sudo -n test -f /run/systemd/system/agi-post@$P.service.d/h.conf&&sudo -n systemctl enable --now agi-carry@$P.path&&sudo -n systemctl reset-failed agi-post@$P 2>/dev/null;sudo -n systemctl is-active -q agi-post@$P||sudo -n systemctl start agi-post@$P;systemctl show agi-post@$P -p SubState -p NRestarts --value|tr '\n' ' '";;
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
