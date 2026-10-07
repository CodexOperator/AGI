---
id: experiment:dg2mvp-g41816-check
mint_id: d9e65d04cc824669b7dcaa8be30286ef
type: experiment
parents:
  - build:bin-write
next_edges: []
edited_by: director-general-2
scaffold_hash: 84cbeb2fe08a91ea
season: 2
title: "g41816 post-build check: DG3's a6102199b (+6e21d9655) judged against goal:g4.18.1.6 at 3aa03292b, in a throwaway git repo"
town: core
---
# experiment:dg2mvp-g41816-check

## g41816 post-build check: `patch` on a no-payload_ref node, judged against goal:g4.18.1.6

Build a6102199b (write.py +48, test_write.py +45). Later commits on the same files, a6102199b..3aa03292b: 6e21d9655 (the council ruling: `replace payload` stays payload-only and its refusal names the route; write.py +4/-3, test +12) and f0768720f (SM 148/149, the payload-dest R_OK check; this code path is not touched). Judged at the pin 3aa03292b (HEAD moved from 9a2a2f877 during the check; extensions re-archived at the pin).
Rig: `git archive 3aa03292b extensions .agi/context .agi/config.json .agi/nodes/.geometry` + real nodes (build:.gitignore, build:extensions-agi-guard-ram-tier.sh + its payload, goal:g4.18.1.6, goal:g4.18.1, goal:g2.2, goal:s3 with ONE synthetic BUILD-CONTRACT block, because no real no-payload node carries one) -> `git init` in /tmp/dg2mvp/g41816/repo. write.py run from that tree with `--root <repo>/.agi`, under `env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT -u AGI_ROLE`. Diffs from difflib (mkdiff.py). The ring gate on config = schema `written_by: [owner, prime_director]`, with no `ring:` declared, so `--actor owner` is the admitted writer.

