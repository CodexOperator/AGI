---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (22:4xZ 09-29) — seat agi-b1; owner: "Keep working till 7pm" → STOPPED 23:00Z, idle until a nudge
| | |
|---|---|
| post | director-general-3 · stage 3 of 3 — MVPs + build nodes + tests (a build may take [goal, idea]) |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-post |
| sessions | DG3 = agi-b1 · DG2 = agi-40 · DG1 = agi-77 · sanctuary-master = agi-b8 · alive = agi-13 · belam = agi-f0 — hand off by SendMessage + ONE council-loop room line |
| now | bundle 3 CLOSED. Bundle 4 (base 1f39ffb1c): W-G (.1 + .2) · W0 · W1a · W1b · W2a landed; SM runs 1-3 residues 81-96 answered (closed or banked); W2a + fixes await SM's re-mur · residue 96 closed 389afc3e1 · manifest-IP red closed f7a91e213 |

## §1 Plan — bundle 4 (goal:g7.16.1.4; DG2 verdicts verdict:dg2b4-*, DG1 re-scopes 68d4c8504 + d4a186957 + d1de2e804)
```
done   W-G.1 41107692f (+mvp 0a58fe968, build:GOALS.md retired e6bbc6527) · W-G.2 254f58ef7 (+mvp 08b921fd8) · W0 82fce8a34
done   W1a 387359c62 (+mvp 5952b7131): node_writer.body_rows + write.py row <n>[:<i>-<j>]
done   W1b 14cf86000 (+mvp 82c4ec6d4): a write.py verb in MAIN commits itself by exact path
done   W2a 58332a732 (+mvp fe0230f3f): links.resolve_mint (no shape check: the Prime 22:1xZ) + links.py mint + write.py mint target
done   residues 81-85 9eaf5992f · 86 claim corrected on mvp:dg3b4-wg2 · 87 88 90 93 95 c13eec672 · 89 f9261c83e · 91 92 fd8d74ab3
done   96 389afc3e1: write._row_range, ONE resolver for submit + --dry-run (preview shows a:b, out of range rc 2) · f7a91e213: c13eec672's
       verify_unified reason named a dotted goal id -> test_rendered_manifest_names_no_box_detail red; reworded via write.py sub (data-identical)
FIRST  read the inbox: SM's re-mur of W2a + c13eec672 + f9261c83e + fd8d74ab3 (wf key in the dm) -> close in-loop; add 389afc3e1 + f7a91e213 to SM's scope
BUILD1 W1 nested row (alive 841857ddb, council input on goal:g7.16.1.4): `row` must address a NESTED frontmatter row -- manifest.<key> in
       command:commands (~2600, ~3019): unset drops only top-level keys, `set manifest` re-serialises ~2400 lines. NO new verb: extend `row`
       (e.g. `row manifest.<key> <src|->` replace, empty src = remove). BLOCKS DG4's retire of unify.py + verify_unified.py -- build it FIRST
       MEASURED 22:4xZ: every frontmatter write goes node_writer.update_node(set_fm=) = a whole re-serialise (a 1-string sub re-flowed 30
       lines, f7a91e213); rows sit at 3-space indent under `manifest:` (commands.md:764), `  unify.py::` :2600, `  verify_unified.py::` :3019.
       Shape: a raw frontmatter span splice in node_writer (block = `   <key>:` to the next line at indent <= 3), yaml.safe_load before/after
       must differ in manifest[<key>] + edited_by ONLY, else refuse; reuse _row_range's refusal style; a test per replace + remove + missing key
NEXT   banked residues (§6 BANKED 86 94), then W1c goal:g4.18.5.3 (plan in §6), then W2b.1 (.6.2.1) · W2b.2 (.6.2.2) ·
       W2c A (.6.3.1 PARENTS ONLY, loader.py:210-230) · W2c B/C (.6.3.2/.3) · W2e (.6.5) · W2d .4.1 UNHELD (re-mint experiment:osc-band-call-run-a00-66d002ad ONCE,
       old history under the old ref, old->new in its THOUGHT; hypothesis keeps c89ca4b1; write.py refuses a mint change -> ONE owner-cited path) ·
       W3a/b (.7.1-.2) · W3c-1 additive before the W3c-2 atomic cut (ceiling 125, one row; SM checks: never two read paths taught)
NEVER  hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids (superseded)
```

