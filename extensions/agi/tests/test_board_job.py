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
    assert line == f"[board] {staged[:7]} refused: (b) path staged.txt"   # .44.2: the line names the sha, the rule, the path


def test_mutant_ff_always_lands_the_staged_work(box):
    assert box.job().returncode == 0
    staged = box.hand_commit_on_branch()
    m = mutant(box.tmp, "    if refused:\n        _notice(args.notice, f\"[board] {refused[0][0][:7]} refused: {refused[0][1]}\")\n        return 3\n    try:   # the suite lock",
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
    assert line.startswith(f"[board] {forged[:7]} refused: (a)") and "%G?=N" in line


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
    assert box.notice.read_text().startswith(f"[board] {forged[:7]} refused: (a)") and "%G?=G" in box.notice.read_text()


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
    assert got.returncode == 3 and f"{staged[:7]} refused: (b) path staged.txt" in got.stderr   # .42.2: hand work OFF nodes/ still blocks
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
    m = mutant(box.tmp, 'opts = [] if hand else ["-X", "theirs"]', "opts = []")
    got = box.job(src=m)
    assert got.returncode == 3 and box.tip() == old                         # RED: the real file settles it (the row above; this is Fc's mutant)


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


# ---- goal:g7.16.1.11.42.2 (council 3/3 10-15): the :28 land takes the Prime's own NODE commits (F1-F9)
class PrimeBox:
    """Commits on posts/belam as the Prime's hand: any paths, modes, committer, signer. Each lands on the branch tip."""

    def __init__(self, box):
        self.b = box
        self.keys = {}

    def principal(self, who):
        """A second ring member (`who`@agi) with its own key; returns the key's .pub path."""
        if who not in self.keys:
            key = self.b.home / f"key_{who}"
            run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key), "-C", who, check=True)
            with open(self.b.signers, "a") as fh:
                fh.write(f'{who}@agi namespaces="git" {" ".join(key.with_suffix(".pub").read_text().split()[:2])}\n')
            self.keys[who] = f"{key}.pub"
        return self.keys[who]

    def commit(self, files=None, delete=(), move=(), modes=None, committer="belam", signer=None, msg="belam: a node edit",
               onto=None, ref="refs/heads/posts/belam", merge=None):
        """One commit on `onto` (default the branch tip): write `files`, delete, `git mv` pairs, chmod/symlink via `modes`
        {path: '755'|'symlink'}. `signer` = a principal other than the seat's (key in the ring), None = the seat's own."""
        b = self.b
        wt = b.tmp / "prime"
        if wt.exists():
            shutil.rmtree(wt)
        b.g("worktree", "add", "-q", "--detach", str(wt), onto or b.tip())
        for path, text in (files or {}).items():
            (wt / path).parent.mkdir(parents=True, exist_ok=True)
            (wt / path).write_text(text)
        for path in delete:
            (wt / path).unlink()
        for src, dst in move:
            (wt / dst).parent.mkdir(parents=True, exist_ok=True)
            b.g("mv", src, dst, cwd=wt)
        for path, how in (modes or {}).items():
            if how == "symlink":
                (wt / path).unlink(missing_ok=True)
                (wt / path).symlink_to("elsewhere")
            else:
                (wt / path).chmod(0o755)
        b.g("add", "-A", cwd=wt)
        env = dict(b.env, GIT_AUTHOR_NAME=committer, GIT_AUTHOR_EMAIL=f"{committer}@agi",
                   GIT_COMMITTER_NAME=committer, GIT_COMMITTER_EMAIL=f"{committer}@agi")
        sign = [] if signer is None else ["-c", f"user.signingkey={self.principal(signer)}"]
        got = run("git", "-C", str(wt), *sign, "commit", "-q", "-m", msg, env=env)
        assert got.returncode == 0, got.stderr
        c = b.rev("HEAD", wt)
        b.g("update-ref", ref, c)
        b.g("worktree", "remove", "--force", str(wt))
        return c

    def job_commit(self):
        """A commit that IS the job's own (exact subject + Board-job trailer, G by the seat): what the commit step makes."""
        b = self.b
        wt = b.tmp / "prime"
        if wt.exists():
            shutil.rmtree(wt)
        b.g("worktree", "add", "-q", "--detach", str(wt), b.tip())
        (wt / ".agi" / "cell.txt").write_text(f"{os.urandom(4).hex()}\n")
        b.g("add", "-A", cwd=wt)
        got = run("git", "-C", str(wt), "commit", "-q", "-m", SUBJECT, "-m", "Board-job: metrics_cell", env=b.env)
        assert got.returncode == 0, got.stderr
        c = b.rev("HEAD", wt)
        b.g("update-ref", "refs/heads/posts/belam", c)
        b.g("worktree", "remove", "--force", str(wt))
        return c


