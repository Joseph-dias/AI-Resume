from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from xai_sdk import AsyncClient
from xai_sdk.chat import system, user


class AIHandler:
    def __init__(
        self,
        model: str = "grok-3",
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        load_dotenv()
        self._client = AsyncClient()
        self._model = model
        self._system_prompt = system_prompt
        self._history: list = []

    def set_system_prompt(self, prompt: str) -> None:
        self._system_prompt = prompt

    def reset(self) -> None:
        self._history = []

    async def stream(self, user_message: str) -> AsyncGenerator[str, None]:
        chat = self._client.chat.create(model=self._model)
        chat.append(system(self._system_prompt))
        for msg in self._history:
            chat.append(msg)
        user_msg = user(user_message)
        chat.append(user_msg)

        final_response = None
        async for response, chunk in chat.stream():
            final_response = response
            yield chunk.content

        self._history.append(user_msg)
        if final_response is not None:
            self._history.append(final_response)

    async def chat(self, user_message: str) -> str:
        return "".join([chunk async for chunk in self.stream(user_message)])
