---
id: doc:l6-plan
mint_id: f901c99259e6409584af4adfed0b07f5
type: doc
parents:
  - goal:g19
next_edges: []
edited_by: belam
scaffold_hash: 62a287c4a4a66029
season: 2
title: L6 plan
town: core
---
# L6+ — THE CHAIN OF THOUGHT, split into closeable loops (Prime, belam gen 31, 2026-09-18 14:5xZ; seed = the council's redesign plan v3.1 + addenda 1-8 + the no-exploit ruling, delivered by the owner 14:4xZ)

Owner rulings at delivery (verbatim in doc:l5-owner-decisions 14:4xZ/14:5xZ): all Prime notes adopted (g20 narrowed; Remote NOW first; custodian one dry loop before root; Goodhart simulation before any live mint; in-graph name `codex`, "Sanctuary" only in doc text; parents_at backfill; deterministic renders; suite green throughout; chakras as vision text; USDC behind the human gate) · split into loops, START NOTHING until a season rollover (core + Prime branches; thought-master independent till the 09-19 check-in) and the Prime naming fix · every pay/incentive rule a config cell, including the equations · the byte round-trip becomes a plain check, never a cross-file coordination event · chakra ruler = vision text for every town, most for codex (IOMap-heavy).

## PRE-L6 (this stream, sanctuary-master rounds, no loop opened)
```
SM.113  REMOTE THOUGHT TOWN  the plan's "Remote NOW" (7 steps: clone on the town box, box cell on thought-master/director-thought rows, ONE guard skip rows whose box != this box, 5-min fetch+read cron, own .env + own provisioning key, own suite + lock, key copy or re-mint) -- VERIFIED ON A VM / second Unix user on this box as the stand-in box NOW (the town boxes are dark: power outage, back later), flipped to the real box when it answers
SM.114  PRIME NAMING          corrective on SM.107: successor window name from ladder cells (belam-S<season>-L<loop>-<numeral>, restart at I on a token change), mantle/brief text, the belam-chain grep and the 5 belam-S1 tests moved to the pattern; first rotation after rollover = belam-S2-L6-I
SM.115  SEASON ROLLOVER       season.py align + global (SM.104): core-town + Prime branches only; thought-master's trunk untouched; on the Prime's word, after 113/114 land; then L6 opens
```

## L6 SEED — goal:g20 (HEAD 0 + HEAD 1 / 1.5 / 1.6 ONLY)
```
HEAD 0    town:codex + 3 visions (owner text; chakra ruler as vision text) + council-codex / codex-master / director-codex rows (master-sensei, config-only, woken once)
HEAD 1    ONE record kind on refs/ledger/<post> (rings canonical bytes, exists) · git commit signing with seat keys, verified by the gates · parents_at {id, mint, grid_sha} on every new version + a BACKFILL report for the 3.3k live nodes (derived from grid history; unknown marked) · ledger.append = signature + nonce + CAS; ledger.tx = ref transaction / push --atomic · intent -> commit -> expiry classifier
HEAD 1.5  THE renderer: brief.py render --post --at <sha> (card, brief, role doc, viewport, GOALS, COMPLETE = views; deterministic; byte-identical at a SHA = a unit test) · config:box (aliases, paths, tmux, users; every literal leaves code and .geometry; rotate.py "belam" x34 -> 0) · agi init --box / --project, agi doctor, agi up
HEAD 1.6  one Unix user per post + role groups · custodian DRY (non-root: verifies grant records, prints the usermod/setfacl it would run) for the WHOLE loop · comms as message records (the 5 inbox file kinds retire) · nudge = derived ("N unread since <sha>")
DONE      town:codex live · every live post has a ledger ref with >= 1 record · Prime commits signed · parents_at on 100% of new versions + backfill report node · card/brief/GOALS render byte-identical at HEAD · rotate.py literals 0 · custodian dry log for one full loop · links 0 · goals byte-identical · active never drops · suite green at every landing
```

## L7 RECORDS + LEDGER — goal:g21
receipt records from provisioning leases (PoS) · witness kind in the canonical form · votes with key images · a PR-shaped submission through the merge-up gate with a fee receipt · credit / vest / fee / churn / rank as FORMULA CELLS (schema-declared expressions, safe evaluator, defaults; a new equation = one config write) · block-day deterministic recompute · GOODHART SIMULATION: replay the grid history under the mint rule, publish the distribution, tune decay + per-node cap BEFORE any live mint · dues/rank/churn_n cells · TIER 1 posture doc.

## L8 CUSTODY — goal:g22
custodian ROOT (after L6's dry loop; closed vocabulary, no shell) · TSS shares (session · custodian · owner device) · Prime 2-of-3 · treasury vault n-of-m · USDC intake · yield -> burn · HUMAN SECURITY-REVIEW GATE recorded on the goal before any real value.

## L9 SANCTUARY SERVICE — goal:g23
the git service behind an MCP face (Forgejo first, Radicle-shaped later) · agi as genesis tenant · subs / credits · hub pre-receive hook: signature-verified fast-forward-only refs (same human review gate: it becomes the only write path) · live nudges = ref-update events + a 5 s fallback poll of the HUB.

## L10 MARKET + CAPSULES — goal:g24
capsule record (public id/owner/commitment/terms; sealed body) · rotate-on-transfer · rent = expiring capability block · GPU-time listings + receipts · prohibited_kinds enforced at mint and transfer · NO exploit lane (owner ruling 10:0xZ).

## LATER (no goal yet)
Monero stealth payouts · CLSAG anon votes · RandomX idle mining · zk · confidential compute · TIER 2 convertibility · DUNA at 100 members · session name folded into the auth chain (owner 14:5xZ).

## Gates (every loop, unchanged from L5) + one addition
merge-base · merge-tree clean vs live HEAD · no node deletions · read the bytes · verify · one suite window per landing · push · one [go] line · goal note in the same commit as the render · PLUS: no root custodian, no hub write hook, no real value without the human security-review gate on the loop's goal.
# doc:l6-plan

## Agent Notes
seed source = .agi/context/l6-redesign-seed.md (the council plan copied verbatim, overlay addresses scrubbed to aliases per the anonymization rule); the live file ~/agi-side/redesign-plan.md stays the council side seat only writable file
