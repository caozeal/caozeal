#!/usr/bin/env python3
"""生成可点击的项目药丸（每项一张 SVG，README 里用 <a> 包起来即可跳转）。"""
from pathlib import Path

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BG = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
MARK = "#3fb950"
H = 30
FS = 13
PAD_L = 12
PAD_R = 14
MARK_W = 14

ITEMS = [
    ("postme", "postme"),
    ("dsh-plugins", "dsh-plugins"),
    ("openviking-codebuddy-plugin", "openviking-codebuddy-plugin"),
    ("cbstats", "cbstats"),
    ("skill-manager", "skill-manager"),
    ("next-code", "next-code"),
]


def char_w(fs: float) -> float:
    return fs * 0.6


out_dir = Path(__file__).resolve().parent.parent / "assets"
out_dir.mkdir(parents=True, exist_ok=True)

for slug, label in ITEMS:
    w = int(PAD_L + MARK_W + len(label) * char_w(FS) + PAD_R)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{label}">
<style>
  text {{ font-family: {FONT}; font-size: {FS}px; font-weight: 500; }}
</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{H - 1}" rx="7" fill="{BG}" stroke="{BORDER}"/>
<text x="{PAD_L}" y="{H // 2 + 4}" fill="{MARK}" font-size="11">▸</text>
<text x="{PAD_L + MARK_W}" y="{H // 2 + 4}" fill="{TEXT}">{label}</text>
</svg>
"""
    p = out_dir / f"link-{slug}.svg"
    p.write_text(svg)
    print(f"{p.name}  {w}x{H}")