@pytest.fixture
def pb(box):
    return PrimeBox(box)


NODE = ".agi/nodes/goal/x.md"
LAND_ENV = lambda box: dict(box.env, GIT_CONFIG_GLOBAL="/dev/null")      # uid belam's git names no signers file


def _refuses(box, rule, path=None, env=None):
    head = box.rev("HEAD")
    got = box.job("land", env=env or LAND_ENV(box))
    assert got.returncode == 3 and box.rev("HEAD") == head, got.stderr
    line = box.notice.read_text().strip().splitlines()[-1]
    assert f" refused: {rule}" in line and (path is None or path in line), line
    return line


def test_f5_a_primes_node_commits_interleaved_with_the_jobs_own_land_whole_with_one_board_line(box, pb):
    pb.commit({NODE: "1\n"})
    pb.job_commit()
    pb.commit({".agi/nodes/idea/y.md": "2\n"})
    pb.job_commit()
    tip = pb.commit({NODE: "3\n"})
    got = box.job("land", env=LAND_ENV(box))
    assert got.returncode == 0, got.stderr
    assert box.rev("HEAD") == tip                                         # ff, no commit
    assert len([ln for ln in got.stdout.splitlines() if " board: MAIN " in ln]) == 1


def test_f1_a_node_only_rule_a_prime_commit_touching_the_engine_is_refused_and_main_is_unmoved(box, pb):
    bad = pb.commit({"extensions/x.py": "print(1)\n"})
    line = _refuses(box, "(b)", "extensions/x.py")
    assert line == f"[board] {bad[:7]} refused: (b) path extensions/x.py"
    assert box.tip() == bad


def test_f1_mutant_without_rule_b_the_engine_commit_lands(box, pb):
    bad = pb.commit({"extensions/x.py": "print(1)\n"})
    m = mutant(box.tmp, '            if not path.startswith(NODES) or path.startswith(NOT_UNDER):\n                return f"(b) path {path}"',
               '            if False:\n                return f"(b) path {path}"')
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f2_a_geometry_piece_is_refused_it_becomes_every_posts_bin(box, pb):
    pb.commit({".agi/nodes/.geometry/engine-post.md": "x\n"})
    _refuses(box, "(b)", ".agi/nodes/.geometry/engine-post.md")


def test_f2_mutant_without_the_geometry_exclusion_the_piece_lands(box, pb):
    bad = pb.commit({".agi/nodes/.geometry/engine-post.md": "x\n"})
    m = mutant(box.tmp, 'NODES, NOT_UNDER = ".agi/nodes/", (".agi/nodes/.geometry/", ".agi/nodes/town/")',
               'NODES, NOT_UNDER = ".agi/nodes/", (".agi/nodes/town/",)')
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f2b_a_town_node_is_refused_the_town_mirror_reads_it_into_every_crontab(box, pb):
    pb.commit({".agi/nodes/town/x.md": "x\n"})
    _refuses(box, "(b)", ".agi/nodes/town/x.md")


def test_f2b_mutant_allowing_town_lands_it(box, pb):
    bad = pb.commit({".agi/nodes/town/x.md": "x\n"})
    m = mutant(box.tmp, 'NODES, NOT_UNDER = ".agi/nodes/", (".agi/nodes/.geometry/", ".agi/nodes/town/")',
               'NODES, NOT_UNDER = ".agi/nodes/", (".agi/nodes/.geometry/",)')
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f3_a_node_commit_signed_by_another_principal_is_refused(box, pb):
    pb.commit({NODE: "x\n"}, committer="sanctuary-master", signer="sanctuary-master")
    line = _refuses(box, "(a)")
    assert "signer sanctuary-master@agi" in line


