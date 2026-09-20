#!/usr/bin/env python3
"""TypeSafe choice replay for hypothesis:lm-typesafe-replay-200.

Reads cases.jsonl, POSTs each state to the TypeSafe systemone endpoint,
parses choice + confidence, writes results.jsonl.

CONTRACT:
  * TYPESAFE_KEY is read from os.environ AT CALL TIME (never cached, never printed,
    never written to any file).
  * With no key the script makes ZERO network calls and exits 2.
  * Offline/per-case errors are recorded, never fabricated.

Usage:
  python3 replay.py            # runs both sets against cases.jsonl
  python3 replay.py --dry      # same, but no network even if key present
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "cases.jsonl")
RESULTS = os.path.join(HERE, "results.jsonl")
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"

CRITERIA_A = {
    "proved": "the recorded verdict is proved",
    "disproved": "the recorded verdict is disproved",
    "inconclusive_lean_proved": "the recorded verdict leans proved but is not conclusive",
    "inconclusive_lean_disproved": "the recorded verdict leans disproved but is not conclusive",
    "pending": "no verdict was recorded",
}
CRITERIA_B = {
    "merge-up": "the line reports work merged upward to a parent",
    "decision": "the line records a decision made",
    "rotation": "the line concerns session or role rotation",
    "red": "the line reports a failure, blocker or red status",
    "rule": "the line states a rule",
    "complete": "the line reports a task or round complete",
    "owner": "the line is addressed to or from the owner",
}
INSTRUCTIONS = (
    "You are replaying a decision the graph already made. "
    "Choose the single label that best matches the supplied state. "
    "Answer with the choice field and a confidence between 0 and 1."
)


def criteria_for(rec):
    return CRITERIA_B if rec["set"] == "B" else CRITERIA_A


def load_cases():
    with open(CASES, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def ask(key, state, criteria):
    body = json.dumps({
        "state": state,
        "model": MODEL,
        "questions": {"q": {
            "type": "choice",
            "instructions": INSTRUCTIONS,
            "criteria": criteria,
        }},
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            status = resp.status
    except urllib.error.HTTPError as e:
        status = e.code
        payload = None
    return status, payload, time.time() - t0


def main():
    dry = "--dry" in sys.argv
    key = os.environ.get("TYPESAFE_KEY")  # read at call time; never logged
    cases = load_cases()

    if not key or dry:
        reason = "no_key" if not key else "dry_run"
        with open(RESULTS, "w", encoding="utf-8") as fh:
            for rec in cases:
                fh.write(json.dumps({
                    "set": rec["set"], "id": rec["id"],
                    "label": rec["label"], "blocked": reason,
                }, ensure_ascii=False) + "\n")
        sys.stderr.write(
            "blocked:%s -- %d records marked, 0 network calls, key %s\n"
            % (reason, len(cases), "absent" if not key else "present (--dry)"))
        return 2

    with open(RESULTS, "w", encoding="utf-8") as fh:
        for rec in cases:
            status, payload, dt = ask(key, rec["state"], criteria_for(rec))
            choice = confidence = None
            if isinstance(payload, dict):
                q = payload.get("questions", {}).get("q", payload)
                if isinstance(q, dict):
                    choice = q.get("choice")
                    confidence = q.get("confidence")
            fh.write(json.dumps({
                "set": rec["set"], "id": rec["id"], "label": rec["label"],
                "choice": choice, "confidence": confidence,
                "http_status": status, "latency_s": round(dt, 4),
            }, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
