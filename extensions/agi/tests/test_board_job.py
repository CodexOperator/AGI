"""goal:g7.16.1.11.42 (option E, council 3/3 15:07Z, C1-C6): the board job's commit is G, made in the seat's own uid,
and the human uid's one step lands only the job's own commits.

Real git, a real ssh signing key + allowed-signers file, a stand-in writer (what metrics_cell.py/write.py do: one
commit with the exact subject). MUTANTS are source copies of board_job.py edited with a replace that must change the
text; each must break the row it names (the assertion the REAL file passes fails on it).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "bin" / "board_job.py"
SUBJECT = "write.py: town:local-maxxing (belam)"
WRITER = ["sh", "-c", 'date +%s%N > .agi/cell.txt && git add -A && git commit -q -m "write.py: town:local-maxxing (belam)"']

pytestmark = pytest.mark.skipif(not shutil.which("ssh-keygen"), reason="ssh-keygen is needed to sign")


def run(*args, cwd=None, env=None, check=False):
    return subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True, check=check)


class Box:
    """A MAIN repo (trunk checked out), a posts/belam branch, the seat's HOME with signing, a notice file."""

    def __init__(self, tmp: Path, sign: bool = True):
        self.tmp, self.home = tmp, tmp / "home"
        self.home.mkdir()
        self.main, self.work, self.notice = tmp / "main", tmp / "work", tmp / "notice"
        key = self.home / "id_ed25519"
        run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", "belam", check=True)
        signers = self.signers = tmp / "allowed_signers"
        signers.write_text(f'belam@agi namespaces="git" {" ".join(key.with_suffix(".pub").read_text().split()[:2])}\n')
        cfg = ["[user]", f"\tsigningkey = {key}.pub", "\temail = belam@agi", "\tname = belam",
               "[gpg]", "\tformat = ssh", '[gpg "ssh"]', f"\tallowedSignersFile = {signers}",
               "[safe]", "\tdirectory = *"]
        if sign:
            cfg += ["[commit]", "\tgpgsign = true"]
        (self.home / ".gitconfig").write_text("\n".join(cfg) + "\n")
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "GIT_CONFIG_GLOBAL": str(self.home / ".gitconfig"),
                    "GIT_CONFIG_SYSTEM": "/dev/null"}
        self.main.mkdir()
        self.g("init", "-q", "-b", "trunk")
        (self.main / ".agi").mkdir()
        (self.main / ".agi" / "cell.txt").write_text("0\n")
        self.g("add", "-A")
        self.commit("base")
        self.g("branch", "posts/belam")

    def g(self, *a, cwd=None, env=None):
        return run("git", "-C", str(cwd or self.main), *a, env=env or self.env)

    def commit(self, msg, cwd=None, extra=()):
        got = self.g("commit", "-q", "-m", msg, *extra, cwd=cwd)
        assert got.returncode == 0, got.stderr
        return self.rev("HEAD", cwd)

    def rev(self, r, cwd=None):
        return self.g("rev-parse", r, cwd=cwd).stdout.strip()

    def tip(self):
        return self.rev("refs/heads/posts/belam")

    def hand_commit_on_branch(self, msg="belam: staged work (.40.1 waits on the pytest)"):
        """The Prime's hand: a commit on posts/belam that is NOT the job's (same committer)."""
        wt = self.tmp / "hand"
        if wt.exists():
            shutil.rmtree(wt)
        self.g("worktree", "add", "-q", "--detach", str(wt), "posts/belam")
        (wt / "staged.txt").write_text(msg)
        self.g("add", "-A", cwd=wt)
        c = self.commit(msg, cwd=wt)
        self.g("update-ref", "refs/heads/posts/belam", c)
        self.g("worktree", "remove", "--force", str(wt))
        return c

    def job(self, verb="commit", writer=None, src=SRC, extra=(), env=None, work=None):
        args = [sys.executable, str(src), verb, "--main", str(self.main), "--post", "belam", "--notice", str(self.notice),
                "--signers", str(self.signers)]
        if verb == "commit":
            args += ["--job", "metrics_cell", "--work", str(work or self.work), *extra, "--", *(writer or WRITER)]
        return run(*args, env=env or self.env)

    def sig(self, rev):
        return self.g("log", "-1", "--format=%G?", rev).stdout.strip()

    def body(self, rev):
        return self.g("log", "-1", "--format=%s%n%b", rev).stdout


