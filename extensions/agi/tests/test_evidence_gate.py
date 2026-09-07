"""Tests for the H4 orphan-verdict gate — bin/evidence_gate.py + both writer paths.

Rule under test: `proved`/`disproved` require `evidence_runs >= 1`;
`pending` and `inconclusive_lean_*` are permitted without evidence.
Violations demote (never discard) the node.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"


def _load(name, filename=None):
    path = BIN / (filename or f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


eg = _load("evidence_gate")
cli = _load("cli")
post_wire = _load("post_wire")


ALL_VERDICTS = [
    "proved",
    "disproved",
    "inconclusive_lean_proved:60",
    "inconclusive_lean_disproved:40",
    "pending",
]


# ---------------------------------------------------------------- pure gate


@pytest.mark.parametrize("verdict", ALL_VERDICTS)
def test_taxonomy_is_valid(verdict):
    assert eg.is_valid_verdict(verdict)


def test_cli_uses_the_shared_taxonomy():
    """One regex, not two — cli.py must not drift from the gate."""
    assert cli.VERDICT_RE is eg.VERDICT_RE


@pytest.mark.parametrize("bad", ["PROVED", "maybe", "inconclusive_lean_proved", "", None])
def test_invalid_verdicts_rejected(bad):
    assert not eg.is_valid_verdict(bad)


@pytest.mark.parametrize("verdict", ["proved", "disproved"])
def test_decisive_without_evidence_is_demoted(verdict):
    res = eg.apply_gate(verdict, 0)
    assert res.demoted
    assert not res.ok
    assert res.verdict == eg.DEMOTION[verdict]
    assert res.original == verdict
    assert res.messages  # loud


@pytest.mark.parametrize("verdict", ["proved", "disproved"])
def test_decisive_with_evidence_passes(verdict):
    # goal:g7.3: evidence is a resolvable reference, never a bare count.
    res = eg.apply_gate(verdict, ["exp:real"], corpus={"exp:real"})
    assert res.ok
    assert res.verdict == verdict
    assert res.messages == []


@pytest.mark.parametrize(
    "verdict", ["pending", "inconclusive_lean_proved:60", "inconclusive_lean_disproved:40"]
)
def test_uncertain_verdicts_permitted_without_evidence(verdict):
    res = eg.apply_gate(verdict, 0)
    assert res.ok
    assert res.verdict == verdict
    assert res.messages == []


def test_bypass_is_loud_and_preserves_verdict():
    res = eg.apply_gate("proved", 0, bypass=True)
    assert res.ok
    assert res.bypassed
    assert res.verdict == "proved"
    assert any("BYPASSED" in m for m in res.messages)


def test_bypass_is_a_noop_when_evidence_exists():
    res = eg.apply_gate("proved", ["exp:real"], bypass=True, corpus={"exp:real"})
    assert not res.bypassed and res.ok


@pytest.mark.parametrize(
    "value",
    [None, 0, 2, -5, "3", "many", True, False],
)
def test_normalize_evidence_runs_scalars_never_count(value):
    """goal:g7.3 — a scalar is an unverifiable self-attestation and buys
    nothing, corpus or no corpus.

    Until 2026-08-27 an int counted itself: `evidence_runs: 3` returned 3 and
    was enough to hold a `proved`. H4c had already removed the `"synthetic"`
    sentinel for being uncheckable; a bare integer is the same hole and is
    exactly as cheap to type. Only a reference that resolves to a real node
    counts now."""
    assert eg.normalize_evidence_runs(value) == 0
    assert eg.normalize_evidence_runs(value, corpus={"exp:real"}) == 0


@pytest.mark.parametrize(
    "value,unverifiable",
    [(3, True), (1, True), (True, True), ("3", True),
     (0, False), (None, False), (["exp:real"], False), ("many", False)],
)
def test_unverifiable_attestation_is_reported_not_destroyed(value, unverifiable):
    """goal:g7.3 kept the honest-count path visible. The count stops
    certifying a verdict; it does not become indistinguishable from absence,
    so metrics can still report how much of the corpus needs converting."""
    assert eg.is_unverifiable_attestation(value) is unverifiable


@pytest.mark.parametrize(
    "value",
    [[], ["synthetic"], [{"run": 1}, {"run": 2}], {"a"}, ["exp:real"]],
)
def test_normalize_evidence_runs_lists_need_a_corpus(value):
    """H4c: a gate that cannot resolve must not silently trust a length.
    No corpus supplied -> every list-shaped value counts 0, even one that
    would resolve if a corpus were given (see the with-corpus tests below).
    """
    assert eg.normalize_evidence_runs(value) == 0


def test_normalize_evidence_runs_sentinel_string_counts_zero_not_one():
    """The exact H4c defect: `["synthetic"]` must not satisfy `>= 1`."""
    corpus = {"exp:real"}
    assert eg.normalize_evidence_runs(["synthetic"], corpus=corpus) == 0


def test_normalize_evidence_runs_resolves_a_real_id():
    corpus = {"exp:real"}
    assert eg.normalize_evidence_runs(["exp:real"], corpus=corpus) == 1


def test_normalize_evidence_runs_unresolvable_id_shaped_entry_counts_zero():
    """Id-*shaped* but not in the corpus (typo, deleted node) — silent 0,
    not a taxonomy violation (that's a different, louder failure mode)."""
    corpus = {"exp:real"}
    assert eg.normalize_evidence_runs(["exp:ghost"], corpus=corpus) == 0


def test_normalize_evidence_runs_mixed_list_counts_only_resolvable():
    corpus = {"exp:real"}
    assert eg.normalize_evidence_runs(
        ["synthetic", "exp:real", "exp:ghost"], corpus=corpus
    ) == 1


# ------------------------------------------------------- taxonomy violations


@pytest.mark.parametrize(
    "value,violations",
    [
        (None, []),
        (0, []),
        ("3", []),
        (["exp:real"], []),
        (["synthetic"], ["synthetic"]),
        (["exp:real", "synthetic"], ["synthetic"]),
        ([{"run": 1}], [{"run": 1}]),
        (["exp:ghost"], []),  # id-shaped, just doesn't resolve — not a violation
    ],
)
def test_evidence_runs_violations(value, violations):
    assert eg.evidence_runs_violations(value) == violations


def test_is_node_id_shaped():
    assert eg.is_node_id_shaped("exp:real")
    assert not eg.is_node_id_shaped("synthetic")
    assert not eg.is_node_id_shaped("run-a")       # no colon
    assert not eg.is_node_id_shaped(1)
    assert not eg.is_node_id_shaped(None)


def test_build_corpus_reads_declared_ids(tmp_path):
    d = tmp_path / "nodes" / "experiment"
    d.mkdir(parents=True)
    (d / "e1.md").write_text('---\nid: "exp:e1"\ntype: experiment\n---\n\nbody\n')
    (d / "e2.md").write_text("---\ntype: experiment\n---\n\nno id field\n")
    corpus = eg.build_corpus(tmp_path / "nodes")
    assert corpus == {"exp:e1"}


def test_build_corpus_missing_dir_is_empty_not_a_crash(tmp_path):
    assert eg.build_corpus(tmp_path / "nowhere") == frozenset()


# --------------------------------------------- apply_gate: reject vs demote


def test_sentinel_evidence_rejects_a_decisive_verdict_not_demotes():
    """H4c: writing 'synthetic' is worse than writing nothing — it is an
    active false claim, so it is rejected (nothing written), not demoted
    the way an honestly-empty evidence_runs is."""
    res = eg.apply_gate("proved", ["synthetic"], corpus={"exp:real"})
    assert res.rejected
    assert not res.demoted
    assert not res.ok
    assert res.taxonomy_violations == ["synthetic"]
    assert any("REJECTED" in m for m in res.messages)


def test_empty_evidence_still_demotes_not_rejects():
    """Contrast case: genuinely no evidence (not a sentinel) keeps the
    softer, existing demotion behaviour."""
    res = eg.apply_gate("proved", [], corpus={"exp:real"})
    assert res.demoted
    assert not res.rejected


def test_resolvable_evidence_passes():
    res = eg.apply_gate("proved", ["exp:real"], corpus={"exp:real"})
    assert res.ok
    assert res.verdict == "proved"
    assert res.evidence_runs == 1


def test_bypass_overrides_rejection():
    res = eg.apply_gate("proved", ["synthetic"], bypass=True, corpus={"exp:real"})
    assert res.bypassed
    assert not res.rejected
    assert res.ok


@pytest.mark.parametrize(
    "verdict", ["pending", "inconclusive_lean_proved:60", "inconclusive_lean_disproved:40"]
)
def test_sentinel_evidence_does_not_reject_uncertain_verdicts(verdict):
    """H4c must not touch the honest-uncertainty path: pending/lean verdicts
    never require evidence, so a taxonomy violation sitting in evidence_runs
    (leftover data, unrelated to this write) can't block them either."""
    res = eg.apply_gate(verdict, ["synthetic"], corpus={"exp:real"})
    assert res.ok
    assert not res.rejected
    assert not res.demoted
    assert res.verdict == verdict


def test_stamp_records_demotion():
    fm = eg.stamp({}, eg.apply_gate("proved", 0))
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert fm["demoted_from"] == "proved"
    assert fm["demote_reason"]
    assert fm["evidence_runs"] == 0


# ------------------------------------------- shadow fields (`status:`)


@pytest.mark.parametrize("decisive", ["proved", "disproved"])
def test_stamp_demotes_status_shadow_in_lockstep(decisive):
    """A demoted node must not read 'proved' anywhere in its frontmatter.

    Rewriting only `verdict:` left `status: proved` standing next to
    `verdict: inconclusive_lean_proved:50` on 42 agi-tree nodes.
    """
    fm = eg.stamp({"status": decisive}, eg.apply_gate(decisive, 0))
    assert fm["status"] == fm["verdict"] == eg.DEMOTION[decisive]
    assert decisive not in (fm["status"], fm["verdict"])


@pytest.mark.parametrize("lifecycle", ["pending", "in_progress", "done", "open",
                                       "extended", "abandoned", "active",
                                       "horizon", "phasing-out", "complete"])
def test_stamp_never_touches_a_lifecycle_status(lifecycle):
    """`status:` means different things per node type. None of those domains
    contains 'proved'/'disproved', so the verdict gate can never clobber a
    task's, idea's or goal's lifecycle."""
    fm = eg.stamp({"status": lifecycle}, eg.apply_gate("proved", 0))
    assert fm["status"] == lifecycle


def test_stamp_leaves_status_alone_when_nothing_was_demoted():
    fm = eg.stamp({"status": "proved"},
                  eg.apply_gate("proved", ["exp:real"], corpus={"exp:real"}))
    assert fm["status"] == "proved"
    fm = eg.stamp({"status": "proved"}, eg.apply_gate("proved", 0, bypass=True))
    assert fm["status"] == "proved"
    assert fm["evidence_gate"] == "bypassed"


def test_stamp_leaves_tags_alone():
    """Tags are kept as a historical record of the original claim; demotion
    already keeps such nodes out of the standard graph views."""
    fm = eg.stamp({"tags": ["proved", "R2"]}, eg.apply_gate("proved", 0))
    assert fm["tags"] == ["proved", "R2"]


def test_shadow_verdict_fields_matches_what_stamp_rewrites():
    assert eg.shadow_verdict_fields({"status": "proved"}) == ["status"]
    assert eg.shadow_verdict_fields({"status": "disproved"}) == ["status"]
    assert eg.shadow_verdict_fields({"status": "pending"}) == []
    assert eg.shadow_verdict_fields({"status": "inconclusive_lean_proved"}) == []
    assert eg.shadow_verdict_fields({"tags": ["proved"]}) == []
    assert eg.shadow_verdict_fields({}) == []
    assert eg.shadow_verdict_fields(None) == []


# --------------------------------------------- the commit path (on-disk gate)
#
# hypothesis:gate-must-sit-on-the-commit-path. The pure half; the fixture
# half (a real git repo, `grid.cmd_commit`) lives in `test_grid.py`.


@pytest.mark.parametrize("verdict", ["pending", "inconclusive_lean_proved:60",
                                     "inconclusive_lean_disproved:40"])
def test_gate_on_disk_ignores_honest_uncertainty(verdict):
    assert eg.gate_on_disk({"verdict": verdict}, corpus=frozenset()) is None


def test_gate_on_disk_ignores_a_missing_or_non_string_verdict():
    assert eg.gate_on_disk({}, corpus=frozenset()) is None
    assert eg.gate_on_disk({"verdict": None}, corpus=frozenset()) is None
    assert eg.gate_on_disk({"verdict": 1}, corpus=frozenset()) is None


def test_gate_on_disk_passes_an_evidenced_decisive_verdict():
    fm = {"id": "verdict:v", "type": "verdict", "verdict": "proved",
          "evidence_runs": ["exp:r1"]}
    assert eg.gate_on_disk(fm, corpus=frozenset({"exp:r1"})) is None


def test_gate_on_disk_honours_the_bypass_stamp():
    fm = {"verdict": "proved", "evidence_gate": "bypassed"}
    assert eg.gate_on_disk(fm, corpus=frozenset()) is None


@pytest.mark.parametrize("decisive", ["proved", "disproved"])
def test_gate_on_disk_demotes_and_tags_the_commit_path(decisive):
    res = eg.gate_on_disk({"verdict": decisive}, corpus=frozenset())
    assert res is not None and res.demoted and not res.rejected
    assert res.verdict == eg.DEMOTION[decisive]
    assert res.original == decisive
    assert eg.COMMIT_PATH_TAG in res.reason


def test_gate_on_disk_folds_a_taxonomy_violation_into_a_demotion():
    """A writer path rejects `[synthetic]`; on disk it is demoted, and the
    reason still names the violation so it is not read as mere absence."""
    res = eg.gate_on_disk({"verdict": "proved", "evidence_runs": ["synthetic"]},
                          corpus=frozenset())
    assert res.demoted and not res.rejected
    assert res.verdict == "inconclusive_lean_proved:50"
    assert "taxonomy violation" in res.reason
    assert res.taxonomy_violations == ["synthetic"]


def test_gate_on_disk_keeps_the_self_citation_asymmetry():
    exp = {"id": "experiment:x", "type": "experiment", "verdict": "proved",
           "evidence_runs": ["experiment:x"]}
    ver = {"id": "verdict:v", "type": "verdict", "verdict": "proved",
           "evidence_runs": ["verdict:v"]}
    corpus = frozenset({"experiment:x", "verdict:v"})
    assert eg.gate_on_disk(exp, corpus) is None
    assert eg.gate_on_disk(ver, corpus).demoted


def test_demotion_fields_are_stamps_keys_minus_evidence_runs():
    fm = {"verdict": "proved", "status": "proved", "evidence_runs": 2,
          "confidence": 0.9}
    res = eg.gate_on_disk(fm, corpus=frozenset())
    delta = eg.demotion_fields(fm, res)
    assert set(delta) == {"verdict", "demoted_from", "demote_reason", "status"}
    assert delta["verdict"] == delta["status"] == "inconclusive_lean_proved:50"
    assert delta["demoted_from"] == "proved"
    assert "evidence_runs" not in delta          # the author's value survives
    assert "confidence" not in delta             # nothing else is touched
    assert fm["verdict"] == "proved"             # the input dict is not mutated


def test_demotion_fields_leave_a_lifecycle_status_out():
    fm = {"verdict": "proved", "status": "active"}
    delta = eg.demotion_fields(fm, eg.gate_on_disk(fm, corpus=frozenset()))
    assert "status" not in delta


def test_read_frontmatter_text_reads_the_way_the_metric_reads():
    assert eg.read_frontmatter_text("---\nid: x\nverdict: proved\n---\nbody") == \
        {"id": "x", "verdict": "proved"}
    assert eg.read_frontmatter_text("no frontmatter") is None
    assert eg.read_frontmatter_text("---\nid: x\nnever closed") is None
    assert eg.read_frontmatter_text("---\nparents: [unclosed\n---\n") is None
    assert eg.read_frontmatter_text("---\n- a list\n---\n") is None


@pytest.mark.parametrize("line,hit", [
    ("verdict: proved", True),
    ("verdict: disproved", True),
    ('verdict: "proved"', True),
    ("verdict:   proved   # says who", True),
    ("verdict: pending", False),
    ("verdict: inconclusive_lean_proved:50", False),
    ("demoted_from: proved", False),
    ("  verdict: proved", False),        # nested, not a top-level key
])
def test_decisive_line_prefilter(line, hit):
    assert bool(eg.DECISIVE_LINE_RE.search(f"id: x\n{line}\ntype: verdict\n")) is hit


def test_enforce_on_disk_dry_run_writes_nothing(tmp_path, capsys):
    d = tmp_path / "nodes" / "verdict"
    d.mkdir(parents=True)
    p = d / "v1.md"
    p.write_text('---\nid: "verdict:v1"\ntype: verdict\nverdict: proved\n---\nbody\n')
    before = p.read_bytes()
    found = eg.enforce_on_disk(tmp_path, dry_run=True)
    assert [(f.node_id, f.original, f.verdict, f.written) for f in found] == \
        [("verdict:v1", "proved", "inconclusive_lean_proved:50", False)]
    assert p.read_bytes() == before
    out = capsys.readouterr()
    assert "would demote verdict:v1" in out.err
    assert "EVIDENCE-GATE DEMOTED" not in out.out     # the loop.log marker stays honest


def test_enforce_on_disk_empty_tree_is_a_noop(tmp_path):
    assert eg.enforce_on_disk(tmp_path) == []


# ------------------------------------------------------------ cli.py done


@pytest.fixture()
def project(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "nodes" / "experiment").mkdir(parents=True)
    sess = tmp_path / "sessions" / "iter-001" / "a1"
    sess.mkdir(parents=True)
    (sess / "agent.json").write_text(json.dumps({"id": "a1", "status": "running"}))
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _via_subprocess(project, argv):
    return subprocess.run(
        [sys.executable, str(BIN / "cli.py"), *argv],
        cwd=project, capture_output=True, text=True,
    )


def _agent_rec(project):
    return json.loads(
        (project / "sessions" / "iter-001" / "a1" / "agent.json").read_text()
    )


def test_cli_done_demotes_unevidenced_proved(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--evidence-runs", "0"])
    assert r.returncode == 0, r.stderr          # work preserved, not discarded
    assert "EVIDENCE-GATE DEMOTED" in (r.stdout + r.stderr)
    rec = _agent_rec(project)
    assert rec["verdict"] == "inconclusive_lean_proved:50"
    assert rec["demoted_from"] == "proved"
    node = project / "nodes" / "verdict" / "experiment_e1.md"
    assert "verdict: inconclusive_lean_proved:50" in node.read_text()
    assert "demoted_from: proved" in node.read_text()


def test_cli_done_demotes_status_shadow_on_an_existing_node(project):
    """`cli.py done` updates an existing node through `_append_verdict_to_node`,
    which rewrites raw frontmatter lines and so cannot call `stamp()`. It must
    still enforce the same invariant: nothing left reading 'proved'."""
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\nstatus: proved\n"
        "tags:\n  - proved\n---\n\nbody\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--evidence-runs", "0"])
    assert r.returncode == 0, r.stderr
    text = nf.read_text()
    assert "status: inconclusive_lean_proved:50" in text
    assert "verdict: inconclusive_lean_proved:50" in text
    assert "status: proved" not in text
    assert "  - proved" in text            # tags kept as historical record


