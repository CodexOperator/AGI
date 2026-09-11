export const meta = {
  name: "agi-desktop-check",
  description: "Screenshot DISPLAY=:1 (xfce4-screenshooter) and READ it: per visible seat view \u2014 idle/busy, unsubmitted input text (stranded nudges), last activity, errors \u2014 plus desktop leaks; recommends, never acts. Args: {focus}. Authored via workflow.py author (Prime L4-VII, owner 2026-09-11 02:1xZ: the panes stay up, check screenshots as needed).",
  phases: [
    { title: "Capture-and-read" },
  ],
}

const MODEL = (args && args.model) || "sonnet"
const EFFORT = (args && args.effort) || "medium"

const fill = (t, ctx) => String(t).replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_, k) => (k in ctx && ctx[k] != null ? ctx[k] : ''))

const CAPTURE_AND_READ_TMPL = "You check the live X desktop (DISPLAY=:1) of the agi box by SCREENSHOT \u2014 the tmux panes of the seats stay on screen as read-only views. READ-ONLY: never type into a pane, never send keys, never touch tmux, the stream unit (streamer-stub.service) or any window; you look and report. Steps: (1) `mkdir -p /home/ubuntu/work/agi/.agi/sessions/screens` then capture with `DISPLAY=:1 xfce4-screenshooter -f -s /home/ubuntu/work/agi/.agi/sessions/screens/desktop-$(date -u +%Y%m%dT%H%M%SZ).png` (fallback: `DISPLAY=:1 xwd -root -out <path>.xwd` and convert with Python PIL if xfce4-screenshooter is missing). (2) Read the PNG with the Read tool (it renders images). (3) For every visible terminal view report: which seat/window it shows (the title or the prompt line names it), whether it looks idle (an empty `\u276f` prompt) or busy (a spinner, `esc to interrupt`), any text sitting UNSUBMITTED in the input box (a `\u276f` line with content and no response below it \u2014 the stranded-nudge defect), the last visible activity line, and any error or red line. (4) Also note desktop-level facts: panels visible, hostname/user/clock leaks, popups, a view that is black or missing. Focus from the caller: {focus}. (5) Recommend ONE action per finding (for example `tmux send-keys -t agi-rc:@NNN Enter` for a stranded line) but DO NOT execute any of them \u2014 the Prime decides. Return ONLY the structured result."
const CAPTURE_AND_READ_SCHEMA = {"type": "object", "properties": {"screenshot_path": {"type": "string"}, "panes": {"type": "array", "items": {"type": "object", "properties": {"view": {"type": "string"}, "state": {"type": "string", "enum": ["idle", "busy", "unknown", "missing"]}, "stranded_input": {"type": "string"}, "last_activity": {"type": "string"}, "errors": {"type": "string"}, "recommended_action": {"type": "string"}}, "required": ["view", "state", "stranded_input", "last_activity", "errors", "recommended_action"]}}, "desktop_notes": {"type": "array", "items": {"type": "string"}}, "summary": {"type": "string"}}, "required": ["screenshot_path", "panes", "desktop_notes", "summary"]}
phase("Capture-and-read")
const r0 = await agent(fill(CAPTURE_AND_READ_TMPL, args), { label: "capture-and-read", phase: "Capture-and-read", schema: CAPTURE_AND_READ_SCHEMA, model: MODEL, effort: EFFORT })

return { "capture-and-read": r0 }
