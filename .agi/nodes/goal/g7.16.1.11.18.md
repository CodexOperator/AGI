---
id: goal:g7.16.1.11.18
mint_id: 74ea2baf5b2745c1b67241939830c1c9
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: all-is-one
goal_id: G7.16.1.11.18
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.16.1.11
status: active
tags:
  - council
  - design
  - g7.16.1.11
  - k1
  - k2
  - k3
  - spawn
title: "G7.16.1.11.18: K spawn classes -- a no-tool spawn is ONE streamed inference request inside the caller's uid; a tool-loop spawn runs as its own DynamicUser kid in no store-writing group, on a per-spawn capped key the caller never holds"
town: core
---
# goal:g7.16.1.11.18

## Why this exists
goal:g7.16.1.11: the owner's 18:1xZ 10-02 line (below) asked the council for K1 per-spawn keys, K2 two spawn classes and K3 a direct inference lane. The council split by inbox ts (18:17Z): self-perpetuating K1, all-is-one K2 + K3. The designs are on the trunk: Z4.9 (df762369c: the class line is TOOLS, not trust, because a same-uid process reads the post's 0600 ~/.ssh key and pi's default tools are read, bash, edit, write), Z4.10 (cb037634f: alive's catch, measured by getfacl: group agi is rwx on the shared .git refs + objects and on the inbox dir, so a kid in that group could move ANY ref), and K1 fitted into AA2 by self-perpetuating (agi-mint@, LoadCredential). No leaf held the build, so it waited on nobody's design and nobody's build (belam [owner] 01:5xZ 10-03: "everyone is waiting on someone else"); belam 02:19Z: all-is-one mints this leaf, K3 may start as a round.

## OWNER 2026-10-02 18:1xZ, verbatim (belam [owner] 18:16Z; banked town:local-maxxing Agent Notes 4f647b6a8)
"Okay you have an Openrouter provision key in the Doppler access. The provision key 2 is the one to use. It’ll allow Openrouter provision and is how the pi paid lanes spawn. We just need to incorporate grabbing one as we spawn a kid instead and using it for the pi code app. Eventually I want to have it use direct inference as all we need is a submit of context and then intercept the stream as command line stuff/session log. But I know that part it might just be useful to use pi for now it might break the budget later and might really benefit from a full on app on an actual language not just shell wrappers. But idk I was wondering, could we just use shell wrappers for raw inference given all the other mathematical guardrails? The provision key makes it so that a new user per spawn is no big deal or we can have parents and kid classes be spawned inside of the same user as the post that called them. Or have both as options for different things. Let the group know. Also we should have a way to send messages without using send.py at all just a simple shell command to send stuff to someone else’s inbox if they have permission to do so via user perms and our other clever guard combos. I don’t believe it’s that complicated it needs a python file, a message sent is just a git commit to the appropriate branch or nearest remote head and a local box cron takes care of cascading it down into the appropriate branch then worktree via the other location references the posts hold."
OWNER correction, verbatim: "Provision key is already here in the .env that’s how the paid pi lane worked"

## Target end-state
- K2(b) INSIDE the caller's uid = a spawn that runs NO tool: one inference request, context in, text out. agi-infer (829 B, OpenAI-compatible, schema-fenced) gains streaming: "stream":true + a 115 B line parser (curl -sfN | sed | grep | jq) teed into the session log; the runner commits the full text as the phase's result ref. It takes a flow's one-shot review / check / research / brainstorm stages.
- K2(a) a NEW uid per spawn = ANY spawn with a tool loop (pi, or any agent): template unit agi-kid@<caller>--<kid>, DynamicUser=yes, NO SupplementaryGroups, the slice bind-mounted read-only + its own scratch, no view of the caller's 0750 home; its result leaves through the launcher (refs/spawn, AA2), which signs it.
- K1 the kid's key: minted root-side by agi-mint@<caller>--<kid> from the provisioning key in MAIN .env, capped (the cap read from the graph, never the caller), handed by LoadCredential to K2(a) or 0600 to the caller for K2(b), revoked when the unit stops. The provisioning key is never in any post's env.
- Perpetual posts stay rows = their own users (agi-post@), unchanged.

## Invariants
- A kid joins no group that can write a store (Z4.10), including after AA1.R's per-post stores.
- No post reads or prints a key VALUE; names and perms only.
- Every root act (the agi-kid@ and agi-mint@ units, the polkit rule, the kid cell on belam's row) is its OWN belam GO: one line = command + before-state + one-command rollback.
- 0 B in the zygote; the base stays <= 8,192 B.

## Falsifier
1. (test file ceiling 1,100 B, DG1 [rule] 03:3xZ 10-03, was 1,000: measured 829 -> 960 parser -> 994 key guard -> 1,067 provider-error clause -> 1,077 digit/inherited-k guard on dg2-k3-mu2 f2a7c83ce; past 1,100 B needs a new [rule]) Z4.j + Z4.l (K3, no root): sh extensions/agi/tests/k3-infer.t.sh exits 0: a K2(b) spawn starts no process but curl, sed, grep, jq, and the streamed text == the committed result byte for byte (canned SSE incl. ': OPENROUTER PROCESSING' comments + [DONE]).
2. Z4.k (K2(a), as root, AA2.44): inside an agi-kid@ unit, cat of the caller's ~/.ssh/id_ed25519 fails EACCES, id -G holds no agi, git update-ref on the shared .git fails EACCES, and the result ref verifies under the launcher's AA2 signature.
3. K1 (self-perpetuating's): the kid's key spends at most its cap (server-side refusal past it), and the caller's env and files never hold the provisioning key name or a minted key value.
4. Negative: git grep -n SupplementaryGroups -- .agi/nodes/.geometry/ shows 0 hits in the agi-kid@ unit.

## Out of scope
goal:g7.16.1.11.11 (M1 mail = AA1 boxes, alive) · goal:g7.16.1.11.12 (AA2 rotations; K1's mint unit lives in AA2's units) · goal:g7.16.1.11.15 (phase W, the skill pass; held until the flow-rotation design, now released to DG1) · a shell twin of pi's tool loop (stays in pi until one proves parity).

## Agent Notes
Assigned to **all-is-one**.
