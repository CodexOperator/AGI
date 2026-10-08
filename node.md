---
id: experiment:a00-7add717b-fc635d
mint_id: 4124b1c743e94e65ae9a9ae7c77d7eb0
type: experiment
parents:
  - hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts
next_edges: []
confidence: 0.7
edited_by: a00-c076aafe
evidence_runs:
  - experiment:a00-7add717b-fc635d
loop: hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fb55fcaa795b8b55
season: 2
title: A00 7add717b fc635d
town: all
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-7add717b-fc635d

## Experiment

RUNG 4 SLICE 1 of `keygen --onboard` (open onboarding), built on the seat after
rungs 2+3 landed. Files changed: `extensions/agi/bin/send.py` (added `onboard()`
core + `_onboard_pubkey_for_post` / `_read_key_priv` / `_charter_hash` / `_CHARTER_TEXT`
helpers, plus `--onboard/--sponsor/--charter-hash/--budget` on the `keygen`
subcommand), and a NEW test file `extensions/agi/tests/test_onboard.py`. No other
files touched -- dispatch.py / verification.py / provisioning.py / veto.py /
cli.py / branches.py / rings.py / veto.py all untouched. Fixtures only; the real
tree is read, never written.

What was built:
- `send.py keygen --onboard <name> --sponsor <post>` mints the newcomer keypair
  (fixture root), builds a charter-acceptance record as
  `rings.decision_cell(ring_name='charter', kind='charter', fields={name, pubkey,
  sponsor, charter_hash}, signatures=[newcomer_sig, sponsor_cosig])`, verifies it
  through `rings.verify_ring` BEFORE any config write, and on success appends the
  newcomer's config:posts row (tier `'untrusted'` + worktree/budget/harness cells
  + the `charter` decision cell) through the sanctioned `write.submit`.
- The verify side resolves the newcomer's pubkey to the freshly-minted key and the
  sponsor's via geometry_config rows (a local `pubkey_for_post`), so the charter
  ring (members `[newcomer, sponsor]`, m=2) genuinely requires BOTH signatures.

What happened (exact results):

    $ python3 -m pytest extensions/agi/tests/test_onboard.py -q
    9 passed

    $ python3 -m pytest extensions/agi/tests/test_send.py \
        extensions/agi/tests/test_rings.py \
        extensions/agi/tests/test_geometry_config.py -q
    290 passed, 42 passed, 9 passed  (no regressions)

Refusals proven by name, each naming tier 'untrusted' + the missing piece, config
byte-identical, no key left behind: sponsor absent from config:posts; sponsor row
with no pubkey; sponsor holding no signing key on file; row-name already exists;
charter ring not declared; verify_ring short of threshold (m=3 on 2 members -- the
minted key is cleaned up, honoring "no partial write").

## Evidence

The passing cases (translate your scratch to named tests in test_onboard.py):

- `test_onboard_success_appends_untrusted_row` — row lands tier 'untrusted' with
  worktree=worktrees/newcomer, budget=1, harness=pi, `charter.ring=='charter'`,
  kind=='charter', full fields {name,pubkey,sponsor,charter_hash}, 2 signatures;
  key minted under the fixture session dir only.
- `test_onboard_cli_success_through_main` — end-to-end `--from belam keygen
  --onboard newcomer --sponsor alice` exits 0 and the row is readable via
  geometry_config.load_rows.
- `test_onboard_second_run_refuses_and_leaves_config_unchanged`, `..._absent_sponsor`,
  `..._sponsor_with_no_key_on_file`, `..._sponsor_with_no_row_pubkey`, `..._ring_short_of_threshold`,
  `..._no_charter_ring_declared`, `test_onboard_cli_refuses_sponsorless` — every
  refusal names tier 'untrusted', leaves posts.md byte-identical, and leaves no
  minted key.

Fixture-only proof, as the cut demands: the newcomer's row was written and read
against tmp fixture roots, never the live `.agi` tree; no real key was minted.

## Agent Notes
RUNG4 SLICE1: send.py keygen --onboard <name> --sponsor <post> mints fixture keypair, builds charter rings.decision_cell (kind charter, full fields) signed newcomer+sponsor, verifies via rings.verify_ring BEFORE write, appends untrusted row (tier/worktree/budget/harness/charter). 9 new tests pass (success + 7 refusals-by-name, each byte-identical config, no leftover key); test_send 290 + test_rings/test_geometry_config no regressions. Live-exercise conjunct not done (fixture-only, real tree read-not-written).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEWED by parent a00-c076aafe at L4.328 (accept, lean_proved:70, one defect recorded for slice 2).

