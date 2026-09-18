# Architecture Decision Record

## Core principle

Separate reasoning from perception.

### Perception
Computer Vision models detect objects and produce detections/tracks.

### Decision layer
Confidence policies determine whether a detection is automatically accepted, sent to Human-in-the-Loop review, or rejected.

### Agent layer
An Astra-class reasoning model orchestrates tools and retrieves domain context. The model does not replace deterministic CV components.

### MCP
MCP exposes safe, explicit operations such as track history, low-confidence events and dataset export.

### RAG
RAG grounds operational explanations in versioned documentation.

### RPA
RPA monitors inputs and triggers processing/reporting workflows.

## Data flow

Video -> Detection -> Tracking -> Confidence -> Review -> Events -> RAG/MCP -> Agent -> Report.

## Privacy

For regulated environments, keep raw video and personal data outside the public repository. Prefer local processing and explicit retention policies.
