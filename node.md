---
id: experiment:a00-3a5520d8-5aa48d
mint_id: 51850265a8b04174a39ece29e98f3b2c
type: experiment
parents:
  - hypothesis:l4-rotate-defaults-is-one-top-level-map-the-prime-can-write-as-one-value-timeout-and-closeout-per-role
next_edges: []
confidence: 0.95
edited_by: a00-bd1c1cb7
evidence_runs:
  - experiment:a00-3a5520d8-5aa48d
loop: hypothesis:l4-rotate-defaults-is-one-top-level-map-the-prime-can-write-as-one-value-timeout-and-closeout-per-role@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "_role_timeout(root,\"director\") against (a) config:rotations with templates.director.timeout_s=900 and NO rotate_defaults, (b) rotate_defaults.timeout_s.director=900", "expected": "(a) 600 -- the old per-template read is dead; (b) 900 -- the one top-level map feeds it", "observed": "(a) 600, (b) 900", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "_load_rotate_defaults(root) against rotate_defaults absent / a list / a scalar / the OLD templates.<role>.rotate_defaults cell / a quoted-JSON str cell", "expected": "{} for absent/list/scalar/old-template; the parsed dict for quoted JSON", "observed": "{}, {}, {}, {}, {\"closeout\": {\"director\": true}}", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "_ranks(root) with top-level ranks [helper,director,prime_director] PLUS a hijack rotate_defaults.ranks [prime_director]; and with no top-level ranks", "expected": "top-level ranks wins, rotate_defaults.ranks ignored; DEFAULT_RANKS when absent", "observed": "[helper,director,prime_director]; DEFAULT_RANKS", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "write.py config:rotations --dry-run for BOTH 0a lines on this round tree; git diff HEAD --name-only to check the round never writes config:rotations", "expected": "both lines print a TOP-LEVEL set (no dotted nesting) and the round diff touches no config:rotations file", "observed": "set ranks = [...] ; set rotate_defaults = {...} ; 0 config:rotations paths in diff", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 4ef4fdf9ede0db05
season: 2
title: A00 3a5520d8 5aa48d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3a5520d8-5aa48d

## Experiment

SL7.117 — g15 CLAIM, built on the bytes. The SL7.114/115 readers
(`_role_timeout` reading `templates.<role>.timeout_s`, cmd_rotate's closeout
block reading `templates.<role>.rotate_defaults`) named dotted keys `write.py`
cannot nest on config:rotations — keys the Prime can never write. Implemented
the hypothesis: ONE top-level `rotate_defaults` map, the Prime's single-JSON
value, feeds both reads.

Changes (rotate.py):
- `_load_rotate_defaults(root) -> dict` — the ONE reader. Reads frontmatter
top-level `rotate_defaults`; {} when absent/not-a-map; a quoted-JSON str cell
`{...}` is json.loads()-ed so the shape survives "set rotate_defaults {…}"
quoting (the digit-string attention from the SL7.114 harvest).
- `_role_timeout` now reads `rotate_defaults.timeout_s.<role>` (int or
digit-only string, else 600). Old `templates.<role>.timeout_s` read DELETED.
- cmd_rotate closeout block reads `rotate_defaults.closeout.<role>` (else
False). Old `templates.<role>.rotate_defaults` read DELETED. `_ranks` untouched.

Tests touched (<= 4, in the two named files only):
- test_rotate_verb_resolvers.py: `test_role_timeout_from_template_or_default`
and `test_role_timeout_digit_string_...` rewritten to the new top-level shape.
- test_rotate_verb.py: new `test_closeout_default_from_rotate_defaults_map`
reading `rotate_defaults.closeout.<role>` true/false/absent. `_write_geo`
gained the `rotations=` kwarg to write the config node.

## Evidence

Built bytes proven on the round's tree:

    $ python3 -m pytest extensions/agi/tests/test_rotate_verb_resolvers.py extensions/agi/tests/test_rotate_verb.py -q
    .....  21 passed in 0.35s

Falsifiers checked against the built bytes:
- dotted-key read left anywhere? -- none (grep of rotate.py: only
  `rotate_defaults` top-level via `_load_rotate_defaults`, plus the EXCLUDED
  closeout CARD form `template[closeout].slots`).
- fallback to templates.<role>.*? -- none; both old reads deleted, not kept.
- a third reader? -- no; `_role_timeout` (14426) and the cmd_rotate closeout
  block (16736) are the only two, both through `_load_rotate_defaults`.
- a write to config:rotations? -- none in this round; the Prime's two 0a
  lines are documented below and must NOT run until this lands on main.

Intended Prime application (EXACTLY TWO 0a lines on config:rotations, each
write.py --dry-run-proven on main before applying):

    set ranks ["prime_director","director","helper"]
    set rotate_defaults {"timeout_s": {"prime_director": 900, "director": 900, "helper": 600}, "closeout": {}}

(the round itself never writes config:rotations.)

## Agent Notes
Built g15 claim: ONE top-level rotate_defaults map (timeout_s+closeout per role) replaces the two un-writable templates.<role>.timeout_s / templates.<role>.rotate_defaults reads; _load_rotate_defaults is the single reader, both old reads deleted. 21 tests pass (2 timeout tests reshaped + 1 closeout test added).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.117: read the diff bytes (rotate.py _load_rotate_defaults/_role_timeout/cmd_rotate, both test files), ran one negative probe per claim conjunct against the built bytes, all pass. The two Prime 0a lines were re-proven by write.py config:rotations --dry-run on this round tree and both print a top-level set (no dotted nesting). Accepted, verdict kept proved.
<!-- THOUGHT:END -->

SL7.117 parent review: ACCEPTED. Probes recorded (4/4 conjuncts). rotate.py reads ONE top-level rotate_defaults map; old templates.<role>.timeout_s / templates.<role>.rotate_defaults reads deleted (probe: templates timeout_s=900 -> 600). ranks untouched (top-level wins over a hijack rotate_defaults.ranks). Round touched no config:rotations. Two 0a lines dry-run-proven: set ranks ["prime_director","director","helper"] and set rotate_defaults {"timeout_s": {"prime_director": 900, "director": 900, "helper": 600}, "closeout": {}}.
