# AYORAI Vision Intelligence — Architecture

## Design principle

**Separate perception, deterministic decisions and reasoning.**

### 1. Perception

Computer Vision models produce object detections and tracking information.

### 2. Decision

The confidence engine determines whether an event is automatically accepted, routed to Human-in-the-Loop review, or rejected.

### 3. Tool layer

MCP exposes explicit, auditable operations such as track history, low-confidence events and annotation export.

### 4. Knowledge layer

RAG provides versioned domain context to the reasoning layer.

### 5. Agent layer

The AI orchestrator selects tools and combines retrieved context with structured vision events.

### 6. Automation

RPA watches input locations and initiates processing/reporting workflows.

## Data flow

```
Video
  ↓
Detection
  ↓
Tracking
  ↓
Confidence
  ↓
Human Review
  ↓
Structured Events
  ↓
MCP + RAG
  ↓
Agent
  ↓
Dashboard / Report / Dataset
```

## Privacy and security

For regulated environments, raw video and personal data must remain outside the public Git repository. Prefer local/private processing where required, enforce retention policies, authenticate operators and maintain an audit trail.
