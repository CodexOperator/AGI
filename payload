#!/bin/sh
# lab-repack.sh: ONE geometric repack of the lab repo under a hold (goal:g7.16.1.14; A1 placed 3/3 by sanctuary-master
# 14:0xZ 11-17 with H1-H3 + M1-M3 + the line-count rule, RAN 15:01Z: 3497 packs -> 2, cat-file 8.1 s -> 56 ms; A2 (b)
# placed 3/3 15:3xZ: this is what agi-lab-pack-count's FIRE alarm asks belam to run, by hand, until the council words
# self-firing). Run as agi-belam on encryption-town (sudo -n for root and uid 1000):
#   lab-repack.sh pre | held | post        (held = the bounded hold, HOLD_S, default 600 s; post = the timings + PASS line)
#   A1_H=<scratch repo owned by uid 1000> A1_D=<log dir> lab-repack.sh rehearse   (the core alone, no hold, no lab)
#   lab-repack.sh loose    (the L-FIRE, (E): pack every loose object by id, NO pack deleted, NO hold, NO freeze)
# After A1: a unit wait reads 'inactive' or 'failed' EXACTLY, never 'is-active -q' (which reads 'activating' as stopped).
set -u
H=${A1_H:-/data/nas/lab/data/work/agi}            # the server-local path of the lab repo (export /data/nas -> lab /data)
D=${A1_D:-/data/scratch/belam/a1}; mkdir -p $D
POSTS="director-thought-1 director-thought-goals director-thought-review director-thought-science less-is-more plasma remix thought-master"
now(){ date -u +%TZ; }
stop(){ echo "STOP $(now): $*"; [ -e ${D:-/nonexistent}/ran ] && [ ! -e $D/ok ] && [ "${INNER:-}" ] && { restore; touch $D/restored; }; exit 3; }
# AS_OWNER / SU: how git and find reach the repo; the defaults are the lab's (uid 1000 owns every pack; root reads the
# export). The loose lane test sets both EMPTY to run on a scratch repo as itself; no lab run ever sets them.
AS_OWNER=${AS_OWNER-sudo -n -u belam}; SU=${SU-sudo -n}
G(){ $AS_OWNER git -c safe.directory=$H -C $H "$@"; }        # uid 1000 = the owner of every pack
L(){ b=$(printf '%s\n' "$1" | base64 -w0); (cd /data/play/shael-rig && sudo -n -u belam ./rig ssh "sudo -n /usr/local/sbin/agi-lab exec sh -c 'echo $b | base64 -d | sh'"); }
# read NAME CMD...: stdout -> $D/NAME, stderr -> $D/NAME.err; prints lines; STOP on 0 lines or stderr
rd(){ n=$1; shift; "$@" >$D/$n 2>$D/$n.err; r=$?; c=$(wc -l <$D/$n); echo "read $n: rc=$r lines=$c stderr=$(wc -c <$D/$n.err)B"
  [ $r = 0 ] && [ $c -gt 0 ] && [ ! -s $D/$n.err ] || { head -3 $D/$n.err; stop "$n NOT READ"; }; }
packs(){ p=$(sudo -n find $H/.git/objects/pack -maxdepth 1 -name '*.pack' | wc -l); k=$(sudo -n find $H/.git/objects/pack -maxdepth 1 -name '*.keep' | wc -l)
  b=$(sudo -n du -sb $H/.git/objects/pack | cut -f1); lo=$(sudo -n find $H/.git/objects -mindepth 2 -maxdepth 2 -path '*/objects/[0-9a-f][0-9a-f]/*' | wc -l)
  o=$(sudo -n find $H/.git/objects/pack -maxdepth 1 -name '*.keep' -printf '%TY-%Tm-%Td\n' | sort | head -1)
  echo "packs=$p keep=$k packs_without_keep=$((p-k)) keep_oldest=${o:-none} pack_bytes=$b loose_objects=$lo"
  echo "midx=$(sudo -n test -e $H/.git/objects/pack/multi-pack-index && echo yes || echo no) commit-graph=$(sudo -n test -e $H/.git/objects/info/commit-graph && echo yes || echo no) alternates=$(sudo -n test -e $H/.git/objects/info/alternates && echo yes || echo no)"; }
