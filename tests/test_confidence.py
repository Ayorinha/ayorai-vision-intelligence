from src.vision.confidence import ConfidenceAction, classify_confidence

def test_high_confidence_is_auto_accepted():
    assert classify_confidence(0.95) == ConfidenceAction.AUTO_ACCEPT

def test_medium_confidence_requires_human_review():
    assert classify_confidence(0.80) == ConfidenceAction.HUMAN_REVIEW

def test_low_confidence_is_rejected():
    assert classify_confidence(0.40) == ConfidenceAction.REJECT
