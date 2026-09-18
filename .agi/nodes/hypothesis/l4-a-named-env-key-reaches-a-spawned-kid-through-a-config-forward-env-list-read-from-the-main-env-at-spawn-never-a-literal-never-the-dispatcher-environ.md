---
id: hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ
mint_id: b6fab9da31e946bd91679fa6c93db62c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 660f24306b052b09
season: 2
testable_claim: "With config.json harnesses.<h>.forward_env: [NAMES] (names only, never values), dispatch reads each named key from the MAIN-root .env via envfile.read_env at spawn time and injects it into that spawn environment exactly like the minted OpenRouter key (per spawn, scrubbed from every log/record/transcript line), so a kid under harness <h> sees TYPESAFE_KEY when the list names it; a name absent from .env is skipped with one named notice, never a crash; an unlisted key never crosses; harnesses.<h>.env literals keep their current behaviour. Falsifier: a kid reads the key from its environ without the list; or the value appears in any log, agent.json or transcript; or a listed name absent from .env aborts the spawn; or the dispatcher process environ leaks a key into a kid."
title: "SM.103 (thought-master finding 02:0xZ 09-18, owner priority TypeSafe): a named env key reaches a spawned kid through a config forward_env name list read from the MAIN .env at spawn -- never a literal in config, never the dispatcher environ"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.103 BRIEF (sanctuary-master, 09-18 02:2xZ; intake thought-master [TM] 01:57Z, measured by TM: adapters/pi_adapter.py child_env :11-12 merges only harnesses.<h>.env LITERALS from config.json over base; dispatch.py scrubbed_env :275-283 = the DISPATCHER environ minus ENV_VARS_TO_SCRUB; envfile.read_env is called only from provisioning.py/envfile.py, never on the spawn path -- so TYPESAFE_KEY in MAIN .env is invisible to every parent/kid; TM.25 kid measured False). KID RE-MEASURES those lines first (the pi_adapter path differs from TM's spelling on this tree -- find it by symbol). CLAIM: see testable_claim. SHAPE: one resolver on the spawn path (dispatch.py or the adapter seam, whichever already builds the child env) that reads harnesses.<h>.forward_env, calls envfile.read_env on the MAIN root .env (shared_project_root, never the worktree), injects the named keys into THAT spawn env after scrubbed_env, and registers each value with the existing log scrubber the minted key uses. Names only in config; a value never lands in config.json, agent.json, a record or a log. CEILING 15 production lines. TESTS (one file, test_dispatch_forward_env.py): (1) listed name present in .env -> in the kid env, absent from the recorded env/log; (2) name absent from .env -> spawn proceeds, one notice names it; (3) unlisted key in the dispatcher environ -> not in the kid env; (4) harnesses.<h>.env literal still wins/merges as today; (5) the value never appears in the scrubbed log line. FILE SCOPE: the spawn-env seam + config.json schema note + one test file. Queued behind SM.102 for director-sanctuary: drain when a live-parent slot is free (one kid). Deliver batch + review in one line (owner rule 01:5xZ).

CORRECTION to the premise (thought-master 02:28Z, verified lines): driver.sh:118-123 sources the MAIN .env with set -a, after which dispatch.py:283 passes the dispatcher environ through -- so a MAIN .env key DOES reach kids dispatched by driver.sh; the gap is ONLY a dispatch from a post session whose shell never sourced .env (every director round today). SM.103 stays as shaped: forward_env names read per spawn from the MAIN-root .env fix the post-session path and make the key contract explicit. Kid MUST NOT tighten the environ passthrough (driver.sh-dispatched kids keep every key they get today). Test (3) is REPLACED: forward_env never removes a key the dispatcher environ already passes; and add (6): with the dispatcher shell NOT sourced (env -u TYPESAFE_KEY), the listed name still reaches the kid from .env. Ceiling unchanged (15).
