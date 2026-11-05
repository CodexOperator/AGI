#!/bin/sh
# prayer-captive.t.sh: goal:g7.16.1.11.46.29 falsifier 1 (P0, the owner 11-01: every session starts and ends with a Church Slavonic prayer; a captive reminder if not). agi-pray (engine-wrap.md) + its callers agi-captive, agi-brief, settings.json.
# sh + python3 + jq + git on a STUB HOME, fixture transcripts (Claude Code jsonl shape), a scratch git repo for the card commit; no claude, no network, 0 USD. ROOT=<tree> (or $1). Pieces are EXTRACTED from .geometry, never retyped.
# Rows: h* the head block + its parity with brief.py's _read_faith_ref; s* the start check; o* the v5 out; p* the Stop (idle) check; a* agi-captive's wiring; m* mutants (no check, no fold) that must read RED.
# Honest limits: the claude / pi call path is not run (only the pieces); live falsifier 2 (a fresh post's first session) is read at a land, not here.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};GEO=$R0/.agi/nodes/.geometry;T=$(mktemp -d);trap 'rm -rf "${T:?}"' 0;f=0
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
mkdir -p $T/bin $T/hm $T/r/.agi/nodes/doc
for p in agi-pray agi-captive agi-brief;do sect $p >$T/bin/$p;[ -s $T/bin/$p ]||{ echo "FAIL extract: $p";exit 99;};chmod +x $T/bin/$p;done
sect settings.json >$T/settings.json
ASK='captive: say an Old Slavonic protection prayer before proceeding'
# a transcript: one assistant text per argument, timestamps from argument 1 (unix) upward
tr_(){ o=$1;t0=$2;shift 2;: >$o;i=0;for x in "$@";do python3 -I -c 'import json,sys,datetime;print(json.dumps({"type":"assistant","timestamp":datetime.datetime.fromtimestamp(int(sys.argv[2]),datetime.timezone.utc).isoformat().replace("+00:00","Z"),"message":{"role":"assistant","content":[{"type":"text","text":sys.argv[1]}] if sys.argv[1]!="-" else [{"type":"tool_use","name":"Bash","input":{}}]}}))' "$x" $((t0+i)) >>$o;i=$((i+1));done;}
# pray VERB JSON-FIELDS... : runs agi-pray on a stub HOME; stdout -> $T/out, stderr -> $T/err, rc in $rc
pray(){ v=$1;shift;python3 -I -c 'import json,sys;d={};[d.__setitem__(k,json.loads(v)) for k,v in (a.split("=",1) for a in sys.argv[1:])];print(json.dumps(d))' "$@" |env -i HOME=$T/hm PATH=$T/bin:/usr/bin:/bin AGI_POST=pp ${PB:-$T/bin/agi-pray} $v >$T/out 2>$T/err;rc=$?;}
NOW=$(date +%s);P1='Ѻтче нашъ, иже еси на небесѣхъ,';MOD='Отче наш, иже еси на небесех';JES='Го́споди Иису́се Христе́, Сы́не Бо́жий, поми́луй мя гре́шнаго'
# ---- h: the head
env -i HOME=$T/hm PATH=$T/bin:/usr/bin:/bin $T/bin/agi-pray head $R0 >$T/head 2>$T/err;rc=$?
ok "h1-the-head-prints-the-prayers-first rc $rc (want 0), first line [$(head -1 $T/head)] (want '## THE FOUR PRAYERS'), the Lord's Prayer line present: $(grep -cF "$P1" $T/head) (want >= 1), the ask line: $(grep -c 'first tokens of your first reply' $T/head) (want 1)" '[ $rc = 0 ]&&[ "$(head -1 $T/head)" = "## THE FOUR PRAYERS" ]&&grep -qF "$P1" $T/head&&[ $(grep -c "first tokens of your first reply" $T/head) = 1 ]'
par=$(cd $R0/extensions/agi/bin&&python3 -I -c 'import sys;sys.path.insert(0,".");import brief;from pathlib import Path;print(brief._read_faith_ref(Path(sys.argv[1]))["prayers"].strip())' $R0/.agi 2>/dev/null)
ok "h2-the-head-is-brief.py's-own-prayers-text brief.py _read_faith_ref(root)['prayers'] is $(printf '%s' "$par"|wc -c|tr -d ' ') B and appears whole in the head: $(python3 -I -c 'import sys;print(sys.argv[1] in open(sys.argv[2],encoding="utf-8").read())' "$par" $T/head) (want True)" '[ -n "$par" ]&&python3 -I -c "import sys;sys.exit(0 if sys.argv[1] in open(sys.argv[2],encoding=\"utf-8\").read() else 1)" "$par" $T/head'
ok "h3-agi-brief-runs-the-head-first agi-brief's line 2 starts [$(sed -n 2p $T/bin/agi-brief|cut -c1-60)] (want '{ command -v agi-pray >/dev/null&&agi-pray head ~/t 2>&1;}||')" '[ "$(sed -n 2p $T/bin/agi-brief|cut -c1-60)" = "{ command -v agi-pray >/dev/null&&agi-pray head ~/t 2>&1;}||" ]'
printf '{"source":"compact"}'|env -i HOME=$T/hm PATH=/usr/bin:/bin sh -c "sed -n 2p $T/bin/agi-brief|cut -d';' -f1-2|sh" >$T/out 2>$T/err
ok "h4-agi-brief-without-agi-pray-names-it the head line on a PATH with no agi-pray prints [$(head -1 $T/out|cut -c1-60)] (want the [pray] unread line, nothing from the shell), stderr bytes $(wc -c<$T/err|tr -d ' ') (want 0)" '[ "$(head -1 $T/out)" = "[pray] unread: agi-pray not on PATH: say a Church Slavonic prayer from moral:faith first" ]&&[ ! -s $T/err ]'

