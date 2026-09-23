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

## §1 Plan -- TMM.37-41 (ask thought-master first; an owner order in my pane: act, then tell)
```
batch B   ✅ SWR-RS.01 (C2 fires every seed · B no fire) · ✅ C2 mur accept_with_residue · ⏳ RS.01 mur (mur-director-thought-2)
          after the RS.01 mur: TMM.38(2) deviation THOUGHT on a00-1864ce6e · TMM.38(3) letter_frequency floor notes on B, C2, gap_table.md · TMM.39(a) gap_table.md b/c labels to scorer.py · TMM.41 C2's 3 residues in place -> ONE batch-B merge-up
batch A   G.01 HELD on its loop branch @109bcb618 (off-scope, parent overflowed, unreviewed) -> ⏳ research-review rr-mp02-g01 (propose-only)
          then the grammar ALONE (pi deepseek, cap 1, wall 120, ONE kid, refuses off-scope output) -- dispatch line to thought-master first
          then T.01 = finalize the 282 segments as MP.02's held-out set (grammar-labelled), per the review
owner     ⏳ CFG.01 a00-e9111187 config-max pass (hypothesis:lm-every-experiment-path-is-a-config-variable) · Rules item 13 in agent-prompt.md (23663947a)
done      TMM.39 (b)(c)(d) 9755735e0 · TMM.40 a00-e51d276e pending 70939506c · TMM.41 slot finding noted · g5.24.4 draft discarded
guards    nothing under extensions/ (except the owner-ordered item 13) · orders wall 120 on paid rounds · no pi-local round live across 11:41Z · no multi-kid round under a pi-local parent
```

## §2 Landed
```
SWR-C2.02  posts ref 37a4cf1e7 · C2 IFEval strict 0.802218 (434/541) >= 423 FIRES single-run · with HE 92.9pct rel C2 clears BOTH on single runs · owner-added arm, not the named {B,C1,A} · done-unreported: parent died on 401 key expired -> NO parent review
checks     541/541 exact order · scored rows == committed file 541/541 · reductions exact · C2 == B on 28/541 (LoRA live) · links 3947/0 · goals 309 byte-identical
SWR-RS.01  1826d71c6 (ff, pushed) · kid a00-1864ce6e verdict proved, parent accepted (4 probes) · my recompute from the 30 rows matches · finding: langdetect-only seeding not reproducible, noise sits in keywords:letter_frequency (stdlib random)
dm         thought-master 07:58Z: TMM.32 crossed in flight (B re-score never dispatched) · C2 numbers · key-TTL finding · TMM.33 intake
```

## §3 🔴 Where it stops
```
08:5xZ 09-23  LIVE: RS.01 mur (agi-director-thought-swr-rs-01) · research-review rr-mp02-g01 (agi-director-thought-rr-mp02-g01) · CFG.01 a00-e9111187 (cap 1)
ASKED  thought-master 08:5xZ: where to record G.01's deviation THOUGHT (MP.02 vs the held kid nodes)
next   RS.01 mur lands -> batch-B edits -> ONE batch-B merge-up · rr-mp02-g01 lands -> read, report, grammar dispatch line to thought-master · CFG.01 lands -> harvest, report
exact  cd /data/work/agi/.agi/worktrees/post-director-thought && python3 extensions/agi/bin/send.py read director-thought && systemctl --user is-active agi-director-thought-swr-rs-01 agi-director-thought-rr-mp02-g01
window no pi-local round live across the Prime pass-2 (11:41Z)
```

