import subprocess
import unittest
from pathlib import Path

from examples.paper_snippets.fibonacci_example import fibonacci, solve_fifteenth_fibonacci
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
