#!/bin/sh
# f1-nspawn.sh: goal:g7.16.1.11.44.8 F1 -- "the same stop -> start in an nspawn container on this box with claude stubbed" (owner GO 10-22 19:34Z; council design 3/3 19:38:34Z + R1/R2 19:45:00Z).
#   sh f1-nspawn.sh run TRUNK_SHA ANSWERS_FILE [OUT_DIR]   HOST, ROOT. The ONLY root line (belam's host act, from a GATED sha). Builds the image once, boots ONE container, collects, tears down, prints the summary. rc 0 PASS, 1 FAIL, 2 INCONCLUSIVE.
#   sh f1-nspawn.sh inner                                  INSIDE the container (its own unit runs it). Refuses everywhere else (M1) before it touches anything.
#   F1_LIB=1 . f1-nspawn.sh                                the .t.sh sources the functions; nothing runs.
# What it proves: the property of agi-town-start.t.sh st2-RT2 (same active agi-post@ set, same crontab bytes, ONE "[town] up" line per post), read for REAL in the container (systemctl, crontab, refs/box), not from the fakes' logs; the 3 RT2 mutants
# each RED in the container; and, as its OWN line, whether the FIRST start brings up exactly the boot=true rows (R2). 0 USD: the image holds no claude binary, only the stub. Nothing here touches the live town: no bind of a live home, .env, key, ~/.claude or /data/work.
# Cells (env): F1_REPO (the live repo, /data/work/agi: read-only, fetched from) · F1_DATA (/data: rootfs + image live here) · F1_BOX (encryption-town) · F1_MIRROR · F1_TIMEOUT (seconds, whole run) · F1_CGROOT · F1_MEMINFO · F1_ROOT (a test prefix for the in-container paths).
F1_REPO=${F1_REPO:-/data/work/agi};F1_DATA=${F1_DATA:-/data};F1_BOX=${F1_BOX:-encryption-town};F1_ROOT=${F1_ROOT:-};F1_MAIN=${F1_MAIN:-/data/work/agi}
F1_MEM_MAX_M=1500;F1_TIMEOUT=${F1_TIMEOUT:-14400};F1_QTIMEOUT=${F1_QTIMEOUT:-60};F1_STEPTIMEOUT=${F1_STEPTIMEOUT:-3000}
F1_PKGS="systemd,systemd-sysv,dbus,libpam-systemd,sudo,cron,git,jq,acl,python3,python3-yaml,strace,bsdutils,util-linux,openssh-client,procps,ca-certificates,tmux,passwd,coreutils"
die(){ echo "f1: $*" >&2;exit 1;}
SELF=$0
# ---------------------------------------------------------------- M1: refuse the host. Three legs; any miss = rc != 0 with NOTHING touched (called before any other act).
refuse_host(){ v=$(systemd-detect-virt --container 2>/dev/null)
 [ "$v" = systemd-nspawn ]||die "[M1] systemd-detect-virt --container says '${v:-none}', want systemd-nspawn: nothing touched"
 mk=$(cat "$F1_ROOT/.f1-marker" 2>/dev/null);[ -n "$mk" ]||die "[M1] no build marker in the rootfs: nothing touched"
 [ "$(cat "$F1_ROOT$F1_MAIN/.git/f1-marker" 2>/dev/null)" = "$mk" ]||die "[M1] MAIN/.git does not carry the rootfs marker (a host MAIN never does): nothing touched";}
# ---------------------------------------------------------------- M6: the live town. Memory first, then the slice read, then the host before/after.
mem_ok(){ a=$(awk '/^MemAvailable:/{print $2}' "${F1_MEMINFO:-/proc/meminfo}" 2>/dev/null);[ -n "$a" ]||die "[M6] MemAvailable unreadable: nothing started"
 [ "$a" -ge $(( (F1_MEM_MAX_M+1024)*1024 )) ]||die "[M6] MemAvailable $((a/1024)) MB < MemoryMax $F1_MEM_MAX_M MB + 1 GB: nothing started (belam drops caches first)";}
