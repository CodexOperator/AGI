---
id: hypothesis:l4-provisioning-absent-refuses-late
mint_id: d72f161a46d44ef2a7bfd60ba57f207d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 0d9026580e2783cb
season: 2
testable_claim: "When provisioning.available(root) is False AND the runtime key (OPENROUTER_API_KEY) is absent or unusable, dispatch.py's pre-flight currently admits the spawn (check_runtime_key_floor fail-opens on key_usage()==None) rather than refusing before a budget slot is spent. Falsifiable: reproduce that exact state (no provisioning key, no/invalid runtime key) and confirm a spawn is admitted and the spawned agent's first LLM call 401s, before a fix; after the fix, the same state must refuse pre-flight with a named message. Disproved if the current pre-flight already refuses this state somewhere not yet found."
thought_session: sanctuary-helper-cd
title: Pre-flight fails open when neither provisioning nor a usable runtime key exist; a spawned kid discovers the 401 mid-round instead
---
<!-- BODY:BEGIN -->
# hypothesis:l4-provisioning-absent-refuses-late

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.122 brief -- pre-flight fails open when neither provisioning nor a usable runtime key exist

Assigned by sanctuary-director (rotation/verification noted in THOUGHT).

ROOT-CAUSED before writing this, against extensions/agi/bin/provisioning.py
and dispatch.py's pre-flight block (~line 1254) as they stand now:
provisioning.available(root) reports whether a MINTING-capable provisioning
key exists (separate from the shared runtime key, OPENROUTER_API_KEY).
check_runtime_key_floor reads the runtime key's usage via key_usage(root);
when there is NO runtime key at all, key_usage returns None and the floor
check reads that as "no runtime key to guard" -> (True, None), fail-open.
That fail-open is correct when provisioning IS available (a fresh per-spawn
key gets minted instead, so the runtime key gates nothing real). It is NOT
obviously correct when provisioning is ALSO absent: every spawned agent
then inherits the shared runtime key directly per dispatch.py's own
comment ("absence is a supported state ... nothing here changes shape"),
so if THAT key is also missing or unusable, nothing distinguishes "no key
to guard because another mechanism covers it" from "no key at all, and
nothing covers it." The spawned kid would discover this on its first LLM
call (a 401), not before a budget slot is spent.

NOT YET CONFIRMED, real remaining work: I have not traced this to a live
401, and read only to roughly dispatch.py:1260 -- there may be a check
further down I have not seen. Reproduce the absent-both-credentials state
(or find where, if anywhere, it is already prevented) and confirm a spawn
is actually attempted rather than refused, before implementing the fix.

DIRECTION: when provisioning.available(root) is False, add an explicit
check that the runtime key is CONFIGURED AND READABLE (not merely "capped
and within floor") before admitting a slot, refusing with a named message
distinct from the existing floor-refusal wording ("no credential" vs.
"credential too low"). Do not weaken the existing fail-open behaviour for
the cases it correctly covers (network errors; provisioning-available
making the runtime key irrelevant).

Files: extensions/agi/bin/provisioning.py, extensions/agi/bin/dispatch.py
(pre-flight block only), their tests. Kid ceiling 2. No full-suite run.

REPORT: one experiment node stating precisely where in the current code
the gap lives (cite file:line), whether a live 401 was reproduced, and the
fix + falsifier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Point rotated again this generation (sanctuary-director-11 [3d6888] ->
seat-sanctuary-director-16 [4a9edc], third rotation this session). Verified
independently, same as the prior two: tmux+ListAgents join (@245, busy,
matches) and config:seats read fresh at origin/season/s2 HEAD (sanctuary-
director row session_ref 4a9edc, matches). Proceeded on that basis. This
node's brief was root-caused against my own current tree before writing,
not transcribed from the assignment message.
<!-- THOUGHT:END -->
