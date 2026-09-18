# AYORAI Vision Intelligence

> Agentic Computer Vision platform for object detection, persistent tracking, uncertainty-aware annotation, Human-in-the-Loop review, MCP tools, RAG and RPA orchestration.

## Architecture

```
Video / RTSP
    |
    v
Computer Vision -> Detection -> Multi-Object Tracking
    |                         |
    +---- Confidence ----------+
              |
              v
      Human-in-the-Loop
              |
              v
       FastAPI / MCP
          |       |
         RAG    Tools
          \       /
           GPT-6 Astra*
              |
              v
     Dashboard / Reports / Dataset

* Astra is treated as the reasoning/orchestration layer; detection and tracking
  remain explicit computer-vision components.
```

## Engineering goals

- Reduce manual annotation effort through automation.
- Preserve persistent IDs across frames.
- Route uncertain detections to human review instead of silently accepting them.
- Expose operational capabilities as MCP tools.
- Ground agent responses in domain documentation through RAG.
- Automate ingestion and reporting with RPA workflows.
- Keep the system observable, testable and container-ready.

## Repository structure

```
src/
  vision/      detection, tracking and confidence logic
  mcp/         MCP tool contracts
  rag/         retrieval interfaces
  agents/      orchestration contracts
  api/         FastAPI application
  rpa/         ingestion automation
tests/
docs/
.github/workflows/
```

## Status

This repository starts with a production-oriented architecture and deterministic MVP contracts. Model providers, trackers, vector stores and external MCP runtimes are isolated behind interfaces so they can be replaced without rewriting the application core.

## Security

No credentials, private videos or regulated personal data belong in Git. Use `.env` locally and keep real operational data outside the repository.

## Author

**Anderson Leon Ayora — AI Engineer | Applied AI · Document Intelligence · Generative AI · Intelligent Automation**

Part of the AYORAI engineering portfolio.