slice_ok(){ u=$(machinectl show "$1" -p Unit --value 2>/dev/null);[ -n "$u" ]||{ echo "slice-read none";return 1;};s=$(systemctl show "$u" -p Slice --value 2>/dev/null);echo "slice-read $u $s";[ "$s" = machine.slice ];}
F1_SIGNERS=${F1_SIGNERS:-/var/lib/agi/allowed_signers};F1_TRUNKREF=${F1_TRUNKREF:-refs/heads/core/season3/main}
hg(){ git -c safe.directory="$F1_REPO" -C "$F1_REPO" "$@";}
# the host before/after (council 20:25:36Z 10-22): the town mails all day (15 refs/box tips moved in 2 h), so a digest compare would fail every run. A host-side change is HARD only when the container or the harness could have caused it.
hostread(){ mkdir -p "$1.d";rm -f "$1.d"/*
 { systemctl list-units 'agi-post@*' --all --plain --no-legend 2>/dev/null|awk '{print "unit",$1,$3,$4}'|sort
   for u in $(getent passwd|cut -d: -f1|grep '^agi-'|sort);do crontab -l -u $u >"$1.d/cron.$u" 2>/dev/null;echo "cron $u $(sha256sum <"$1.d/cron.$u"|cut -c1-16)";done
   hg for-each-ref --format='box %(refname) %(objectname)' refs/box 2>/dev/null|sort
   echo "cronsmd $(hg rev-parse -q --verify "$F1_TRUNKREF:.agi/nodes/.geometry/crons.md" 2>/dev/null)";} >"$1";}
# prints `hard ...` / `inconclusive ...` / `info ...` / `raw ...` lines: B = before file, A = after file ($RUN names this run)
hostdelta(){ B=$1;A=$2
 [ -s "$B" ]&&[ -s "$A" ]||{ echo "hard host before/after read missing";return 0;}
 # agi-post@ units: up = active | activating (auto-restart is activating) | reloading. HARD only for a unit that was up before and is not now.
 awk 'NR==FNR{if($1=="unit")b[$2]=$3;next}$1=="unit"{a[$2]=$3}END{for(u in b){up=(b[u]=="active"||b[u]=="activating"||b[u]=="reloading");au=(a[u]=="active"||a[u]=="activating"||a[u]=="reloading");if(up&&!au)printf "hard unit %s was %s, now %s\n",u,b[u],(a[u]==""?"gone":a[u])}}' "$B" "$A"
 awk 'NR==FNR{if($1=="unit")b[$2]=$3" "$4;next}$1=="unit"{a[$2]=$3" "$4}END{for(u in a)if(b[u]!=a[u])print "info unit",u,(b[u]==""?"new":b[u]),"->",a[u];for(u in b)if(a[u]=="")print "info unit",u,b[u],"-> gone"}' "$B" "$A"
 # crontabs: a change is listed with its diff; HARD only if the trunk's crons.md blob did not change in the window (grid_sync's 5-min apply legitimately rewrites)
 cm=hard;[ "$(sed -n 's/^cronsmd //p' "$B")" = "$(sed -n 's/^cronsmd //p' "$A")" ]||cm=info
 for u in $(sed -n 's/^cron \([^ ]*\) .*/\1/p' "$B" "$A"|sort -u);do [ "$(grep "^cron $u " "$B")" = "$(grep "^cron $u " "$A")" ]&&continue
  echo "$cm cron $u changed (trunk crons.md blob $([ $cm = hard ]&&echo unchanged||echo CHANGED) in the window)";diff "$B.d/cron.$u" "$A.d/cron.$u" 2>&1|head -20|sed "s/^/raw cron $u: /";done
 # refs/box: the delta RAW (ref old new | sha | %G? | author | subject), then the rules
 : >"$A.refs";sg=;[ -r "$F1_SIGNERS" ]&&sg=1
 awk '$1=="box"{print $2,$3}' "$A"|while read -r ref new;do old=$(awk -v r="$ref" '$1=="box"&&$2==r{print $3}' "$B");[ "$old" != "$new" ]||continue;rg=$new;[ -z "$old" ]||rg="$old..$new"
  hg -c gpg.format=ssh -c gpg.ssh.allowedSignersFile="$F1_SIGNERS" log -n 200 --format='%H|%G?|%an|%ae|%s' $rg 2>/dev/null|sed "s|^|$ref ${old:-none} $new \| |";done >>"$A.refs"
 awk '$1=="box"{print $2}' "$B"|while read -r ref;do grep -q "^box $ref " "$A"||echo "info box $ref deleted";done
 head -200 "$A.refs"|sed 's/^/raw box /'
 if [ -s "$A.refs" ];then
  if [ -z "$sg" ];then echo "inconclusive $(wc -l <"$A.refs"|tr -d ' ') new refs/box commit(s) and $F1_SIGNERS is unreadable: their signatures cannot be verified"
  else awk -F'|' '{if($3!="G")print "hard box a new commit is not G against the live allowed_signers: " $0}' "$A.refs"|head -5;fi
  awk -F'|' -v run="$RUN" '{split($1,h," ");x=tolower(h[1] " " $4 " " $5);if(index(x,"f1")>0||(run!=""&&index(h[1] " " $4 " " $5,run)>0))print "hard box a ref or author names the run or f1: " $0}' "$A.refs"|head -5
  awk -F'|' '$6 ~ /^\[town\] /{print "hard box a new [town] commit appeared in the window (a host-leg slip goes out G under belam'"'"'s key): " $0}' "$A.refs"|head -5;fi;}
# the rm guard: only a dir this harness created, by its fixed name, holding the marker it wrote, not a symlink, not under a live mount
rm_rootfs(){ d=$1;run=$2
 case $d in "$F1_DATA"/f1-nspawn-[0-9]*) ;; *) echo "f1: rm refused: $d is not $F1_DATA/f1-nspawn-<run>" >&2;return 1;; esac
 case $d in *..*|*/) echo "f1: rm refused: odd path $d" >&2;return 1;; esac
 [ -d "$d" ]&&[ ! -L "$d" ]||{ echo "f1: rm refused: $d is not a plain directory" >&2;return 1;}
 [ "$(cat "$d/.f1-marker" 2>/dev/null)" = "f1-$run" ]||{ echo "f1: rm refused: $d does not hold the marker f1-$run" >&2;return 1;}
 ! grep -qF " $d" /proc/self/mountinfo 2>/dev/null||{ echo "f1: rm refused: a mount is live under $d" >&2;return 1;}
 rm -rf --one-file-system "$d";}
