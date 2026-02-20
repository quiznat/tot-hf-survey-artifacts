"""Tests for Hugging Face inference adapter parsing and error handling."""

from __future__ import annotations

import unittest

from phase2_baselines.adapters import HuggingFaceInferenceModel


class HuggingFaceAdapterTests(unittest.TestCase):
    def test_extracts_generated_text_from_list_response(self) -> None:
        def fake_request(endpoint, payload, headers, timeout):
            del endpoint, payload, headers, timeout
            return [{"generated_text": "PROMPT final answer"}]

        model = HuggingFaceInferenceModel(
            model_id="demo/model",
            api_token="token",
            request_function=fake_request,
        )
        output = model.generate("PROMPT")
        self.assertEqual(output, "final answer")

    def test_extracts_chat_choice_content(self) -> None:
        def fake_request(endpoint, payload, headers, timeout):
            del endpoint, payload, headers, timeout
            return {"choices": [{"message": {"content": "chat answer"}}]}

        model = HuggingFaceInferenceModel(
            model_id="demo/model",
            api_token="token",
            request_function=fake_request,
        )
        output = model.generate("PROMPT")
        self.assertEqual(output, "chat answer")

    def test_raises_on_hf_error(self) -> None:
        def fake_request(endpoint, payload, headers, timeout):
            del endpoint, payload, headers, timeout
            return {"error": "model loading"}

        model = HuggingFaceInferenceModel(
            model_id="demo/model",
            api_token="token",
            request_function=fake_request,
        )
        with self.assertRaises(RuntimeError):
            model.generate("PROMPT")


if __name__ == "__main__":
    unittest.main()
