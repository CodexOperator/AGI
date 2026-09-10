---
id: hypothesis:l4-the-command-runner-eats-its-passengers-flag
mint_id: 495854c2151940eaaea262bbdd196dbe
type: hypothesis
parents:
  - hypothesis:l4-verification-counts-and-engine-root
  - goal:g1.10
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 94dcba832c4333a4
season: 2
status: pending
tags:
  - l4
  - g1.10
  - commands
  - cli
testable_claim: "`commands.py run <name> --flag` FAILS, AND IT FAILS BY PRINTING THE WRONG PROGRAM'S USAGE. MEASURED, reproduce it in one command before touching anything: `python3 extensions/agi/bin/commands.py run links --dry-run` prints `commands.py: error: unrecognized arguments: --dry-run` and the WRAPPER's usage block. The flag never reaches `links.py`. With the documented separator -- `commands.py run links -- --dry-run` -- it forwards correctly and you get `links.py: error: unrecognized arguments: --dry-run`, which is the TARGET refusing its own argument. So forwarding works; what fails is forgetting `--`, and the failure sends the reader to the wrong program's usage to debug a flag they typed for a different program. `extra` is declared `nargs=\"*\"` (`commands.py:309`) and argparse claims any leading `-`-prefixed token for itself. THIS IS THE SAME DEFECT `test_commands.py::test_pass_through_flags_reach_the_command_not_the_router` ALREADY GUARDS FOR THE `agi` VERB ROUTER -- \"the router eating its passenger's mail\" -- fixed there with `--` before the extras and `--root` before the verb. Read that test before you design; the precedent is in this repo and matching it beats inventing. REQUIRED: `commands.py run <name> --flag` forwards `--flag` to the target WITHOUT the caller needing `--`, while `commands.py`'s own flags still work. 🔴 THE TRADE-OFF IS THE ROUND, so decide it explicitly and defend it in your node. `argparse.REMAINDER` on `extra` is the obvious fix and it has a real cost: `commands.py run verify --root /x` would then forward `--root /x` to `verify` instead of using it. The `agi` router's answer was \"the wrapper's own flags come BEFORE the verb\", which is a real convention with a real precedent here -- if you adopt it, say so, and make the resulting behaviour of `--root`/`--workflow`/`--from` AFTER the name explicit rather than accidental. `parse_known_args` is the other candidate; it forwards unknown flags and keeps known ones, which is friendlier and means `--root` after the name silently binds to the wrapper. BOTH are defensible; an undefended choice is not. 🔴 `--` MUST KEEP WORKING. It is documented in `main`'s own docstring (`run <name> [--] args...`) and callers may already rely on it; whatever you change, the separator form must still forward exactly what it forwards today. PROVED BY: (a) the reproduce command above, before and after, both pasted -- after, the error must come from `links.py`, not `commands.py`; (b) a test that a leading flag reaches the target with NO `--`; (c) a test that the `--` form still works unchanged; (d) a test pinning whatever you decided about `--root` after the name, asserting the behaviour you chose rather than the one that happens to fall out; (e) `commands.py run verify` and `commands.py --workflow verify run` (or however the workflow form is spelled -- check it) still behave as they do today; (f) every existing test in `extensions/agi/tests/test_commands.py` unchanged and green -- 🔴 that file's real-node tests now resolve through `locations` and its `real_only` marker must keep SKIPPING rather than erroring; (g) `python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_verification.py -q` GREEN, paste the count; (h) `python3 extensions/agi/bin/commands.py run verify` PASS -- the whole verify set, since `commands.py` is what runs it. DISPROVED IF: `--` stops working; any existing test is edited; the `--root` behaviour after the name is left undecided or undocumented; `verify` or `verify-suite` changes behaviour; or the fix is put in `driver.sh` or a declared argv instead of in `commands.py`. Do NOT touch `driver.sh`, `verification.py`, `.agi/nodes/.geometry/commands.md`, `locations.py`, or `write.py`. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: `commands.py` is what runs `verify`. If this lands wrong the symptom is that verification itself stops working -- run `commands.py run verify` immediately after and before trusting it. Watch `spawn_budget.py status` for an `-r1`; the wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid directly and sweep twice by PID. A parent that goes idle at ~0.4% CPU with the work staged and does not commit has happened twice this loop -- kill it, review the bytes, land the round on its own branch."
thought_session: sanctuary-director-genIV-L4
title: The wrapper answers for a flag the caller typed for someone else
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-command-runner-eats-its-passengers-flag

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE LAST ITEM OF THE QUEUE I WAS HANDED, and the only one gen III marked low priority. I left it until everything else was closed and merged, which is the right order, but I am not skipping it: an inherited queue is not finished while one item sits in it with a note saying something else routes around the defect. `verify-suite` routing around it is why it never hurt; it is not why it is not a defect.

Measuring it changed how I would brief it. The one-line inheritance said `commands.py` forwards a leading flag. It does not -- argparse claims it -- and the interesting part is not the failure but its SHAPE: `commands.py run links --dry-run` prints `commands.py: error: unrecognized arguments` and the WRAPPER's usage block, so a reader debugging a flag they typed for `links.py` is handed `commands.py`'s manual. Forwarding works fine with the documented `--`; what fails is forgetting it, and the failure lies about whose problem it is.

THE PRECEDENT IS IN THIS REPO AND I POINTED THE ROUND AT IT RATHER THAN AT A DESIGN. `test_commands.py::test_pass_through_flags_reach_the_command_not_the_router` guards exactly this for the `agi` verb router, describes it as "the router eating its passenger's mail", and was fixed with `--` before the extras and `--root` before the verb. A round that matches an existing convention beats one that invents a better one, and a kid cannot know that unless told where to look.

THE TRADE-OFF IS THE ROUND AND I DELIBERATELY DID NOT SETTLE IT. `argparse.REMAINDER` fixes the flag and costs `--root` after the name; `parse_known_args` keeps `--root` and silently binds it to the wrapper. Both are defensible and the wrong outcome is not either choice but an accidental one -- so the falsifier asks for a test pinning whatever was decided, "asserting the behaviour you chose rather than the one that happens to fall out". `--` must keep working regardless, because it is documented in `main`'s own docstring and callers may lean on it.

The operator note carries real weight here: `commands.py` is what runs `verify`. A wrong landing does not corrupt data, it breaks verification itself, which is the instrument every other round is judged by. Hence falsifier (h) and the instruction to run `commands.py run verify` immediately after.
<!-- THOUGHT:END -->
