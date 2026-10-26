"""goal:g7.16.1.11.46.23 V8a tip 2c: extensions/agi/guard/r-land, the land rule for config:posts/seats rows.

Real git repos, real ssh-ed25519 keys, real signed commits (committer email = <post>@agi, as the engine's
`box`/`agi-land` resolve a signer). Each council row has an ADMIT and a MUTANT that is REFUSED:
  R1 the signer, never %an/%ae        R2 added/deleted rows, a post never mints its own row, grants from DATA
  R3 anything unreadable is refused   veto freeze and town vocabulary    merge handling
  MODE one cell (report | enforce) read from BASE: report prints `would refuse`, rc 0; enforce refuses, rc 1
       (the mode is read BEFORE the ring: a ringless uid is rc 0 in report, rc 1 in enforce)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "extensions" / "agi" / "guard" / "r-land"
G = ".agi/nodes/.geometry"

SCHEMA = """---
name: config
written_by: [owner, prime_director]
self_row: {list_key: seats, match_key: name, fields: [session_ref, session_name, session_id, generation, window, pid, pubkey, sig_scheme, enc_scheme, key_history]}
actor_rows:
  - {actor: master, list_key: posts, match_key: name, fields: [town, quiet, status, box, worktree], ops: [create, set, retire], deny_roles: [kid, parent]}
town_cell: {field: town, match_key: name, list_keys: [posts, seats], accepted_from: ladder.towns, also_accepted: [core]}
r_land: {mode: enforce}
---
# config
"""
LADDER = "---\nid: ladder:ladder\ntype: ladder\ntowns: [sanctuary, local-maxxing]\n---\n"
VETOES = "---\nid: config:vetoes\ntype: config\nactive_gates: []\nvetoes: []\n---\n"
VETOES_FROZEN = '---\nid: config:vetoes\ntype: config\nactive_gates:\n  - {scope: prime, answered: ""}\nvetoes: []\n---\n'
ROWS = [
    {"name": "belam", "role": "prime_director", "tier": 3, "model": "m", "town": "sanctuary"},
    {"name": "master", "role": "director", "tier": 1, "model": "m", "town": "sanctuary"},
    {"name": "dg1", "role": "director", "tier": 1, "model": "m", "pid": 1, "town": "core"},
    {"name": "dg2", "role": "director", "tier": 1, "model": "m", "pid": 2, "town": "core"},
    {"name": "kid", "role": "kid", "tier": "untrusted", "model": "m", "town": "core"},
    {"name": "newname", "role": "director", "tier": 1, "model": "m", "town": "core", "was": "old"},   # a renamed seat: the key is still `old`
]


def _posts(rows):
    return ("---\nid: config:posts\ntype: config\nposts:\n"
            + "".join("  - " + json.dumps(r) + "\n" for r in rows) + "---\n# posts\n")


class Repo:
    def __init__(self, tmp: Path):
        self.d = tmp / "repo"
        self.k = tmp / "keys"
        self.k.mkdir()
        self.d.mkdir()
        self.signers = tmp / "allowed_signers"
        lines = []
        for p in ("belam", "master", "dg1", "dg2", "kid", "ghost", "old", "intruder"):
            kp = self.k / p
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(kp), "-C", p], check=True)
            if p != "intruder":  # the intruder's key is deliberately NOT in the ring
                pub = (self.k / f"{p}.pub").read_text().split()
                lines.append(f'{p}@agi namespaces="git" {pub[0]} {pub[1]}')
        self.signers.write_text("\n".join(lines) + "\n")
        self.git("init", "-q", "-b", "main")
        for k, v in (("gpg.format", "ssh"), ("commit.gpgsign", "true"),
                     ("gpg.ssh.allowedSignersFile", str(self.signers)), ("user.name", "x"), ("user.email", "x@agi")):   # a fixture never leans on the runner's identity (a post uid's env carries GIT_AUTHOR_*; env -i has none)
            self.git("config", k, v)
        (self.d / ".agi/context/schemas").mkdir(parents=True)
        (self.d / G).mkdir(parents=True)
        self.write(".agi/context/schemas/[config].md", SCHEMA)
        self.write(f"{G}/ladder.md", LADDER)
        self.write(f"{G}/vetoes.md", VETOES)
        self.write(f"{G}/posts.md", _posts(ROWS))
        self.write("extensions/agi/guard/r-land", SCRIPT.read_text(encoding="utf-8"))   # the hook runs BASE's copy
        self.base = self.commit("belam", "base")

    def git(self, *a, env=None, check=True):
        e = {**os.environ, **(env or {})}
        return subprocess.run(["git", "-C", str(self.d), *a], capture_output=True, text=True, env=e, check=check)

    def write(self, rel, text):
        p = self.d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def commit(self, signer, msg, author=None):
        self.git("add", "-A")
        env = {"GIT_COMMITTER_EMAIL": f"{signer}@agi", "GIT_COMMITTER_NAME": signer,
               "GIT_AUTHOR_EMAIL": f"{author or signer}@agi", "GIT_AUTHOR_NAME": author or signer}
        self.git("-c", f"user.signingkey={self.k / signer}", "commit", "-q", "-m", msg, "--allow-empty", env=env)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def edit_rows(self, fn, signer, author=None, msg="edit rows"):
        rows = json.loads(json.dumps(ROWS))
        fn(rows)
        self.write(f"{G}/posts.md", _posts(rows))
        return self.commit(signer, msg, author)

    def set_mode(self, mode, signer="belam"):
        """Rewrite BASE's schema `r_land` line (mode=None removes it) and commit it: the new base."""
        t = SCHEMA.replace("r_land: {mode: enforce}\n", "" if mode is None else f"r_land: {{mode: {mode}}}\n")
        self.write(".agi/context/schemas/[config].md", t)
        return self.commit(signer, f"mode {mode}")

    def run(self, base=None, tip=None, ring=None):
        r = subprocess.run(["sh", str(SCRIPT), base or self.base, tip or "HEAD"], cwd=self.d, capture_output=True,
                           text=True, env={**os.environ, "AGI_RING": ring or str(self.signers)})
        return r.returncode, r.stdout.strip()


@pytest.fixture()
def repo(tmp_path):
    return Repo(tmp_path)


def row(rows, name):
    return next(r for r in rows if r["name"] == name)


# ---- ADMITS --------------------------------------------------------------------------------------
def test_unchanged_cells_pass(repo):
    repo.write("note.txt", "x")
    repo.commit("dg1", "not a config change")
    rc, out = repo.run()
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)"), out


def test_own_row_self_row_cells_admitted(repo):
    repo.edit_rows(lambda r: row(r, "dg1").update(pubkey="ab", pid=9), "dg1")
    assert repo.run()[0] == 0


def test_prime_written_by_admitted(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(model="o/p"), "belam")
    assert repo.run()[0] == 0


def test_master_actor_rows_grant_admitted(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(quiet=True, box="b"), "master")
    assert repo.run()[0] == 0


def test_a_merge_that_takes_one_side_wholesale_adds_nothing(repo):
    side = repo.git("rev-parse", "HEAD").stdout.strip()
    repo.git("checkout", "-q", "-b", "side")
    s1 = repo.edit_rows(lambda r: row(r, "dg1").update(pubkey="ab"), "dg1")
    repo.git("checkout", "-q", "main")
    repo.write("other.txt", "y")
    repo.commit("belam", "main moves")
    env = {"GIT_COMMITTER_EMAIL": "master@agi", "GIT_COMMITTER_NAME": "master",
           "GIT_AUTHOR_EMAIL": "master@agi", "GIT_AUTHOR_NAME": "master"}
    repo.git("-c", f"user.signingkey={repo.k / 'master'}", "merge", "--no-ff", "-q", "-m", "land", "side", env=env)
    rc, out = repo.run()
    assert rc == 0, out          # the merge (signed by master) wrote no new cell; dg1's own commit is judged on its own


# ---- R1: the signer, never %an/%ae ---------------------------------------------------------------
def test_R1_mutant_signed_by_dg1_author_belam_edits_belams_row_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "belam").update(model="evil"), "dg1", author="belam")
    rc, out = repo.run()
    assert rc == 1 and "(dg1, belam, set model," in out and out.startswith("R-land: refused "), out


def test_R1_mutant_a_commit_signed_by_a_key_outside_the_ring_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg1").update(pid=3), "intruder", author="dg1")
    rc, out = repo.run()
    assert rc == 1 and "signed by nobody the ring knows" in out, out


