from enum import StrEnum

class ConfidenceAction(StrEnum):
    AUTO_ACCEPT = "auto_accept"
    HUMAN_REVIEW = "human_review"
    REJECT = "reject"

def classify_confidence(
    confidence: float,
    review_threshold: float = 0.70,
    auto_accept_threshold: float = 0.90,
) -> ConfidenceAction:
    if confidence >= auto_accept_threshold:
        return ConfidenceAction.AUTO_ACCEPT
    if confidence >= review_threshold:
        return ConfidenceAction.HUMAN_REVIEW
    return ConfidenceAction.REJECT
