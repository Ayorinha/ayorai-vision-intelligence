from src.policy import Risk, authorize


def test_critical_actions_require_human():
    decision = authorize("release", Risk.CRITICAL)
    assert decision.allowed is False
    assert decision.requires_human is True


def test_unknown_action_is_denied():
    decision = authorize("delete_everything", Risk.HIGH)
    assert decision.allowed is False
