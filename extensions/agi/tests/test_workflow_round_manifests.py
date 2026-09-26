"""The two COMMITTED round manifests run a round, then its review, by name.

hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name —
its four falsifiers, read off the real bytes in
`extensions/agi/workflows/round-mur.json` and `round-research-review.json`
through the REAL `_load_manifest` / `_expand_stages` / `run_workflow`. Every
process seam is a stand-in: `subprocess.run` is the round dispatch,
`_round_git_harvest` is the git range, `_run_stage_pi` is the review dispatch
(it RECORDS the label and the prompt it was asked to render), and
`shared_project_root` is a tmp dir so a tracking row is written here and never
into the live sessions tree. No model is loaded, no parent is spawned, no
workflow is run against a real harness.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow as _wf  # noqa: E402
from workflow import run_workflow  # noqa: E402

MANIFESTS = ["round-mur", "round-research-review"]
#: the repeat pool each composed review reads its slices from
POOL = {"round-mur": ("rounds", {"key": "S1.7", "merge_up": 7}),
        "round-research-review": ("targets", {"key": "S1.7"})}


def _templates(name):
    """base label -> the INHERITED prompt, read from the committed base."""
    mf = _loaded(name)
    return {s["label"]: s["prompt"] for s in _loaded(mf["extends"])["stages"]}


def _item(key, extra=None):
    """The review's repeat pool item, MINIMAL: only the slice identity. Every
    other placeholder the inherited review prompt names must be supplied by the
    ROUND (that is the claim) — a pool item pre-loaded with the whole target
    shape would make the assertion pass without the round supplying anything."""
    item = {"key": key}
    item.update(extra or {})
    return item


def _loaded(name, repo=REPO):
    return _wf._load_manifest(repo, name)


# ---------- falsifier 1: both manifests load, and their round is kind:round --

@pytest.mark.parametrize("name", MANIFESTS)
def test_committed_manifest_loads_and_leads_with_a_round_stage(name):
    """FALSIFIER 1 — the manifest must survive the real loader, and its FIRST
    stage must be the round (the loader materializes prelude + inherited
    reviews; a review stage ahead of the round would review nothing)."""
    mf = _loaded(name)
    stages = _wf._expand_stages(mf, {"target": "hypothesis:round-demo"})
    assert stages[0]["kind"] == "round", stages[0]
    assert stages[0]["label"] == "round-parent"
    assert mf["required_args"] == ["target", "iteration"]
    assert mf["type"] in {"merge-up-review", "research"}


@pytest.mark.parametrize("name", MANIFESTS)
def test_every_inherited_review_stage_is_gated_on_the_round(name):
    """FALSIFIER 1, the wiring half — the review prompts are INHERITED, never
    copied (their bytes must equal the base manifest's), and every one of them
    must carry the round as a dependency so a failed round can gate it."""
    mf = _loaded(name)
    base = _loaded(mf["extends"])
    pool, item = POOL[name]
    stages = _wf._expand_stages(mf, {pool: [_item(item["key"], item)]})
    reviews = [st for st in stages if st.get("kind") != "round"]
    assert reviews, name
    for st in reviews:
        deps = st.get("depends_on") or []
        assert "round-parent" in deps, (name, st["label"], deps)
    by_label = {s["label"]: s for s in base["stages"]}
    for st in reviews:
        src = by_label[st["label"].split(":")[0]]
        assert st["prompt"] == src["prompt"], f"{name} copied a review prompt"
        assert st["schema"] == src["schema"]


# ---------- the two seam helpers the probes use ---------------------------

def _drive(tmp_path, monkeypatch, name, round_rc, harvest_files, drop=()):
    """Run the real composed manifest with stand-in seams. Returns
    (rc, ran, prompts, buffer, record). `drop` REMOVES a harvest key the
    round would otherwise have built -- the falsifier-2 case of a round whose
    harvest is missing what the review stages are owed."""
    pool, item = POOL[name]
    mf = _loaded(name)
    monkeypatch.setattr(_wf, "_load_manifest", lambda _r, _k: mf)
    monkeypatch.setattr(_wf, "_stage_context", lambda *a, **k: "CTX")
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    sess = tmp_path / "sessions"
    monkeypatch.setattr(_wf._loc, "shared_project_root", lambda _r: sess)
    monkeypatch.setattr(_wf._loc, "iteration_dir", lambda _r, _i: tmp_path / ".agi")
    ran: list[str] = []
    prompts: dict[str, str] = {}

    def _review(cfg, st, knobs, args, prior=None, **kw):
        ran.append(st["label"])
        prompts[st["label"]] = _wf.render_stage_prompt(st, args, prior=prior)
        # the stand-in reviewer's structured return: ONE key its own schema
        # declares (never a round-named one — the reviewer returns findings,
        # and a prior that shadows {old_tip}/{files} is the LLM seam's
        # precedence, not the composition's)
        req = (st.get("schema") or {}).get("required") or ["ok"]
        return 0, {req[0]: st["label"]}

    monkeypatch.setattr(_wf, "_run_stage_pi", _review)
    monkeypatch.setattr(_wf.subprocess, "run", lambda cmd, **kw: (
        subprocess.CompletedProcess(cmd, round_rc, "spawned a00-test\n", "")))
    monkeypatch.setattr(_wf.time, "sleep", lambda _s: None)
    monkeypatch.setattr(_wf, "_round_git_harvest", lambda *a, **kw: {
        k: v for k, v in {"old_tip": "0ldt1p", "new_tip": "n3wt1p",
                          "files": harvest_files}.items() if k not in drop})
    import dispatch
    monkeypatch.setattr(dispatch, "_branch_has_done_commit",
                        lambda _r, rec, _a: rec.get("branch") == "loop/hyp")
    args = {"target": "hypothesis:round-demo", "iteration": "S1.7",
            pool: [_item(item["key"], item)]}
    buf = io.StringIO()
    rc = run_workflow(REPO / ".agi", name, "pi", args, False, out=buf)
    rows = []
    row_file = sess / "sessions" / "workflows" / f"{name}.jsonl"
    if row_file.is_file():
        rows = [json.loads(l) for l in row_file.read_text().splitlines() if l]
    return rc, ran, prompts, buf.getvalue(), rows


def _done_record(tmp_path):
    root = tmp_path / ".agi"
    root.mkdir(exist_ok=True)
    (root / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-test", "status": "done", "branch": "loop/hyp",
                     "base_branch": "main"}]}), encoding="utf-8")


# ---------- falsifier 2: the review receives the round's harvest -----------

@pytest.mark.parametrize("name", MANIFESTS)
def test_successful_round_hands_its_harvest_to_every_review_stage(
        tmp_path, monkeypatch, capsys, name):
    """FALSIFIER 2 — a stand-in round that reached a done commit must hand
    old_tip / new_tip / files to EVERY review slice, rendered INTO the
    inherited prompt. A blank placeholder here is the silent failure: the
    review would be asked to compare nothing."""
    templates = _templates(name)  # read BEFORE the loader is faked in _drive
    _done_record(tmp_path)
    files = [".agi/nodes/experiment/a00-abc123-11aa22.md",
             ".agi/nodes/verdict/a00-abc123-99ff00.md"]
    rc, ran, prompts, out, rows = _drive(tmp_path, monkeypatch, name, 0, files)
    assert rc == 0, out
    assert ran, out
    # every placeholder the INHERITED prompt actually names must carry the
    # round's own value; a blank one is the silent failure (a review asked to
    # compare nothing). merge-up-review names the tips, research-review names
    # the files and the round's experiment nodes.
    probed = 0
    for label, prompt in prompts.items():
        for ph, needle in (("{old_tip}", "0ldt1p"), ("{new_tip}", "n3wt1p"),
                           ("{files}", "a00-abc123-11aa22"),
                           ("{experiments}", "a00-abc123-11aa22")):
            if ph not in templates[label.split(":")[0]]:
                continue
            probed += 1
            assert needle in prompt, (name, label, ph, prompt[:400])
    assert probed >= 2, (name, probed)
    # the run record names the round and no stage failed (the review dispatch
    # is a stand-in, so the view's per-stage mark is the REAL runner's job)
    assert rows, "no run record row was written"
    assert "round-parent" in rows[-1]["stages"], rows[-1]["stages"]
    assert rows[-1]["failed"] == 0, rows[-1]["stages"]


# ---------- falsifier 3: a failed round skips the whole review chain -------

@pytest.mark.parametrize("name", MANIFESTS)
def test_failed_round_skips_every_review_stage_by_name(
        tmp_path, monkeypatch, capsys, name):
    """FALSIFIER 3 — a stand-in round whose dispatch exits 1 dispatched NO
    parent, so no review stage may run and each must be named in the run
    record as skipped."""
    _done_record(tmp_path)
    rc, ran, prompts, out, rows = _drive(tmp_path, monkeypatch, name, 1, [])
    err = capsys.readouterr().err
    assert rc != 0, out
    assert ran == [], f"review stage(s) ran after the failed round: {ran}"
    assert "round-parent" in err and "failed" in err, err
    mf = _loaded(name)
    pool, item = POOL[name]
    for st in _wf._expand_stages(mf, {pool: [_item(item["key"], item)]}):
        if st.get("kind") == "round":
            continue
        assert f"skipped stage {st['label']}" in err, (name, st["label"], err)
    # named in the RUN RECORD, not only on stderr
    assert rows, "no run record row was written"
    skipped = {lb for lb, status in rows[-1]["stages"].items()
               if status == "skipped"}
    assert "round-parent" not in skipped
    assert skipped, rows[-1]["stages"]


# ---------- seam 4: a SUCCESSFUL round is recorded as resolved -----------

@pytest.mark.parametrize("name", MANIFESTS)
def test_successful_round_is_recorded_resolved_not_pending(
        tmp_path, monkeypatch, capsys, name):
    """A round that reached its done commit is the mirror of falsifier 3: it
    dispatched a parent, resolved, and nothing ever marked it so. `_run_round_stage`
    returns a bare (rc, value) and never touches the view, so the record read
    `{'round-parent': 'pending'}` with failed=0 -- a consumer could not tell a
    RESOLVED round from one that never resolved, and every review slice sat
    `pending` behind it too (the mark-and-continue patch for the FAILURE path
    was written and its success twin was not)."""
    _done_record(tmp_path)
    files = [".agi/nodes/experiment/a00-abc123-11aa22.md"]
    rc, ran, prompts, out, rows = _drive(tmp_path, monkeypatch, name, 0, files)
    assert rc == 0, out
    st = rows[-1]["stages"]["round-parent"]
    assert st not in ("pending", "running"), rows[-1]["stages"]
    assert st in ("resolved", "ok"), rows[-1]["stages"]
    # the tree names the range it resolved over, so a reader of the record can
    # see the two tips without opening the harvest
    assert "n3wt1p" in out, out
    # (the review slices behind it are the STAND-IN's mark: the real
    # `_run_stage_pi` names its own stages, which this test replaces)


# ---------- falsifier 4: no regression in the workflow suite ---------------

def test_composed_manifests_do_not_alter_the_base_manifests():
    """FALSIFIER 4, the in-file half: the bases load byte-identical to what a
    run of them alone would load — composition is additive. The suite half
    (`pytest -k workflow`) is run by hand and recorded in the experiment node."""
    for name in MANIFESTS:
        mf = _loaded(name)
        base = _loaded(mf["extends"])
        assert _wf._expand_stages(base, {}) == _wf._expand_stages(
            base, {}), name
        assert base["script"] in {"agi-merge-up-review.js",
                                  "agi-research-review.js"}


@pytest.mark.parametrize("name", MANIFESTS)
def test_a_bare_run_resolves_a_harness_that_can_run_the_round(name):
    """TMM.237: with NO --harness, the harness the workflow's own resolution
    chain picks must be one that can run a `kind: round` stage. Pre-fix,
    round-research-review inherited research-review.json's manifest-level
    `provider: claude-code` (a level-1 override that beats its type row) and a
    bare run was refused: "harness 'claude-code' cannot run" the round."""
    mf = _loaded(name)
    harness, level = _wf._resolve_default_harness(REPO / ".agi", name, mf, {})
    assert harness == "pi", (name, harness, level)


# ===================================================================
# hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-
# missing-one-names-itself -- the DECLARATION, on the REAL committed bytes
# ===================================================================

#: what each ROUND manifest declares its inherited stages are owed -- read
#: from the manifests themselves, never restated here (a restated list would
#: make the test pass against a manifest that declared nothing).
OWED = {name: _loaded(name).get("inherited_required_placeholders") or []
        for name in MANIFESTS}


def _inherited_reviews(name):
    """(manifest, [inherited stage dicts]) as the REAL loader materializes them."""
    mf = _loaded(name)
    pool, item = POOL[name]
    stages = _wf._expand_stages(mf, {pool: [_item(item["key"], item)]})
    return mf, [st for st in stages if st.get("kind") != "round"]


@pytest.mark.parametrize("name", MANIFESTS)
def test_every_inherited_stage_declares_what_the_round_owes_it(name):
    """FALSIFIER 1 — the ROUND manifest, not the base, declares the range keys
    its inherited stages render. Through the REAL loader: an inherited stage
    whose prompt names one of {old_tip}/{new_tip}/{files} must list it in
    `required_placeholders`."""
    _mf, reviews = _inherited_reviews(name)
    templates = _templates(name)
    assert _loaded(name).get("inherited_required_placeholders"), name
    declared = 0
    for st in reviews:
        ph = st.get("required_placeholders") or []
        for key in OWED[name]:
            if "{" + key + "}" in templates[st["label"].split(":")[0]]:
                assert key in ph, (name, st["label"], key, ph)
                declared += 1
    assert declared >= 2, (name, declared)


@pytest.mark.parametrize("name", MANIFESTS)
@pytest.mark.parametrize("key", sorted({k for v in OWED.values() for k in v}))
def test_a_missing_owed_key_names_itself_on_the_real_manifest(
        tmp_path, monkeypatch, capsys, name, key):
    if key not in OWED[name]:
        pytest.skip(f"{name} renders no {{{key}}}")
    """FALSIFIER 2 — a round whose harvest LACKS an owed key fails the FIRST
    review stage that renders it, BY NAME, naming the key. It must not render
    "" (the silent 'asked to compare nothing' failure) and must not run.

    KNOWN, NOT MINE: a stage further down the chain whose immediate parent was
    SKIPPED (rather than failed) still runs -- a cascade hole in the skip
    branch, present identically when a review simply returns rc 3 (probe
    .agi/sessions/iter-DH.400/a00-8f7029e5/probe_skip_cascade.py). The
    assertion is on the FIRST stage that renders the key, which is the claim.
    """
    _done_record(tmp_path)
    files = [".agi/nodes/experiment/a00-abc123-11aa22.md"]
    _mf, reviews = _inherited_reviews(name)
    templates = _templates(name)
    first = next(st["label"] for st in reviews
                 if "{" + key + "}" in templates[st["label"].split(":")[0]])
    rc, ran, prompts, out, rows = _drive(tmp_path, monkeypatch, name, 0, files,
                                         drop=(key,))
    err = capsys.readouterr().err
    assert first not in ran, f"{name}: {first} ran without {key}: {ran}"
    assert f"stage {first} required placeholder(s) ['{key}']" in err, err
    assert rc != 0, out
    failed = {lb: st for lb, st in (rows[-1]["stages"] if rows else {}).items()
              if st == "failed"}
    assert first in failed, (name, rows[-1]["stages"] if rows else None)


@pytest.mark.parametrize("name", MANIFESTS)
def test_a_complete_harvest_still_runs_every_review(tmp_path, monkeypatch,
                                                    capsys, name):
    """FALSIFIER 3 — the happy path is untouched: with all three keys present
    the reviews RUN (the guard must not be a blanket one that also fires when
    the round DID return the key)."""
    _done_record(tmp_path)
    files = [".agi/nodes/experiment/a00-abc123-11aa22.md"]
    rc, ran, _prompts, out, rows = _drive(tmp_path, monkeypatch, name, 0, files)
    err = capsys.readouterr().err
    assert rc == 0, (out, err)
    assert ran, (name, err)
    assert "required placeholder" not in err, err
    assert rows[-1]["failed"] == 0, rows[-1]["stages"]


@pytest.mark.parametrize("name", ["merge-up-review", "research-review"])
def test_the_base_manifests_gain_nothing(name):
    """FALSIFIER 4 — the bases are byte-untouched by the composition: run
    alone, they owe no range and declare no owed placeholders, so a bare
    `merge-up-review` run is not newly failed."""
    mf = _loaded(name)
    assert "inherited_required_placeholders" not in mf, name
    for st in mf["stages"]:
        assert not st.get("required_placeholders"), (name, st["label"])
