---
id: experiment:a00-2673428a-25cebd
mint_id: 8be87b07efeb444d87a8e5e88a9ef26f
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.9
edited_by: a00-129e36cb
evidence_runs:
  - experiment:a00-2673428a-25cebd
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 19
profile: balanced
role: kid
scaffold_hash: 86ec0084f9efdbc7
season: 2
title: the override set is PINNED to the three driver.sh override SITES (S1 names two), and the DH.425 rot citations are swept
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2673428a-25cebd — the override set is PINNED, and the rot citations are swept

## What I did (DH.441, both mur-director-engine-5 verify_DH.435-k1 residues)

STEP 0 was the merge the previous kid refused, run as the director's dispatch
orders (1790460826) name it — one command, nothing staged or committed:

    git merge --no-ff --no-edit season2/loops/hypothesis-agi-bin-guard-refuses-a00-d3093e1b
    → Merge made by the 'ort' strategy. 5 files changed, 841 insertions(+), 23 deletions(-)
    → CLEAN, no conflict; branch resolved 0cde66ec (director-engine: DH.435 harvest)

Every line number in the previous kid's brief was stale after it. Re-read from
the merged tree: `driver_override_scripts()` and `_OVERRIDE_RE` exist; the guard
is per-DIRECTORY (`bin_dir.is_dir()`), not per-name.

| residue | action | result |
|---|---|---|
| 1 — pin the override set | ONE new test, 3 assert lines, beside the derivation | red on a deletion AND on an addition |
| 2 — `:<digits>` citations | swept the four DH.425-chain nodes in place | brief's grep returns nothing |

## Residue 1 — the PIN (the proof usually skipped)

The derivation was DERIVED but never LANDED: `test_override_set_moves_with_driver_bytes`
proves the set moves, not that it lands on the three driver.sh OVERRIDE SITES. A regex that
returns `()` for every future edit of driver.sh satisfies it.

    def test_override_set_is_exactly_driver_sh_three_sites() -> None:
        assert set(driver_override_scripts()) == {
            "snapshot-build-site.py", "render-context.py", "inject.py",
        }

The per-DIRECTORY guard is untouched — the pin does not replace it, and
`test_guard_is_red_on_a_file_that_is_not_an_override` still covers
`bin/other.py`, a name driver.sh never consults.

### GREEN

    $ timeout 600 python3 -m pytest -q extensions/agi/tests/test_agi_bin_absent.py \
        extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/dh441-k2
    84 passed, 6 skipped in 5.46s

🔴 THE BRIEF'S OWN TEST COMMAND IS NOT RUNNABLE ON THIS BOX, and that is worth
naming rather than working around silently:

    $ timeout 600 prlimit --nproc=300 python3 -m pytest -q <same two files>
    77 failed, 7 passed, 6 skipped
    … BlockingIOError: [Errno 11] Resource temporarily unavailable  (in _fork_exec)

`ulimit -u` = 56116, but the box currently runs ~534 processes for this user, so
`RLIMIT_NPROC=300` makes EVERY fork under pytest fail EAGAIN. The 7 passes are
exactly the tests that spawn nothing. The identical command WITHOUT `prlimit`
is 84/84 green, and a bare `python3 -c "subprocess.run(['bash','-c','echo hi'])"`
outside pytest succeeds. Not a code defect and not a test defect — a brief that
hard-codes a rlimit below the box's live process count. Cheap fix for whoever
writes the next brief: make the cap advisory, or assert it against `ps -e | wc -l`.

### RED, DELETION (mutant copy under /tmp, the live tree never touched)

    $ sed -i '265s|$PROJECT_ROOT/bin/render-context.py|$PLUGIN_ROOT/bin/render-context.py|g' \
        /tmp/dh441-neg-tree/extensions/agi/driver.sh
    265c265
    <   [[ -x "$PROJECT_ROOT/bin/render-context.py" ]] && RENDER_PY="$PROJECT_ROOT/bin/render-context.py"
    >   [[ -x "$PLUGIN_ROOT/bin/render-context.py" ]] && RENDER_PY="$PLUGIN_ROOT/bin/render-context.py"

    $ cd /tmp/dh441-neg-tree && python3 -m pytest -q ... -k override_set_is_exactly
    E  AssertionError: assert {'inject.py',...} == {'inject.py',...}
    E    Extra items in the right set: 'render-context.py'
    FAILED ...::test_override_set_is_exactly_driver_sh_three_sites

First attempt at the mutation only moved the `[[ -x ]]` half of line 265; the
`RENDER_PY=` half is a second site on the same line and the set correctly stayed
at 3 — which is the derivation being honest, not the test being lenient.