TIM='h=$(getent passwd agi-thought-master | cut -d: -f6); cd $h/t; for i in 1 2 3; do s=$(date +%s%N); runuser -u agi-thought-master -- env HOME=$h git cat-file -t HEAD >/dev/null; e=$(date +%s%N); echo "cat-file run$i $(( (e-s)/1000000 ))ms"; done; for i in 1 2 3; do s=$(date +%s%N); runuser -u agi-thought-master -- env -C $h/t AGI_POST=thought-master HOME=$h PATH=/opt/agi/bin:/usr/bin:/bin timeout 20 box i >/dev/null; r=$?; e=$(date +%s%N); echo "row6 run$i rc=$r $(( (e-s)/1000000 ))ms"; done'
med(){ grep "^$1 " | sed 's/.* \([0-9]*\)ms$/\1/' | sort -n | sed -n 2p; }
timings(){ L "$TIM" > $D/tim.$1 2>&1; cat $D/tim.$1; echo "($1: run1 is the COLD read) median cat-file=$(med cat-file <$D/tim.$1)ms row6=$(med row6 <$D/tim.$1)ms lines=$(wc -l <$D/tim.$1)"; }

# H3 (all-is-one): a freeze does not close a pack. One line per post: procs in its cgroup, git procs, objects/pack paths in maps+fd.
H3='for p in '"$POSTS"'; do cg=$(systemctl show -p ControlGroup --value agi-post@$p.service); n=0; g=0; k=0; e=0; for x in $(cat /sys/fs/cgroup$cg/cgroup.procs); do n=$((n+1)); [ "$(cat /proc/$x/comm 2>/dev/null)" = git ] && g=$((g+1)); u=$(stat -c %U /proc/$x 2>/dev/null) || continue; o=$(runuser -u $u -- sh -c "cat /proc/$x/maps && ls -l /proc/$x/fd" 2>&1); if [ $? != 0 ]; then [ -d /proc/$x ] && e=$((e+1)); else k=$((k+$(printf "%s\n" "$o" | grep -c "objects/pack"))); fi; done; echo "$p procs=$n git=$g pack=$k unread=$e"; done' 
h3(){ L "$H3" > $D/h3.$1 2>&1; c=$(grep -c ' procs=' $D/h3.$1); echo "H3 $1: lines=$c $(awk '{print $1":"$3","$4","$5}' $D/h3.$1 | tr '\n' ' ')"
  [ "$c" = 8 ] || stop "H3 $1 NOT READ ($c of 8 lines)"; grep ' procs=0 ' $D/h3.$1 && stop "H3 $1: a post cgroup with no process = NOT READ"; grep -v ' unread=0$' $D/h3.$1 && stop "H3 $1: a process whose maps/fd its own uid could not read = NOT READ"; return 0; }

# M3: fsck by the LIST: sorted output + line count; rc and stderr printed
fl(){ G fsck --connectivity-only >$D/fsck.$1.raw 2>$D/fsck.$1.err; r=$?; sort $D/fsck.$1.raw >$D/fsck.$1; echo "fsck $1: rc=$r lines=$(wc -l <$D/fsck.$1) stderr=$(wc -l <$D/fsck.$1.err) ($(cut -d' ' -f1,2 $D/fsck.$1 | sort | uniq -c | tr -s ' ' | tr '\n' ';'))"
  [ $r = 0 ] && [ -s $D/fsck.$1 ] && [ ! -s $D/fsck.$1.err ] || stop "fsck $1 NOT READ / rc $r"; }
