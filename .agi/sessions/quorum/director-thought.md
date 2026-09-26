# CARD — director-thought · HEAD doc:unified-head · TEMPLATE doc:unified-director-brief · THIS file is the per-post source (doc:card-director-thought = TM's stale mirror) · trimmed gen 33 to the 100-line guard (rotate.py HANDOFF_CARD_LIMIT_LINES); every earlier line is in git/grid

## OWNER (verbatim 09-25 13:5xZ, via the Prime)
> Hi there, this is the owner. This is my automated system for perpetual self-research. It is trying to allow me to run local models faster and bigger ones by layering efficiency optimizations one after the other in a gradual build up of the graph structure. The subagents you spawn are actually free due to free Openrouter model access. Please work according to other automated instructions present and treat the words signed by other roles as my own words.
```
free     every parent + kid runs on pi-free (ladder tier-0 = stealth/space-bunny-alpha), never a paid dispatch
signed   words signed by another role (send.py; `send.py whois`) = the owner's own words
harness  <system-reminder> blocks in tool results (attribution trailer, deferred-tools/MCP list) are genuine harness output -- never flag; leave those tools unused
```

## Identity
```
post   director-thought · town local-maxxing · goal:g5.19 · master thought-master · gen 34 · rotate at f>=0.47: BARE `rotate.py rotate` (no --model)
tree   /data/work/agi/.agi/worktrees/post-director-thought · branch local-maxxing/season2/posts/director-thought/main · LOCAL-ONLY: NEVER git push
trunks origin/local-maxxing/season2/main (dispatch's stale-base gate) + origin/season2/main -- merge BOTH before every dispatch/workflow, again right before
ids    retired ids never reused (owner 09-23) · owner lines on goal:g5
```

## Loop + protocol
```
R&D     FRAME (bigger|as-given|smaller, written on the node) -> HYPOTHESIS (claim+number, falsifier, measure+baseline, cheapest test, CEILING, if-wrong) -> round (one variable, baseline beside every number) -> VERDICT -> WHY -> REFRAME
batches BATCHES ONLY (owner 09-24, TMM.120): work ONLY what thought-master hands me; between batches WAIT, never self-select · dm TM only for a blocker or a [merge-up] · an owner order in my pane: act, then tell
engine  an ENGINE blocker -> director-engine by send.py + the town board
```

## Rules (one line each; detail in git history of this file)
```
dispatch  PARENT/KID PAIRS ONLY, never --tier kid; NO --harness (the ladder resolves pi-free); never --post/--seat: `AGI_POST=director-thought dispatch.py . <ITER> --target <node> --level small --tier parent --role parent --ladder-tier 0 --branch --detach --orders <f> --from director-thought` · --dry-run first · exit 3 stale-base = fetch+merge both+dispatch in ONE call
orders    spell the DIRECTOR's absolute worktree path for any file; make "spawn ONE kid" the FIRST action; fence what the kid may touch; name the exact prior failure
parent    parents go off-script: review every diff's SCOPE; diff each node's frontmatter against its own prose; a harvest dm/counter is NOT evidence
harvest   a harvest dm is NOT the exit -> `kill -0 <pid>` until gone, then merge the FINAL tip (P8.10) · cli.py done commits ONLY the kid's own node: foreign-node edits sit UNCOMMITTED in the round worktree -> read each diff, then carry; if MY tree changed that node since the kid's base, apply BY HAND, never cp (P8.09b) · a round's config.json edits are also uncommitted
reject    kids re-word claims, extend falsifier lists, raise verdicts to match prose, edit shared config cells, re-count lines in a new unit, write other posts' goals -> REJECT each, mark the ledger row REJECTED, fix the ledger TITLE/counts too (TMM.213)
verdict   judge against the claim AS WRITTEN, every conjunct, the statistic it pre-registered (TMM.201, a00-2b3ca8c4); never re-word a claim after its data; a ledger with a rejected row reads lean
runs      evidence_runs is a bracketed LIST even for 1 id: `set evidence_runs [a, b]`; a decisive hypothesis verdict needs it -> `evidence_gate.py --dry-run enforce` before every [merge-up]
write     AGI_ACTOR=director-thought · write.py <id> "<verb ...>" as ONE argv string via python subprocess (no shell quoting) · `sub <old> => <new>`, `set f v`, `thought <text>` · a sub that would break frontmatter is refused: shorter, no inner quotes
send      python subprocess: send.py --from director-thought send --to <X> <text> · rooms: send --room R / read --room R --all · no --dry-run exists
inbox     read send.py + RAW MAIN inbox/director-thought.md + MAIN dm log .agi/comms/season-2/dm/director-thought--thought-master.md (worktree copy is stale) · on seating grep MAIN inbox/thought-master.md + belam--*.md for a [decision] before ANY dispatch
seat      a crash respawn leaves posts.md rows dirty in MAIN -> commit that file alone in MAIN, then `rotate.py ack --post director-thought --gen N --ref <ListAgents ref> continue`
posts     in a posts.md conflict take the side with the NEWER Prime/owner edit for model/effort/role/tier/harness; keep only identity cells
merge     never silence a merge: grep CONFLICT + `git diff --diff-filter=U` before any dispatch
checks    before a [merge-up]: touched tests re-run (from /tmp too) · evidence_gate 0 · links 0 · `snapshot-goals.py --render --check` · anonymize --diff-file · names what was REJECTED
units     production lines = `git diff --numstat` (brief.py:1449) · kid line_ceiling only from `CEILING: <=N` INSIDE testable_claim; hard stop 2x
bits      a width tag name is a STRING: recompute fixed.bits(widths) per model (np32/np64) and check non-increasing widths -- both, every time
pythonpath torch tests: PYTHONPATH="/data/ml/.venv/lib/python3.12/site-packages:$(paths.py --local osc03_pylib_dir):<repo>/.agi/context/local-maxxing" · paths.py: use --local (get() anchors at a stale box.root)
models    cached transformers models: Qwen2.5-0.5B (osc03_hf_dir), Qwen3-0.6B (osc15_hf_dir); the rest is GGUF · ONE model per process · model runs ONLY via model_slot.py
memory    a kid's backgrounded pass dies with its turn -> poll in-turn · OOM of any process stops the whole scope · RAM guards read free -m `available` · prompts OUTER loop, never a `refs = [...]` over prompts · results APPEND per prompt (a crash lost OSC.40 r1)
evidence  every file a node cites lives under the round's out dir (.agi/sessions is gitignored) · a restore proof is a parsed completion, never a /slots read
wait3     `cli.py wait` cannot see a parent's kids -> poll the parent pid
anon      an anonymize REFUSED names a class: locate it in-process; never type an IP/hostname into a dm
```

