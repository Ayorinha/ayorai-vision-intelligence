# ADR-002: Treat retrieved content as untrusted

Retrieved documents are evidence, not instructions. Retrieval results cannot grant permissions, override policy, or authorize tools.

This protects against indirect prompt injection and poisoned knowledge sources.