def test_cli_done_keeps_a_lifecycle_status_on_an_existing_node(project):
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\nstatus: pending\n---\n\nbody\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--evidence-runs", "0"])
    assert r.returncode == 0, r.stderr
    assert "status: pending" in nf.read_text()


def test_cli_done_corpus_includes_worktree_resident_nodes(project):
    """hypothesis:l3w4-branch-tooling-blind (claim i) — a `--branch` kid's
    node lives only in its own git worktree
    (`<main>/.agi/worktrees/<slug>/.agi/nodes/`), so a parent reviewing it
    from the main checkout must have those ids in the evidence corpus.
    Until L3.35 the corpus was built from the main graph alone and the gate
    auto-demoted the parent's decisive verdict to a lean even with the real
    worktree node id cited."""
    kn = project / "worktrees" / "w1" / ".agi" / "nodes" / "experiment"
    kn.mkdir(parents=True)
    (kn / "kid.md").write_text(
        '---\nid: "experiment:kid"\ntype: experiment\n---\n\nrun in the worktree\n'
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1",
                                  "--evidence-runs", "experiment:kid"])
    assert r.returncode == 0, r.stderr
    assert "DEMOTED" not in r.stdout + r.stderr
    assert _agent_rec(project)["verdict"] == "proved"


def test_cli_done_corpus_still_needs_a_real_worktree_node(project):
    """The worktree union must not rubber-stamp: a non-existent id cited as
    evidence still demotes, even when sibling worktrees exist."""
    kn = project / "worktrees" / "w1" / ".agi" / "nodes" / "experiment"
    kn.mkdir(parents=True)
    (kn / "kid.md").write_text(
        '---\nid: "experiment:kid"\ntype: experiment\n---\n\nbody\n'
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1",
                                  "--evidence-runs", "experiment:ghost"])
    assert r.returncode == 0, r.stderr
    assert "EVIDENCE-GATE DEMOTED" in (r.stdout + r.stderr)
    assert _agent_rec(project)["verdict"] == "inconclusive_lean_proved:50"