def test_f3_mutant_trusting_g_alone_lands_the_other_principals_node_commit(box, pb):
    bad = pb.commit({NODE: "x\n"}, committer="sanctuary-master", signer="sanctuary-master")
    m = mutant(box.tmp, '    if ce != f"{post}@agi" or g != "G" or who != f"{post}@agi":\n        return f"(a)',
               '    if g != "G":\n        return f"(a)')
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f6_committer_belam_but_signed_by_another_ring_key_is_refused(box, pb):
    pb.commit({NODE: "x\n"}, committer="belam", signer="other")
    line = _refuses(box, "(a)")
    assert "committer belam@agi" in line and "signer other@agi" in line


def test_f6_mutant_trusting_the_committer_field_lands_it(box, pb):
    bad = pb.commit({NODE: "x\n"}, committer="belam", signer="other")
    m = mutant(box.tmp, '    if ce != f"{post}@agi" or g != "G" or who != f"{post}@agi":\n        return f"(a)',
               '    if ce != f"{post}@agi":\n        return f"(a)')
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f6b_an_unsigned_node_commit_by_the_seat_is_refused(box, pb):
    wt = box.tmp / "unsigned"
    box.g("worktree", "add", "-q", "--detach", str(wt), box.tip())
    (wt / NODE).parent.mkdir(parents=True, exist_ok=True)
    (wt / NODE).write_text("x\n")
    box.g("add", "-A", cwd=wt)
    assert run("git", "-C", str(wt), "-c", "commit.gpgsign=false", "commit", "-q", "-m", "belam: unsigned", env=box.env).returncode == 0
    box.g("update-ref", "refs/heads/posts/belam", box.rev("HEAD", wt))
    box.g("worktree", "remove", "--force", str(wt))
    _refuses(box, "(a)")


def test_f4_a_symlink_or_an_exec_bit_in_a_node_is_refused(box, pb):
    pb.commit({NODE: "x\n"}, modes={NODE: "symlink"})
    _refuses(box, "(c)", NODE)


def test_f4_an_exec_bit_is_refused_too(box, pb):
    pb.commit({NODE: "x\n"}, modes={NODE: "755"})
    _refuses(box, "(c)", "mode 100755")


def test_f4_mutant_without_rule_c_the_symlink_lands(box, pb):
    bad = pb.commit({NODE: "x\n"}, modes={NODE: "symlink"})
    m = mutant(box.tmp, '        if status[:1] != "D" and mode != "100644":', "        if False:")
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f7_the_notice_names_the_sha_the_rule_and_the_path_in_one_line(box, pb):
    bad = pb.commit({"extensions/x.py": "print(1)\n"})
    box.job("land", env=LAND_ENV(box))
    hits = [ln for ln in box.notice.read_text().splitlines() if bad[:7] in ln and "(b)" in ln and "extensions/x.py" in ln]
    assert len(hits) == 1


def test_f7_mutant_the_old_generic_line_names_none_of_them(box, pb):
    bad = pb.commit({"extensions/x.py": "print(1)\n"})
    m = mutant(box.tmp, '        _notice(args.notice, f"[board] {refused[0][0][:7]} refused: {refused[0][1]}")\n        return 3\n    try:   # the suite lock',
               "        _notice(args.notice, _staged_line(post, len(refused), main, refused[0][0], args.signers))\n        return 3\n    try:   # the suite lock")
    box.job("land", src=m, env=LAND_ENV(box))
    hits = [ln for ln in box.notice.read_text().splitlines() if "(b)" in ln and "extensions/x.py" in ln]
    assert hits == []


def test_f8_a_deleted_node_is_refused_a_node_renamed_into_deprecated_lands(box, pb):
    pb.commit({NODE: "the node body, long enough for rename detection to hold on to\n" * 5})
    assert box.job("land", env=LAND_ENV(box)).returncode == 0            # the add lands
    head = box.rev("HEAD")
    gone = pb.commit(delete=[NODE])
    _refuses(box, "(e)", NODE)
    box.g("update-ref", "refs/heads/posts/belam", head)
    moved = pb.commit(move=[(NODE, ".agi/nodes/deprecated/goal/x.md")])
    assert box.job("land", env=LAND_ENV(box)).returncode == 0 and box.rev("HEAD") == moved
    assert gone != moved


def test_f8_mutant_without_rule_e_the_delete_lands(box, pb):
    pb.commit({NODE: "x\n"})
    assert box.job("land", env=LAND_ENV(box)).returncode == 0
    gone = pb.commit(delete=[NODE])
    m = mutant(box.tmp, '        if status[:1] == "D":   #', "        if False:   #")
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == gone