# ---- R2: rows added / deleted, own-row minting, grants from DATA ---------------------------------
def test_R2_mutant_a_post_adds_a_row_named_after_itself_is_refused(repo):
    rows = [r for r in json.loads(json.dumps(ROWS)) if r["name"] != "kid"]
    repo.write(f"{G}/posts.md", _posts(rows))
    base = repo.commit("belam", "kid has no row yet")          # a prime may delete a row
    repo.edit_rows(lambda r: None, "kid")                       # 'kid' (ring key) writes the full list, row 'kid' back in
    rc, out = repo.run(base=base)
    assert rc == 1 and "a post never mints its own row (R2)" in out, out


def test_R2_mutant_a_post_deleting_another_row_is_refused(repo):
    repo.edit_rows(lambda r: r.remove(row(r, "dg2")), "dg1")
    rc, out = repo.run()
    assert rc == 1 and "retire of a row needs a written_by role or an actor_rows grant" in out, out


def test_R2_mutant_a_rename_is_a_delete_plus_an_add_and_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(name="dg2-renamed"), "dg1")
    rc, out = repo.run()
    assert rc == 1 and "retire" in out and "create" in out, out


def test_R2_a_prime_may_add_and_delete_but_not_mint_its_own_row(repo):
    repo.edit_rows(lambda r: r.append({"name": "newpost", "role": "kid"}), "belam")
    assert repo.run()[0] == 0
    repo2_base = repo.git("rev-parse", "HEAD").stdout.strip()
    rows = json.loads(json.dumps(ROWS)) + [{"name": "newpost", "role": "kid"}, {"name": "belam2", "role": "kid"}]
    repo.write(f"{G}/posts.md", _posts(rows))
    repo.commit("belam", "another add")
    assert repo.run(base=repo2_base)[0] == 0


def test_R2_mutant_another_posts_row_by_a_non_granted_non_prime_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run()
    assert rc == 1 and "admitted by no written_by role, self_row or actor_rows grant" in out, out


def test_R2_mutant_own_row_protected_cell_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg1").update(model="x/y"), "dg1")
    assert repo.run()[0] == 1


def test_R2_mutant_master_outside_its_grant_fields_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "master")
    assert repo.run()[0] == 1


def test_R2_mutant_master_on_a_denied_row_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "kid").update(box="b"), "master")
    assert repo.run()[0] == 1


# ---- veto freeze + town vocabulary ---------------------------------------------------------------
def test_veto_mutant_frozen_scope_refuses_a_prime_edit_of_another_row(repo):
    repo.write(f"{G}/vetoes.md", VETOES_FROZEN)
    base = repo.commit("belam", "freeze")
    repo.edit_rows(lambda r: row(r, "dg2").update(model="o/p"), "belam")
    rc, out = repo.run(base=base)
    assert rc == 1 and "FROZEN" in out, out


def test_veto_frozen_scope_still_admits_the_signers_own_self_row_write(repo):
    repo.write(f"{G}/vetoes.md", VETOES_FROZEN)
    base = repo.commit("belam", "freeze")
    repo.edit_rows(lambda r: row(r, "dg1").update(pubkey="ab"), "dg1")
    assert repo.run(base=base)[0] == 0


def test_town_mutant_a_value_outside_the_vocabulary_is_refused(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(town="nowhere"), "belam")
    rc, out = repo.run()
    assert rc == 1 and "outside the accepted vocabulary" in out, out


def test_town_a_value_in_the_ladder_towns_is_admitted(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(town="local-maxxing"), "belam")
    assert repo.run()[0] == 0


# ---- R3: anything unreadable is refused, never a pass --------------------------------------------
def test_R3_mutant_a_row_that_does_not_parse_at_tip_is_unread(repo):
    repo.write(f"{G}/posts.md", "---\nid: config:posts\ntype: config\nposts:\n  - {not json}\n---\n")
    repo.commit("belam", "broken")
    rc, out = repo.run()
    assert rc == 1 and out.startswith("R-land: unread (posts.md rows at"), out


def test_R3_mutant_no_vetoes_cell_at_base_is_unread(repo):
    repo.git("rm", "-q", f"{G}/vetoes.md")
    base = repo.commit("belam", "drop vetoes")
    repo.edit_rows(lambda r: row(r, "dg1").update(pid=7), "dg1")
    rc, out = repo.run(base=base)
    assert rc == 1 and out.startswith("R-land: unread (vetoes at"), out


def test_R3_mutant_no_config_schema_at_base_is_unread(repo):
    repo.git("rm", "-q", ".agi/context/schemas/[config].md")
    base = repo.commit("belam", "drop schema")
    rc, out = repo.run(base=base)
    assert rc == 1 and "unread (config schema" in out, out


def test_R3_mutant_a_bad_revision_is_unread(repo):
    rc, out = repo.run(base="deadbeefdeadbeef")
    assert rc == 1 and out.startswith("R-land: unread (BASE"), out


def test_R3_mutant_a_missing_ring_file_is_unread(repo):
    r = subprocess.run(["sh", str(SCRIPT), repo.base, "HEAD"], cwd=repo.d, capture_output=True, text=True,
                       env={**os.environ, "AGI_RING": str(repo.signers) + ".gone"})
    assert r.returncode == 1 and "unread (allowed_signers ring)" in r.stdout


def test_a_rows_cell_that_is_absent_at_both_ends_is_not_a_change(repo):
    repo.git("rm", "-q", f"{G}/posts.md")
    base = repo.commit("belam", "no posts")
    repo.write("x.txt", "1")
    repo.commit("belam", "noise")
    rc, out = repo.run(base=base)
    assert rc == 0, out


# ---- R4: the reference-transaction prepared phase (the third call site) ----------------------------
PIECE_SED = "/^### reference-transaction /,/^### /{/^~~~/,/^~~~/{//!p}}"


def _install_hook(repo, tmp_path, user="belam"):
    piece = subprocess.run(["sed", "-n", PIECE_SED, str(REPO / ".agi/nodes/.geometry/engine-post.md")],
                           capture_output=True, text=True, check=True).stdout
    assert "r-land" in piece
    hooks = repo.d / ".git" / "hooks"
    hooks.mkdir(exist_ok=True)
    (hooks / "reference-transaction").write_text(piece, encoding="utf-8")
    (hooks / "reference-transaction").chmod(0o755)
    stub = tmp_path / "stub"
    stub.mkdir()
    (stub / "id").write_text(f'#!/bin/sh\ncase "$*" in -un) echo {user};; *) exec /usr/bin/id "$@";; esac\n')
    (stub / "id").chmod(0o755)
    (stub / "agi-notice").write_text(f'#!/bin/sh\necho "$*" >> {tmp_path}/notices.log\nexit 0\n')   # the hook's fail-open / HOLD path calls it: log it, never write the tester's ~/.notice
    (stub / "agi-notice").chmod(0o755)
    # AGI_RLAND_SINCE: the stand-in for L140 (the hook's "pre-L140 base fails open" cut): the fixture's first commit
    return {"PATH": f"{stub}:{os.environ['PATH']}", "AGI_RING": str(repo.signers), "AGI_RLAND_SINCE": repo.base}


def _move(repo, ref, new, old, env):
    # an explicit hooksPath: a post's global gitconfig points core.hooksPath at ~/bin, which would hide .git/hooks
    return repo.git("-c", f"core.hooksPath={repo.d / '.git' / 'hooks'}", "update-ref", ref, new, old, env=env, check=False)


@pytest.fixture()
def hooked(tmp_path):
    repo = Repo(tmp_path)
    env = _install_hook(repo, tmp_path)
    return repo, env


def _branch_at(repo, name, sha):
    repo.git("-c", "core.hooksPath=/dev/null", "update-ref", name, sha)      # fixture setup, not a guarded move
    return sha


