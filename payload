// Inline workflow that started life in a session scratch dir (Belam S1, L3.40).
// Registered as it runs so it survives the session; dispatched via workflow.py run.
export const meta = {
  name: 'l3w-route-probe',
  description: 'Two-stage probe: emit each target, then a critic pass',
  phases: [{ title: 'Emit' }, { title: 'Critic' }],
}
const MODEL = (args && args.model) || 'sonnet'
const EFFORT = (args && args.effort) || 'low'
const EMIT_SCHEMA = { type: 'object', properties: { slug: { type: 'string' }, ok: { type: 'boolean' } }, required: ['slug', 'ok'] }
const CRITIC_SCHEMA = { type: 'object', properties: { ok: { type: 'boolean' } }, required: ['ok'] }
phase('Emit')
const emitted = await parallel(TARGETS.map(t => agent(`Emit a JSON verdict for slug ${t.slug}.`, { label: `emit:${t.slug}`, phase: 'Emit', schema: EMIT_SCHEMA, model: MODEL, effort: EFFORT }))).filter(Boolean)
phase('Critic')
const critic = await agent(`You are the critic. Check the ${emitted.length} emissions. Return {ok}.`, { label: 'critic', phase: 'Critic', schema: CRITIC_SCHEMA, model: MODEL, effort: EFFORT })
log(`${emitted.length} emissions`)
