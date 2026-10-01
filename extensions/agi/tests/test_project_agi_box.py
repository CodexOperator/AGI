"""G6: the projected agi-post drop-in carries AGI_BOX=<row box>."""
import pathlib, re, shutil, subprocess
import pytest

WT = pathlib.Path(__file__).resolve().parents[3]
GEO = ".agi/nodes/.geometry"
ROW = ('  - {"name": "t1", "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"},'
       ' "role": "director", "tier": 1, "harness": "claude-code", "box": "%s"}\n')
SECT = "/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}"


def project(tmp_path, engine_text=None, box="local-town", path=None):
    if not shutil.which("jq"):
        pytest.skip("jq absent")
    repo, out = tmp_path / "repo", tmp_path / "out"
    (repo / GEO).mkdir(parents=True)
    for f in (WT / GEO).glob("engine*.md"):
        shutil.copy(f, repo / GEO / f.name)
    if path:  # G7.5: pin the projected unit's Environment=PATH inside the tmp copy
        u = repo / GEO / "engine-root.md"
        u.write_text(re.sub(r"(?m)^(Environment=PATH=)\S+", lambda m: m[1] + path, u.read_text()))
    if engine_text is not None:
        (repo / GEO / "engine.md").write_text(engine_text)
    (repo / GEO / "posts.md").write_text("---\nposts:\n" + ROW % box)
    g = lambda *a, **k: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True, **k)
    g("init", "-q"); g("add", "-A")
    g("-c", "user.name=t", "-c", "user.email=t.invalid", "commit", "-qm", "x")
    sect = subprocess.run(["sed", "-n", SECT, str(repo / GEO / "engine.md")], capture_output=True, text=True, check=True).stdout
    subprocess.run(["sh", "-s", str(out), "HEAD"], input=sect, cwd=repo, env={"PATH": "/usr/bin:/bin", "AGI_BOX": box},
                   check=True, capture_output=True, text=True)
    return (out / ("agi-post" + "@t1.service.d") / "h.conf").read_text()


@pytest.mark.parametrize("box", ["local-town", "other-town"])
def test_dropin_carries_agi_box(tmp_path, box):
    conf = project(tmp_path, box=box)
    assert f"AGI_BOX={box}" in conf and "AGI_ROLE=director" in conf and "AGI_LADDER_TIER=1" in conf


def test_old_bytes_lack_agi_box(tmp_path):
    old = subprocess.run(["git", "-C", str(WT), "show", f"6b536b730:{GEO}/engine.md"], capture_output=True, text=True)
    if old.returncode:
        pytest.skip("old tip not in this clone")
    assert "AGI_BOX" not in project(tmp_path, old.stdout)