# M1: mode/owner/group of every pack-dir file, counted
m1(){ sudo -n find $H/.git/objects/pack -maxdepth 1 -type f -printf '%m %u %g\n' | sort | uniq -c >$D/m1.$1; echo "M1 $1: lines=$(wc -l <$D/m1.$1) $(tr -s ' ' <$D/m1.$1 | tr '\n' ';')"; [ -s $D/m1.$1 ] || stop "M1 $1 NOT READ"; }
# M2: ADD-ONLY restore from the hard-link copy, then fsck by the list
restore(){ echo "-- M2 RESTORE (add-only) $(now)"; sudo -n cp -al --update=none $H/.git/objects.a1-before/. $H/.git/objects/ 2>$D/restore.err; echo "restore cp rc=$? stderr=$(wc -l <$D/restore.err) (judged by the counts + M3, never by rc)"; packs | tee $D/packs.restored
  echo "restored vs BEFORE: loose $(sed -n 's/.*loose_objects=\([0-9]*\).*/\1/p' $D/packs.restored) (BEFORE $(sed -n 's/.*loose_objects=\([0-9]*\).*/\1/p' $D/packs.before)); every BEFORE pack-dir name present: $(sudo -n find $H/.git/objects/pack -maxdepth 1 -type f -printf '%f\n' | sort | comm -23 $D/names.before - | wc -l) missing"; fl restored
  cmp -s $D/fsck.before $D/fsck.restored && echo "M3 restored: dangling list byte-equal to BEFORE" || echo "M3 restored: list DIFFERS from BEFORE (diff in $D)"; }

# the BEFORE -> M2 copy -> RUN -> AFTER core (held-inner; and rehearse, on a scratch repo)
core(){
  echo "-- BEFORE $(now)"; packs | tee $D/packs.before; rd refs.before G for-each-ref --format='%(objectname) %(refname)'
  sudo -n find $H/.git/objects/pack -maxdepth 1 -type f -printf '%f\n' | sort >$D/names.before; echo "pack-dir names before: $(wc -l <$D/names.before)"
  m1 before; ref=$H/.git/objects/pack/$(sudo -n find $H/.git/objects/pack -maxdepth 1 -name '*.pack' -perm 444 -printf '%f\n' | head -1)
  sudo -n getfacl -p --omit-header $ref | grep -v '^$' >$D/acl.ref; echo "M1 ref ACL (a 444 pack): $(tr '\n' ' ' <$D/acl.ref)"; [ -s $D/acl.ref ] || stop "M1 ACL NOT READ"
  echo "M1: core.sharedRepository=$(G config --get core.sharedRepository || echo unset); the run's umask set to 0002 (uid 1000's own)"
  fl before
  echo "M2: host $(cp --version | head -1) (restore uses cp -al --update=none)"
  echo "-- M2 COPY $(now)"; sudo -n rm -rf $H/.git/objects.a1-before; sudo -n cp -al $H/.git/objects $H/.git/objects.a1-before || stop "M2 copy failed"
  bp=$(sudo -n find $H/.git/objects.a1-before/pack -maxdepth 1 -name '*.pack' | wc -l); bl=$(sudo -n find $H/.git/objects.a1-before -mindepth 2 -maxdepth 2 -path '*/objects.a1-before/[0-9a-f][0-9a-f]/*' | wc -l)
  ap=$(sed -n 's/^packs=\([0-9]*\).*/\1/p' $D/packs.before); al=$(sed -n 's/.*loose_objects=\([0-9]*\).*/\1/p' $D/packs.before)
  echo "M2 copy: packs $bp (BEFORE $ap), loose $bl (BEFORE $al)"; [ "$bp" = "$ap" ] && [ "$bl" = "$al" ] && [ "$bp" -gt 0 ] || stop "M2 copy counts differ: no RUN"
  echo "-- REPACK $(now)"; touch $D/ran; s=$(date +%s); (umask 0002; G repack -d --geometric=2) >$D/repack.out 2>&1; r=$?; echo "repack rc=$r $(( $(date +%s)-s ))s"; tail -5 $D/repack.out; [ $r = 0 ] || stop "repack rc $r"
  echo "-- AFTER $(now)"; packs | tee $D/packs.after; rd refs.after G for-each-ref --format='%(objectname) %(refname)'
  cmp -s $D/refs.before $D/refs.after && echo "refs: byte-equal ($(wc -l <$D/refs.after) lines)" || { diff $D/refs.before $D/refs.after | head; stop "refs changed"; }
  m1 after; new=$(sudo -n find $H/.git/objects/pack -maxdepth 1 -type f -printf '%f\n' | sort | comm -13 $D/names.before -); echo "new pack-dir files: $(echo "$new" | grep -c .)"
  bad=0; for f in $new; do x=$(sudo -n stat -c '%a %u %g' $H/.git/objects/pack/$f); m=${x%% *}; case " $(awk '{print $2}' $D/m1.before | tr '\n' ' ') " in *" $m "*) ;; *) bad=1;; esac; [ "${x#* }" = "1000 1000" ] || bad=1; case ${m#${m%?}} in 4|5|6|7) ;; *) bad=1;; esac
    sudo -n getfacl -p --omit-header $H/.git/objects/pack/$f | grep -v '^$' | cmp -s - $D/acl.ref || bad=1; echo "  $f: $x acl=$(sudo -n getfacl -p --omit-header $H/.git/objects/pack/$f | grep -v '^$' | cmp -s - $D/acl.ref && echo ref || echo DIFF)"; done
  if [ $bad = 1 ]; then echo "M1: a new file differs from BEFORE: fix to the ref"; for f in $new; do sudo -n chown 1000:1000 $H/.git/objects/pack/$f; sudo -n chmod 0444 $H/.git/objects/pack/$f; sudo -n setfacl --set-file=$D/acl.ref $H/.git/objects/pack/$f; done
    for f in $new; do sudo -n getfacl -p --omit-header $H/.git/objects/pack/$f | grep -v '^$' | cmp -s - $D/acl.ref || stop "M1: $f still differs after the fix"; done; echo "M1: fixed, read again: ref"; else echo "M1: every new file matches the BEFORE line (mode in set, 1000:1000, other-read, ACL == ref)"; fi
  fl after; cmp -s $D/fsck.before $D/fsck.after && echo "M3: dangling list byte-equal ($(wc -l <$D/fsck.after) lines)" || { diff $D/fsck.before $D/fsck.after | head -5; stop "M3: dangling list changed"; }
  touch $D/ok
}