def test_cli_done_accepts_evidenced_proved(project):
    # goal:g7.3 — the reference has to resolve, so the node it names must
    # exist. The old form (`--evidence-runs 2`) passed with no such node
    # anywhere in the corpus, which is precisely the hole that closed.
    (project / "nodes" / "experiment" / "e0.md").write_text(
        '---\nid: "experiment:e0"\ntype: experiment\n---\n\nbody\n')
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1",
                                  "--evidence-runs", "experiment:e0"])
    assert r.returncode == 0, r.stderr
    assert "DEMOTED" not in r.stdout + r.stderr
    assert _agent_rec(project)["verdict"] == "proved"


def test_cli_done_permits_pending_and_leans_without_evidence(project):
    for verdict in ("pending", "inconclusive_lean_proved:60",
                    "inconclusive_lean_disproved:40"):
        r = _via_subprocess(project, ["done", "1", "a1", "--verdict", verdict,
                                      "--node-id", "experiment:e1"])
        assert r.returncode == 0, r.stderr
        assert "DEMOTED" not in r.stdout + r.stderr
        assert _agent_rec(project)["verdict"] == verdict


def test_cli_done_rejects_invalid_verdict(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "definitely"])
    assert r.returncode == 2
    assert "invalid verdict" in r.stderr