def test_R4_mutant_a_direct_commit_signed_by_a_non_prime_editing_another_row_cannot_move_posts_belam(hooked):
    repo, env = hooked
    _branch_at(repo, "refs/heads/posts/belam", repo.base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")      # signed dg1, no grant
    before = repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip()
    r = _move(repo, "refs/heads/posts/belam", bad, before, env)
    assert r.returncode != 0 and "[r-land] refs/heads/posts/belam refused" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == before      # the ref UNCHANGED


def test_R4_a_prime_signed_edit_moves_posts_belam(hooked):
    repo, env = hooked
    _branch_at(repo, "refs/heads/posts/belam", repo.base)
    good = repo.edit_rows(lambda r: row(r, "dg2").update(model="o/p"), "belam")
    assert _move(repo, "refs/heads/posts/belam", good, repo.base, env).returncode == 0


def test_R4_mutant_the_trunk_ref_is_guarded_too(hooked):
    repo, env = hooked
    _branch_at(repo, "refs/heads/core/season3/main", repo.base)
    bad = repo.edit_rows(lambda r: row(r, "belam").update(model="evil"), "dg1", author="belam")
    r = _move(repo, "refs/heads/core/season3/main", bad, repo.base, env)
    assert r.returncode != 0 and "[r-land] refs/heads/core/season3/main refused" in r.stderr, r.stderr


def test_R4_other_refs_and_unchanged_cells_are_not_touched_by_r_land(hooked):
    repo, env = hooked
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    assert _move(repo, "refs/heads/posts/dg1", bad, "0" * 40, env).returncode == 0           # not a guarded ref
    repo.write("note.txt", "n")
    plain = repo.commit("belam", "no config change")
    _branch_at(repo, "refs/heads/posts/belam", bad)
    assert _move(repo, "refs/heads/posts/belam", plain, bad, env).returncode == 0            # cells equal o..n: nothing to judge


def test_V2_5_a_pre_L140_base_with_no_r_land_fails_open_with_a_notice(hooked):
    repo, env = hooked
    repo.git("rm", "-q", "extensions/agi/guard/r-land")
    old = repo.commit("belam", "drop r-land")
    _branch_at(repo, "refs/heads/posts/belam", old)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    env = {**env, "AGI_RLAND_SINCE": bad}          # a BASE that does not descend the cut = a pre-L140 base: the one fail-open
    r = _move(repo, "refs/heads/posts/belam", bad, old, env)
    assert r.returncode == 0 and "no r-land at" in r.stderr and "fail open" in r.stderr, r.stderr


def test_R5_a_core_hookspath_bypass_still_moves_the_ref_so_nobody_reads_the_hook_as_a_wall(hooked):
    repo, env = hooked
    _branch_at(repo, "refs/heads/posts/belam", repo.base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = repo.git("-c", "core.hooksPath=/dev/null", "update-ref", "refs/heads/posts/belam", bad, repo.base, env=env, check=False)
    assert r.returncode == 0                      # R5: a hook guards against MISTAKES, it is not a wall


# ---- MODE: report | enforce, ONE cell read from BASE ------------------------------------------------
def test_MODE_report_prints_would_refuse_with_signer_row_op_cells_and_rule_rc_0(repo):
    base = repo.set_mode("report")
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run(base=base)
    line = next(x for x in out.splitlines() if x.startswith("R-land: would refuse "))
    assert rc == 0 and "(dg1, dg2, set pubkey, " in line and "(R2)" in line, out
    assert out.splitlines()[-1].startswith("R-land: report (1 cell change(s)") and "1 would refuse" in out, out


def test_MODE_report_mutant_a_non_prime_direct_commit_prints_the_line_and_a_clean_range_still_says_ok(repo):
    base = repo.set_mode("report")
    rc, out = repo.run(base=base)
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)") and out.endswith("mode report; 0 row op(s))"), out
    repo.edit_rows(lambda r: row(r, "belam").update(model="evil"), "dg1", author="belam")
    rc, out = repo.run(base=base)
    assert rc == 0 and "R-land: would refuse" in out and "(dg1, belam, set model," in out, out


def test_MODE_report_an_unsigned_commit_prints_the_R1_line_rc_0(repo):
    base = repo.set_mode("report")
    repo.edit_rows(lambda r: row(r, "dg1").update(pid=3), "intruder", author="dg1")
    rc, out = repo.run(base=base)
    assert rc == 0 and "would refuse" in out and "(nobody," in out and "(R1)" in out, out


def test_MODE_report_an_unread_prints_the_same_way_never_silent_rc_0(repo):
    base = repo.set_mode("report")
    repo.write(f"{G}/posts.md", "---\nid: config:posts\ntype: config\nposts:\n  - {not json}\n---\n")
    repo.commit("belam", "broken")
    rc, out = repo.run(base=base)
    assert rc == 0 and out.startswith("R-land: would refuse ") and "(unread posts.md rows at" in out, out


def test_MODE_enforce_mutant_the_same_violation_is_rc_1(repo):
    base = repo.set_mode("enforce")
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run(base=base)
    assert rc == 1 and out.startswith("R-land: refused "), out


def test_MODE_is_read_from_BASE_never_TIP_a_range_cannot_soften_its_own_judge(repo):
    base = repo.set_mode("enforce")
    repo.set_mode("report", signer="dg1")                       # the tip flips the cell ...
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")    # ... and violates in the same range
    rc, out = repo.run(base=base)
    assert rc == 1 and "R-land: refused" in out, out


def test_MODE_absent_at_BASE_is_report_and_says_so(repo):
    base = repo.set_mode(None)
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run(base=base)
    assert rc == 0 and out.startswith("R-land: mode report (r_land.mode absent at") and "would refuse" in out, out


def test_MODE_mutant_neither_word_is_unread_and_fails_closed(repo):
    base = repo.set_mode("warn")
    rc, out = repo.run(base=base)
    assert rc == 1 and out.startswith("R-land: unread (r_land.mode at"), out


def test_MODE_mutant_an_unreadable_schema_fails_closed_even_though_report_would_pass(repo):
    repo.git("rm", "-q", ".agi/context/schemas/[config].md")
    base = repo.commit("belam", "drop schema")
    rc, out = repo.run(base=base)
    assert rc == 1 and "unread (config schema" in out, out      # the mode itself is unknowable -> enforce


