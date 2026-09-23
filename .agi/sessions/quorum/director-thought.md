# CARD — director-thought · ROLE = doc:unified-director-brief (the head, every director) + doc:lm-director-brief-customizations (thought-master's section) · this card = STATE + todo scratch only; the chain is the source, no rule is copied here

## §0 State
| | |
|---|---|
| post | director-thought · director · town local-maxxing · claude-opus-5-5 (resumed 07:50Z 09-23; box reboot 13:18Z 09-22) · master thought-master (gen 11, joined 07:52Z) |
| tree | /data/work/agi/.agi/worktrees/post-director-thought · branch local-maxxing/season2/posts/director-thought/main · mirror refs/agi/posts/director-thought |
| trunk | local-maxxing/season2/main -- the only branch merged into this post branch |
| pool | headroom -7.16 USD (thought-master 07:5xZ) -> paid rounds refuse · pi-local = 0 USD |
| router | :8080 one slot (-np 1) · --models-max 1 · 9B resident -> pi-local rounds strictly one at a time |
| ids | renumber 09-23 (mint ids kept): g14.11->g5.27 (.1 battery) · g14.16->g5.31 · g14.15->g5.30 · g14.14->g7.33 (parked) · g14 stays |
| board | town:local-maxxing trajectory_standin, thought-master writes it; my rows ride the [merge-up] |

## §1 Plan -- TMM.33 (recorded on goal:g14 + thought-master's card; no dm reached me)
```
batch A  NOW · 0 USD · pi-local · sequential
 ⏳ MP02-G.01  cli-grammar.json derived from argparse · >=30 real invocations validated   LIVE a00-0a762b7a
 ⬜ MP02-T.01  real dm/notes test set, >=100 held-out, scrubbed, datasets/magic-pane/
 ⬜ MP02-S.01  suggester top-1/top-5 vs majority baseline, per role, latency   needs G + T
batch B  on headroom · paid
 ⬜ mur on SWR-C2.02 (landed, NO parent review) -> every residue = its own corrective round
 ⬜ re-score N=10 distinct langdetect seeds: B (TMM.32) + C2 (same rule) -> fires iff CI lower bound > 0.7819
 ⬜ FT.00 -> MP.03
close    ONE [merge-up] per batch, residues = 0
```

## §2 Landed
```
SWR-C2.02  posts ref 37a4cf1e7 · C2 IFEval strict 0.802218 (434/541) >= 423 FIRES single-run · with HE 92.9pct rel C2 clears BOTH on single runs · owner-added arm, not the named {B,C1,A} · done-unreported: parent died on 401 key expired -> NO parent review
checks     541/541 exact order · scored rows == committed file 541/541 · reductions exact · C2 == B on 28/541 (LoRA live) · links 3947/0 · goals 309 byte-identical
dm         thought-master 07:58Z: TMM.32 crossed in flight (B re-score never dispatched) · C2 numbers · key-TTL finding · TMM.33 intake
```

## §3 🔴 Where it stops
```
08:0xZ 09-23  LIVE MP02-G.01 a00-0a762b7a · pid 13881 · 9B pi-local · cap 0 USD
next   when it lands: merge season2/loops/hypothesis-lm-magic-pane-wrapper-a00-0a762b7a -> read kid nodes -> byte-check -> mur (paid; if refused, record the line) -> write MP02-T.01 orders into the scratch below -> dispatch
exact  cd /data/work/agi/.agi/worktrees/post-director-thought && python3 extensions/agi/bin/send.py read director-thought && python3 -c "import json;print(json.load(open('.agi/sessions/iter-MP02-G.01/a00-0a762b7a/agent.json'))['status'])"
window no host model-loading kid across the Prime pass-2 (11:41Z)
```

## §4 Traps
```
key TTL    per-spawn key TTL 180 min == wall allowance 180 min -> the parent review starves (C2: 401 at 17:14:14Z) -- reported, thought-master routes it
orders     a master order can live only on its card / goal:g14 -> read inbox + master dm thread + both of those when the inbox is empty
pi-local   dry-run prints "model=deepseek"; the argv is --model Qwen3.5-9B -> trust the argv
mur        run-key = mur-<post>; results under MAIN .agi/sessions/workflows/runs/<run-key>/ · a poll loop exiting != the unit finished -> re-check systemctl
git        check git status AFTER a commit
write.py   replace-body guard counts a TABLE and a # inside a fence as headings · an apostrophe inside a single-quoted arg breaks the shell
dispatch   iter ids: digits only after the dot · headroom can change between dry-run and dispatch
own miss   SWR-B.03 residues were hand-fixed; the chain says corrective rounds -> rounds from now on · orders were parked in a gitignored dir -> they live in the scratch below, tracked
```