# ---------------------------------------------------------------- the results file: one `key value` line per fact
rec(){ echo "$*" >>"$O/res";}
rget(){ awk -v k="$1" '$1==k{sub(/^[^ ]* ?/,"");v=$0;f=1}END{if(f)print v;exit !f}' "$2";}
# ---------------------------------------------------------------- M7: the verdict, computed from the files, never defaulted. TWO lines (R2): (i) RT2, (ii) first-start set. Overall = FAIL while either fails.
verdict(){ D=$1;R=$D/res;fl=;inc=;hard=;L1=;L2=
 g(){ rget "$1" "$R";}
 vneed(){ for k;do g $k >/dev/null||fl="$fl; missing read $k";done;}
 for k in expect rows set.A set.B nrestarts.A nrestarts.B rcstop rcstart marked.stop crondig.pre crondig.post town.A town.B mut.start mut.stop mut.town;do vneed $k;done
 for l in $(grep '^setupfail ' "$R" 2>/dev/null|tr ' ' '_');do inc="$inc; setup: $(echo $l|tr '_' ' '|cut -c11-)";done
 inc="$inc$(grep '^inconclusive ' "$R" 2>/dev/null|sed 's/^inconclusive /; /')"
 fl="$fl$(grep '^fail ' "$R" 2>/dev/null|sed 's/^fail /; /')"
 [ ! -e "$D/timeout" ]||inc="$inc; timeout: the run hit F1_TIMEOUT"
 me=$(cat "$D/mem.events" 2>/dev/null);case $me in *"max "[1-9]*|*"oom_kill "[1-9]*)inc="$inc; the container hit MemoryMax ($(echo $me|tr '\n' ' '))";; esac
 [ -e "$D/host.delta" ]||hard="$hard; host before/after delta missing"
 hard="$hard$(grep '^hard ' "$D/host.delta" 2>/dev/null|sed 's/^hard /; THE LIVE TOWN CHANGED: /')"
 inc="$inc$(grep '^inconclusive ' "$D/host.delta" 2>/dev/null|sed 's/^inconclusive /; host: /')"
 # (ii) first-start set == the boot=true names
 ex=$(g expect);s0=$(g set.A);rw=$(g rows);extra=;for x in $s0;do case " $ex " in *" $x "*);; *)extra="$extra $x";; esac;done;miss=;for x in $ex;do case " $s0 " in *" $x "*);; *)miss="$miss $x";; esac;done
 cause="agi.sh:280 rows() has no boot filter";[ -z "$miss" ]||cause="not R2 (a boot post is missing), see the raw reads";for x in $extra;do case " $rw " in *" $x "*);; *)cause="not R2 (an extra name is not a row of the box), see the raw reads";; esac;done
 rc1=$(g rcstart1) && [ "$rc1" != 0 ] && cause="not R2 (the first start itself failed, rc $rc1), see the raw reads"
 if [ -z "$s0" ];then L2="FAIL first-start set is EMPTY (empty == empty never passes)"
 elif [ -z "$extra$miss" ];then L2="PASS first-start set == the $(echo $ex|wc -w|tr -d ' ') boot=true names"
 else L2="FAIL first-start set != the boot=true names: rows $(echo $rw|wc -w|tr -d ' '), boot=true $(echo $ex|wc -w|tr -d ' '), set $(echo $s0|wc -w|tr -d ' '); extra:$extra; missing:${miss:- none}; cause: $cause";fi
 # (i) RT2
 r=;s1=$(g set.B)
 [ -n "$s1" ]&&[ "$s1" = "$s0" ]||r="$r; set after start 2 [$s1] != set before stop [$s0]"
 for t in A B;do for kv in $(g nrestarts.$t);do [ "${kv#*=}" = 0 ]||r="$r; NRestarts $t $kv";done;done
 [ "$(g rcstop)" = 0 ]||r="$r; stop rc $(g rcstop)";[ "$(g rcstart)" = 0 ]||r="$r; start 2 rc $(g rcstart)"
 [ "$(g marked.stop)" = 0 ]||r="$r; marked after stop = $(g marked.stop), want 0"
 [ -n "$(g crondig.pre)" ]&&[ "$(g crondig.pre)" = "$(g crondig.post)" ]||r="$r; crontab bytes differ: before stop [$(g crondig.pre)] after start [$(g crondig.post)]"
 tw=$(g town.B);for p in $s1;do [ $p = belam ]&&continue;case " $tw " in *" $p=1 "*);; *)r="$r; town line count for $p is not 1 ($tw)";; esac;done
 eng=$(grep '^fail ' "$R" 2>/dev/null|sed 's/^fail /; /'|tr -d '\n');[ -z "$eng" ]||r="$r$eng"
 for m in start stop town;do [ "$(g mut.$m)" = red ]||r="$r; mutant $m is not RED ($(g mut.$m))";done
 if [ -n "$r" ];then L1="FAIL${r#;}";else L1="PASS the round trip on the recorded set ($(echo $s1|wc -w|tr -d ' ') posts), crontab bytes equal, marked 0, one town line each, 3 mutants RED";fi
 [ -z "$r" ]||fl="$fl; RT2:${r#;}"
 case $L2 in FAIL*)fl="$fl; first-start set";; esac
 if [ -n "$hard" ];then O1=FAIL;C="${hard#;}";elif [ -n "$inc" ];then O1=INCONCLUSIVE;C="${inc#;}";elif [ -n "$fl" ];then O1=FAIL;C="${fl#;}";else O1=PASS;C=;fi
 V_OUT=$O1;V_L1=$L1;V_L2=$L2;V_C=$C;V_FAIL=$fl;V_INC=$inc;}