# ---- F9: a merge passes only when it is exactly the clean merge of two checked parents
def _trunk_landing(box):
    """MAIN lands an engine change (what SM's stack does) while the Prime's node commit waits on posts/belam."""
    (box.main / "extensions").mkdir(exist_ok=True)
    (box.main / "extensions" / "x.py").write_text("a = 1\nb = 2\nc = 3\n")
    box.g("add", "-A")
    return box.commit("SM landed an engine change", extra=["--no-gpg-sign"])


def _merge(box, pb, p1, p2, hand_edit=None, signer=None, msg="belam: sync merge of the trunk"):
    wt = box.tmp / "mergewt"
    if wt.exists():
        shutil.rmtree(wt)
    box.g("worktree", "add", "-q", "--detach", str(wt), p1)
    merged = box.g("merge", "--no-commit", "--no-ff", p2, cwd=wt)
    assert merged.returncode == 0, merged.stdout + merged.stderr
    if hand_edit:
        (wt / "extensions" / "x.py").write_text(hand_edit)
        box.g("add", "-A", cwd=wt)
    got = box.g("commit", "-q", "-m", msg, cwd=wt)
    assert got.returncode == 0, got.stderr
    c = box.rev("HEAD", wt)
    box.g("update-ref", "refs/heads/posts/belam", c)
    box.g("worktree", "remove", "--force", str(wt))
    return c


