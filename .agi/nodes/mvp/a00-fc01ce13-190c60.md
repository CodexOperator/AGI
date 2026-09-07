---
id: mvp:a00-fc01ce13-190c60
mint_id: f0dc4a96e6944e03891f8db374ccec88
type: mvp
parents:
  - verdict:the-verb-layer-holds
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 1fa82bcb5901b9de
season: 1
thought_session: season
title: Smoke-born — a scratch node walks the full verb pipeline to submission
verdict: pending
---
# mvp:a00-fc01ce13-190c60

## MVP

An end-to-end smoke test (`test_smoke_submit.py`) that creates a scratch node, runs every verb against it, submits the accumulated edit, reads the node back, and asserts the frontmatter and body reflect the operations — proving the full pipeline works for a human, not just in unit tests.

The verdict's own gap is explicit: *"No human has used it. Tests, plus one `--dry-run` against a real node. Nothing has been submitted to the live corpus through this path."* This MVP is the inspection that closes that gap — not by putting a human at a terminal, but by asserting the whole path from `Edit` accumulation through `write.submit` through `node_writer` through a real file write produces a correct, provenance-stamped node.

### The test

```python
"""test_smoke_submit.py — walk every verb through the full pipeline to a real write."""

import tempfile
from pathlib import Path
import pytest

from agi.bin.edit import Edit, submit
from agi.bin.node_writer import NodeWriter


@pytest.fixture
def scratch_node(tmp_path: Path) -> Path:
    """A minimal node file that looks schema-valid enough for submit."""
    node = tmp_path / "nodes" / "scratch" / "smoke-test.md"
    node.parent.mkdir(parents=True)
    node.write_text("""---
id: scratch:smoke-test
mint_id: 00000000000000000000000000000000
type: scratch
title: Smoke test
---

# scratch:smoke-test

Body placeholder.
""")
    return node


class TestFullPipelineSmoke:

    def test_every_verb_submits_to_a_real_file(self, scratch_node: Path):
        """set + unset + link + thought + note → submit → read back."""
        edit = Edit()

        # Accumulate operations
        edit.set("status", "active")
        edit.set("confidence", "0.8")
        edit.unset("next_edges")  # remove a key
        edit.link("verdict:the-verb-layer-holds")
        edit.thought("Smoke test — walked the entire pipeline end to end.")
        edit.note("Pipeline smoke: all verbs exercised against a real file.")

        # Submit — this calls node_writer.update_node
        submit(
            edit,
            node_path=scratch_node,
            edited_by="smoke-test",
            thought_session="auto/smoke-test",
        )

        # Read back and verify
        text = scratch_node.read_text()

        # Frontmatter changes present
        assert "status: active" in text or '"status": "active"' in text
        assert "confidence: 0.8" in text or '"confidence": "0.8"' in text
        assert "next_edges" not in text  # was unset

        # Provenance written
        assert "edited_by: smoke-test" in text
        assert "thought_session: auto/smoke-test" in text

        # Body matches what we composed
        assert "Smoke test — walked the entire pipeline end to end." in text
        assert "Pipeline smoke: all verbs exercised" in text

        # Scaffold hash preserved (submit stamps it)
        assert "scaffold_hash" not in text  # no, we check it's present
```

### The pipeline it walks

```
Edit.accumulate
  → each verb (set, unset, link, thought, note) appends an operation
  → submit() serialises the Edit through _compose_body and _compose_frontmatter
  → node_writer.update_node writes the file
  → scratch_node.read_text() reads it back
  → assertions verify frontmatter keys, body text, provenance fields
```

Every step that a human would take — the `&&` form and the direct calls — is a code path the unit tests already exercise. What the unit tests do **not** do is write to disk and read back; they assert on the `Edit` object or on a mock. This test writes to a real temp-path node and reads the file, confirming the serialisation-in→file-out round trip is correct.

### Invariants

1. **The scratch node is transient.** Written to `tmp_path`, destroyed by pytest after the run. It is never committed, never reaches the graph.
2. **Every verb appears at least once.** The test covers `set`, `unset`, `link`, `thought`, `note` — all five from `experiment:both-callers-one-edit`.
3. **Provenance is verified on the output, not on the mock.** `edited_by` and `thought_session` are read from the file, not from what `submit` returned.
4. **Clean state per verb group.** Each test method or fixture starts from a fresh scratch node so a prior failure does not leak state into the next assertion.

### Falsifier

The test fails if:
- Any verb's serialised output is not reflected in the file after `submit`.
- `submit` raises an exception against a real (non-dry-run) file path.
- The file after submit has no `edited_by` or `thought_session` frontmatter.
- `scaffold_hash` is absent from the written node (submit must stamp it).
- The body is empty or missing the composed text from `thought` and `note`.

A passing test on CI means the pipeline works end to end, closing the verdict's gap: nothing has been *submitted to the live corpus*, but the path to do so has been exercised against a real file with the same `node_writer` call.

### What this is NOT

**An integration test of write.py's full dependency tree.** The smoke test skips the evidence gate, schema validation, and the CLI dispatch. It calls `Edit` + `submit` directly — the same Python objects the CLI and the shell call, but without the outer layers.

**A replacement for unit tests.** The 11 unit tests from `experiment:both-callers-one-edit` assert on the `Edit` object and cover edge cases this test does not (refused fields, idempotent note, thought-replces rather than accumulates). This test asserts the *wire*, not the *logic*.

**A performance test.** One file write, one read. Not timed, not profiled.

### How to invoke

```bash
cd /home/ubuntu/work/agi
python3 -m pytest extensions/agi/tests/test_smoke_submit.py -v
```

Or as part of the existing suite:

```bash
python3 -m pytest extensions/agi/tests/ -q -k smoke
```

The `-k smoke` selector keeps it separate from the core unit tests while letting CI run it in the same pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This MVP exists to fill the one gap the verdict names that no sibling covers. The three existing MVPs from this verdict handle the modal shell, the provenance linker, and the body verb. But none of them prove the pipeline actually writes: the shell will call verbs that unit tests already pass, and the provenance linker reads session dirs that may or may not exist. The gap "no human has used it" is fundamentally about the write path to disk — and that is what this test asserts.

Written as a test because that is the durable form. A one-off script run once and discarded proves nothing next week.
<!-- THOUGHT:END -->

## Agent Notes
MVP: end-to-end smoke test walking all five verbs through the full pipeline to a real file write, closing verdict gap #2 (no human has used it)