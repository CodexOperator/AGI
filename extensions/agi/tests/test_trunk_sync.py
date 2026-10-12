"""goal:g7.16.1.11.41 targets 2-4 -- agi-sync: the trunk is merged into posts/P at the end of EVERY turn, and a merge
that cannot complete is SAID by name, never skipped in silence.

The shipped pieces (agi-sync, agi-turn, agi-flush, agi-notice: the bytes in engine-post.md, extracted the way the unit's
extraction extracts a piece) run in a scratch ~/t with a real git repo, a throwaway ssh signing key and a stub `box`.
Rows: (a) a clean divergence is merged by ONE signed two-parent commit; (b) a conflict leaves the branch unmoved and
writes `[trunk-conflict] P: N path(s) conflict with TRUNK: paths` to ~/.notice AND boxes the post's parent; (c) it comes
back once per turn while it lasts (the notice, claimed, is re-added), the box is sent once per trunk tip; (d) the
cadence: a plain agi-turn (the Stop hook) carries the trunk, and so does agi-flush; (e) a kid and an unresolvable trunk.
(a2) a posts/P merely behind the trunk moves by CAS to the trunk tip with 0 new commits.
MUTANTS: the silent `&&` chain back (no notice) / the notice without the box / the box on every turn / agi-turn that
does not call agi-sync (cadence) each go RED on their own row.
"""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
POST_MD = ROOT / ".agi" / "nodes" / ".geometry" / "engine-post.md"


def piece(name: str) -> str:
    out, inp, fence = [], False, False
    for ln in POST_MD.read_text().splitlines():
        if ln.startswith(f"### {name} "):
            inp = True
            continue
        if inp and ln.startswith("##"):
            break
        if inp and ln.startswith("~~~"):
            fence = not fence
            continue
        if inp and fence:
            out.append(ln)
    assert out, f"{name} is not a fenced piece of engine-post.md"
    return "\n".join(out) + "\n"


