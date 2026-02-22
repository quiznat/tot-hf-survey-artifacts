#!/usr/bin/env python3
"""Render publication-style flow diagrams for manuscript assets.

Outputs for each diagram:
  - PNG fallback used by paper.html/PDF conversion
  - SVG vector file for high-fidelity web display and reuse
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DOT = shutil.which("dot")

BG = "#ffffff"
EDGE = "#5f7390"
NODE_FILL = "#f8fbff"
NODE_BORDER = "#4f6485"
TITLE = "#14181f"

BASE_GRAPH = (
    f'bgcolor="{BG}", pad="0.35", nodesep="0.55", ranksep="0.70", '
    f'splines="polyline", fontname="Helvetica", fontcolor="{TITLE}", '
    'labelloc="t", margin="0.15"'
)
BASE_NODE = (
    f'shape="box", style="rounded,filled", fillcolor="{NODE_FILL}", '
    f'color="{NODE_BORDER}", penwidth="2.0", fontname="Helvetica", '
    'fontsize="20", margin="0.14,0.10"'
)
BASE_EDGE = (
    f'color="{EDGE}", penwidth="1.8", arrowsize="0.8", '
    'fontname="Helvetica", fontsize="15", labeldistance="1.4"'
)


def ensure_dot_available() -> None:
    if DOT:
        return
    raise SystemExit(
        "Graphviz 'dot' is required to render diagrams. "
        "Install with: brew install graphviz"
    )


def write_and_render(name: str, dot_source: str) -> None:
    dot_path = ASSETS / f"{name}.dot"
    svg_path = ASSETS / f"{name}.svg"
    png_path = ASSETS / f"{name}.png"

    dot_path.write_text(dot_source, encoding="utf-8")

    subprocess.run([DOT, "-Tsvg", str(dot_path), "-o", str(svg_path)], check=True)
    subprocess.run(
        [DOT, "-Tpng", "-Gdpi=140", str(dot_path), "-o", str(png_path)],
        check=True,
    )


def smolagents_arch_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", label="smolagents Architecture", fontsize="32"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          agents [label="Agents\\n- CodeAgent\\n- ToolAgent\\n- MultiStep"];
          models [label="Models\\n- HfApiModel\\n- LiteLLM\\n- OpenAI"];
          tools [label="Tools\\n- @tool\\n- Tool\\n- Pipeline"];
          memory [label="Memory\\n- Step Log\\n- Tool Calls\\n- Errors"];
          planning [label="Planning\\n- Action\\n- Selection\\n- Tool Pick"];
          execution [label="Execution\\n- Code\\n- Execution\\n- Sandbox"];

          {{ rank=same; agents; models; tools }}
          {{ rank=same; memory; planning; execution }}

          agents -> models [dir=none];
          models -> tools [dir=none];
          agents -> memory;
          models -> planning;
          tools -> execution;
        }}
        """
    ).strip() + "\n"


def multistep_state_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", label="MultiStepAgent State Diagram", fontsize="32"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          input [label="Input Task"];
          init [label="Initialize State"];
          plan [label="Generate / Update Plan"];
          step [label="Execute Next Step"];
          observe [label="Collect Observation"];
          goal [shape="diamond", style="filled", fillcolor="#edf2f8", label="Goal\\nSatisfied?"];
          replan [shape="diamond", style="filled", fillcolor="#edf2f8", label="Need\\nReplan?"];
          out [label="Return Final Response"];

          input -> init -> plan -> step -> observe -> goal;
          goal -> out [label="Yes"];
          goal -> replan [label="No"];
          replan -> plan [label="Yes"];
          replan -> step [label="No"];
        }}
        """
    ).strip() + "\n"


def tool_flow_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", label="Tool-Augmented LLM Flow", fontsize="32"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          query [label="User Query"];
          reason [label="LLM Reasoning Step"];
          need [shape="diamond", style="filled", fillcolor="#edf2f8", label="Need\\nTool?"];
          select [label="Select Tool + Arguments"];
          exec [label="Execute Tool"];
          obs [label="Tool Observation"];
          ans [label="Generate Final Answer"];

          query -> reason;
          reason -> need;
          need -> select [label="Yes"];
          need -> ans [label="No"];
          select -> exec;
          exec -> obs;
          obs -> reason [label="Observation loop", constraint=false];

          {{ rank=same; select; ans }}
        }}
        """
    ).strip() + "\n"


def tot_agent_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", label="ToT-Enhanced Agent", fontsize="32"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          thought [label="Thought Generation"];
          eval [label="Evaluate States"];
          select [label="Select Best Path"];
          memory [label="Memory Store"];
          action [label="Action Planning"];
          tools [label="Tool Execution"];
          feedback [label="Observation Feedback"];

          {{ rank=same; thought; eval; select }}
          {{ rank=same; action; tools }}

          thought -> eval -> select;
          thought -> memory;
          eval -> memory;
          select -> memory;
          memory -> action;
          memory -> tools;
          action -> tools;
          action -> feedback;
          tools -> feedback;
          feedback -> memory;
        }}
        """
    ).strip() + "\n"


def survey_method_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", label="Survey Method Flow (Frozen Run)", fontsize="32"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          seed [label="Seeded Corpus\\n(Pre-Curated ToT+Agent Scope)"];
          records [label="Records Identified\\nn = 30"];
          screened [label="Title/Abstract Screened\\nn = 30"];
          fulltext [label="Full-Text Assessed\\nn = 30"];
          included [label="Studies Included in Synthesis\\nn = 22"];
          excl [label="Full-Text Exclusions\\nn = 8\\n- Out of scope / method fit\\n- Insufficient extraction detail"];
          dup [shape="note", style="filled", fillcolor="#eef3f9", color="#9aa9be", fontsize="14", label="duplicates removed: 0"];

          seed -> records -> screened -> fulltext -> included;
          fulltext -> excl [label="excluded"];
          dup -> records [style="dashed", arrowhead="none"];

          {{ rank=same; fulltext; excl }}
        }}
        """
    ).strip() + "\n"


def main() -> None:
    ensure_dot_available()
    ASSETS.mkdir(parents=True, exist_ok=True)

    diagrams = {
        "diagram_smolagents_arch": smolagents_arch_dot(),
        "diagram_multistep_state": multistep_state_dot(),
        "diagram_tool_flow": tool_flow_dot(),
        "diagram_tot_agent": tot_agent_dot(),
        "diagram_survey_method": survey_method_dot(),
    }

    for name, source in diagrams.items():
        write_and_render(name, source)

    print("Rendered Graphviz manuscript diagrams (PNG + SVG) in assets/.")


if __name__ == "__main__":
    main()