@pytest.fixture
def box(tmp_path):
    return Box(tmp_path)


def mutant(tmp_path: Path, old: str, new: str) -> Path:
    text = SRC.read_text()
    assert text.count(old) == 1, f"mutant anchor not unique: {old!r}"
    p = tmp_path / "board_job_mutant.py"
    p.write_text(text.replace(old, new))
    return p


# ---- C2 / C3: the commit is G, exact subject, the job named by a trailer, ONE commit on the old tip
def test_commit_is_g_with_exact_subject_and_job_trailer(box):
    old = box.tip()
    got = box.job()
    assert got.returncode == 0, got.stderr
    new = box.tip()
    assert new != old and box.rev(f"{new}^") == old                      # CAS shape: new^1 == the old tip
    assert box.g("rev-list", "--count", f"{old}..{new}").stdout.strip() == "1"
    assert box.sig(new) == "G"                                           # C2
    subject, _, rest = box.body(new).partition("\n")
    assert subject == SUBJECT and "Board-job: metrics_cell" in rest      # C3: exact subject + trailer
    assert box.g("log", "-1", "--format=%ce", new).stdout.strip() == "belam@agi"
    assert box.rev("HEAD") != new                                        # the commit step never touches MAIN's branch


def test_an_unsignable_commit_is_never_published(tmp_path):
    b = Box(tmp_path, sign=False)                                         # no commit.gpgsign: the commit would be N
    old = b.tip()
    got = b.job()
    assert got.returncode == 3 and "not G" in got.stderr
    assert b.tip() == old                                                 # nothing published, no new ref


def test_mutant_publishing_without_the_g_check_is_red(tmp_path):
    b = Box(tmp_path, sign=False)
    old = b.tip()
    m = mutant(tmp_path, 'if sig != "G":   # C2: an N is never published', "if False:")
    assert b.job(src=m).returncode == 0 and b.tip() != old               # the mutant publishes an N: test_an_unsignable... forbids it
    assert b.sig(b.tip()) != "G"


# ---- C5: never ~/t; the ff makes no commit
def test_the_job_refuses_the_primes_own_tree(box):
    got = box.job(work=box.home / "t")
    assert got.returncode == 2 and "~/t" in got.stderr
    assert not (box.home / "t").exists()


def test_land_ffs_main_to_the_tip_and_makes_no_commit(box):
    assert box.job().returncode == 0
    tip, before = box.tip(), box.rev("HEAD")
    got = box.job("land")
    assert got.returncode == 0, got.stderr
    assert box.rev("HEAD") == tip                                         # MAIN IS the tip: an ff
    assert box.g("rev-list", "--count", f"{before}..HEAD").stdout.strip() == "1"   # only the job's one commit arrived
    assert box.g("rev-list", "--parents", "-1", "HEAD").stdout.split()[1:] == [before]   # not a merge made by land