# release everything the hold stopped or froze; safe to run when nothing was held
  rel(){ echo "-- RELEASE $(now)"
  for p in $POSTS; do L "systemctl thaw agi-post@$p.service" >/dev/null 2>&1; done
  L "systemctl start $(for p in $POSTS; do printf 'agi-boxwake@%s.service agi-carry@%s.path ' $p $p; done) agi-lab-carry-in.timer"
  sudo -n systemctl start agi-lt-carry.timer
  echo "lab: $(L "systemctl is-active agi-lab-carry-in.timer $(for p in $POSTS; do printf 'agi-boxwake@%s.service agi-carry@%s.path agi-post@%s.service ' $p $p $p; done)" | sort | uniq -c | tr '\n' ' ')"
  echo "lab freezer: $(L "for p in $POSTS; do systemctl show -p FreezerState --value agi-post@\$p.service; done" | sort | uniq -c | tr '\n' ' ')"
  echo "encryption-town: agi-lt-carry.timer $(systemctl is-active agi-lt-carry.timer)"; }

case ${1:-} in
pre)
  echo "== PRE $(now)"
  v=$(git --version | awk '{print $3}'); echo "host git $v"; dpkg --compare-versions "$v" ge 2.33 || stop "host git < 2.33"
  lv=$(L 'git --version' | awk '{print $3}'); echo "lab git $lv"
  echo "runs on: encryption-town (the NFS server), server-local path $H/.git"
  echo "mounting hosts (export of /data/nas): $(sudo -n exportfs -v | tr -s ' \t\n' ' ' | grep -o '/data/nas [^ ]*')"
  echo "nfs clients now: $(sudo -n ss -tnH state established '( sport = :2049 )' | awk '{print $4}' | cut -d: -f1 | sort -u | tr '\n' ' ')"
  fr=$(df -B1 --output=avail $H | tail -1); pb=$(sudo -n du -sb $H/.git/objects/pack | cut -f1); echo "free=$fr pack_bytes=$pb need=$((2*pb))"; [ $fr -ge $((2*pb)) ] || stop "free < 2x pack bytes"
  echo "borrowers: $(sudo -n grep -rl "$H\|/data/work/agi" /data/nas/lab/data/work/*/.git/objects/info/alternates /data/nas/lab/var/lib/agi/*/g.git/objects/info/alternates 2>/dev/null | wc -l) alternates files name this repo"
  echo "fsck BEFORE (outside the hold, read only):"; G fsck --connectivity-only >$D/fsck.pre 2>&1; echo "fsck.pre rc=$? lines=$(wc -l <$D/fsck.pre)"; head -5 $D/fsck.pre
  timings before ;;
