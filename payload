# agi-bridge

Pi extension that injects `context/INJECTION.md` (the agi-tree graph map) into
the agent's system prompt on every `before_agent_start` event, refreshing the
map per-agent-turn so each iteration of the loop sees an up-to-date graph after
the previous commit.

## Behavior

1. Walks up from `ctx.cwd` to find `agi-tree.config.json` (legacy name
   `autoresearch-tree.config.json` still resolves). If absent, the hook is a
   no-op (safe to install globally).
2. If `<projectRoot>/context/INJECTION.md` is missing or older than 5 minutes,
   re-renders it via `python3 <pluginRoot>/bin/snapshot-build-site.py` then
   `python3 <pluginRoot>/bin/render-context.py <projectRoot>/nodes`, with
   `AGI_TREE_PROJECT_ROOT=<projectRoot>` in env (and the legacy
   `AUTORESEARCH_TREE_PROJECT_ROOT` alongside it during the rename window).
3. Appends the first 80 lines of `INJECTION.md` to `event.systemPrompt`,
   prefixed with a header carrying an iter count (from `sessions/` dir count).

All steps are try/catch wrapped; failures degrade silently to no-op via
`ctx.ui.notify({ level: "debug" })`.

## Discovery

Pi discovers this extension via the parent repo's `package.json`:
`{ "pi": { "extensions": ["./extensions"] } }`. Both
`extensions/agi/` and `extensions/agi-bridge/` are picked up automatically.

## Plugin root resolution

`$AGI_TREE_PLUGIN_ROOT` (legacy: `$AUTORESEARCH_TREE_PLUGIN_ROOT`) → sibling
extension dir from `import.meta.url` → fallback `~/.hermes/agi/extensions/agi`.