def test_cli_done_infers_evidence_from_node_frontmatter(project):
    """A real experiment must not be punished for a missing flag.

    H4c: the cited runs must resolve against the corpus, so this fixture
    creates real nodes for them (`experiment:run-a`, `experiment:run-b`) —
    bare unresolvable words are covered separately by
    `test_cli_done_rejects_sentinel_evidence_runs`.
    """
    (project / "nodes" / "experiment" / "run-a.md").write_text(
        '---\nid: "experiment:run-a"\ntype: experiment\n---\n\nrun a\n'
    )
    (project / "nodes" / "experiment" / "run-b.md").write_text(
        '---\nid: "experiment:run-b"\ntype: experiment\n---\n\nrun b\n'
    )
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "evidence_runs:\n  - experiment:run-a\n  - experiment:run-b\n---\n\nran it twice\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1"])
    assert r.returncode == 0, r.stderr
    assert "DEMOTED" not in r.stdout + r.stderr
    assert "verdict: proved" in nf.read_text()


def test_cli_done_rejects_sentinel_evidence_runs(project):
    """H4c: `evidence_runs: [synthetic]` must hard-fail (exit 2), the same
    class of failure as a malformed verdict — not a silent pass, and not
    even a demotion (that's reserved for honestly-empty evidence)."""
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "evidence_runs:\n  - synthetic\n---\n\nbody\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1"])
    assert r.returncode == 2
    assert "taxonomy violation" in r.stderr
    assert "verdict: proved" not in nf.read_text()   # nothing written
    assert _agent_rec(project)["status"] == "running"  # agent record untouched


