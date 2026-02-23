#!/usr/bin/env python3
"""Render publication-style flow diagrams for manuscript assets.

Outputs for each diagram:
  - SVG for web manuscript rendering
  - PDF for LaTeX/PDF manuscript rendering
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DOT = shutil.which("dot")

BG = "#ffffff"
INK = "#162130"
LINE = "#445a79"
NODE_FILL = "#ffffff"
MANUSCRIPT_FONT = "Latin Modern Roman"

BASE_GRAPH = (
    f'bgcolor="{BG}", pad="0.06", nodesep="0.34", ranksep="0.50", '
    f'splines="polyline", fontname="{MANUSCRIPT_FONT}", fontcolor="{INK}", margin="0.02"'
)
BASE_NODE = (
    f'shape="box", style="filled", fillcolor="{NODE_FILL}", '
    f'color="{LINE}", penwidth="1.5", fontname="{MANUSCRIPT_FONT}", '
    'fontsize="10", margin="0.06,0.05"'
)
BASE_DECISION = (
    f'shape="diamond", style="filled", fillcolor="{NODE_FILL}", '
    f'color="{LINE}", penwidth="1.5", fontname="{MANUSCRIPT_FONT}", fontsize="10", '
    'margin="0.04,0.04"'
)
BASE_EDGE = (
    f'color="{LINE}", penwidth="1.3", arrowsize="0.70", '
    f'fontname="{MANUSCRIPT_FONT}", fontsize="8", fontcolor="{INK}"'
)


def ensure_dot_available() -> bool:
    if DOT:
        return True
    print(
        "Warning: Graphviz 'dot' not found; skipping diagram render and using "
        "checked-in diagram assets.",
        file=sys.stderr,
    )
    return False


def write_and_render(name: str, dot_source: str) -> None:
    dot_path = ASSETS / f"{name}.dot"
    svg_path = ASSETS / f"{name}.svg"
    pdf_path = ASSETS / f"{name}.pdf"

    dot_path.write_text(dot_source, encoding="utf-8")

    subprocess.run([DOT, "-Tsvg", str(dot_path), "-o", str(svg_path)], check=True)
    subprocess.run([DOT, "-Tpdf", str(dot_path), "-o", str(pdf_path)], check=True)


def smolagents_arch_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", ranksep="0.58", nodesep="0.38"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          agents [label="Agents\\nCodeAgent\\nToolAgent\\nMultiStepAgent", width="2.10"];
          models [label="Models\\nHfApiModel\\nLiteLLM\\nOpenAI", width="2.10"];
          tools [label="Tools\\n@tool\\nTool\\nPipeline", width="2.10"];

          memory [label="Memory\\nStep Log\\nTool Calls\\nErrors", width="2.10"];
          planning [label="Planning\\nAction\\nSelection\\nTool Pick", width="2.10"];
          execution [label="Execution\\nCode\\nExecution\\nSandbox", width="2.10"];

          {{ rank=same; agents; models; tools }}
          {{ rank=same; memory; planning; execution }}

          agents -> models [dir=none, arrowhead=none, arrowtail=none];
          models -> tools [dir=none, arrowhead=none, arrowtail=none];

          agents -> memory [tailport=s, headport=n, weight=100, minlen=2];
          models -> planning [tailport=s, headport=n, weight=100, minlen=2];
          tools -> execution [tailport=s, headport=n, weight=100, minlen=2];

          memory -> planning [style=invis, weight=10];
          planning -> execution [style=invis, weight=10];
        }}
        """
    ).strip() + "\n"


def multistep_state_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", ranksep="0.56", nodesep="0.34"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          input [label="Input Task"];
          init [label="Initialize State"];
          plan [label="Generate / Update Plan"];
          step [label="Execute Next Step"];
          observe [label="Collect Observation"];
          goal [{BASE_DECISION}, label="Goal\\nSatisfied?"];
          replan [{BASE_DECISION}, label="Need\\nReplan?"];
          out [label="Return Final Response"];

          input -> init -> plan -> step -> observe -> goal;
          goal -> out [label="Yes"];
          goal -> replan [label="No"];
          replan -> plan [label="Yes", constraint=false];
          replan -> step [label="No", constraint=false];

          {{ rank=same; goal; replan }}
        }}
        """
    ).strip() + "\n"


def tool_flow_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", ranksep="0.52", nodesep="0.30"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          query [label="User Query"];
          reason [label="LLM Reasoning Step"];
          need [{BASE_DECISION}, label="Need\\nTool?"];
          select [label="Select Tool + Arguments"];
          execute [label="Execute Tool"];
          observe [label="Tool Observation"];
          answer [label="Generate Final Answer"];

          query -> reason -> need;
          need -> select [label="Yes"];
          need -> answer [label="No"];
          select -> execute -> observe;
          observe -> reason [constraint=false];

          {{ rank=same; select; answer }}
        }}
        """
    ).strip() + "\n"


def tot_agent_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", ranksep="0.56"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          thought [label="Thought Generation"];
          evaluate [label="Evaluate States"];
          select [label="Select Best Path"];
          memory [label="Memory Store"];
          action [label="Action Planning"];
          tool [label="Tool Execution"];
          feedback [label="Observation Feedback"];

          {{ rank=same; thought; evaluate; select }}
          {{ rank=same; action; tool }}

          thought -> evaluate -> select;
          thought -> memory;
          evaluate -> memory;
          select -> memory;

          memory -> action;
          memory -> tool;
          action -> tool;

          action -> feedback;
          tool -> feedback;
          feedback -> memory [constraint=false];
        }}
        """
    ).strip() + "\n"


def survey_method_dot() -> str:
    return dedent(
        f"""
        digraph G {{
          graph [{BASE_GRAPH}, rankdir="TB", ranksep="0.56"];
          node [{BASE_NODE}];
          edge [{BASE_EDGE}];

          seed [label="Seeded Corpus\\n(Pre-Curated ToT+Agent Scope)"];
          records [label="Records Identified\\nn = 30"];
          dupes [label="Duplicates Removed\\nn = 0"];
          screened [label="Title/Abstract Screened\\nn = 30"];
          fulltext [label="Full-Text Assessed\\nn = 30"];
          included [label="Studies Included in Synthesis\\nn = 22"];
          excluded [label="Full-Text Exclusions\\nn = 8\\nOut of scope / method fit\\nInsufficient extraction detail"];

          seed -> records -> dupes -> screened -> fulltext -> included;
          fulltext -> excluded [label="Excluded", constraint=false];

          {{ rank=same; fulltext; excluded }}
        }}
        """
    ).strip() + "\n"


def main() -> None:
    if not ensure_dot_available():
        return
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

    print("Rendered Graphviz manuscript diagrams (SVG + PDF) in assets/.")


if __name__ == "__main__":
    main()
