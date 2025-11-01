"""Conversation flow used both in runtime and unit tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class Step:
    """Single step of the onboarding flow."""

    title: str
    body: str


class ConversationFlow:
    """Simple helper that tracks the user onboarding journey."""

    def __init__(self, steps: Iterable[Step], final_link: str) -> None:
        self._steps: List[Step] = list(steps)
        if not self._steps:
            raise ValueError("Conversation must contain at least one step")
        self._final_link = final_link

    @property
    def steps(self) -> List[Step]:
        return list(self._steps)

    @property
    def final_link(self) -> str:
        return self._final_link

    def first(self) -> Step:
        return self._steps[0]

    def next_step(self, current_index: int) -> Step | None:
        next_index = current_index + 1
        if next_index >= len(self._steps):
            return None
        return self._steps[next_index]

    def is_last(self, index: int) -> bool:
        return index >= len(self._steps) - 1


DEFAULT_STEPS: List[Step] = [
    Step(
        title="Добро пожаловать!",
        body=(
            "Я помогу вам пройти короткий onboarding. Нажимайте \"Далее\" после"
            " прочтения каждого шага."
        ),
    ),
    Step(
        title="Расскажите о себе",
        body=(
            "Мы собрали для вас полезные материалы по запуску. После ознакомления"
            " переходите к финальному шагу."
        ),
    ),
    Step(
        title="Почти готово",
        body="Нажмите \"Получить ссылку\", чтобы перейти к финальному ресурсу.",
    ),
]


def build_default_flow(final_link: str) -> ConversationFlow:
    """Create a flow with opinionated onboarding copy."""

    return ConversationFlow(DEFAULT_STEPS, final_link)
