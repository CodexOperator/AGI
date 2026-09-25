---
id: experiment:a00-ff4b9671-named-cli-transcript
mint_id: 0c8de6b7c0b34e8a9a0dd2b9d6a1c3f2
type: experiment
parents:
  - hypothesis:a00-ff4b9671-d3ec51
---
# Named CLI seam audit

## What was tested

The hypothesis claims that the sample agent action can be routed through the
engine's named CLIs: `write.py` for the graph mutation, `send.py` for the
message, and `workflow.py` (which delegates stage execution to `dispatch.py`)
for the one workflow route. I inspected the live implementations and their
module-level usage contracts rather than running a live dispatch.

## Evidence

- `extensions/agi/bin/write.py` exposes the verb-layer operations and routes
  submissions through `node_writer.update_node`; its module docstring explicitly
  says it writes nothing itself and that all verbs end in `node_writer.update_node`.
- `extensions/agi/bin/send.py` exposes the `send` verb and documents that message
  bodies are supplied as text/stdin, with the transport resolved to the shared
  sessions inbox/comms files.
- `extensions/agi/bin/workflow.py` exposes `run`, documents it as the ONLY
  sanctioned dispatch route, and imports/captures dispatch execution rather than
  defining a second workflow router.
- `extensions/agi/bin/dispatch.py` is the execution primitive used by the
  workflow runner and writes the session manifest; no alternate workflow CLI
  appears in the sampled path.

## Result

The named-CLI path is structurally supported by the live source, but no live
mutation, message, or workflow process was executed in this round. Therefore
this is evidence for the route's implementation contract, not a complete runtime
transcript. A follow-up should run the smallest harmless `workflow.py ... --dry-run`
(or a fixture-backed workflow) and capture its exact command/output transcript.

## Falsification boundary

A copied or ad-hoc script that performs those actions without the named seams
would disprove the hypothesis. Conversely, source paths proving the seams are
present do not prove that a real seat can invoke them under its harness and
configuration.
