"""oMLX local provider (OpenAI-compatible Chat Completions)."""

from __future__ import annotations

from typing import Any

from core.anthropic import ReasoningReplayMode, build_base_request_body
from core.anthropic.conversion import OpenAIConversionError
from providers.base import ProviderConfig
from providers.defaults import OMLX_DEFAULT_BASE
from providers.exceptions import InvalidRequestError
from providers.openai_compat import OpenAIChatTransport


class OmlxProvider(OpenAIChatTransport):
    """oMLX provider using OpenAI-compatible ``/chat/completions`` endpoint."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="OMLX",
            base_url=config.base_url or OMLX_DEFAULT_BASE,
            api_key=config.api_key,
        )

    def _build_request_body(
        self, request: Any, thinking_enabled: bool | None = None
    ) -> dict:
        try:
            return build_base_request_body(
                request,
                reasoning_replay=ReasoningReplayMode.REASONING_CONTENT,
            )
        except OpenAIConversionError as exc:
            raise InvalidRequestError(str(exc)) from exc