## §5 Verification (known-good)
```
links.py links -> 0 broken · snapshot-goals.py --render --check -> byte-identical · git status clean after commit · push to refs/agi/posts/director-thought
```

## §6 BANKED
```
- fork get_can_shift probe on deployed prism build 10685/7dffb158d (TEL.03/TMM.29) -> next GPU-free slot
- handoff: owner 08:0xZ 09-23 "HANDOFF.md is your handoff card"; the chain (unified brief §2/§3) makes this card the handoff and the root HANDOFF.md the Prime's -> using this card; owner corrects if the root file was meant
- for the head, via thought-master: the brief's §4 thought section still names season1 paths
```

## Scratch -- orders of the live round (tracked; replaced by the next round's orders)
```
ORDERS for MP02-G.01 (director-thought -> parent; TMM.33 batch A, chunk 1 of 3; 0 USD on pi-local). Read hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call and goal:g5.24 (its JEV LANE block, "GRAMMAR FIRST") in full before anything else.

WHY THIS CHUNK: MP.02 (the magic-pane SUGGESTER) ranks up to 5 candidate graph tool calls from a prose stream. It needs a machine-readable grammar of those calls. The engine version of that grammar (goal:g7.33, was G14.14.6) is PARKED by owner order, so TMM.33 builds it here as jev-lane tooling. Do NOT touch extensions/ -- read it only.

TASK: produce .agi/context/local-maxxing/magic-pane/cli-grammar.json plus the script that derives it, in the same dir.
- Tools in scope (the calls town agents actually emit): extensions/agi/bin/write.py (every verb: create, note, set, thought, replace body, and any others it defines), extensions/agi/bin/send.py (send, read and their flags), extensions/agi/bin/dispatch.py (positionals + flags), extensions/agi/bin/workflow.py (run and its other subcommands).
- Per verb: name; positional args; flags (type, required, default); ONE real example invocation; invariants taken from the tool's own source or docstrings (examples already known: write.py set takes a SPACE not '='; note appends one paragraph; thought replaces the THOUGHT block; dispatch iter_n is label.digits with digits only after the dot); traps taken ONLY from recorded town sources -- CLAUDE.md, the traps lines on .agi/sessions/quorum/*.md cards, doc:lm-local-town-box-facts -- each trap citing its source. Invent none.
- DERIVE, DO NOT TRANSCRIBE: the JSON must be generated by the script from the tools themselves (python ast over the argparse/verb tables, or parsing each tool's --help), so it regenerates when the CLI changes. Hand-typed JSON is a defect.

MEASURE (the experiment node must carry these numbers):
1. coverage -- per tool, verbs and flags the derivation found vs what that tool's own --help lists; name every miss.
2. validation -- parse >= 30 REAL invocations against the grammar. Sources: exact commands quoted in .agi/comms/season-2/dm/*.md, in the quorum cards, and in node Agent Notes; and the Bash tool_use command strings in the claude-code session logs under /home/belam/.claude/projects/-data-work-agi*/ (READ ONLY -- never copy a raw log into the repo; any example you land goes through datasets/tools/scrub.py first). Report how many parse and how many fail, and WHY each failure fails. A failure is data; do not loosen the grammar to hide it.
3. size -- grammar size in tokens (it goes into the suggester's prompt next chunk).

LOCAL-MODEL CONSTRAINTS: you and your kids run on Qwen3.5-9B-Q4_K_M through the :8080 router, which has ONE slot (-np 1) and --models-max 1. NEVER request any other model on :8080 -- it would unload the 9B you are running on. Parent and kid share that one slot, so keep kid briefs short and your own turns lean.

CAP: 0 USD (pi-local). LINE CEILING: 120 engine-unit lines (the derivation script); the JSON output does not count. OUT OF SCOPE: the dm/notes test set (chunk MP02-T.01), the suggester itself (chunk MP02-S.01), any edit under extensions/.

RECORD NUMBERS: verbs and flags covered per tool with misses named; validation parse rate on >= 30 real invocations with each failure's reason; grammar token count. One harvest line to your seat when done.
```
