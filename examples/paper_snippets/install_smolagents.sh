#!/usr/bin/env bash
set -euo pipefail

# Basic installation
pip install smolagents

# Common extras from official installation docs
pip install "smolagents[toolkit]"       # Default tools
pip install "smolagents[transformers]"  # Local Hugging Face models
pip install "smolagents[litellm]"       # Multi-provider routing
pip install "smolagents[openai]"        # OpenAI API models
pip install "smolagents[gradio]"        # Gradio UI
pip install "smolagents[all]"           # All optional extras
