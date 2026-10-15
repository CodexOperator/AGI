"""goal:g7.16.1.11.41 target 1 -- the unit's piece extraction reads the LANDED trunk, never the post's own worktree.

The REAL ExecStartPre line of agi-post@.service (the one that extracts the fenced `### piece` blocks into ~/bin; the
bytes in engine-root.md, %i -> the post, %t -> a scratch run dir) runs in a scratch HOME against a scratch MAIN repo:
the trunk branch carries a piece the post's own branch (a stale t) lacks, and a CHANGED version of one it has. Falsifier
1: after the line, ~/bin carries the TRUNK's bytes. Falsifier 3: AGI_TRUNK as a 40-hex sha, a 10-hex sha or a tag is
refused by name before anything is written. The glob is the unit's AGI_PIECE_GLOB cell (a new engine-p2.md joins
without an edit; engine-grow.md and engine-root.md do not). MUTANTS: extract from t again / a 10-hex sha accepted / a
hand-listed glob each go RED on their own row.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
GEO = ".agi/nodes/.geometry"
ROOT_MD = ROOT / GEO / "engine-root.md"


def unit_lines() -> tuple[str, str]:
    """(glob cell value, the extraction ExecStartPre body) from the shipped agi-post@.service block."""
    glob, body = None, None
    for ln in ROOT_MD.read_text().splitlines():
        if ln.startswith('Environment="AGI_PIECE_GLOB='):
            glob = ln[len('Environment="AGI_PIECE_GLOB='):-1]
        if ln.startswith("ExecStartPre=sh -c '") and "ls-tree" in ln:
            body = ln[len("ExecStartPre=sh -c '"):-1]
    assert glob and body, "the unit's glob cell or extraction line is not in engine-root.md"
    return glob, body


def piece(name: str, text: str) -> str:
    return f"### {name} (1 B)\n~~~sh\n{text}\n~~~\n\n"


HEAD = "---\nid: config:x\n---\n# x\n\n"


class Post:
    def __init__(self, tmp: Path, body: str, glob: str):
        self.home, self.run, self.main = tmp / "h", tmp / "run", tmp / "main"
        self.body, self.glob = body.replace("%i", "p").replace("%t", str(self.run)), glob
        (self.run / "agi-p").mkdir(parents=True)
        self.home.mkdir()
        g = self.main / GEO
        g.mkdir(parents=True)
        self.env = {"PATH": "/usr/bin:/bin", "HOME": str(self.home), "GIT_CONFIG_GLOBAL": "/dev/null",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        # the OLD state, which the post's own branch (and so its t) keeps
        (g / "engine.md").write_text(HEAD + piece("zyg", "echo zyg-old") + piece("agi-run", "echo run"))
        (g / "engine-post.md").write_text(HEAD + piece("oldpiece", "echo OLD") + piece("gitconfig", "[x]") +
                                          piece("settings.json", "{}"))
        (g / "engine-grow.md").write_text(HEAD + piece("growonly", "echo grow"))
        self.git(self.main, "init", "-q", "-b", "trunk")
        self.git(self.main, "add", "-A")
        self.git(self.main, "commit", "-qm", "old")
        self.git(self.main, "branch", "posts/p")
        self.git(self.main, "worktree", "add", "-q", str(self.home / "t"), "posts/p")
        # the LANDED trunk moves on: a changed piece, a new piece, a new engine-p2.md in the glob
        (g / "engine-post.md").write_text(HEAD + piece("oldpiece", "echo NEW") + piece("gitconfig", "[x]") +
                                          piece("settings.json", "{}") + piece("newpiece", "echo landed"))
        (g / "engine-p2.md").write_text(HEAD + piece("p2piece", "echo p2"))
        (g / "engine-root.md").write_text(HEAD + piece("rootonly", "echo root"))
        self.git(self.main, "add", "-A")
        self.git(self.main, "commit", "-qm", "landed")
        self.git(self.main, "tag", "v1", "trunk")

    def git(self, repo, *a):
        return subprocess.run(["git", "-C", str(repo), *a], env=self.env, capture_output=True, text=True,
                              check=True).stdout.strip()

    def go(self, trunk="trunk", glob="__default__", fail=None, shims=None, ro_new=False):
        """Run the line. `fail` = a substring: a git shim exits 128 on any git call whose argv holds it (a failing ls-tree / show).
        `shims` = {tool: substring}: that tool, found first on PATH, exits 1 on any call whose argv holds the substring (mv, sed).
        `ro_new`: a mkdir shim makes `mkdir bin.new` leave the dir READ-ONLY, so every piece write into it fails."""
        env = {**self.env, "O": str(self.main), "AGI_TRUNK": trunk}
        g = self.glob if glob == "__default__" else glob
        if g is not None:
            env["AGI_PIECE_GLOB"] = g
        want = dict(shims or {})
        if fail:
            want["git"] = fail
        if want or ro_new:
            shim = self.home.parent / "shim"
            shim.mkdir(exist_ok=True)

            def real(tool):
                return subprocess.run(["which", tool], env=self.env, capture_output=True, text=True).stdout.strip()
            for tool, sub in want.items():
                code = 128 if tool == "git" else 1
                (shim / tool).write_text(f'#!/bin/sh\ncase "$*" in *"{sub}"*) echo "shim: {tool} failed" >&2; exit {code};; esac\nexec {real(tool)} "$@"\n')
                (shim / tool).chmod(0o755)
            if ro_new:
                (shim / "mkdir").write_text(f'#!/bin/sh\n{real("mkdir")} "$@"||exit $?\ncase "$*" in "bin.new") chmod 555 bin.new;; esac\n')
                (shim / "mkdir").chmod(0o755)
            env["PATH"] = f"{shim}:{env['PATH']}"
        return subprocess.run(["sh", "-c", self.body], env=env, cwd=str(self.home), capture_output=True, text=True)

    def seed(self, **files):
        """What the LAST start left in ~/bin (a retired piece, a stale copy): written before the line runs."""
        (self.home / "bin").mkdir(exist_ok=True)
        for n, t in files.items():
            (self.home / "bin" / n.replace("_", "-")).write_text(t)

    def snap(self):
        """Every entry of ~/bin with its bytes: 'byte-equal' is a dict compare."""
        b = self.home / "bin"
        return {f.name: f.read_bytes() for f in sorted(b.iterdir())} if b.is_dir() else None

    def bin(self, name):
        p = self.home / "bin" / name
        return p.read_text() if p.exists() else None


def rows(body: str, glob: str, mk) -> list[str]:
    bad = []

    def chk(name, cond):
        if not cond:
            bad.append(name)

    p = Post(mk("ok"), body, glob)
    r = p.go()
    chk("a-the line succeeds on a branch trunk", r.returncode == 0)
    chk("a-the trunk's CHANGED piece is what lands in ~/bin (the stale t has the old one)", p.bin("oldpiece") == "echo NEW\n")
    chk("a-a piece only the trunk has lands in ~/bin", p.bin("newpiece") == "echo landed\n")
    chk("g-a new engine-p2.md joins the glob without an edit", p.bin("p2piece") == "echo p2\n")
    chk("g-engine-grow.md and engine-root.md are not in the glob", p.bin("growonly") is None and p.bin("rootonly") is None)
    chk("a-the post's own branch is never read: its old piece is gone", "OLD" not in (p.bin("oldpiece") or ""))
    head = p.git(p.main, "rev-parse", "trunk")
    for name, trunk in (("a 40-hex sha", head), ("a 10-hex sha", head[:10]), ("a tag", "v1")):
        p = Post(mk("bad" + name.split()[1]), body, glob)
        r = p.go(trunk=trunk)
        chk(f"r-{name} as AGI_TRUNK is refused by name", r.returncode == 255 and "[bad-trunk]" in r.stderr)
        chk(f"r-{name}: nothing was extracted", p.bin("oldpiece") is None and p.bin("newpiece") is None)
    p = Post(mk("noglob"), body, glob)
    r = p.go(glob=None)
    chk("r-an unset glob cell is refused by name", r.returncode == 255 and "[no-glob]" in r.stderr and p.bin("newpiece") is None)
    # cut 3 (council 11:25Z 10-14): ~/bin is EXACTLY the trunk's piece set after the line
    p = Post(mk("exact"), body, glob)
    p.seed(agi_link="retired 10-08", oldpiece="stale copy", agi_run="stale run")
    (p.home / "bin" / ".dot").write_text("hidden")
    r = p.go()
    chk("s-the line succeeds over a bin with leavings", r.returncode == 0)
    chk("s-a piece absent from the trunk is absent from ~/bin after the line (agi-link, a dotfile)", p.bin("agi-link") is None and p.bin(".dot") is None)
    chk("s-a piece the trunk has is the trunk's bytes, not the stale copy", p.bin("oldpiece") == "echo NEW\n" and p.bin("agi-run") == "echo run\n")
    chk("s-~/bin is exactly the trunk's piece set (gitconfig and settings.json move out)", sorted(p.snap()) == ["agi-run", "newpiece", "oldpiece", "p2piece", "zyg"])
    gc, st = p.home / ".gitconfig", p.home / ".claude" / "settings.json"
    chk("s-gitconfig and settings.json land outside bin", gc.exists() and st.exists() and gc.read_text() == "[x]\n" and st.read_text() == "{}\n")
    chk("s-no scratch dir is left", not (p.home / "bin.new").exists() and not (p.home / "bin.old").exists())
    # fail closed and loud: the old bin/ byte-equal, no swap
    for i, (what, kw) in enumerate((("a trunk with no agi-run", {"glob": "engine-p2.md"}),
                     ("a git show that fails", {"fail": "show trunk:.agi/nodes/.geometry/engine-post.md"}),
                     ("a git ls-tree that fails", {"fail": "ls-tree"}),
                     # council fix-forward (10-14 14:10Z): the swap's second mv fails -> the restore puts bin back; a piece write fails -> named
                     ("an mv bin.new bin that fails", {"shims": {"mv": "bin.new bin"}}),
                     ("a piece write that fails (one piece)", {"shims": {"sed": "### newpiece "}}),
                     ("a bin.new that is not writable", {"ro_new": True}))):
        if kw.get("ro_new") and os.geteuid() == 0:
            continue                      # root writes into a 555 dir: the row cannot mean anything
        p = Post(mk(f"fc{i}"), body, glob)        # never a name the shim's pattern can match
        p.seed(agi_link="retired 10-08", oldpiece="stale copy", agi_run="stale run")
        before = p.snap()
        r = p.go(**kw)
        chk(f"f-{what}: exit 255 and '[extract-failed]' by name", r.returncode == 255 and "[extract-failed]" in r.stderr)
        chk(f"f-{what}: the old ~/bin is byte-equal (no swap)", p.snap() == before)
        chk(f"f-{what}: no scratch dir is left", not (p.home / "bin.new").exists())
        if "show" in what:
            chk("f-a failed show names the FILE", "engine-post.md" in r.stderr)
        if "ls-tree" in what:
            chk("f-a failed ls-tree is named", "ls-tree" in r.stderr)
        if "mv bin.new" in what:
            chk("f-a failed swap is named", "[extract-failed] swap" in r.stderr)
            chk("f-a failed swap: bin is a directory again (the restore ran) and no bin.old is left", (p.home / "bin").is_dir() and not (p.home / "bin.old").exists())
        if "one piece" in what:
            chk("f-a failed piece write names the FILE and the piece", "engine-post.md newpiece" in r.stderr and "agi-run is not" not in r.stderr)
        if "not writable" in what:
            chk("f-a bin.new that is not writable names a piece write, not the agi-run check", "[extract-failed] .agi" in r.stderr and "agi-run is not" not in r.stderr)
    return bad


def test_the_shipped_line_passes_every_row(tmp_path_factory):
    glob, body = unit_lines()
    assert rows(body, glob, lambda n: tmp_path_factory.mktemp(n)) == []


def mutant(old: str, new: str):
    glob, body = unit_lines()
    assert old in body, f"the mutant no longer applies: {old!r}"
    return body.replace(old, new, 1), glob


MUTANTS = {
    # extract from the post's own worktree again
    "extracts-from-t": lambda: mutant("$G show $AGI_TRUNK:$f>.e", "cat t/$f>.e"),
    # a 10-hex sha (and a tag, a 40-hex sha) accepted: the branch check dropped
    "any-ref-accepted": lambda: mutant('case $($G rev-parse --symbolic-full-name $AGI_TRUNK 2>/dev/null) in refs/heads/*|refs/remotes/*);;*)echo "[bad-trunk] $AGI_TRUNK is not a branch">&2;exit 255;;esac;', ""),
    # cut 3: no clear -- the extraction adds over bin/ again (retired pieces survive)
    "no-clear": lambda: mutant("mv bin bin.old&&mv bin.new bin||", "cp -a bin.new/. bin/||"),
    # swap anyway: no agi-run check / a failed show or ls-tree carried on
    "no-agi-run-check": lambda: mutant('[ -s bin.new/agi-run ]||x agi-run is not in the extracted set;', ""),
    "show-failure-ignored": lambda: mutant('>.e||x $f;', '>.e;'),
    "ls-tree-failure-ignored": lambda: mutant('||x ls-tree $AGI_TRUNK;', ';'),
    # fix-forward: the restore dropped (a failed second mv leaves NO bin/) / the piece write's failure ignored
    "restore-dropped": lambda: mutant("[ -d bin ]||mv bin.old bin;", ""),
    "sed-write-failure-ignored": lambda: mutant(">bin.new/$x||x $f $x;", ">bin.new/$x;"),
    # a hand-listed glob instead of the unit's cell
    "a-hand-list": lambda: mutant("for g in $AGI_PIECE_GLOB;do", "for g in engine.md engine-post.md;do"),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_a_mutant_goes_red(name, tmp_path_factory):
    body, glob = MUTANTS[name]()
    assert rows(body, glob, lambda n: tmp_path_factory.mktemp(n)) != [], f"mutant {name} stayed green"
