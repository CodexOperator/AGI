#!/bin/sh
# sysctl-check.sh -- goal:g7.16.1.11.40.1.1 target 3a (ii): the vm.vfs_cache_pressure stopgap lives in /etc/sysctl.d as BYTES (the boxkit row
# agi-vm-sysctl), and this check proves it on the box: the file is THERE (a box move or a reinstall that drops it is rc 1, not silence), every
# `key = value` in it equals the LIVE kernel value (sysctl -n), and, when EXPECTED names the rendered bytes, the file equals them.
# Run by the box owner after the install + `sysctl --system`, and again after any box move. Read-only: it changes nothing.
# Env (defaults are the box's): SYSCTL_D SYSCTL_FILE PROC_SYS EXPECTED.
D=${SYSCTL_D:-/etc/sysctl.d};F=${SYSCTL_FILE:-60-agi-vm.conf};PROC_SYS=${PROC_SYS:-/proc/sys};EXPECTED=${EXPECTED:-};rc=0
[ -r "$D/$F" ] || { echo "RED sysctl: $D/$F is missing or unreadable (installed by the box owner; a box move or a reinstall drops it)";exit 1;}
if [ -n "$EXPECTED" ];then cmp -s "$EXPECTED" "$D/$F" && echo "ok bytes: $D/$F equals the rendered row" || { echo "RED bytes: $D/$F differs from $EXPECTED";rc=1;};else echo "bytes: not checked (EXPECTED unset)";fi
tmp=$(mktemp) || exit 2;trap 'rm -f "$tmp"' EXIT
awk '/^[ \t]*(#|$)/{next} {i=index($0,"="); if(!i)next; k=substr($0,1,i-1); v=substr($0,i+1); gsub(/^[ \t]+|[ \t]+$/,"",k); gsub(/^[ \t]+|[ \t]+$/,"",v); print k "\t" v}' "$D/$F" >"$tmp"
[ -s "$tmp" ] || { echo "RED sysctl: $D/$F sets nothing";exit 1;}
while IFS="	" read -r key want;do
 live=$(cat "$PROC_SYS/$(printf %s "$key"|tr . /)" 2>/dev/null|tr -s ' \t' '  '|sed 's/^ //;s/ $//')
 if [ "$live" = "$want" ];then echo "ok $key = $want (live)";else echo "RED $key: $D/$F says '$want', the kernel has '${live:-<unreadable>}' (sysctl --system not run, or overridden later)";rc=1;fi
done <"$tmp"
exit $rc
