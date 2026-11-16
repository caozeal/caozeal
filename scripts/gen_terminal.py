#!/usr/bin/env python3
"""生成 README 的终端窗口 SVG（CLI 组件样式）。纯标准库。"""
from pathlib import Path

W = 860
BAR_H = 38
PAD = 28
ROW = 21
FS = 13

BG = "#0d1117"
BAR = "#161b22"
BORDER = "#30363d"
PROMPT = "#3fb950"
CMD = "#e6edf3"
OUT = "#8b949e"
ACCENT = "#58a6ff"
DIM = "#6e7681"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# (kind, a, b)
ROWS = [
    ("prompt", "whoami", ""),
    ("out", "CodePlayer · Software Engineer · 10 yrs", ""),
    ("blank", "", ""),
    ("prompt", "cat ~/now", ""),
    ("out", "agent tooling · model gateway · long-term memory", ""),
    ("blank", "", ""),
    ("prompt", "stack --list", ""),
    ("kv", "backend", "Java · Spring Boot · MySQL · Redis · Docker"),
    ("kv", "tooling", "TypeScript · Swift · Rust · Python"),
    ("blank", "", ""),
    ("prompt", "contact --open", ""),
    ("out", "github.com/caozeal  ·  caozeal.github.io", ""),
    ("blank", "", ""),
    ("prompt", "", ""),
]

H = BAR_H + PAD + 10 + (len(ROWS) - 1) * ROW + 30

parts = []
rows_svg = []
y = BAR_H + PAD + 10
X = PAD
for kind, a, b in ROWS:
    line_parts = []
    if kind == "blank":
        pass
    elif kind == "prompt":
        line_parts.append(
            f'<text x="{X}" y="{y}"><tspan fill="{PROMPT}" font-weight="700">❯ </tspan>'
            f'<tspan fill="{CMD}">{esc(a)}</tspan></text>'
        )
        if a == "":
            line_parts.append(
                f'<rect class="blink" x="{X + 18}" y="{y - 11}" width="8" height="14" fill="{CMD}"/>'
            )
    elif kind == "out":
        line_parts.append(f'<text x="{X}" y="{y}" fill="{OUT}">{esc(a)}</text>')
    elif kind == "ls":
        line_parts.append(f'<text x="{X}" y="{y}" fill="{ACCENT}">{esc(a)}</text>')
        line_parts.append(f'<text x="{X + 272}" y="{y}" fill="{OUT}">{esc(b)}</text>')
    elif kind == "kv":
        line_parts.append(f'<text x="{X}" y="{y}" fill="{PROMPT}">{esc(a)}</text>')
        line_parts.append(f'<text x="{X + 74}" y="{y}" fill="{OUT}">{esc(b)}</text>')
    if line_parts:
        delay = (len(rows_svg)) * 0.16
        parts.append(f'<g class="ln" style="animation-delay:{delay:.2f}s">' + "".join(line_parts) + '</g>')
    rows_svg.append(1)
    y += ROW

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: CodePlayer — software engineer, agent tooling">
<style>
  text {{ font-family: {FONT}; font-size: {FS}px; white-space: pre; }}
  @keyframes blink {{ 0%, 45% {{ opacity: 1; }} 50%, 95% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
  .blink {{ animation: blink 1.1s steps(1, end) infinite; }}
  @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  .ln {{ animation: fade .28s ease both; }}
</style>
<defs>
  <clipPath id="win"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10"/></clipPath>
</defs>
<g clip-path="url(#win)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{BAR_H}" fill="{BAR}"/>
  <circle cx="22" cy="{BAR_H // 2}" r="6" fill="#ff5f57"/>
  <circle cx="42" cy="{BAR_H // 2}" r="6" fill="#febc2e"/>
  <circle cx="62" cy="{BAR_H // 2}" r="6" fill="#28c840"/>
  <text x="{W // 2}" y="{BAR_H // 2 + 4}" fill="{DIM}" text-anchor="middle" font-size="12">caozeal@mac — zsh</text>
  <line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="{BORDER}"/>
{chr(10).join(parts)}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{BORDER}"/>
</svg>
"""

out = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg)
print(f"wrote {out} ({len(svg)} bytes, {W}x{H})")