class Box:
    """A scratch post: ~/t (a repo on `trunk` with posts/p), bin/ with the pieces, a stub box that records its mail."""

    def __init__(self, tmp: Path, overrides: dict | None = None):
        self.home = tmp / "h"
        self.t = self.home / "t"
        self.bin = tmp / "bin"
        self.mail = tmp / "mail"
        self.bin.mkdir()
        self.t.mkdir(parents=True)
        pieces = {n: piece(n) for n in ("agi-sync", "agi-notice", "agi-turn", "agi-flush")}
        pieces.update(overrides or {})
        for n, body in pieces.items():
            (self.bin / n).write_text(body)
            (self.bin / n).chmod(0o755)
        (self.bin / "box").write_text(f'#!/bin/sh\necho "$@" >>{self.mail}\ncat >>{self.mail}\n')
        (self.bin / "box").chmod(0o755)
        key = tmp / "key"
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)], check=True)
        self.env = {"PATH": f"{self.bin}:/usr/bin:/bin", "HOME": str(self.home), "AGI_POST": "p", "AGI_TRUNK": "trunk",
                    "AGI_WT": str(tmp / "wt"), "RUNTIME_DIRECTORY": str(tmp / "rt"), "GIT_CONFIG_GLOBAL": "/dev/null",
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        (tmp / "wt").mkdir()
        self.git("init", "-q", "-b", "trunk")
        self.git("config", "gpg.format", "ssh")
        self.git("config", "user.signingkey", str(key) + ".pub")
        geo = self.t / ".agi" / "nodes" / ".geometry"
        geo.mkdir(parents=True)
        (geo / "posts.md").write_text('---\n---\n  - {"name": "p", "parent": "mast", "engine": {"v": 4}}\n')
        (self.t / "f.txt").write_text("base\n")
        self.commit("base")
        self.git("branch", "posts/p")

    def git(self, *a, check=True):
        return subprocess.run(["git", "-C", str(self.t), *a], env=self.env, capture_output=True, text=True,
                              check=check).stdout.strip()

    def commit(self, msg):
        self.git("add", "-A")
        self.git("commit", "-qm", msg)

    def on(self, branch, fn, msg):
        self.git("checkout", "-q", branch)
        fn()
        self.commit(msg)

    def settle(self):
        """~/t detached at the post branch, the way a real post sits."""
        self.git("checkout", "-q", "--detach", "posts/p")

    def run(self, script: str, *args, **env):
        e = {**self.env, **env}
        return subprocess.run([str(self.bin / script), *args], env=e, capture_output=True, text=True, cwd=str(self.t))

    def notice(self):
        p = self.home / ".notice"
        return p.read_text() if p.exists() else ""

    def tip(self, ref="posts/p"):
        return self.git("rev-parse", ref)

    def mailed(self):
        return self.mail.read_text() if self.mail.exists() else ""


def write(box, rel, text):
    return lambda: (box.t / rel).write_text(text)


def diverge_clean(box):
    box.on("trunk", write(box, "g.txt", "trunk side\n"), "trunk moves")
    box.on("posts/p", write(box, "h.txt", "post side\n"), "post work")
    box.settle()


def diverge_conflict(box):
    box.on("trunk", write(box, "f.txt", "trunk edit\n"), "trunk edits f")
    box.on("posts/p", write(box, "f.txt", "post edit\n"), "post edits f")
    box.settle()


def rows(overrides, tmp_path_factory) -> list[str]:
    """Every row against the pieces (shipped, or with `overrides`); returns the names of the rows that FAIL."""
    bad = []

    def chk(name, cond):
        if not cond:
            bad.append(name)

    # (a) a clean divergence: ONE signed two-parent merge, no notice
    b = Box(tmp_path_factory.mktemp("a"), overrides)
    diverge_clean(b)
    old, T = b.tip(), b.tip("trunk")
    r = b.run("agi-sync")
    new = b.tip()
    chk("a-rc 0", r.returncode == 0)
    chk("a-the branch moved to a merge of the old tip and the trunk",
        new != old and b.git("rev-parse", new + "^1") == old and b.git("rev-parse", new + "^2") == T)
    chk("a-the merge commit is signed", "gpgsig" in b.git("cat-file", "-p", new))
    chk("a-no notice, no mail", b.notice() == "" and b.mailed() == "")
    r = b.run("agi-sync")
    chk("a-already carrying the trunk: nothing moves", b.tip() == new and r.returncode == 0 and b.notice() == "")

    # (a2) BEHIND ONLY: posts/P is an ancestor of the trunk -> a CAS fast-forward, no commit (board_job.py land refuses a non-own commit)
    b = Box(tmp_path_factory.mktemp("a2"), overrides)
    b.on("trunk", write(b, "g.txt", "trunk side\n"), "trunk moves")
    b.settle()
    T, n0 = b.tip("trunk"), b.git("rev-list", "--all", "--count")
    r = b.run("agi-sync")
    chk("a2-behind: posts/p is the trunk tip", b.tip() == T and r.returncode == 0)
    chk("a2-behind: 0 new commits", b.git("rev-list", "--all", "--count") == n0)
    chk("a2-behind: no notice, no mail", b.notice() == "" and b.mailed() == "")

    # (b) a conflict: branch unmoved, named, boxed to the parent
    b = Box(tmp_path_factory.mktemp("b"), overrides)
    diverge_conflict(b)
    old, T = b.tip(), b.tip("trunk")
    r = b.run("agi-sync")
    chk("b-rc 0 on a conflict (a Stop hook never fails)", r.returncode == 0)
    chk("b-the branch is left as it is", b.tip() == old)
    n = b.notice()
    chk("b-[trunk-conflict] names the post, the count, the trunk and the path",
        re.search(r"^\[trunk-conflict\] p: 1 path\(s\) conflict with trunk: f\.txt$", n, re.M) is not None)
    chk("b-the line is on stderr too", "[trunk-conflict] p: 1 path(s)" in r.stderr)
    chk("b-the parent is boxed: send mast + the line", b.mailed().startswith("send mast") and "[trunk-conflict] p:" in b.mailed())

    # (c) once per turn while it lasts; boxed once per trunk tip
    b.run("agi-notice")                                         # the post reads (claims) its notice
    chk("c-the notice is gone once read", b.notice() == "")
    b.run("agi-sync")
    chk("c-it comes back the next turn", "[trunk-conflict] p: 1 path(s)" in b.notice())
    chk("c-the same trunk tip is boxed ONCE", b.mailed().count("send mast") == 1)
    b.on("trunk", write(b, "f.txt", "trunk edit again\n"), "trunk moves again")
    b.settle()
    b.run("agi-sync")
    chk("c-a NEW trunk tip is boxed again", b.mailed().count("send mast") == 2)

    # (d) the cadence: a plain agi-turn (the Stop hook) and agi-flush both carry the trunk
    for who in ("agi-turn", "agi-flush"):
        b = Box(tmp_path_factory.mktemp("d" + who), overrides)
        diverge_clean(b)
        T = b.tip("trunk")
        r = b.run(who)
        chk(f"d-{who} carries the trunk (is-ancestor)",
            subprocess.run(["git", "-C", str(b.t), "merge-base", "--is-ancestor", T, "posts/p"], env=b.env).returncode == 0)
        chk(f"d-{who} leaves ~/t detached on the merged tip", b.git("rev-parse", "HEAD") == b.tip())
    b = Box(tmp_path_factory.mktemp("dc"), overrides)
    diverge_conflict(b)
    old = b.tip()
    b.run("agi-turn")
    chk("d-a conflicted agi-turn is named and moves nothing", b.tip() == old and "[trunk-conflict]" in b.notice())

    # (e) a kid does nothing; an unresolvable trunk is named
    b = Box(tmp_path_factory.mktemp("e"), overrides)
    diverge_conflict(b)
    r = b.run("agi-sync", AGI_ROLE="kid")
    chk("e-a kid: rc 0, no notice, no mail", r.returncode == 0 and b.notice() == "" and b.mailed() == "")
    r = b.run("agi-sync", AGI_TRUNK="no-such-trunk")
    chk("e-an unresolvable trunk is named", r.returncode == 0 and "[trunk-merge-failed] p: no-such-trunk" in b.notice())
    return bad


def test_the_shipped_pieces_pass_every_row(tmp_path_factory):
    assert rows({}, tmp_path_factory) == []


def mut(name, old, new):
    p = piece(name)
    assert old in p, f"the mutant no longer applies to {name}: {old!r}"
    return {name: p.replace(old, new, 1)}


MUTANTS = {
    # the old silent chain: a conflict is skipped, nothing said
    "silent-on-conflict": lambda: mut("agi-sync", 'echo "$m">&2;agi-notice add "$m"', ":"),
    # the notice is written but the parent is never boxed
    "never-boxes-the-parent": lambda: mut("agi-sync", "&&echo \"$m (trunk", "&&true||echo \"$m (trunk"),
    # boxed on every turn, not once per trunk tip
    "boxes-every-turn": lambda: mut("agi-sync", '[ "$(cat ~/.trunk-boxed 2>/dev/null)" = $T ]||', ""),
    # today's merge-when-behind: a behind posts/P gets a "P: merge <trunk>" commit (tree == the trunk's), never its own
    "merges-when-behind": lambda: mut("agi-sync", 'git merge-base --is-ancestor $b $T&&{ git update-ref $b $T $t||agi-notice add "[trunk-merge-failed] $P: cannot move posts/$P";exit 0;}\n', ""),
    # the cadence: agi-turn no longer calls agi-sync
    "turn-does-not-sync": lambda: mut("agi-turn", "unset GIT_INDEX_FILE;agi-sync;", "unset GIT_INDEX_FILE;"),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_a_mutant_goes_red(name, tmp_path_factory):
    assert rows(MUTANTS[name](), tmp_path_factory) != [], f"mutant {name} stayed green"
