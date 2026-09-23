# belam — Prime card (local-town)

The Prime's live handoff is `HANDOFF.md` at the repo root (`build:HANDOFF.md`, read in ranges). This card carries only the where-it-stops slot `rotate.py` reads; `.agi/sessions/belam.stops` is the same slot as a file.

### 🔴 Where it stops
```
08:2xZ 09-23 ROTATING at the line (gen 1, meter 0.468, Opus 5.5). FIRST, in order:
 1. RE-ARM the two session crons from .agi/sessions/prime-merge.crons.md (daily "13 8 * * *" + PASS 2 one-shot "41 11 23 9 *"; if 11:41Z is past, run PASS 2 at once under case (d)). gen 1 deleted its own copies before rotating.
 2. DOC UNIFICATION PASS (owner 08:1xZ 09-23, verbatim on goal:g14): 'let's do a doc unification pass ... in the L6 doc ... most of it can be done very simply via graph writes. Don't touch the complicated parts of L6 just the doc simplification part. Just look at how the chain SoT doc for grokbot is structured.'
    L6 doc = doc:s3-plan (title 'L6 plan'); the doc part = HEAD 1.5 'card, brief, role doc ... = views' — the RENDERER (brief.py render) is code: OUT of scope; do the graph-write half only.
    MODEL (core's grok chain SoT): doc:standing-llm-ops (now a STUB, folded 09-22) -> doc:director-grok-internals [PLACEHOLDERS · SECTION:PROFILE (TOWN · BRANCH · GRAPH COORD · NESTED GOAL AUTHORITY (HARD) · STANDING byte-identical) · SECTION:ROUTINE_SYNC · SECTION:ROUTINE_WATCH] + doc:belam-grok-internals (Prime) + doc:grok-harness-internals-sync (post-agnostic seed + sync recipe).
    CLAUDE SIDE TODAY (bytes): unified-director-brief 27070 (§0-§4 + per-master sections sanctuary/thought/prime) · lm-director-brief-customizations 9031 · cards TM 11584 / DT 6235 / DE 4096 · briefs/*-duties 5-12 KB · SKILL.md 58377 · l3-command-ladder-brief 76477 · prime brief 8.8 KB.
    TARGET (owner: 1-2 role docs + 1-2 unified docs): e.g. doc:director-claude-internals in the grok shape (fold unified-director-brief + lm-director-brief-customizations) + the Prime brief in the same shape; cards thin (identity + stops + pointer). write.py create/replace body only; no engine code; owner verbatim stays in nodes.
 3. Town: thought-master @3 · director-thought @4 · director-engine @5 resumed on Opus 5.5 (rows df483f001, pins set, seat models match). TM runs experiments through DT (owner focus); DE HELD on g7.33 (core's). TM's board = town:local-maxxing trajectory_standin (schema grant).
Then as before: daily activation + passes; quiet push-only · batch-max · diagram-max.
```

## 🔴 Where it stops
```
08:2xZ 09-23 ROTATING at the line (gen 1, meter 0.468, Opus 5.5). FIRST, in order:
 1. RE-ARM the two session crons from .agi/sessions/prime-merge.crons.md (daily "13 8 * * *" + PASS 2 one-shot "41 11 23 9 *"; if 11:41Z is past, run PASS 2 at once under case (d)). gen 1 deleted its own copies before rotating.
 2. DOC UNIFICATION PASS (owner 08:1xZ 09-23, verbatim on goal:g14): 'let's do a doc unification pass ... in the L6 doc ... most of it can be done very simply via graph writes. Don't touch the complicated parts of L6 just the doc simplification part. Just look at how the chain SoT doc for grokbot is structured.'
    L6 doc = doc:s3-plan (title 'L6 plan'); the doc part = HEAD 1.5 'card, brief, role doc ... = views' — the RENDERER (brief.py render) is code: OUT of scope; do the graph-write half only.
    MODEL (core's grok chain SoT): doc:standing-llm-ops (now a STUB, folded 09-22) -> doc:director-grok-internals [PLACEHOLDERS · SECTION:PROFILE (TOWN · BRANCH · GRAPH COORD · NESTED GOAL AUTHORITY (HARD) · STANDING byte-identical) · SECTION:ROUTINE_SYNC · SECTION:ROUTINE_WATCH] + doc:belam-grok-internals (Prime) + doc:grok-harness-internals-sync (post-agnostic seed + sync recipe).
    CLAUDE SIDE TODAY (bytes): unified-director-brief 27070 (§0-§4 + per-master sections sanctuary/thought/prime) · lm-director-brief-customizations 9031 · cards TM 11584 / DT 6235 / DE 4096 · briefs/*-duties 5-12 KB · SKILL.md 58377 · l3-command-ladder-brief 76477 · prime brief 8.8 KB.
    TARGET (owner: 1-2 role docs + 1-2 unified docs): e.g. doc:director-claude-internals in the grok shape (fold unified-director-brief + lm-director-brief-customizations) + the Prime brief in the same shape; cards thin (identity + stops + pointer). write.py create/replace body only; no engine code; owner verbatim stays in nodes.
 3. Town: thought-master @3 · director-thought @4 · director-engine @5 resumed on Opus 5.5 (rows df483f001, pins set, seat models match). TM runs experiments through DT (owner focus); DE HELD on g7.33 (core's). TM's board = town:local-maxxing trajectory_standin (schema grant).
Then as before: daily activation + passes; quiet push-only · batch-max · diagram-max.
```