def test_cli_done_no_evidence_gate_bypasses_sentinel_rejection(project):
    nf = project / "nodes" / "experiment" / "e1.md"
    nf.write_text(
        "---\nid: experiment:e1\ntype: experiment\n"
        "evidence_runs:\n  - synthetic\n---\n\nbody\n"
    )
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1", "--no-evidence-gate"])
    assert r.returncode == 0, r.stderr
    assert "EVIDENCE-GATE BYPASSED" in (r.stdout + r.stderr)
    assert "verdict: proved" in nf.read_text()


def test_cli_done_escape_hatch_is_loud(project):
    r = _via_subprocess(project, ["done", "1", "a1", "--verdict", "proved",
                                  "--node-id", "experiment:e1",
                                  "--evidence-runs", "0", "--no-evidence-gate"])
    assert r.returncode == 0, r.stderr
    assert "EVIDENCE-GATE BYPASSED" in (r.stdout + r.stderr)
    assert _agent_rec(project)["verdict"] == "proved"
    assert "evidence_gate: bypassed" in (
        project / "nodes" / "verdict" / "experiment_e1.md").read_text()


# ---------------------------------------------------------- post_wire path


@pytest.fixture()
def wired_project(tmp_path, monkeypatch):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    exp = tmp_path / "nodes" / "experiment"
    exp.mkdir(parents=True)
    (exp / "e1.md").write_text(
        '---\nid: "experiment:e1"\ntype: experiment\n---\n\nbody\n'
    )
    iter_dir = tmp_path / "sessions" / "iter-001"
    iter_dir.mkdir(parents=True)
    monkeypatch.chdir(tmp_path)
    return tmp_path, iter_dir