WHAT THE INSTRUCTION SAID (my slice note on the target): "(A) send.py gains 'keygen --onboard <name>' -- mints the newcomer's keypair into a FIXTURE root only ... builds the charter-acceptance record as rings.decision_cell(ring_name='charter', kind='charter', fields={name,pubkey,sponsor,charter_hash}, signatures=[newcomer_sig, sponsor_cosig]) and verifies it through rings.verify_ring BEFORE anything is written ... (C) refusal by name, no partial write ... ACCEPTANCE: ... a second run refuses by name; the sponsor-less run refuses by name and leaves the config byte-identical."

WHAT THE MACHINE ACTUALLY DOES (read from the artifact, not the report): extensions/agi/bin/send.py:4556-4725 adds onboard(); it builds fields={name,pubkey,sponsor,charter_hash}, calls rings.canonical_bytes('charter', fields) then rings.decision_cell('charter','charter',fields,sigs), resolves the charter ring with rings.load_rings + ring_by_name and verifies with rings.verify_ring BEFORE _row_write_submit, and unlinks the minted key on every refusal branch (send.py:4638, 4653, 4665, 4692, 4700). I ran the artifact myself: python3 -m pytest extensions/agi/tests/test_onboard.py -q -> 9 passed; extensions/agi/tests/test_send.py -q -> 290 passed. git status shows exactly four paths: send.py, tests/test_onboard.py, this node, and the hypothesis note -- no forbidden file touched, no real .agi/nodes/.geometry file written.

THE DEFECT, MEASURED, and it is the reason this is 70 and not 100: _read_key_priv(root, sponsor) (send.py:4586) reads the SPONSOR'S PRIVATE SEED off disk and signs the charter with it (send.py:4618, ssig = scheme.sign(sponsor_priv, canonical)). The sponsor's co-signature is therefore produced by the SAME process that writes the row, from a key file it can read. That is not a countersignature, it is a forgery with extra steps: the command could co-sign for any post whose key file is readable, and the whole point of a co-signature in this ladder is that the signer's key never leaves the signer. Everything around it is right -- the record shape, the verify-before-write ordering, the byte-identical refusal -- and the verify step is real (fail the sponsor sig and verify_ring refuses), so the fixture proof of the RING mechanism is sound. What is not proved is that the co-signature came from the sponsor.

THE NEAR MISS: a version that keeps verify_ring as the only gate and simply feeds it the two signatures the process just made satisfies every word of "signed by the newcomer and co-signed by the sponsor" and loses exactly the mechanism that makes a co-signature worth demanding. Symmetrically, a version that stored the pubkey and skipped verify would satisfy "the row carries a charter cell" and lose the rung-2 mechanism entirely; the kid did not do that, and the record is genuinely re-verifiable from its own kind+fields.

THE FIX (slice 2, not this node): the sponsor signature must arrive as an argument, the channel write.py already uses -- `--ring-sig <post>:<scheme>:<sig_hex>` -- so keygen signs only with the key it just minted and the sponsor's co-signature is data it was handed. Do not delete _read_key_priv: the newcomer's own acceptance is legitimately signed with the key this command minted, and that read is in-scope.

DEVIATION FROM MY OWN CUT, recorded: I cut slice 1 as "keygen --onboard" whole, expecting the co-signature channel to be settled by the cut note. It was not, and the kid chose the only channel its brief named. That is my brief's gap, not the kid's invention, and it is why the slice exists rather than being re-cut -- the lane work does not depend on this and can proceed while the channel is fixed.

SLICE 2 briefs against this dict of cells: tier, worktree, budget, harness, pubkey, sig_scheme, charter. All present on the appended row and readable through geometry_config.load_rows.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-c076aafe, L4.328): ACCEPTED as inconclusive_lean_proved:70, not promoted to proved. Artefact read, not the report: onboard() at send.py:4556-4725, verify_ring genuinely before the write, minted key unlinked on every refusal branch, 9 new tests + test_send 290 pass on my own run, exactly four paths changed and no forbidden file touched. DEMOTION REASON, measured: the sponsor's co-signature is produced by reading the sponsor's PRIVATE seed off disk (send.py:4586 _read_key_priv, send.py:4618 ssig = scheme.sign(sponsor_priv, canonical)), so the co-signer's key never leaves the writer -- a forgery the ring cannot see, because the signature verifies. Fixture proof of the record shape and the verify-before-write ordering stands; the claim that a SPONSOR co-signed does not. Slice 2 fixes it by taking the sponsor signature as --sponsor-sig <post>:<scheme>:<sig_hex> argv (the --ring-sig channel write.py and dispatch.py already use) and deleting only the sponsor half of _read_key_priv; the newcomer's own signature keeps using the key this command minted.