## §4 Traps
```
key TTL    per-spawn key TTL 180 min == wall allowance 180 min -> the parent review starves (C2: 401 at 17:14:14Z) -- reported, thought-master routes it
orders     TMM.33 never reached me; TMM.34 landed only in the raw inbox while send.py read printed empty -> every lap: send.py read + raw inbox tail + master card + goal:g14
pi-local   dry-run prints "model=deepseek"; the argv is --model Qwen3.5-9B -> trust the argv
mur        run-key = mur-<post>; results under MAIN .agi/sessions/workflows/runs/<run-key>/ · a poll loop exiting != the unit finished -> re-check systemctl
git        check git status AFTER a commit
write.py   replace-body guard counts a TABLE and a # inside a fence as headings · an apostrophe inside a single-quoted arg breaks the shell
dispatch   iter ids: digits only after the dot · headroom can change between dry-run and dispatch
actor      export AGI_ACTOR=director-thought before write.py -- without it edited_by falls back to USER=belam (my past edits read belam)
kids       a pi-local parent's kids do NOT inherit --harness pi-local -> they run pi/openrouter deepseek
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

## Scratch -- orders (tracked; live rounds' orders replaced when they land, drafts dispatch only on go)
```
ORDERS CFG.01 (director-thought -> parent · OWNER order 09-23 ~08:4xZ, verbatim on goal:g14 · pi deepseek · cap 1 USD)
read first  hypothesis:lm-every-experiment-path-is-a-config-variable · extensions/agi/lib/agent-prompt.md Rules item 13 (read only)
task        every path literal in the town's experiment scripts becomes a named variable under paths in .agi/config.json, read through ONE shared reader
inventory   2026-09-23: 19 of 51 tracked .py/.sh under datasets/ and .agi/context/local-maxxing/ carry 40 literals (15 files .agi/context/local-maxxing · 3 datasets/switch-rule · 1 datasets/kid-sft/build_corpus.py) -- re-derive it yourself, do not trust this count
reader      one small reader that both .py and .sh can call (prints paths.<key>, relative values resolved from the repo root) -- it lives with the town tooling, NEVER under extensions/
config      add only the keys you convert · descriptive names · each value = the exact literal it replaces (repo-relative where the literal was)
behavior    per key: prove the variable resolves to the exact literal it replaced · per converted script: its smallest honest check still passes (--help, a dry run, or an import)
nodes       Reproduce / Command lines in these chains that call a converted script cite paths.<key> -- a correction in place via write.py, results never rewritten · a node citing a converted file's bytes as evidence gets ONE note: converted, values identical, prior bytes at <commit>
never       anything under extensions/ · result data (.jsonl / .json outputs) · regenerating any result · loop branch season2/loops/hypothesis-lm-magic-pane-wrapper-a00-0a762b7a (held for thought-master)
kids        split by area if it helps, <= 3 kids · one experiment node per kid under the hypothesis
wall        call done by 120 min wall-clock whatever the state (key TTL 180) -- land what is converted, name what is left
cap         1 USD · line ceiling 120 engine-unit lines per kid
record      keys added · literals converted per file · literals left + why · per-key resolved-value proof · checks run · nodes corrected · one harvest line to your seat
```

```
ORDERS MP02-T.01 -- DRAFT, dispatch only on thought-master's GO (director-thought -> parent · TMM.37 ASK 2 · batch A chunk 2 of 3 · pi deepseek · cap 1 USD)
read first  hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call (MP.02) · goal:g5.24.3 · the MP02-G.01 kid node(s) + .agi/context/local-maxxing/magic-pane/cli-grammar.json (the label vocabulary)
task        MP.02's held-out set: >= 100 REAL segments, each = the prose an author wrote up to just before a structured call -> the call that author actually invoked next
sources     the masters' committed dm transcripts (.agi/comms/season-2/dm/*.md, 90 tracked) · MP.01's census: 63 forms = 39 kept + 24 dropped for too-short prose (datasets/magic-pane/metrics_strict.json) -- reuse the 39, never edit MP.01's segments.jsonl
label rule  every label parses under G.01's cli-grammar.json; a next call that does not parse stays OUT and is counted with its reason -- never forced to fit
record      per source · per role (master / director / prime / parent / kid) · per verb · the majority class and its share (S.01's baseline) · the unparsed count + reasons
scrub       every landed segment passes datasets/tools/scrub.py; no raw log copied in
land        datasets/magic-pane/<date>/, distinct from MP.01's segments.jsonl · ONE experiment node under MP.02
never       anything under extensions/ · the suggester itself (S.01) · the GPU or :8080
wall        call done by 120 min whatever the state (key TTL 180); if < 100 segments by then, land what exists and name the gap
cap         1 USD · line ceiling 120 engine-unit lines
```

MP02-G.01 (dispatched 07:58Z):
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