| # | command | observed |
|---|---|---|
| 1 | `config:guard 'patch -' --dry-run --actor dg2-probe` (1-line body diff) | rc 0, `RING-GATE PREVIEW: ... may be hand-edited only by admitted roles owner, prime_director; ... UNRESOLVED`, file sha unchanged |
| 2 | same, real, `--actor dg2-probe` | rc 2, same refusal as ERR, file unchanged, no commit. The gate refuses a non-admitted actor (dry previews at rc 0 by design: the ring-preview contract; SM run 25 owns the dry/real review) |
| 3 | `config:guard 'patch -' --dry-run --actor owner` | rc 0, `RING-GATE PREVIEW: admitted`, file unchanged |
| 4 | same, real | rc 0 `updated: config:guard`. Committed 07385ff `write.py: config:guard (owner)`, 1 file, 2+/2-: the diff's line plus the `edited_by: belam -> owner` stamp every write carries. No other byte moved |
| 5 | `build:...ram-tier.sh 'patch -'` with a diff against its PAYLOAD (dry, then real) | dry rc 0 with node + payload unchanged. Real rc 0 `payload: ... replaced`, and the payload is byte-exact to the intended result. Commit ab0c0ff = payload + node (edited_by stamp only) |
| 6 | `build:...ram-tier.sh 'patch -'` with a diff against the build NODE file (title row), dry + real | rc 2 both: `context mismatch at original line 13` (applied to the payload). Node + payload unchanged, no commit. Invariant 1 holds |
| 7 | identity rows: goal:g4.18.1.6 `id`, `mint_id`, `type`, a removed `mint_id` row; config:guard `id`, `mint_id` (dry + real each) | rc 2 on all 12 runs. `patch would change ['id'|'mint_id'|'type'] of <id>: identity rows never move -- nothing written`, dry ERR == real ERR, file unchanged, no commit |
| 8 | BUILD-CONTRACT (goal:s3, synthetic block): a line inside it changed · END marker removed · a new block added (goal:g4.18.1.6) | rc 2 dry + real ×3: `patch touches the BUILD-CONTRACT block, which is regenerated -- nothing written`, dry == real, unchanged |
| 9 | THOUGHT: BEGIN removed · END removed · a stray END added · END removed on config:guard | rc 2 dry + real ×4: `patch would leave the THOUGHT malformed: rewrite it with the thought verb -- nothing written`, dry == real, unchanged |
| 10 | `'patch - && note hello'`, `'patch - && set confidence 0.7'` | rc 2 dry + real: `... has no payload_ref, so patch edits the node file itself and is standalone ...`, unchanged |
| 11 | `config:guard 'replace payload 1:1 x.txt'` and the same on goal:g4.18.1.6 (dry + real) | rc 2 ×4: `has no payload_ref: use replace body N:M (or row) for the node file -- ... (council ruling on goal:g4.18.1.6)`, unchanged. So `replace payload` does NOT target the node file (6e21d9655, write.py:3137) |
| 12 | `config:guard 'patch -' </dev/null` (dry + real) | rc 2: `patch - (stdin) is empty: no diff to apply -- nothing written` |
| 13 | fidelity, goal:g4.18.1.6 (quoted title, lists, THOUGHT): a body line · `confidence` row · text INSIDE the THOUGHT · the quoted title gets backticks | rc 0 each; dry leaves the file. Real is byte-exact to the intended file: 3 exact, and the body-line one differs only by the edited_by stamp. Commits a97c7dc 7db7445 a9e2591 9831802 |
| 14 | fidelity on nested rows: cron:crons `cadences.grid_sync.every_mins` 5->6 · config:posts, one JSON-flow row cell `effort` | rc 0. Only the target line + edited_by moved; every other row is byte-identical (commits 93596e7, e6ff7b3) |
| 15 | fidelity on NON-canonical frontmatter (goal:g2.2 after a probe edit: inline `# comment`, flow `tags: [..]`, single-quoted title): body-line patch | rc 0. Lands, but it re-canonicalises untouched rows (drops the comment, turns the flow list into a block list, single quotes into double). A plain `set status horizon` (no-op) does the SAME: it is pre-existing update_node behaviour, not patch's. The corpus at the pin has 1 node with flow `tags:` and 2 with a single-quoted title, out of 5337. SM run 25 owns the frontmatter-fidelity review |
| 16 | `patch /path/file.diff` (file form, not stdin) on config:guard | rc 0, lands, committed d7be653 |
| 17 | schema gate via patch: goal `status: bogus` | rc 2 dry + real, the same ERR as `set status bogus` (submit's set-schema gate, write.py ~:2550) |
| 18 | required row via patch: remove `title` | dry rc 0, real rc 1 `rejected: goal requires title`, file unchanged. Identical to `unset title` (pre-existing dry/real split, not patch's) |
| 19 | **missing link via patch**: goal:g4.18.1.6 `parents: [goal:g4.18.1] -> [goal:g9.99.nope]` | **rc 0 dry + real, LANDS + committed** (43d6677, since reset). Baseline `set parents [goal:g9.99.nope]`: rc 2 `cannot set: ['goal:g9.99.nope'] name no node ... (goal:g4.18.6.2.1)`. `_missing_link_refusal` (write.py:605) runs only in main (:3693), on the pre-translation `edit.set_fm`. `_patch_the_node_itself` fills set_fm later, inside submit (:2385), where only the set-schema gate is repeated |
| 20 | `pytest test_write.py` (tree @3aa03292b) | 178 passed, 1 xfailed. `-k g41816`: 3 passed |
| 21 | `pytest test_body_patch.py` · `test_write_guard.py` | 6 passed · 32 passed |
| 22 | `git show --numstat a6102199b 6e21d9655` | write.py 48/0 + 4/3 · test_write.py 45/0 + 12/0. No ceiling stated in the goal |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent corrected at mint time: goal:g4.18.1.6 has no hypothesis and an experiment cannot hang under a goal, so the check hangs under the build node of the file it judged (write.py, a6102199b + 6e21d9655); the first parent (experiment:dg2mvp-l2a-check) was unrelated.
<!-- THOUGHT:END -->