held)   # H2: the held section is bounded; the OUTER always releases, whatever the inner did
  echo "== HELD (bounded: timeout ${HOLD_S:-600} s) $(now)"
  rm -f $D/ran $D/ok $D/restored
  INNER=1 timeout -k 20 ${HOLD_S:-600} sh "$0" held-inner; r=$?
  [ $r != 0 ] && [ -e $D/ran ] && [ ! -e $D/ok ] && [ ! -e $D/restored ] && { echo "outer: killed after the RUN, AFTER not green: restore while still held"; INNER= restore; }
  rel
  case $r in 0) echo "== HELD OK $(now)";; 124|137) echo "STOP $(now): held section passed ${HOLD_S:-600} s = NOT READ, never a pass"; exit 3;; *) echo "STOP $(now): held-inner rc $r"; exit 3;; esac ;;
held-inner)
  L 'test -e /fast/.game-on' && stop "/fast/.game-on present (player)"
  (cd /data/play/shael-rig && sudo -n -u belam ./rig ssh 'loginctl show-session $(loginctl show-seat seat0 -p ActiveSession --value) -p Class --value') | grep -qx greeter || stop "seat0 not at the greeter (player)"
  echo "player: none (no .game-on; seat0 = greeter)"
  sudo -n systemctl stop agi-lt-carry.timer
  for i in $(seq 60); do systemctl is-active agi-lt-carry.service | grep -q -x -E 'inactive|failed' && break; sleep 2; done
  systemctl is-active agi-lt-carry.service | grep -q -x -E 'inactive|failed' || stop "agi-lt-carry.service still running"; echo "held: encryption-town agi-lt-carry.timer stopped, service inactive"
  L "systemctl stop agi-lab-carry-in.timer $(for p in $POSTS; do printf 'agi-carry@%s.path agi-boxwake@%s.service ' $p $p; done)"
  L "for i in \$(seq 90); do systemctl is-active agi-lab-carry-in.service $(for p in $POSTS; do printf 'agi-carry@%s.service ' $p; done) | grep -v -x -E 'inactive|failed' | grep -q . || exit 0; sleep 2; done; exit 1" || stop "lab carry still running"
  echo "held: lab carry-in timer, 8 carry paths, 8 wake loops stopped; $(L "systemctl is-active agi-lab-carry-in.service agi-lab-carry-in.timer $(for p in $POSTS; do printf 'agi-carry@%s.path agi-carry@%s.service agi-boxwake@%s.service ' $p $p $p; done)" | sort | uniq -c | tr '\n' ' ')"
  # H1: nothing respawns a frozen post -- print what could act on a quiet lab post, STOP if one would
  L "systemctl show -p Restart -p WatchdogUSec -p RuntimeMaxUSec agi-post@plasma.service" | tr '\n' ' ' | tee $D/h1.unit; echo
  grep -q 'WatchdogUSec=0' $D/h1.unit && grep -q 'RuntimeMaxUSec=infinity' $D/h1.unit || stop "H1: a lab post unit has a watchdog or runtime cap"
  echo "H1: Restart=always acts only on EXIT; a freeze is not an exit; no watchdog, no runtime cap"
  lt=$(L "systemctl list-timers --all --no-legend | awk '{print \$NF}' | grep -i -E 'agi|keepalive|stall|heal|watch' | grep -v -x agi-lab-carry-in.service"); echo "H1: lab agi/watch timers besides carry-in: ${lt:-none}"; [ -z "$lt" ] || stop "H1: unheld lab timer $lt"
  lk=$(L "systemctl list-units --all --no-legend --plain '*keepalive*' '*stall*' '*heal*' | awk '{print \$1}'"); echo "H1: lab keepalive/stall/heal units: ${lk:-none}"; [ -z "$lk" ] || stop "H1: lab unit $lk"
  er=$(sudo -n -u belam git -C /data/work/agi grep -l -E 'agi-lab exec|rig ssh' HEAD -- extensions/agi/bin extensions/agi/guard ':(exclude)extensions/agi/guard/lab-repack' | wc -l); echo "H1: engine files that reach into the lab, this script's own dir excluded: $er (heal / rc-keepalive act on encryption-town units only; stall_watch acts on nothing)"; [ "$er" = 0 ] || stop "H1: engine reaches the lab"
  echo "idle = claude has no child AND its screen log ~/o unchanged >= 30 s (a turn redraws its spinner there; rc-keepalive's rule)"
  for p in $POSTS; do
    ok=; for i in $(seq 60); do
      L "c=\$(pgrep -f -x 'claude --remote-control $p .*' | head -1); [ -n \"\$c\" ] && [ -z \"\$(pgrep -P \$c)\" ] && [ \$(( \$(date +%s) - \$(stat -c %Y /var/lib/agi/$p/o) )) -ge 30 ]" && { L "systemctl freeze agi-post@$p.service"; ok=1; break; }; sleep 3; done
    [ "$ok" ] || stop "$p never idle in 180 s"; done
  echo "held: posts frozen at idle: $(L "for p in $POSTS; do systemctl show -p FreezerState --value agi-post@\$p.service; done" | sort | uniq -c | tr '\n' ' ')"
  for i in $(seq 30); do g=$(L 'pgrep -c -x git'); [ "${g:-0}" = 0 ] && break; sleep 2; done; [ "${g:-0}" = 0 ] || stop "git still running in the lab: $(L 'pgrep -a -x git')"
  hg=$(sudo -n sh -c "for d in /proc/[0-9]*; do readlink \$d/cwd; done 2>/dev/null" | grep -c "^$H"); echo "git in lab 0; host processes with cwd in the lab repo: $hg"; [ "$hg" = 0 ] || stop "a host process sits in $H"
  h3 freeze
  for p in $(awk '$3!="git=0" || $4!="pack=0" || $5!="unread=0" {print $1}' $D/h3.freeze); do
    echo "H3: $p holds git/pack at the freeze: thaw, wait for idle, freeze again"; L "systemctl thaw agi-post@$p.service"; ok=
    for i in $(seq 40); do sleep 3; L "c=\$(pgrep -f -x 'claude --remote-control $p .*' | head -1); [ -n \"\$c\" ] && [ -z \"\$(pgrep -P \$c)\" ] && [ \$(( \$(date +%s) - \$(stat -c %Y /var/lib/agi/$p/o) )) -ge 30 ]" && { L "systemctl freeze agi-post@$p.service"; ok=1; break; }; done
    [ "$ok" ] || stop "H3: $p not idle again in 120 s"; done
  h3 run; awk '$3!="git=0" || $4!="pack=0" || $5!="unread=0"' $D/h3.run | grep . && stop "H3: a post holds git or a pack at the RUN"
  hp=$(sudo -n sh -c "for x in /proc/[0-9]*; do { cat \$x/maps; ls -l \$x/fd; } 2>/dev/null | grep -c '$H/.git/objects/pack'; done" | awk '{s+=$1} END{print s+0}'); echo "H3 encryption-town: processes' maps+fd naming the lab packs: $hp"; [ "$hp" = 0 ] || stop "H3: a host process holds a lab pack"
  core
  echo "-- inner done $(now)" ;;
