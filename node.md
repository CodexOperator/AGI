---
id: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
mint_id: 95a5ec0892db44249e4b46f153e4fdf4
type: hypothesis
parents:
  - goal:g5.27
next_edges: []
edited_by: director-engine
scaffold_hash: 60168a69ee34cb1b
season: 2
testable_claim: The rendered pi argv carries --no-context-files exactly once with every prior element intact, and every rendered pi parent and kid brief carries the paid-for path guard from one brief.py constant.
title: "pi agents load NO context file (--no-context-files in pi.toml) and the pi role briefs carry the paid-for path guard from one constant: ~14,000 tokens off every pi turn (CTX.01, TMM.99 + the owner)"
town: local-maxxing
---
# hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard

## Measured
- extensions/agi/templates/harness/pi.toml:6-11 -- the pi argv is DATA (harness_template.render, pi_adapter.py:223-224) and
  carries no --no-context-files, so pi's own context discovery walks cwd -> / and loads every AGENTS.md / CLAUDE.md it
  meets, deduped by PATH: in a worktree that is the worktree copy AND the main checkout's = 2 copies. director-thought's
  CTX.01 (experiment:a00-e98ba376-7ff2aa, harvest c83d904440 on DT's branch): a stub recorded pi's first request at
  56,019 bytes with context files vs 1,751 without = -54,268 bytes, ~14,040 tokens per pi turn; only Project Context differs.
- DT's coverage table (datasets/brain-swap/2026-09-24/a00-e98ba376-claude-heading-coverage.md @c83d904440): of CLAUDE.md's
  10 sections, the ONE rule a pi parent or kid acts on that its head / role brief / orders do not already carry is the
  paid-for path pair -- never create .agi/bin/snapshot-build-site.py or .agi/bin/render-context.py, never recreate
  .agi/context/kits/ or .agi/context/plans/build-site.md. The rest is director / owner / orientation material.
- brief.py:1759 and :1801 -- the pi parent briefs' forbidden line ("no push, no sync, no rebase, no `grid.py`, ...")
  carries no such path guard; the kid brief's forbidden line likewise (find it by the same phrase).
- _append_prompt_args (pi_adapter.py:97-110) delivers the head, brief and skill prompt through --append-system-prompt,
  which --no-context-files does not touch.
## CLAIM
pi agents load NO context file: pi.toml's argv gains "--no-context-files" (one template element), and the paid-for path
guard becomes ONE module constant in brief.py that every pi role brief's forbidden line references. A worktree pi agent's
first request then carries 0 copies of CLAUDE.md (~14,000 tokens less per pi turn) and still carries the one rule it
would otherwise lose. The --append-system-prompt entries are unchanged.
## Dispatch line
config-max: none / template-max: pi.toml gains ONE argv element "--no-context-files" / code: brief.py -- ONE module
constant (the guard clause) referenced by each pi role brief's forbidden line, no literal copies
## FALSIFIERS
- the rendered pi argv lacks --no-context-files, carries it twice, or loses any existing element
- a rendered pi parent or kid brief lacks the guard clause, or the clause exists as more than one literal
- test_adapters.py, test_brief.py, test_brief_render.py or test_briefing.py red after the change
## TESTS
new: test_adapters.py::test_pi_argv_loads_no_context_files (the rendered argv carries "--no-context-files" exactly once,
every prior element intact) and test_brief_render.py::test_every_pi_role_brief_names_the_paid_for_path_guard (the parent
and kid briefs carry the clause from the one constant). Neighbours: test_adapters.py, test_brief.py, test_brief_render.py,
test_briefing.py.
## FILE SCOPE
extensions/agi/templates/harness/pi.toml (all 12 lines)
extensions/agi/bin/brief.py -- the pi role briefs' forbidden lines (~1755-1805 and the kid brief's equivalent) + one constant
extensions/agi/tests/test_adapters.py, extensions/agi/tests/test_brief_render.py (append only)
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn) ·
~6 production lines + 1 template element · 0 USD · lean (TMM.94)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine on TMM.99 (TM 04:13Z: CTX.01 GO, one build round) and the OWNER's question in this pane 04:2xZ, verbatim: 'Do we even need Claude Md I thought parent and kid role doc took care of everything'. DT's own coverage table shows the only operative rule a pi parent or kid would lose is the paid-for path guard, so this round builds ZERO copies plus the guard moved into the brief, not TMM.99's one copy: ~14,000 tokens per pi turn instead of ~7,000. Parent goal:g5.27 = the home of the harness leaves (AGI_HARNESS export, per-harness max_live); DT's hypothesis:lm-pi-agents-load-claude-md-twice lives on DT's branch (@c83d904440), not yet in this tree.
<!-- THOUGHT:END -->
