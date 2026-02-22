import subprocess
import unittest
from pathlib import Path

from examples.paper_snippets.agent_runtime_examples import (
    ChatRequest,
    CodeAgent,
    InferenceClientModel,
    MultiStepAgent,
    handle_chat,
)
from examples.paper_snippets.code_action_examples import (
    calculator,
    composable_pipeline,
    stock_alerts,
)
from examples.paper_snippets.builtin_tools_examples import (
    DuckDuckGoSearchTool,
    PythonInterpreterTool,
    VisitWebpageTool,
    WikipediaSearchTool,
)
from examples.paper_snippets.fibonacci_example import fibonacci, solve_fifteenth_fibonacci
from examples.paper_snippets.monitoring_examples import InMemoryTracer, InstrumentedRunner
from examples.paper_snippets.optimization_examples import (
    CachedToTSupport,
    EarlyTerminationPolicy,
    ThoughtNode,
)
from examples.paper_snippets.orchestration_examples import retry_with_recovery
from examples.paper_snippets.prompt_templates import (
    build_evaluation_prompt,
    build_generation_prompt,
)
from examples.paper_snippets.strategy_examples import (
    AdaptiveToTAgent,
    HybridReasoningAgent,
    RecoverableAgent,
    compare_tool_selection,
)
from examples.paper_snippets.transparency_examples import Result, SelectedPath, explain_decision
from examples.paper_snippets.tool_examples import (
    DatabaseTool,
    analyze_website,
    fetch_stock_price,
    fetch_stock_price_schema,
    smart_search,
)


ROOT = Path(__file__).resolve().parents[1]
SNIPPET_DIR = ROOT / "examples" / "paper_snippets"


