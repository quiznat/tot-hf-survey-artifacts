#!/usr/bin/env bash
set -euo pipefail

# Create virtual environment
python -m venv agent_env
source agent_env/bin/activate

# Install dependencies (aligned with Section 3.3.3)
pip install smolagents
pip install "smolagents[transformers]"  # Local Hugging Face models
pip install "smolagents[openai]"        # OpenAI API models
pip install "smolagents[litellm]"       # Multi-provider routing

# Optional: local runtime acceleration
pip install torch accelerate
