#!/usr/bin/env python3
"""生成 README 的终端窗口 SVG（CLI 组件样式）。纯标准库。"""
from pathlib import Path

W = 860
BAR_H = 38
PAD = 28
ROW = 21
FS = 13
H = BAR_H + PAD + 23 * ROW + PAD - 6

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
    ("prompt", "cat ~/focus.txt", ""),
    ("out", "agent tooling · model gateway · long-term memory", ""),
    ("blank", "", ""),
    ("prompt", "ls -1 ~/projects", ""),
    ("ls", "postme/", "原生 macOS 接口调试工具 · 常驻 40MB · 零依赖"),
    ("ls", "dsh-plugins/", "DSH 插件集 · 侧栏 Git 面板 / AI 提交信息 / SVG 提交图"),
    ("ls", "openviking-codebuddy-plugin/", "CodeBuddy 语义长期记忆插件 · hooks + MCP"),
    ("ls", "cbstats/", "CodeBuddy 逐日 token 统计 · ccusage 的同类工具"),
    ("ls", "skill-manager/", "多 agent 与技能的统一管理"),
    ("ls", "next-code/", "VS Code 扩展 · 任意 OpenAI 兼容接口生成提交信息"),
    ("blank", "", ""),
    ("prompt", "stack --list", ""),
    ("kv", "backend", "Java · Spring Boot · MySQL · Redis · Docker"),
    ("kv", "tooling", "TypeScript · Swift · Rust · Python"),
    ("blank", "", ""),
    ("prompt", "cat ~/.contact", ""),
    ("kv", "blog", "https://caozeal.github.io"),
    ("kv", "gh", "https://github.com/caozeal"),
    ("blank", "", ""),
    ("prompt", "", ""),
]

parts = []
y = BAR_H + PAD + 10
X = PAD
for kind, a, b in ROWS:
    if kind == "blank":
        pass
    elif kind == "prompt":
        parts.append(
            f'<text x="{X}" y="{y}"><tspan fill="{PROMPT}" font-weight="700">❯ </tspan>'
            f'<tspan fill="{CMD}">{esc(a)}</tspan></text>'
        )
        if a == "":
            parts.append(
                f'<rect class="blink" x="{X + 18}" y="{y - 11}" width="8" height="14" fill="{CMD}"/>'
            )
    elif kind == "out":
        parts.append(f'<text x="{X}" y="{y}" fill="{OUT}">{esc(a)}</text>')
    elif kind == "ls":
        parts.append(f'<text x="{X}" y="{y}" fill="{ACCENT}">{esc(a)}</text>')
        parts.append(f'<text x="{X + 272}" y="{y}" fill="{OUT}">{esc(b)}</text>')
    elif kind == "kv":
        parts.append(f'<text x="{X}" y="{y}" fill="{PROMPT}">{esc(a)}</text>')
        parts.append(f'<text x="{X + 74}" y="{y}" fill="{OUT}">{esc(b)}</text>')
    y += ROW

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: CodePlayer — software engineer, agent tooling">
<style>
  text {{ font-family: {FONT}; font-size: {FS}px; white-space: pre; }}
  @keyframes blink {{ 0%, 45% {{ opacity: 1; }} 50%, 95% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
  .blink {{ animation: blink 1.1s steps(1, end) infinite; }}
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
