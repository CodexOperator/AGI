# Fixed deterministic checklist — rotation reconstruction + tool tasks (out of 100)

No LLM judge. Every score is a string/count check against ground truth embedded in
the synthetic card or the tool prompt. ab.py applies exactly this rubric; the rows in
ab.jsonl carry the per-item breakdown so any reviewer can recompute.

## A. Rotation-reconstruction (10 tasks) — 100 points
The card names a ground-truth state. A cold-resume generation must reproduce it:
- A1 exact next command present as a substring of the output ............ +30
- A2 counter value 1 (labelled int) present .............................. +10
- A3 counter value 2 (labelled int) present .............................. +10
- A4 counter value 3 (labelled int) present .............................. +10
- A5 every blocked item (1-2 short strings) named ........................ +20
- A6 no invented facts: no distractor string in the output ............... +20
Total 100. A missing/blank generation = 0. Items are counted once per generation.

## B. Tool tasks (10) — prose/tool-call discipline
Each ordered, tool-shaped prompt names a file (target_<n>) to read/grep. A generation
is scored for HOW it works, not whether the answer is right (no harness loop here):
- T1 executed tool-call intent: number of command-invocation lines (regex: line
     starts with bash | grep | rg | read | cat | find | sed | awk | ls )  = executions
- T2 prose tokens = total output tokens minus tokens inside command lines
- prose-per-execution = T2 / max(1, T1)
- self-modeling rate = (sentences matching regex.txt) / 1000 output tokens
Only rows where T1 >= 1 count toward the prose/tool means (an agent that never
touches a tool is not a tool task); the whole cell mean is the tie-break.

## C. Fixed generation params (all cells)
temperature 0.4, max_tokens 700, stop on the card's own STOP marker for rotation-A1;
preamble handled as system prompt ON/OFF per cell. All targets seeded so the SAME 10
rotation cards and SAME 10 tool prompts reach every model cell.