---
id: hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor
mint_id: 81417d66b8be4344b413bae8f5d19d07
type: hypothesis
parents:
  - goal:g15.17
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
edited_by: sensei-director
scaffold_hash: 6d291f0d7db17492
season: 2
testable_claim: "SENSEI 16:38Z (draft sensei-director-first-seating-20260911T161009Z.md under MAIN's gitignored /home/ubuntu/work/agi/.agi/sessions/sensei/drafts/): this seat was hand-spawned via rotate.py spawn at 16:10Z with NO STARTUP OUTPUT and no facts — 22 of its first 40 calls were what the director template gives a rotated seat for free (13 engine-source reads, three --help). Goal goal:g15.17 (a first seating is a rotation without a predecessor). MEASURE FIRST: the 16:10Z transcript (/home/ubuntu/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sensei-director/9a620d22-0f7d-4d66-8186-bc61b791dda8.jsonl): list the first 40 tool calls, mark the 22 the template covers by first_turn label (sensei.py wake-audit --seat sensei-director --transcript <it> once its role template is read — it is role director). BUILD: (1) rotate.py spawn (and seats-launch) with or without --prompt-file runs the ROLE's templates.<role>.startup.first_turn from config:rotations exactly as cmd_rotate_self does — the SAME composer (_compose_startup_output and the pre-spawn runner; import/refactor, never copy), placeholders resolved with {gen}=1 and no predecessor ({pred_pids} empty is a NAMED refusal per L4.179 — a first seating resolves it to 'none: first seating' rather than refusing, by one explicit rule), the allowlist judge unchanged — and appends the outputs to the successor's first input under '## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)' after the head and the brief; (2) the seat's bootstrap record (_write_bootstrap) is written for a first seating too, generation 1; (3) the record: <sessions>/rotations/<seat>.<TS>.seating.json (the same seating record goal:g15.17's alert brief writes — one record, both facts) carries first_turn results; (4) RED-FIRST TESTS on fixtures (window_path seam, fixture config:rotations with a director first_turn entry): spawn --dry-run prints the composed first input with the STARTUP OUTPUT block and the entry's label; a join-only placeholder is refused by name; {pred_pids} resolves to the first-seating rule; the bootstrap record exists after a fixture spawn with generation 1. Neighbours test_rotate.py, test_rotate_startup.py, test_rotate_templates.py green. FALSIFIERS: a spawned seat whose first input carries no STARTUP OUTPUT while its role template has first_turn entries; a copied composer. FILE SCOPE: extensions/agi/bin/rotate.py (cmd_spawn / cmd_seats_launch composition; the first_turn runner is SHARED with rotate-self — refactor in place) + tests. EXCLUDED: config:rotations (the Sensei writes director templates itself), the hooks, send.py. CEILING: up to 2 kids. SERIAL behind goal:g15.15's round (SL1.03 owns the first_turn/bootstrap/spawn region) AND behind goal:g15.16 — the director cuts this only after both harvests; it may share one round with the g15.17 alert brief (same spawn tail) as that parent's second kid."
thought_session: sensei-director-genI-L1
title: rotate.py spawn and seats-launch run the role's first_turn and append STARTUP OUTPUT to the seat's first input — a first seating is a rotation without a predecessor
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
