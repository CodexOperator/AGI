#!/bin/sh
# start-check.sh: the gate START CHECK (own57 item 4; council 3/3 = alive [decision] 19:28:39Z 10-27, on belam's 19:2xZ floor).
# Run it in the command that starts a suite: `sh skills/agi-master-gate/start-check.sh >> $O/summary || exit 3`.
# Floor: MemAvailable >= 3072 MiB on encryption-town, 6144 elsewhere, keyed on AGI_BOX (never the host name); memory PSI `some` avg10 < 5;
# io PSI `some` avg60 < 50 (`some`, never `full`: some >= full, the stricter bar). Prints ONE reading line every run (floor + its source +
# MemAvailable + both PSI values). A read of nothing names itself: AGI_BOX unset or unknown -> 6144 + its source named; MemAvailable or a PSI
# file unreadable -> rc 4 + a named line, never a start. rc 0 = start, 3 = below the check, 4 = a reading UNREAD.
# Fixtures (the lane gate-start-check.t.sh): START_MEMINFO, START_PSI_MEM, START_PSI_IO replace the /proc paths.
MI=${START_MEMINFO:-/proc/meminfo}; PMF=${START_PSI_MEM:-/proc/pressure/memory}; PIF=${START_PSI_IO:-/proc/pressure/io}
case "${AGI_BOX:-}" in encryption-town) FL=3072; SRC="AGI_BOX=encryption-town";; "") FL=6144; SRC="AGI_BOX unread";; *) FL=6144; SRC="AGI_BOX=$AGI_BOX (not encryption-town)";; esac
FREE=$(awk '/^MemAvailable:/{print int($2/1024)}' "$MI" 2>/dev/null)
PM=$(sed -n 's/^some avg10=\([0-9.]*\).*/\1/p' "$PMF" 2>/dev/null)
PI=$(sed -n 's/^some avg10=[0-9.]* avg60=\([0-9.]*\).*/\1/p' "$PIF" 2>/dev/null)
echo "start check: floor $FL from $SRC; MemAvailable ${FREE:-UNREAD} MiB; memory PSI some avg10 ${PM:-UNREAD}; io PSI some avg60 ${PI:-UNREAD}"
[ -n "$FREE" ] && [ -n "$PM" ] && [ -n "$PI" ] || { echo "UNREAD: a start reading is empty ($([ -n "$FREE" ] || printf 'MemAvailable from %s ' "$MI")$([ -n "$PM" ] || printf 'memory PSI from %s ' "$PMF")$([ -n "$PI" ] || printf 'io PSI from %s' "$PIF")), not started"; exit 4; }
[ "$FREE" -ge "$FL" ] && awk -v m="$PM" -v i="$PI" 'BEGIN{exit !(m < 5 && i < 50)}' || { echo "BELOW the start check, not started"; exit 3; }
exit 0