summary(){ D=$1;R=$D/res;verdict "$D"
 echo "F1 OUTCOME: $V_OUT${V_C:+  ($V_C)}"
 echo "  (i)  RT2, F1 as written ........ $V_L1"
 echo "  (ii) first-start set ........... $V_L2"
 echo "harness sha256 $(sha256sum "$SELF" 2>/dev/null|cut -c1-64)  blob $(git hash-object "$SELF" 2>/dev/null)"
 for k in trunk image box; do echo "$k $(rget $k "$D/meta" 2>/dev/null)";done
 echo "--- stub behaviour and readings (NOT measured; council 20:25:36Z D3, D6)"
 echo "claude stub: logs argv, prints the line '? for shortcuts' (an unmeasured stand-in: no start step reads a ready byte, agi.sh stuck() matches only the 6 dialog titles), runs \`box read\` every 5 s like a real post so stop's blast sees the acks, ends in \`exec sleep infinity\` (NRestarts must be 0)."
 echo "also stubbed: gh (auth status -> 0), pi, and guard-init (--status -> 0: its layers are HOST layers, absent in nspawn). The memory-PSI ExecStartPre, agi.sh's load gate and /proc/loadavg are the HOST's inside nspawn."
 echo "stop mutant: agi-belam's own cron block left standing (the crons.py remove call dropped), as RT2 does; pstop refuses a foreign-ROOT block outright. RED comes from marked_sum = crons.py marked per agi- uid against the real crontab."
 echo "--- raw reads (res)";cat "$R" 2>/dev/null
 echo "--- host before / after (hard = the container or the harness could have caused it; info and raw = the live town's own traffic, listed)";cat "$D/host.delta" 2>/dev/null;echo "-- before";cat "$D/host.before" 2>/dev/null;echo "-- after";cat "$D/host.after" 2>/dev/null
 echo "--- container memory (peak, last memory.events, agi.slice at run time, slice read)";cat "$D/mem.peak" "$D/mem.events" "$D/slice.read" 2>/dev/null;sed -n '1p;$p' "$D/agislice" 2>/dev/null
 echo "--- captive transcript";cat "$D/captive" 2>/dev/null
 echo "--- steps";cat "$D/steps" 2>/dev/null;}
# ================================================================ INSIDE the container
inner_env(){ . "$F1_ROOT/f1/env";O=$F1_ROOT/f1/out;ANS=$F1_ROOT/f1/answers;M=$F1_ROOT$F1_MAIN;AGSH=$M/extensions/agi/bin/agi.sh;CRONS=$M/extensions/agi/bin/crons.py
 export AGI_MAIN=$M AGI_BOX=$BOX PIN=$SHA AGI_GUARD_INIT=$F1_ROOT/f1/guard-init-stub AGI_TOWN_BOXBIN=$F1_ROOT/opt/agi/bin/box PRIME_USER=belam;}
step(){ echo "$(date -u +%H:%M:%SZ) $*" >>"$O/steps";}
G(){ git -c safe.directory="$M" -C "$M" "$@";}
uidsf(){ getent passwd|cut -d: -f1|grep '^agi-'|sort;}
rowsf(){ G show "$SHA:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$BOX" 'select(has("harness") and .box==$x)|.name'|sort;}
bootf(){ G show "$SHA:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$BOX" 'select(has("harness") and .box==$x and .boot==true)|.name'|sort;}
wait_go(){ i=0;while [ ! -e "$F1_ROOT/f1/go" ];do i=$((i+1));[ $i -le 120 ]||{ rec setupfail wait_go "no /f1/go in 120 s (the host refused the slice read, or died)";return 1;};sleep 1;done;}
psi(){ grep '^some' /proc/pressure/memory 2>/dev/null|head -1;}
# a snapshot of the town as the container reads it (M2, M3): $1 = label
marked_sum(){ n=0;for u in $(uidsf);do c=$(python3 "$CRONS" marked --root "$M" --user $u 2>/dev/null)||c=X;case $c in ''|*[!0-9]*)c=99;; esac;n=$((n+c));done;echo $n;}
cron_dig(){ for u in $(uidsf);do echo "$u=$(crontab -l -u $u 2>/dev/null|sha256sum|cut -c1-16)";done|tr '\n' ' ';}
setnow(){ systemctl list-units 'agi-post@*' --plain --no-legend --state=active 2>/dev/null|awk '{sub(/^agi-post@/,"",$1);sub(/\.service$/,"",$1);print $1}'|sort|tr '\n' ' '|sed 's/ $//';}
restarts(){ for p in $(setnow);do echo "$p=$(systemctl show agi-post@$p.service -p NRestarts --value 2>/dev/null)";done|tr '\n' ' ';}
snap(){ rec "set.$1 $(setnow)";rec "nrestarts.$1 $(restarts)";rec "psi.$1 $(psi)";rec "units.$1 $(systemctl list-units 'agi-*' --plain --no-legend --state=active 2>/dev/null|awk '{print $1}'|sort|tr '\n' ' ')";}
# M4: the counted town line per post over <tip>..refs/box/belam/<p>; tips = a file of `p sha` lines (empty file = from the root)
townlines(){ for p in $(setnow);do [ $p = belam ]&&continue;t=$(awk -v p=$p '$1==p{print $2}' "$1" 2>/dev/null);rg=refs/box/belam/$p;[ -z "$t" ]||rg="$t..$rg"
  echo "$p=$(G log --format=%B $rg 2>/dev/null|grep -cxF "[town] up $SHA")";done|tr '\n' ' '|sed 's/ $//';}