def test_f9i_a_clean_sync_merge_of_a_trunk_tip_with_an_engine_change_lands(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    t = _trunk_landing(box)
    m = _merge(box, pb, n1, t)
    got = box.job("land", env=LAND_ENV(box))
    assert got.returncode == 0, got.stderr + box.notice.read_text() if box.notice.exists() else got.stderr
    assert box.rev("HEAD") == m                                           # 0 false refusals on the sync merge


def test_f9ii_the_same_merge_with_one_hand_edited_engine_line_is_refused(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    t = _trunk_landing(box)
    _merge(box, pb, n1, t, hand_edit="a = 1\nb = 2\nc = 99\n")
    head = box.rev("HEAD")
    got = box.job("land", env=LAND_ENV(box))
    assert got.returncode == 3 and box.rev("HEAD") == head
    assert "(m) the tree is not the clean merge" in box.notice.read_text()


def test_f9ii_mutant_without_the_tree_equality_the_hand_edit_lands(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    t = _trunk_landing(box)
    bad = _merge(box, pb, n1, t, hand_edit="a = 1\nb = 2\nc = 99\n")
    m = mutant(box.tmp, '            if mt.returncode or mt.stdout.split("\\n", 1)[0] != _rev(repo, f"{sha}^{{tree}}"):',
               "            if mt.returncode:")
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f9iii_a_merge_whose_second_parent_is_not_in_main_is_refused(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    side = pb.commit({".agi/nodes/idea/side.md": "s\n"}, onto=box.rev("trunk"), ref="refs/heads/side")
    m = _merge(box, pb, n1, side)
    head = box.rev("HEAD")
    got = box.job("land", env=LAND_ENV(box))
    assert got.returncode == 3 and box.rev("HEAD") == head and box.tip() == m
    assert "(m) parent 2" in box.notice.read_text()


def test_f9iii_mutant_without_the_second_parent_rule_a_landable_side_branch_lands(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    side = pb.commit({".agi/nodes/idea/side.md": "s\n"}, onto=box.rev("trunk"), ref="refs/heads/side")
    bad = _merge(box, pb, n1, side)
    m = mutant(box.tmp, "        if not _is_ancestor(repo, p2, main_head):", "        if False:")
    box.job("land", src=m, env=LAND_ENV(box))
    assert box.rev("HEAD") == bad


def test_f9_a_merge_signed_by_another_principal_is_refused_even_when_clean(box, pb):
    n1 = pb.commit({NODE: "1\n"})
    t = _trunk_landing(box)
    wt = box.tmp / "mergewt"
    box.g("worktree", "add", "-q", "--detach", str(wt), n1)
    assert box.g("merge", "--no-commit", "--no-ff", t, cwd=wt).returncode == 0
    env = dict(box.env, GIT_COMMITTER_NAME="sanctuary-master", GIT_COMMITTER_EMAIL="sanctuary-master@agi")
    got = run("git", "-C", str(wt), "-c", f"user.signingkey={pb.principal('sanctuary-master')}", "commit", "-q", "-m", "merge", env=env)
    assert got.returncode == 0, got.stderr
    box.g("update-ref", "refs/heads/posts/belam", box.rev("HEAD", wt))
    box.g("worktree", "remove", "--force", str(wt))
    _refuses(box, "(a)")


# ---- .42.2 follow-up (council 3/3 20:21Z): the :23 commit step on top of the Prime's node commits
def test_fa_ahead_with_one_pending_prime_node_commit_the_job_commits_on_top(box, pb):
    prime = pb.commit({NODE: "x\n"})
    got = box.job()
    assert got.returncode == 0, got.stderr
    new = box.tip()
    assert box.rev(f"{new}^") == prime and box.sig(new) == "G"              # the board commit sits on the Prime's; :28 lands both


def test_fa_mutant_keeping_not_own_refuses_the_pending_prime_node_commit(box, pb):
    prime = pb.commit({NODE: "x\n"})
    m = mutant(box.tmp, "            refused = not_land_ok(main, head, tip, post, args.signers)\n        else:   # diverged",
               "            refused = [(c, \"not the job's\") for c in not_own(main, head, tip, post, args.signers)]\n        else:   # diverged")
    got = box.job(src=m)
    assert got.returncode == 3 and box.tip() == prime


def _shared_doc(box):
    """x.md on the trunk AND on posts/belam, three lines: the base both sides then edit."""
    (box.main / ".agi" / "nodes" / "doc").mkdir(parents=True)
    (box.main / ".agi" / "nodes" / "doc" / "x.md").write_text("l1\nl2\nl3\n")
    box.g("add", "-A")
    base = box.commit("x.md on the trunk")
    box.g("update-ref", "refs/heads/posts/belam", base)
    return base


XMD = ".agi/nodes/doc/x.md"


def _fb_setup(box, pb):
    _shared_doc(box)
    prime = pb.commit({XMD: "l1\nPRIME l2\nl3\n"})
    (box.main / XMD).write_text("l1\nMAIN l2\nl3\n")
    box.g("add", "-A")
    box.commit("MAIN edits the same line")
    return prime


def test_fb_a_conflict_between_main_and_a_prime_hunk_stops_the_line_and_loses_nothing(box, pb):
    prime = _fb_setup(box, pb)
    got = box.job()
    assert got.returncode == 3, got.stderr
    assert box.tip() == prime                                               # posts/belam unchanged
    hits = [ln for ln in box.notice.read_text().splitlines() if prime[:7] in ln and "x.md" in ln]
    assert len(hits) == 1                                                   # ONE line naming the Prime sha and the path
    assert box.g("show", f"{box.tip()}:{XMD}").stdout.count("PRIME l2") == 1   # the Prime's line is still there


def test_fb_mutant_x_theirs_kept_for_a_mixed_range_drops_the_prime_line_in_silence(box, pb):
    prime = _fb_setup(box, pb)
    m = mutant(box.tmp, 'opts = [] if hand else ["-X", "theirs"]', 'opts = ["-X", "theirs"]')
    got = box.job(src=m)
    assert got.returncode == 0 and box.tip() != prime
    assert box.g("show", f"{box.tip()}:{XMD}").stdout.count("PRIME l2") == 0   # RED: gone, rc 0, no notice
    assert not box.notice.exists()


def test_fc_job_commits_only_diverged_x_theirs_still_takes_main(box):
    assert box.job().returncode == 0
    _main_edits_the_cell(box)
    got = box.job()
    assert got.returncode == 0, got.stderr                                  # today's behaviour, unchanged
    assert not box.notice.exists()


def test_fb_a_clean_merge_with_a_prime_commit_takes_main_without_a_stall(box, pb):
    _shared_doc(box)
    pb.commit({XMD: "l1\nPRIME l2\nl3\n"})
    (box.main / "other.txt").write_text("y")
    box.g("add", "-A")
    box.commit("a landing elsewhere on MAIN")
    got = box.job()
    assert got.returncode == 0, got.stderr
    assert not box.notice.exists()
    assert box.g("show", f"{box.tip()}:{XMD}").stdout.count("PRIME l2") == 1