# ---- CAS: a raced tip is exit 4 and never a commit over the other writer's
def test_a_raced_tip_is_exit_4_and_the_other_writers_commit_survives(box):
    racer = ("sh -c 'git commit -q --allow-empty -m raced && git update-ref refs/heads/posts/belam HEAD "
             "$(git rev-parse refs/heads/posts/belam)'")
    # the writer first makes its commit, then a peer (agi-at) advances posts/belam under it
    peer = box.tmp / "peer"
    box.g("worktree", "add", "-q", "--detach", str(peer), "posts/belam")
    box.commit("peer card", cwd=peer, extra=("--allow-empty",))
    peer_tip = box.rev("HEAD", peer)
    script = (f'date +%s%N > .agi/cell.txt && git add -A && git commit -q -m "{SUBJECT}" && '
              f'git --git-dir={box.main}/.git update-ref refs/heads/posts/belam {peer_tip}')
    got = box.job(writer=["sh", "-c", script])
    assert got.returncode == 4 and "[raced]" in got.stderr
    assert box.tip() == peer_tip                                          # the peer's commit is still the tip


def test_mutant_without_the_cas_overwrites_the_other_writers_tip(box):
    peer = box.tmp / "peer"
    box.g("worktree", "add", "-q", "--detach", str(peer), "posts/belam")
    box.commit("peer card", cwd=peer, extra=("--allow-empty",))
    peer_tip = box.rev("HEAD", peer)
    script = (f'date +%s%N > .agi/cell.txt && git add -A && git commit -q -m "{SUBJECT}" && '
              f'git --git-dir={box.main}/.git update-ref refs/heads/posts/belam {peer_tip}')
    m = mutant(box.tmp, 'if _rev(work, f"{new}^") != _rev(main, ref):', "if False:")
    text = m.read_text().replace('f"--force-with-lease={ref}:{base}"', '"--force"')
    m.write_text(text)
    box.job(src=m, writer=["sh", "-c", script])
    assert box.tip() != peer_tip                                          # the mutant drops the peer's staged commit: the real file keeps it


# ---- the job's LOG (belam 04:0xZ, goal:g7.16.1.11.42): every line is stamped UTC, a [raced] line names old -> seen
STAMP = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ ")


def _raced_run(box, src=SRC):
    """A writer commits, then a peer (agi-at) advances posts/belam under the job; returns (the tip the job started from, the peer's tip, the run)."""
    start = box.tip()
    peer = box.tmp / "peer"
    box.g("worktree", "add", "-q", "--detach", str(peer), "posts/belam")
    box.commit("peer card", cwd=peer, extra=("--allow-empty",))
    peer_tip = box.rev("HEAD", peer)
    script = (f'date +%s%N > .agi/cell.txt && git add -A && git commit -q -m "{SUBJECT}" && echo "writer says hi" && '
              f'git --git-dir={box.main}/.git update-ref refs/heads/posts/belam {peer_tip}')
    return start, peer_tip, box.job(src=src, writer=["sh", "-c", script])


def test_every_line_of_a_run_carries_a_utc_stamp_the_writers_own_included(box):
    got = box.job(writer=["sh", "-c", WRITER[2] + ' && echo "updated: town:local-maxxing"'])
    lines = [l for l in (got.stdout + got.stderr).splitlines() if l.strip()]
    assert got.returncode == 0 and len(lines) >= 2
    assert all(STAMP.match(l) for l in lines), lines
    assert any(l.endswith("updated: town:local-maxxing") for l in lines)                 # the writer's line, stamped by the job


def test_a_raced_runs_line_carries_the_stamp_and_both_shas(box):
    start, peer_tip, got = _raced_run(box)
    assert got.returncode == 4
    (raced,) = [l for l in got.stderr.splitlines() if "[raced]" in l]
    m = re.match(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) \[raced\] posts/belam moved under the job: next hour \(old ([0-9a-f]{12}) -> seen ([0-9a-f]{12})\)$", raced)
    assert m, raced
    assert m.group(2) == start[:12] and m.group(3) == peer_tip[:12]                      # old = the tip the job built on, seen = what the ref is now


def test_mutant_without_the_stamp_a_line_cannot_be_placed_in_time(box):
    m = mutant(box.tmp, 'print(f"{_now()} {line}", file=sys.stderr if err else sys.stdout)', 'print(f"{line}", file=sys.stderr if err else sys.stdout)')
    got = box.job(src=m)
    assert not all(STAMP.match(l) for l in (got.stdout + got.stderr).splitlines() if l.strip())      # the real file stamps them all (row above)


