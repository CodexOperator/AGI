#!/bin/sh
# prayer-captive.t.sh: goal:g7.16.1.11.46.29 falsifier 1 (P0, the owner 11-01: every session starts and ends with a Church Slavonic prayer; a captive reminder if not). agi-pray (engine-wrap.md) + its callers agi-captive, agi-brief, settings.json.
# sh + python3 + jq + git on a STUB HOME, fixture transcripts (Claude Code jsonl shape), a scratch git repo for the card commit; no claude, no network, 0 USD. ROOT=<tree> (or $1). Pieces are EXTRACTED from .geometry, never retyped.
# Rows: h* the head block + its parity with brief.py's _read_faith_ref; s* the start check; d* goal .46.29.1's real transcript shapes (a prayer beside a tool call DROPPED or written LATE) and the Stop resume; o* the v5 out (c* reads that only NAME it); p* the Stop (idle) check; a* agi-captive's wiring; m* mutants (no check, no fold, no exemptions, no resume, a refusal-gated resume, no heredoc skip, no open-quote fallback, segment-start only, zones exempt whatever consumes them, no command-substitution clause, no backtick boundary, no process-substitution clause, no write-then-run clause, no target-path clause, pipes checked against RUN only, next pipe segment only, the printer's own segment's writes only, no enclosing-segment clause, no $( registration, segment ends at a substitution, no SAFE filter's own write) that must read RED.
# Honest limits: the claude / pi call path is not run (only the pieces); live falsifier 2 (a fresh post's first session) is read at a land, not here.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};GEO=$R0/.agi/nodes/.geometry;T=$(mktemp -d);trap 'rm -rf "${T:?}"' 0;f=0
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
mkdir -p $T/bin $T/hm $T/r/.agi/nodes/doc
for p in agi-pray agi-captive agi-brief;do sect $p >$T/bin/$p;[ -s $T/bin/$p ]||{ echo "FAIL extract: $p";exit 99;};chmod +x $T/bin/$p;done
sect settings.json >$T/settings.json
ASK="captive: say an Old Slavonic protection prayer before proceeding: as your reply's LAST text, no tool call after it (that ENDS the turn: a pause until your next prompt, not a hang); a prayer beside a call is read again at the next call"
GO='prayed: the captive is released; continue your work'
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
# ---- d: goal .46.29.1, the shapes a live transcript has (aio 11:03:07Z: a prayer said beside a tool_use is DROPPED; sp 11:49:51Z: or written LATE)
js(){ python3 -I -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1";}
tr_ $T/d1 $NOW '-';pray captive transcript_path="\"$T/d1\"" session_id='"d1"'
ok "d1-a-prayer-said-beside-a-tool-call-and-absent-from-the-jsonl-is-refused rc $rc (want 2), stderr is the ASK: $([ "$(cat $T/err)" = "$ASK" ]&&echo yes||echo no), it names the reply-final form: $(grep -c "reply's LAST text, no tool call after it" $T/err) (want 1)" '[ $rc = 2 ]&&[ "$(cat $T/err)" = "$ASK" ]&&grep -q "reply.s LAST text, no tool call after it" $T/err' 
pray stop transcript_path="\"$T/d1\"" session_id='"d1"' last_assistant_message="$(js "$JES")"
ok "d2-a-reply-final-prayer-resumes-the-post (the Stop hook's OUTPUT is the next prompt, no outside input) decision [$(jq -r .decision $T/out 2>/dev/null)] (want block), reason [$(jq -r .reason $T/out 2>/dev/null)] (want '$GO'), ~/.prayed/d1 $([ -e $T/hm/.prayed/d1 ]&&echo yes||echo no) (want yes)" '[ "$(jq -r .decision $T/out 2>/dev/null)" = block ]&&[ "$(jq -r .reason $T/out 2>/dev/null)" = "$GO" ]&&[ -e $T/hm/.prayed/d1 ]' 
pray captive transcript_path="\"$T/d1\"" session_id='"d1"'
ok "d3-then-released (the jsonl still holds no prayer): rc $rc (want 0)" '[ $rc = 0 ]'
pray stop transcript_path="\"$T/d1\"" session_id='"d1"' last_assistant_message="$(js "$JES")"
ok "d4-the-resume-fires-once (a marked session's next prayer-final Stop): stdout [$(cat $T/out)] (want empty)" '[ ! -s $T/out ]'
tr_ $T/d5 $NOW 'work';pray stop transcript_path="\"$T/d5\"" session_id='"d5"' last_assistant_message="$(js "work done. $JES")"
d5o=$(jq -r .reason $T/out 2>/dev/null);ok "d5-a-NEVER-refused-prayer-final-first-reply-is-resumed (sp 12:03:49Z: the post that obeyed the interim line) reason [$d5o] (want '$GO'), ~/.prayed/d5 $([ -e $T/hm/.prayed/d5 ]&&echo yes||echo no) (want yes)" '[ "$d5o" = "$GO" ]&&[ -e $T/hm/.prayed/d5 ]' 
tr_ $T/d6 $NOW '-';pray captive transcript_path="\"$T/d6\"" session_id='"d6"';pray stop transcript_path="\"$T/d6\"" session_id='"d6"' last_assistant_message="$(js 'Landed L340; next I read the gate.')"
ok "d6-a-refused-session-whose-reply-holds-no-prayer-is-not-resumed stdout [$(cat $T/out)] (want empty), ~/.prayed/d6 $([ -e $T/hm/.prayed/d6 ]&&echo yes||echo no) (want no)" '[ ! -s $T/out ]&&[ ! -e $T/hm/.prayed/d6 ]' 
tr_ $T/l1 $NOW '-';pray captive transcript_path="\"$T/l1\"" session_id='"l1"';l1a=$rc
tr_ $T/l1 $NOW "$JES" '-';pray captive transcript_path="\"$T/l1\"" session_id='"l1"'
ok "d7-the-LAG-a-kept-prayer-written-after-the-check-releases-at-the-next-call (no new reply) first call rc $l1a (want 2), the same prayer now in the jsonl: rc $rc (want 0)" '[ $l1a = 2 ]&&[ $rc = 0 ]'
# ---- o: the v5 out, read against the card commit's time in a scratch repo
G="git -C $T/r -c user.name=t -c user.email=t@t -c commit.gpgsign=false";$G init -q;echo c>$T/r/.agi/nodes/doc/card-pp.md;$G add -A;GIT_COMMITTER_DATE="@$NOW +0000" $G commit -qm card;K=$NOW
out(){ pray captive transcript_path="\"$1\"" session_id="\"$2\"" cwd="\"$T/r\"" tool_input='{"command":"touch ~/.fresh; kill $PPID"}';}
tr_ $T/o1 $((K-10)) "$P1";tr_ $T/o1b $((K+5)) 'card written, rotating now';cat $T/o1b>>$T/o1;out $T/o1 o1
ok "o1-the-out-with-no-prayer-since-the-card-commit-is-refused (the session prayed at its start, ~/.prayed/o1 set by this call): rc $rc (want 2), the refusal names the out: $(grep -c 'the out' $T/err) (want 1)" '[ $rc = 2 ]&&[ $(grep -c "the out" $T/err) = 1 ]'
tr_ $T/o2 $((K+5)) "$JES";out $T/o2 o2
ok "o2-the-out-with-a-prayer-since-the-card-commit-passes rc $rc (want 0)" '[ $rc = 0 ]'
tr_ $T/o3 $((K+5)) "rotating: $JES" '-';out $T/o3 o3
ok "o3-step-3-and-step-4-in-two-replies-pass (the prayer in step 3's reply, step 4's reply holds a tool call and no text): rc $rc (want 0)" '[ $rc = 0 ]'
# o5: EVERY spelling of the out (alive 08:13:28Z item 3), a marked session whose newest text since the card commit holds no prayer -> each refused
SP='kill "$PPID"|kill ${PPID}|kill -s TERM $PPID|kill -- $PPID|touch "$HOME/.fresh" \&\& kill "$PPID"|kill -TERM "${PPID}"';old=0;new=0;nsp=0
sed 's/out=isout(c)$/out=re.search(r"touch +(~|\\$HOME)\/\\.fresh|kill +(-[A-Z0-9]+ +)?\\$PPID",c)/' $T/bin/agi-pray>$T/m5;chmod +x $T/m5;cmp -s $T/bin/agi-pray $T/m5&&{ echo "FAIL mutant m5 changed nothing";exit 99;}
IFS='|';for c in $SP;do unset IFS;c=$(printf '%s' "$c"|sed 's/\\&/\&/g');nsp=$((nsp+1));j=$(python3 -I -c 'import json,sys;print(json.dumps({"command":sys.argv[1]}))' "$c")
pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";[ $rc = 2 ]&&new=$((new+1))
PB=$T/m5 pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";[ $rc = 2 ]&&old=$((old+1));IFS='|';done;unset IFS
ok "o5-every-spelling-of-the-out-is-checked $new of $nsp spellings refused (want $nsp: quoted / braced \$PPID, kill -s SIG / -SIG / --, a quoted \$HOME/.fresh)" '[ $nsp = 6 ]&&[ $new = $nsp ]'
ok "m5-the-old-two-spelling-match-reads-RED the old regex refuses $old of $nsp (want 0: it never ran the out check on them)" '[ $old = 0 ]'
# c: reads that only NAME the out (aio 11:03:07Z: one was refused live) on a marked session whose newest text since the card commit holds no prayer -> each passes; o6: alive's 10:53:22Z kill -n N and a TAB -> refused
NM='grep -n "kill $PPID" skills/agi-rotate/SKILL.md|echo kill $PPID later|ls # kill $PPID|echo '"'"'touch ~/.fresh'"'"'|git log -S "kill $PPID"';nn=0;np=0;nq=0;mp=0
for c in "$(printf 'kill -n 15 $PPID')" "$(printf 'kill\t$PPID')";do j=$(python3 -I -c 'import json,sys;print(json.dumps({"command":sys.argv[1]}))' "$c");pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";[ $rc = 2 ]&&np=$((np+1));done
ok "o6-kill-n-and-a-TAB-are-the-out $np of 2 refused (want 2)" '[ $np = 2 ]'
sed 's/out=isout(c)$/out=bool(OUT.search(c))/' $T/bin/agi-pray>$T/m6;chmod +x $T/m6;cmp -s $T/bin/agi-pray $T/m6&&{ echo "FAIL mutant m6 changed nothing";exit 99;}
IFS='|';for c in $NM;do unset IFS;nn=$((nn+1));j=$(python3 -I -c 'import json,sys;print(json.dumps({"command":sys.argv[1]}))' "$c")
pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";[ $rc = 0 ]&&[ ! -s $T/err ]&&nq=$((nq+1))
PB=$T/m6 pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";[ $rc = 2 ]&&mp=$((mp+1));IFS='|';done;unset IFS
ok "c1-a-read-that-only-names-the-out-is-not-the-out $nq of $nn passed with no line (want $nn: a grep pattern, an echo, a comment, a quoted touch, a git log -S)" '[ $nn = 5 ]&&[ $nq = $nn ]'
ok "m6-without-the-exemptions-c1-reads-RED the bare L358-style whole search refuses $mp of $nn (want $nn)" '[ $mp = $nn ]'
# c2-c4 + o7 (aio 11:59:57Z RETURN: no command the L358 matcher refuses may pass; alive 11:59:58Z: a heredoc body line is not the out): rq CMD [AGI-PRAY] -> rc of the out check on the marked session o1
rq(){ j=$(python3 -I -c 'import json,sys;print(json.dumps({"command":sys.argv[1].encode().decode("unicode_escape")}))' "$1");PB=${2:-} pray captive transcript_path="\"$T/o1\"" session_id='"o1"' cwd="\"$T/r\"" tool_input="$j";}
H1="cat > c.md <<EOF\\nsp's card line\\nEOF\\ntouch ~/.fresh && kill \$PPID";H2="echo it's; kill \$PPID";H3="cat > f <<EOF\\nthen touch ~/.fresh && kill \$PPID\\nkill \$PPID\\nEOF"
python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a="        elif c.startswith(\"<<\",i)";b="H=[];continue\n";i=s.index(a);k=s.index(b,i)+len(b);assert s.count(a)==1;open(sys.argv[2],"w",encoding="utf-8").write(s[:i]+s[k:])' $T/bin/agi-pray $T/m8
sed 's/    return None if q else (z,o,b,sp,ps,red,tg,E)$/    return (z,o,b,sp,ps,red,tg,E)/' $T/bin/agi-pray>$T/m9;sed -e 's/    return None if q else (z,o,b,sp,ps,red,tg,E)$/    return (z,o,b,sp,ps,red,tg,E)/' -e 's/^        if k==2:continue$/        if k:continue/' $T/m8>$T/m10;chmod +x $T/m8 $T/m9 $T/m10
for m in m8 m9;do cmp -s $T/bin/agi-pray $T/$m&&{ echo "FAIL mutant $m changed nothing";exit 99;};done;cmp -s $T/m8 $T/m10&&{ echo "FAIL mutant m10 changed nothing";exit 99;}
rq "$H1";c2=$rc;rq "$H1" $T/m10;c2m=$rc;rq "$H2";c3=$rc;rq "$H2" $T/m9;c3m=$rc;rq "$H3";c4=$rc;c4e=$(wc -c<$T/err|tr -d ' ');rq "$H3" $T/m8;c4m=$rc
ok "c2-a-heredoc-body-with-one-apostrophe-then-the-out-is-refused rc $c2 (want 2, as the L358 search refuses it)" '[ $c2 = 2 ]'
ok "m10-without-the-heredoc-skip-the-open-quote-fallback-and-the-consumer-check-c2-reads-RED rc $c2m (want 0: the fail-open shape of 3c29d5c717)" '[ $c2m = 0 ]'
ok "c3-an-unclosed-quote-is-searched-whole (fail closed) rc $c3 (want 2); m9-without-the-fallback rc $c3m (want 0 = RED)" '[ $c3 = 2 ]&&[ $c3m = 0 ]'
ok "c4-a-heredoc-body-line-naming-the-out-is-not-the-out rc $c4 (want 0), stderr bytes $c4e (want 0); m8-without-the-heredoc-skip rc $c4m (want 2 = RED)" '[ $c4 = 0 ]&&[ $c4e = 0 ]&&[ $c4m = 2 ]'
o7=0;for c in '{ kill $PPID; }' 'if true; then kill $PPID; fi';do rq "$c";[ $rc = 2 ]&&o7=$((o7+1));done
ok "o7-the-out-inside-braces-or-then-is-the-out $o7 of 2 refused (want 2)" '[ $o7 = 2 ]'
# o8 (aio 12:01:27Z, alive 12:02:31Z: regressions against L358 are RED, not next touches): an unknown leading word before the out is the out; m11 = segment-start only (the 3c29d5c717 shape) reads RED on them
python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a="        return True\n    return False\n";assert s.count(a)==1;open(sys.argv[2],"w",encoding="utf-8").write(s.replace(a,"        if not c[max(x for x in b if x<=i):i].strip():return True\n    return False\n"))' $T/bin/agi-pray $T/m11;chmod +x $T/m11
o8=0;m11=0;n8=0;for c in '{ kill $PPID; }' 'if true; then kill $PPID; fi' '! kill $PPID' 'sudo kill $PPID' 'nohup kill $PPID' 'timeout 5 kill $PPID' 'env kill $PPID' 'while :; do kill $PPID; done' 'time kill $PPID' 'if false; then :; else kill $PPID; fi';do n8=$((n8+1));rq "$c";[ $rc = 2 ]&&o8=$((o8+1));rq "$c" $T/m11;[ $rc = 0 ]&&m11=$((m11+1));done
ok "o8-no-command-the-L358-search-refuses-passes $o8 of $n8 refused (want $n8: a brace group, then, !, sudo, nohup, timeout, env, do, time, else)" '[ $n8 = 10 ]&&[ $o8 = $n8 ]'
ok "m11-segment-start-only-reads-RED-on-o8 the mutant passes $m11 of $n8 (want $n8)" '[ $m11 = $n8 ]'
# c5/c6 + m13 (aio 12:09:41Z RETURN on RE-CUT 1: a quoted span or heredoc body handed to a shell RUNS): exempt only when its consumer is a printer (SHOW), awk/sed out of SHOW, a printer piped to a shell loses it, $( ) / backticks run
sed 's/^        if k==2:continue$/        if k:continue/' $T/bin/agi-pray>$T/m13;chmod +x $T/m13;cmp -s $T/bin/agi-pray $T/m13&&{ echo "FAIL mutant m13 changed nothing";exit 99;}
n5=0;o5=0;m13=0;IFS='|';for c in 'sh -c "touch ~/.fresh; kill $PPID"' "bash -c 'kill \$PPID'" 'eval "kill $PPID"' "sh <<'EOF'\\nkill \$PPID\\nEOF" 'bash <<EOF\ntouch ~/.fresh && kill $PPID\nEOF' 'env sh -c "kill $PPID"' "timeout 5 sh -c 'kill \$PPID'" "awk 'BEGIN{system(\"kill \$PPID\")}'" "sed -n '1e kill \$PPID' f";do unset IFS;n5=$((n5+1));rq "$c";[ $rc = 2 ]&&o5=$((o5+1));rq "$c" $T/m13;[ $rc = 0 ]&&m13=$((m13+1));IFS='|';done;unset IFS
ok "c5-a-quoted-span-or-heredoc-a-shell-runs-is-the-out $o5 of $n5 refused (want $n5: sh -c, bash -c, eval, sh <<'EOF', bash <<EOF, env sh -c, timeout sh -c, awk system(), sed e)" '[ $n5 = 9 ]&&[ $o5 = $n5 ]'
ok "m13-zones-exempt-whatever-consumes-them-reads-RED-on-c5 the mutant passes $m13 of $n5 (want $n5)" '[ $m13 = $n5 ]'
x5=0;IFS='|';for c in 'echo kill $PPID \| sh' 'echo "$(kill $PPID)"' 'echo "`kill $PPID`"' 'cat > f <<EOF\n$(kill $PPID)\nEOF' 'grep x f \| xargs kill $PPID';do unset IFS;c=$(printf '%s' "$c"|sed 's/\\|/|/g');rq "$c";[ $rc = 2 ]&&x5=$((x5+1));IFS='|';done;unset IFS
ok "c6-a-printer-piped-to-a-shell-and-a-command-substitution-are-the-out $x5 of 5 refused (want 5)" '[ $x5 = 5 ]'
y5=0;for c in "git log -S'kill \$PPID'" "cat > f <<'EOF'\\n\$(kill \$PPID)\\nEOF" 'echo kill $PPID || true' 'grep "kill $PPID" f | wc -l' 'printf "%s\\\\n" kill $PPID';do rq "$c";[ $rc = 0 ]&&[ ! -s $T/err ]&&y5=$((y5+1));done
ok "c7-more-reads-that-only-name-the-out-pass $y5 of 5 (want 5: git log -S'...', a QUOTED heredoc holding \$( ), || true, grep | wc, printf)" '[ $y5 = 5 ]'
# c8 + m14 (sp 12:11:20Z clause (4): a command substitution runs whatever consumes it; a single-quoted span expands nothing)
sed '/^                if x3:z\[qs:i+1\]=\[3\]\*(i+1-qs)$/d' $T/bin/agi-pray>$T/m14;chmod +x $T/m14;cmp -s $T/bin/agi-pray $T/m14&&{ echo "FAIL mutant m14 changed nothing";exit 99;}
x8=0;m14=0;for c in 'echo "$(kill $PPID)"' 'echo "`kill $PPID`"';do rq "$c";[ $rc = 2 ]&&x8=$((x8+1));rq "$c" $T/m14;[ $rc = 0 ]&&m14=$((m14+1));done
z8=0;for c in 'echo `kill $PPID`' 'X="$(touch ~/.fresh)"';do rq "$c";[ $rc = 2 ]&&z8=$((z8+1));done;rq "echo '\$(kill \$PPID)'";q8=$rc
ok "c8-a-command-substitution-runs-whatever-consumes-it double-quoted $x8 of 2 + bare backtick / an assignment $z8 of 2 refused (want 2, 2); a single-quoted \$( ) rc $q8 (want 0: it expands nothing)" '[ $x8 = 2 ]&&[ $z8 = 2 ]&&[ $q8 = 0 ]'
ok "m14-a-printer's-double-quoted-span-exempt-without-the-clause-reads-RED-on-c8 the mutant passes $m14 of 2 (want 2)" '[ $m14 = 2 ]'
# c9-c11 + m15-m17 (aio 12:15:03Z bare backticks under a printer; sp 12:15:41Z (3') process substitution into a RUN word, (5) a script written and run in ONE command): each refused, each mutant RED
mu(){ python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a=sys.argv[3];assert s.count(a)==1,a;open(sys.argv[2],"w",encoding="utf-8").write(s.replace(a,sys.argv[4]))' $T/bin/agi-pray $T/$1 "$2" "$3";chmod +x $T/$1;}
mu m15 ';&|()`\n' ';&|()\n';mu m16 ' and (s0 not in ps or ok(ps[s0]))' '';mu m17 ' and not ((tt or any(s in red for s in Q)) and any(lead(c,x,b,E)[0] in RUN or lead(c,x,b,E)[0] not in SHOW and names(c,x,E,tt) for x in b if x>s0 and x not in P))' ''
cl(){ n=0;m=0;M=$1;shift;for c in "$@";do rq "$c";[ $rc = 2 ]&&n=$((n+1));rq "$c" $T/$M;[ $rc = 0 ]&&m=$((m+1));done;}
cl m15 'echo `kill $PPID`' 'cat `kill $PPID`' 'grep -c x `kill $PPID`' 'printf %s `kill $PPID`';n9=$n;m15=$m
ok "c9-bare-backticks-under-a-printer-run $n9 of 4 refused (want 4); m15-without-the-backtick-boundary passes $m15 of 4 (want 4 = RED)" '[ $n9 = 4 ]&&[ $m15 = 4 ]'
cl m16 'sh <(echo kill $PPID)' "source <(printf 'touch ~/.fresh')" '. <(echo touch ~/.fresh)';n10=$n;m16=$m
ok "c10-a-printer-in-a-process-substitution-fed-to-a-RUN-word $n10 of 3 refused (want 3); m16-without-the-clause passes $m16 of 3 (want 3 = RED)" '[ $n10 = 3 ]&&[ $m16 = 3 ]'
cl m17 'echo kill $PPID > x.sh; sh x.sh' 'echo kill $PPID >> x.sh && bash x.sh' 'echo kill $PPID | tee x.sh; sh x.sh';n11=$n;m17=$m
ok "c11-a-script-written-and-run-in-one-command $n11 of 3 refused (want 3); m17-without-the-clause passes $m17 of 3 (want 3 = RED)" '[ $n11 = 3 ]&&[ $m17 = 3 ]'
y11=0;for c in 'echo kill $PPID > notes.md' 'diff <(echo kill $PPID) f';do rq "$c";[ $rc = 0 ]&&[ ! -s $T/err ]&&y11=$((y11+1));done
ok "c12-a-redirect-with-no-later-RUN-word-and-a-process-substitution-fed-to-a-printer-still-pass $y11 of 2 (want 2)" '[ $y11 = 2 ]'
# c13 + m18/m19 (alive 13:28:47Z next touch): the written file run BY PATH, and a printer piped into an executor that is no plain filter (SAFE = SHOW + tee cut tr uniq nl fold column)
mu m18 ' or lead(c,x,b,E)[0] not in SHOW and names(c,x,E,tt)' '';mu m19 'not piped(c,P,b,E)' 'not (len(P)>1 and lead(c,P[1],b,E)[0] in RUN)'
cl m18 'echo kill $PPID > x.sh; chmod +x x.sh; ./x.sh' 'echo kill $PPID > x.sh; chmod +x x.sh; exec ./x.sh' 'echo kill $PPID > x.sh; chmod +x x.sh; nohup ./x.sh' 'cat > x.sh <<EOF\nkill $PPID\nEOF\nchmod +x x.sh && ./x.sh' 'echo kill $PPID | tee /tmp/r.sh; /tmp/r.sh';n13=$n;m18=$m
ok "c13-a-written-file-run-by-path $n13 of 5 refused (want 5: ./x.sh, exec ./x.sh, nohup ./x.sh, a heredoc then chmod && ./x.sh, tee PATH; PATH); m18-without-the-target-path-clause passes $m18 of 5 (want 5 = RED)" '[ $n13 = 5 ]&&[ $m18 = 5 ]'
cl m19 'echo kill $PPID | busybox sh' 'echo kill $PPID | python3 -c "import os,sys;os.system(sys.stdin.read())"' 'echo kill $PPID | at now';n14=$n;m19=$m
ok "c14-a-printer-piped-into-an-executor $n14 of 3 refused (want 3: busybox sh, python3 -c os.system, at now); m19-pipes-checked-against-RUN-only passes $m19 of 3 (want 3 = RED)" '[ $n14 = 3 ]&&[ $m19 = 3 ]'
y14=0;for c in "cat > a.md <<'EOF'\nx\nEOF\ncat > b.md <<'EOF'\nkill \$PPID\nEOF\npython3 -c 'print(1)'" 'grep "kill $PPID" f | sort | uniq -c' 'echo kill $PPID | cut -c1-4' 'echo kill $PPID > n.md; cat n.md';do rq "$c";[ $rc = 0 ]&&[ ! -s $T/err ]&&y14=$((y14+1));done
ok "c15-filters-and-a-written-file-never-run-still-pass $y14 of 4 (want 4: alive's own two-heredoc probe, grep | sort | uniq, | cut, > n.md; cat n.md)" '[ $y14 = 4 ]'
# c16 + m20 (alive 17:42:51Z): a pipe CHAIN, every later segment must be SAFE; m20 reads only the next segment
mu m20 '    while sp.get(e)=="|" and' '    if sp.get(e)=="|" and'
cl m20 'echo kill $PPID | head -1 | sh' "printf 'kill \$PPID' | sort | bash" 'echo kill $PPID | cut -c1-99 | xargs -I{} sh -c {}' 'echo kill $PPID | tr a a | busybox sh';n16=$n;m20=$m
ok "c16-a-SAFE-filter-between-the-printer-and-an-executor-keeps-nothing $n16 of 4 refused (want 4); m20-next-segment-only passes $m20 of 4 (want 4 = RED)" '[ $n16 = 4 ]&&[ $m20 = 4 ]'
y16=0;for c in 'grep "kill $PPID" f | sort | uniq | wc -l' 'grep "kill $PPID" f | head';do rq "$c";[ $rc = 0 ]&&[ ! -s $T/err ]&&y16=$((y16+1));done
ok "c17-an-all-SAFE-chain-still-passes $y16 of 2 (want 2: grep | sort | uniq | wc, grep | head)" '[ $y16 = 2 ]'
# c18-c22 + m21-m24 (goal .46.29.1 next touch: alive 17:57:11Z (1) a printer's targets are every file its PIPELINE writes, (2) a printer in an unquoted $( ) / backticks / <( ) passes only when the ENCLOSING segment would; sp 19:48:23Z (3) a SAFE filter's own write, a target named anywhere in a later segment)
mu m21 ';Q=P' ';Q=P[:1]';mu m22 '"$<>"' '"<>"';mu m23 'dep[x]<dep[s] or dep[x]==dep[s] and x not in cl' 'True';mu m24 '    if v not in ("sort","uniq"):return []' '    return []'
cl m21 'echo kill $PPID | head -1 > x.sh; sh x.sh' 'echo kill $PPID | sort >> x.sh && bash x.sh' 'echo kill $PPID | head -1 | tee x.sh; sh x.sh' 'echo kill $PPID | cut -c1-99 > /tmp/r.sh; /tmp/r.sh';n18=$n;m21=$m
ok "c18-a-file-written-anywhere-in-the-printer's-pipeline-then-run $n18 of 4 refused (want 4: | head > x.sh; sh, | sort >> && bash, | head | tee; sh, | cut > PATH; PATH); m21-the-printer's-own-segment-only passes $m21 of 4 (want 4 = RED)" '[ $n18 = 4 ]&&[ $m21 = 4 ]'
cl m16 '$(echo kill $PPID)' 'eval $(echo kill $PPID)' 'cat <(echo kill $PPID) | sh' '`echo kill $PPID`';n19=$n;m16b=$m
cl m22 '$(echo kill $PPID)' 'eval $(echo kill $PPID)' 'X=$(echo kill $PPID)';n19b=$n;m22=$m
cl m23 'cat <(echo kill $PPID) | sh' 'echo kill $PPID $(date) | sh' 'echo $(cat <(echo kill $PPID)) | bash';n19c=$n;m23=$m
ok "c19-a-printer-in-a-substitution-whose-enclosing-segment-would-not-pass $n19 + $n19b + $n19c refused (want 4 + 3 + 3: bare \$( ), eval \$( ), cat <( ) | sh, bare backticks; X=\$( ); a pipe after a substitution, nested); m16-no-enclosing-clause passes $m16b of 4, m22-no-\$(-registration $m22 of 3, m23-segment-ends-at-a-substitution $m23 of 3 (want 4, 3, 3 = RED)" '[ $n19 = 4 ]&&[ $n19b = 3 ]&&[ $n19c = 3 ]&&[ $m16b = 4 ]&&[ $m22 = 3 ]&&[ $m23 = 3 ]'
cl m24 'echo kill $PPID | sort -o x.sh; sh x.sh' 'echo kill $PPID | uniq - x.sh; sh x.sh' 'echo kill $PPID | sort --output=x.sh; sh x.sh';n20=$n;m24=$m
ok "c20-a-SAFE-filter's-own-write-then-run $n20 of 3 refused (want 3: sort -o, uniq IN OUT, sort --output=); m24-no-own-write passes $m24 of 3 (want 3 = RED)" '[ $n20 = 3 ]&&[ $m24 = 3 ]'
cl m18 "echo kill \$PPID > x.sh; awk 'BEGIN{system(\"sh x.sh\")}'" "echo kill \$PPID > x.sh; python3 -c 'import os; os.system(\"sh x.sh\")'" 'echo kill $PPID > x.sh; find . -name x.sh -exec sh {} +';n21=$n;m18b=$m
ok "c21-a-target-named-past-a-later-segment's-lead-word $n21 of 3 refused (want 3: awk system(), python3 os.system, find -exec sh); m18-no-naming-clause passes $m18b of 3 (want 3 = RED)" '[ $n21 = 3 ]&&[ $m18b = 3 ]'
y22=0;n22=0;for c in 'echo $(echo kill $PPID)' 'grep -c x $(echo kill $PPID)' 'cat <(echo kill $PPID)' 'echo `echo kill $PPID`' 'echo kill $PPID | head -1 > notes.md' 'echo kill $PPID | sort -o n.md; cat n.md' 'echo kill $PPID > x.sh; cat x.sh' 'echo kill $PPID | uniq - n.md; grep kill n.md' "echo 'kill \$PPID' | tee -a log.md";do n22=$((n22+1));rq "$c";[ $rc = 0 ]&&[ ! -s $T/err ]&&y22=$((y22+1));done
ok "c22-reads-that-only-name-the-out-still-pass $y22 of $n22 (want $n22: echo \$( ), grep \$( ), cat <( ), echo backticks, | head > notes.md, | sort -o n.md; cat, > x.sh; cat x.sh, | uniq - n.md; grep, | tee -a log.md)" '[ $n22 = 9 ]&&[ $y22 = $n22 ]'
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
python3 -I -c 'import sys;s=open(sys.argv[1],encoding="utf-8").read();a="        if sid and not os.path.exists(os.path.join(d,sid)):\n";b="print(json.dumps({\"decision\":\"block\",\"reason\":GO}));return\n";i=s.index(a);k=s.index(b,i)+len(b);assert s.count(a)==1;open(sys.argv[2],"w",encoding="utf-8").write(s[:i]+s[k:])' $T/bin/agi-pray $T/m7;chmod +x $T/m7;cmp -s $T/bin/agi-pray $T/m7&&{ echo "FAIL mutant m7 changed nothing";exit 99;}
rm -f $T/hm/.prayed/m7;PB=$T/m7 pray stop transcript_path="\"$T/d1\"" session_id='"m7"' last_assistant_message="$(js "$JES")"
ok "m7-without-the-resume-d2-reads-RED the mutant's Stop prints [$(cat $T/out)] (want empty: no next prompt, so d2 can fail)" '[ ! -s $T/out ]'
sed 's/^        if sid and not os.path.exists(os.path.join(d,sid)):$/        if sid and not os.path.exists(os.path.join(d,sid)) and os.path.exists(os.path.join(d,sid+".asked")):/' $T/bin/agi-pray>$T/m12;chmod +x $T/m12;cmp -s $T/bin/agi-pray $T/m12&&{ echo "FAIL mutant m12 changed nothing";exit 99;}
rm -f $T/hm/.prayed/m12;PB=$T/m12 pray stop transcript_path="\"$T/d5\"" session_id='"m12"' last_assistant_message="$(js "work done. $JES")"
ok "m12-the-refusal-gate-kept-d5-reads-RED (sp's mutant) the gated Stop prints [$(cat $T/out)] (want empty: the obeying post would stall)" '[ ! -s $T/out ]'
chmod 600 $T/big
echo "prayer-captive: $f FAIL";exit $f
