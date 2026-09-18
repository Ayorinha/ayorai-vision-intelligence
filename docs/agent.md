# Agent architecture

The agent boundary is evidence-first:

1. receive objective;
2. retrieve local knowledge;
3. expose registered tools;
4. return evidence and tool availability;
5. optionally connect a local/private LLM provider.

This avoids presenting an unverified model integration as production capability. The orchestration contract is ready for an LLM adapter.
