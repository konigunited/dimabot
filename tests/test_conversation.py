from bot.conversation import ConversationFlow, Step, build_default_flow


def test_conversation_flow_iterates_steps_in_order():
    steps = [
        Step(title="A", body="1"),
        Step(title="B", body="2"),
        Step(title="C", body="3"),
    ]
    flow = ConversationFlow(steps, "https://example.com")

    assert flow.first() == steps[0]
    assert flow.next_step(0) == steps[1]
    assert flow.next_step(1) == steps[2]
    assert flow.next_step(2) is None
    assert flow.is_last(2)
    assert flow.final_link == "https://example.com"


def test_build_default_flow_uses_given_final_link():
    final_link = "https://example.org/final"
    flow = build_default_flow(final_link)

    assert flow.first().title == "Добро пожаловать!"
    assert flow.final_link == final_link
    assert flow.next_step(len(flow.steps) - 1) is None


def test_conversation_requires_at_least_one_step():
    try:
        ConversationFlow([], "https://example.com")
    except ValueError as exc:
        assert "at least one step" in str(exc)
    else:  # pragma: no cover - defensive branch
        raise AssertionError("Expected ValueError for empty steps list")
