---
id: config:vetoes
mint_id: bcb38232a5b54b6aaff540aab310af22
type: config
parents:
  - hypothesis:l4-a-veto-freezes-never-frees
next_edges: []
active_gates: []
edited_by: belam
expiry_seconds: 86400
rate_limit_per_window: 2
scaffold_hash: 0558542fb6a84c50
veto_room: veto
vetoes: []
window_seconds: 3600
---
<!-- BODY:BEGIN -->
# config:vetoes

RUNG 3's human-gate geometry (hypothesis:l4-a-veto-freezes-never-frees). One
node carries the rate-limit/expiry bounds AND the live freeze state AND the
veto log -- so every veto/expiry/answer lands in ONE file, and the "an
unanswered gate freezes, never frees" property is just this node still
carrying an ``active_gates`` entry whose ``answered`` is empty.

`active_gates` is the human_gate state: a council+Keep majority veto (a
rungs.verify_ring m-of-n over the FULL veto fields) appends a freeze entry
here for its scope with an EMPTY ``answered``; every gated Prime-scope act
(`is_frozen`) refuses by name while that entry stands. Only an owner answer
in the `veto_room` fills `answered` and clears it -- a timeout, a restart or
a rotation never does. `vetoes` is the append-only log of what was filed,
when it expires, and whether the owner answered it.

`rate_limit_per_window` vetoes per `window_seconds` are allowed on one scope;
the (N+1)th is refused. `expiry_seconds` is the authority window a veto has
to SET a gate -- a veto past it is inert (it can no longer set a gate; a gate
it already set stays frozen until answered, by the never-frees rule).

Defaults: this cell is absent/empty on a normal tree, so a scope is FREE. The
node is READ ONLY by gates; only veto.py's own accept/answer path writes here.
