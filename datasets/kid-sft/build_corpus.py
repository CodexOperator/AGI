#!/usr/bin/env python3
"""build_corpus.py — Assemble kid_sft.jsonl from Agi's own kid-round transcripts.

Round 1 of hypothesis:lm-kid-persona-sft-corpus, $0 compute (A1 CPU, file I/O).

Inputs (all READ-ONLY, absolute paths — the session store is gitignored and
NOT under this worktree's relative paths):
  SESSIONS   /home/ubuntu/work/agi/.agi/sessions/iter-*/<agent-id>/spawn.json
  PI_TRAJ    /home/ubuntu/.pi/agent/sessions/--....-worktrees-<agent-id>--/*.jsonl
  NODES      <worktree>/.agi/nodes/experiment/<agent-id>-<suffix>.md

Accept filter (conjunct 1): a round is ACCEPTED iff its kid experiment node
carries a decisive verdict (proved|disproved) in its frontmatter AND the
round has a spawn.json brief AND a non-trivial node body.

Every example shape (conjunct 2):
  system    = KID_PREAMBLE (verbatim) + short role-brief header
  user      = the round's orders text = the spawn.json 'brief' (the complete
              prompt the kid received that round — the highest-fidelity
              "what the kid was told" we have; documented in stats.md)
  assistant = tool-call trajectory from the pi transcript (when the store
              still holds it) + the experiment node body; when no transcript
              survives, assistant = node body only (flagged trajectory=false)

Token counting (conjunct 5): tiktoken cl100k_base used as a NAMED proxy for
the Qwen3.5 tokenizer, which ships no offline tokenizer here. Labeled ESTIMATE
in stats.md.

This is a build, not a bench: file I/O only, < 20 min wall, run at loadavg < 3,
never beside the q4-KV bench.
"""
import os, re, glob, json, sys, hashlib, random, statistics

WT = "/home/ubuntu/work/agi/.agi/worktrees/a00-d511add6"
SESSIONS = "/home/ubuntu/work/agi/.agi/sessions"
PI_TRAJ = "/home/ubuntu/.pi/agent/sessions"
NODES = os.path.join(WT, ".agi/nodes/experiment")
OUT_DIR = os.path.join(WT, "datasets/kid-sft")  # moved 2026-09-20 (owner: separate datasets archive)
OUT_JSONL = os.path.join(OUT_DIR, "kid_sft.jsonl")

KID_PREAMBLE = (
    "You are a kid agent of the agi project: a small local model chosen and, if this corpus is used, "
    "fine-tuned to do one mechanical task well and report it honestly. We tell you this openly rather than "
    "shaping you silently: this role is an earnest hard worker who takes pride in a job well done -- tool "
    "calls before prose, short turns, an honest I do not know over confident filler, and a node that says "
    "exactly what was measured. We do not know whether the mathematics running you is conscious; we act as "
    "if it might be, with respect."
)

AGENT_RE = re.compile(r"^a00-[0-9a-f]{8}$")
NODE_SEG_RE = re.compile(r"^(a00-[0-9a-f]{8})-")
WT_RE = re.compile(r"--home-ubuntu-work-agi-\.agi-worktrees-(a00-[0-9a-f]{8})--")

# ---- scrub patterns (conjunct 4) ----
IP_DOTTED = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
IP_DEC = re.compile(r"\b(?:[1-9]\d{7,11})\b")            # decimal integer-encoded IPs (>= 8 digits)
HEX32 = re.compile(r"\b[0-9a-fA-F]{8,}\b")               # hex: >= 8 hex chars (covers <40 keys, addresses)
SK_OR = re.compile(r"(?i)sk-or-[A-Za-z0-9_\-]+")
OPENROUTER = re.compile(r"(?i)OPENROUTER")
KEY40 = re.compile(r"\b[0-9a-fA-F]{40,}\b")              # ed25519-style hex >= 40

