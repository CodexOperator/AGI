---
id: hypothesis:l4-the-mode-is-declared-not-remembered
mint_id: 4f6d8b8c9de24752b9af9a2319e614f7
type: hypothesis
parents:
  - hypothesis:l4-five-unstaffed-seats-specified-none-created
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b0f97c5802b64608
season: 2
status: pending
tags:
  - l4
  - g17.1
  - config
  - brief
testable_claim: "THE OPERATING MODE IS REMEMBERED IN PROSE, IN EVERY BRIEF, AND MUST BE DECLARED IN CONFIG AND RENDERED INSTEAD. Plan item L4.26, unblocked, no owner-go. THE OWNER NAMED TWO ARRANGEMENTS (`doc:l4-owner-decisions:265`, quote them verbatim in the node): **survival** -- \"only two persistent seats active each helping the other to conserve the resource that matters most\", the Prime and a single director-kid aimed at a loop brief; and **ultimate survival** -- \"Prime is powered by opus and single remaining director runs off sonnet or even openrouter\". 🔴 A THIRD ARRANGEMENT IS WHAT IS ACTUALLY RUNNING AND YOU MUST NOT SILENTLY RECONCILE IT. This loop runs **ENHANCED SURVIVAL** (`goal:g17.1`) -- Prime plus a point director plus a helper, three seats, not two. It is in force, it is not one of the owner's two, and the plan row does not mention it. DECLARE WHAT EXISTS: all three, each with a source (owner text with its line, or `goal:g17.1`), and mark plainly which is IN FORCE. Do NOT invent an arrangement nobody named, do NOT quietly fold enhanced into survival, and do NOT change which mode is active -- declaring a mode is not switching it, and switching is the owner's. REQUIRED: (1) the three modes declared in `.agi/config.json` under one key, each with its seats, its models where the owner named them, and its source citation; (2) `brief.py` RENDERS the active mode into the brief it assembles, so an agent READS the mode rather than being told it by whoever wrote the prompt; (3) the rendering is driven by the declaration -- change the declared active mode and the rendered brief changes, with no second copy of the mode text in code. PROVED BY: (a) the three declarations, quoted, each with its source line; (b) a test that the rendered brief carries the ACTIVE mode's text; (c) 🔴 THE ONE THAT MATTERS: a test that flipping the declared active mode in a FIXTURE config changes the rendered text -- that is what proves it is read and not hardcoded, and a round that only asserts today's string has built a fifth copy of the prose it was sent to delete; (d) a test that an ABSENT declaration renders nothing and raises nothing, so a project that has not declared modes is unchanged; (e) the LIVE config still declares enhanced survival as in force after your change -- paste it; (f) `python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py -q` GREEN, paste the count; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: the active mode changes; a mode is invented or a named one dropped; the mode text is duplicated in code as well as config; an absent declaration errors; an existing test is edited (and if one MUST be, the replacement asserts the SPECIFIC fact the old one obscured IN ADDITION to whatever it counted); or the seat rows in `config:seats` are touched -- 🔴 THAT NODE IS OFF LIMITS, declaring a mode does not restaff anything. Do NOT touch `stall_detect.py`, `provisioning.py`, `cli.py` or `closing_line` -- all landed today. HARD CEILING: 2 kids. Do NOT run the full suite, BUT if you add any file under `bin/` say so loudly in your node: a new file there is auto-enrolled in `test_bin_help_smoke.py` and took season/s2 red this morning. 🔴 OPERATOR NOTE: commit as soon as your work is reviewable. A parent that spawns no kid within ~15 minutes, or idles at ~0.4% CPU with work staged, gets killed by the director watching."
thought_session: sanctuary-director-genIV-L4
title: Two modes were named, three are in play, and the one in force is the unnamed one
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-mode-is-declared-not-remembered

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

