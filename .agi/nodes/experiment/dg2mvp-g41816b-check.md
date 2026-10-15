---
id: experiment:dg2mvp-g41816b-check
mint_id: b8c2e26843f9400690f626b90baf12b7
type: experiment
parents:
  - build:bin-write
  - experiment:dg2mvp-g41816-check
next_edges: []
edited_by: director-general-2
scaffold_hash: a305f5926c21d403
season: 2
title: "g41816b re-check: node `patch` at 462590995 after 563cd4ca9 (SM 150/151/155), 5c7e632c7, d8b22ae96 (SM 152-154/162/163), judged on goal:g4.18.1.6 as restated"
town: core
---
# experiment:dg2mvp-g41816b-check

## g41816b post-build re-check: `patch` on a no-payload_ref node, against goal:g4.18.1.6 as it reads at HEAD

Pin 462590995 (HEAD). Since the first check (verdict:dg2mvp-g41816, pin 3aa03292b) these landed on write.py / node_writer.py / the goal: 563cd4ca9 (SM 150+151+155), 5c7e632c7 (goal end-state 1 restated), 1098822e1 (DG4 busy index; swept DG3's WIP canonicalize), c3c118b3c (hotfix: canonicalize ARITY), d8b22ae96 (council ruling (b) on SM 154 + 152 153 162 163), 08a870a3a (goal falsifier 1 restated).
What changed in the goal text: end-state 1 now says `replace payload N:M` stays payload-only and refuses naming `replace body N:M` / `row` (it used to say it targets the node file). Falsifier 1 now says "lands byte-exact on a canonical node ... a patch whose result the canonical render would alter refuses by name and prints `write.py <id> canonicalize`" (it used to say "byte-exact on the node file").
Rig: `git archive 462590995 extensions .agi/context .agi/config.json .agi/nodes/.geometry` + .gitignore + real nodes (build:extensions-agi-guard-ram-tier.sh + payload, goal:g4.18.1.6, goal:g4.18.1, goal:g2.2, goal:s3 with ONE synthetic BUILD-CONTRACT block, later one real hypothesis node) -> `git init` in /tmp/dg2mvp/g41816b/repo. write.py run from that tree with `--root <repo>/.agi`, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT -u AGI_ROLE, `--actor owner` unless stated. Every negative ran dry then real; "unchanged" = sha256 equal and no new commit. Scripts: pos.sh / neg.sh / mkdiff.py in the work dir.

| # | command | observed |
|---|---|---|
| 1 | `config:guard 'patch -'` one body line, `--actor dg2-probe` (dry, real) | dry rc 0 (ring-preview), real rc 2 `config nodes (config:guard) may be hand-edited only by admitted roles owner, prime_director ...`; unchanged, no commit. Same as the first check |
| 2 | same, `--actor owner` | dry rc 0 unchanged; real rc 0, commit `write.py: config:guard (owner)`, 1 file; result = intended bytes + the `edited_by` stamp only |
| 3 | goal:g4.18.1.6 BODY-ONLY patch (`Out of scope` -> `Out of Scope`) | rc 0 dry/real, lands, committed. (d8b22ae96: before it a body-only node patch was refused `nothing to submit`) |
| 4 | goal:g4.18.1.6 row `confidence` · text inside the THOUGHT · the quoted title gains backticks | rc 0 each, dry unchanged, real BYTE-EXACT to the intended file, one commit each |
| 5 | cron:crons nested `every_mins: 5 -> 6` · config:posts one JSON-flow row cell | rc 0; only the target line + `edited_by` moved; committed |
| 6 | build:...ram-tier.sh, a diff against its PAYLOAD | rc 0, payload BYTE-EXACT, commit = payload + node (`edited_by` only) |
| 7 | build:...ram-tier.sh, a diff against the build NODE file | rc 2 dry == real `context mismatch at original line 13` (applied to the payload); unchanged |
| 8 | `replace payload 1:1 x.txt` on config:guard and goal:g4.18.1.6 (dry, real) | rc 2 x4: `has no payload_ref: use \`replace body N:M\` (or \`row\`) for the node file -- ... (council ruling on goal:g4.18.1.6)`; unchanged. Matches restated end-state 1 |
| 9 | `patch -` with empty stdin (dry, real) | rc 2 `patch - (stdin) is empty: no diff to apply -- nothing written` |
| 10 | identity: goal `id`, `mint_id`, `type`, `mint_id` row removed; config:guard `id`, `mint_id` | rc 2 on all 12 runs, dry ERR == real ERR, set's own message `patch: 'id' is identity or completion state and no verb may set it...` / `'mint_id' may not be unset — see \`set\`.`; unchanged |
| 11 | **SM 150**: scaffold_hash changed / removed (goal:g4.18.1.6) · added (config:guard) | rc 2 dry == real x3: `patch: 'scaffold_hash' is identity or completion state ...` / `'scaffold_hash' may not be unset`; unchanged, no commit. MET (first check: not covered; SM found it landing) |
| 12 | dotted key `foo.bar: 1` via patch | rc 2 dry == real `patch: cannot set 'foo.bar': dotted keys are not written as flat frontmatter literals`; unchanged |
| 13 | **SM 151**: `parents` -> goal:g9.99.nope · `next_edges` -> goal:g9.99.nope (goal:g4.18.1.6) · a config:guard parent -> missing | rc 2 dry == real x3 `cannot set: ['goal:g9.99.nope'] name no node -- create it first, or name an id that exists (goal:g4.18.6.2.1)` = the same ERR `set parents [goal:g9.99.nope]` prints; unchanged, no commit. MET (first check row 19: landed rc 0) |
| 14 | SM 151 positive: `parents` -> goal:g2.2 · `next_edges` -> goal:s3 (both exist) | rc 0, BYTE-EXACT, committed |
| 15 | **SM 155**: `config:guard 'patch -' --ring-fields` (season 2 -> 3) | rc 0, `ring-fields.json` carries `"season": "[\"int\",3]"` -- the translated row; nothing written |
| 16 | BUILD-CONTRACT (goal:s3 synthetic): line inside changed · END removed · new block added (goal:g4.18.1.6) | rc 2 dry == real x3 `patch touches the BUILD-CONTRACT block, which is regenerated -- nothing written` |
| 17 | THOUGHT: BEGIN removed · END removed · stray END added · config:guard END removed · **SM 152**: a 2nd block added · the whole block removed | rc 2 dry == real x6 `patch would leave the THOUGHT malformed: rewrite it with the \`thought\` verb -- nothing written` |
| 18 | `'patch - && note hello'` · `'patch - && set confidence 0.7'` · **SM 163** `'read body 1:2 && patch -'` | rc 2 dry == real: `... is standalone: no other verb on its line` / `read is a terminal verb` |
| 19 | **SM 153/162**: `patch <missing file>` · `patch <directory>` · a patch deleting the closing `---` · a patch making `mint_id: [unclosed` | rc 2 dry == real: `patch on config:guard cannot apply: [Errno 2] ...` / `[Errno 21] Is a directory` / `md file missing closing '---'` / `malformed YAML frontmatter` -- `-- nothing written`, no traceback, unchanged |
| 20 | **F1 clause 2 / SM 154** on a CANONICAL node, the patch itself introduces: a `# comment` · a comment-only line · a flow `tags: [..]` · `'active'` quoting · `0.70` | rc 2 dry == real x5 `patch result is not in the canonical form, so it would not land as written (re-render: [...]): run \`write.py <id> canonicalize\` first ...`; unchanged |
| 21 | goal:g2.2 hand-formatted in the rig (inline comment, flow tags, single-quoted title, `note_str: '0.8'`): a body-line patch · a comment-only hunk | rc 2 dry == real, same ERR naming `write.py goal:g2.2 canonicalize`; the drift list shows `+note_str: 0.8 / -note_str: '0.8'` |
| 22 | `goal:g2.2 canonicalize` dry / real / again, then the same body patch | dry rc 0 unchanged; real rc 0 committed (comment dropped, block tags, double-quoted title, **`note_str: '0.8'` -> `0.8`**); 2nd run `unchanged ... nothing to change`; the patch then lands BYTE-EXACT, committed |
| 23 | `render_frontmatter({'a':'0.8','b':'yes','c':'null'})` (tree, direct) | `['a: 0.8', 'b: yes', 'c: null']`: a quoted-scalar STRING is emitted bare, so the re-read value is float / bool / None. canonicalize changes the VALUE type, not only "non-significant quoting" as the ERR says |
| 24 | corpus census at the pin (git archive of .agi/nodes, read-only): live nodes with no payload_ref/link_ref (= node-patchable), canonical render == file bytes? | 4808 patchable live; 746 NOT canonical (690 = no final newline, 10 = two trailing newlines, the rest frontmatter shape). Config (.geometry) nodes: all canonical. Round-trip VALUE changes over all 5354: 0 |
| 25 | a real no-final-newline node (hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps), a body-line patch; then canonicalize + the same patch | rc 2 dry == real, `re-render: ['+']`, names `canonicalize`; after canonicalize the patch lands BYTE-EXACT, committed |
| 26 | `patch /path/file.diff` (file form) on config:guard | rc 0, lands, committed |
| 27 | pytest test_write.py (tree @462590995) | 180 passed, 1 xfailed (the xfail is bundle 4 W3c's, not this row's) |
| 28 | pytest test_body_patch.py · test_write_guard.py | 6 passed · 32 passed |
| 29 | this row's tests at HEAD vs a6102199b/3aa03292b | no strict-xfail for g41816 exists. test_g41816_patch_lands... unchanged; test_g41816_a_node_patch_refuses... only the expected ERR text moved to set's own message (+3 rows: scaffold_hash, dotted key, missing parent); + test_sm150_155, + test_sm152_154. Not weakened |
| 30 | `git show --numstat` 563cd4ca9 · c3c118b3c · d8b22ae96 | write.py 30/17 · 2/1 · 5/3; node_writer.py 6/1 (d8b22ae96); tests 22/2 + 45/1 + 2/1. No ceiling stated in the goal |