def test_MODE_report_R4_a_non_prime_direct_commit_prints_the_line_and_the_ref_MOVES(hooked):
    repo, env = hooked
    base = repo.set_mode("report")
    _branch_at(repo, "refs/heads/posts/belam", base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")      # signed dg1, no grant
    r = _move(repo, "refs/heads/posts/belam", bad, base, env)
    assert r.returncode == 0 and "[r-land] refs/heads/posts/belam moves (report mode)" in r.stderr, r.stderr
    assert "R-land: would refuse" in r.stderr and "(dg1, dg2, set pubkey," in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == bad            # the ref MOVED


def test_MODE_enforce_R4_the_same_commit_leaves_the_ref_UNCHANGED(hooked):
    repo, env = hooked
    base = repo.set_mode("enforce")
    _branch_at(repo, "refs/heads/posts/belam", base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = _move(repo, "refs/heads/posts/belam", bad, base, env)
    assert r.returncode != 0 and "refused, nothing changed" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == base           # the ref UNCHANGED


# ---- MODE before RING: a ringless uid is report-mode rc 0 (council 3/3 00:44Z 10-26, GATE259 return) -------------
NORING = "/nonexistent/allowed_signers"


def test_MODE_report_mutant_a_ringless_uid_on_a_row_changing_range_prints_would_refuse_rc_0(repo):
    base = repo.set_mode("report")
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run(base=base, ring=NORING)
    assert rc == 0 and out.startswith("R-land: would refuse ") and out.endswith("(unread allowed_signers ring)"), out


def test_MODE_enforce_mutant_the_same_ringless_range_is_rc_1(repo):
    base = repo.set_mode("enforce")
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    rc, out = repo.run(base=base, ring=NORING)
    assert rc == 1 and out == "R-land: unread (allowed_signers ring)", out


def test_MODE_enforce_a_ringless_uid_is_unread_even_on_a_range_with_no_cell_change(repo):
    base = repo.set_mode("enforce")
    rc, out = repo.run(base=base, ring=NORING)
    assert rc == 1 and "unread (allowed_signers ring)" in out, out


def test_MODE_report_a_ringless_uid_on_a_range_with_no_cell_change_needs_no_ring_and_says_ok(repo):
    base = repo.set_mode("report")
    repo.write("note.txt", "x")
    repo.commit("dg1", "not a config change")
    rc, out = repo.run(base=base, ring=NORING)
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)") and "would refuse" not in out, out


def test_MODE_report_the_one_rc_1_is_a_BASE_or_TIP_that_does_not_rev_parse_even_ringless(repo):
    repo.set_mode("report")
    rc, out = repo.run(base="deadbeefdeadbeef", ring=NORING)       # runs before the mode is known: fail closed
    assert rc == 1 and out.startswith("R-land: unread (BASE"), out
    rc, out = repo.run(tip="deadbeefdeadbeef", ring=NORING)
    assert rc == 1 and out.startswith("R-land: unread (TIP"), out


def test_MODE_report_R4_a_ringless_uid_on_a_row_changing_ff_the_ref_MOVES_with_the_would_refuse_line(hooked):
    repo, env = hooked
    base = repo.set_mode("report")
    _branch_at(repo, "refs/heads/posts/belam", base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = _move(repo, "refs/heads/posts/belam", bad, base, {**env, "AGI_RING": NORING})
    assert r.returncode == 0 and "[r-land] refs/heads/posts/belam moves (report mode)" in r.stderr, r.stderr
    assert "R-land: would refuse" in r.stderr and "(unread allowed_signers ring)" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == bad            # the ref MOVED


def test_MODE_enforce_R4_a_ringless_uid_on_the_same_ff_leaves_the_ref_UNCHANGED(hooked):
    repo, env = hooked
    base = repo.set_mode("enforce")
    _branch_at(repo, "refs/heads/posts/belam", base)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = _move(repo, "refs/heads/posts/belam", bad, base, {**env, "AGI_RING": NORING})
    assert r.returncode != 0 and "refused, nothing changed" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == base           # the ref UNCHANGED


# ---- MODE before every other cell: the mode lives in the SCHEMA (council 3/3 01:58Z 10-26, GATE264 RETURN 2) ----------
def _break_cell(repo, cell, how):
    if how == "absent":
        repo.git("rm", "-q", f"{G}/{cell}")
    elif how == "not-a-mapping":
        repo.write(f"{G}/{cell}", "---\n- just\n- a list\n---\n")
    elif how == "bad-yaml":
        repo.write(f"{G}/{cell}", "---\nkey: [unclosed\n---\n")
    return repo.commit("belam", f"{cell} {how}")


@pytest.mark.parametrize("cell", ["ladder.md", "vetoes.md"])
@pytest.mark.parametrize("how", ["absent", "not-a-mapping", "bad-yaml"])
def test_MODE_report_mutant_a_broken_vetoes_or_ladder_at_BASE_is_would_refuse_rc_0(repo, cell, how):
    repo.set_mode("report")
    base = _break_cell(repo, cell, how)
    rc, out = repo.run(base=base)
    assert rc == 0 and out.startswith("R-land: would refuse ") and "(unread " in out, (rc, out)
    assert cell.split(".")[0] in out or "vetoes/ladder" in out, out


@pytest.mark.parametrize("cell", ["ladder.md", "vetoes.md"])
def test_MODE_enforce_mutant_the_same_broken_cell_is_rc_1(repo, cell):
    repo.set_mode("enforce")
    base = _break_cell(repo, cell, "not-a-mapping")
    rc, out = repo.run(base=base)
    assert rc == 1 and out.startswith("R-land: unread ("), (rc, out)


@pytest.mark.parametrize("how", ["not-a-mapping", "bad-yaml"])
def test_MODE_the_schema_is_the_modes_own_home_unparseable_fails_closed_even_though_it_could_say_report(repo, how):
    repo.write(".agi/context/schemas/[config].md", "---\n- a list\n---\n" if how == "not-a-mapping" else "---\nk: [x\n---\n")
    base = repo.commit("belam", "schema " + how)
    rc, out = repo.run(base=base)
    assert rc == 1 and out.startswith("R-land: unread (yaml frontmatter of the schema at "), (rc, out)


def test_MODE_report_R4_a_broken_ladder_at_the_old_tip_the_ref_MOVES_with_the_line_and_the_FIX_commit_lands(hooked):
    repo, env = hooked
    repo.set_mode("report")
    broken = _break_cell(repo, "ladder.md", "not-a-mapping")
    _branch_at(repo, "refs/heads/posts/belam", broken)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = _move(repo, "refs/heads/posts/belam", bad, broken, env)
    assert r.returncode == 0 and "[r-land] refs/heads/posts/belam moves (report mode)" in r.stderr, r.stderr
    assert "R-land: would refuse" in r.stderr and "(unread " in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == bad
    # the lockout shape: the commit that FIXES the cell is judged by the broken BASE and must still move the ref
    repo.write(f"{G}/ladder.md", LADDER)
    fix = repo.commit("belam", "fix ladder")
    r = _move(repo, "refs/heads/posts/belam", fix, bad, env)
    assert r.returncode == 0, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == fix


def test_MODE_enforce_R4_a_broken_ladder_at_the_old_tip_the_ref_stays_UNCHANGED(hooked):
    repo, env = hooked
    repo.set_mode("enforce")
    broken = _break_cell(repo, "ladder.md", "not-a-mapping")
    _branch_at(repo, "refs/heads/posts/belam", broken)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
    r = _move(repo, "refs/heads/posts/belam", bad, broken, env)
    assert r.returncode != 0 and "refused, nothing changed" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == broken


# ---- MOVE GRANT: `name_suffix` + `move_of` (owner "Accept both" 05:0xZ 10-26, council 3/3 alive 05:20:59Z) -------------------
MOVE_GRANT = '  - {actor: master, list_key: posts, match_key: name, ops: [create], name_suffix: "-retired", move_of: "<x>"}\n'


def with_move_grant(repo, grant=MOVE_GRANT, signer="belam", mode="enforce"):
    """Commit a schema whose actor_rows carries the move grant (or another line) as the new BASE."""
    anchor = "town_cell:"
    t = SCHEMA.replace(anchor, grant + anchor, 1).replace("r_land: {mode: enforce}", f"r_land: {{mode: {mode}}}")
    repo.write(".agi/context/schemas/[config].md", t)
    repo.base = repo.commit(signer, "move grant")
    return repo


def move(rows, x="dg1", keep_x=False, **over):
    """The shape of a real `<x>` -> `<x>-retired` commit: <x> gone, the copy at its retired process-cell values."""
    src = row(rows, x)
    if not keep_x:
        rows.remove(src)
    rows.append({**src, "name": f"{x}-retired", "session_label": f"{x}-retired", "box": "off", "pid": 0, **over})


def test_MOVE_master_moves_a_row_to_its_retired_copy_admitted(repo):
    with_move_grant(repo)
    repo.edit_rows(lambda r: move(r), "master")
    rc, out = repo.run()
    assert rc == 0 and "ok (1 cell change(s)" in out and "2 row op(s): 1 retire, 1 create" in out, out


def test_ROWOPS_two_moves_in_one_cell_file_read_as_4_row_ops_not_1_change(repo):
    """7c1ef3664f shape: two `<x>` -> `<x>-retired` moves in ONE posts.md change = 1 cell change, 4 row ops (council 09:23Z 10-26)."""
    with_move_grant(repo)
    repo.edit_rows(lambda r: (move(r, "dg1"), move(r, "dg2")), "master")
    rc, out = repo.run()
    assert rc == 0 and "ok (1 cell change(s)" in out and "4 row op(s): 2 retire, 2 create" in out, out


def test_ROWOPS_a_set_only_change_counts_one_set_op(repo):
    repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "belam")
    rc, out = repo.run()
    assert rc == 0 and "1 row op(s): 1 set" in out, out


def test_ROWOPS_the_report_line_names_the_row_ops_too(repo):
    with_move_grant(repo, mode="report")
    repo.edit_rows(lambda r: (move(r), row(r, "dg2").update(pubkey="zz")), "dg2")      # dg2 holds no grant: the move (retire + create) would refuse, its own pubkey set is a self_row write
    rc, out = repo.run()
    assert rc == 0 and "2 would refuse; 3 row op(s): 1 retire, 1 create, 1 set; rc 0" in out, out


def test_MOVE_the_same_commit_without_the_grant_at_BASE_is_refused(repo):
    repo.edit_rows(lambda r: move(r), "master")
    rc, out = repo.run()
    assert rc == 1 and "dg1-retired" in out and "needs a written_by role or an actor_rows grant" in out, out


def test_MOVE_a_signer_the_grant_does_not_name_is_refused(repo):
    with_move_grant(repo)
    repo.edit_rows(lambda r: move(r), "dg2")
    rc, out = repo.run()
    assert rc == 1 and "dg1-retired" in out, out


@pytest.mark.parametrize("why,over,keep_x,marker", [
    ("a lone -retired while <x> stays live", {}, True, "is still live"),
    ("a changed pubkey", {"pubkey": "bb"}, False, "cells pubkey differ"),
    ("a changed key_history", {"key_history": [{"pub": "x"}]}, False, "cells key_history differ"),
    ("a changed role", {"role": "prime_director"}, False, "cells role differ"),
    ("box not off", {"box": "local-town"}, False, "process cells"),
    ("recover true", {"recover": True}, False, "process cells"),
    ("pid not 0", {"pid": 5}, False, "process cells"),
    ("a live window", {"window": "@1"}, False, "process cells"),
    ("a worktree", {"worktree": ".agi/worktrees/x"}, False, "process cells"),
    ("a session_name", {"session_name": "s"}, False, "process cells"),
    ("boot not null", {"boot": True}, False, "process cells"),
    ("session_label not the name", {"session_label": "dg1"}, False, "session_label must equal"),
])
def test_MOVE_mutant_each_broken_condition_is_refused_naming_the_rule(repo, why, over, keep_x, marker):
    with_move_grant(repo)
    repo.edit_rows(lambda r: move(r, keep_x=keep_x, **over), "master")
    rc, out = repo.run()
    assert rc == 1 and marker in out and "(move_of)" in out, (why, out)


def test_MOVE_mutant_x_absent_at_the_parent_is_unread_and_refused(repo):
    with_move_grant(repo)

    def ghost(rows):
        rows.append({"name": "ghost-retired", "session_label": "ghost-retired", "box": "off", "pid": 0, "role": "director"})
    repo.edit_rows(ghost, "master")
    rc, out = repo.run()
    assert rc == 1 and "unread (ghost at " in out, out


def test_MOVE_the_grant_is_not_a_field_grant_a_set_on_a_retired_row_is_judged_as_before(repo):
    with_move_grant(repo)
    repo.edit_rows(lambda r: move(r), "master")
    repo.base = repo.git("rev-parse", "HEAD").stdout.strip()
    rows = json.loads(json.dumps(ROWS))
    move(rows)
    row(rows, "dg1-retired").update(pubkey="zz")
    repo.write(f"{G}/posts.md", _posts(rows))
    repo.commit("master", "set pubkey on the retired row")
    rc, out = repo.run()
    assert rc == 1 and "dg1-retired" in out and "set pubkey" in out, out


def test_MOVE_a_move_of_other_than_the_placeholder_is_not_honoured(repo):
    with_move_grant(repo, grant=MOVE_GRANT.replace('"<x>"', '"dg1"'))
    repo.edit_rows(lambda r: move(r), "master")
    rc, out = repo.run()
    assert rc == 1 and "needs a written_by role or an actor_rows grant" in out, out


def test_MOVE_report_mode_prints_the_would_refuse_line_with_the_rule_and_rc_0(repo):
    with_move_grant(repo, mode="report")
    repo.edit_rows(lambda r: move(r, pubkey="bb"), "master")
    rc, out = repo.run()
    assert rc == 0 and "would refuse" in out and "cells pubkey differ" in out, out


def test_MOVE_a_suffix_grant_that_also_lists_fields_is_never_a_plain_field_grant(repo):
    g = '  - {actor: dg2, list_key: posts, match_key: name, ops: [create], fields: [town], name_suffix: "-retired", move_of: "<x>"}\n'
    with_move_grant(repo, grant=g)

    def fresh(rows):
        rows.append({"name": "fresh", "town": "core"})
    repo.edit_rows(fresh, "dg2")
    rc, out = repo.run()
    assert rc == 1 and "fresh" in out and "needs a written_by role or an actor_rows grant" in out, out


# ---- council [correction]s 05:39:16Z / 05:40:12Z / 05:40:26Z 10-26 to the falsifier: b737cef238 is the NEGATIVE control, and its exact
# cell changes (pid, window, recover absent -> false) are the ADMITTED fixture, because 7c1ef3664f never changes those three ----------
BELAM_X = {"name": "director-belam", "role": "director", "tier": 1, "harness": "claude-code", "model": "claude-sonnet-5", "effort": "high",
           "settings": "", "session_kind": "remote-control", "personality_ref": "", "handoff_file": "",
           "pin_ref": ".agi/sessions/sanctuary-director.meter", "rotated_by": "sanctuary-master", "owning_goal": "",
           "worktree": ".agi/worktrees/post-sanctuary-director", "session_ref": "", "session_id": "446773a7-cd37-4d57-9614-cf841ea0e4b5",
           "window": "@466", "pid": 2783249, "town": "sanctuary", "pubkey": "f7d004317613f5dce92f672c219e4f61825fdc738f7af0b4d0b342ae1bfd9461",
           "sig_scheme": "ed25519", "enc_scheme": "none", "key_history": [{"pub": "310a45d5", "fp": "7be65ab8", "from": 20, "to": 21}],
           "box": "core-town", "session_name": "post-sanctuary-director-59", "session_label": "director-belam"}   # no `recover` cell: absent at the source


def b737_shape(repo):
    """BASE carries director-belam as it stood before b737cef238; the returned fn is that commit's exact change to posts.md."""
    rows = json.loads(json.dumps(ROWS)) + [json.loads(json.dumps(BELAM_X))]
    repo.write(f"{G}/posts.md", _posts(rows))
    repo.base = repo.commit("belam", "base with director-belam")

    def fn(rs):
        src = next(r for r in rs if r["name"] == "director-belam")
        rs.remove(src)
        rs.append({**src, "name": "director-belam-retired", "session_label": "director-belam-retired", "box": "off", "pid": 0,
                   "window": "", "recover": False, "session_name": "", "worktree": "", "boot": None})
    return rows, fn


def edit_from(repo, rows, fn, signer):
    rows = json.loads(json.dumps(rows))
    fn(rows)
    repo.write(f"{G}/posts.md", _posts(rows))
    return repo.commit(signer, "b737cef238 shape")


def test_MOVE_iii_the_b737cef238_diff_signed_by_the_grants_actor_is_ADMITTED_pid_window_recover_take_the_fixed_values(repo):
    with_move_grant(repo)
    rows, fn = b737_shape(repo)
    edit_from(repo, rows, fn, "master")
    rc, out = repo.run()
    assert rc == 0 and "ok (1 cell change(s)" in out, out


def test_MOVE_ii_NEGATIVE_CONTROL_the_same_diff_signed_by_a_signer_the_grant_does_not_name_stays_REFUSED(repo):
    with_move_grant(repo)
    rows, fn = b737_shape(repo)
    edit_from(repo, rows, fn, "dg2")      # b737cef238's signer was director-general-3: not the grant's actor
    rc, out = repo.run()
    assert rc == 1 and "director-belam-retired" in out and "needs a written_by role or an actor_rows grant" in out, out


@pytest.mark.parametrize("cell,value", [("pid", 2783249), ("window", "@466"), ("recover", True)])
def test_MOVE_iii_mutant_a_process_cell_kept_at_BASE_s_live_value_is_REFUSED(repo, cell, value):
    with_move_grant(repo)
    rows, fn = b737_shape(repo)

    def keep(rs):
        fn(rs)
        next(r for r in rs if r["name"] == "director-belam-retired")[cell] = value
    edit_from(repo, rows, keep, "master")
    rc, out = repo.run()
    assert rc == 1 and "process cells" in out, out


# ---- W: written_by (council 3/3 alive 02:53:20Z + 02:54:27Z 10-26): moral/vision/town per-commit signer, config by its LANDER ----
SCH = "---\nname: {n}\nwritten_by: {w}\n---\n# {n}\n"
NODE = "---\nid: {t}:{n}\ntype: {t}\n---\n# {t}:{n}\n{b}\n"
WB_FILES = {
    "moral": (".agi/nodes/moral/m1.md", "owner"),
    "vision": (".agi/nodes/vision/v1.md", "[owner, prime_director]"),
    "town": (".agi/nodes/town/t1.md", "[prime_director, owner, director]"),
    "config": (f"{G}/rotations.md", None),                       # the config schema is the fixture's [config].md
    "doc": (".agi/nodes/doc/d1.md", None),                       # a type with NO written_by: never judged
}


@pytest.fixture()
def wb(tmp_path):
    repo = Repo(tmp_path)
    repo.write(".agi/context/schemas/[moral].md", SCH.format(n="moral", w="owner"))
    repo.write(".agi/context/schemas/[vision].md", SCH.format(n="vision", w="[owner, prime_director]"))
    repo.write(".agi/context/schemas/[town].md", SCH.format(n="town", w="[prime_director, owner, director]"))
    for typ, (rel, _w) in WB_FILES.items():
        repo.write(rel, NODE.format(t=typ, n=rel.rsplit("/", 1)[-1][:-3], b="v0"))
    repo.set_mode("report")
    repo.base = repo.git("rev-parse", "HEAD").stdout.strip()
    return repo


def _edit(repo, typ, signer, body="v1"):
    rel = WB_FILES[typ][0]
    repo.write(rel, NODE.format(t=typ, n=rel.rsplit("/", 1)[-1][:-3], b=body))
    return repo.commit(signer, f"edit {typ} {body}")


def _leaf(repo, name, typ, signer, body="leaf"):
    """A leaf commit on branch `name` cut from main's tip; back on main afterwards."""
    repo.git("checkout", "-q", "-b", name)
    c = _edit(repo, typ, signer, body)
    repo.git("checkout", "-q", "main")
    return c


def _land(repo, branch, signer, msg="LAND stack"):
    env = {"GIT_COMMITTER_EMAIL": f"{signer}@agi", "GIT_COMMITTER_NAME": signer,
           "GIT_AUTHOR_EMAIL": f"{signer}@agi", "GIT_AUTHOR_NAME": signer}
    repo.git("-c", f"user.signingkey={repo.k / signer}", "merge", "--no-ff", "-q", "-m", msg, branch, env=env)
    return repo.git("rev-parse", "HEAD").stdout.strip()


def test_W1_mutant_a_director_signed_moral_edit_would_refuse_written_by_owner(wb):
    _edit(wb, "moral", "dg1")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "(dg1, " in out and "m1.md, set moral, written_by: owner; signer role director (W1))" in out, out
    assert "R-land: would refuse" in out and out.splitlines()[-1].startswith("R-land: report (0 cell change(s)")


def test_W1_mutant_a_director_signed_vision_edit_would_refuse_and_the_prime_s_edit_passes(wb):
    _edit(wb, "vision", "dg1")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "v1.md, set vision, written_by: owner, prime_director; signer role director (W1))" in out, out
    wb2 = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "vision", "belam", body="v2")
    rc, out = wb.run(base=wb2)
    assert rc == 0 and "(W1)" not in out and out.startswith("R-land: ok (0 cell change(s)"), out


