#!/bin/sh
# unit-paths.sh POST [Key=path ...]: goal:g7.16.1.11.39.1 -- run ON THE TARGET box (box-move.sh feeds it through `ssh ... sh -s`, before it stops the post or edits the row): read the units as RENDERED there (`systemctl cat agi-post@POST`, agi-boxwake@POST and agi-carry@POST (goal:g7.16.1.11.39.2: its ExecStart is the absolute box-carry word, no new key), the template + every drop-in, %i = POST) and check that every host path they name EXISTS: the command word of each Exec* line (after the prefix characters - @ + ! :, and past `env` options and VAR=val words), WorkingDirectory, EnvironmentFile, ReadWritePaths, ReadOnlyPaths. A leading `-` is NOT a pass: it tells systemd it may skip a missing path, not that a move may. A missing path = `[unit-path] <unit> <Key> <path> missing on <box>` on stderr and rc 7; agi-post@POST not readable = `[unit-path] ... unreadable`, rc 7 (agi-boxwake@ is a claude post's and agi-carry@ a held post's, so their absence is not an error). Each `Key=path` after POST is a NAMED exemption (the `sh move.unit-optional` cell of config:guard, one reason each): a path that host-act creates AFTER this check or that a post may lack. Read only: nothing is created. Not checked, by design: a word that is not an absolute path (systemd looks it up in PATH), one holding $ or a specifier other than %i %I %t %%, and /run /proc /dev /sys (made by systemd or the kernel).
P=$1;shift;B=${AGI_BOX:-$(hostname -s)};bad=0;L=
for u in agi-post@$P agi-boxwake@$P agi-carry@$P;do
 t=$(systemctl cat $u.service 2>/dev/null)&&[ -n "$t" ]||{ case $u in agi-post@*)echo "[unit-path] $u.service unreadable on $B: systemctl cat failed">&2;bad=1;;esac;continue;}
 L="$L$(printf '%s\n' "$t"|awk -v U=$u.service -v P="$P" '
 function strip(s){ while(s ~ /^[-@+!:]/) s=substr(s,2); return s }
 function sub_(s){ gsub(/%i|%I/,P,s); gsub(/%t/,"/run",s); gsub(/%%/,"%",s); return s }
 function emit(k,w){ w=sub_(w); if(w !~ /^\// || w ~ /[$%*]/ || w ~ /^\/(run|proc|dev|sys)(\/|$)/) return; print U, k, w }
 /^[A-Za-z]+=/ { k=$0; sub(/=.*/,"",k); v=substr($0,length(k)+2)
   if(k ~ /^Exec/){ n=split(v,a," "); w=strip(a[1]); emit(k,w); if(w ~ /(^|\/)env$/){ for(i=2;i<=n;i++){ if(a[i] ~ /^-/ || a[i] ~ /=/) continue; emit(k,a[i]); break } } }
   else if(k=="WorkingDirectory"||k=="EnvironmentFile") emit(k,strip(v))
   else if(k=="ReadWritePaths"||k=="ReadOnlyPaths"){ n=split(v,a," "); for(i=1;i<=n;i++) emit(k,strip(a[i])) } }')
"
done
M=$(printf '%s\n' "$L"|while read -r u k w;do [ -n "$w" ]||continue;[ -e "$w" ]&&continue;ex=0;for e in "$@";do [ "$(echo "$e"|sed "s/%i/$P/g")" = "$k=$w" ]&&ex=1;done;[ $ex = 1 ]||echo "[unit-path] $u $k $w missing on $B";done)
[ -z "$M" ]||{ echo "$M">&2;bad=1;}
[ $bad = 0 ]||exit 7
