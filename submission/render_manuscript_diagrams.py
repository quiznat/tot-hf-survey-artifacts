#!/usr/bin/env python3
"""Render manuscript-style PNG diagrams used as export fallbacks.

This script regenerates:
  - assets/diagram_smolagents_arch.png
  - assets/diagram_multistep_state.png
  - assets/diagram_tool_flow.png
  - assets/diagram_tot_agent.png
  - assets/diagram_survey_method.png
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

W = 1400
H = 900

COLORS = {
    "page": "#f3f5f8",
    "frame": "#d6dce5",
    "title": "#14181f",
    "text": "#16293d",
    "muted": "#3f526c",
    "box_fill": "#f7f9fc",
    "box_border": "#49698f",
    "line": "#5f7390",
    "decision_fill": "#edf2f8",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        )
    else:
        candidates.extend(
            [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
        )
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = load_font(54, bold=True)
BOX_TITLE_FONT = load_font(34, bold=True)
BOX_TEXT_FONT = load_font(24, bold=False)
LABEL_FONT = load_font(24, bold=False)


def new_canvas() -> Tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), COLORS["page"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([(12, 12), (W - 12, H - 12)], outline=COLORS["box_border"], width=3)
    return img, draw


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    return x1 - x0, y1 - y0


def draw_title(draw: ImageDraw.ImageDraw, text: str) -> None:
    tw, th = text_size(draw, text, TITLE_FONT)
    draw.text(((W - tw) // 2, 34), text, fill=COLORS["title"], font=TITLE_FONT)


def draw_box(
    draw: ImageDraw.ImageDraw,
    rect: Tuple[int, int, int, int],
    title: str,
    lines: Sequence[str] | None = None,
) -> None:
    x0, y0, x1, y1 = rect
    draw.rounded_rectangle(rect, radius=14, fill=COLORS["box_fill"], outline=COLORS["box_border"], width=4)

    title_rows = title.split("\n")
    title_sizes = [text_size(draw, row, BOX_TITLE_FONT) for row in title_rows]
    title_h = sum(h for _, h in title_sizes) + (len(title_rows) - 1) * 4
    y = y0 + 14
    for row, (tw, th) in zip(title_rows, title_sizes):
        title_x = x0 + (x1 - x0 - tw) // 2
        draw.text((title_x, y), row, fill=COLORS["title"], font=BOX_TITLE_FONT)
        y += th + 4

    if not lines:
        return

    _, line_h = text_size(draw, "Ag", BOX_TEXT_FONT)
    y += 8
    for line in lines:
        draw.text((x0 + 16, y), f"- {line}", fill=COLORS["muted"], font=BOX_TEXT_FONT)
        y += line_h + 8


def draw_diamond(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    w: int,
    h: int,
    label: str,
) -> None:
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy)]
    draw.polygon(pts, fill=COLORS["decision_fill"], outline=COLORS["box_border"], width=4)
    rows = label.split("\n")
    row_sizes = [text_size(draw, row, LABEL_FONT) for row in rows]
    total_h = sum(h for _, h in row_sizes) + (len(rows) - 1) * 4
    y = cy - total_h // 2
    for row, (tw, th) in zip(rows, row_sizes):
        draw.text((cx - tw // 2, y), row, fill=COLORS["title"], font=LABEL_FONT)
        y += th + 4


def draw_polyline(
    draw: ImageDraw.ImageDraw,
    points: Sequence[Tuple[int, int]],
    arrow: bool = True,
    width: int = 4,
) -> None:
    draw.line(points, fill=COLORS["line"], width=width, joint="curve")
    if arrow and len(points) >= 2:
        p0 = points[-2]
        p1 = points[-1]
        draw_arrow_head(draw, p0, p1, width=width)


def draw_arrow_head(
    draw: ImageDraw.ImageDraw,
    p0: Tuple[int, int],
    p1: Tuple[int, int],
    width: int = 4,
) -> None:
    x0, y0 = p0
    x1, y1 = p1
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 16
    spread = math.pi / 7
    p2 = (x1 - int(length * math.cos(angle - spread)), y1 - int(length * math.sin(angle - spread)))
    p3 = (x1 - int(length * math.cos(angle + spread)), y1 - int(length * math.sin(angle + spread)))
    draw.polygon([p1, p2, p3], fill=COLORS["line"], outline=COLORS["line"])


def draw_label(
    draw: ImageDraw.ImageDraw,
    pos: Tuple[int, int],
    text: str,
    align: str = "left",
) -> None:
    tw, th = text_size(draw, text, BOX_TEXT_FONT)
    x, y = pos
    if align == "center":
        x -= tw // 2
    elif align == "right":
        x -= tw
    pad_x = 8
    pad_y = 4
    draw.rounded_rectangle(
        [(x - pad_x, y - pad_y), (x + tw + pad_x, y + th + pad_y)],
        radius=6,
        fill=COLORS["page"],
        outline=None,
    )
    draw.text((x, y), text, fill=COLORS["muted"], font=BOX_TEXT_FONT)


def center(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    x0, y0, x1, y1 = rect
    return ((x0 + x1) // 2, (y0 + y1) // 2)


def top(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    x0, y0, x1, _ = rect
    return ((x0 + x1) // 2, y0)


def bottom(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    x0, _, x1, y1 = rect
    return ((x0 + x1) // 2, y1)


def left(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    x0, y0, _, y1 = rect
    return (x0, (y0 + y1) // 2)


def right(rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    _, y0, x1, y1 = rect
    return (x1, (y0 + y1) // 2)


def render_smolagents_arch() -> None:
    img, draw = new_canvas()
    draw_title(draw, "smolagents Architecture")

    boxes = {
        "agents": (130, 185, 470, 335),
        "models": (530, 185, 870, 335),
        "tools": (930, 185, 1270, 335),
        "memory": (130, 430, 470, 615),
        "planning": (530, 430, 870, 615),
        "execution": (930, 430, 1270, 615),
    }

    draw_box(draw, boxes["agents"], "Agents", ["CodeAgent", "ToolAgent", "MultiStep"])
    draw_box(draw, boxes["models"], "Models", ["HfApiModel", "LiteLLM", "OpenAI"])
    draw_box(draw, boxes["tools"], "Tools", ["@tool", "Tool", "Pipeline"])
    draw_box(draw, boxes["memory"], "Memory", ["Step Log", "Tool Calls", "Errors"])
    draw_box(draw, boxes["planning"], "Planning", ["Action", "Selection", "Tool Pick"])
    draw_box(draw, boxes["execution"], "Execution", ["Code", "Execution", "Sandbox"])

    draw_polyline(draw, [right(boxes["agents"]), left(boxes["models"])], arrow=False)
    draw_polyline(draw, [right(boxes["models"]), left(boxes["tools"])], arrow=False)
    draw_polyline(draw, [bottom(boxes["agents"]), top(boxes["memory"])])
    draw_polyline(draw, [bottom(boxes["models"]), top(boxes["planning"])])
    draw_polyline(draw, [bottom(boxes["tools"]), top(boxes["execution"])])

    img.save(ASSETS / "diagram_smolagents_arch.png", optimize=True)


def render_multistep_state() -> None:
    img, draw = new_canvas()
    draw_title(draw, "MultiStepAgent State Diagram")

    input_box = (520, 140, 900, 220)
    init_box = (520, 245, 900, 325)
    plan_box = (520, 350, 900, 430)
    step_box = (520, 455, 900, 535)
    obs_box = (520, 560, 900, 640)
    out_box = (970, 675, 1320, 755)

    draw_box(draw, input_box, "Input Task")
    draw_box(draw, init_box, "Initialize State")
    draw_box(draw, plan_box, "Generate / Update Plan")
    draw_box(draw, step_box, "Execute Next Step")
    draw_box(draw, obs_box, "Collect Observation")
    draw_box(draw, out_box, "Return Final Response")

    goal_c = (250, 600)
    replan_c = (250, 430)
    draw_diamond(draw, goal_c[0], goal_c[1], 250, 140, "Goal\nSatisfied?")
    draw_diamond(draw, replan_c[0], replan_c[1], 250, 140, "Need\nReplan?")

    draw_polyline(draw, [bottom(input_box), top(init_box)])
    draw_polyline(draw, [bottom(init_box), top(plan_box)])
    draw_polyline(draw, [bottom(plan_box), top(step_box)])
    draw_polyline(draw, [bottom(step_box), top(obs_box)])

    # Observation -> Goal check (route below box to avoid crossing text)
    goal_right = (goal_c[0] + 125, goal_c[1])
    draw_polyline(draw, [bottom(obs_box), (bottom(obs_box)[0], 680), (goal_right[0], 680), goal_right], arrow=False)
    draw_arrow_head(draw, (goal_right[0], 680), goal_right)

    # Goal yes -> return final (kept below observation box)
    draw_polyline(draw, [goal_right, (goal_right[0], 715), (940, 715), left(out_box)], arrow=False)
    draw_arrow_head(draw, (940, 715), left(out_box))
    draw_label(draw, (928, 680), "Yes", align="center")

    # Goal no -> replan decision
    draw_polyline(draw, [(goal_c[0], goal_c[1] - 70), (goal_c[0], replan_c[1] + 70)])
    draw_label(draw, (154, 504), "No (goal)")

    # Replan yes -> plan
    draw_polyline(draw, [(replan_c[0] + 125, replan_c[1]), (430, 430), left(plan_box)], arrow=False)
    draw_arrow_head(draw, (430, 430), left(plan_box))
    draw_label(draw, (365, 392), "Yes")

    # Replan no -> execute step
    draw_polyline(draw, [(replan_c[0] + 125, replan_c[1]), (430, 495), left(step_box)], arrow=False)
    draw_arrow_head(draw, (430, 495), left(step_box))
    draw_label(draw, (336, 506), "No (replan)")

    img.save(ASSETS / "diagram_multistep_state.png", optimize=True)


def render_tool_flow() -> None:
    img, draw = new_canvas()
    draw_title(draw, "Tool-Augmented LLM Flow")

    query_box = (50, 340, 290, 440)
    reason_box = (340, 340, 650, 440)
    select_box = (890, 170, 1240, 270)
    exec_box = (890, 315, 1240, 415)
    obs_box = (890, 460, 1240, 560)
    answer_box = (890, 605, 1240, 705)

    draw_box(draw, query_box, "User Query")
    draw_box(draw, reason_box, "LLM Reasoning Step")
    draw_box(draw, select_box, "Select Tool + Arguments")
    draw_box(draw, exec_box, "Execute Tool")
    draw_box(draw, obs_box, "Tool Observation")
    draw_box(draw, answer_box, "Generate Final Answer")

    need_center = (760, 390)
    draw_diamond(draw, need_center[0], need_center[1], 220, 130, "Need\nTool?")

    draw_polyline(draw, [right(query_box), left(reason_box)])
    draw_polyline(draw, [right(reason_box), (need_center[0] - 110, need_center[1])])

    draw_polyline(
        draw,
        [(need_center[0] + 110, need_center[1]), (850, 390), (850, 220), left(select_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (850, 220), left(select_box))
    draw_label(draw, (820, 288), "Yes")

    draw_polyline(draw, [bottom(select_box), top(exec_box)])
    draw_polyline(draw, [bottom(exec_box), top(obs_box)])
    draw_polyline(draw, [bottom(obs_box), top(answer_box)])

    # No-tool shortcut to final answer
    draw_polyline(
        draw,
        [(need_center[0], need_center[1] + 65), (760, 655), left(answer_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (760, 655), left(answer_box))
    draw_label(draw, (730, 592), "No")

    # Observation loop back to reasoning
    draw_polyline(
        draw,
        [left(obs_box), (840, 510), (840, 485), (520, 485), (520, 440), bottom(reason_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (520, 485), (520, 440))
    draw_label(draw, (670, 494), "Observation Loop", align="center")

    img.save(ASSETS / "diagram_tool_flow.png", optimize=True)


def render_tot_agent() -> None:
    img, draw = new_canvas()
    draw_title(draw, "ToT-Enhanced Agent")

    thought = (80, 165, 420, 285)
    evaluate = (530, 165, 870, 285)
    select = (980, 165, 1320, 285)
    memory = (530, 335, 870, 445)
    action = (140, 545, 500, 665)
    tools = (900, 545, 1260, 665)
    feedback = (530, 730, 870, 840)

    draw_box(draw, thought, "Thought Generation")
    draw_box(draw, evaluate, "Evaluate States")
    draw_box(draw, select, "Select Best Path")
    draw_box(draw, memory, "Memory Store")
    draw_box(draw, action, "Action Planning")
    draw_box(draw, tools, "Tool Execution")
    draw_box(draw, feedback, "Observation Feedback")

    # Top reasoning chain
    draw_polyline(draw, [right(thought), left(evaluate)])
    draw_polyline(draw, [right(evaluate), left(select)])

    # Thought/select contribute to memory
    mem_top_left = (590, memory[1])
    mem_top_right = (810, memory[1])
    draw_polyline(draw, [bottom(thought), (bottom(thought)[0], 315), (mem_top_left[0], 315), mem_top_left], arrow=False)
    draw_arrow_head(draw, (mem_top_left[0], 315), mem_top_left)
    draw_polyline(draw, [bottom(select), (bottom(select)[0], 315), (mem_top_right[0], 315), mem_top_right], arrow=False)
    draw_arrow_head(draw, (mem_top_right[0], 315), mem_top_right)

    # Memory dispatches plans/tools
    draw_polyline(draw, [bottom(memory), (700, 500), (top(action)[0], 500), top(action)], arrow=False)
    draw_arrow_head(draw, (top(action)[0], 500), top(action))
    draw_polyline(draw, [bottom(memory), (700, 500), (top(tools)[0], 500), top(tools)], arrow=False)
    draw_arrow_head(draw, (top(tools)[0], 500), top(tools))

    # Planning and execution interaction
    draw_polyline(draw, [right(action), left(tools)])

    # Both feed observations
    draw_polyline(draw, [bottom(action), (bottom(action)[0], 700), (top(feedback)[0] - 120, 700), (top(feedback)[0] - 120, top(feedback)[1])], arrow=False)
    draw_arrow_head(draw, (top(feedback)[0] - 120, 700), (top(feedback)[0] - 120, top(feedback)[1]))
    draw_polyline(draw, [bottom(tools), (bottom(tools)[0], 700), (top(feedback)[0] + 120, 700), (top(feedback)[0] + 120, top(feedback)[1])], arrow=False)
    draw_arrow_head(draw, (top(feedback)[0] + 120, 700), (top(feedback)[0] + 120, top(feedback)[1]))

    # Feedback loop to memory (via left margin to avoid crossing labels)
    draw_polyline(draw, [left(feedback), (90, left(feedback)[1]), (90, 390), left(memory)], arrow=False)
    draw_arrow_head(draw, (90, 390), left(memory))

    img.save(ASSETS / "diagram_tot_agent.png", optimize=True)


def render_survey_method() -> None:
    img, draw = new_canvas()
    draw_title(draw, "Survey Method Flow (Frozen Run)")

    note_box = (220, 130, 1180, 225)
    step1 = (450, 270, 890, 365)
    step2 = (450, 395, 890, 490)
    step3 = (450, 520, 890, 615)
    step4 = (450, 645, 890, 740)
    excl = (950, 505, 1320, 655)

    draw_box(draw, note_box, "Seeded Corpus\n(Pre-Curated ToT+Agent Scope)")
    draw_box(draw, step1, "Records Identified\nn = 30")
    draw_box(draw, step2, "Title/Abstract Screened\nn = 30")
    draw_box(draw, step3, "Full-Text Assessed\nn = 30")
    draw_box(draw, step4, "Studies Included in Synthesis\nn = 22")
    draw_box(draw, excl, "Full-Text Exclusions\nn = 8", ["Out of scope / method fit", "Insufficient extraction detail"])

    draw_polyline(draw, [bottom(note_box), top(step1)])
    draw_polyline(draw, [bottom(step1), top(step2)])
    draw_polyline(draw, [bottom(step2), top(step3)])
    draw_polyline(draw, [bottom(step3), top(step4)])
    draw_polyline(draw, [right(step3), left(excl)])

    draw_label(draw, (920, 542), "excluded", align="center")
    draw_label(draw, (362, 244), "duplicates removed: 0")

    img.save(ASSETS / "diagram_survey_method.png", optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    render_smolagents_arch()
    render_multistep_state()
    render_tool_flow()
    render_tot_agent()
    render_survey_method()
    print("Rendered manuscript-style diagram PNGs in assets/.")


if __name__ == "__main__":
    main()
