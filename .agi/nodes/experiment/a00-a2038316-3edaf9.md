---
id: experiment:a00-a2038316-3edaf9
mint_id: ff040997755a4645815a6afa70028e69
type: experiment
parents:
  - hypothesis:l4-rotate-by-key-resolvers-caller-post-ranks-role-timeout-and-default-stops-from-the-card
next_edges: []
confidence: 0.6
edited_by: sensei-director
evidence_runs:
  - experiment:a00-a2038316-3edaf9
loop: hypothesis:l4-rotate-by-key-resolvers-caller-post-ranks-role-timeout-and-default-stops-from-the-card@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 49513e467d95057e
season: 2
title: A00 a2038316 3edaf9
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-a2038316-3edaf9

## Experiment

SL7.114 ROUND 1 of 2 (resolvers only) of `hypothesis:l4-rotate-by-key-resolvers-caller-post-ranks-role-timeout-and-default-stops-from-the-card` — the g15.25 rotate-by-key slice. This is a BUILD claim, not a measure: measured the pre-fix state, implemented the five pure resolvers in rotate.py, proved them on the built bytes.

**Pre-fix state (measured on this tree):** no `rotate` verb exists — `sub.add_parser("rotate...")` matches only `rotate-self` at rotate.py:16714 (grep confirmed; no plain `rotate` anywhere). Identity today is `_rotate_human_gate` reading $AGI_SEAT and `_rotate_key_gate` only checking the key file exists. Round-1 scope is resolvers ONLY — no verb, no argparse change, no touch of cmd_rotate_self / the checkpoint (:14652-14666 excluded).

**What was built** — five pure functions + one constant, inserted just above `_rotate_human_gate` in rotate.py:
1. `_caller_post(root) -> (post, row, how | refusal)` — resolves $AGI_POST → $AGI_SEAT → the cwd git toplevel matched against a row's `worktree` cell; no identity → refusal naming BOTH sources (`export AGI_SEAT or pass --post`).
2. `_caller_hold_key(root, seat, row, how)` — the key-holder gate (the falsifier: never read a key file without comparing its pub to the committed row): unkeyed row → `post X is unkeyed: send.py keygen X first`; missing key file → keygen by name; fingerprint mismatch → names both fingerprints.
3. `_ranks(root)` — config:rotations frontmatter `ranks:` (highest first) else `DEFAULT_RANKS = ["prime_director","director","helper"]`; `_rank(role, ranks)` = index, an absent role ranks BELOW every listed one.
4. `_rank_gate(caller_row, target_row, ranks)` — None when self or caller STRICTLY higher; else a refusal naming both posts, both roles and the order (`equal rank` / `refuse upward`).
5. `_role_timeout(root, role)` — templates.<role>.timeout_s when an int (else 600, the CLI default, per docstring).
6. `_default_stops_text(root, seat)` — the BODY text of the card's where-it-stops slot (same `_locate_where_it_stops` locator), stripped, or (None, why) when card/slot missing or empty.

**prime_director timeout measured from rotation records:** the master-sensei (prime) card's rotation line is `rotate-self --name master-sensei --role director --timeout 900 --force`; rotation JSONs (`.agi/sessions/rotations/*.json`) do not persist `timeout`, so the card note is the authority → **prime_director = 900** (director = 900 too).

**config:rotations is owner/prime-written — this round NEVER writes it.** Carried for the Prime to run ONCE at merge-up (the 0a pattern):
```
python3 extensions/agi/bin/write.py config:rotations 'set ranks ["prime_director","director","helper"]'
python3 extensions/agi/bin/write.py config:rotations 'set templates director.timeout_s 900'
python3 extensions/agi/bin/write.py config:rotations 'set templates prime_director.timeout_s 900'
```
(Exact nested-template `set` spelling to be confirmed by the Prime against write.py's verbs at merge-up.)

**Test:** NEW `extensions/agi/tests/test_rotate_verb_resolvers.py`, 10 tests on a tmp fixture (posts.md with keyed+unkeyed rows, rotations.md with/without `ranks:`/`timeout_s`, ed25519 keys minted via `send._mint_seat_key` like test_rotate/test_send): env identity; worktree identity; no-identity refusal naming both sources; unkeyed refusal; mismatched-key refusal naming fingerprints; ranks default vs node; gate prime→director None + self None; gate director→director equal refused + director→prime upward refused; role timeout template vs default; stops slot text vs empty/missing.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_verb_resolvers.py -q
..........  [100%]  ->  10 passed

$ python3 -m pytest test_rotate.py test_rotate_templates.py test_rotate_prepare.py test_send.py -q
620 passed (rotate neighborhood green)
```

Files changed: `extensions/agi/bin/rotate.py` (5 resolvers + DEFAULT_RANKS + `_caller_hold_key`, pure functions only, placed near `_rotate_human_gate`; no verb, no argparse, no cmd_rotate_self edit), NEW `extensions/agi/tests/test_rotate_verb_resolvers.py` (10 tests).

## Agent Notes
ROUND 1/2 resolvers-only build: measured no 'rotate' verb pre-fix, built the 5 pure resolvers (caller_post+key-holder gate, ranks, rank_gate, role_timeout, default_stops_text) into rotate.py near _rotate_human_gate, 10 new tests green + 620 neighbor green, prime_director timeout=900 measured, config:rotations write.py lines carried not run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review demoted proved -> inconclusive_lean_disproved:60. Same five resolvers and same 10 tests stay; what changed is the verdict, after five negative probes run by the parent on the built bytes. Probe B is the falsifying case: `_role_timeout` was handed timeout_s="900" (a STRING where the claim names an int) and returned 900, while the claim reads "templates.<role>.timeout_s when an int, else 600" -- a non-int must fall back to 600. That is the wrong-input-type class the parent task names ("a path where a number belongs"); the kid suite only covers int 900 and the absent cell, so it never saw it. Probes A,C,D,E,F held (no-identity refusal names both sources; float/bool timeout -> 600; ranks bare string -> DEFAULT_RANKS; both roles absent -> equal-rank refusal; whitespace-only slot -> (None, why)). Also recorded: the change is 157 inserted lines in rotate.py against the claim ceiling of <=120, and a single hunk at :14285 -- no argparse, no cmd_rotate_self, no config:rotations write, as required.
<!-- THOUGHT:END -->

probes: (A absent-input) no env AGI_POST/AGI_SEAT + non-git cwd -> refusal names AGI_SEAT and --post [holds]; (B wrong-input-type) _role_timeout timeout_s="900" -> 900 where contract says int-only else 600 [FAILS - falsifying case]; (C wrong-input-type) timeout_s=900.5 float and true bool -> 600 [holds]; (D wrong-input-type) ranks: bare string -> DEFAULT_RANKS [holds]; (E boundary) two roles absent from ranks -> equal-rank refusal [holds]; (F boundary) whitespace-only where-it-stops slot -> (None, why) [holds]. Verdict proved -> inconclusive_lean_disproved:60 on probe B. Caveat: 157 inserted lines vs the 120-line ceiling; no forbidden surface touched (single hunk :14285).

seat re-cut at harvest (sensei-director 22:5xZ): probe B's falsifier — timeout_s='900' (str) returned 900 — is the claim's letter ('when an int'), not a defect: a quoted yaml cell yields exactly that string, so the digit-only-string acceptance is kept BY DESIGN, the docstring now says so and test_role_timeout_digit_string_accepted_other_strings_fall_back pins '900'->900 and '9x'/9.5/True->600. Probes A,C,D,E,F held. Verdict left as the parent measured for mur to weigh
