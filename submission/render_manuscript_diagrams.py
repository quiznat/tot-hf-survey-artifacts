#!/usr/bin/env python3
"""Render manuscript-style PNG diagrams used as export fallbacks.

This script regenerates:
  - assets/diagram_smolagents_arch.png
  - assets/diagram_multistep_state.png
  - assets/diagram_tool_flow.png
  - assets/diagram_tot_agent.png
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

    t_w, t_h = text_size(draw, title, BOX_TITLE_FONT)
    title_x = x0 + (x1 - x0 - t_w) // 2
    title_y = y0 + 14
    draw.text((title_x, title_y), title, fill=COLORS["title"], font=BOX_TITLE_FONT)

    if not lines:
        return

    _, line_h = text_size(draw, "Ag", BOX_TEXT_FONT)
    y = title_y + t_h + 12
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

    input_box = (525, 145, 875, 235)
    init_box = (525, 270, 875, 360)
    plan_box = (525, 395, 875, 485)
    step_box = (525, 520, 875, 610)
    obs_box = (525, 645, 875, 735)
    out_box = (990, 640, 1320, 730)

    draw_box(draw, input_box, "Input Task")
    draw_box(draw, init_box, "Initialize State")
    draw_box(draw, plan_box, "Generate / Update Plan")
    draw_box(draw, step_box, "Execute Next Step")
    draw_box(draw, obs_box, "Collect Observation")
    draw_box(draw, out_box, "Return Final Response")

    goal_c = (255, 690)
    replan_c = (255, 520)
    draw_diamond(draw, goal_c[0], goal_c[1], 260, 150, "Goal\nSatisfied?")
    draw_diamond(draw, replan_c[0], replan_c[1], 260, 150, "Need\nReplan?")

    draw_polyline(draw, [bottom(input_box), top(init_box)])
    draw_polyline(draw, [bottom(init_box), top(plan_box)])
    draw_polyline(draw, [bottom(plan_box), top(step_box)])
    draw_polyline(draw, [bottom(step_box), top(obs_box)])

    draw_polyline(draw, [left(obs_box), (410, 690), (goal_c[0] + 130, goal_c[1])], arrow=False)
    draw_arrow_head(draw, (410, 690), (goal_c[0] + 130, goal_c[1]))

    draw_polyline(draw, [(goal_c[0], goal_c[1] - 75), (goal_c[0], replan_c[1] + 75)])
    draw.text((295, 600), "No", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    draw_polyline(draw, [(goal_c[0] + 130, goal_c[1]), (960, 690), left(out_box)], arrow=False)
    draw_arrow_head(draw, (960, 690), left(out_box))
    draw.text((920, 650), "Yes", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    draw_polyline(
        draw,
        [(replan_c[0] + 130, replan_c[1]), (420, 520), (420, 440), left(plan_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (420, 440), left(plan_box))
    draw.text((350, 470), "Yes", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    draw_polyline(
        draw,
        [(replan_c[0], replan_c[1] + 75), (255, 625), (420, 625), left(step_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (420, 625), left(step_box))
    draw.text((185, 570), "No", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    img.save(ASSETS / "diagram_multistep_state.png", optimize=True)


def render_tool_flow() -> None:
    img, draw = new_canvas()
    draw_title(draw, "Tool-Augmented LLM Flow")

    query_box = (60, 345, 300, 455)
    reason_box = (350, 345, 720, 455)
    select_box = (900, 185, 1250, 295)
    exec_box = (900, 330, 1250, 440)
    obs_box = (900, 475, 1250, 585)
    answer_box = (900, 620, 1250, 730)

    draw_box(draw, query_box, "User Query")
    draw_box(draw, reason_box, "LLM Reasoning Step")
    draw_box(draw, select_box, "Select Tool + Arguments")
    draw_box(draw, exec_box, "Execute Tool")
    draw_box(draw, obs_box, "Tool Observation")
    draw_box(draw, answer_box, "Generate Final Answer")

    need_center = (790, 400)
    draw_diamond(draw, need_center[0], need_center[1], 220, 130, "Need\nTool?")

    draw_polyline(draw, [right(query_box), left(reason_box)])
    draw_polyline(draw, [right(reason_box), (680, 400)], arrow=False)
    draw_polyline(draw, [(680, 400), (need_center[0] - 110, need_center[1])], arrow=False)
    draw_arrow_head(draw, (680, 400), (need_center[0] - 110, need_center[1]))

    draw_polyline(draw, [(need_center[0] + 110, need_center[1]), (860, 400), (860, 240), left(select_box)], arrow=False)
    draw_arrow_head(draw, (860, 240), left(select_box))
    draw.text((836, 288), "Yes", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    draw_polyline(draw, [bottom(select_box), top(exec_box)])
    draw_polyline(draw, [bottom(exec_box), top(obs_box)])
    draw_polyline(draw, [bottom(obs_box), top(answer_box)])

    draw_polyline(
        draw,
        [left(obs_box), (860, 530), (860, 505), (560, 505), (560, 455), bottom(reason_box)],
        arrow=False,
    )
    draw_arrow_head(draw, (560, 505), (560, 455))
    draw.text((650, 514), "Observation Loop", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    draw_polyline(draw, [(need_center[0], need_center[1] + 65), (790, 675), left(answer_box)], arrow=False)
    draw_arrow_head(draw, (790, 675), left(answer_box))
    draw.text((745, 618), "No", fill=COLORS["muted"], font=BOX_TEXT_FONT)

    img.save(ASSETS / "diagram_tool_flow.png", optimize=True)


def render_tot_agent() -> None:
    img, draw = new_canvas()
    draw_title(draw, "ToT-Enhanced Agent")

    thought = (90, 165, 430, 285)
    evaluate = (530, 165, 870, 285)
    select = (970, 165, 1310, 285)
    memory = (530, 330, 870, 450)
    action = (140, 530, 480, 670)
    tools = (920, 530, 1260, 670)
    feedback = (530, 725, 870, 845)

    draw_box(draw, thought, "Thought Generation")
    draw_box(draw, evaluate, "Evaluate States")
    draw_box(draw, select, "Select Best Path")
    draw_box(draw, memory, "Memory Store")
    draw_box(draw, action, "Action Planning")
    draw_box(draw, tools, "Tool Execution")
    draw_box(draw, feedback, "Observation Feedback")

    draw_polyline(draw, [right(thought), left(evaluate)], arrow=False)
    draw_polyline(draw, [right(evaluate), left(select)], arrow=False)

    t_bottom = bottom(thought)
    s_bottom = bottom(select)
    m_left = left(memory)
    m_right = right(memory)
    draw_polyline(draw, [t_bottom, (t_bottom[0], 300), (m_left[0], 300), (m_left[0], m_left[1])], arrow=False)
    draw_polyline(draw, [s_bottom, (s_bottom[0], 300), (m_right[0], 300), (m_right[0], m_right[1])], arrow=False)

    m_bottom = bottom(memory)
    a_top = top(action)
    t_top = top(tools)
    draw_polyline(draw, [m_bottom, (m_bottom[0], 500)], arrow=False)
    draw_polyline(draw, [(m_bottom[0], 500), (a_top[0], 500), a_top], arrow=False)
    draw_polyline(draw, [(m_bottom[0], 500), (t_top[0], 500), t_top], arrow=False)

    a_right = right(action)
    t_left = left(tools)
    draw_polyline(draw, [a_right, (t_left[0], a_right[1])], arrow=False)

    fb_top = top(feedback)
    a_bottom = bottom(action)
    t_bottom2 = bottom(tools)
    draw_polyline(draw, [a_bottom, (a_bottom[0], 695), (fb_top[0], 695), fb_top], arrow=False)
    draw_polyline(draw, [t_bottom2, (t_bottom2[0], 695), (fb_top[0], 695), fb_top], arrow=False)
    draw_polyline(draw, [(700, a_right[1]), (700, fb_top[1])], arrow=False)

    draw_polyline(draw, [bottom(feedback), (700, 680), (700, 450), top(memory)], arrow=False)

    img.save(ASSETS / "diagram_tot_agent.png", optimize=True)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    render_smolagents_arch()
    render_multistep_state()
    render_tool_flow()
    render_tot_agent()
    print("Rendered manuscript-style diagram PNGs in assets/.")


if __name__ == "__main__":
    main()