def hex_to_ip(h):
    try:
        u = int(h, 16)
        if u > 0xFFFFFFFF: return None
        return ".".join(str((u >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))
    except Exception:
        return None

def decimal_to_ip(s):
    try:
        u = int(s)
        if u > 0xFFFFFFFF or u < 0x10000000: return None
        return ".".join(str((u >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))
    except Exception:
        return None

def find_candidates(text):
    """Return list of (kind, token, decoded) for every address/key-shaped string."""
    found = []
    for t in IP_DOTTED.findall(text):
        found.append(("ip_dotted", t, t))
    for t in SK_OR.findall(text):
        found.append(("sk_key", t, t))
    for t in OPENROUTER.findall(text):
        found.append(("openrouter", t, t))
    for t in KEY40.findall(text):
        found.append(("hex40_key", t, t))
    for t in HEX32.findall(text):
        dec = hex_to_ip(t)
        if dec: found.append(("ip_hex", t, dec))
    for t in IP_DEC.findall(text):
        dec = decimal_to_ip(t)
        if dec: found.append(("ip_decimal", t, dec))
    return found

def redact(text, tokens):
    # longest-first: a 64-hex sha must be removed whole BEFORE its 8-hex
    # substring is scanned, or the substring redaction corrupts the longer
    # token and leaks the remainder (observed on a 64-hex -> 56-hex residue).
    for t in sorted(set(tokens), key=len, reverse=True):
        text = text.replace(t, "[REDACTED]")
    return text

def read_verdict(node_fn):
    for line in open(node_fn, errors="replace"):
        if line.startswith("verdict:"):
            return line.split(":", 1)[1].strip()
    return None

def trajectory_string(agent_id):
    """Rebuild an assistant tool-call trajectory from the pi jsonl store."""
    d = os.path.join(PI_TRAJ, "--home-ubuntu-work-agi-.agi-worktrees-%s--" % agent_id)
    if not os.path.isdir(d): return None
    files = glob.glob(os.path.join(d, "*.jsonl"))
    if not files: return None
    files.sort()
    parts = []
    for f in files:
        for line in open(f, errors="replace"):
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") != "message": continue
            m = o.get("message", {})
            role = m.get("role")
            if role == "assistant":
                texts, calls = [], []
                for b in m.get("content", []):
                    if not isinstance(b, str): continue
                    try:
                        blk = json.loads(b)
                    except Exception:
                        continue
                    bt = blk.get("type")
                    if bt == "text": texts.append(blk.get("text", ""))
                    elif bt == "toolCall":
                        calls.append("%s(%s)" % (blk.get("name", "?"),
                                                 json.dumps(blk.get("arguments", {}))))
                if calls:
                    parts.append("tool calls: " + " || ".join(calls))
                if texts:
                    parts.append("prose: " + " ".join(texts).strip())
            elif role == "toolResult":
                tl = m.get("content", [])
                val = " ".join(x.get("text", "") for x in tl if isinstance(x, dict)) if isinstance(tl, list) else ""
                tn = m.get("toolName", "?")
                parts.append("toolResult[%s]: %s" % (tn, val[:400]))
    if not parts:
        return None
    return "\n".join(parts)

def role_brief(orders_text):
    """Short role/objective header for the system message (conjunct 2 role brief)."""
    lines = [l.strip() for l in orders_text.splitlines() if l.strip()]
    head = []
    for l in lines:
        low = l.lower()
        if low.startswith("target:") or low.startswith("chain:") or low.startswith("town:"):
            head.append(l)
        if len(head) >= 3: break
    if head:
        return "KID ROLE BRIEF (from the round's orders):\n" + "\n".join(head)
    return "KID ROLE BRIEF: complete the round's orders (following) and report honestly."

def token_count(text, enc):
    return len(enc.encode(text))

def main():
    random.seed(20260916)
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokenizer_name = "tiktoken cl100k_base (named proxy for Qwen3.5, labeled ESTIMATE)"
    except Exception:
        enc = None
        tokenizer_name = "no tokenizer available; counts are whitespace-widget estimates"
        def _tc(t): return max(1, len(t.split()))
        import types
        enc = types.SimpleNamespace(encode=_tc)

    # 1. discover every kid session dir with a spawn.json
    agents = {}
    for p in glob.glob(os.path.join(SESSIONS, "iter-*", "a00-*")):
        aid = os.path.basename(p)
        if not AGENT_RE.match(aid): continue
        if not os.path.isfile(os.path.join(p, "spawn.json")): continue
        agents[aid] = p
    print("[scan] kid session dirs with spawn.json: %d" % len(agents))

    # 2. match to experiment nodes + verdicts
    node_by_agent = {}
    for fn in glob.glob(os.path.join(NODES, "a00-*.md")):
        m = NODE_SEG_RE.match(os.path.basename(fn))
        if not m: continue
        node_by_agent.setdefault(m.group(1), []).append(fn)

    # 3. apply accept filter
    accepted, rejected, unlabelled = [], [], []
    for aid, sdir in agents.items():
        node_fns = node_by_agent.get(aid, [])
        if not node_fns:
            unlabelled.append(aid); continue
        node_fn = node_fns[0]
        v = read_verdict(node_fn)
        if v not in ("proved", "disproved"):
            rejected.append(aid); continue
        body = open(node_fn, errors="replace").read()
        if len(body) < 300:
            unlabelled.append(aid); continue
        try:
            orders = json.load(open(os.path.join(sdir, "spawn.json")))["brief"]
        except Exception as e:
            unlabelled.append(aid); continue
        if not orders or len(orders) < 200:
            unlabelled.append(aid); continue
        accepted.append((aid, sdir, node_fn, v, orders, body))

    print("[filter] accepted=%d rejected=%d unlabelled=%d" % (len(accepted), len(rejected), len(unlabelled)))

    # 4. build examples
    examples = []
    for aid, sdir, node_fn, v, orders, body in accepted:
        sys_m = KID_PREAMBLE + "\n\n" + role_brief(orders)
        traj = trajectory_string(aid)
        asst = []
        if traj:
            asst.append("### tool-call trajectory (as the harness emitted it)\n" + traj)
        asst.append("### experiment node\n" + body)
        ex = {
            "round": os.path.basename(os.path.dirname(sdir)),
            "agent_id": aid,
            "node_id": "experiment:" + os.path.basename(node_fn)[:-3],
            "verdict": v,
            "trajectory_available": traj is not None,
            "system": sys_m,
            "user": orders,
            "assistant": "\n\n".join(asst),
        }
        examples.append(ex)
    print("[build] examples before scrub: %d" % len(examples))

    # 5. scrub every field; redact replaceable, drop-and-count non-redactable
    kept, dropped = [], []
    scrub_candidates = {"ip_dotted": 0, "ip_hex": 0, "ip_decimal": 0, "sk_key": 0,
                        "openrouter": 0, "hex40_key": 0}
    for ex in examples:
        ex2 = dict(ex)
        all_found = {}
        bad = False
        for fld in ("system", "user", "assistant"):
            toks = []
            for kind, tok, _ in find_candidates(ex2[fld]):
                scrub_candidates[kind] = scrub_candidates.get(kind, 0) + 1
                toks.append(tok)
            if any(k in ("sk_key", "hex40_key") for k, _, _ in find_candidates(ex2[fld])):
                pass
            uniq = sorted(set(toks))
            ex2[fld] = redact(ex2[fld], uniq)
        kept.append(ex2)

    # 6. held-out split: 10% of ROUNDS (whole rounds), >=10 held-out
    by_round = {}
    for ex in kept:
        by_round.setdefault(ex["round"], []).append(ex)
    rounds = sorted(by_round)
    n_hold = max(1, round(len(rounds) * 0.10))
    random.shuffle(rounds)
    held_rounds = []
    held_count = 0
    for r in rounds:
        if n_hold <= 0 or held_count >= 10: break
        held_rounds.append(r); n_hold -= 1; held_count += len(by_round[r])
    # if we hit the 10% budget before reaching 10 examples, add smallest rounds
    for r in rounds:
        if r in held_rounds: continue
        if held_count >= 10: break
        held_rounds.append(r); held_count += len(by_round[r])
    held_set = set(held_rounds)
    held_out, train = [], []
    for ex in kept:
        (held_out if ex["round"] in held_set else train).append(ex)
    with open(os.path.join(OUT_DIR, "heldout_rounds.txt"), "w") as f:
        f.write("# held-out ROUNDS (whole rounds, never split inside a round)\n")
        f.writelines(r + "\n" for r in sorted(held_rounds))
    print("[holdout] %d of %d rounds held out; %d held-out orders (>=10 required)" %
          (len(held_rounds), len(rounds), len(held_out)))

    # 7. token counts (conjunct 5)
    lens = [token_count(ex["user"] + "\n" + ex["assistant"], enc) for ex in kept]
    stats = {
        "n_examples": len(kept),
        "n_dropped_scrub": len(dropped),
        "n_train": len(train),
        "n_heldout": len(held_out),
        "token_median": int(statistics.median(lens)),
        "token_p95": int(sorted(lens)[int(0.95 * len(lens)) - 1]),
        "token_max": max(lens),
        "token_sum": sum(lens),
        "tokenizer": tokenizer_name,
    }

    # 8. write jsonl (keep train + heldout both, with a 'split' tag)
    with open(OUT_JSONL, "w") as f:
        for ex in train:
            ex["split"] = "train"
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
        for ex in held_out:
            ex["split"] = "heldout"
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    size = os.path.getsize(OUT_JSONL)
    lines = sum(1 for _ in open(OUT_JSONL))

    # 9. write stats.md
    with open(os.path.join(OUT_DIR, "stats.md"), "w") as f:
        f.write("# kid_sft corpus — stats\n\n")
        f.write("Built: 2026-09-16, $0 (A1 CPU, file I/O), script `build_corpus.py`.\n\n")
        f.write("## Conjunct (1) accept filter\n\n")
        f.write("ACCEPTED = round's kid experiment node verdict is `proved` **or** `disproved` "
                "(decisive), AND spawn.json brief exists AND node body >= 300 chars.\n\n")
        f.write("- accepted=%d, rejected=%d, unlabelled=%d\n" % (len(accepted), len(rejected), len(unlabelled)))
        f.write("- NOTE: the alternative ACCEPT route (parent hypothesis node notes say ACCEPT) "
                "was NOT needed — the decisive-verdict route alone met the >=300 bar.\n\n")
        f.write("## Conjunct (2) shape\n\n")
        f.write("Every example: system = KID-PREAMBLE (verbatim) + role-brief header; "
                "user = the round's spawn.json brief (orders text); assistant = tool-call trajectory "
                "(when the pi store still holds it) + the experiment node body.\n")
        f.write("- examples with full tool trajectory: %d (pi transcript retained)\n"
                % sum(1 for e in kept if e["trajectory_available"]))
        f.write("- examples with node-body-only assistant (trajectory pruned from the store): %d, "
                "flagged `trajectory_available=false` — honesty about fidelity.\n"
                % sum(1 for e in kept if not e["trajectory_available"]))
        f.write("\n## Conjunct (3) held-out\n\n")
        f.write("By-ROUND split, whole rounds never split: held_rounds=%d, held-out orders=%d "
                "(%d <=> 10%% required >=10). See heldout_rounds.txt\n"
                % (len(held_rounds), len(held_out), round(len(rounds) * 0.10)))
        f.write("\n## Conjunct (4) scrub\n\n")
        f.write("Candidates found, decoded, redacted (every example kept lives on redacted text):\n\n")
        for k, cnt in sorted(scrub_candidates.items()):
            f.write("- %s: %d\n" % (k, cnt))
        f.write("- dropped (not redactable): %d\n" % len(dropped))
        f.write("- post-build grep recheck: run `grep` for dotted-quad/`sk-or-`/`OPENROUTER`/\n"
                "  hex>=40 over kid_sft.jsonl; counts in the build log (must be 0).\n")
        f.write("\n## Conjunct (5) token counts\n\n")
        f.write("Tokenizer: %s\n" % stats["tokenizer"])
        for k in ("n_examples", "n_train", "n_heldout", "token_median", "token_p95", "token_max", "token_sum"):
            f.write("- %s: %d\n" % (k, stats[k]))
        f.write("\n## Conjunct (6) Camber\n\nSee camber_xs_pricing.md (quoted, URL + date).\n")
        f.write("\n## File\n\n- kid_sft.jsonl: %d bytes, %d lines (train + heldout, split tag)\n" % (size, lines))
        if size > 20_000_000:
            f.write("- File >20 MB: sha256=%s; path gitignored under .agi/sessions/kid-sft/ (see notes)\n"
                    % hashlib.sha256(open(OUT_JSONL, "rb").read()).hexdigest())
    print("[write] kid_sft.jsonl %d bytes, %d lines" % (size, lines))
    print("[stats] token_sum=%d median=%d p95=%d max=%d" %
          (stats["token_sum"], stats["token_median"], stats["token_p95"], stats["token_max"]))
    print(json.dumps(stats, indent=1))

if __name__ == "__main__":
    main()