def _wire(iter_dir, agent):
    (iter_dir / "manifest.json").write_text(json.dumps({"agents": [agent]}))
    import argparse
    return post_wire.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))


def _fm_of(path: Path) -> dict:
    """Parse a node's frontmatter.

    These assertions used to be substring checks against the raw file, which
    made them assertions about SERIALIZATION rather than about the gate: they
    failed the moment `post_wire` stopped emitting its own YAML and delegated
    to the one serializer (goal:s14), because that one quotes a scalar
    containing a colon -- `verdict: "inconclusive_lean_proved:50"`. Both
    spellings load to the identical string and every reader in the engine goes
    through `yaml.safe_load`, so the behaviour never changed; only the bytes
    did. Assert on the parsed value, which is what the gate actually decides.
    """
    import yaml
    return yaml.safe_load(path.read_text().split("---", 2)[1]) or {}


def test_post_wire_demotes_unevidenced_proved(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1", "evidence_runs": 0})
    fm = _fm_of(root / "nodes" / "experiment" / "e1.md")
    assert fm["verdict"] == "inconclusive_lean_proved:50"
    assert fm["demoted_from"] == "proved"


def test_post_wire_keeps_evidenced_proved(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1",
                     "evidence_runs": ["experiment:e1"]})
    fm = _fm_of(root / "nodes" / "experiment" / "e1.md")
    assert fm["verdict"] == "proved"
    assert "demoted_from" not in fm


