#!/bin/sh
# graph-metrics.t.sh: goal:g3.8 (DG1 15:47Z; design = doc:rse-aa1-boxes AA1.S at alive/aa1n e6693df0b): the old metrics are read again. ONE cron job as belam runs `success_metrics.py --line | write.py set metrics_line` and the town node carries ONE `metrics_line` cell; metrics.py refuses a root with no nodes/; every null is NAMED on the line, never a number the engine does not have.
# sh + git + python3 on a SCRATCH project (the engine's bin dir is COPIED under it, so crons.py's repo_root, success_metrics.py's root and write.py's graph are all the scratch); a v5 uid cannot read every uid's files, so nothing here touches the live box. No network (no OpenRouter key in the env or the scratch), 0 USD, a scratch crontab FILE (never the user's crontab). BIN = the extensions/agi/bin dir under test (default: ROOT's); a reference / mutant = BIN=<an edited copy of that dir>. The crons lanes read ROOT's own `.agi/nodes/.geometry/crons.md` (the node the builder edits). One ok/FAIL line per case; exit = FAIL count.
# Lanes: A crons (a1 the shipped node declares the job ONCE with the AA1.S fields; a2 `crons.py apply` makes a scratch crontab agree, idempotently; a3 (dropped: DG1 15:59Z, a duplicate-key loader in crons.py is out of this round); a4 the rendered cron line, run by sh in the scratch, writes the cell) · B success_metrics.py --line (b1 ONE line in the AA1.S shape, rc 0, bounded, no && ; b2 exact counts on a known graph; b3 the 7 success metrics each a number or UNMEASURED(reason), none a number it does not have; b4 the reason names the real cause; b5 an ABSENT graph counter is named, not dropped, not 0; b6 a dead metrics.py gives no invented number; b7 a missing ladder node still gives a line) · C metrics.py (c1 a root with no nodes/ is REFUSED: rc != 0, ONE reason line, 0 METRIC lines; c2 control: a normal root prints the SAME 39 METRIC lines as before; c2-help `--help` / `-h` are usage requests, not roots (rc 0, usage, 0 METRIC lines); c3 control: an EMPTY nodes/ is not refused; c4 control: the functions the SessionStart hook imports still work on a root with no nodes/) · D the write (d1 dry-run admitted, writes nothing; d2 one cell replaced whole, value round-trips through YAML; d3 trajectory_standin untouched; d4 a second set by the same actor is last-wins, ONE key).
# Honest limits: AA1.S names no byte bound beyond today's 634 B, so b1 pins 1,024 B (one constant: LINEMAX). b5 pins that an absent graph counter is NAMED (the AA1.S prototype formatter skips absent keys, which this lane calls a defect). d-lanes are green today (write.py set already works): they guard the builder, they are not the RED set.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin};SRC=$R0/extensions/agi/src;LINEMAX=1024
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST OPENROUTER_API_KEY OPENROUTER_PROVISIONING_KEY
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$SRC AGI_BOX=local-town HOME=$T/home;mkdir -p $T/home
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
# nd DIR ID PARENT [EXTRA]: one node file under nodes/DIR
nd(){ { printf -- '---\nid: %s\nmint_id: %s\ntype: %s\nparents:\n  - %s\n%s---\nbody\n' $2 $(printf '%s' $2|md5sum|cut -c1-32) ${2%%:*} $3 "$4"; } >$G_/nodes/$1/${2#*:}.md;}
# mkp NAME [full]: the scratch project. graph = goal g1 <- ideas i1 i2 <- hypothesis h1 (child of i1) <- experiment e1 (verdict proved, evidence_runs 2), ONE deprecated idea i3, and a hand-made one-line ladder node: the counts are the fixture's own. `full` instead copies ROOT's real town node, ladder, crons node and [box] schema (what write.py / crons.py read), committed so write.py is not "dirty".
mkp(){ P=$T/$1;G_=$P/.agi;rm -rf $P;mkdir -p $G_/nodes/goal $G_/nodes/idea $G_/nodes/hypothesis $G_/nodes/experiment $G_/nodes/deprecated/idea $G_/nodes/town $G_/nodes/.geometry $G_/context/schemas $P/extensions/agi $G_/sessions
 $G init -q $P;echo '{}'>$G_/config.json;cp -r $BIN $P/extensions/agi/bin;find $P/extensions/agi/bin -name __pycache__ -prune -exec rm -rf {} +;ln -s $SRC $P/extensions/agi/src
 printf -- '---\nid: goal:g1\nmint_id: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1\ntype: goal\nparents: []\nstatus: active\n---\nbody\n' >$G_/nodes/goal/g1.md
 nd idea idea:i1 goal:g1;nd idea idea:i2 goal:g1;nd hypothesis hypothesis:h1 idea:i1;nd experiment experiment:e1 hypothesis:h1 'verdict: proved
evidence_runs: 2
';nd deprecated/idea idea:i3 goal:g1 'status: deprecated
'
 if [ "$2" = full ];then cp $R0/.agi/nodes/town/local-maxxing.md $G_/nodes/town/;cp $R0/.agi/nodes/.geometry/ladder.md $R0/.agi/nodes/.geometry/crons.md $G_/nodes/.geometry/;cp "$R0/.agi/context/schemas/[box].md" $G_/context/schemas/
 else printf -- '---\nid: ladder:ladder\nmint_id: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb2\ntype: ladder\nparents:\n  - goal:g1\ncurrent_season: 2\n---\nbody\n' >$G_/nodes/.geometry/ladder.md;fi
 $G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm fixture;}
sm(){ (cd $P&&python3 extensions/agi/bin/success_metrics.py "$@" 2>$T/sm.err);}   # stdout only: the cron line is `L=$(...)`, stderr never reaches the cell
xv(){ grep -oE "(^| )$2=(UNMEASURED\([^)]*\)|[^ ]+)"|head -1|sed "s/^ //;s/^[^=]*=//";}   # value of key $2 on the line on stdin (a reason may hold spaces)
mt(){ (cd $P&&python3 extensions/agi/bin/metrics.py "$@" 2>&1);}
cr(){ (cd $P&&python3 extensions/agi/bin/crons.py "$1" --root $G_ --crontab-file $T/ct 2>&1);}
mkp pm
# ---- B: success_metrics.py --line
sm --line $G_ >$T/b1.out;brc=$?;line=$(head -1 $T/b1.out);bn=$(wc -l <$T/b1.out|tr -d ' ');bb=$(wc -c <$T/b1.out|tr -d ' ')
ok "b1-one-line-aa1s-shape success_metrics.py --line on the scratch root prints exactly ONE line ($bn) in the AA1.S shape '<UTC minute> graph: k=v ... | success: k=v ...' (got: $(echo "$line"|cut -c1-90)...), rc $brc (want 0), $bb B (bound $LINEMAX), no '&&' (write.py splits a verb on it)" '[ $brc = 0 ]&&[ "$bn" = 1 ]&&echo "$line"|grep -Eq "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z graph: .* \| success: .*$"&&[ "$bb" -le $LINEMAX ]&&! echo "$line"|grep -q "&&"'
lv(){ echo "$line"|xv x $1;}
ok "b2-exact-counts on the known graph (6 live nodes incl. a one-line ladder + 1 deprecated, 6 edges, 1 decisive verdict) the line carries node_count=$(lv node_count) (want 7) active_node_count=$(lv active_node_count) (want 6) deprecated_node_count=$(lv deprecated_node_count) (want 1) edge_count=$(lv edge_count) (want 6) decisive_verdicts=$(lv decisive_verdicts) (want 1) conclusive_verdicts=$(lv conclusive_verdicts) (want 1)" '[ "$(lv node_count)" = 7 ]&&[ "$(lv active_node_count)" = 6 ]&&[ "$(lv deprecated_node_count)" = 1 ]&&[ "$(lv edge_count)" = 6 ]&&[ "$(lv decisive_verdicts)" = 1 ]&&[ "$(lv conclusive_verdicts)" = 1 ]'
SEVEN="avg_tokens_per_turn hierarchy_tokens_per_hour conclusive_verdicts overview_accuracy_vs_last_season subscription_tokens_per_season vision_adherence_score openrouter_subscription_spend_ratio"
bad=;for k in $SEVEN;do v=$(lv $k);case "$v" in UNMEASURED\(?*\))ok_=1;;[0-9]*)ok_=1;;*)bad="$bad $k=${v:-ABSENT}";;esac;done
ok "b3-seven-metrics-number-or-named-null each of the 7 success metrics is on the line as a number or UNMEASURED(<reason>), none absent, none None/null/0-for-null:${bad:- all 7 well-formed}" '[ -z "$bad" ]'
nulls="avg_tokens_per_turn hierarchy_tokens_per_hour overview_accuracy_vs_last_season subscription_tokens_per_season vision_adherence_score openrouter_subscription_spend_ratio";badn=;for k in $nulls;do case "$(lv $k)" in UNMEASURED\(?*\));;*)badn="$badn $k=$(lv $k)";;esac;done
ok "b3b-the-six-nulls-are-named in the scratch (no token counter, no key) the six null metrics all read UNMEASURED(reason), never a bare number:${badn:- all six named}" '[ -z "$badn" ]'
# b4: the reason names the REAL cause: avg_tokens_per_turn with NO write-log vs a write-log whose rows carry a tokens field must not read the same
r0=$(lv avg_tokens_per_turn);printf '{"tokens": 5}\n'>$G_/sessions/write-log.jsonl;sm --line $G_ >$T/b4.out;r1=$(head -1 $T/b4.out|xv x avg_tokens_per_turn);rm -f $G_/sessions/write-log.jsonl
ok "b4-reason-names-the-cause avg_tokens_per_turn reads '$r0' with no write-log and '$r1' when the write-log carries a tokens field: both UNMEASURED(<reason>) and the two reasons differ (a null whose reason never changes is not naming anything)" 'case "$r0" in UNMEASURED\(?*\));;*)false;;esac&&case "$r1" in UNMEASURED\(?*\));;*)false;;esac&&[ "$r0" != "$r1" ]'
# b5/b6: a stub metrics.py in the scratch bin copy (success_metrics resolves metrics.py beside itself). b5 = it prints only SOME counters (no thought_coverage, no decisive_verdicts); b6 = it dies with no output
KEYS="node_count active_node_count deprecated_node_count edge_count evidence_fraction decisive_verdicts decisive_evidence_fraction broken_links thought_coverage longest_chain_length outcome_coverage"
mkp ps;printf '#!/usr/bin/env python3\nprint("METRIC node_count=6")\nprint("METRIC active_node_count=5")\nprint("METRIC deprecated_node_count=1")\nprint("METRIC edge_count=4")\nprint("METRIC evidence_fraction=0.5")\nprint("METRIC decisive_evidence_fraction=0.5")\nprint("METRIC broken_links=0")\nprint("METRIC longest_chain_length=3")\nprint("METRIC outcome_coverage=0.0")\n'>$P/extensions/agi/bin/metrics.py
sm --line $G_ >$T/b5.out;l5=$(head -1 $T/b5.out);m5(){ echo "$l5"|xv x $1;}
bad5=;for k in $KEYS;do case "$(m5 $k)" in UNMEASURED\(?*\))ok_=1;;[0-9]*)ok_=1;;*)bad5="$bad5 $k=$(m5 $k)";;esac;done
ok "b5a-absent-reason-text (alive 16:00Z) an ABSENT graph key reads exactly UNMEASURED(absent from metrics.py): thought_coverage '$(m5 thought_coverage)', decisive_verdicts '$(m5 decisive_verdicts)'" '[ "$(m5 thought_coverage)" = "UNMEASURED(absent from metrics.py)" ]&&[ "$(m5 decisive_verdicts)" = "UNMEASURED(absent from metrics.py)" ]'
ok "b5-absent-graph-counter-is-named with a metrics.py that does not emit thought_coverage nor decisive_verdicts, EVERY one of the 11 graph keys is still on the line as a number or UNMEASURED(reason) (absent: not dropped):${bad5:- all 11 present}; thought_coverage reads '$(m5 thought_coverage)' (want UNMEASURED(...), not 0), conclusive_verdicts reads '$(m5 conclusive_verdicts)' (want UNMEASURED(...))" '[ -z "$bad5" ]&&case "$(m5 thought_coverage)" in UNMEASURED\(?*\));;*)false;;esac&&case "$(m5 conclusive_verdicts)" in UNMEASURED\(?*\));;*)false;;esac'
ok "b5b-present-counters-stay-numbers (control) the counters the stub DID emit keep their numbers: node_count=$(m5 node_count) edge_count=$(m5 edge_count) evidence_fraction=$(m5 evidence_fraction)" '[ "$(m5 node_count)" = 6 ]&&[ "$(m5 edge_count)" = 4 ]&&[ "$(m5 evidence_fraction)" = 0.5 ]'
printf '#!/usr/bin/env python3\nimport sys\nsys.exit(3)\n'>$P/extensions/agi/bin/metrics.py;sm --line $G_ >$T/b6.out;b6rc=$?;cp $T/sm.err $T/b6.err;g6=$(grep -o 'graph: .* | success' $T/b6.out|head -1)
b6bad=;l6=$(head -1 $T/b6.out);for k in $KEYS conclusive_verdicts;do v6=$(echo "$l6"|xv x $k);[ "$v6" = "UNMEASURED(metrics.py rc=3)" ]||b6bad="$b6bad $k='$v6'";done
ok "b6b-dead-reason-carries-the-rc (alive 16:00Z) a DEAD metrics.py reads UNMEASURED(metrics.py rc=N) with its real exit code (3) in EVERY graph key and in conclusive_verdicts, so a dead tool never reads like a counter with no source yet:${b6bad:- all 12 carry rc=3}" '[ -z "$b6bad" ]'
ok "b6-dead-metrics-py-invents-nothing a metrics.py that exits 3 with no output: --line still prints ONE line ($(wc -l <$T/b6.out|tr -d ' ')), rc $b6rc (want 0), every one of the 11 graph keys UNMEASURED(reason) and none a number (graph part: '$(echo "$g6"|cut -c1-110)'), 0 Traceback (stderr)" '[ $b6rc = 0 ]&&[ "$(wc -l <$T/b6.out|tr -d " ")" = 1 ]&&[ -n "$g6" ]&&! echo "$g6"|sed "s/UNMEASURED([^)]*)//g"|grep -Eq "[a-z_]+=[0-9]"&&[ "$(echo "$g6"|grep -o "UNMEASURED("|wc -l|tr -d " ")" -ge 11 ]&&[ "$(grep -c Traceback $T/b6.err)" = 0 ]'
mkp p1;printf '#!/usr/bin/env python3\nimport os\nopen(os.environ["RUNS"], "a").write("run\\n")\nfor k in ("node_count=6", "active_node_count=5", "deprecated_node_count=1", "edge_count=4", "evidence_fraction=0.5", "decisive_verdicts=1", "decisive_evidence_fraction=0.5", "broken_links=0", "thought_coverage=0.1", "longest_chain_length=3", "outcome_coverage=0.0"):\n    print("METRIC " + k)\n'>$P/extensions/agi/bin/metrics.py;: >$T/runs;export RUNS=$T/runs;sm --line $G_ >$T/b8.out;b8rc=$?
ok "b8-one-metrics-py-run-per-tick (DG1 15:59Z) one --line run starts metrics.py exactly ONCE ($(wc -l <$T/runs|tr -d ' ') run(s), want 1; the live run is about a minute, the cron fires hourly) and conclusive_verdicts is read from THAT stream ($(head -1 $T/b8.out|xv x conclusive_verdicts), want 1), rc $b8rc" '[ "$(wc -l <$T/runs|tr -d " ")" = 1 ]&&[ "$(head -1 $T/b8.out|xv x conclusive_verdicts)" = 1 ]&&[ $b8rc = 0 ]'
mkp pl;rm -f $G_/nodes/.geometry/ladder.md;sm --line $G_ >$T/b7.out;b7rc=$?;cp $T/sm.err $T/b7.err
ok "b7-no-ladder-node-still-one-line a graph with no ladder node (season.py cannot name the season): --line still prints ONE line ($(wc -l <$T/b7.out|tr -d ' ')) and exits 0 (rc $b7rc), 0 Traceback, overview_accuracy_vs_last_season UNMEASURED(reason): '$(head -1 $T/b7.out|cut -c1-70)'; today the run dies with ERR: ladder node not found (stderr: $(head -1 $T/b7.err|cut -c1-50))" '[ $b7rc = 0 ]&&[ "$(wc -l <$T/b7.out|tr -d " ")" = 1 ]&&[ "$(grep -c Traceback $T/b7.err)" = 0 ]&&head -1 $T/b7.out|grep -q "overview_accuracy_vs_last_season=UNMEASURED("'
# ---- C: metrics.py
mkp pm
mt $P >$T/c1.out;c1rc=$?;c1n=$(wc -l <$T/c1.out|tr -d ' ');c1m=$(grep -c '^METRIC ' $T/c1.out)
ok "c1-no-nodes-root-refused metrics.py given a root with NO nodes/ (the repo root, not <repo>/.agi) is REFUSED: rc $c1rc (want != 0), ONE reason line ($c1n; '$(head -1 $T/c1.out|cut -c1-100)') naming nodes, $c1m METRIC lines (want 0); today rc 0 + 39 all-zero METRIC lines" '[ $c1rc != 0 ]&&[ "$c1n" = 1 ]&&[ "$c1m" = 0 ]&&head -1 $T/c1.out|grep -q nodes'
mt $G_ >$T/c2.out;c2rc=$?
cat >$T/c2.gold <<'EOF'
METRIC longest_chain_length=3
METRIC avg_chain_depth=0.86
METRIC mvp_count=0
METRIC outcome_coverage=0.0
METRIC chain_branching_factor=2.0
METRIC node_count=7
METRIC edge_count=6
METRIC scoring_mvp_count=0
METRIC scoring_hypothesis_count=1
METRIC backward_mvp_count=0
METRIC retired_goal_nodes=0
METRIC retired_open_hypotheses=0
METRIC deprecated_open_hypotheses=0
METRIC deprecated_excluded_nodes=1
METRIC unattributed_nodes=0
METRIC goals_horizon=0
METRIC goals_retired=0
METRIC goals_complete=0
METRIC goal_count=1
METRIC deprecation_score_delta=0.0
METRIC deprecated_node_count=1
METRIC active_node_count=6
METRIC unpushed_commits=-1
METRIC unpushed_reason=no-upstream
METRIC verdicts_asserting=1
METRIC verdicts_pending=0
METRIC verdicts_evidence_backed=0
METRIC evidence_fraction=0.0
METRIC decisive_verdicts=1
METRIC decisive_evidence_fraction=0.0
METRIC unevidenced_decisive_verdicts=1
METRIC shadow_decisive_verdicts=0
METRIC shadow_decisive_no_verdict=0
METRIC broken_links=0
METRIC thought_coverage=0.0
METRIC nodes_with_thought=0
METRIC evidence_weighted_depth=0.0
METRIC primary_metric=outcome_coverage
METRIC primary_value=0.0
EOF
ok "c2-normal-root-same-metric-lines (control) a normal root (<repo>/.agi) prints the SAME 39 METRIC lines as before the change (rc $c2rc; $(diff $T/c2.gold $T/c2.out|grep -c '^[<>]') differing lines)" '[ $c2rc = 0 ]&&diff -q $T/c2.gold $T/c2.out >/dev/null'
(cd $P&&python3 extensions/agi/bin/metrics.py) >$T/c2b.out 2>&1
ok "c2b-cwd-resolution-same (control) with NO root argument, run from the repo root, the nearest .agi/ wins and the lines are the same ($(diff $T/c2.gold $T/c2b.out|grep -c '^[<>]') differing)" 'diff -q $T/c2.gold $T/c2b.out >/dev/null'
# c2-help (DG1 16:31Z, SM range red test_bin_help_smoke[metrics.py]): `metrics.py --help` / `-h` is a usage request, NOT a root: rc 0, a usage line, 0 METRIC lines, never the 'has no nodes' refusal. (A real no-nodes dir stays refused: c1.)
for hf in --help -h;do mt $hf >$T/c2h.out;hrc=$?;hm=$(grep -c '^METRIC ' $T/c2h.out);hn=$(grep -ci 'no nodes' $T/c2h.out);hu=$(grep -ci 'usage' $T/c2h.out)
ok "c2-help-$hf-is-not-a-root metrics.py $hf: rc $hrc (want 0), a usage line ($hu, want >= 1), $hm METRIC lines (want 0), 'no nodes' text $hn time(s) (want 0)" '[ $hrc = 0 ]&&[ "$hu" -ge 1 ]&&[ "$hm" = 0 ]&&[ "$hn" = 0 ]';done
mkp pe;rm -rf $G_/nodes;mkdir $G_/nodes;mt $G_ >$T/c3.out;c3rc=$?
ok "c3-empty-nodes-dir-not-refused (control) an EMPTY nodes/ (the directory, nothing in it) is a fresh graph, not a wrong root: rc $c3rc (want 0), node_count=$(sed -n 's/^METRIC node_count=//p' $T/c3.out) (want 0); only a MISSING nodes/ is refused" '[ $c3rc = 0 ]&&[ "$(sed -n "s/^METRIC node_count=//p" $T/c3.out)" = 0 ]'
mkp pm;c4=$(cd $P&&python3 -c "
import sys;sys.path.insert(0,'extensions/agi/bin')
from pathlib import Path
import metrics
try:
    m=metrics.compute(Path('$P'));print('compute-ok',m['node_count'])
except SystemExit as e: print('EXIT',e.code)
except Exception as e: print('EXC',type(e).__name__)
" 2>&1|tail -1)
ok "c4-hook-functions-unchanged (control) the SessionStart hook imports functions, not main(): metrics.compute() on a root with no nodes/ still RETURNS (got '$c4'); the refusal lives in main(), a hook must not die on it" 'case "$c4" in compute-ok*);;*)false;;esac'
# ---- A: crons
mkp pc full;: >$T/ct;cr show >$T/a1.out;a1d=$(awk '/^desired:/{f=1;next} /^$/{f=0} f' $T/a1.out);a1c=$(echo "$a1d"|grep -c 'success_metrics.py --line')
yf=$(cd $P&&python3 -c "
import yaml
fm=yaml.safe_load(open('$G_/nodes/.geometry/crons.md').read().split('---')[1])
j=(fm.get('cadences') or {}).get('graph_metrics') or {}
print('A1OK' if (j.get('schedule')=='23 * * * *' and j.get('enabled') is True and j.get('box')=='local-town' and str(j.get('why_box') or '').strip() and 'success_metrics.py --line' in str(j.get('cmd'))) else 'A1BAD '+repr(j)[:90])" 2>&1|tail -1)
ok "a1-shipped-node-declares-the-job-once crons.py show over ROOT's crons.md lists graph_metrics ONCE ($a1c line(s) with success_metrics.py --line) at '23 * * * *' ($(echo "$a1d"|grep 'success_metrics.py --line'|head -1|cut -c1-14)), and the node's cadence cell (schedule 23 * * * *, enabled, box local-town, a why_box, the cmd) reads: $yf (want A1OK); today the job is absent" '[ "$a1c" = 1 ]&&echo "$a1d"|grep "success_metrics.py --line"|head -1|grep -q "^  23 \* \* \* \* "&&[ "$yf" = A1OK ]'
ng=$(grep -c '^  graph_metrics:' $G_/nodes/.geometry/crons.md);nm=$(grep -c 'metrics.py' $G_/nodes/.geometry/crons.md)
ok "a1b-exactly-once-in-the-node the node has ONE graph_metrics cadence key ($ng, want 1) and 'metrics.py' appears on exactly ONE line of it ($nm, want 1: the cmd; the prose says nothing that would match twice)" '[ "$ng" = 1 ]&&[ "$nm" = 1 ]'
cr apply >$T/a2.out;a2n=$(grep -c 'success_metrics.py --line' $T/ct);cp $T/ct $T/ct.1;cr apply >/dev/null;cr show >$T/a2s.out
ok "a2-apply-makes-the-crontab-agree after crons.py apply on a scratch crontab file the job is installed ONCE ($a2n line(s), want 1) at minute 23 hourly ($(grep 'success_metrics.py --line' $T/ct|head -1|cut -c1-14)), a second apply leaves the file byte-identical ($(cmp -s $T/ct $T/ct.1&&echo same||echo CHANGED)) and show reports no drift ($(grep -c DRIFT $T/a2s.out) DRIFT)" '[ "$a2n" = 1 ]&&grep "success_metrics.py --line" $T/ct|head -1|grep -q "^23 \* \* \* \* "&&cmp -s $T/ct $T/ct.1&&! grep -q DRIFT $T/a2s.out'
# a4: the rendered cron line itself, run by sh in the scratch (belam's job end to end): the town node gets the cell
mkp pc full;: >$T/ct;cr apply >/dev/null;cl=$(grep 'success_metrics.py --line' $T/ct|head -1|cut -d' ' -f6-);mkdir -p $HOME/logs
(cd $P&&sh -c "$cl") >$T/a4.out 2>&1;a4rc=$?;cell=$(sed -n 's/^metrics_line: //p' $G_/nodes/town/local-maxxing.md|head -1);NC=$(mt $G_|sed -n 's/^METRIC node_count=//p')
ok "a4-the-cron-line-writes-the-cell the rendered job line, run by sh in the scratch project, exits $a4rc (want 0) and leaves ONE metrics_line cell on town:local-maxxing holding the SAME node_count as metrics.py on that project ($NC) and conclusive_verdicts=1 (cell: $(echo "$cell"|cut -c1-80)...)" '[ $a4rc = 0 ]&&[ "$(grep -c "^metrics_line:" $G_/nodes/town/local-maxxing.md)" = 1 ]&&echo "$cell"|grep -q "node_count=$NC "&&echo "$cell"|grep -q "conclusive_verdicts=1"'
# ---- D: the write (write.py set metrics_line as belam on the town node)
mkp pw full;TN=$G_/nodes/town/local-maxxing.md;sha0=$(sha256sum <$TN|cut -d' ' -f1)
V1='2026-10-07T15:05Z graph: node_count=5813 active_node_count=5574 evidence_fraction=0.898 thought_coverage=0.521 | success: avg_tokens_per_turn=UNMEASURED(no source yet) conclusive_verdicts=1235 openrouter_subscription_spend_ratio=UNMEASURED(no source yet)'
V2='2026-10-07T16:23Z graph: node_count=5900 active_node_count=5650 | success: conclusive_verdicts=1300'
wr(){ (cd $P&&python3 extensions/agi/bin/write.py town:local-maxxing "set metrics_line $1" --actor belam $2 2>&1);}
wr "$V1" --dry-run >$T/d1.out;d1rc=$?;sha1=$(sha256sum <$TN|cut -d' ' -f1)
ok "d1-dry-run-admitted-writes-nothing (control) write.py set metrics_line as belam --dry-run: rc $d1rc, the ring gate says admitted ($(grep -c 'admitted' $T/d1.out)), the town node is byte-identical after ($([ $sha0 = $sha1 ]&&echo same||echo CHANGED))" '[ $d1rc = 0 ]&&grep -q admitted $T/d1.out&&[ $sha0 = $sha1 ]'
wr "$V1" >$T/d2a.out;wr "$V2" >$T/d2b.out
rt=$(cd $P&&python3 -c "
import yaml
fm=yaml.safe_load(open('$TN').read().split('---')[1])
print('RT', fm.get('metrics_line')=='''$V2''', len([k for k in fm if k=='metrics_line']))" 2>&1|tail -1)
ok "d2-one-cell-replaced-whole (control) two sets by the same actor leave ONE metrics_line line in the node ($(grep -c '^metrics_line:' $TN)), holding the SECOND value whole and round-tripping through YAML ('$rt'); the first value is gone ($(grep -c 'node_count=5813' $TN) occurrences)" '[ "$(grep -c "^metrics_line:" $TN)" = 1 ]&&[ "$rt" = "RT True 1" ]&&! grep -q "node_count=5813" $TN'
tr=$(cd $P&&python3 - <<PYEOF 2>&1|tail -1
import yaml,subprocess
a=yaml.safe_load(open('$R0/.agi/nodes/town/local-maxxing.md').read().split('---')[1])
b=yaml.safe_load(open('$TN').read().split('---')[1])
same=a.get('trajectory_standin')==b.get('trajectory_standin')
oth={k for k in set(a)|set(b) if k not in ('metrics_line',) and a.get(k)!=b.get(k)}
print('TS',same,sum('metrics: HEAD + KV' in str(x) for x in b.get('trajectory_standin',[])),sorted(oth))
PYEOF
)
ok "d3-trajectory-standin-untouched (control) after the sets the town node's trajectory_standin is identical to ROOT's, its 'metrics: HEAD + KV' entry still appears once, and no other frontmatter key changed: '$tr' (want TS True 1 [])" '[ "$tr" = "TS True 1 []" ]'
ok "d4-last-wins-one-key (control) a third set by the same actor replaces again (still ONE metrics_line line: $(wr "$V1" >/dev/null;grep -c '^metrics_line:' $TN)), and the cell now holds the last value ($(grep -c 'node_count=5813' $TN) occurrence of the first value, want 1)" '[ "$(grep -c "^metrics_line:" $TN)" = 1 ]&&[ "$(grep -c "node_count=5813" $TN)" = 1 ]'
# ---- E: the four residues of mur-sm21-dg3-gmetrics2 (DG1 RULINGS 16:52Z), RED on 41956e53d5. Everything is observed through the shipped surfaces (success_metrics.py --line, the RENDERED cron line run by sh in the scratch, the node bytes, git): how the job is split into files is the builder's.
# R1: hierarchy_tokens_per_hour reads a row's tokens FIELD, never the substring "tokens" (a node-id slug like ...first-prose-tokens-... is not a counter)
mkp pr1;python3 -c '
import json
for i in range(3000): print(json.dumps({"ts": i, "verb": "set", "node": "goal:g1"}))
for n in ("idea:first-prose-tokens-a", "idea:first-prose-tokens-b", "idea:first-prose-tokens-c", "hypothesis:first-prose-tokens-d"): print(json.dumps({"ts": 9000, "verb": "set", "node": n}))
print(json.dumps({"ts": 9001, "verb": "note", "msg": "count the tokens later"}))
' >$G_/sessions/write-log.jsonl;sm --line $G_ >$T/r1a.out;r1a=$(head -1 $T/r1a.out|xv x hierarchy_tokens_per_hour)
python3 -c '
import json
for i in range(3000): print(json.dumps({"ts": i, "verb": "set", "node": "goal:g1", "tokens": 12}))
' >$G_/sessions/write-log.jsonl;sm --line $G_ >$T/r1b.out;r1b=$(head -1 $T/r1b.out|xv x hierarchy_tokens_per_hour)
ok "r1a-substring-is-not-a-counter a write-log whose only 'tokens' text is inside node-id slugs (4 rows) and a note value (1 row), no row with a tokens field: hierarchy_tokens_per_hour reads '$r1a' (want UNMEASURED(no source yet)); 41956e53d5 reads (no live counter) over the live 2.29 MB log" '[ "$r1a" = "UNMEASURED(no source yet)" ]'
ok "r1b-a-tokens-field-is-the-counter-reading (control) a write-log whose rows carry a tokens FIELD: hierarchy_tokens_per_hour reads '$r1b' (want UNMEASURED(no live counter)), different from r1a" '[ "$r1b" = "UNMEASURED(no live counter)" ]'
# R2: the hourly job never leaves town:local-maxxing dirty. The RENDERED cron line, run by sh in the scratch, in four states.
mkp pj full;TN=$G_/nodes/town/local-maxxing.md;echo '{"values":{"core":{"suite_lock":{"hold_wait_s":1}}}}'>$G_/config.json;$G -C $P commit -qam cfg;: >$T/ct;cr apply >/dev/null;cl=$(grep 'success_metrics.py --line' $T/ct|head -1|cut -d' ' -f6-)
[ -n "$cl" ]||cl=$(grep 'success_metrics.py' $T/ct|head -1|cut -d' ' -f6-)
jb(){ LOG=$(echo "$cl"|sed 's/.*>> \([^ ]*\) .*/\1/');: >$LOG;(cd $P&&sh -c "$cl") >$T/job.out 2>&1;jrc=$?;cat $LOG >>$T/job.out;jn=$(grep -c . $T/job.out);jdirty=$($G -C $P status --porcelain --untracked-files=no|wc -l|tr -d ' ');}   # the cron line appends to a per-project log: that log IS the job's output
dirtyp(){ $G -C $P status --porcelain -- "$TN"|wc -l|tr -d ' ';}
jb;r2a=$(grep -c "^metrics_line:" $TN)
ok "r2a-clean-node-writes-one-cell (control) on a clean node with no lock the job exits $jrc (want 0), the town node carries ONE metrics_line cell ($r2a) and the scratch repo is clean after ($jdirty dirty path(s), want 0)" '[ $jrc = 0 ]&&[ "$r2a" = 1 ]&&[ "$jdirty" = 0 ]'
mkp pj full;TN=$G_/nodes/town/local-maxxing.md;echo '{"values":{"core":{"suite_lock":{"hold_wait_s":1}}}}'>$G_/config.json;$G -C $P commit -qam cfg;printf 'a hand edit\n'>>$TN;s0=$(sha256sum <$TN|cut -d' ' -f1);h0=$($G -C $P rev-parse HEAD)
jb;s1=$(sha256sum <$TN|cut -d' ' -f1);h1=$($G -C $P rev-parse HEAD)
ok "r2b-dirty-node-is-skipped a node that is ALREADY dirty (a hand edit): the job exits $jrc (want 0) after ONE output line ($jn: '$(head -1 $T/job.out|cut -c1-70)', containing skip), the node bytes are unchanged ($([ $s0 = $s1 ]&&echo same||echo CHANGED)) and HEAD did not move ($([ $h0 = $h1 ]&&echo same||echo MOVED): the hand edit is not laundered into a commit)" '[ $jrc = 0 ]&&[ "$jn" = 1 ]&&grep -qi skip $T/job.out&&[ $s0 = $s1 ]&&[ $h0 = $h1 ]'
mkp pj full;TN=$G_/nodes/town/local-maxxing.md;echo '{"values":{"core":{"suite_lock":{"hold_wait_s":1}}}}'>$G_/config.json;$G -C $P commit -qam cfg;sleep 120 & LP=$!;echo $LP >$G_/sessions/verify-suite.lock;s0=$(sha256sum <$TN|cut -d' ' -f1);h0=$($G -C $P rev-parse HEAD)
jb;kill $LP 2>/dev/null;s1=$(sha256sum <$TN|cut -d' ' -f1);h1=$($G -C $P rev-parse HEAD)
ok "r2c-held-suite-lock-is-skipped with the graph's verify-suite.lock held by a LIVE pid ($LP) the job exits $jrc (want 0) after ONE output line ($jn: '$(head -1 $T/job.out|cut -c1-70)', containing skip), the node bytes are unchanged ($([ $s0 = $s1 ]&&echo same||echo CHANGED)), HEAD did not move ($([ $h0 = $h1 ]&&echo same||echo MOVED)) and the node is clean ($(dirtyp) dirty); 41956e53d5 writes the node, waits, exits 3 and leaves it dirty" '[ $jrc = 0 ]&&[ "$jn" = 1 ]&&grep -qi skip $T/job.out&&[ $s0 = $s1 ]&&[ $h0 = $h1 ]&&[ "$(dirtyp)" = 0 ]'
mkp pj full;TN=$G_/nodes/town/local-maxxing.md;printf '#!/usr/bin/env python3\nimport sys\nn = sys.argv[1]\nsys.argv = sys.argv[:2]\np = "%s"\nt = open(p).read()\nopen(p, "w").write(t.replace("\\nscaffold_hash:", "\\nmetrics_line: stub\\nscaffold_hash:", 1))\nprint("commit refused: the write landed uncommitted; exit 3")\nsys.exit(3)\n' $TN >$P/extensions/agi/bin/write.py;$G -C $P add -A;$G -C $P commit -qm stubwrite;h0=$($G -C $P rev-parse HEAD)
jb;h1=$($G -C $P rev-parse HEAD);r2d=$($G -C $P show --stat --format= HEAD|grep -c '|');r2dn=$($G -C $P show --stat --format= HEAD|grep '|'|grep -c 'nodes/town/local-maxxing.md')
ok "r2d-write-exit-3-leaves-the-node-clean a write that still exits 3 (a stub write.py that edits the node and exits 3, the race after the pre-check): after the job the node is clean ($(dirtyp) dirty, want 0) and the scratch repo is clean ($jdirty), the recover commit is BY EXACT PATH (HEAD moved: $([ $h0 != $h1 ]&&echo yes||echo NO); it touches $r2d path(s), want 1: the node ($r2dn)); no checkout / reset (the metrics_line cell survived: $(grep -c '^metrics_line:' $TN)); job rc $jrc" '[ "$(dirtyp)" = 0 ]&&[ "$jdirty" = 0 ]&&[ $h0 != $h1 ]&&[ "$r2d" = 1 ]&&[ "$r2dn" = 1 ]&&[ "$(grep -c "^metrics_line:" $TN)" = 1 ]'
# R3: the cell is metrics_line (sorts between master and scaffold_hash), so a town -> s2 merge-up where another writer rewrote edited_by is CLEAN
mkp pj full;TN=$G_/nodes/town/local-maxxing.md;base=$($G -C $P rev-parse --abbrev-ref HEAD);$G -C $P checkout -q -b other;sed -i 's/^edited_by: .*/edited_by: thought-master/' $TN;$G -C $P commit -qam other-writer;$G -C $P checkout -q $base;jb
nb=$(cd $P&&python3 -c "
import yaml
fm=yaml.safe_load(open('$TN').read().split('---')[1]);k=list(fm)
i=k.index('metrics_line') if 'metrics_line' in k else -1
print('NB', k[i-1] if i>0 else None, k[i+1] if 0<=i<len(k)-1 else None, 'graph_metrics' in k)" 2>&1|tail -1)
ok "r3a-cell-sorts-between-master-and-scaffold_hash after the job the town node's frontmatter has the cell 'metrics_line' with neighbours '$nb' (want NB master scaffold_hash False: not next to edited_by, and no graph_metrics cell)" '[ "$nb" = "NB master scaffold_hash False" ]'
$G -C $P merge -q --no-edit other >$T/mg.out 2>&1;mrc=$?;eb=$(sed -n 's/^edited_by: //p' $TN)
ok "r3b-merge-with-an-edited_by-rewrite-is-clean a scratch merge of two branches, one rewriting edited_by (another writer), one holding the job's cell write, exits $mrc (want 0: no conflict), keeps both (edited_by '$eb', want thought-master; $(grep -c '^metrics_line:' $TN) metrics_line cell) and leaves no conflict markers ($(grep -c '^<<<<<<<' $TN))" '[ $mrc = 0 ]&&[ "$eb" = thought-master ]&&[ "$(grep -c "^metrics_line:" $TN)" = 1 ]&&[ "$(grep -c "^<<<<<<<" $TN)" = 0 ]'
# R4: --line makes NO authenticated OpenRouter call (credit_balance / key_usage replaced by recorders that raise)
mkp p4;printf 'import os\ndef _rec(n):\n    open(os.environ["CALLS"], "a").write(n + "\\n")\n    raise RuntimeError("no network in the lane")\ndef credit_balance(*a, **k):\n    _rec("credit_balance")\ndef key_usage(*a, **k):\n    _rec("key_usage")\ndef list_all_keys(*a, **k):\n    _rec("list_all_keys")\n'>$P/extensions/agi/bin/provisioning.py;: >$T/calls;export CALLS=$T/calls;sm --line $G_ >$T/r4.out;r4rc=$?;r4n=$(wc -l <$T/calls|tr -d ' ')
ok "r4-line-makes-no-openrouter-call success_metrics.py --line with credit_balance / key_usage / list_all_keys replaced by recorders: $r4n call(s) (want 0; the cron fires hourly and each call is a 30 s authenticated GET whose result the line discards), rc $r4rc (want 0), subscription_tokens_per_season '$(head -1 $T/r4.out|xv x subscription_tokens_per_season)' and openrouter_subscription_spend_ratio '$(head -1 $T/r4.out|xv x openrouter_subscription_spend_ratio)' both UNMEASURED(no source yet), as before" '[ "$r4n" = 0 ]&&[ $r4rc = 0 ]&&[ "$(head -1 $T/r4.out|xv x subscription_tokens_per_season)" = "UNMEASURED(no source yet)" ]&&[ "$(head -1 $T/r4.out|xv x openrouter_subscription_spend_ratio)" = "UNMEASURED(no source yet)" ]'
echo "graph-metrics: $f FAIL"
exit $f
