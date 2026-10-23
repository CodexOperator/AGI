"""goal:g7.16.1.11.46.11 (V10a, doc:brainstorm-unify §35): the retired identity
variable is named NOWHERE outside the history paths, so a regression is a red
within one lap, never a ruling made twice (hypothesis:l4-a-seat-is-a-post-
everywhere ruled it once and the word came back).

STRICT (council 3/3, alive 21:05Z 10-23): the scan covers every tracked AND
untracked file of the repo except four EXPLICIT history paths (council 21:3xZ:
never a generic "any deprecated segment"): `.agi/nodes/deprecated/`,
`extensions/agi/guard/deprecated/` (the three retired guard drop-ins),
`.agi/sessions/rotations/` and `datasets/`. There is NO pattern exemption: a quoted (`>`) line is a hit like
any other. The ONE escape is ALLOW below, a committed allowlist keyed by path +
sha256 of the exact line, for an owner-verbatim line only; it is empty today
(0 such lines on the trunk) and a stale entry is itself red.

The variable's name is built by concatenation, so this file never names it.
The scan never skips: a ROOT that is not a git tree (a git-archive copy) fails
loud, so the guard cannot pass on a skip (council F1, alive 22:2xZ 10-23).
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
NAME = "AGI_" + "SEAT"
EXCLUDE = (":(exclude).agi/nodes/deprecated",
           ":(exclude)extensions/agi/guard/deprecated",
           ":(exclude).agi/sessions/rotations",
           ":(exclude)datasets")

#: path -> {sha256(exact line text)}: owner-verbatim lines only, each with the
#: owner's date in a comment. Empty: the trunk carries none (council reading).
ALLOW: dict[str, set[str]] = {}


def _digest(line: str) -> str:
    return hashlib.sha256(line.encode()).hexdigest()


def _hits(root: Path, allow: dict[str, set[str]]) -> list[str]:
    """Every `path:line:text` naming the variable outside the history paths
    and not allowlisted by exact line hash."""
    r = subprocess.run(
        ["git", "-C", str(root), "grep", "--untracked", "-n", "-I", "-F", "-e", NAME,
         "--", ".", *EXCLUDE],
        capture_output=True, text=True)
    assert r.returncode in (0, 1), r.stderr
    out = []
    for row in r.stdout.splitlines():
        path, _, rest = row.partition(":")
        _, _, text = rest.partition(":")
        if _digest(text) in allow.get(path, set()):
            continue
        out.append(row)
    return out


def _git_tree(tmp_path: Path, files: dict[str, str]) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for rel, body in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    return root


def test_the_repo_names_the_retired_variable_nowhere():
    hits = _hits(ROOT, ALLOW)
    assert hits == [], f"{len(hits)} hit(s), first: {hits[:5]}"


def test_every_allowlist_entry_still_matches_a_live_line():
    for path, digests in ALLOW.items():
        lines = (ROOT / path).read_text().splitlines()
        live = {_digest(ln) for ln in lines if NAME in ln}
        assert digests <= live, f"stale ALLOW entry for {path}"


def test_mutant_a_planted_untracked_scratch_file_under_extensions_is_red(tmp_path):
    root = _git_tree(tmp_path, {"extensions/agi/scratch.sh": f"{NAME}=x\n"})
    assert _hits(root, {}) == [f"extensions/agi/scratch.sh:1:{NAME}=x"]


def test_mutant_a_quoted_line_is_not_spared(tmp_path):
    root = _git_tree(tmp_path, {".agi/nodes/doc/x.md": f"> owner: {NAME} again\n"})
    assert len(_hits(root, {})) == 1


def test_the_allowlist_spares_only_the_exact_line(tmp_path):
    line = f"> owner 10-23: {NAME} verbatim"
    root = _git_tree(tmp_path, {".agi/nodes/doc/x.md": line + "\n" + line + "!\n"})
    allow = {".agi/nodes/doc/x.md": {_digest(line)}}
    assert _hits(root, allow) == [f".agi/nodes/doc/x.md:2:{line}!"]


def test_mutant_a_deprecated_dir_elsewhere_is_scanned(tmp_path):
    """Only the four named paths are history: a `deprecated/` under bin/ is not."""
    root = _git_tree(tmp_path, {"extensions/agi/bin/deprecated/x": f"{NAME}=x\n"})
    assert _hits(root, {}) == [f"extensions/agi/bin/deprecated/x:1:{NAME}=x"]


def test_the_history_paths_are_not_scanned(tmp_path):
    root = _git_tree(tmp_path, {
        ".agi/nodes/deprecated/doc/old.md": f"{NAME}\n",
        "extensions/agi/guard/deprecated/post-env/52.conf": f"{NAME}\n",
        ".agi/sessions/rotations/r.seating.json": f"{NAME}\n",
        "datasets/kid-sft/a.jsonl": f"{NAME}\n",
    })
    assert _hits(root, {}) == []