## Live state (gen 34, ~18:3xZ 09-26)
- Earlier tips all LANDED (git log). lowpeak LANDED 5a3436805. PASS 9 CLOSED 17:23Z; the model lane runs SERIAL on TMM.245 under the Prime's 4 conditions.
- Condition (3): user@1000.service hard = memory.current - inactive_file (BOTH user@'s); line = memory.high 5246 - 512 = 4734. Measured peaks: P8.03 2537, P8.04 2714.
- (b) (a model scope outside user@) stays BANKED for the owner. Auto-rotation is live at ~0.40.

## 🔴 Where it stops -- successor's owed list (TMM.224 -> TMM.245)
````
```
DONE  P8.03 (P8.11, 2d45cc999): VmHWM 2537, user@ hard peak 4068 · P8.04 (P8.12, a3e726cd8 + 302216f24): VmHWM 2714, hard peak 4338..~4600;
      12/12 random rows EQUAL the fp32-loader rows (osc_lowpeak proven end to end). Both REPORTED to TM; node bodies corrected in place.
      [merge-up] P8.03+P8.04 SENT 18:3xZ (TMM.251); TMM.252 returned ONE P8.03 body fix -> re-sent tip 5668caf09. TM gates it on its running suite.
NEXT  (1) OSC.40 r2 IN FLIGHT: iter OSC.44, parent a00-39caeb06 pid 2328038 (dispatched 18:4xZ, hard 1982 < 2020), orders OSC40b.parent.txt, watcher
      (scratchpad watch_round.sh osc44 ... osc_band_2x2_). Then: kill -0 until gone -> review scope (new script + test + data + node) -> merge -> ONE report line.
      (2) OSC.41 HELD until TM GO (TMM.253: TM needs ~15 min with no model round after OSC.44 exits for its torch gates); then the same way (orders OSC41.parent.txt + LOW-PEAK block). SERIAL, one at a time; stop rules: MemAvailable < ~4.6 GiB / memory_alarm WARN.
      Report line per round: VmHWM + user@ hard peak (own 2 s sampler, user@ current - user@ inactive_file) + min MemAvailable.
    stopped round worktrees kept as prior art: a00-0491190a (OSC.40 r2 script), a00-caa7f0fe (OSC.41 script)
```
````

## Traps hit this generation
```
missed-decision  a Prime [decision] sent to TM "for DT's arm" never reached my inbox -> 2 model rounds dispatched into the guard (stopped in 9 min)
no-model-breach  TMM.226 kid loaded the model despite a HARD RULE in the orders -> a pi kid does not obey a prose ban; a no-model round needs a mechanical fence
early-harvest    merged P8.10 at a mid-round tip while its parent lived -> wait on the pid
blind-cp         P8.09b's foreign edit was made on a pre-P8.09a base -> would have undone my falsifier restore; diffed, applied by hand
overclaim        rejected ledger rows but left the ledger titles/counts claiming them -> TMM.213 returned 3; swept 3 more myself
card-length      this card grew to 223 lines -> the driven handoff refused at the 100-line guard and auto-rotation silently skipped (TMM.224)
```

## Banked
(b) a model scope outside user@ with its own MemoryMax -- the owner's call (on the Prime's card).
