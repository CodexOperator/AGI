#!/bin/sh
# target-fit.sh: goal:g7.16.1.11.39.3 -- run ON THE TARGET, in the SAME ssh as unit-paths.sh (box-move.sh streams this file first, then unit-paths.sh, into one `sh -s`), BEFORE the stop and the row edit. a dry-run push never runs the target's receive-pack, so a full disk or a refs dir the pushing uid cannot write would surface only after the stop (rc 4). Two reads of the target, nothing else: (1) the free space under TF_REPO (df -Pk, the filesystem the carry lands on) must be >= TF_MIN_KB (the `sh move.target-fit` cell of config:guard); (2) a probe file can be created AND removed in TF_REPO/.git/refs/heads as the pushing uid. Either failing = `[target-unfit] <box> df|refs-write <reading>` on stderr and rc 9 (stream ends: unit-paths.sh never runs); both fine = falls through. NOT caught, by design: a pre-receive hook's verdict (only a real push runs it) and a target ref that advances between the dry run and the push.
B=${AGI_BOX:-$(hostname -s)};R=${TF_REPO:?};M=${TF_MIN_KB:?};u=0
free=$(df -Pk "$R" 2>/dev/null|awk 'NR==2{print $4}')
case $free in ''|*[!0-9]*)echo "[target-unfit] $B df unreadable: df -Pk $R gave '$free'">&2;u=1;;*)[ "$free" -ge "$M" ]||{ echo "[target-unfit] $B df $free KB free under $R, the floor is $M KB">&2;u=1;};;esac
p=$R/.git/refs/heads/.unfit-probe.$$
if ( : >"$p" ) 2>/dev/null;then rm -f "$p" 2>/dev/null&&[ ! -e "$p" ]||{ echo "[target-unfit] $B refs-write probe $p was created but could not be removed">&2;u=1;};else echo "[target-unfit] $B refs-write cannot create a file in $R/.git/refs/heads as $(id -un)">&2;u=1;fi
[ $u = 0 ]||exit 9