def test_mutant_a_raced_line_without_the_shas_is_red(box):
    m = mutant(box.tmp, 'next hour (old {_sh(base)} -> seen {_sh(_rev(main, ref))})")', 'next hour")')
    _, _, got = _raced_run(box, src=m)
    (raced,) = [l for l in got.stderr.splitlines() if "[raced]" in l]
    assert not re.search(r"old [0-9a-f]{12} -> seen [0-9a-f]{12}", raced)                 # the real file names both (row above)


# ---- C6: the second-lander guard
def test_land_refuses_staged_work_that_is_not_the_jobs(box):
    assert box.job().returncode == 0
    staged = box.hand_commit_on_branch()
    head = box.rev("HEAD")
    got = box.job("land")
    assert got.returncode == 3
    assert box.rev("HEAD") == head and box.tip() == staged               # no ff, the staged commit still only on the branch
    line = box.notice.read_text().strip()
    assert line == f"[board] posts/belam carries 1 commits not the job's (first {staged[:7]}, %G?=G): no ff, the board line waits"


def test_mutant_ff_always_lands_the_staged_work(box):
    assert box.job().returncode == 0
    staged = box.hand_commit_on_branch()
    m = mutant(box.tmp, "    if staged:\n        _notice(args.notice, _staged_line(post, len(staged), main, staged[0], args.signers))\n        return 3\n    try:   # the suite lock",
               "    try:   # the suite lock")
    box.job("land", src=m)
    assert box.rev("HEAD") == staged                                      # RED: the 'ff always' mutant lands unreviewed work


# ---- council 18:06Z condition (b): land checks the signature and the principal ITSELF
def _forge(box, signed_by=None):
    """A commit on posts/belam that LOOKS like the job's (exact subject, a Board-job trailer, committer email belam@agi);
    unsigned unless signed_by (a key file) is given. Any uid in group agi can move posts/belam, so this is the attack."""
    wt = box.tmp / "forge"
    if wt.exists():
        shutil.rmtree(wt)
    box.g("worktree", "add", "-q", "--detach", str(wt), "posts/belam")
    (wt / ".agi" / "cell.txt").write_text("forged\n")
    box.g("add", "-A", cwd=wt)
    env = dict(box.env, GIT_AUTHOR_NAME="x", GIT_AUTHOR_EMAIL="x@evil", GIT_COMMITTER_NAME="x", GIT_COMMITTER_EMAIL="belam@agi")
    sign = ["-c", "commit.gpgsign=false"] if signed_by is None else ["-c", "commit.gpgsign=true", "-c", f"user.signingkey={signed_by}"]
    got = run("git", "-C", str(wt), *sign, "commit", "-q", "-m", SUBJECT, "-m", "Board-job: forged", env=env)
    assert got.returncode == 0, got.stderr
    c = box.rev("HEAD", wt)
    box.g("update-ref", "refs/heads/posts/belam", c)
    box.g("worktree", "remove", "--force", str(wt))
    return c


def test_an_unsigned_commit_dressed_as_the_jobs_is_not_landed(box):
    forged = _forge(box)
    assert box.sig(forged) in ("N", "")                                   # %G? = N (or no verdict: no signers file in this config)
    head = box.rev("HEAD")
    env = dict(box.env, GIT_CONFIG_GLOBAL="/dev/null")                    # uid belam's git: it names NO signers file
    got = box.job("land", env=env)
    assert got.returncode == 3 and box.rev("HEAD") == head               # MAIN unmoved
    line = box.notice.read_text().strip()
    assert forged[:7] in line and "%G?=N" in line and line.endswith("no ff, the board line waits")