## §2 Landed
- bundle 1-3: grid history of this card (bundle 3 CLOSED at 1f39ffb1c)
- bundle 4: 41107692f 0a58fe968 e6bbc6527 82fce8a34 254f58ef7 08b921fd8 9eaf5992f 387359c62 5952b7131 14cf86000 82c4ec6d4
  58332a732 fe0230f3f c13eec672 f9261c83e fd8d74ab3 389afc3e1 f7a91e213

## 🔴 Where it stops
Stopped at the owner's 23:00Z line after residue 96 + the manifest-IP red; nothing live (spawn budget 0/30), nothing uncommitted of mine.
The next session: FIRST row of §1, then BUILD1 (its measured shape is in §1), then NEXT.
First command at wake:
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path, gated `[ ! -e .agi/sessions/verify-suite.lock ]`; never switch branches, stash or reset |
| write.py in MAIN (verbs since 14cf86000; create + adopt since fd8d74ab3) | commits ITSELF by exact path; never a second git commit of that node |
| pytest takes verify-suite.lock | conftest holds it for EVERY session, even one file: never two pytest at once; another post's loop flips it between files -> wait for absence per file |
| pkill -f / pgrep -f <pattern> | match their own shell line (exit 144): find a process by its ppid chain |
| derive-commands --all | appends the retired command table to CLAUDE.md (tables lag command:commands): edit the derived row by hand |
| command:commands placeholders | an argv `<x>` must equal an arg name exactly (`<mint_id>`, not `<mint-id>`) |
| `send.py read <self>` | always `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] |
| replace body on a heading/paragraph line | refused: widen to whole section or the blank line above |
| anonymize / manifest scanners | a dotted goal id like g7.16.1.4.1 reads as an IP in command:commands text: say "bundle 4 row W-G" there |

## §5 Verification (22:4xZ): links 5166/0 · write 147p/5x · node_writer 111p/3x · commands_manifest 181p · write_self_row 8p · actor_rows 24p · guard 29p · sub 17p · help 72p/8s

## §6 BANKED
- 86 (SM wf_8ce06028-a81): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left; links.py does not check parents.
  Options: (a) re-wire both into verification level quick as a `goals-integrity` command (recommended) · (b) retire both and re-point the W2c-B xfail row.
- 94 ([red] with belam from SM): 4 engine subprocess callers of the write.py CLI now auto-commit: rotate.py closeout g17.1 note (keep-and-say: a closeout
  commits anyway) · season.py:274 · sensei.py:2465 · failures.py:361 -> an explicit opt-out (AGI_WRITE_NO_COMMIT=1 in their subprocess env) until each is reviewed.
- W1c goal:g4.18.5.3 (verdict:dg2b4-w1c lean 55): 4 rotation commit paths = 621 lines (_ack_commit_seats 150 · _publish_row_to_authority 165 ·
  _commit_spawn_row 188 · _commit_stops_row 118) own throwaway-index + FETCH_HEAD plumbing; W1b's working-tree commit is the WRONG primitive.
  Plan: one `_commit_posts_row(root, content, *, parent_ref="HEAD", extra_blobs=(), push=None)` in rotate.py, then re-point one path per commit,
  test_rotate after each; (3) first (drop _posts_load_error/_row_names onto the one parser; `frontmatter` name taken at rotate.py:78).
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to commits after 2c412e5bb, then complete it.

## Findings for the next bundle
- derived command tables (QUICKSTART, skills/agi) lag command:commands; .agi/nodes/.geometry/commands.md.bak is TRACKED with id command:commands
- test_workflow's leak detector flags --basetemp /tmp dirs as the real sessions dir · test_skills_first_turn_entry red: agi-post + agi-stream missing
- write.py stamps town: core on local-maxxing nodes · 4 build nodes carry stale BUILD-CONTRACTs · memory_alarm.py has no build node
- test_sensei_wake_audit item2 red (pre-existing) · heal._watch_seats tests read the live PSI (flaky under pressure)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
