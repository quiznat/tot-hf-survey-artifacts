# Paper Snippet Examples

This directory contains runnable, tested examples that back manuscript snippets.

## Mapped Sections
- `fibonacci_example.py`: Section 3.4.2 generated-code example.
- `prompt_templates.py`: Section 2.3.2 and 2.3.3 prompt-template examples.
- `code_action_examples.py`: Section 3.4.1 code-as-action runnable examples.
- `agent_runtime_examples.py`: Section 3.4.2, 3.4.3, 3.5.2, 3.6.6, and 3.7.1 runtime/deployment stand-ins.
- `builtin_tools_examples.py`: Section 3.6.1 built-in tool examples.
- `orchestration_examples.py`: Section 3.5.3 recovery/retry orchestration example.
- `monitoring_examples.py`: Section 3.7.2 tracing/observability example.
- `optimization_examples.py`: Section 5.3.1 and 5.3.2 optimization examples.
- `transparency_examples.py`: Section 6.4.1 explanation/trace rendering example.
- `tool_examples.py`: Section 3.6.2-3.6.4 tool examples (`fetch_stock_price`, `analyze_website`, `smart_search`, `DatabaseTool`, schema object).
- `install_smolagents.sh`: Section 3.3.3 installation block.
- `setup_env.sh`: Section 5.1.1 environment setup block.
- `Dockerfile`: Section 3.7.1 containerized deployment block.

## Run Validation
```bash
python3 -m unittest tests/test_paper_snippets.py
```
