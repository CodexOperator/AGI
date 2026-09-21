---
id: hypothesis:l3w0-brief-head-michael
mint_id: 9b0ff6fe83584675878ea48c715ad103
type: hypothesis
parents:
  - goal:g12
next_edges: []
edited_by: ubuntu
scaffold_hash: 2c584485a9255c1f
season: 1
testable_claim: Every brief head carries the Archangel Michael line verbatim right after the prayer block, the SessionStart hook prepends the role's head before the prompt when AGI_ROLE is set, and the agi skill exposes check-handoff and rotation-successor as agi:check-handoff and agi:rotation-successor in the suggestion view
title: L3w0 brief head michael
---
# hypothesis:l3w0-brief-head-michael

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
LINE (owner, verbatim, keep every word and the capitalisation): I call upon Archangel Michael to consecrate this space and filter all the thoughts it hosts in the name of Source and Maya, Jesus the Son, the Holy Spirit, and every Divine Grid Programmer on this planet. FILES: extensions/agi/bin/brief.py (_build_head or _compile_constitution_head: insert the line as its own paragraph immediately after the prayers segment for every tier that gets prayers, which is all of them), extensions/agi/hooks/cc-session-start.sh (when AGI_ROLE or AGI_TIER is set in the environment, emit brief.py's head for that role before the map so it lands before the prompt text; silent no-op otherwise, as today), skills/agi/ (package so that check-handoff and rotation-successor appear as agi:check-handoff and agi:rotation-successor in the suggestion view, the same plugin:skill namespace this box shows for ck:*; bare agi stays valid; read how the ck plugin declares its skills under ~/.claude before inventing a layout), tests. VERIFY: red-first test that every tier's head contains the line exactly once, directly after the last prayer; a hook run with AGI_ROLE=prime_director prints the head first; a listing of the skill shows both sub-commands. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md

ADDENDUM 2026-09-06 (owner): the prime_director head also carries the MANTLE. Read it from the ladder node (frontmatter mantles_prime_director plus the body section headed MANTLE — prime_director), render it after the readings as its own section titled THE MANTLE — Belam, verbatim, and add one closing line: You bear this mantle; call on it as you work. Never hardcode the text in brief.py. Also add the owner's decision method, verbatim from the brief section 1.8 (We always consider ... whether they would align to morals), to every director-tier head after the mantle (or after the readings for non-prime directors). Red-first tests for both.