# ---- s: the start check
tr_ $T/t0 $NOW 'I will start the work now.';pray captive transcript_path="\"$T/t0\"" session_id='"s0"'
ok "s1-no-prayer-is-refused rc $rc (want 2), stderr [$(cat $T/err)] (want the exact captive text)" '[ $rc = 2 ]&&[ "$(cat $T/err)" = "$ASK" ]'
tr_ $T/t1 $NOW "$P1" 'then the work';pray captive transcript_path="\"$T/t1\"" session_id='"s1"'
ok "s2-a-prayer-passes-and-is-remembered rc $rc (want 0), ~/.prayed/s1: $([ -e $T/hm/.prayed/s1 ]&&echo yes||echo no) (want yes)" '[ $rc = 0 ]&&[ -e $T/hm/.prayed/s1 ]'
pray captive transcript_path="\"$T/t0\"" session_id='"s1"'
ok "s3-never-per-turn a session that prayed once (~/.prayed/s1), now read on a transcript with no prayer: rc $rc (want 0)" '[ $rc = 0 ]'
pray captive transcript_path="\"$T/nope.jsonl\"" session_id='"s9"'
ok "s4-an-unreadable-transcript-passes-with-one-line rc $rc (want 0), [pray] unread lines $(grep -c '^\[pray\] unread' $T/err) (want 1)" '[ $rc = 0 ]&&[ $(grep -c "^\[pray\] unread" $T/err) = 1 ]'
printf 'not json' |env -i HOME=$T/hm PATH=$T/bin:/usr/bin:/bin $T/bin/agi-pray captive >$T/out 2>$T/err;rc=$?
ok "s5-unreadable-hook-input-passes-with-one-line rc $rc (want 0), [pray] lines $(grep -c '^\[pray\] unread' $T/err) (want 1)" '[ $rc = 0 ]&&[ $(grep -c "^\[pray\] unread" $T/err) = 1 ]'
tr_ $T/t2 $NOW "$MOD";pray captive transcript_path="\"$T/t2\"" session_id='"s2"'
ok "s6-the-modern-Lord's-Prayer-passes ('$MOD'): rc $rc (want 0)" '[ $rc = 0 ]'
tr_ $T/t3 $NOW "$JES";pray captive transcript_path="\"$T/t3\"" session_id='"s3"'
ok "s7-the-stressed-Jesus-Prayer-passes rc $rc (want 0)" '[ $rc = 0 ]'
tr_ $T/t4 $NOW 'Our Father, who art in heaven; Gospodi pomiluy';pray captive transcript_path="\"$T/t4\"" session_id='"s4"'
ok "s8-English-or-transliterated-is-not-Church-Slavonic rc $rc (want 2)" '[ $rc = 2 ]'
# marker FIRST (alive 08:04:04Z): a marked session's tool call never opens the transcript (a mode-000 file would read 'unread' if it were opened)
tr_ $T/big $NOW 'no prayer here';chmod 000 $T/big;pray captive transcript_path="\"$T/big\"" session_id='"s1"'
ok "s9-a-marked-session-opens-no-transcript ~/.prayed/s1 set, transcript mode 000: rc $rc (want 0), stderr bytes $(wc -c<$T/err|tr -d ' ') (want 0: no [pray] unread line, so it was never opened)" '[ $rc = 0 ]&&[ ! -s $T/err ]'
pray captive transcript_path="\"$T/t0\"" session_id='"sa"' agent_id='"agent-1"' agent_type='"general-purpose"'
ok "s10-a-subagent-call-is-never-captive (agent_id set, the transcript holds no prayer): rc $rc (want 0), stderr bytes $(wc -c<$T/err|tr -d ' ') (want 0)" '[ $rc = 0 ]&&[ ! -s $T/err ]'
# ---- o: the v5 out, read against the card commit's time in a scratch repo
G="git -C $T/r -c user.name=t -c user.email=t@t -c commit.gpgsign=false";$G init -q;echo c>$T/r/.agi/nodes/doc/card-pp.md;$G add -A;GIT_COMMITTER_DATE="@$NOW +0000" $G commit -qm card;K=$NOW
out(){ pray captive transcript_path="\"$1\"" session_id="\"$2\"" cwd="\"$T/r\"" tool_input='{"command":"touch ~/.fresh; kill $PPID"}';}
tr_ $T/o1 $((K-10)) "$P1";tr_ $T/o1b $((K+5)) 'card written, rotating now';cat $T/o1b>>$T/o1;out $T/o1 o1
ok "o1-the-out-with-no-prayer-since-the-card-commit-is-refused (the session prayed at its start, ~/.prayed/o1 set by this call): rc $rc (want 2), the refusal names the out: $(grep -c 'the out' $T/err) (want 1)" '[ $rc = 2 ]&&[ $(grep -c "the out" $T/err) = 1 ]'
tr_ $T/o2 $((K+5)) "$JES";out $T/o2 o2
ok "o2-the-out-with-a-prayer-since-the-card-commit-passes rc $rc (want 0)" '[ $rc = 0 ]'
tr_ $T/o3 $((K+5)) "rotating: $JES" '-';out $T/o3 o3
ok "o3-step-3-and-step-4-in-two-replies-pass (the prayer in step 3's reply, step 4's reply holds a tool call and no text): rc $rc (want 0)" '[ $rc = 0 ]'
pray captive transcript_path="\"$T/o2\"" session_id='"o4"' cwd='"/nonexistent-dir-x"' tool_input='{"command":"kill $PPID"}'
ok "o4-an-unread-card-commit-passes-with-one-line rc $rc (want 0), [pray] lines $(grep -c '^\[pray\] unread' $T/err) (want 1)" '[ $rc = 0 ]&&[ $(grep -c "^\[pray\] unread" $T/err) = 1 ]'
# ---- p: the Stop (idle) check
tr_ $T/p1 $NOW "$P1" 'Nothing left on my queue; going idle.';pray stop transcript_path="\"$T/p1\""
ok "p1-an-idle-empty-reply-with-no-prayer-is-blocked-once stdout decision [$(jq -r .decision $T/out 2>/dev/null)] (want block), the reason holds the captive text: $(grep -cF "$ASK" $T/out) (want 1)" '[ "$(jq -r .decision $T/out 2>/dev/null)" = block ]&&grep -qF "$ASK" $T/out'
pray stop transcript_path="\"$T/p1\"" stop_hook_active=true
ok "p2-stop-hook-active-never-loops stdout [$(cat $T/out)] (want empty), rc $rc (want 0)" '[ ! -s $T/out ]&&[ $rc = 0 ]'
tr_ $T/p3 $NOW "Nothing left; going idle. $JES";pray stop transcript_path="\"$T/p3\""
ok "p3-an-idle-reply-that-prays-passes stdout [$(cat $T/out)] (want empty)" '[ ! -s $T/out ]'
tr_ $T/p4 $NOW 'Landed L340; next I read the gate.';pray stop transcript_path="\"$T/p4\""
ok "p4-a-working-reply-is-not-asked (never per turn) stdout [$(cat $T/out)] (want empty)" '[ ! -s $T/out ]'
tr_ $T/p5 $NOW "$P1" "Nothing left; going idle. $JES" 'mail read; staying idle.';pray stop transcript_path="\"$T/p5\"" session_id='"p5"'
ok "p5-an-earlier-idle-reply-that-prayed-ends-the-asking (sp 07:59:53Z: never per turn) a later 'staying idle' reply with no prayer: stdout [$(cat $T/out)] (want empty)" '[ ! -s $T/out ]'
tr_ $T/p6 $NOW "$P1" 'Nothing left; going idle.';pray stop transcript_path="\"$T/p6\"" session_id='"p6"';b1=$(jq -r .decision $T/out 2>/dev/null)
tr_ $T/p6 $NOW "$P1" 'Nothing left; going idle.' 'Still nothing to do; staying idle.';pray stop transcript_path="\"$T/p6\"" session_id='"p6"'
ok "p6-the-stop-check-asks-once-per-session the first idle stop: [$b1] (want block), ~/.prayed/p6.end $([ -e $T/hm/.prayed/p6.end ]&&echo yes||echo no) (want yes); a second idle stop, no prayer: stdout [$(cat $T/out)] (want empty)" '[ "$b1" = block ]&&[ -e $T/hm/.prayed/p6.end ]&&[ ! -s $T/out ]'
# ---- a: agi-captive's wiring
cap(){ printf '{"tool_input":{"command":"ls"},"transcript_path":"%s","session_id":"%s"}' "$1" "$2"|env -i HOME=$T/hm PATH=$3/usr/bin:/bin sh $T/bin/agi-captive >$T/out 2>$T/err;rc=$?;}
cap $T/t0 a1 $T/bin:
ok "a1-agi-captive-refuses-through-agi-pray no prayer, no fill window: rc $rc (want 2), stderr [$(cat $T/err)]" '[ $rc = 2 ]&&[ "$(cat $T/err)" = "$ASK" ]'
cap $T/t1 a2 $T/bin:
ok "a2-agi-captive-passes-after-a-prayer rc $rc (want 0), stderr bytes $(wc -c<$T/err|tr -d ' ') (want 0)" '[ $rc = 0 ]&&[ ! -s $T/err ]'
mkdir -p $T/nopray;cp $T/bin/agi-captive $T/nopray/;cap $T/t0 a3 ""
ok "a3-agi-pray-absent-passes-with-one-line (never a lock) rc $rc (want 0), [pray] lines $(grep -c '^\[pray\] unread: agi-pray not on PATH' $T/err) (want 1)" '[ $rc = 0 ]&&[ $(grep -c "^\[pray\] unread: agi-pray not on PATH" $T/err) = 1 ]'
printf '#!/bin/sh\ncat >/dev/null;exit 1\n'>$T/crash;chmod +x $T/crash;mkdir -p $T/cb;cp $T/crash $T/cb/agi-pray;cap $T/t0 a4 $T/cb:
ok "a4-a-crashing-agi-pray-is-not-a-lock (rc 1 is not a refusal) rc $rc (want 0)" '[ $rc = 0 ]'
ok "a5-settings-wires-the-stop-check Stop hooks [$(jq -r '[.hooks.Stop[].hooks[].command]|join(",")' $T/settings.json)] holds agi-pray stop" 'jq -e "[.hooks.Stop[].hooks[].command]|index(\"agi-pray stop\")" $T/settings.json>/dev/null'
# ---- m: mutants of the REAL piece, each must read RED on its row
sed 's/print(ASK,file=sys.stderr);sys.exit(2)/pass/' $T/bin/agi-pray>$T/m1;chmod +x $T/m1;cmp -s $T/bin/agi-pray $T/m1&&{ echo "FAIL mutant m1 changed nothing";exit 99;}
PB=$T/m1 pray captive transcript_path="\"$T/t0\"" session_id='"m1"'
ok "m1-without-the-check-s1-reads-RED rc $rc (want 0 = the mutant lets a prayerless session through, so s1 can fail)" '[ $rc = 0 ]'
python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a="def fold(s):\n";i=s.index(a)+len(a);open(sys.argv[2],"w",encoding="utf-8").write(s[:i]+"    return s.casefold()\n"+s[i:])' $T/bin/agi-pray $T/m2;chmod +x $T/m2
PB=$T/m2 pray captive transcript_path="\"$T/t2\"" session_id='"m2"'
ok "m2-without-the-fold-the-modern-Otche-row-reads-RED rc $rc (want 2 = the mutant refuses '$MOD', so s6 can fail)" '[ $rc = 2 ]'
sed -e '/^        if e and os.path.exists(e):return$/d' -e 's/if not idle(last) or any(idle(t) and prays(t) for _,t in T\[:-1\]):return/if not idle(last):return/' $T/bin/agi-pray>$T/m3;[ $(diff $T/bin/agi-pray $T/m3|grep -c '^<') = 2 ]||{ echo "FAIL mutant m3 cut $(diff $T/bin/agi-pray $T/m3|grep -c '^<') line(s), want 2";exit 99;};chmod +x $T/m3;cmp -s $T/bin/agi-pray $T/m3&&{ echo "FAIL mutant m3 changed nothing";exit 99;}
rm -f $T/hm/.prayed/p6.end;PB=$T/m3 pray stop transcript_path="\"$T/p5\"" session_id='"m3"';m3a=$(jq -r .decision $T/out 2>/dev/null);PB=$T/m3 pray stop transcript_path="\"$T/p6\"" session_id='"p6"';m3b=$(jq -r .decision $T/out 2>/dev/null)
ok "m3-without-the-once-per-session-read-p5-and-p6-read-RED the mutant blocks p5's later idle [$m3a] and p6's second idle [$m3b] (want block, block)" '[ "$m3a" = block ]&&[ "$m3b" = block ]'
python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a="    if marked and not out:return\n    T=tr()\n";assert a in s;open(sys.argv[2],"w",encoding="utf-8").write(s.replace(a,"    T=tr()\n    if marked and not out:return\n"))' $T/bin/agi-pray $T/m4;chmod +x $T/m4
PB=$T/m4 pray captive transcript_path="\"$T/big\"" session_id='"s1"'
ok "m4-the-transcript-read-before-the-marker-reads-RED on s9's input the mutant opens the mode-000 transcript: [pray] unread lines $(grep -c '^\[pray\] unread' $T/err) (want 1), so s9 can fail" '[ $(grep -c "^\[pray\] unread" $T/err) = 1 ]'
chmod 600 $T/big
echo "prayer-captive: $f FAIL";exit $f
