/**
 * agi-bridge — Pi Extension
 *
 * Injects the agi thoughtgraph map (context/INJECTION.md) into the
 * agent's system prompt on every `before_agent_start` event, so each iteration
 * of the loop sees a fresh map after the previous commit.
 *
 * No-op outside agi-tree projects (no agi-tree.config.json found by walking up
 * from ctx.cwd; the legacy name autoresearch-tree.config.json also resolves).
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import * as fs from "node:fs";
import * as path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const FRESH_MS = 5 * 60 * 1000; // 5 min
const INJECTION_LINES = 80;

console.log("[agi-bridge] loaded");

/** Canonical name first; the legacy name stays accepted during the rename window. */
const CONFIG_NAMES = ["agi-tree.config.json", "autoresearch-tree.config.json"];

/** Walk up from `start` looking for agi-tree.config.json. */
function findProjectRoot(start: string): string | null {
  let d = path.resolve(start);
  while (d !== path.dirname(d)) {
    if (CONFIG_NAMES.some((name) => fs.existsSync(path.join(d, name)))) return d;
    d = path.dirname(d);
  }
  return null;
}

/** Resolve plugin root (where bin/snapshot-build-site.py lives). */
function findPluginRoot(): string | null {
  const envRoot =
    process.env.AGI_TREE_PLUGIN_ROOT ?? process.env.AUTORESEARCH_TREE_PLUGIN_ROOT;
  if (envRoot) {
    return envRoot;
  }
  // Walk up from this file looking for sibling extension dir
  // (extensions/agi-bridge -> extensions/agi)
  try {
    const here = path.dirname(fileURLToPath(import.meta.url));
    const sibling = path.resolve(here, "..", "agi");
    const pkg = path.join(sibling, "..", "..", "package.json");
    if (fs.existsSync(pkg)) {
      const parsed = JSON.parse(fs.readFileSync(pkg, "utf8"));
      if (parsed?.name === "agi" && fs.existsSync(sibling)) {
        return sibling;
      }
    }
    if (fs.existsSync(path.join(sibling, "bin", "render-context.py"))) {
      return sibling;
    }
  } catch {
    /* fall through */
  }
  const fallback = path.join(
    process.env.HOME ?? "",
    "agi",
    "extensions",
    "agi",
  );
  return fs.existsSync(fallback) ? fallback : null;
}

/** Count session subdirs to derive an iter count. */
function countIters(projectRoot: string): number {
  try {
    const sessionsDir = path.join(projectRoot, "sessions");
    if (!fs.existsSync(sessionsDir)) return 0;
    return fs
      .readdirSync(sessionsDir, { withFileTypes: true })
      .filter((e) => e.isDirectory()).length;
  } catch {
    return 0;
  }
}

/** Re-render INJECTION.md by shelling out to the python pipeline. */
function refreshInjection(pluginRoot: string, projectRoot: string): void {
  const env = {
    ...process.env,
    AGI_TREE_PROJECT_ROOT: projectRoot,
    AUTORESEARCH_TREE_PROJECT_ROOT: projectRoot, // legacy, rename window
  };
  const opts = { env, cwd: projectRoot, timeout: 30_000 } as const;
  spawnSync("python3", [path.join(pluginRoot, "bin", "snapshot-build-site.py")], opts);
  spawnSync(
    "python3",
    [path.join(pluginRoot, "bin", "render-context.py"), path.join(projectRoot, "nodes")],
    opts,
  );
}

export default function agiBridge(pi: ExtensionAPI): void {
  pi.on("before_agent_start", async (event, ctx) => {
    try {
      const projectRoot = findProjectRoot(ctx.cwd);
      if (!projectRoot) return undefined; // not an agi-tree project

      const injectionPath = path.join(projectRoot, "context", "INJECTION.md");

      // Check freshness; refresh if missing or stale
      let needsRefresh = true;
      try {
        const st = fs.statSync(injectionPath);
        needsRefresh = Date.now() - st.mtimeMs > FRESH_MS;
      } catch {
        needsRefresh = true;
      }

      if (needsRefresh) {
        const pluginRoot = findPluginRoot();
        if (!pluginRoot) {
          ctx.ui?.notify?.({
            level: "debug",
            message: "[agi-bridge] plugin root not found; skipping refresh",
          });
        } else {
          try {
            refreshInjection(pluginRoot, projectRoot);
          } catch (e) {
            ctx.ui?.notify?.({
              level: "debug",
              message: `[agi-bridge] refresh failed: ${
                e instanceof Error ? e.message : String(e)
              }`,
            });
          }
        }
      }

      if (!fs.existsSync(injectionPath)) return undefined;

      const raw = fs.readFileSync(injectionPath, "utf8");
      const first = raw.split("\n").slice(0, INJECTION_LINES).join("\n");
      const iter = countIters(projectRoot);
      const header = `## agi-tree map (auto-injected, refreshed iter-${iter})\n\n`;
      const block = header + first;

      return {
        systemPrompt: (event.systemPrompt ?? "") + "\n\n" + block,
      };
    } catch (e) {
      try {
        ctx.ui?.notify?.({
          level: "debug",
          message: `[agi-bridge] error: ${
            e instanceof Error ? e.message : String(e)
          }`,
        });
      } catch {
        /* ignore notify failure */
      }
      return undefined;
    }
  });
}
