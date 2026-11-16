#!/usr/bin/env python3
"""生成整块面板 SVG：二进制雨横幅 + 终端窗口，统一 CRT 扫描与故障效果。纯标准库。"""
import random
from pathlib import Path

W = 900
HERO_H = 230
CARD_X, CARD_Y, CARD_W = 20, 250, 860
BAR_H = 38
PAD = 28
ROW = 21
FS = 13

GREEN = "#39d353"
BG = "#0a0e13"
PANEL = "#0d1117"
BAR = "#161b22"
BORDER = "#30363d"
CMD = "#e6edf3"
OUT = "#8b949e"
ACCENT = "#58a6ff"
DIM = "#6e7681"
CYAN = "#22d3ee"
MAGENTA = "#f472b6"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

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

CARD_H = BAR_H + PAD + 10 + (len(ROWS) - 1) * ROW + 30
H = CARD_Y + CARD_H + 20


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rain_column(x: int, rnd: random.Random) -> str:
    n = 26
    spans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 14}">{rnd.choice("01")}</tspan>'
        for i in range(n)
    )
    return (
        f'<g opacity="{rnd.uniform(0.26, 0.70):.2f}" '
        f'style="animation:fall {rnd.uniform(9, 19):.2f}s linear infinite;'
        f'animation-delay:-{rnd.uniform(0, 19):.2f}s">'
        f'<text x="{x}" y="0" font-size="12" letter-spacing="2">{spans}</text></g>'
    )


def terminal_rows() -> str:
    parts = []
    y = CARD_Y + BAR_H + PAD + 10
    idx = 0
    for kind, a, b in ROWS:
        line = []
        if kind == "prompt":
            line.append(
                f'<text x="{CARD_X + PAD}" y="{y}"><tspan fill="{GREEN}" font-weight="700">❯ </tspan>'
                f'<tspan fill="{CMD}">{esc(a)}</tspan></text>'
            )
            if a == "":
                line.append(
                    f'<rect class="blink" x="{CARD_X + PAD + 18}" y="{y - 11}" width="8" height="14" fill="{CMD}"/>'
                )
        elif kind == "out":
            line.append(f'<text x="{CARD_X + PAD}" y="{y}" fill="{OUT}">{esc(a)}</text>')
        elif kind == "kv":
            line.append(f'<text x="{CARD_X + PAD}" y="{y}" fill="{GREEN}">{esc(a)}</text>')
            line.append(f'<text x="{CARD_X + PAD + 74}" y="{y}" fill="{OUT}">{esc(b)}</text>')
        if line:
            parts.append(
                f'<g class="ln" style="animation-delay:{idx * 0.09:.2f}s">' + "".join(line) + "</g>"
            )
        idx += 1
        y += ROW
    return "\n".join(parts)


