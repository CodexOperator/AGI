#!/usr/bin/env node
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import contextTrim from "./a00-54d3d9b0-context-trim.js";

const root = process.cwd();
const config = JSON.parse(readFileSync(resolve(root, ".agi/config.json"), "utf8"));
const out = resolve(root, config.paths.local_maxxing.brain_swap_out_dir);
const marker = "ASSISTANT_MARKER_TEXT";
const system = "s".repeat(26600);
const messages = [
  { role: "assistant", content: [{ type: "text", text: marker }] },
  { role: "toolResult", content: [{ type: "text", text: "x".repeat(100000) }] },
  { role: "toolResult", content: [{ type: "text", text: "y".repeat(100000) }] },
];
let handler;
contextTrim({ on(name, callback) { if (name === "context") handler = callback; } });
const result = handler({ messages: structuredClone(messages) }, {
  getContextUsage: () => null,
  getSystemPrompt: () => system,
});
const returned = result.messages;
const placeholder = returned[1].content[0].text;
const estimate = (JSON.stringify(returned).length + system.length) / 4;
const brief = text => text.length > 40 ? `${JSON.stringify(text.slice(0, 40))} (length ${text.length})` : JSON.stringify(text);
const checks = [
  ["a length", returned.length === messages.length, `${returned.length} === 3`],
  ["b roles", JSON.stringify(returned.map(m => m.role)) === JSON.stringify(messages.map(m => m.role)), JSON.stringify(returned.map(m => m.role))],
  ["c assistant", returned[0].content[0].text === marker, JSON.stringify(returned[0].content[0].text)],
  ["d placeholders", returned[1].content[0].text === placeholder && returned[2].content[0].text === placeholder, JSON.stringify([brief(returned[1].content[0].text), brief(returned[2].content[0].text)])],
  ["e estimate", estimate < 43616, `${estimate} < 43616`],
];
let ok = true;
const output = checks.map(([name, passed, value]) => { ok &&= passed; return `${passed ? "PASS" : "FAIL"} ${name}: ${value}`; }).join("\n") + `\nexit=${ok ? 0 : 1}\n`;
mkdirSync(out, { recursive: true });
writeFileSync(resolve(out, "a00-21b0d141-context-trim-fallback.stdout.txt"), output);
process.stdout.write(output);
if (!ok) process.exitCode = 1;
