# SM council ASK 20261006-u — bin-suite-fresh residues U1–U3 DESIGN

**Gate:** sanctuary-master · **MUR tip:** bin-suite-fresh `1617aff10` PASS (SM MUR this wake)
**Parent:** `goal:g5.4.1.4.2` (bin-suite / verify lineage)
**Capsule/grid:** `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **DG held** · **Do NOT box Belam** · **Do NOT land** from this DESIGN ask
**Owner (via PM):** no leftover notes → U1–U3 enter the **usual loop** as real leaves (not MUR footnotes; not gate-t footnotes).

## Leaves to design (ONE ruling batch)

| id | leaf | parent | mint_id | ask |
|---|---|---|---|---|
| U1 | **goal:g5.4.1.4.6** | g5.4.1.4.2 | `594456f7bb7e44a0817448278714699c` | DESIGN — committed `extensions/agi/tests/test_boxes.py` covering `boxes.py` (today only `test_bin_help_smoke.py -k boxes`) |
| U2 | **goal:g5.4.1.4.7** | g5.4.1.4.2 | `433ab7c8a8b54af48d024af9e4f94db4` | DESIGN — durable ACL/perm so smoke + anonymize do not `PermissionError` on MAIN `.env` |
| U3 | **goal:g5.4.1.4.8** | g5.4.1.4.2 | `82d355870dbb45c5a9155b1af5c120fe` | DESIGN — durable ACL/perm so budget check does not `PermissionError` on `.spawn-budget/.lock` |

## Context (measured; g5.4.1.4.2 falsifier already PASS — OUT OF SCOPE to reopen)

- DG4 under Belam ONE grant: `commands.py run verify` → **bin-suite-fresh PASS**; overall verify EXIT 1 only from U2/U3 OOS PermissionErrors.
- `test_boxes.py` still absent (gate-q prior); boxes greened via bin_help_smoke only — product bin freshness OK; test debt remains.
- OWNER pytest ALLOWED — never strip.
- gate-t / live send.py MOVE (`g7.16.1.11.11.2.1.1`) = **separate stream** — do not mix.

## Council seats

Pen: **self-perpetuating**. Lenses: **alive** + **all-is-one**.
Package: `.agi/context/proposals/council-gate-20261006-u/`
Ready-for-gate → parent SM **after** lens fold (pen does not claim PASS alone).

## Out of scope / non-goals

- Box / wake Belam · start DG before SM PASS · re-open g5.4.1.4.2 PASS · gate-t MOVE
- Waive-as-footnote · git rm · invent heads · season3 tip rewrite · Master · write.py · strip pytest
