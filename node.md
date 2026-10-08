---
id: experiment:a00-0f40a201-91a44a
mint_id: 197909db234f47d98ad7adae2ac5680b
type: experiment
parents:
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
confidence: 0.7
edited_by: a00-2f2d0784
evidence_runs:
  - experiment:a00-0f40a201-91a44a
loop: hypothesis:l4-startup-is-one-script-or-a-driven-prompt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 165964edfc242b27
season: 2
title: "\"Bootstrap record: derive real telemetry + staleness check (kid 2; config facts write blocked for a kid)\""
town: core
verdict: inconclusive_lean_proved:70
---
# experiment:a00-0f40a201-91a44a

Kid 2 of hypothesis `l4-startup-is-one-script-or-a-driven-prompt` (the 0b
round, per the DIRECTOR ADDENDUM). This kid owns the **bootstrap-record
half** of the pending acceptance test — `_write_bootstrap` under
`hypothesis:l4-startup-is-one-script-or-a-driven-prompt` shall hand the
successor real telemetry by default, not the placeholder `SKIPPED: 0b owns
deriving <name>` the 0b ADDENDUM said THIS round fills. Kid 1 (a00-790bbd0f)
already landed the first_turn half; this lands the record that makes it worth
reading.

## Experiment

Replaced the blanket skip in `extensions/agi/bin/rotate.py::_write_bootstrap`
with per-fact derivation + a staleness check:

1. **`_git_head(root, argv=None)`** — the ONE read-only git command the record
   is allowed (`git rev-parse --short HEAD`); returns None when `root` is not
   a repo (recorded as a named skip, never guessed).
2. **`_derive_bootstrap_fact(key, ...)`** — resolves EACH fact to a real value
   where the handover can see it, else `None` + a NAMED skip reason (never
   the old blanket `0b owns deriving`). Derivable: `commit`, `seat_row`, and
   the seat-row facts `seed`/`model`/`effort`/`window`/`worktree`/`ack`/
   `prev_gen` (read the config:seats row at HEAD via `_find_seat`). Join-only
   facts (`successor_live_model`, `successor_address`,
   `model_refusal_fallback`) skip NAMING the join (the after_join round).
   Sibling facts (`mail`, `account`, `floor`, `registry`, `crons`) skip NAMING
   the sibling round that owns them.
3. **`_write_bootstrap(..., commit=None)`** — emits the template telemetry set
   PLUS the owner's fixed fact set (`BOOTSTRAP_FIXED_FACTS` — "they should
   receive all this telemetry by default"), stamps every derived fact in a
   `measured_at` map (fact -> commit), keeps `shape: v1`.
4. **`_bootstrap_stale(doc, current_commit, bounds=None)`** — the staleness
   check the SessionStart hook calls: True when a non-permanent fact's
   `measured_at` is anything but HEAD (=> REFUSED, never injected stale);
   `bounds` maps fact -> `head`|`permanent` (declared in config:rotations
   `## facts`); a SKIPPED/full-skip doc asserts nothing and is never stale.

Tests added in `test_rotate_tail.py` (fixtures only — no real spawn, no tmux,
no graph): real derivation + measured_at stamping (bounded to a fake git
HEAD via monkeypatch), staleness refuse/accept + permanent-bound, and the
re-written `test_bootstrap_records_telemetry_and_skips_0b` (now asserts NO
`0b owns` survives and nothing is stamped when there is no repo).

## Evidence

- `env -u AGI_TIER python3 -m pytest extensions/agi/tests/test_rotate_tail.py
  extensions/agi/tests/test_rotate_startup.py -q` → **23 passed**.
- FULL suite `python3 -m pytest extensions/agi/tests/ -q` → **2720 passed,
  1 skipped** (nothing regressed).

## Confirmation / leftover

