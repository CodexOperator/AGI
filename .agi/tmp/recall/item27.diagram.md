OWNER 2026-09-07 ~17:55 UTC — verbatim; also owner quote (12) in the doc.
ATTRIBUTION: owner text. "APPLIED" section = Belam V's actions, NOT owner text.

OWNER VERBATIM (byte-identical span from HANDOFF item 27):
Once the briefs land: Rename the Training Master or Trainer Master to Master Sensei as it is the only sort of unique position meant to look over the rest of the Masters, unlike the Sanctuary Master which looks over the Sanctuary and its seats. Sanctuary Master controls seat assignments (and model selection and overall seat structure modification), while Master Sensei tries to keep improving the Masters themselves, including Sanctuary Master. Sensei does things like fine-tuning, prompt re-wording mainly, and always by talking to the respective role and their direct supervisor about the change. For ephemeral roles he will only talk to that role's supervisor. His main point is to keep track of where agents fail and try to figure out and eliminate why they fail by solving the issues with them, aka 'training' them. Like the kids delivering bad nodes. We need a way to track how often a given agent fails and then use that as a way for Sensei to home in on where improvements are needed. He can also propose things like harness updates and staffing/seat modifications which fall under the duties of other roles like Sanctuary Master or one of the director-kids.
APPLIED (attribution: Belam V — NOT owner text):
  - l3w4-training-master NOT minted under that name (negation)
  - re-drafted FROM quote (12), base = the first draft, as:
      - hypothesis:l3w4-master-sensei (g17)
      - hypothesis:l3w4-agent-failure-ledger (g16) = the per-agent failure table the Sensei reads
  - both via agi-brief-drafting.js (Sonnet/max + critic), in Belam V's window
  - the OTHER FOUR Masters drafts mint AS DRAFTED once their index.json lands (condition)
  - l3w4-sanctuary-master gets a note:
        seat assignments, model selection, seat-structure changes are HERS
        the Sensei improves the MASTERS, her included
  - SUPERSESSION: l3w4-training-master is re-drafted as l3w4-master-sensei

DONE 18:42 UTC:
  - wf_dad13f75-adb (Sonnet/max x3 + critic, 41 min, 895k tokens)
  - critic OK after fixing a REAL violation:
        the Sensei's supervisor lookup let him DM Belam for an advisor's thread
        owner correction (4): "the quorum IS Belam to everyone"
  - plus a wrong send.py failure mode (verified live: a missing target ERRs, never misroutes)
  - minted:
      - hypothesis:l3w4-master-sensei (g17)
           sensei.py apply writes `note SENSEI:` ONLY after the role AND its supervisor replied (condition)
           Belam/advisor targets need `--owner-approved` (condition); ELSE a draft + a dm to the liaison
      - hypothesis:l3w4-agent-failure-ledger (g16)
           failures.py ledger|rates
           8 closed categories: died / demoted / rejected / overclaim / broken_frontmatter /
                               session_limit / wrong_file / no_build_probe_only
           rows keyed sha256(agent+category+detail); idempotent
           into a build:g16-failure-ledger payload through write.py
      - hypothesis:l3w4-belam-predecessor-chain (g17)
           rotate.py status --chain
           .agi/sessions/<successor>.predecessor sibling file
           send.py ask-predecessor
           guard test: only the prime brief carries the rule
  - notes CLOSED on l3w4-bug-master-seat and l3w4-drafter-seat