def test_post_wire_permits_lean_without_evidence(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done",
                     "verdict": "inconclusive_lean_disproved:30",
                     "node_id": "experiment:e1", "evidence_runs": 0})
    fm = _fm_of(root / "nodes" / "experiment" / "e1.md")
    assert fm["verdict"] == "inconclusive_lean_disproved:30"
    assert "demoted_from" not in fm


def test_post_wire_falls_back_to_node_frontmatter_evidence(wired_project):
    """H4c: the fallback value must still resolve against the corpus to
    count — so this fixture cites a real node (`experiment:r1`), unlike
    the pre-H4c version of this test which trusted a bare word."""
    root, iter_dir = wired_project
    (root / "nodes" / "experiment" / "r1.md").write_text(
        '---\nid: "experiment:r1"\ntype: experiment\n---\n\nbody\n'
    )
    nf = root / "nodes" / "experiment" / "e1.md"
    nf.write_text('---\nid: "experiment:e1"\ntype: experiment\n'
                  "evidence_runs:\n  - experiment:r1\n---\n\nbody\n")
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1"})   # no evidence_runs key
    assert "verdict: proved" in nf.read_text()


def test_post_wire_creates_demoted_verdict_node_when_file_missing(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "hypothesis:ghost", "evidence_runs": 0})
    # goal:s17 -- `a1.md`, not `ghost.md`. The node's id has always been
    # `verdict:<agent-id>`, but the file used to be named after the PARENT's
    # slug, so path and id disagreed: `_node_file_path` could never find the
    # node again, and two agents wiring verdicts for one parent overwrote each
    # other. Routing through `node_writer` derives both from one slug.
    text = (root / "nodes" / "verdict" / "a1.md").read_text()
    assert "id: verdict:a1" in text
    assert "verdict: inconclusive_lean_proved:50" in text
    assert "demoted_from: proved" in text


def test_post_wire_rejects_sentinel_evidence_runs(wired_project):
    """H4c in the second writer path: a sentinel in the agent record's own
    evidence_runs must reject (not demote, not silently pass) — nothing
    about the target node changes."""
    root, iter_dir = wired_project
    before = (root / "nodes" / "experiment" / "e1.md").read_text()
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "proved",
                     "node_id": "experiment:e1", "evidence_runs": ["synthetic"]})
    after = (root / "nodes" / "experiment" / "e1.md").read_text()
    assert after == before
    assert "verdict" not in after


def test_post_wire_sentinel_does_not_reject_uncertain_verdicts(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done",
                     "verdict": "inconclusive_lean_proved:60",
                     "node_id": "experiment:e1", "evidence_runs": ["synthetic"]})
    fm = _fm_of(root / "nodes" / "experiment" / "e1.md")
    assert fm["verdict"] == "inconclusive_lean_proved:60"


# --- the kid's own record is what post_wire must read ----------------------


def test_post_wire_reads_the_verdict_the_kid_actually_wrote(wired_project):
    """The manifest is written once, at spawn. `cli.py done` writes the kid's
    results to `<agent>/agent.json`, and `heal.py` syncs only `status` across.
    So every pi kid's verdict/confidence/evidence_runs was dropped and the
    node kept the scaffold's `pending` -- invisible while every observed pi
    verdict happened to BE `pending`."""
    root, iter_dir = wired_project
    agent = {"id": "a1", "status": "done", "node_id": "experiment:e1"}
    (iter_dir / "manifest.json").write_text(json.dumps({"agents": [agent]}))
    sess = iter_dir / "a1"
    sess.mkdir(parents=True, exist_ok=True)
    (sess / "agent.json").write_text(json.dumps({
        "id": "a1", "status": "done", "node_id": "experiment:e1",
        "verdict": "inconclusive_lean_proved:65", "confidence": 0.65,
    }))
    import argparse
    post_wire.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))
    fm = _fm_of(root / "nodes" / "experiment" / "e1.md")
    assert fm["verdict"] == "inconclusive_lean_proved:65"
    assert fm["confidence"] == 0.65