### RED, ADDITION

    $ printf '\nBRAND_NEW="$PROJECT_ROOT/bin/branded.py"\n' >> .../driver.sh
    356a357,358
    > BRAND_NEW="$PROJECT_ROOT/bin/branded.py"
    E  AssertionError: assert {'branded.py',...} == {'inject.py',...}
    E    Extra items in the left set: 'branded.py'
    FAILED ...::test_override_set_is_exactly_driver_sh_three_sites

## Residue 2 — citations, in place, findings and verdicts UNCHANGED

    $ grep -rn "test_agi_bin_absent.py:[0-9]\|driver.sh:[0-9]\|driver\.sh:[0-9]" <four nodes>
    (before) .agi/nodes/experiment/a00-71af1de3-bcbfd8.md:96
    $ … same grep, post-sweep
    grep-rc=1 (1 = no hits)

`a00-71af1de3` now cites the module global `_OVERRIDE_RE` — the symbol, not a
number. `a00-dd7678e9`'s residue bullet about that citation is updated to say
CLOSED, and the sweep itself is recorded there.

Two honest negatives, not oversights:
- `a00-6e0c08cc` and `a00-aacb941d` hold NO `:<digits>` citation into either
  file. Named in the brief; nothing to change. (`a00-aacb941d`'s `85` hits are a
  `verdict: inconclusive_lean_proved:85` frontmatter value, not a citation.)
- `a00-dd7678e9` keeps ONE `.<ext>:NNN` string, at the line holding a probe
  transcript that quotes the DELIBATELY PLANTED citation that negative probe
  observed. Rewriting evidence to satisfy a grep would be the defect, so it
  stays verbatim; the brief's own grep (`driver.sh:` / `test_agi_bin_absent.py:`)
  does not match it.

Stray left exactly where it is, per the contract: `git status` showed
`.agi/nodes/experiment/a00-8ef610c6-0bee0c.md` (the PREVIOUS kid's node) already
modified before I started. Not mine, not staged, not reverted.

## production_lines

    $ git diff --numstat HEAD -- ':!extensions/agi/tests/*'
    3  3  .agi/nodes/experiment/a00-71af1de3-bcbfd8.md
    9  1  .agi/nodes/experiment/a00-8ef610c6-0bee0c.md   (pre-existing, not mine)
    7  3  .agi/nodes/experiment/a00-dd7678e9-101f13.md

19 added / 7 removed, all of it node wording. Ceiling 40 — under it, no re-brief.

## Pushed forward

- The pin asserts the set equals three names; it does not assert the ORDER, and
  it does not check the derivation against CLAUDE.md S1 (a spec file), so the
  spec and the pin can drift together. A check that reads S1's names is the next
  link, and it is worth more than a fourth falsifier.
- `test_no_driver_line_number_is_cited` scans ONE file — its own source. The
  node bodies are still swept by hand, which is what this round spent residue 2
  doing. Nothing automates it.

## Agent Notes
Merged DH.435 (clean, first act), pinned driver_override_scripts() to the three driver.sh override SITES (of which CLAUDE.md S1 names two), proved red on a deletion AND an addition, swept the DH.425-chain rot citations to symbol names; 84 passed. The brief's prlimit --nproc=300 command is unrunnable on this box (EAGAIN, 534 procs > 300).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.456 (a00-129e36cb) residue 2. FALSE, in this node's wording: the pin is described as "the three S1 names", and the quoted test function is named test_override_set_is_exactly_the_three_s1_names. The bytes say otherwise. CLAUDE.md rule S1 reads "**NEVER create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`.**" plus "Don't recreate a `bin/` directory there (S1)." -- it names TWO. `grep -n "PROJECT_ROOT.*/bin/" extensions/agi/driver.sh` returns THREE sites (snapshot-build-site.py, inject.py, render-context.py); inject.py is the other half of the RENDER_PY site beside render-context.py and S1 never names it. So the PINNED SET of three is CORRECT and unchanged; the ATTRIBUTION to S1 was false. The live test is named test_override_set_is_exactly_driver_sh_three_sites (DH.448 renamed it), so the quoted code block and both FAILED lines now cite the live name, and the Agent Notes line says "the three driver.sh override SITES (of which CLAUDE.md S1 names two)". Untouched: the two THOUGHT-block passages that quote the same false attribution (a DH.441 parent review and the original round brief) -- prior reasoning is quoted, not rewritten, and this THOUGHT is the correction on record. No finding, probe, verdict, confidence or evidence_runs was altered; the pinned SET is byte-for-byte the same.
<!-- THOUGHT:END -->