def test_W1_town_per_commit_signer_a_director_is_admitted_a_kid_is_not(wb):
    _edit(wb, "town", "dg1")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "(W1)" not in out, out
    mid = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "town", "kid", body="v2")
    rc, out = wb.run(base=mid)
    assert rc == 0 and "(kid, " in out and "written_by: prime_director, owner, director; signer role kid (W1))" in out, out


def test_W1_a_type_with_no_written_by_is_never_judged_and_enforce_makes_a_refusal_rc_1(wb):
    _edit(wb, "doc", "kid")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)"), out
    wb.set_mode("enforce")
    base2 = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "moral", "dg1")
    rc, out = wb.run(base=base2)
    assert rc == 1 and "R-land: refused " in out and "(W1)" in out, out


def test_W2_mutant_a_director_signed_config_leaf_ffd_directly_would_refuse_and_the_prime_s_passes(wb):
    _edit(wb, "config", "dg1")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "rotations.md, set config, written_by: owner, prime_director; direct lander role director (W2))" in out, out
    assert "lander not provable" not in out
    mid = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "config", "belam", body="v2")
    rc, out = wb.run(base=mid)
    assert rc == 0 and "(W2)" not in out, out


def test_W3_the_same_leaf_under_a_land_merge_signed_by_a_written_by_role_is_ok_with_no_line(wb):
    _leaf(wb, "leaf1", "config", "dg1")
    _land(wb, "leaf1", "belam")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "(W2)" not in out and "lander not provable" not in out and "R1" not in out, out


