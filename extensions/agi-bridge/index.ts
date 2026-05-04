/**
 * autoresearch-tree-bridge — Pi Extension
 *
 * Injects the autoresearch-tree graph map (context/INJECTION.md) into the
 * agent's system prompt on every `before_agent_start` event, so each iteration
 * of an autoresearch-create loop sees a fresh map after the previous commit.
 *
 * No-op outside autoresearch-tree projects (no autoresearch-tree.config.json
 * found by walking up from ctx.cwd).
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import * as fs from "node:fs";
import * as path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const FRESH_MS = 5 * 60 * 1000; // 5 min
const INJECTION_LINES = 80;

console.log("[autoresearch-tree-bridge] loaded");

/** Walk up from `start` looking for autoresearch-tree.config.json. */
function findProjectRoot(start: string): string | null {
  let d = path.resolve(start);
  while (d !== path.dirname(d)) {
    if (fs.existsSync(path.join(d, "autoresearch-tree.config.json"))) return d;
    d = path.dirname(d);
  }
  return null;
}

/** Resolve plugin root (where bin/snapshot-build-site.py lives). */
function findPluginRoot(): string | null {
  if (process.env.AUTORESEARCH_TREE_PLUGIN_ROOT) {
    return process.env.AUTORESEARCH_TREE_PLUGIN_ROOT;
  }
  // Walk up from this file looking for sibling extension dir
  // (extensions/autoresearch-tree-bridge -> extensions/autoresearch-tree)
  try {
    const here = path.dirname(fileURLToPath(import.meta.url));
    const sibling = path.resolve(here, "..", "autoresearch-tree");
    const pkg = path.join(sibling, "..", "..", "package.json");
    if (fs.existsSync(pkg)) {
      const parsed = JSON.parse(fs.readFileSync(pkg, "utf8"));
      if (parsed?.name === "autoresearch-tree" && fs.existsSync(sibling)) {
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
    "autoresearch-tree",
    "extensions",
    "autoresearch-tree",
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
  const env = { ...process.env, AUTORESEARCH_TREE_PROJECT_ROOT: projectRoot };
  const opts = { env, cwd: projectRoot, timeout: 30_000 } as const;
  spawnSync("python3", [path.join(pluginRoot, "bin", "snapshot-build-site.py")], opts);
  spawnSync(
    "python3",
    [path.join(pluginRoot, "bin", "render-context.py"), path.join(projectRoot, "nodes")],
    opts,
  );
}

export default function autoresearchTreeBridge(pi: ExtensionAPI): void {
  pi.on("before_agent_start", async (event, ctx) => {
    try {
      const projectRoot = findProjectRoot(ctx.cwd);
      if (!projectRoot) return undefined; // not an autoresearch-tree project

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
            message: "[autoresearch-tree-bridge] plugin root not found; skipping refresh",
          });
        } else {
          try {
            refreshInjection(pluginRoot, projectRoot);
          } catch (e) {
            ctx.ui?.notify?.({
              level: "debug",
              message: `[autoresearch-tree-bridge] refresh failed: ${
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
      const header = `## autoresearch-tree map (auto-injected, refreshed iter-${iter})\n\n`;
      const block = header + first;

      return {
        systemPrompt: (event.systemPrompt ?? "") + "\n\n" + block,
      };
    } catch (e) {
      try {
        ctx.ui?.notify?.({
          level: "debug",
          message: `[autoresearch-tree-bridge] error: ${
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
