# Human-in-the-Loop

The review policy is intentionally explicit:

- confidence >= 0.90: automatic acceptance
- 0.70 <= confidence < 0.90: human review
- confidence < 0.70: rejection / reprocessing candidate

These thresholds are engineering defaults for the MVP, not measured production results. Production thresholds must be calibrated against a representative validation dataset.

Every human decision should become an auditable event containing:

- track ID
- original prediction
- confidence
- reviewer
- decision
- timestamp
- optional correction
