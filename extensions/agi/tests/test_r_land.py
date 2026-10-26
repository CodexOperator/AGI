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
        for p in ("belam", "master", "dg1", "dg2", "kid", "intruder"):
            kp = self.k / p
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(kp), "-C", p], check=True)
            if p != "intruder":  # the intruder's key is deliberately NOT in the ring
                pub = (self.k / f"{p}.pub").read_text().split()
                lines.append(f'{p}@agi namespaces="git" {pub[0]} {pub[1]}')
        self.signers.write_text("\n".join(lines) + "\n")
        self.git("init", "-q", "-b", "main")
        for k, v in (("gpg.format", "ssh"), ("commit.gpgsign", "true"),
                     ("gpg.ssh.allowedSignersFile", str(self.signers)), ("user.name", "x")):
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
    (stub / "agi-notice").write_text("#!/bin/sh\nexit 0\n")        # the hook's fail-open path calls it: never write the tester's ~/.notice
    (stub / "agi-notice").chmod(0o755)
    return {"PATH": f"{stub}:{os.environ['PATH']}", "AGI_RING": str(repo.signers)}


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


def test_R4_no_r_land_at_the_old_tip_fails_open_with_a_notice(hooked):
    repo, env = hooked
    repo.git("rm", "-q", "extensions/agi/guard/r-land")
    old = repo.commit("belam", "drop r-land")
    _branch_at(repo, "refs/heads/posts/belam", old)
    bad = repo.edit_rows(lambda r: row(r, "dg2").update(pubkey="zz"), "dg1")
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
    assert rc == 0 and out.startswith("R-land: ok (0 cell change(s)") and out.endswith("mode report)"), out
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
