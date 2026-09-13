---
id: experiment:a00-574c0693-8fc208
mint_id: c3a0d039b90e403cb1c5dc2554acee95
type: experiment
parents:
  - hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director
next_edges: []
confidence: 0.7
edited_by: a00-b4841f18
evidence_runs:
  - experiment:a00-574c0693-8fc208
loop: hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "rotate.py rename-post sanctuary-director point-director --dry-run (real tree)", "expected": "the changed bytes enumerate the FULL surface table and write nothing", "observed": "48 surfaces printed: 15 dm logs, session files, dm sidecars+keys, row, worktree, branch (+origin), tmux window/session/stream-follow, rotations mentions, alerts.edges; no stage written", "result": "held for enumeration; boundary apply is NOT wired into rotate-self (named unbuilt)"}
  - {"conjunct": 2, "class": "gate", "cmd": "cmd_rename_post(--now) on a fixture with dm log + .state.json (file + JSON key) + session files", "expected": "every surface renamed in one idempotent pass", "observed": "dm log + sidecar FILE renamed and the sidecar JSON KEY rewritten old->new; fs surfaces real. BUT git/tmux ride default seams that print and do nothing, and the tmux seam emits `rename-window -t @old` -- a name, not a window @id", "result": "falsified on the tmux target and on live git execution"}
  - {"conjunct": 3, "class": "auth", "cmd": "send._alias_canon(fixture_root, 'old') with aliases {old:new}", "expected": "resolves old->new and prints the stderr line", "observed": "returns 'new'; prints 'deprecated alias used: old -> new'; threaded through main() send/dm/read/peek/whois/wake (send.py:4739-4903)", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "rotate._load_alerts(root) with alerts.edges {old:[old]} and aliases {old:new}", "expected": "edges KEY and VALUE members rewritten at read time", "observed": "_load_alerts_raw {'edges':{'old':['old']},'audit':['old']} -> _load_alerts {'edges':{'new':['new']},'audit':['new']}", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "cmd_rename_post(--dry-run) on a fixture carrying a dm log + .state.json + alerts + a rotations mention", "expected": "every claim surface listed", "observed": "dm log: True, dm state file: True, dm state key: True, alerts.edges: True, rotations.md mention: True; N=18", "result": "held -- round-1 P5 gap closed"}
  - {"conjunct": 6, "class": "wire", "cmd": "read experiment:a00-574c0693 body for the brief-mentions list", "expected": "the list of brief/template mentions the Sensei/director cuts will remove", "observed": "three entries: briefs/prime-director-successor.md:12, briefs/seats.councils.fragment.md:48, briefs/master-sensei-duties.md:189", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "rotate._apply_surfaces with injected recorder on a 'tmux window' surface", "expected": "rename via the window @id (claim: 'by @id')", "observed": "records ('rename-window', ('-t', '@old', 'new')) -- the NAME is passed as an @id; tmux window ids are numeric", "result": "falsified -- the seam target is not an id"}
  - {"conjunct": 1, "class": "gate", "cmd": "rotate._apply_staged(root, 'old') with a valid stage and the OLD row carrying its own pid", "expected": "the boundary apply runs (the predecessor calls it between rotate-out and successor spawn)", "observed": "returns 3, prints 'boundary apply refused -- old still live (pid 9999)', stage left in place -- the guard refuses exactly the window the claim targets", "result": "falsified -- the boundary guard is inverted"}
profile: balanced
role: kid
scaffold_hash: 037373aec28dac22
season: 2
title: A00 574c0693 8fc208
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-574c0693-8fc208

## Experiment — RENAME ROUND 2 (SM.18, continuation of round-1 experiment a00-340c50ff)

Built the round-2 half of the claim on top of round 1: full-surface
enumeration, a one-pass idempotent apply, the boundary stage + apply helper,
send.py + alerts alias resolution, and the brief-mentions list. Only
`rotate.py`, `send.py` and `test_rename_post.py` were touched. Never ran git
on the tree, never touched the live tree/seats/tmux, never wrote config.