def test_mutant_land_without_the_signature_check_ffs_the_forged_commit(box):
    forged = _forge(box)
    m = mutant(box.tmp, '    if g != "G" or who != f"{post}@agi":\n        return False', "    pass")
    box.job("land", src=m, env=dict(box.env, GIT_CONFIG_GLOBAL="/dev/null"))
    assert box.rev("HEAD") == forged                                      # RED: the real file refuses it (the row above)


def test_a_commit_signed_by_another_key_on_the_ring_is_not_the_seats(box):
    other = box.home / "other_key"
    run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(other), "-C", "other", check=True)
    with open(box.signers, "a") as fh:                                    # a second, LEGITIMATE ring member
        fh.write(f'other@agi namespaces="git" {" ".join(other.with_suffix(".pub").read_text().split()[:2])}\n')
    forged = _forge(box, signed_by=f"{other}.pub")
    assert box.sig(forged) == "G"                                         # the signature itself verifies: a valid key, the wrong principal
    head = box.rev("HEAD")
    got = box.job("land", env=dict(box.env, GIT_CONFIG_GLOBAL="/dev/null"))
    assert got.returncode == 3 and box.rev("HEAD") == head
    assert forged[:7] in box.notice.read_text() and "%G?=G" in box.notice.read_text()


def test_mutant_land_that_takes_any_ring_key_ffs_the_other_principals_commit(box):
    other = box.home / "other_key"
    run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(other), "-C", "other", check=True)
    with open(box.signers, "a") as fh:
        fh.write(f'other@agi namespaces="git" {" ".join(other.with_suffix(".pub").read_text().split()[:2])}\n')
    forged = _forge(box, signed_by=f"{other}.pub")
    m = mutant(box.tmp, '    if g != "G" or who != f"{post}@agi":', '    if g != "G":')
    box.job("land", src=m, env=dict(box.env, GIT_CONFIG_GLOBAL="/dev/null"))
    assert box.rev("HEAD") == forged                                      # RED: the real file requires the seat's principal


def test_the_commit_step_also_refuses_to_stack_on_staged_work(box):
    staged = box.hand_commit_on_branch()
    got = box.job()
    assert got.returncode == 3 and "not the job's" in got.stderr
    assert box.tip() == staged                                            # no board commit on top of work waiting on a pytest


def test_an_own_only_branch_lands_whole(box):
    assert box.job().returncode == 0 and box.job().returncode == 0       # two hours of board commits, MAIN never moved
    tip = box.tip()
    assert box.job("land").returncode == 0 and box.rev("HEAD") == tip


# ---- the base: MAIN ahead is a pure ref move; diverged takes MAIN with a signed merge only when every commit is the job's
def test_main_ahead_moves_the_branch_without_a_commit(box):
    (box.main / "other.txt").write_text("x")
    box.g("add", "-A")
    ahead = box.commit("a landing on MAIN")
    assert box.job().returncode == 0
    new = box.tip()
    assert box.rev(f"{new}^") == ahead                                    # the board commit sits on MAIN's tip
    assert box.g("rev-list", "--count", f"{ahead}..{new}").stdout.strip() == "1"


def test_diverged_with_only_the_jobs_commits_takes_main_by_a_signed_merge(box):
    assert box.job().returncode == 0
    (box.main / "other.txt").write_text("x")
    box.g("add", "-A")
    ahead = box.commit("a landing on MAIN")
    assert box.job().returncode == 0
    new = box.tip()
    parents = box.g("rev-list", "--parents", "-1", new).stdout.split()[1:]
    assert len(parents) == 1                                              # the board commit itself
    take = parents[0]
    assert box.sig(take) == "G" and box.body(take).startswith("board: take MAIN")
    assert ahead in box.g("rev-list", "--parents", "-1", take).stdout.split()[1:]
    assert box.job("land").returncode == 0 and box.rev("HEAD") == new


