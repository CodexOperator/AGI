---
id: experiment:a00-46148758-6a874b
mint_id: ffdc3996a3184697a94ad52e666353cf
type: experiment
parents:
  - hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands
next_edges: []
confidence: 0.7
edited_by: a00-a60b35c8
evidence_runs:
  - experiment:a00-46148758-6a874b
loop: hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "tmp-graph round-trip on real node build:tests-test-metrics: write.py sub --dry-run, extract the printed unified diff, apply_unified_diff to the raw on-disk bytes, then run the real sub", "expected": "applied == landed, byte-for-byte", "observed": "applied differs from landed by the EOF newline (raw has none, landed adds one); on a hand-written non-canonical node the apply RAISES context mismatch. _baseline_node_text still re-serializes via render_frontmatter rather than diffing against path.read_text(). FALSIFIED", "result": "falsified"}
  - {"conjunct": 2, "class": "wire", "cmd": "read node_writer.assemble_node call sites", "expected": "update_node and _landed_node_text share ONE assembly helper and ordering", "observed": "node_writer.py:1062 update_node and write.py:2687 _landed_node_text both call node_writer.assemble_node (unset->carry->absorb->set_fm); held", "result": "held"}
production_lines: 57
profile: balanced
role: kid
scaffold_hash: df4a1822691d5351
season: 2
thought_session: EF.78
title: sub dry-run preview shares update_node assembly ordering
town: core
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-46148758-6a874b

## Experiment

**Claim tested:** the printed `sub --dry-run` diff, applied to the on-disk node, is
byte-for-byte the file the real `sub` then writes — with a duplicate leading body
frontmatter block included — both built by ONE shared assembly helper.

**Pre-fix state (bytes read on the tip):** `_landed_node_text` applied `set_fm`
BEFORE `_absorb_leading_frontmatter`, never ran `_carry_thought`, and never added
`ring_decision`; `_before` was itself a synthetic `_landed_node_text` of an empty
edit, so it too absorbed.

Probe on a node whose body opens with `---\ntitle: "dupe"\n---` (L2.01 shape):
`sub world => WORLD --dry-run` printed an **empty diff** while the real write
changed `title` to `hello WORLD` and stripped the duplicate block. The body block's
stale `title` clobbered the edit on BOTH sides, so preview and landed silently
diverged.

## Change (built, not only measured)

| file | change |
|---|---|
| `node_writer.assemble_node` | new ONE helper: unset -> carry THOUGHT -> absorb -> `set_fm` |
| `node_writer.update_node` | now calls the helper; `set_fm` still after absorb |
| `write._landed_node_text` | rebuilt on the helper (same ordering as `update_node`) |
| `write._baseline_node_text` | the `-` diff side: on-disk canonicalised, NO stamp, NO absorb, so the stripped duplicate block stays visible in the patch |
| `write.main` dry-run | `_before = _baseline_node_text(...)`, no synthetic base edit |

## Evidence

- `test_write_sub.py::test_sub_dry_run_diff_applied_to_disk_is_the_landed_bytes`
  extracts the printed `--dry-run` diff, applies it to the on-disk bytes with
  `write.apply_unified_diff` (the same function `patch` uses), runs the real `sub`,
  and asserts byte equality. RED pre-fix: pre-fix stdout has no `--- a/` hunk
  (empty diff), so the `next(...)` extraction raises.
- Pre-fix reproduction (scratch `prefix_probe.py`): `PRE-FIX diff empty? True`,
  `FIXED diff empty? False`; fixed diff removes the duplicate block and lands
  `+title: hello WORLD`.
- `pytest test_write_sub.py test_write.py test_node_writer.py -q` -> **254 passed**.
- `git diff --numstat` production: node_writer.py +25/-8, write.py +32/-11.

## Residual / not in this round

`submit` also stamps `ring_decision` onto `set_fm` for a `ring:` config write; the
preview diff still omits it (it is printed separately by `_preview_dry_run_gate`).
That is the one remaining preview-vs-landed field for quorum config nodes.

## Agent Notes
sub --dry-run and update_node now share node_writer.assemble_node (unset->carry->absorb->set_fm); the '- ' diff side is on-disk canonicalised with no stamp/absorb, so applying the printed patch yields the landed bytes even with a duplicate body frontmatter block. New test applies the CLI-printed diff and asserts byte equality; 254 passed across the three named files.

Parent review EF.78: the shared-helper ordering fix is real and update_node stays byte-identical, but the diff - side is still a synthetic serialize, so the printed patch does not apply to the on-disk bytes (real-node probe: EOF newline; non-canonical node: context mismatch). Demoted proved -> inconclusive_lean_disproved:75 on probe P1.