tips(){ for p in $(sed -n 's/^running //p' $F1_ROOT/etc/agi/town.state 2>/dev/null);do echo "$p $(G rev-parse -q --verify refs/box/belam/$p 2>/dev/null)";done;}
# M5: the captive flow, fail closed. $@ = the agi.sh command. Answers come ONLY from the answers file; an unknown [ask] KEY, any [owner-do], a hang = FAIL with the line printed.
cap(){ leg=$1;shift;n=0
 while :;do timeout "$F1_STEPTIMEOUT" "$@" >"$O/cap.out" 2>"$O/cap.err";rc=$?;{ echo "== $leg rc=$rc";cat "$O/cap.out";sed 's/^/stderr: /' "$O/cap.err"|tail -40;} >>"$O/transcript.$leg"
  case $rc in
  20)line=$(grep '^\[ask\] ' "$O/cap.out"|head -1);k=$(echo "$line"|sed -n 's/^\[ask\] \([A-Z][A-Z0-9_]*\):.*/\1/p');v=
   [ -z "$k" ]||v=$(awk -F= -v k="$k" '$1==k{print substr($0,length(k)+2)}' "$ANS" 2>/dev/null|head -1)
   echo "Q [$leg] $line | A ${v:-<none>}" >>"$O/captive"
   [ -n "$v" ]||{ rec fail "captive: $leg asked '$line' and the answers file has no such key";return 20;}
   n=$((n+1));[ $n -le 6 ]||{ rec fail "captive: $leg asked more than 6 questions";return 20;}
   timeout "$F1_QTIMEOUT" "$1" "$2" answer "$k" "$v" >/dev/null 2>&1||{ rec fail "captive: answering $k hung or failed";return 20;};;
  21)line=$(grep '^\[owner-do\] ' "$O/cap.out"|head -1);echo "Q [$leg] $line | A <owner-do: refused>" >>"$O/captive";rec fail "captive: $leg printed $line";return 21;;
  124)rec fail "captive: $leg hung ($F1_STEPTIMEOUT s)";return 124;;
  *)return $rc;; esac;done;}
# the mutants: ONE exact-anchor edit of the container's clone of agi.sh (never the trunk), restored by git afterwards. An anchor that is not found exactly once is a setup failure, not a green.
patch_agsh(){ python3 - "$1" "$2" "$3" <<'PYEOF'
import sys
f,a,b=sys.argv[1:4];s=open(f).read()
if s.count(a)!=1: sys.exit(3)
open(f,'w').write(s.replace(a,b))
PYEOF
}
restore_agsh(){ G checkout -q -- extensions/agi/bin/agi.sh&&[ -z "$(G status --porcelain -- extensions/agi/bin/agi.sh)" ];}
inner(){ refuse_host||{ rc=$?;exit $rc;}
 inner_env;mkdir -p "$O";: >"$O/res";rec started "$(date -u +%FT%TZ)"
 wait_go||exit 1
 trap 'exit 130' INT TERM HUP;trap 'systemctl poweroff >/dev/null 2>&1' 0
 rec harness-in-container "$(sha256sum "$F1_ROOT/f1/f1-nspawn.sh"|cut -c1-64)"
 EXPECT=$(bootf|tr '\n' ' '|sed 's/ $//');ROWS=$(rowsf|tr '\n' ' '|sed 's/ $//');rec expect "$EXPECT";rec rows "$ROWS"
 [ -n "$ROWS" ]||{ rec setupfail rows "no rows for box $BOX at $SHA";return 1;}
 # ---- the owner's act on a fresh box (done here, logged): the group, the prime user, the stubs the real start would otherwise ask the owner for
 step prep;groupadd agi 2>/dev/null;useradd -m -s /bin/sh belam 2>/dev/null;id belam >/dev/null 2>&1||{ rec setupfail prep "no user belam";return 1;}
 install -d "$F1_ROOT/opt/agi/bin" "$F1_ROOT/usr/local/bin" "$F1_ROOT/f1/out/claude";chmod 1777 "$F1_ROOT/f1/out/claude"
 printf '#!/bin/sh\nexit 0\n' >"$F1_ROOT/opt/agi/bin/pi";chmod 755 "$F1_ROOT/opt/agi/bin/pi"
 printf '#!/bin/sh\nexit 0\n' >"$F1_ROOT/f1/guard-init-stub"   # guard-init's layers are HOST layers (sysctl, earlyoom...): they do not exist in nspawn; named in the summary
 printf '#!/bin/sh\ncase "$1 $2" in "auth status")exit 0;; esac\nexit 0\n' >"$F1_ROOT/usr/local/bin/gh";chmod 755 "$F1_ROOT/usr/local/bin/gh"
 # M2: claude = a stub. Logs argv, prints the ready line, and stays up (agi-post@ is Restart=always RestartSec=30: a stub that exits flaps the set). It ALSO reads its mail every 5 s, as a real post does, so stop's blast sees the ack (held ref) and does not wait ack_wait_s=600 per stop.
 printf '%s\n' '#!/bin/sh' 'echo "$(date -u +%FT%TZ) $(id -un) $*" >>/f1/out/claude/argv.log 2>/dev/null' 'echo "? for shortcuts"' '(while :;do box read >/dev/null 2>&1;sleep 5;done)&' 'exec sleep infinity' >"$F1_ROOT/usr/local/bin/claude";chmod 755 "$F1_ROOT/usr/local/bin/claude"
 printf '%s\n' "$(date -u +%FT%TZ) $EXPECT" >"$F1_ROOT/f1/out/claude/boot-names"
 # ---- the host act, for real (agi.sh host at the pin); the users come from the pinned projection
 step host;timeout "$F1_STEPTIMEOUT" sh "$AGSH" host >"$O/host.out" 2>&1;rc=$?;rec rchost $rc
 [ $rc = 0 ]||{ rec fail "agi.sh host rc $rc: $(tail -3 "$O/host.out"|tr '\n' ' '|cut -c1-300)";return 1;}
 for p in $ROWS;do getent passwd agi-$p >/dev/null||{ rec fail "agi.sh host left no user agi-$p";return 1;};h=$(getent passwd agi-$p|cut -d: -f6)
  install -d -o agi-$p -g agi-$p -m 750 "$h" "$h/.claude"||{ rec setupfail homes "cannot make $h";return 1;};printf '{"f1":"stub login, no secret"}\n' >"$h/.claude/.credentials.json";chown agi-$p:agi-$p "$h/.claude/.credentials.json";chmod 600 "$h/.claude/.credentials.json";done
 # ---- the first start (S1..S9), then THE ROUND TRIP
 step start1;rec psi.start1 "$(psi)";cap start1 sh "$AGSH" start;rc=$?;rec rcstart1 $rc
 if [ $rc != 0 ];then hc=$(hot);[ -z "$hc" ]||rec inconclusive "a post start was refused or held by the HOST's load: $hc (start 1)";rec fail "first start rc $rc: $(tail -3 "$O/cap.err"|tr '\n' ' '|cut -c1-300)";snap A;return 1;fi
 sleep 20;snap A;rec town.A "$(townlines /dev/null)"
 rec crondig.start1 "$(cron_dig)"
 rec crondig.pre "$(cron_dig)"
 step stop;rec psi.stop "$(psi)";cap stop sh "$AGSH" stop;rc=$?;rec rcstop $rc;rec marked.stop "$(marked_sum)";cp $F1_ROOT/etc/agi/town.state "$O/town.state.afterstop" 2>/dev/null;rec ack-lines "$(grep -c '^ack ' $F1_ROOT/etc/agi/town.state 2>/dev/null) held/card/noack: $(awk '/^(ack|noack)/{print $1" "$3}' $F1_ROOT/etc/agi/town.state 2>/dev/null|sort|uniq -c|tr '\n' ';')"
 rec set.stopped "$(setnow)";rec crondig.stopped "$(cron_dig)"
 tips >"$O/tips.stop"
 step start2;rec psi.start2 "$(psi)";cap start2 sh "$AGSH" start;rc=$?;rec rcstart $rc
 if [ $rc != 0 ];then hc=$(hot);[ -z "$hc" ]||rec inconclusive "a post start was refused or held by the HOST's load: $hc (start 2)";fi
 sleep 20;snap B;rec town.B "$(townlines "$O/tips.stop")";rec crondig.post "$(cron_dig)";rec marked.up "$(marked_sum)"
 [ $rc = 0 ]||{ rec fail "start 2 rc $rc: $(tail -3 "$O/cap.err"|tr '\n' ' '|cut -c1-300)";}
 if [ $rc = 0 ];then mutants;else for m in start stop town;do rec mut.$m "not-run: start 2 failed";done;fi
 step done;return 0;}