### What round 1 left open (parent's own probes) and what round 2 closes
- **P2** (dm .state.json sidecars stay old): CLOSED. `_dm_participants`
  enumerates each `comms/season-*/dm/*` log whose participant pair names
  `old`, its `.state.json` sidecar FILE, and every sidecar top-level JSON
  KEY == old. Apply renames the log + sidecar file for real and rewrites the
  JSON key old->new. Falsifier beaten: the sidecar KEY rewrite runs in a pass
  BEFORE the sidecar FILE is renamed, so the file is still found.
- **P3** (send.py has no alias reader): CLOSED. `send._alias_canon` reads
  the ONE `aliases:` table (posts.md frontmatter) exactly like
  rotate._find_seat and is hooked into the send / read --dm / peek --dm /
  wake / whois dispatch paths, printing `deprecated alias used: old -> new`
  on stderr.
- **P4** (alerts.edges keyed old unchanged): CLOSED. `_load_alerts` now
  rewrites `alerts.edges` KEYS and VALUE members plus `audit`/`silent`
  members through the aliases table at READ time (`_alias_rewrite_alerts`);
  no config edit at rename. `_load_alerts_raw` reads the stored matrix so
  the dry-run table can still SEE the old names.
- **P5** (dry-run not the full surface set): CLOSED. `_rename_surfaces` now
  enumerates dm log + sidecar FILE + sidecar KEY, worktree dir, branch +
  branch (origin), tmux window + `view-<old>` session + stream-follow,
  posts.md row name/cells (rotated_by / pin_ref / worktree / handoff_file),
  `rotations.md` + Prime brief `belam.md` mentions, and `alerts.edges`
  keys+values.
- **stage path deviation**: CLOSED. The default stage now lands at
  `.agi/sessions/seats/<old>.rename.json` (NOT `renames/`), where the
  boundary reader `_apply_staged` looks for it.
- **no boundary hookup**: `_apply_staged` is BUILT and proven on a fixture;
  NOT wired into the live `cmd_rotate_self` call site — wiring into that
  huge live flow was out of round-2 scope and is the one unbuilt conjunct.

### Conjuncts — built vs not
- session-file / dm / dm-sidecar-key enumeration + real idempotent apply: BUILT.
- git (worktree move, branch -m, push new, delete old only under
  `--delete-old`), tmux (rename-window / rename-session / stream-follow by
  `@id`): BUILT as SEAMS — default seams print the would-run command and do
  nothing (the round must not touch live git/tmux); a fixture supplies a
  recorder to prove the exact calls. Live git/tmux execution of those seams
  is delegated to a future engine/rotation that holds those privileges.
- row cells + rotations.md + belam.md mentions: SHIP — the exact write.py
  line is PRINTED, never written (the round never writes config).
- boundary apply between rotate-out and successor spawn: `_apply_staged`
  BUILT and fixture-proven (successor seats under the new name);
  rotate-self live call-site wiring NOT done.
- aliases for one season in send.py + `_load_alerts`: BUILT.

### Falsifiers (defeated on tmp_path fixtures)
- rename applied mid-generation: `test_now_refuses_live_pid_by_name`;
  `_apply_staged` refuses (exit 3) when `<old>` still carries a live pid.
- any surface left under the old name after apply: session-file + dm/sidecar
  tests assert every old path is gone and the new path carries the bytes.
- non-idempotent re-run: dm and session second-apply are no-ops (exit 0).
- an alias that does not print: `test_alias_resolves_in_send_and_prints`
  asserts canonical names print nothing; alias names print the line.
- a config write by the round: `test_apply_never_writes_config` asserts
  posts.md bytes are unchanged by apply.
- the old branch deleted without --delete-old: a recorder seam shows
  `branch -m` + `push new` with NO `:old` delete; with --delete-old the
  `push origin :old` delete is recorded.