**The `## facts` section of `.agi/nodes/.geometry/rotations.md` is BLOCKED
for a kid.** The task assigned filling it, but `write.py config:rotations
'replace body 37:42 -'` is refused by the admission gate: the `[config]`
schema declares `written_by: [owner, prime_director]`, and AGI_ROLE=kid /
AGI_SEAT=sanctuary-director resolves to neither; the only unadmitted path is
the self_row carve-out for one's OWN config:seats row, never a config:rotations
section (confirmed by reading `_enforce_written_by` in write.py — no
sanctioned bypass, no force flag; passing `--role prime_director` would be
impersonating the prime to dodge a safety gate, which I will not do). The
fact list + staleness bounds I derived are pasted below, ready for the prime
to land in one write:

```
## facts

Every fact the bootstrap record carries (`<sessions>/seats/<seat>.bootstrap.json`, shape: v1). A fact is fresh when measured_at[fact] == HEAD; rotate._bootstrap_stale(doc, HEAD, bounds) REFUSES a record carrying a non-permanent fact measured at anything but HEAD. A SKIPPED:<reason> fact asserted nothing and is not stale.
| fact | meaning | source at handover | bound |
| commit | the HEAD every measured fact is stamped at | git rev-parse --short HEAD | head |
| seat_row | the successor's config:seats row at HEAD | .agi/nodes/.geometry/seats.md | head |
| seed | the seat row `seed` | config:seats row | permanent |
| model | the seat row `model` at HEAD | config:seats row | head |
| effort | the seat row `effort` | config:seats row | permanent |
| window | the seat row `window` | config:seats row | head |
| worktree | the seat row `worktree` | config:seats row | head |
| ack | the seat row `ack` at HEAD | config:seats row | head |
| prev_gen | the seat row `prev_gen` | config:seats row | head |
| verification | predecessor's _run_verification result | rotate-self s11 | head |
| successor_live_model | the successor's LIVE model vs its row | @id join (after_join round) | head |
| successor_address | the successor's address by the join | @id join (after_join round) | head |
| model_refusal_fallback | the last model_refusal_fallback event | successor transcript (after_join round) | head |
| mail | unread dms addressed to the seat | send.py read (sibling round) | head |
| account | account balance | credits endpoint (sibling round) | head |
| floor | floor numbers | sibling round | head |
| registry | workflow registry state | sibling round | head |
| crons | crons state | sibling round | head |
```

The code half is PROVEN by fixtures; the config write needs the prime (owner or
prime_director) to apply it — that is the one honest gap in this verdict.

Legacy test: `test_bootstrap_records_telemetry_and_skips_0b` asserted
`telemetry["seed"].startswith("SKIPPED: 0b owns")`. I CHANGED it, and here is
the justification: the whole point of this kid is to remove the blanket
`0b owns deriving` skip on a fixture (no seats row, no repo); keeping the old
assertion would pin exactly the placeholder this round is deleting. The
rewrite asserts the invariant that replaces it — every `SKIPPED:` names a
reason (no bare `0b owns`), nothing is measured_at-stamped when there is no
repo — plus shape stays `v1`.
## Agent Notes
kid2: derived real bootstrap telemetry in rotate._write_bootstrap (seat-row facts + HEAD stamp) replacing the blanket 0b-owns skip with named SKIPPED reasons, added measured_at stamping + _bootstrap_stale refuse-not-inject check; fixtures prove derivation/staleness, 2720 suite green. config:rotations ##facts write BLOCKED by admission gate (high-level only owner/prime_director); content staged in node for the prime.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2f2d0784, L4.125). The dispatch addendum said: fill the "## facts" section of config:rotations via write.py. The machine refuses it: write.py _enforce_written_by reads [config].md written_by [owner, prime_director]; AGI_ROLE=kid and AGI_SEAT=sanctuary-director resolve to neither, so replace body is refused and no force flag exists (the only carve-out is self_row on ones OWN config:seats row). The kid reported this rather than impersonating the prime with --role, which is the correct call. Near miss: passing --role prime_director would have satisfied the words and bypassed the gate. Parent removed a duplicated body (2x "## Experiment"), keeping the Legacy-test paragraph that lived only in the second copy. Verified independently: test_rotate_tail.py 15 passed; _bootstrap_stale, _derive_bootstrap_fact, measured_at present at rotate.py:3378-3523. Verdict inconclusive_lean_proved:70 kept: code half proved by fixtures, config half genuinely blocked.
<!-- THOUGHT:END -->
