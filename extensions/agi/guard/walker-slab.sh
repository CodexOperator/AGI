#!/bin/sh
# walker-slab.sh LABEL CMD [ARG...] -- goal:g7.16.1.11.40.1.1 target 3c: ONE row of the per-walker table. READ-ONLY and non-root: it runs CMD, and reads
# the cgroup's kernel slab (memory.stat) before, at its PEAK (polled every INTERVAL seconds while CMD runs) and after, with the box's dentry and inode
# counts and the wall time. A walker's slab delta is only readable from a COLD cache (a warm one adds ~nothing), so run it right after the box owner's
# `echo 2 > /proc/sys/vm/drop_caches`; the row says which it was by the dentry count before. It drops nothing and writes nothing but its one stdout row.
# Row (tab separated): label wall_s slab_before_mib slab_peak_mib slab_after_mib peak_delta_mib dentries_before dentries_after inodes_before inodes_after rc
# Env: CG (default /sys/fs/cgroup/agi.slice) INTERVAL (default 0.5) DENTRY (default /proc/sys/fs/dentry-state) INODE (default /proc/sys/fs/inode-nr).
CG=${CG:-/sys/fs/cgroup/agi.slice};INTERVAL=${INTERVAL:-0.5};DENTRY=${DENTRY:-/proc/sys/fs/dentry-state};INODE=${INODE:-/proc/sys/fs/inode-nr}
L=${1:?label};shift;[ $# -gt 0 ]||{ echo "usage: walker-slab.sh LABEL CMD [ARG...]" >&2;exit 2;}
slab(){ awk '$1=="slab"{printf "%d",$2/1048576}' "$CG/memory.stat" 2>/dev/null||echo 0;}
nd(){ awk '{print $1}' "$DENTRY" 2>/dev/null||echo 0;};ni(){ awk '{print $1}' "$INODE" 2>/dev/null||echo 0;}
pk=$(mktemp)||exit 2;trap 'rm -f "$pk"' EXIT
sb=$(slab);db=$(nd);ib=$(ni);echo "$sb" >"$pk";t0=$(date +%s.%N)
( while :;do s=$(slab);p=$(cat "$pk");[ "$s" -gt "$p" ]&&echo "$s" >"$pk";sleep "$INTERVAL";done ) &
w=$!
"$@" >/dev/null 2>&1;rc=$?
t1=$(date +%s.%N);kill "$w" 2>/dev/null;wait "$w" 2>/dev/null
sa=$(slab);p=$(cat "$pk");[ "$sa" -gt "$p" ]&&p=$sa
printf '%s\t%.1f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$L" "$(echo "$t1 - $t0"|bc 2>/dev/null||awk "BEGIN{print $t1-$t0}")" "$sb" "$p" "$sa" "$((p-sb))" "$db" "$(nd)" "$ib" "$(ni)" "$rc"
exit 0