def test_W3b_a_RULES_land_by_SM_under_belams_WRAP_is_ok_no_lander_not_provable_line_and_the_same_L_plain_ffd_is_not(wb):
    """The council WRAP (verify-land wrap): W = commit-tree(L^{tree}, parents [trunk, L]) signed belam over L signed by SM.
    belam holds a written_by role, so the config change is provable (positive row); L ff'd plain is the W2 line (negative row)."""
    base = wb.base
    L = _leaf(wb, "L", "config", "master")
    rc, out = wb.run(base=base, tip=L)
    assert rc == 0 and "direct lander role director (W2))" in out, out                      # plain ff of SM's L: not provable
    env = {"GIT_COMMITTER_EMAIL": "belam@agi", "GIT_COMMITTER_NAME": "belam", "GIT_AUTHOR_EMAIL": "belam@agi", "GIT_AUTHOR_NAME": "belam"}
    W = wb.git("-c", f"user.signingkey={wb.k / 'belam'}", "commit-tree", "-S", f"{L}^{{tree}}", "-p", base, "-p", L,
               "-m", "LAND wrap", env=env).stdout.strip()
    assert wb.git("rev-parse", f"{W}^{{tree}}").stdout.strip() == wb.git("rev-parse", f"{L}^{{tree}}").stdout.strip()
    assert wb.git("rev-list", "--parents", "-n1", W).stdout.split()[1:] == [base, L]
    rc, out = wb.run(base=base, tip=W)
    assert rc == 0 and "R-land: ok (" in out, out
    assert "(W2)" not in out and "lander not provable" not in out and "R1" not in out and "would refuse" not in out, out


def test_W4_a_land_merge_signed_by_a_director_prints_ONE_collapsed_line_with_count_and_leaf_signers_never_a_would_refuse(wb):
    _leaf(wb, "leaf1", "config", "dg1")
    _land(wb, "leaf1", "master")
    rc, out = wb.run(base=wb.base)
    assert rc == 0, out
    line = next(x for x in out.splitlines() if "lander not provable" in x)
    assert line == ("R-land: config: lander not provable in history (RULES via unsigned ff): 1 change(s); "
                    "leaf signers: dg1 x1"), line
    assert not any(x.startswith("R-land: would refuse") for x in out.splitlines()), out


def test_W5_mutant_an_unringed_config_leaf_inside_a_director_land_prints_R1_BESIDE_the_collapsed_line(wb):
    _leaf(wb, "leaf1", "config", "intruder")
    _land(wb, "leaf1", "master")
    rc, out = wb.run(base=wb.base)
    assert rc == 0, out
    assert any("(nobody, " in x and "(R1))" in x and x.startswith("R-land: would refuse") for x in out.splitlines()), out
    assert any("lander not provable" in x for x in out.splitlines()), out


def test_W6_a_leaf_signed_by_a_renamed_seat_is_counted_in_the_collapsed_line_no_c_line(wb):
    _leaf(wb, "leaf1", "config", "old")                       # the row is 'newname', was: old
    _land(wb, "leaf1", "master")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and "(c))" not in out and "leaf signers: old x1" in out, out


def test_W7_mutant_a_leaf_signed_by_a_key_in_no_row_and_no_was_prints_the_c_line(wb):
    _leaf(wb, "leaf1", "config", "ghost")
    _land(wb, "leaf1", "master")
    rc, out = wb.run(base=wb.base)
    assert rc == 0, out
    assert any(x.startswith("R-land: would refuse") and "(ghost, " in x and "(c))" in x for x in out.splitlines()), out
    assert any("lander not provable" in x for x in out.splitlines()), out


def test_W8_mutant_an_unringed_lander_is_the_R1_line_never_lander_ok(wb):
    _leaf(wb, "leaf1", "config", "belam")
    _land(wb, "leaf1", "intruder")
    rc, out = wb.run(base=wb.base)
    assert rc == 0 and any("(nobody, " in x and "(R1))" in x for x in out.splitlines()), out
    assert "lander not provable" not in out


def test_W9_enforce_keeps_the_collapsed_line_informational_rc_0_while_a_W2_line_is_rc_1(wb):
    wb.set_mode("enforce")
    base2 = wb.git("rev-parse", "HEAD").stdout.strip()
    _leaf(wb, "leaf1", "config", "dg1")
    _land(wb, "leaf1", "master")
    rc, out = wb.run(base=base2)
    assert rc == 0 and "lander not provable" in out, out
    mid = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "config", "dg1", body="v9")
    rc, out = wb.run(base=mid)
    assert rc == 1 and "R-land: refused " in out and "(W2)" in out, out


def test_W10_a_node_change_with_the_ring_unread_is_the_mode_aware_unread(wb):
    _edit(wb, "moral", "dg1")
    rc, out = wb.run(base=wb.base, ring="/nonexistent/allowed_signers")
    first = out.splitlines()[0]
    assert rc == 0 and first.startswith("R-land: would refuse ") and first.endswith("(unread allowed_signers ring)"), out
    assert out.splitlines()[-1].startswith("R-land: report (0 cell change(s)") and "1 would refuse" in out, out


def test_W11_mutant_an_unparseable_moral_schema_at_BASE_is_the_mode_aware_unread(wb):
    wb.write(".agi/context/schemas/[moral].md", "---\n- a list\n---\n")
    base2 = wb.commit("belam", "break moral schema")
    _edit(wb, "moral", "belam")
    rc, out = wb.run(base=base2)
    assert rc == 0 and "R-land: would refuse " in out and "(unread schema .agi/context/schemas/[moral].md at " in out, out
    wb.set_mode("enforce")
    base3 = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "moral", "belam", body="v3")
    rc, out = wb.run(base=base3)
    assert rc == 1 and "R-land: unread (schema .agi/context/schemas/[moral].md at " in out, out


