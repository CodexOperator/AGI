# Deferred optimization ideas (autoresearch tree)

## Graph load time (graph_core)

### ✅ PROVED: C-based YAML parser (CSafeLoader) in frontmatter.py
- Replaced `yaml.safe_load()` with `yaml.load(text, Loader=CSafeLoader)` in `_parse_md`
- Cold load 1178ms → 298ms (-74.7%)
- Adds graceful fallback: `yaml.CSafeLoader` → `yaml.SafeLoader`
- Engine edit, graph_core/persistence/frontmatter.py

### Stale ideas (from old GraphDomain codebase — deleted/migrated)
- ~~Second-pass file re-reads in parsers (parse_tasks, parse_skills, etc.)~~ — old code
- ~~Lazy _precompute_key_paths~~ — old code
- ~~add_node dedup optimization~~ — old code
- ~~_cache_ver bump convention~~ — old code, not applicable to new architecture