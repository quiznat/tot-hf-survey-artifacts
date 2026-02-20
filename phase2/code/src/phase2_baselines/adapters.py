"""Model adapters for scripted and Hugging Face inference backends."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib import request
from urllib.error import HTTPError, URLError


@dataclass
class ScriptedModel:
    """Deterministic adapter returning pre-scripted responses in order."""

    responses: list[str] = field(default_factory=list)
    fallback: str = ""

    def generate(self, prompt: str) -> str:
        del prompt
        if self.responses:
            return self.responses.pop(0)
        return self.fallback


RequestFunction = Callable[[str, dict[str, Any], dict[str, str], int], Any]


@dataclass
class HuggingFaceInferenceModel:
    """Hugging Face Inference API adapter using plain HTTP requests."""

    model_id: str
    api_token: str
    timeout_seconds: int = 120
    max_new_tokens: int = 192
    temperature: float = 0.0
    top_p: float = 1.0
    endpoint_base: str = "https://router.huggingface.co/v1"
    request_function: RequestFunction | None = None

    def generate(self, prompt: str) -> str:
        endpoint = f"{self.endpoint_base}/chat/completions"
        payload = {
            "model": self.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        response = self._post_json(endpoint, payload, headers)
        output = self._extract_generated_text(response, prompt)
        if not output:
            raise RuntimeError(f"Hugging Face returned empty output for model {self.model_id}")
        return output

    def _post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
        headers: dict[str, str],
    ) -> Any:
        if self.request_function is not None:
            return self.request_function(endpoint, payload, headers, self.timeout_seconds)

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(endpoint, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Hugging Face HTTP error {exc.code} for {self.model_id}: {details}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(f"Hugging Face request failed for {self.model_id}: {exc}") from exc

    @staticmethod
    def _extract_generated_text(response: Any, prompt: str) -> str:
        if isinstance(response, dict):
            if "error" in response:
                raise RuntimeError(f"Hugging Face inference error: {response['error']}")
            if "generated_text" in response:
                return HuggingFaceInferenceModel._strip_prompt_prefix(str(response["generated_text"]), prompt)
            if "choices" in response and response["choices"]:
                first = response["choices"][0]
                if isinstance(first, dict):
                    message = first.get("message", {})
                    if isinstance(message, dict) and "content" in message:
                        return str(message["content"]).strip()
                    if "text" in first:
                        return str(first["text"]).strip()
            return ""

        if isinstance(response, list):
            if not response:
                return ""
            first = response[0]
            if isinstance(first, dict) and "generated_text" in first:
                return HuggingFaceInferenceModel._strip_prompt_prefix(str(first["generated_text"]), prompt)
            if isinstance(first, str):
                return HuggingFaceInferenceModel._strip_prompt_prefix(first, prompt)
            return ""

        if isinstance(response, str):
            return HuggingFaceInferenceModel._strip_prompt_prefix(response, prompt)

        return ""

    @staticmethod
    def _strip_prompt_prefix(output: str, prompt: str) -> str:
        stripped = output.strip()
        if stripped.startswith(prompt):
            stripped = stripped[len(prompt):].strip()
        return stripped