class TestPaperSnippets(unittest.TestCase):
    def test_agent_runtime_examples(self) -> None:
        model = InferenceClientModel("meta-llama/Llama-3.3-70B-Instruct")
        agent = CodeAgent(tools=[], model=model)
        self.assertEqual(agent.run("What is the 15th Fibonacci number?"), "610")

        configured = CodeAgent(
            tools=[],
            model=model,
            max_steps=10,
            planning_interval=3,
            additional_authorized_imports=["math", "random"],
            executor_type="local",
            executor_kwargs=None,
        )
        self.assertEqual(configured.max_steps, 10)
        self.assertEqual(configured.planning_interval, 3)
        self.assertEqual(configured.additional_authorized_imports, ["math", "random"])

        sandboxed = CodeAgent(
            tools=[],
            model=model,
            additional_authorized_imports=["math", "datetime"],
            executor_type="docker",
            executor_kwargs={"image": "python:3.11-slim", "network": "none"},
        )
        self.assertEqual(sandboxed.executor_type, "docker")
        self.assertEqual(sandboxed.executor_kwargs["network"], "none")

        ms_agent = MultiStepAgent(tools=[], model=model, planning_interval=2)
        multi_result = ms_agent.run(
            "Analyze the impact of recent AI regulations on tech stocks."
        )
        self.assertIn("search news and regulation updates", multi_result)
        self.assertIn("summarize likely impacts", multi_result)

    def test_local_chat_handler(self) -> None:
        agent = CodeAgent(tools=[], model=InferenceClientModel("demo-model"))
        response = handle_chat(agent, ChatRequest(message="What is the 15th Fibonacci number?"))
        self.assertEqual(response["response"], "610")

    def test_prompt_templates(self) -> None:
        generation = build_generation_prompt(
            task="Solve 24 game",
            current_path="used numbers: 3, 8",
            k=3,
        )
        evaluation = build_evaluation_prompt(
            task="Solve 24 game",
            thought_path="Try multiplication first",
        )
        self.assertIn("Generate 3 different possible next steps", generation)
        self.assertIn("Rate how promising this approach is on a scale of 0-10", evaluation)

    def test_code_action_examples(self) -> None:
        self.assertEqual(calculator("15 * 24"), 360.0)
        summary = composable_pipeline("Bitcoin price history")
        self.assertIn("line-chart", summary)
        alerts = stock_alerts(["AAPL", "GOOGL", "MSFT"], threshold=180)
        self.assertTrue(any("GOOGL" in msg for msg in alerts))
        self.assertTrue(any("MSFT" in msg for msg in alerts))
        self.assertFalse(any("AAPL" in msg for msg in alerts))

    def test_builtin_tools_examples(self) -> None:
        search_tool = DuckDuckGoSearchTool()
        wiki_tool = WikipediaSearchTool()
        visit_tool = VisitWebpageTool()
        python_tool = PythonInterpreterTool()

        self.assertTrue(search_tool("tot agents").startswith("duckduckgo:"))
        self.assertTrue(wiki_tool("tree of thoughts").startswith("wikipedia:"))
        self.assertTrue(visit_tool("https://example.com").startswith("visited:"))
        self.assertEqual(python_tool("sum(range(100))"), 4950.0)

    def test_retry_with_recovery(self) -> None:
        attempts = {"n": 0}
        seen_errors: list[str] = []

        def run_fn(task: str) -> str:
            attempts["n"] += 1
            if attempts["n"] < 3:
                raise RuntimeError(f"boom:{attempts['n']}")
            return f"ok:{task}"

        def add_recovery_context(task: str, err: Exception) -> str:
            return f"{task} | recovered from {err}"

        def log_error(err: Exception) -> None:
            seen_errors.append(str(err))

        result = retry_with_recovery(
            task="initial task",
            run_fn=run_fn,
            add_recovery_context=add_recovery_context,
            log_error=log_error,
            max_attempts=3,
        )
        self.assertIn("recovered", result)
        self.assertEqual(seen_errors, ["boom:1", "boom:2"])

    def test_monitoring_examples(self) -> None:
        tracer = InMemoryTracer()
        runner = InstrumentedRunner(tracer=tracer)

        result = runner.run(
            task="demo",
            run_fn=lambda t: f"done:{t}",
            steps=4,
            tools_used=["search", "calc"],
        )
        self.assertEqual(result, "done:demo")
        self.assertIsNotNone(tracer.last_span)
        assert tracer.last_span is not None
        self.assertEqual(tracer.last_span.attributes["task"], "demo")
        self.assertEqual(tracer.last_span.attributes["steps"], 4)

    def test_optimization_examples(self) -> None:
        support = CachedToTSupport()
        eval_calls = {"n": 0}
        gen_calls = {"n": 0}

        def evaluate_fn(prompt: str) -> float:
            eval_calls["n"] += 1
            return float(len(prompt))

        def generate_fn(prompt: str, k: int) -> list[str]:
            gen_calls["n"] += 1
            return [f"{prompt}:{i}" for i in range(k)]

        p = "evaluate me"
        self.assertEqual(support.cached_evaluate(p, evaluate_fn), support.cached_evaluate(p, evaluate_fn))
        self.assertEqual(eval_calls["n"], 1)

        out1 = support.cached_generate("gen", 3, generate_fn)
        out2 = support.cached_generate("gen", 3, generate_fn)
        self.assertEqual(out1, out2)
        self.assertEqual(gen_calls["n"], 1)

        policy = EarlyTerminationPolicy(confidence_threshold=0.9)
        self.assertTrue(policy.should_terminate([ThoughtNode(score=9.5), ThoughtNode(score=7.0)]))
        self.assertFalse(policy.should_terminate([ThoughtNode(score=8.0)]))

    def test_tool_selection_strategy_examples(self) -> None:
        comparison = compare_tool_selection(
            "Compare two open-source vector databases for a production RAG stack."
        )
        self.assertEqual(comparison["traditional_result"], "executed:blog_post_first")
        self.assertEqual(comparison["tot_best_candidate"], "docs_and_repo_evidence")
        self.assertEqual(comparison["tot_result"], "executed:docs_and_repo_evidence")
        ranked_names = [name for name, _ in comparison["tot_ranked_scores"]]
        self.assertIn("community_sentiment", ranked_names)

    def test_recoverable_agent(self) -> None:
        agent = RecoverableAgent()
        report = agent.execute_with_recovery(
            ["collect_sources", "fail_primary_lookup", "draft_summary"]
        )
        self.assertIn("collect_sources", report.completed_actions)
        self.assertIn("fallback_primary_lookup", report.completed_actions)
        self.assertIn("draft_summary", report.completed_actions)
        self.assertGreaterEqual(report.retry_count, 1)
        self.assertGreaterEqual(len(report.errors), 1)
        self.assertIsNone(report.replanned_from_step)

    def test_hybrid_reasoning_agent(self) -> None:
        agent = HybridReasoningAgent(complexity_threshold=7)
        simple = agent.run("Add two numbers.")
        complex_task = agent.run(
            "Compare three architecture options and plan a multi-step migration with trade-offs."
        )
        self.assertEqual(simple["mode"], "cot")
        self.assertEqual(complex_task["mode"], "tot")
        self.assertGreaterEqual(complex_task["complexity"], simple["complexity"])

    def test_adaptive_tot_agent(self) -> None:
        agent = AdaptiveToTAgent()
        simple = agent.adaptive_solve("Summarize this paragraph.")
        complex_task = agent.adaptive_solve(
            "Compare and optimize an ambiguous design with multiple trade-off constraints."
        )
        simple_cfg = simple["config"]
        complex_cfg = complex_task["config"]
        self.assertGreaterEqual(complex_cfg["beam_width"], simple_cfg["beam_width"])
        self.assertGreaterEqual(complex_cfg["max_depth"], simple_cfg["max_depth"])
        self.assertIn("beam=", complex_task["solution"])
        self.assertIn("depth=", complex_task["solution"])

    def test_transparency_examples(self) -> None:
        result = Result(selected_path=SelectedPath(justification="Highest evaluator score"))
        explanation = explain_decision(
            task="Solve arithmetic puzzle",
            search_tree=["path A", "path B", "path C"],
            result=result,
        )
        self.assertIn("Decision Process for: Solve arithmetic puzzle", explanation)
        self.assertIn("Highest evaluator score", explanation)
        self.assertIn("Rejected alternatives", explanation)

    def test_fibonacci(self) -> None:
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(15), 610)
        self.assertEqual(solve_fifteenth_fibonacci(), 610)
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_fetch_stock_price(self) -> None:
        self.assertEqual(fetch_stock_price("AAPL"), "$175.50")
        self.assertEqual(fetch_stock_price("aapl", "2025-01-15"), "$184.63")
        self.assertEqual(fetch_stock_price("UNKNOWN"), "Price data not available")

    def test_analyze_website(self) -> None:
        summary = analyze_website("https://example.com")
        self.assertIn("example.com", summary)

    def test_smart_search(self) -> None:
        self.assertTrue(smart_search("tot", require_recent=True).startswith("news"))
        self.assertTrue(smart_search("tot", require_recent=False).startswith("web"))

    def test_database_tool(self) -> None:
        db = DatabaseTool()
        rows = db.query("SELECT name FROM sample ORDER BY id")
        schema = db.schema()
        self.assertIn("alice", rows)
        self.assertIn("bob", rows)
        self.assertIn("CREATE TABLE", schema)

    def test_schema_object(self) -> None:
        schema = fetch_stock_price_schema()
        self.assertEqual(schema["name"], "fetch_stock_price")
        self.assertIn("ticker", schema["parameters"]["properties"])

    def test_shell_scripts_parse(self) -> None:
        for script in ("install_smolagents.sh", "setup_env.sh"):
            script_path = SNIPPET_DIR / script
            subprocess.run(["bash", "-n", str(script_path)], check=True)

    def test_dockerfile_contains_cmd(self) -> None:
        dockerfile = (SNIPPET_DIR / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn('FROM python:3.11-slim', dockerfile)
        self.assertIn('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]', dockerfile)


if __name__ == "__main__":
    unittest.main()