rehearse)   # A1_H=<scratch repo owned by uid 1000> A1_D=<scratch log dir>: the core alone, no hold, no lab
  [ "$H" != /data/nas/lab/data/work/agi ] || stop "rehearse refuses the lab repo"; INNER=1; rm -f $D/ran $D/ok $D/restored; core; echo "== REHEARSE OK $(now)" ;;
post)
  echo "== POST $(now)"; timings after
  b=$(med cat-file <$D/tim.before); a=$(med cat-file <$D/tim.after); rb=$(med row6 <$D/tim.before); ra=$(med row6 <$D/tim.after)
  echo "PASS LINE: cat-file median ${b}ms -> ${a}ms (< 1000?) ; row6 median ${rb}ms -> ${ra}ms (< 20000?)"
  [ "$a" -lt 1000 ] && [ "$ra" -lt 20000 ] && echo "A1 PASS" || echo "A1 NOT PASS: packs dropped but time did not = the cause is NOT the packs (B gets worded)" ;;
loose)  # the L-FIRE, (E) (council 3/3 18:05Z 11-17: sp's (E), E1 all-is-one + sp's amend, E2/E3 belam, alive's de-dup):
  # pack EVERY loose object by id into ONE new pack, wait past the lab client's acdirmax, then prune-packed.
  # No pack is deleted, so no hold and no freeze: a lab reader never meets a removed pack (the H3 premise), only a
  # removed loose file, which git re-finds in the new pack (E2: 0 of 14340 short reads; E3: a long-lived reader, 0
  # missing with and without the gap, ONE lab sample each; the mid-file ESTALE case SAMPLED (~2 reads in prune's 47 ms),
  # not stressed). Debris (unreachable loose) is packed too, not pruned: it waits for a K-fire, as A2 stands.
  #   (1) ids = 2-hex dir + 38-hex name ONLY (E1: the raw objects/??/* glob feeds tmp_obj_* and pack-objects
  #       dies rc 128 'expected object ID, got garbage', writing NO pack)
  #   (2) pack-objects' rc read on its own line: rc != 0 = NO prune-packed, ONE alarm naming the bad id(s) from its
  #       stderr, exit 4 (sp M2: one 0-byte or corrupt loose file fails the WHOLE pack, every run, until moved aside;
  #       moving it is a K-fire or owner act, never this one's)
  #   (3) that alarm is DE-DUPLICATED across runs (alive): the bad-id list is kept in $LSTATE; the same list alarms
  #       once, a different one alarms again; a green run clears it
  #   (4) the wait goes BETWEEN pack-objects rc 0 and prune-packed (all-is-one): WAIT_S > the client's acdirmax (60 s:
  #       NFSv3, no ac* option, read on the lab client 11-17); kept although E3 did not show it needed (1 sample)
  echo "== LOOSE $(now)"
  W=${WAIT_S:-75}; LSTATE=${LSTATE:-$D/loose.bad}
  lalarm(){ m="[lab-pack] lab-repack.sh loose $(date -u +%H:%MZ) -> ${TO:-sanctuary-master} (and belam's notice): $1. Path $H. Moving a bad loose file aside is a K-fire or owner act."
    if [ -n "${LALARM:-}" ]; then printf '%s\n' "$m" | sh -c "$LALARM"; return $?; fi
    python3 ${AS:-/opt/agi/bin/alarm_spool.py} append --job lab-pack-loose --to ${TO:-sanctuary-master} --text "$m" --max-lines 500 --spool ${STORES:-/var/lib/agi}/belam/alarm.spool && { [ -x ~/bin/agi-notice ] && ~/bin/agi-notice add "$m" || echo "$m" >> ~/.notice; }; }
  ids=$D/loose.ids
  $SU find $H/.git/objects -mindepth 2 -maxdepth 2 -path '*/objects/[0-9a-f][0-9a-f]/*' -printf '%h%f\n' 2>$D/loose.find.err | sed 's#.*/objects/##' | grep -E '^[0-9a-f]{40}$' | sort > $ids
  [ -s $D/loose.find.err ] && { head -3 $D/loose.find.err; stop "loose ids NOT READ (find stderr)"; }
  n=$(wc -l <$ids); echo "loose ids (2-hex dir + 38-hex name; tmp_* never listed): $n"
  [ "$n" -gt 0 ] || { rm -f $LSTATE; echo "== LOOSE OK $(now): nothing loose"; exit 0; }
  $SU find $H/.git/objects/pack -maxdepth 1 -name '*.pack' -printf '%i %f\n' | sort > $D/loose.packs.before
  t0=$(date +%s); (umask 0002; G pack-objects -q $H/.git/objects/pack/pack < $ids) > $D/loose.pack 2>$D/loose.err
  r=$?
  echo "pack-objects rc=$r new=$(cat $D/loose.pack) stderr=$(wc -c <$D/loose.err)B $(now)"
  if [ $r != 0 ]; then
    grep -o -E '[0-9a-f]{40}' $D/loose.err | sort -u > $D/loose.bad.now
    echo "NO prune-packed. bad id(s) from stderr: $(wc -l <$D/loose.bad.now): $(head -5 $D/loose.bad.now | tr '\n' ' ')"; head -3 $D/loose.err
    if [ -f $LSTATE ] && cmp -s $D/loose.bad.now $LSTATE; then echo "alarm: the same bad-id list already alarmed (de-dup, $LSTATE): none sent"
    else lalarm "L-FIRE FAILED: pack-objects rc $r, NO prune-packed, $n loose kept; bad id(s): $(head -5 $D/loose.bad.now | tr '\n' ' ')$(head -c 200 $D/loose.err | tr '\n' ' ')" && cp $D/loose.bad.now $LSTATE && echo "alarm: sent once (state $LSTATE)" || echo "alarm: DELIVERY FAILED (state not written: the next run alarms again)"; fi
    echo "STOP $(now): pack-objects rc $r"; exit 4; fi
  echo "wait ${W} s (> the lab client's acdirmax 60 s) between pack-objects rc 0 and prune-packed"; sleep $W
  t1=$(date +%s); G prune-packed; rp=$?; echo "prune-packed rc=$rp; gap $((t1-t0)) s (>= ${W}) $(now)"; [ $rp = 0 ] || stop "prune-packed rc $rp"
  la=$($SU find $H/.git/objects -mindepth 2 -maxdepth 2 -path '*/objects/[0-9a-f][0-9a-f]/*' ! -name 'tmp_*' | grep -c -E '/[0-9a-f]{38}$')
  $SU find $H/.git/objects/pack -maxdepth 1 -name '*.pack' -printf '%i %f\n' | sort > $D/loose.packs.after
  kept=$(comm -12 $D/loose.packs.before $D/loose.packs.after | wc -l); before=$(wc -l <$D/loose.packs.before)
  # NOT refs byte-equal: the lab posts are NOT frozen, so their commits move refs during the wait. Instead every
  # listed id must still read after the prune (from the new pack): 'missing' = an object lost = STOP.
  G cat-file --batch-check < $ids > $D/loose.check 2>$D/loose.check.err; rc=$?
  ms=$(grep -c ' missing$' $D/loose.check); ok=$(grep -c -v ' missing$' $D/loose.check)
  echo "AFTER: loose $la (listed $n; a later write may add some), old packs kept by inode $kept of $before, packs now $(wc -l <$D/loose.packs.after); listed ids read back $ok of $n, missing $ms (rc $rc)"
  [ "$kept" = "$before" ] || stop "an old pack is GONE (the L-fire never deletes a pack)"
  [ $rc = 0 ] && [ "$ms" = 0 ] && [ "$ok" = "$n" ] && [ ! -s $D/loose.check.err ] || { head -3 $D/loose.check.err; stop "a listed id does not read back"; }
  rm -f $LSTATE; echo "== LOOSE OK $(now)" ;;
*) echo "usage: lab-repack.sh pre|held|post|rehearse|loose"; exit 2;;
esac
