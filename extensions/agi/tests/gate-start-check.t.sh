#!/bin/sh
# gate-start-check.t.sh [ROOT]: own57 item 4 (council 3/3 = alive [decision] 19:28:39Z 10-27): skills/agi-master-gate/start-check.sh, the gate START CHECK.
# Rows: the encryption-town floor 3072 and the 6144 elsewhere, keyed on AGI_BOX; AGI_BOX unset -> 6144 + 'AGI_BOX unread', never 3072; a PSI file absent or
# MemAvailable unreadable -> rc 4 named, never a start; a PSI file whose `some` is over the bar and whose `full` is 0 -> REFUSED; ONE reading line per run.
# Mutants (each a one-token edit on a copy; '# NO EDIT' = an inert mutant, a FAIL): unset AGI_BOX falls to 3072; an empty PSI reading defaults to 0; PSI read
# from `full`. Each must read RED on its row. Fixtures only, no /proc, no git, 0 USD. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};S=$R0/skills/agi-master-gate/start-check.sh;D=$(mktemp -d);trap 'rm -rf $D' 0;f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -f $S ]||{ echo "FAIL inputs: no start-check.sh under $R0";exit 99;}
mi(){ printf 'MemTotal:       16000000 kB\nMemAvailable:   %s kB\n' $1 >$D/mi.$1;echo $D/mi.$1;}
psi(){ printf 'some avg10=%s avg60=%s avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' $1 $2 >$D/p.$1.$2;echo $D/p.$1.$2;}
M45=$(mi 4608000);M29=$(mi 3000000);M70=$(mi 7168000);P0=$(psi 0.00 0.00)
# run SCRIPT BOX MEMINFO PSIMEM PSIIO -> "rc <n>|<stdout>" (BOX '-' = unset)
run(){ o=$(if [ "$2" = - ];then env -u AGI_BOX START_MEMINFO=$3 START_PSI_MEM=$4 START_PSI_IO=$5 sh $1;else env AGI_BOX=$2 START_MEMINFO=$3 START_PSI_MEM=$4 START_PSI_IO=$5 sh $1;fi 2>&1);echo "rc $?|$o";}
a=$(run $S encryption-town $M45 $P0 $P0);ok "et-pass encryption-town, 4500 MiB, PSI 0: starts on floor 3072 from AGI_BOX (got: $a)" 'case "$a" in "rc 0|start check: floor 3072 from AGI_BOX=encryption-town; MemAvailable 4500 MiB;"*) true;; *) false;; esac'
b=$(run $S encryption-town $M29 $P0 $P0);ok "et-below 2929 MiB under the 3072 floor: REFUSED rc 3 (got: $b)" 'case "$b" in "rc 3|"*BELOW*) true;; *) false;; esac'
c=$(run $S - $M45 $P0 $P0);ok "box-unset AGI_BOX unset: floor 6144 named 'AGI_BOX unread', 4500 MiB REFUSED, never 3072 (got: $c)" 'case "$c" in "rc 3|start check: floor 6144 from AGI_BOX unread;"*) true;; *) false;; esac'
d=$(run $S other-town $M70 $P0 $P0);ok "box-other another box: floor 6144 from its AGI_BOX, 7000 MiB starts (got: $d)" 'case "$d" in "rc 0|start check: floor 6144 from AGI_BOX=other-town"*) true;; *) false;; esac'
e=$(run $S encryption-town $M45 $P0 $D/absent);ok "psi-absent the io PSI file absent: rc 4, named UNREAD with its path, never a start (got: $e)" 'case "$e" in "rc 4|"*"io PSI some avg60 UNREAD"*"UNREAD: "*"io PSI from $D/absent"*) true;; *) false;; esac'
g=$(run $S encryption-town $D/absent $P0 $P0);ok "meminfo-unreadable MemAvailable unreadable: rc 4 named (got: $g)" 'case "$g" in "rc 4|"*"MemAvailable from $D/absent"*) true;; *) false;; esac'
PMS=$(psi 7.00 0.00);h=$(run $S encryption-town $M45 $PMS $P0);ok "mem-some-over memory PSI some avg10 7, full 0: REFUSED rc 3 (got: $h)" 'case "$h" in "rc 3|"*"memory PSI some avg10 7.00"*BELOW*) true;; *) false;; esac'
PIS=$(psi 0.00 60.00);i=$(run $S encryption-town $M45 $P0 $PIS);ok "io-some-over io PSI some avg60 60, full 0: REFUSED rc 3 (got: $i)" 'case "$i" in "rc 3|"*"io PSI some avg60 60.00"*BELOW*) true;; *) false;; esac'
n=$(env AGI_BOX=encryption-town START_MEMINFO=$M45 START_PSI_MEM=$P0 START_PSI_IO=$P0 sh $S|grep -c '^start check: ');ok "one-reading-line exactly ONE reading line per run (got: $n)" '[ "$n" = 1 ]'
# mutants: copy, one-token edit, the edit must apply (else NO EDIT = FAIL), the row must read RED
mut(){ sed "$2" $S >$D/m.$1.sh;if cmp -s $S $D/m.$1.sh;then echo "# NO EDIT for [$1]";return 1;fi;echo $D/m.$1.sh;}
if m=$(mut unset-3072 's/"") FL=6144/"") FL=3072/');then x=$(run $m - $M45 $P0 $P0);ok "m-unset-3072-RED the unset box falling to 3072 starts at 4500 MiB: box-unset catches it (got: $x)" '! case "$x" in "rc 3|start check: floor 6144 from AGI_BOX unread;"*) true;; *) false;; esac';else echo "$m";echo "FAIL m-unset-3072 inert";f=$((f+1));fi
if m=$(mut psi-default-0 's/^PI=\$(\(.*\))$/PI=$(\1); PI=${PI:-0}/');then x=$(run $m encryption-town $M45 $P0 $D/absent);ok "m-psi-default-0-RED an absent io PSI read as 0 starts: psi-absent catches it (got: $x)" '! case "$x" in "rc 4|"*) true;; *) false;; esac';else echo "$m";echo "FAIL m-psi-default-0 inert";f=$((f+1));fi
if m=$(mut full 's/^PM=$(sed -n .s\/^some /PM=$(sed -n '"'"'s\/^full /');then x=$(run $m encryption-town $M45 $PMS $P0);ok "m-full-RED memory PSI read from full (0) starts over some 7: mem-some-over catches it (got: $x)" '! case "$x" in "rc 3|"*) true;; *) false;; esac';else echo "$m";echo "FAIL m-full inert";f=$((f+1));fi
echo "gate-start-check.t.sh: $f FAIL";exit $f
