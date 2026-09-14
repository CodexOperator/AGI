---
id: hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi
mint_id: adf46401561047fea8691e7b1b22412d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 525877b19cd30ade
season: 2
status: active
testable_claim: "goal:g15 (owner 2026-09-14 03:0xZ, URGENT; the Claude Code subscription is at 3% for 48 h): GitHub Copilot CLI becomes the THIRD harness beside claude-code and pi, with the same hooks, so any Sanctuary post or round can run on the owner's Copilot Pro plan. Conjuncts, each measured: (1) INSTALL: `npm install -g @github/copilot` (or the current package the GitHub docs name) puts a `copilot` binary on PATH for user ubuntu; `copilot --version` and `copilot help` are quoted into the experiment node; AUTH is tried with the existing gh login (`GH_TOKEN=$(gh auth token)` or `COPILOT_GITHUB_TOKEN`, account CodexOperator) -- if the token lacks the Copilot scope the parent STOPS on that conjunct and reports the exact login command the OWNER must run by hand (device flow), never fakes auth. (2) MODELS: the list of models the CLI offers on this plan (`copilot help` / `--model` choices / the /model command), quoted verbatim, mapped against the ladder rows (parent, kid, director, prime): which of claude-sonnet/opus, gpt-5.x, gemini are there; the answer to the owner's 'does it offer most of the same models' is a table, not a sentence. (3) HEADLESS: a one-turn non-interactive run (`copilot -p '<prompt>' --allow-all-tools` or the documented equivalent) from a fixture cwd returns text and exits 0 -- proven by a real run whose transcript is quoted (one premium request is authorized by this claim). (4) HARNESS ENTRY: `.agi/config.json` gains `harnesses.copilot-cli` in the SAME shape as `harnesses.pi` (adapter, bin, models.parent/kid, allowed_extra) and dispatch.py gains the adapter: brief file -> prompt, model flag, cwd = the round's worktree, the same env scrub and the same reaper knob export as the pi/claude-code launchers; `dispatch.py . <iter> --harness copilot-cli --dry-run` prints the BUILT command with the model from the config row (proof from the built command, never the diff). (5) HOOKS PARITY: the SessionStart map injection and the UserPromptSubmit meter line -- if the CLI has a hooks mechanism (.github/hooks or its config), the two hooks are registered there on a fixture and proven by a session log; if it has none, the adapter injects the map into the prompt and the meter is read from the CLI's own session log/transcript, and the claim says so plainly. (6) ROTATE SHAPE: rotate.py's launch path can seat a post on copilot-cli in a tmux window (interactive `copilot` with the card as the first prompt; send.py's inbox + nudge work unchanged because they are pane-based); there is NO remote-control equivalent -- the owner watches such a post by tmux, and the claim states it. (7) TESTS: every new code path has a fixture-only test (a fake `copilot` binary on PATH, never a live call in the suite); the full engine suite stays green. Falsifiers: no binary installs; auth impossible without the owner; the CLI has no headless mode; the model list lacks every Claude/GPT tier the ladder needs; hooks impossible and prompt injection breaks the map cap. Deliver: the experiment node with every measurement quoted, the code on the round branch, and ONE line for the Prime: models table + auth state + what the owner must do by hand."
title: Copilot CLI is a third harness with the same hooks as claude-code and pi (owner URGENT 2026-09-14 03:0xZ)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