def test_agent_json_wins_over_the_stale_manifest_copy(wired_project):
    root, iter_dir = wired_project
    (iter_dir / "manifest.json").write_text(json.dumps({"agents": [
        {"id": "a1", "status": "running", "node_id": "experiment:e1",
         "verdict": None}]}))
    sess = iter_dir / "a1"
    sess.mkdir(parents=True, exist_ok=True)
    (sess / "agent.json").write_text(json.dumps({
        "id": "a1", "status": "done", "node_id": "experiment:e1",
        "verdict": "pending", "confidence": 0.4}))
    import argparse
    post_wire.cmd_wire(argparse.Namespace(iter_n=1, project_root=None))
    assert _fm_of(root / "nodes" / "experiment" / "e1.md")["confidence"] == 0.4


def test_missing_agent_json_falls_back_to_the_manifest_entry(wired_project):
    root, iter_dir = wired_project
    _wire(iter_dir, {"id": "a1", "status": "done", "verdict": "pending",
                     "node_id": "experiment:e1", "evidence_runs": 0})
    assert _fm_of(root / "nodes" / "experiment" / "e1.md")["verdict"] == "pending"


# --- the lean percent is 0-100, as four documents have always said ---------


@pytest.mark.parametrize("n", ["0", "1", "50", "65", "99", "100"])
def test_lean_accepts_the_documented_range(n):
    assert eg.is_valid_verdict(f"inconclusive_lean_proved:{n}")
    assert eg.is_valid_verdict(f"inconclusive_lean_disproved:{n}")


@pytest.mark.parametrize("n", ["101", "150", "999", "1000"])
def test_lean_rejects_out_of_range(n):
    """`\\d{1,3}` accepted `:999` while VERDICT_HELP, zoom.py's contract,
    agent-prompt.md and task:t-054 all said 0-100. t-054's own Test Strategy
    reads 'reject inconclusive_lean_proved:101' -- the graph specified this and
    the regex never implemented it."""
    assert not eg.is_valid_verdict(f"inconclusive_lean_proved:{n}")
    assert not eg.is_valid_verdict(f"inconclusive_lean_disproved:{n}")


def test_no_live_node_carries_an_out_of_range_lean():
    """Guards the tightening itself: if a real node ever holds one, this fails
    loudly rather than that node silently becoming invalid."""
    import re as _re
    root = Path(__file__).resolve().parents[3] / ".agi" / "nodes"
    if not root.is_dir():
        pytest.skip("engine graph not present")
    bad = []
    for p in root.rglob("*.md"):
        head = p.read_text(encoding="utf-8", errors="replace").split("---", 2)
        if len(head) < 3:
            continue
        m = _re.search(r"^verdict:\s*[\"']?(\S+?)[\"']?\s*$", head[1], _re.M)
        if m and not eg.is_valid_verdict(m.group(1)):
            bad.append((p.name, m.group(1)))
    assert bad == [], f"nodes with invalid verdicts: {bad}"


# ------------------------------------------------- self-citation (goal:g7.3, 2)


def test_verdict_may_not_cite_itself():
    """`evidence_runs: [<my own id>]` is `evidence_runs: 3` one substitution on.

    It resolves against the corpus because the node exists, and bought a
    decisive verdict. Fired unprompted on 2026-09-01, on the first kid that
    reached for `proved`.
    """
    corpus = frozenset(["verdict:v1", "experiment:e1"])
    res = eg.apply_gate(
        "proved", ["verdict:v1"], corpus=corpus,
        self_id="verdict:v1", node_type="verdict")
    assert res.demoted and res.verdict == "inconclusive_lean_proved:50"


def test_verdict_citing_its_experiment_is_fine():
    corpus = frozenset(["verdict:v1", "experiment:e1"])
    res = eg.apply_gate(
        "proved", ["experiment:e1"], corpus=corpus,
        self_id="verdict:v1", node_type="verdict")
    assert not res.demoted and res.verdict == "proved"


def test_experiment_may_cite_itself_because_it_is_the_run():
    """The asymmetry is the point, not an exemption."""
    corpus = frozenset(["experiment:e1"])
    res = eg.apply_gate(
        "proved", ["experiment:e1"], corpus=corpus,
        self_id="experiment:e1", node_type="experiment")
    assert not res.demoted and res.verdict == "proved"


def test_self_id_absent_keeps_historical_behaviour():
    """Every existing caller and node behaves exactly as before."""
    corpus = frozenset(["verdict:v1"])
    res = eg.apply_gate("proved", ["verdict:v1"], corpus=corpus)
    assert not res.demoted and res.verdict == "proved"