# why a post start can be refused or slow for a reason that is not the town's: the unit's memory-PSI ExecStartPre (/proc/pressure/memory is the HOST's inside nspawn) and agi.sh's own load gate (/proc/loadavg and io PSI are the HOST's too). Prints the cause, or nothing.
hot(){ a=$(psi|sed -n 's/.*avg10=\([0-9.]*\).*/\1/p');l=$(cut -d' ' -f1 /proc/loadavg 2>/dev/null);i=$(sed -n 's/^some .*avg60=\([0-9.]*\).*/\1/p' /proc/pressure/io 2>/dev/null)
 c=$(G show "$SHA:.agi/config.json" 2>/dev/null|jq -r '.values.local_maxxing.de_live_parents.ceiling_if|"\(.loadavg1_lt) \(.io_psi_some_avg60_lt)"' 2>/dev/null)
 awk -v a="${a:-0}" -v l="${l:-0}" -v i="${i:-0}" -v LT="${c%% *}" -v IT="${c##* }" 'BEGIN{if(a>40)print "memory PSI avg10 " a " > 40";else if(LT!=""&&l>=LT+0)print "loadavg1 " l " >= " LT;else if(IT!=""&&i>=IT+0)print "io PSI avg60 " i " >= " IT}';}
# ---- the three RT2 mutants IN the container, each RED, each healed by a clean run afterwards. State on entry: the town is UP (start 2 done).
mutants(){ vic=$(echo $EXPECT|tr ' ' '\n'|grep -vx belam|head -1)
 # (a) start drops a post: the clean stop, then a start that stops $vic again at its end
 step mutant-start;cap mstop1 sh "$AGSH" stop||{ rec mut.start "not-run: the clean stop before it failed";rec fail "mutant start: the clean stop failed";return 0;}
 if patch_agsh "$AGSH" '[ -z "$bad" ]||die "[posts] cannot start:$bad (listed; a re-run retries them)"' '[ -z "$bad" ]||die "[posts] cannot start:$bad (listed; a re-run retries them)";systemctl stop agi-post@'"$vic"'.service';then
  cap mstart sh "$AGSH" start;rc=$?;sleep 5;after=$(setnow);rec mut.start.reads "rc=$rc victim=$vic set-after=[$after]"
  if [ $rc != 0 ]||[ "$after" != "$(rget set.B "$O/res")" ];then rec mut.start red;else rec mut.start "GREEN: start rc 0 and the set is unchanged";fi
 else rec mut.start "not-run: anchor not found exactly once";fi
 restore_agsh||rec fail "mutant start: agi.sh not restored";cap mheal1 sh "$AGSH" start||rec fail "mutant start: the clean start did not heal (rc $?)"
 # (c) a start that sends the town line twice: the clean stop, then the mutated start
 step mutant-town;cap mstop2 sh "$AGSH" stop||{ rec mut.town "not-run: the clean stop before it failed";rec fail "mutant town: the clean stop failed";return 0;}
 tips >"$O/tips.m"
 if patch_agsh "$AGSH" '$BOXB town up $PIN)||die' '$BOXB town up $PIN&&sudo -H -u agi-belam env AGI_POST=belam AGI_BOX=$BOX AGI_TRUNK=$TB $BOXB town up $PIN)||die';then
  cap mstart2 sh "$AGSH" start;rc=$?;sleep 5;tl=$(townlines "$O/tips.m");rec mut.town.reads "rc=$rc town-lines=[$tl]"
  case " $tl " in *" "*=2" "*)rec mut.town red;; *)rec mut.town "GREEN: no post shows 2 town lines ($tl)";; esac
 else rec mut.town "not-run: anchor not found exactly once";fi
 restore_agsh||rec fail "mutant town: agi.sh not restored"
 # (b) stop leaves a cron line: the cron remove dropped; the town must NOT end clean
 step mutant-stop;if patch_agsh "$AGSH" '$CR remove --root "$MAIN" --user $u||die "[crons] remove failed for $u"' ':';then
  cap mstop3 sh "$AGSH" stop;rc=$?;mk=$(marked_sum);rec mut.stop.reads "rc=$rc marked-after=$mk"
  if [ $rc != 0 ]||[ "$mk" != 0 ];then rec mut.stop red;else rec mut.stop "GREEN: stop rc 0 and marked 0";fi
 else rec mut.stop "not-run: anchor not found exactly once";fi
 restore_agsh||rec fail "mutant stop: agi.sh not restored";cap mheal3 sh "$AGSH" stop||rec fail "mutant stop: the clean stop did not heal (rc $?)"
 return 0;}
