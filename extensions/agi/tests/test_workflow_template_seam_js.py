"""The .js half of the workflow pairs carries the SAME `{project_root}` seam.

goal:g7.33.14.1 -- the sibling `test_workflow_template_seam_json.py` locks the
7 `*.json` stage manifests. This locks the OTHER half: the hand-maintained
`extensions/agi/workflows/agi-*.js` Claude Code Workflow scripts, which still
named the `/home/ubuntu/work/agi` checkout literal in 14 lines across 9 files
(so a run started in a git worktree pointed its readers at the main checkout).

Precedent for the seam on this side already exists: `agi-research-review.js:18`
`const ROOT = (args && args.project_root) || "."`. Every remaining script now
declares the same one-line ROOT, and every former literal is either
`${ROOT}` (inside a backtick template) or `" + ROOT + "` (inside a
double-quoted string -- these templates carry literal backticks and escaped
quotes, so converting them to template literals is not safe).

The scripts are Workflow DSL, not plain modules (top-level `return`), so the
syntax check strips `export ` and wraps the body in an async function before
`node --check`.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WF = REPO / "extensions" / "agi" / "workflows"

STALE = "/home/ubuntu/work/agi"
SEAM = "const ROOT = (args && args.project_root) ||"
MIGRATED = [
    "agi-brief-drafting",
    "agi-desktop-check",
    "agi-g15-close-triage",
    "agi-l4-plan-research",
    "agi-merge-up-review",
    "agi-prime-open-questions",
    "agi-recovery-survey",
    "agi-round-review",
    "agi-trove-survey",
]


def test_no_workflow_js_carries_the_stale_checkout_literal():
    hits = [p.name for p in sorted(WF.glob("*.js")) if STALE in p.read_text(encoding="utf-8")]
    assert hits == [], hits


def test_every_migrated_script_declares_the_root_seam():
    for name in MIGRATED:
        text = (WF / f"{name}.js").read_text(encoding="utf-8")
        assert SEAM in text, name


def test_no_absolute_slash_is_left_in_front_of_root():
    """The migration replaced the PATH but not the `/` that made it
    absolute. `Repo: /${ROOT}` renders `Repo: /.` when project_root is
    absent -- i.e. the FILESYSTEM ROOT -- and `Repo: //data/work/agi`
    when it is present. A grep for the stale literal cannot see either.
    """
    hits = [(p.name, i) for p in sorted(WF.glob("*.js"))
            for i, l in enumerate(p.read_text(encoding="utf-8").split("\n"), 1)
            if "/${ROOT}" in l or '/" + ROOT' in l]
    assert hits == [], hits


def test_rendered_templates_carry_root_without_a_leading_slash():
    """TMM.199 red 2: the grep above once saw only the template form and missed
    8 lines of `/" + ROOT + "`. Grep proves presence, only a RENDER proves shape:
    evaluate every one-line `const ... = "..."`/backtick string that uses ROOT,
    with and without an injected project_root, and read the rendered text."""
    node = shutil.which("node")
    if not node:  # pragma: no cover - box without node
        return
    root = "/tmp/fake-worktree"
    for name in MIGRATED:
        lines = (WF / f"{name}.js").read_text(encoding="utf-8").split("\n")
        consts, i = [], 0
        while i < len(lines):  # a backtick template may span lines: take it whole
            l = lines[i]
            if re.match(r"const \w+ = `", l) and len(re.findall(r"(?<!\\)`", l)) % 2:
                j = i + 1
                while len(re.findall(r"(?<!\\)`", lines[j])) % 2 == 0:
                    j += 1
                l = "\n".join(lines[i:j + 1])
                i = j
            if re.match(r"const \w+ = [\"`]", l) and re.search(r"\$\{ROOT\}|ROOT \+", l):
                consts.append(l)
            i += 1
        if not consts:  # ROOT only inside object literals: the grep above covers it
            continue
        for injected in (root, None):
            js = (f"const args = {{project_root: {injected!r}}};\n" if injected
                  else "const args = {};\n")
            js += next(l for l in lines if l.startswith(SEAM)) + "\n"
            js += "const out = [];\n"
            names = {v for l in consts
                     for v in re.findall(r"\$\{([A-Za-z_]\w*)\}|\" \+ ([A-Za-z_]\w*) \+ \"", l)
                     for v in v if v}
            defined = {l.split()[1] for l in consts} | {"ROOT", "args"}
            for v in sorted(names - defined):  # other seams render as a visible stub
                js += f"var {v} = '<{v}>';\n"
            for l in consts:
                var = l.split()[1]
                js += l + f"\nout.push({var});\n"
            js += "process.stdout.write(out.join('\\n'));\n"
            proc = subprocess.run([node, "-e", js], text=True, capture_output=True)
            assert proc.returncode == 0, (name, proc.stderr[:400])
            if injected:
                assert root in proc.stdout, name
                assert "/" + root not in proc.stdout, (name, "//" + root)
            else:  # the fallback '.' behind a '/' is the FILESYSTEM root
                m = re.search(r"(?:^|[\s`(])/\.(?=[\s,/)`]|$)", proc.stdout, re.M)
                assert m is None, (name, proc.stdout[max(0, m.start() - 40):m.end() + 40])


def test_root_is_declared_before_it_is_used():
    """A `ROOT` used in a template before its `const` would be a TDZ
    ReferenceError at run time -- invisible to grep, fatal to the run."""
    for name in MIGRATED:
        lines = (WF / f"{name}.js").read_text(encoding="utf-8").split("\n")
        decl = next(i for i, l in enumerate(lines) if l.startswith(SEAM))
        first_use = next(i for i, l in enumerate(lines)
                         if re.search(r"\$\{ROOT\}|ROOT \+", l) and not l.startswith(SEAM))
        assert decl < first_use, (name, decl, first_use)


def test_migrated_scripts_still_parse():
    """Strip the `export` and wrap the body: the Workflow DSL allows a
    top-level `return`, plain `node --check` refuses every script (measured
    pre-change, so a refusal here means MY edit broke a string)."""
    node = shutil.which("node")
    if not node:  # pragma: no cover - box without node
        return
    for name in MIGRATED:
        body = (WF / f"{name}.js").read_text(encoding="utf-8")
        body = re.sub(r"^export (const|function|let|default)", r"\1", body, flags=re.M)
        wrapped = f"async function __wf(){{\n{body}\n}}\n"
        proc = subprocess.run([node, "--input-type=module", "--check"],
                              input=wrapped, text=True, capture_output=True)
        assert proc.returncode == 0, (name, proc.stderr[:400])


def test_migrated_scripts_render_the_injected_root():
    """The seam is only worth anything if the rendered prompt carries the
    INJECTED value -- spot-check the two shapes, template and concat."""
    root = "/tmp/fake-worktree"
    out = (WF / "agi-round-review.js").read_text(encoding="utf-8")
    assert f"${{ROOT}}" in out
    out2 = (WF / "agi-desktop-check.js").read_text(encoding="utf-8")
    assert '" + ROOT + "' in out2
    for name in MIGRATED:
        text = (WF / f"{name}.js").read_text(encoding="utf-8")
        assert root not in text, name