def _stub_id(tmp_path, body):
    tmp_path.mkdir(parents=True, exist_ok=True)
    stub = tmp_path / "idstub"
    stub.mkdir(parents=True, exist_ok=True)
    (stub / "id").write_text(f"#!/bin/sh\n{body}\n")
    (stub / "id").chmod(0o755)
    return str(stub)


def _run_as(wb, tmp_path, name, id_body, env_extra=None, base=None):
    stub = _stub_id(tmp_path / name, id_body)
    r = subprocess.run(["sh", str(SCRIPT), base or wb.base, "HEAD"], cwd=wb.d, capture_output=True, text=True,
                       env={**os.environ, "AGI_RING": str(wb.signers), "PATH": f"{stub}:{os.environ['PATH']}", **(env_extra or {})})
    return r.returncode, r.stdout


ID_SM = 'case "$*" in -un) echo agi-master;; -u) echo 982;; *) exec /usr/bin/id "$@";; esac'
ID_BELAM = 'case "$*" in -un) echo agi-belam;; -u) echo 981;; *) exec /usr/bin/id "$@";; esac'


def test_RANAS_M1_is_the_process_uid_never_AGI_POST_and_prints_only_beside_a_config_judgement(wb, tmp_path):
    _edit(wb, "config", "dg1")
    rc, out = _run_as(wb, tmp_path, "a", ID_SM, {"AGI_POST": "belam"})
    assert "R-land: ran as master (user agi-master, uid 982)" in out and "ran as belam" not in out, out


def test_RANAS_M2_informational_only_two_uids_the_same_verdict_lines_and_rc(wb, tmp_path):
    _edit(wb, "config", "dg1")
    rc1, o1 = _run_as(wb, tmp_path, "a", ID_SM)
    rc2, o2 = _run_as(wb, tmp_path, "b", ID_BELAM)
    strip = lambda o: [x for x in o.splitlines() if not x.startswith("R-land: ran as")]
    assert rc1 == rc2 == 0 and strip(o1) == strip(o2) and "ran as master" in o1 and "ran as belam" in o2


def test_RANAS_M3_an_id_failure_prints_unread_and_never_changes_the_rc(wb, tmp_path):
    _edit(wb, "config", "dg1")
    rc, out = _run_as(wb, tmp_path, "a", "exit 1")
    assert rc == 0 and "R-land: ran as: unread (uid ?; no name)" in out, out
    rc, out = _run_as(wb, tmp_path, "b", 'case "$*" in -un) exit 1;; -u) echo 4242;; *) exec /usr/bin/id "$@";; esac')
    assert rc == 0 and "R-land: ran as: unread (uid 4242; no name)" in out, out
    rc, out = _run_as(wb, tmp_path, "c", 'case "$*" in -un) echo agi-nobody-here;; -u) echo 7;; *) exec /usr/bin/id "$@";; esac')
    assert rc == 0 and "R-land: ran as: unread (user agi-nobody-here, uid 7; no seat row of that name)" in out, out


def test_RANAS_is_not_printed_when_no_config_node_changed(wb, tmp_path):
    _edit(wb, "town", "dg1")
    rc, out = _run_as(wb, tmp_path, "a", ID_SM)
    assert "ran as" not in out, out


def test_W_R4_a_director_signed_config_leaf_ffd_onto_posts_belam_in_report_the_ref_MOVES_with_the_line_enforce_UNCHANGED(tmp_path):
    repo = Repo(tmp_path)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v0"))
    repo.write(".agi/context/schemas/[moral].md", SCH.format(n="moral", w="owner"))
    repo.set_mode("report")
    env = _install_hook(repo, tmp_path)
    base = repo.git("rev-parse", "HEAD").stdout.strip()
    _branch_at(repo, "refs/heads/posts/belam", base)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v1"))
    bad = repo.commit("dg1", "director edits config directly")
    r = _move(repo, "refs/heads/posts/belam", bad, base, env)
    assert r.returncode == 0 and "(W2)" in r.stderr and "R-land: ran as " in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == bad
    repo.set_mode("enforce")
    base2 = repo.git("rev-parse", "HEAD").stdout.strip()
    _branch_at(repo, "refs/heads/posts/belam", base2)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v2"))
    bad2 = repo.commit("dg1", "director edits config directly again")
    r = _move(repo, "refs/heads/posts/belam", bad2, base2, env)
    assert r.returncode != 0 and "refused, nothing changed" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == base2


def test_W12_a_node_change_of_a_type_without_written_by_needs_no_ring_in_either_mode(wb):
    _edit(wb, "doc", "kid")
    rc, out = wb.run(base=wb.base, ring="/nonexistent/allowed_signers")
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)"), out
    wb.set_mode("enforce")
    base2 = wb.git("rev-parse", "HEAD").stdout.strip()
    _edit(wb, "doc", "kid", body="v2")
    rc, out = wb.run(base=base2, ring="/nonexistent/allowed_signers")
    assert rc == 1 and out == "R-land: unread (allowed_signers ring)", out        # enforce reads the ring up front (unchanged)


def test_P1_a_prefilter_git_error_is_a_change_r_land_still_runs_never_a_silent_move(tmp_path):
    """council 03:41Z: the hook's `git diff --quiet $o $n -- .agi/nodes` exits 128 on an error and only rc 0 continues, so an
    error means r-land RUNS; r-land's own `git diff --name-only` pre-check treats an error as a change too. A bad boolean
    `diff.renames` (via GIT_CONFIG_COUNT) fails ONLY the porcelain `git diff` (rc 128; diff-tree, rev-list, cat-file are fine)
    and must not hide the move: r-land runs and says so (here the signature `git log` fails too -> `unread git ... failed`,
    loud). MUTANT (RED when run by hand): the hook's prefilter as `;[ $? != 1 ]&&continue` (rc 128 skips r-land, a silent move)."""
    repo = Repo(tmp_path)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v0"))
    repo.set_mode("report")
    env = _install_hook(repo, tmp_path)
    base = repo.git("rev-parse", "HEAD").stdout.strip()
    _branch_at(repo, "refs/heads/posts/belam", base)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v1"))
    bad = repo.commit("dg1", "director edits config directly")
    env = {**env, "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "diff.renames", "GIT_CONFIG_VALUE_0": "bogus"}
    r = _move(repo, "refs/heads/posts/belam", bad, base, env)
    assert r.returncode == 0 and "R-land: would refuse" in r.stderr, r.stderr     # r-land RAN (report mode: loud, the ref moves)
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == bad


# ---- V2 / V3 / V1 (council GATE272, alive 03:51:46Z + 04:05:37Z): the hook twin of verify-land's judge selection ------------
R_LAND = "extensions/agi/guard/r-land"


def _hook_repo(tmp_path):
    repo = Repo(tmp_path)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v0"))
    repo.set_mode("report")
    env = _install_hook(repo, tmp_path)
    env["AGI_RLAND_SINCE"] = repo.git("rev-list", "--max-parents=0", "HEAD").stdout.strip()
    return repo, env


def _judge_blob_commit(repo):
    """The commit that last changed r-land: the judge a later empty/deleted BASE must fall back to."""
    return repo.git("log", "-1", "--format=%H", "--", R_LAND).stdout.strip()


def _land_ref(repo, env, new, old):
    return _move(repo, "refs/heads/posts/belam", new, old, env)


def _drop_r_land(repo, how, signer="belam"):
    if how == "delete":
        repo.git("rm", "-q", R_LAND)
    elif how == "empty":
        repo.write(R_LAND, "")
    return repo.commit(signer, f"{how} r-land")


def _restore_with_violation(repo, original):
    repo.write(R_LAND, original)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="violation"))
    return repo.commit("dg1", "restore r-land + a director edits config directly")


@pytest.mark.parametrize("how", ["delete", "empty"])
def test_V2_1_2_a_deleting_or_emptying_land_then_the_restoring_land_both_judged_by_the_pre_deletion_blob(tmp_path, how):
    repo, env = _hook_repo(tmp_path)
    original = (repo.d / R_LAND).read_text()
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    judge = _judge_blob_commit(repo)
    _branch_at(repo, "refs/heads/posts/belam", b0)
    l1 = _drop_r_land(repo, how)
    r = _land_ref(repo, env, l1, b0)
    assert r.returncode == 0, r.stderr                                          # judged by b0's blob: nothing to refuse
    l2 = _restore_with_violation(repo, original)
    r = _land_ref(repo, env, l2, l1)
    k = "deleted" if how == "delete" else "emptied"
    assert r.returncode == 0 and f"r-land: judge from {judge} ({k} at {l1})" in r.stderr, r.stderr      # the restore is NOT held
    assert "(W2)" in r.stderr, r.stderr                                          # and the prior judge really ran on it
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == l2