def main() -> None:
    rnd = random.Random(20261116)
    cols = []
    x = 10
    while x < W:
        cols.append(rain_column(x, rnd))
        x += 22

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="CodePlayer — software engineer, agent tooling; terminal session">
<style>
  .rain text {{ font-family: {FONT}; fill: {GREEN}; }}
  .ui {{ font-family: {FONT}; }}
  text {{ font-family: {FONT}; }}
  .term text {{ font-size: {FS}px; white-space: pre; }}
  @keyframes fall {{ from {{ transform: translateY(-364px); }} to {{ transform: translateY(230px); }} }}
  @keyframes scan {{ 0% {{ transform: translateY(-10px); }} 100% {{ transform: translateY({H}px); }} }}
  @keyframes blink {{ 0%, 45% {{ opacity: 1; }} 50%, 95% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
  @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes glitchA {{
    0%, 90%, 100% {{ transform: translate(-3.5px, 0); }}
    91% {{ transform: translate(-7px, 0); }}
    93% {{ transform: translate(3px, -1px); }}
    95% {{ transform: translate(-1px, 1px); }}
    97% {{ transform: translate(2px, 0); }}
  }}
  @keyframes glitchB {{
    0%, 89%, 100% {{ transform: translate(3.5px, 0); }}
    90% {{ transform: translate(7px, 1px); }}
    92% {{ transform: translate(-3px, 0); }}
    94% {{ transform: translate(1px, -1px); }}
    96% {{ transform: translate(-2px, 0); }}
  }}
  @keyframes shake {{
    0%, 90%, 100% {{ transform: translate(0, 0); }}
    91% {{ transform: translate(1px, 0); }}
    93% {{ transform: translate(-1px, 1px); }}
    95% {{ transform: translate(1px, -1px); }}
  }}
  .scan {{ animation: scan 8s linear infinite; }}
  .blink {{ animation: blink 1.1s steps(1, end) infinite; }}
  .ln {{ animation: fade .28s ease both; }}
  .ga {{ animation: glitchA 5.5s steps(1, end) infinite; }}
  .gb {{ animation: glitchB 5.5s steps(1, end) infinite; animation-delay: .05s; }}
  .nm {{ animation: shake 5.5s steps(1, end) infinite; }}
</style>
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0.06"/>
    <stop offset="0.42" stop-color="#fff" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="rainMask"><rect width="{W}" height="{HERO_H}" fill="url(#fade)"/></mask>
  <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BG}" stop-opacity="0.97"/>
    <stop offset="0.68" stop-color="{BG}" stop-opacity="0.86"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0.10"/>
  </linearGradient>
  <linearGradient id="heroFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0.72" stop-color="{BG}" stop-opacity="0"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="scanGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
    <stop offset="0.3" stop-color="{GREEN}" stop-opacity="0.55"/>
    <stop offset="0.7" stop-color="{GREEN}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.45" cy="0.4" r="0.85">
    <stop offset="0.45" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.55"/>
  </radialGradient>
  <pattern id="crt" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.4" fill="#000" opacity="0.85"/>
  </pattern>
  <filter id="glow" x="-25%" y="-25%" width="150%" height="150%">
    <feDropShadow dx="0" dy="0" stdDeviation="9" flood-color="{GREEN}" flood-opacity="0.40"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2.5"/>
  </filter>
  <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.55"/>
  </filter>
  <clipPath id="cardClip">
    <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="10"/>
  </clipPath>
</defs>

<rect width="{W}" height="{H}" fill="{BG}"/>

<!-- 上半：二进制雨 -->
<g class="rain" mask="url(#rainMask)">
{chr(10).join(cols)}
</g>
<rect width="{W}" height="{HERO_H}" fill="url(#shade)"/>
<rect y="{HERO_H - 70}" width="{W}" height="70" fill="url(#heroFade)"/>

<!-- 角标 -->
<path d="M18 40 V18 H40" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0.55"/>
<path d="M{W - 40} {HERO_H - 26} H{W - 18} V{HERO_H - 48}" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0.4"/>

<!-- 名字（RGB 色散 + 故障） -->
<text class="ui ga" x="108" y="104" font-size="52" font-weight="700" fill="{CYAN}" opacity="0.55" letter-spacing="1.5">CodePlayer</text>
<text class="ui gb" x="108" y="104" font-size="52" font-weight="700" fill="{MAGENTA}" opacity="0.50" letter-spacing="1.5">CodePlayer</text>
<text class="ui nm" x="108" y="104" font-size="52" font-weight="700" fill="#f2f7fb" letter-spacing="1.5" filter="url(#glow)">CodePlayer</text>
<text class="ui" x="48" y="103" font-size="42" fill="{GREEN}" opacity="0.9">&gt;<tspan class="blink">_</tspan></text>
<text class="ui" x="110" y="140" font-size="14" fill="#8b949e" letter-spacing="0.6">Software engineer · 10 yrs · now building agent tooling</text>
<text class="ui" x="110" y="170" font-size="13" fill="{GREEN}" opacity="0.55" letter-spacing="1.4">01000011 01010000 · local-first · zero-bloat</text>
<text class="ui" x="48" y="{HERO_H - 14}" font-size="10" fill="#3a4653" letter-spacing="1.4">// 39.9042N 116.4074E · build 2026.11</text>

<!-- 下半：终端窗口 -->
<g filter="url(#cardShadow)">
  <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="10" fill="{PANEL}"/>
</g>
<g clip-path="url(#cardClip)">
  <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{BAR_H}" fill="{BAR}"/>
  <circle cx="{CARD_X + 22}" cy="{CARD_Y + BAR_H // 2}" r="6" fill="#ff5f57"/>
  <circle cx="{CARD_X + 42}" cy="{CARD_Y + BAR_H // 2}" r="6" fill="#febc2e"/>
  <circle cx="{CARD_X + 62}" cy="{CARD_Y + BAR_H // 2}" r="6" fill="#28c840"/>
  <text x="{CARD_X + CARD_W // 2}" y="{CARD_Y + BAR_H // 2 + 4}" fill="{DIM}" text-anchor="middle" font-size="12">caozeal@mac — zsh</text>
  <line x1="{CARD_X}" y1="{CARD_Y + BAR_H}" x2="{CARD_X + CARD_W}" y2="{CARD_Y + BAR_H}" stroke="{BORDER}"/>
  <g class="term">
{terminal_rows()}
  </g>
</g>
<rect x="{CARD_X + 0.5}" y="{CARD_Y + 0.5}" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="10" fill="none" stroke="{BORDER}"/>

<!-- 整屏 CRT 与扫描 -->
<rect width="{W}" height="{H}" fill="url(#crt)" opacity="0.10"/>
<rect width="{W}" height="{H}" fill="url(#vignette)"/>
<g class="scan">
  <rect x="0" y="0" width="{W}" height="1.5" fill="url(#scanGrad)" opacity="0.55"/>
  <rect x="0" y="-2" width="{W}" height="6" fill="url(#scanGrad)" opacity="0.22" filter="url(#soft)"/>
</g>
</svg>
"""
    out = Path(__file__).resolve().parent.parent / "assets" / "panel.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
