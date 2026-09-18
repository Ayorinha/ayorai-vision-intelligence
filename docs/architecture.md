# Architecture

## Runtime flow

1. RPA discovers an input video and creates a job.
2. The vision pipeline runs YOLO detection and tracking.
3. Each detection receives a persistent track identifier when the model provides one.
4. Confidence routing classifies the detection.
5. Uncertain detections create a Human-in-the-Loop review item.
6. Detections, reviews and events are persisted to SQLite.
7. The controlled tool gateway exposes operational actions.
8. RAG retrieves synthetic operational guidance.
9. The agent boundary combines objective, evidence and tools.
10. Dashboard operators inspect jobs and review uncertain detections.

## Responsibility boundaries

- **Computer Vision:** perception.
- **Tracking:** temporal identity.
- **Confidence engine:** deterministic routing.
- **Database:** durable state.
- **RAG:** contextual evidence.
- **Tool registry:** controlled actions.
- **Agent:** reasoning/orchestration boundary.
- **RPA:** process automation.
- **FastAPI:** service interface.
- **Dashboard:** human interaction.

The reasoning layer is deliberately not presented as the detector or tracker.
