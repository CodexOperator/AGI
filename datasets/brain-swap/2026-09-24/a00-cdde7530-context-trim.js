const LIMIT = 60000 - 16384, MARK = "[older tool result elided]";
export default function contextTrim(pi) {
  pi.on("context", ({ messages }) => {
    const trimmed = messages.map((message) => ({ ...message }));
    if (JSON.stringify(trimmed).length / 4 < LIMIT) return;
    for (const message of trimmed) {
      if (message.role !== "toolResult" || message.content?.[0]?.text === MARK) continue;
      message.content = [{ type: "text", text: MARK }];
      if (JSON.stringify(trimmed).length / 4 < LIMIT) break;
    }
    return { messages: trimmed };
  });
}
