const MARK = "[older tool result elided]";
export default function contextTrim(pi) {
  pi.on("context", (event, ctx) => {
    let { messages } = event;
    const usage = ctx.getContextUsage();
    const limit = (usage?.contextWindow ?? 60000) - 16384;
    const estimate = () => (JSON.stringify(messages).length + ctx.getSystemPrompt().length) / 4;
    if ((usage?.tokens ?? estimate()) < limit) return;
    messages = messages.map((message) => structuredClone(message));
    for (const message of messages) {
      if (message.role !== "toolResult" || message.content?.[0]?.text === MARK) continue;
      message.content = [{ type: "text", text: MARK }];
      if (estimate() < limit) break;
    }
    return { messages };
  });
}
