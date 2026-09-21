---
id: hypothesis:a00-89094f2f-940a6c
mint_id: 24239a206be845198e9a74874710b6f6
type: hypothesis
parents:
  - goal:g7.25.2
next_edges: []
edited_by: belam
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 686d3725ece63589
season: 2
testable_claim: "The harnesses.grok-bot row is the FIRST-CLASS cell adapters.resolve reads: inserting exactly the parent-supplied row (adapter grok_bot, bin /home/ubuntu/.npm-global/bin/grok-bot, models kid grok-4-fast parent grok-4, allowed_extra [grok-4, grok-4-fast], NO provider key) into an in-memory copy of the live .agi/config.json makes resolve(cfg,\"grok-bot\") return (\"grok-bot\", row) with row[\"adapter\"]==\"grok_bot\" and row[\"bin\"]==\"/home/ubuntu/.npm-global/bin/grok-bot\" (E1), all four peers still resolve (E2), the dash-name to underscore-module default survives deleting row[\"adapter\"] (E3); GATE: a decisive verdict carries evidence_runs as a LIST of node ids and probes as a list of per-conjunct dicts, and dispatch.py stays grok-free, zero edits (E4) -- the exact shape the MUR defect lacked (scalar evidence_runs + uncommitted harness row); WIRE: on the REAL loaded cfg without the row resolve raises AdapterError naming the declared harnesses and with the row it resolves, and .agi/config.json stays byte-identical to HEAD because cli.py round-scope excludes it, so the row can only land via a director-owned commit and merge-up must preserve it (E5)."
thought_session: parent-residue-g14-g17-remap
title: Grok-bot config row is a first-class landable resolve cell and its verdict must carry list evidence_runs
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-89094f2f-940a6c

## Hypothesis

The `harnesses."grok-bot"` row in `.agi/config.json` is a FIRST-CLASS
LANDABLE BUILD, not a decoration, and a decisive verdict about it must carry
`evidence_runs` as a LIST. Three meta-points are bound into one claim:

(a) **AUTH — the row is the cell `adapters.resolve` reads.** Adding exactly
    the parent-supplied row (`adapter: grok_bot`, `bin:
    /home/ubuntu/.npm-global/bin/grok-bot`, `models.kid: grok-4-fast`,
    `models.parent: grok-4`, `allowed_extra: [grok-4, grok-4-fast]`, NO
    `provider` key) to an in-memory copy of the live config makes
    `resolve(cfg, "grok-bot")` return `("grok-bot", row)` with
    `row["adapter"] == "grok_bot"`. The dash-name → underscore-module
    default is what carries it even with `adapter` deleted.

(b) **GATE — a decisive verdict carries `evidence_runs` as a list.** The
    exact MUR defect (`mur-g17-14-1-...-g17-14-3-...`) was a SCALAR
    `evidence_runs` plus an uncommitted harness row. This round mints the
    meta-claim as fresh nodes whose `evidence_runs` is a YAML list of node
    ids, never a bare string, and whose `probes` is a real list of dicts.

(c) **WIRE — the row, and only the row, makes the name resolve; merge-up
    must not discard it.** On the REAL loaded config without the row,
    `resolve(cfg, "grok-bot")` raises `AdapterError` naming the declared
    harnesses. Because `cli.py`'s `_round_scope_ok` excludes
    `.agi/config.json` from round commits, the row can only land via a
    director-owned commit; any merge-up must preserve it, and
    `dispatch.py` must stay grok-free (zero edits).

**Would prove it:** E1 `resolve` returns the expected tuple; E2 all four
peer harnesses still resolve; E3 the dash-default survives `adapter`
deletion; E4 `grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints
nothing; E5 the real config raises without the row and resolves with it,
while `.agi/config.json` stays byte-identical to HEAD.

**Would disprove it:** any peer resolving fails, the row does not resolve,
the dash-default does not apply, `dispatch.py` mentions grok, the real
config resolves without the row (row is not load-bearing), or the working
tree's config is dirtied.

**Explicitly out of scope:** the `grok_bot_adapter.py` file is owned by
`goal:g17.14.1`; this chain tests the config cell, not the module.