# ================================================================ HOST (root)
build_image(){ TAR=$F1_DATA/f1-nspawn-image/noble.tar;IMGSHA=
 if [ ! -s "$TAR" ];then mkdir -p "$F1_DATA/f1-nspawn-image"||die "cannot make the image dir"
  cn=$(. /etc/os-release;echo "$VERSION_CODENAME");mir=${F1_MIRROR:-http://archive.ubuntu.com/ubuntu}
  echo "f1: mmdebstrap $cn from $mir (the one network use)" >&2
  mmdebstrap --variant=minbase --include="$F1_PKGS" "$cn" "$TAR.part" "$mir"||{ rm -f "$TAR.part";die "mmdebstrap failed";}
  mv "$TAR.part" "$TAR"&&sha256sum "$TAR" >"$TAR.sha256";fi
 IMGSHA=$(sha256sum "$TAR"|cut -c1-64);}
inner_unit(){ printf '%s\n' '[Unit]' 'Description=F1 inner leg' 'After=multi-user.target' 'SuccessAction=poweroff' 'FailureAction=poweroff' '[Service]' 'Type=oneshot' 'TimeoutStartSec=infinity' 'ExecStart=/bin/sh /f1/f1-nspawn.sh inner' 'StandardOutput=file:/f1/out/inner.log' 'StandardError=file:/f1/out/inner.log' '[Install]' 'WantedBy=multi-user.target';}
cleanup(){ [ -z "$NAME" ]||machinectl terminate "$NAME" >/dev/null 2>&1;[ -z "$NP" ]||wait "$NP" 2>/dev/null
 [ -z "$ROOTFS" ]||[ ! -e "$ROOTFS" ]||rm_rootfs "$ROOTFS" "$RUN";}
sample(){ [ -n "$UNIT" ]||return 0;pk=$(systemctl show "$UNIT" -p MemoryPeak --value 2>/dev/null);[ -z "$pk" ]||echo "$pk" >"$OUT/mem.peak.last"
 cg=$(systemctl show "$UNIT" -p ControlGroup --value 2>/dev/null);[ -z "$cg" ]||[ ! -r "${F1_CGROOT:-/sys/fs/cgroup}$cg/memory.events" ]||cp "${F1_CGROOT:-/sys/fs/cgroup}$cg/memory.events" "$OUT/mem.events.last" 2>/dev/null
 { date -u +%H:%M:%SZ;systemctl show agi.slice -p MemoryCurrent -p MemoryHigh 2>/dev/null|tr '\n' ' ';echo;} >>"$OUT/agislice";}
run_host(){ SHA=${1:-};ANS=${2:-};OUT=${3:-}
 [ "$(id -u)" = 0 ]||die "run needs root (belam's host act): nothing touched"
 case $SHA in *[!0-9a-f]*|"")die "usage: run <40-hex trunk sha> <answers-file> [out-dir]";; esac;[ ${#SHA} = 40 ]||die "the sha is not 40 hex"
 [ -f "$ANS" ]||die "answers file '$ANS' not found (an empty file is fine)"
 for c in systemd-nspawn machinectl mmdebstrap systemd-detect-virt systemctl git tar sha256sum jq python3;do command -v $c >/dev/null||die "missing tool: $c: nothing touched";done
 [ "$(systemd-detect-virt --container 2>/dev/null)" != systemd-nspawn ]||die "run is the HOST leg; this is already a container"
 git -c safe.directory="$F1_REPO" -C "$F1_REPO" cat-file -e "$SHA^{commit}" 2>/dev/null||die "$SHA is not a commit of $F1_REPO"
 mem_ok;RUN=$(date -u +%Y%m%d%H%M%S)$$;NAME=f1nspawn-$RUN;ROOTFS=$F1_DATA/f1-nspawn-$RUN;NP=;UNIT=;OUT=${OUT:-$F1_DATA/f1-nspawn-$RUN.out};mkdir -p "$OUT"||die "cannot make $OUT"
 hostread "$OUT/host.before";trap 'exit 130' INT TERM HUP;trap cleanup 0
 build_image;{ echo "trunk $SHA";echo "image $IMGSHA $TAR";echo "box $F1_BOX";echo "run $RUN";} >"$OUT/meta"
 mkdir "$ROOTFS"||die "$ROOTFS exists";printf 'f1-%s\n' "$RUN" >"$ROOTFS/.f1-marker"
 tar -C "$ROOTFS" -xpf "$TAR"||die "extract failed"
 # the repo: a depth-1 fetch of the named sha with a LOCAL branch core/season3/main at it (the unit's ExecCondition refuses a detached trunk)
 MM=$ROOTFS$F1_MAIN;mkdir -p "$MM"&&git init -q "$MM"||die "cannot init the container's MAIN"
 git -C "$MM" fetch -q --depth 1 --upload-pack="git -c safe.directory=$F1_REPO -c uploadpack.allowAnySHA1InWant=true upload-pack" "file://$F1_REPO" "$SHA"||die "depth-1 fetch of $SHA failed"
 git -C "$MM" update-ref refs/heads/core/season3/main "$SHA"&&git -C "$MM" symbolic-ref HEAD refs/heads/core/season3/main&&git -C "$MM" -c core.hooksPath=/dev/null reset -q --hard||die "cannot check out $SHA"
 printf 'f1-%s\n' "$RUN" >"$MM/.git/f1-marker"
 install -d "$ROOTFS/f1/out" "$ROOTFS/etc/systemd/system/multi-user.target.wants"&&install -m 755 "$SELF" "$ROOTFS/f1/f1-nspawn.sh"&&cp "$ANS" "$ROOTFS/f1/answers"
 printf 'SHA=%s\nBOX=%s\nRUN=%s\n' "$SHA" "$F1_BOX" "$RUN" >"$ROOTFS/f1/env";inner_unit >"$ROOTFS/etc/systemd/system/f1-inner.service";ln -sf ../f1-inner.service "$ROOTFS/etc/systemd/system/multi-user.target.wants/f1-inner.service"
 : >"$ROOTFS/etc/machine-id"
 systemd-nspawn --quiet --directory="$ROOTFS" --machine="$NAME" --boot --console=passive --private-network --private-users=pick --private-users-ownership=chown --slice=machine.slice --property=MemoryMax=${F1_MEM_MAX_M}M --link-journal=no >"$OUT/nspawn.log" 2>&1 &
 NP=$!;i=0;while :;do UNIT=$(machinectl show "$NAME" -p Unit --value 2>/dev/null);[ -z "$UNIT" ]||break;i=$((i+1));kill -0 $NP 2>/dev/null&&[ $i -le 90 ]||{ echo "f1: the container never registered: $(tail -3 "$OUT/nspawn.log"|tr '\n' ' ')" >&2;break;};sleep 1;done
 slice_ok "$NAME" >"$OUT/slice.read";sr=$?
 if [ -z "$UNIT" ]||[ $sr != 0 ];then machinectl terminate "$NAME" >/dev/null 2>&1;echo "inconclusive M6: slice/registration read '$(cat "$OUT/slice.read")' (want machine.slice): container terminated, NOTHING run" >"$OUT/res";hostread "$OUT/host.after";hostdelta "$OUT/host.before" "$OUT/host.after" >"$OUT/host.delta";summary "$OUT" >"$OUT/summary.txt";cat "$OUT/summary.txt";cleanup;trap - 0;return 2;fi
 : >"$ROOTFS/f1/go";t0=$(date +%s)
 while kill -0 $NP 2>/dev/null;do sample;[ $(( $(date +%s)-t0 )) -lt $F1_TIMEOUT ]||{ : >"$OUT/timeout";machinectl terminate "$NAME" >/dev/null 2>&1;break;};sleep 5;done
 wait $NP 2>/dev/null;NP=
 [ ! -e "$OUT/mem.peak.last" ]||cp "$OUT/mem.peak.last" "$OUT/mem.peak";[ ! -e "$OUT/mem.events.last" ]||cp "$OUT/mem.events.last" "$OUT/mem.events"
 [ -e "$ROOTFS/f1/out/res" ]&&cp "$ROOTFS/f1/out/res" "$OUT/res"||: >"$OUT/res"
 for f in steps captive inner.log host.out cap.out cap.err; do [ ! -e "$ROOTFS/f1/out/$f" ]||cp "$ROOTFS/f1/out/$f" "$OUT/$f";done;cp "$ROOTFS"/f1/out/transcript.* "$ROOTFS"/f1/out/tips.* "$ROOTFS"/f1/out/town.state.* "$OUT/" 2>/dev/null;cp -r "$ROOTFS/f1/out/claude" "$OUT/claude" 2>/dev/null
 hostread "$OUT/host.after";hostdelta "$OUT/host.before" "$OUT/host.after" >"$OUT/host.delta";summary "$OUT" >"$OUT/summary.txt";cat "$OUT/summary.txt";cleanup;trap - 0 INT TERM HUP
 case $V_OUT in PASS)return 0;; FAIL)return 1;; *)return 2;; esac;}
# ================================================================
[ -z "$F1_LIB" ]||return 0 2>/dev/null||true
case ${1:-} in
run)shift;run_host "$@";exit $?;;
inner)inner;exit $?;;
verdict)summary "$2";exit 0;;
*)die "usage: f1-nspawn.sh run <40-hex trunk sha> <answers-file> [out-dir]  (root)   |   inner (inside the container)";;
esac
