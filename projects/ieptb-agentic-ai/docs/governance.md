# AI Governance Model

## Risk classification

| Capability | Risk | Control |
|---|---:|---|
| Read public procedure | Low | Retrieval allow-list |
| Analyze synthetic remessa | Medium | Validation + audit |
| Access restricted data | High | RBAC + policy |
| Modify enterprise record | Critical | Human approval + dual control |
| Release financial/operational action | Critical | Deterministic gate + human approval |

## Governance controls
1. Data minimization.
2. Purpose limitation.
3. Least privilege.
4. Human oversight.
5. Evidence citation.
6. Audit trail.
7. Model/version traceability.
8. Evaluation before release.
9. Security regression tests.
10. Incident response.

## Model card fields
Every deployed model configuration should record:
- provider/model
- version
- system prompt version
- retrieval configuration
- tool policy version
- evaluation dataset version
- approval date
- known limitations

## Decision policy
The AI layer may recommend an action. It may not silently execute a high-impact action merely because the model produced a high-confidence response.