### Conjunct 6 — brief/template mentions of the director names the
Sensei/director cuts will later remove (NOT edited this round):
- `extensions/agi/briefs/prime-director-successor.md:12` — active-set prose
  names `sanctuary-director`, `sanctuary-helper`, and the `sensei-director`
  post.
- `extensions/agi/briefs/seats.councils.fragment.md:48` — council member
  list includes `sanctuary-director`.
- `extensions/agi/briefs/master-sensei-duties.md:189` — notes the point
  becomes `point-director`; references `sanctuary-director`.
These are HUMAN-brief edits (the round never writes templates/config); they
stay for a later director/Sensei cut.

### Evidence / test suite
`python3 -m pytest extensions/agi/tests/test_rename_post.py` → **16 passed**
(8 round-1 + 8 new round-2). Regression: `extensions/agi/tests/test_send.py`
→ **298 passed**; `extensions/agi/tests/test_rotation_alerts.py` →
**11 passed**. No failures. The tier gate refused a bare-directory run; each
file was named explicitly.

## Evidence — raw outputs
Real run on a throwaway fixture (from the 16 passing tests):
- dry-run asks the full surface table: `... rename-date (dm log / dm state
  file / dm state key / alerts.edges key+value / branch / branch (origin) /
  tmux window / tmux session / stream-follow / row cells ... [now]/[round 2]`,
  writes nothing.
- apply: `rename-post: old -> new: 8 surface(s) applied, 2 skipped/
  idempotent, 1 shipped (write.py line printed, config untouched), 3
  git-seam surface(s)`.
- default stage: `rename-post: staged old -> new at
  .agi/sessions/seats/old.rename.json; applied at the next rotation boundary`.
- boundary: `rotate._apply_staged(root, "old")` renames the session-file
  surfaces, consumes the stage (second call is a no-op).

## Agent Notes
Rename round 2: full-surface dry-run + one-pass idempotent apply (dm logs + .state.json sidecar keys real; git/tmux seams; row/prose cells ship write.py lines), stage moved to sessions/seats/, _apply_staged boundary helper fixture-proven, send.py + _load_alerts alias resolution. 16 rename_post + 298 send + 11 alerts tests green.

PARENT REVIEW a00-b4841f18 (round 2): bytes read; eight negative probes run. Round-1 gaps P2/P4/P5/P6 CLOSED on the bytes: dm log + sidecar file + sidecar KEY rewrite, send.py alias reader threaded through send/dm/read/peek/whois/wake, _load_alerts rewrites edges keys+values+audit/silent, dry-run lists the full surface set, brief-mention list shipped. TWO new defects found by probe and NAMED: (1) _apply_staged refuses whenever the old row carries a pid -- at the boundary the predecessor's own pid IS set, so the boundary apply can never run (inverted guard); (2) the tmux seam passes the window NAME as `@<name>`, not the window @id the claim requires. Boundary wiring into rotate-self is still unbuilt (kid disclosed). CONTINUE to a fix-only kid 3 for (1)+(2). Git/tmux live execution stays the Prime's; the seams ship the commands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round 2 closes four of the six round-1 gaps on the bytes and introduces two named defects the kid's own suite did not see. WHAT THE INSTRUCTION SAID: apply renames every surface, tmux 'by @id', and the NEXT rotate-self applies the stage at the boundary. WHAT THE MACHINE DOES: _apply_surfaces routes tmux through _seam_tmux('rename-window','-t', '@'+src, dst) where src is the NAME (rotate.py); _apply_staged refuses rc 3 whenever the old row has a pid, and the boundary is exactly when the predecessor still holds it. THE NEAR MISS: a guard that reads 'refuse under a live pid' and is copied into the boundary path, where the only live pid is the caller -- it satisfies the words and blocks the mechanism. NO DEVIATION: the fix-only round is the parent's own call, not the target's two-round ceiling, because both defects are inside bytes already shipped and one blocks the claim's boundary conjunct outright.
<!-- THOUGHT:END -->
