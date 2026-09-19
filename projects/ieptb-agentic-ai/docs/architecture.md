# Architecture Decision Record

## 1. Architecture goals
- Production-oriented Python service boundaries.
- Evidence-grounded answers.
- Least-privilege agent tools.
- Human-in-the-loop for consequential operations.
- Full traceability from request to decision.
- Replaceable model/provider layer.

## 2. Agent roles

### Retrieval Agent
Retrieves approved procedures, schemas and rule documents. It cannot mutate enterprise systems.

### Validation Agent
Combines retrieved evidence with deterministic rules to explain validation results. It cannot approve or release a remessa.

### Integration Agent
Uses allow-listed tools to simulate enterprise integrations. Every tool call requires authorization and is logged.

### Audit Agent
Produces a structured audit summary from the execution trace. It has read-only access.

## 3. Tool boundary

Agents never receive unrestricted database or filesystem access.

```text
Agent
  -> Tool Policy
      -> RBAC
          -> Input validation
              -> Allow-listed adapter
                  -> Audit event
```

## 4. Data flow

```text
Input -> validation -> classification -> retrieval -> reasoning
      -> policy checks -> human approval -> integration -> audit
```

## 5. Failure containment
- Tool timeout
- Retry budget
- Circuit breaker
- Maximum agent steps
- Token budget
- Retrieval minimum score
- Human escalation
- Deny-by-default permissions

## 6. Production evolution
A production deployment would add:
- managed secrets
- private networking
- SSO
- enterprise identity
- managed vector database
- centralized observability
- model gateway
- disaster recovery
- formal DPIA/security review
- load testing
- change-management controls
