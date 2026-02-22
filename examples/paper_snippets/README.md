# Paper Snippet Examples

This directory contains runnable, tested examples that back manuscript snippets.

## Mapped Sections
- `fibonacci_example.py`: Section 3.4.2 generated-code example.
- `prompt_templates.py`: Section 2.3.2 and 2.3.3 prompt-template examples.
- `code_action_examples.py`: Section 3.4.1 code-as-action runnable examples.
- `tool_examples.py`: Section 3.6.2-3.6.4 tool examples (`fetch_stock_price`, `analyze_website`, `smart_search`, `DatabaseTool`, schema object).
- `install_smolagents.sh`: Section 3.3.3 installation block.
- `setup_env.sh`: Section 5.1.1 environment setup block.
- `Dockerfile`: Section 3.7.1 containerized deployment block.

## Run Validation
```bash
python3 -m unittest tests/test_paper_snippets.py
```