def _main_edits_the_cell(box, content="MAIN edited the cell\n"):
    (box.main / ".agi" / "cell.txt").write_text(content)
    box.g("add", "-A")
    return box.commit("MAIN edits the node (e.g. its edited_by stamp)")


def test_a_content_conflict_with_main_is_settled_on_mains_side_and_the_board_line_goes_on(box):
    assert box.job().returncode == 0                                        # the job's commit rewrites cell.txt
    ahead = _main_edits_the_cell(box)                                       # MAIN changes the SAME line: a content conflict
    got = box.job()
    assert got.returncode == 0, got.stderr
    new = box.tip()
    take = box.g("rev-list", "--parents", "-1", new).stdout.split()[1]
    assert box.sig(take) == "G" and ahead in box.g("rev-list", "--parents", "-1", take).stdout.split()[1:]
    assert box.g("show", f"{take}:.agi/cell.txt").stdout == "MAIN edited the cell\n"      # MAIN's side won the merge
    assert box.g("show", f"{new}:.agi/cell.txt").stdout != "MAIN edited the cell\n"       # the writer rewrote the cell after it
    assert not box.notice.exists()                                          # nothing stalled, nothing to tell


def test_mutant_without_x_theirs_the_conflict_stalls_the_line(box):
    assert box.job().returncode == 0
    _main_edits_the_cell(box)
    old = box.tip()
    m = mutant(box.tmp, '"--no-ff", "-X", "theirs", "-m"', '"--no-ff", "-m"')
    got = box.job(src=m)
    assert got.returncode == 3 and box.tip() == old                         # RED: the real file settles it (the row above)


def test_a_refusal_the_x_option_cannot_settle_reaches_the_notice_file(box):
    assert box.job().returncode == 0
    box.g("rm", "-q", ".agi/cell.txt")                                      # MAIN deletes the node the job modified: modify/delete
    box.commit("MAIN removes the node")
    old = box.tip()
    got = box.job()
    assert got.returncode == 3 and box.tip() == old
    line = box.notice.read_text().strip()
    assert line.startswith("[board] take MAIN did not merge clean (") and line.endswith("the board line waits")


def test_mutant_a_refusal_with_no_notice_stalls_in_silence(box):
    assert box.job().returncode == 0
    box.g("rm", "-q", ".agi/cell.txt")
    box.commit("MAIN removes the node")
    old = SRC.read_text()
    start = old.index("            _notice(args.notice, f\"[board] take MAIN did not merge clean")
    end = old.index("the board line waits\")", start) + len("the board line waits\")")
    m = box.tmp / "board_job_mutant.py"
    m.write_text(old[:start] + "            print('refused', file=sys.stderr)" + old[end:])
    box.job(src=m)
    assert not box.notice.exists()                                          # RED: the real file writes the line (the row above)


def test_diverged_with_staged_work_is_refused(box):
    box.hand_commit_on_branch()
    (box.main / "other.txt").write_text("x")
    box.g("add", "-A")
    box.commit("a landing on MAIN")
    tip = box.tip()
    got = box.job()
    assert got.returncode == 3 and box.tip() == tip


# ---- the job owns its git env; usage
def test_an_inherited_git_dir_is_ignored(box, tmp_path):
    other = tmp_path / "other"
    run("git", "init", "-q", str(other), env=box.env)
    env = dict(box.env, GIT_DIR=str(other / ".git"), GIT_WORK_TREE=str(other))
    got = box.job(env=env)
    assert got.returncode == 0, got.stderr
    assert run("git", "-C", str(other), "rev-list", "--all", "--count", env=box.env).stdout.strip() == "0"


def test_no_writer_is_usage_rc_2(box):
    got = run(sys.executable, str(SRC), "commit", "--main", str(box.main), "--job", "j", "--work", str(box.work), env=box.env)
    assert got.returncode == 2


def test_help_exits_0():
    got = run(sys.executable, str(SRC), "--help")
    assert got.returncode == 0 and got.stdout.strip()