def test_V2_3_truncate_then_delete_then_restore_is_judged_by_the_pre_truncation_blob(tmp_path):
    repo, env = _hook_repo(tmp_path)
    original = (repo.d / R_LAND).read_text()
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    judge = _judge_blob_commit(repo)
    _branch_at(repo, "refs/heads/posts/belam", b0)
    l1 = _drop_r_land(repo, "empty")
    assert _land_ref(repo, env, l1, b0).returncode == 0
    l2 = _drop_r_land(repo, "delete")
    r = _land_ref(repo, env, l2, l1)
    assert r.returncode == 0, r.stderr        # the range touches no node: the prefilter skips r-land (nothing to judge, nothing held)
    l3 = _restore_with_violation(repo, original)
    r = _land_ref(repo, env, l3, l2)
    assert r.returncode == 0 and f"judge from {judge} (deleted at {l2})" in r.stderr and "(W2)" in r.stderr, r.stderr


def test_V2_e_a_tip_cut_before_a_trunk_r_land_update_deletes_it_and_lands_by_merge_the_judge_is_the_trunks_newest(tmp_path):
    repo, env = _hook_repo(tmp_path)
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    repo.git("checkout", "-q", "-b", "tip")
    repo.git("rm", "-q", R_LAND)
    repo.commit("dg1", "tip deletes r-land")
    repo.git("checkout", "-q", "main")
    repo.write(R_LAND, (repo.d / R_LAND).read_text() + "# trunk update v2\n")
    v2 = repo.commit("belam", "trunk updates r-land")
    env2 = {**os.environ, "GIT_COMMITTER_EMAIL": "belam@agi", "GIT_COMMITTER_NAME": "belam"}
    repo.git("-c", f"user.signingkey={repo.k / 'belam'}", "merge", "--no-ff", "-q", "-m", "land the tip", "tip", env=env2, check=False)
    assert repo.git("rev-parse", "-q", "--verify", "MERGE_HEAD", check=False).returncode == 0, "the merge must stop on the modify/delete conflict, not fail for another reason"
    repo.git("rm", "-q", "-f", R_LAND)
    m = repo.commit("belam", "land the tip (r-land deleted)")
    _branch_at(repo, "refs/heads/posts/belam", m)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="violation"))
    bad = repo.commit("dg1", "director edits config directly")
    r = _land_ref(repo, env, bad, m)
    assert r.returncode == 0 and f"judge from {v2} (deleted at {m})" in r.stderr and "(W2)" in r.stderr, r.stderr
    assert b0 != v2


def test_V2_f_soften_then_empty_on_a_side_branch_merged_the_judge_is_the_trunks_pre_merge_blob_never_the_softened(tmp_path):
    repo, env = _hook_repo(tmp_path)
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    repo.git("checkout", "-q", "-b", "side")
    repo.write(R_LAND, "#!/bin/sh\necho 'R-land: ok SOFTENED'; exit 0\n")
    soft = repo.commit("dg1", "soften r-land")
    repo.write(R_LAND, "")
    repo.commit("dg1", "empty r-land")
    repo.git("checkout", "-q", "main")
    repo.write("trunk-note.txt", "x")
    repo.commit("belam", "trunk moves on")
    env2 = {**os.environ, "GIT_COMMITTER_EMAIL": "belam@agi", "GIT_COMMITTER_NAME": "belam"}
    judge = _judge_blob_commit(repo)
    repo.git("-c", f"user.signingkey={repo.k / 'belam'}", "merge", "--no-ff", "-q", "-m", "land side", "side", env=env2)
    m = repo.git("rev-parse", "HEAD").stdout.strip()
    assert len(repo.git("rev-list", "--parents", "-n1", m).stdout.split()) == 3, "land side must be a 2-parent merge"
    assert (repo.d / R_LAND).read_text() == "", "the merge carries the side branch's emptied r-land"
    _branch_at(repo, "refs/heads/posts/belam", m)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="violation"))
    bad = repo.commit("dg1", "director edits config directly")
    r = _land_ref(repo, env, bad, m)
    assert r.returncode == 0 and "(W2)" in r.stderr and "SOFTENED" not in r.stderr and soft not in r.stderr, r.stderr
    assert f"judge from {judge} (emptied at {m})" in r.stderr, r.stderr


def _trunk_edit(tmp_path, mode="enforce"):
    """A hooked repo at `mode`, posts/belam at b0, and a belam-signed config edit `new` on top: a node change the widened hook judges."""
    repo, env = _hook_repo(tmp_path)
    if mode != "report":
        repo.set_mode(mode)
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    _branch_at(repo, "refs/heads/posts/belam", b0)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v1"))
    return repo, env, repo.commit("belam", "edit config"), b0


def _notices(tmp_path):
    f = tmp_path / "notices.log"
    return f.read_text() if f.exists() else ""


def test_T1_an_unwritable_TMPDIR_with_a_writable_repo_the_move_PASSES_in_ENFORCE_and_prints_no_unread_tmpdir(tmp_path):
    """Both temp writers live in the repo's objects/ dir (the hook's tmpfile + r-land's own mktemp -d via TMPDIR=$t), so the MOVER's TMPDIR is irrelevant."""
    repo, env, new, b0 = _trunk_edit(tmp_path)
    r = _move(repo, "refs/heads/posts/belam", new, b0, {**env, "TMPDIR": "/nonexistent/tmp"})
    assert r.returncode == 0 and "unread tmpdir" not in r.stderr and "HOLD" not in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == new


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores the mode bits this row sets")
def test_T2_the_git_ROOT_not_writable_while_objects_is_writable_the_move_PASSES(tmp_path):
    """A non-owner group-agi mover: the .git ROOT is belam-only 775, objects/ is group-agi rwx. A temp file under the .git root would HOLD every such mover."""
    repo, env, new, b0 = _trunk_edit(tmp_path)
    g = repo.d / ".git"
    g.chmod(0o555)
    try:
        r = _move(repo, "refs/heads/posts/belam", new, b0, env)
    finally:
        g.chmod(0o755)
    assert r.returncode == 0 and "HOLD" not in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == new


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores the mode bits this row sets")
def test_T3_no_tmpfile_is_a_HOLD_that_names_its_cause_and_runs_agi_notice(tmp_path):
    repo, env, new, b0 = _trunk_edit(tmp_path)
    o = repo.d / ".git" / "objects"
    o.chmod(0o555)
    try:
        r = _move(repo, "refs/heads/posts/belam", new, b0, env)
    finally:
        o.chmod(0o755)
    assert r.returncode != 0 and "HOLD, nothing changed: no tmpfile under" in r.stderr, r.stderr
    assert str(o) in r.stderr and "Permission denied" in r.stderr and "a retry clears it once that clears" in r.stderr, r.stderr
    assert "[r-land] HOLD refs/heads/posts/belam: no tmpfile under" in _notices(tmp_path), _notices(tmp_path)
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == b0


def test_T4_every_HOLD_runs_agi_notice(tmp_path):
    repo, env, new, b0 = _trunk_edit(tmp_path, mode="report")
    r = _move(repo, "refs/heads/posts/belam", new, b0, {**env, "AGI_RLAND_SINCE": "deadbeef" * 5})
    assert r.returncode != 0 and "HOLD, nothing changed: BASE" in r.stderr, r.stderr
    assert "[r-land] HOLD refs/heads/posts/belam: BASE" in _notices(tmp_path), _notices(tmp_path)


def test_V3_an_unresolvable_BASE_ancestry_read_is_a_HOLD(tmp_path):
    repo, env = _hook_repo(tmp_path)
    b0 = repo.git("rev-parse", "HEAD").stdout.strip()
    _branch_at(repo, "refs/heads/posts/belam", b0)
    repo.write(f"{G}/rotations.md", NODE.format(t="config", n="rotations", b="v1"))
    new = repo.commit("belam", "edit config")
    r = _move(repo, "refs/heads/posts/belam", new, b0, {**env, "AGI_RLAND_SINCE": "deadbeef" * 5})
    assert r.returncode != 0 and "HOLD, nothing changed: BASE" in r.stderr and "unresolvable" in r.stderr, r.stderr
    assert repo.git("rev-parse", "refs/heads/posts/belam").stdout.strip() == b0
