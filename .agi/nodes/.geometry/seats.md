---
id: config:seats
mint_id: 3e88873e3c204c5088f6ab81322a26de
type: config
parents:
  - goal:g17
edited_by: owner
locations: {}
scaffold_hash: ea45aa757f70e3ef
seats:
  - {"name": "belam", "role": "prime_director", "tier": 3, "harness": "claude-code", "model": "claude-fable-5-1", "effort": "max", "settings": "ultracode", "session_kind": "remote-control", "personality_ref": "", "handoff_file": "<graph_root>/HANDOFF.md", "pin_ref": ".agi/sessions/belam.meter", "rotated_by": "quorum", "owning_goal": ""}
  - {"name": "adv-self-perpetuating", "role": "parent", "tier": 3, "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "", "session_kind": "remote-control", "personality_ref": "vision:self-perpetuating", "handoff_file": "", "pin_ref": ".agi/sessions/adv-self-perpetuating.meter", "rotated_by": "prime", "owning_goal": ""}
  - {"name": "adv-all-is-one", "role": "parent", "tier": 3, "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "", "session_kind": "remote-control", "personality_ref": "vision:all-is-one", "handoff_file": "", "pin_ref": ".agi/sessions/adv-all-is-one.meter", "rotated_by": "prime", "owning_goal": ""}
  - {"name": "adv-alive", "role": "parent", "tier": 3, "harness": "claude-code", "model": "claude-opus-5", "effort": "max", "settings": "", "session_kind": "remote-control", "personality_ref": "vision:alive", "handoff_file": "", "pin_ref": ".agi/sessions/adv-alive.meter", "rotated_by": "prime", "owning_goal": ""}
  - {"name": "liaison", "role": "director", "tier": 1, "harness": "claude-code", "model": "claude-sonnet-5", "effort": "high", "settings": "", "session_kind": "remote-control", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/liaison.meter", "rotated_by": "quorum", "owning_goal": "goal:g17"}
  - {"name": "dir-g1", "role": "director", "tier": 1, "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "high", "settings": "", "session_kind": "fire-and-forget", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/dir-g1.meter", "rotated_by": "advisor", "owning_goal": "goal:g1"}
  - {"name": "dir-g15", "role": "director", "tier": 1, "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "high", "settings": "", "session_kind": "fire-and-forget", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/dir-g15.meter", "rotated_by": "advisor", "owning_goal": "goal:g15"}
  - {"name": "dir-g16", "role": "director", "tier": 1, "harness": "pi", "model": "~z-ai/glm-flash-latest", "effort": "high", "settings": "", "session_kind": "fire-and-forget", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/dir-g16.meter", "rotated_by": "advisor", "owning_goal": "goal:g16"}
thought_session: 7af11157
---
<!-- BODY:BEGIN -->
# config:seats

The seat registry (hypothesis:l3w4-seat-registry, goal:g17). One row per
active seat declares that seat's whole configuration — name, ladder role and
tier, harness, model, effort, settings, session kind, personality ref,
handoff file, meter pin ref, who rotates it, and the goal it owns. The graph
carries the seats; `dispatch.py --seat <name>` and `rotate.py meter --seat
<name>` read them.

Owners (owner text 2026-09-07, recorded in
`.agi/context/l3-command-ladder-brief.md`): the orienting correction (owner 4)
overrides the earlier draft (owner 3) — **quorum is opus on max, director-kids
are opus on high effort; parents and kids as they are now.** Thus belam
fable-5.1/max/ultracode, the three advisors opus-5/max (no ultracode), the
liaison sonnet-5/high owning goal:g17, and one opus-5/high director per
perpetual goal besides g17 (dir-g1, dir-g15, dir-g16). pi parents/kids (tier-0
role `parent`/`kid`) are unchanged, as the owner said — they were not granted
seats.

`pin_ref` is seat-stable: `.agi/sessions/<name>.meter`, written by the code
that already writes `<agent_id>.meter`, keyed off `AGI_SEAT` instead of an
agent id — no graph write, no race on this node.

The `locations: {}` field is present because the `config` type requireds
`locations`; this node's real declaration is `seats`, so the field is empty
rather than a redundant restatement of the shared filesystem facts in
`config:secrets`.

## Agent Notes
OWNER GO, 2026-09-07 22:5x UTC (verbatim: '6.36: go' and, on the open half, 'as far as quorum leave on opus max'). Applied by Belam VII as the owner's own ladder assignment, actor owner. CHANGED, three rows only: dir-g1, dir-g15 and dir-g16 move from claude-code / claude-opus-5 / high to harness pi, model ~z-ai/glm-flash-latest, effort high - the mechanism for this was built and reviewed in L3.32 (hypothesis:l3w4-director-kids-on-glm) and the kid deliberately left the data alone because the owner had only said 'I am considering'. Now it is a decision. UNCHANGED, deliberately: the three advisor seats stay claude-opus-5 max - the owner settled the open quorum question in the same breath, and GLM flash is too weak to arbitrate a 1-1-1 morals split; the liaison stays claude-sonnet-5 high because the owner named that model for the seat that talks to them and it is already the cheapest subscription seat; belam stays fable-5.1 max ultracode (item 13). ONE CONSEQUENCE THE OWNER SHOULD KNOW, changed here rather than left silently wrong: the three flipped rows also move session_kind from tty to fire-and-forget, because a pi spawn is not an interactive session and cannot hold a tty seat the way a claude-code seat does. That means these three director-kids are NOT yet perpetual - they run and exit - and they become perpetual only when hypothesis:l3w4-seat-rotation-loops lands its live proof (rotate.py alarms and rotate-self exist and are tested but no live tmux rotation has ever been observed). Until then this change buys the token saving, not the persistence.
