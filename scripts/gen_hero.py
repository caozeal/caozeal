#!/usr/bin/env python3
"""生成 profile README 的 hero SVG：二进制雨 + 名字。纯标准库。"""
import random
from pathlib import Path

W, H = 900, 230
GREEN = "#39d353"
BG = "#0a0e13"
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def column(x: int, rnd: random.Random) -> str:
    n = 26
    spans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 14}">{rnd.choice("01")}</tspan>'
        for i in range(n)
    )
    dur = rnd.uniform(9, 19)
    delay = -rnd.uniform(0, 19)
    op = rnd.uniform(0.26, 0.70)
    return (
        f'<g opacity="{op:.2f}" style="animation:fall {dur:.2f}s linear infinite;'
        f'animation-delay:{delay:.2f}s">'
        f'<text x="{x}" y="0" font-size="12" letter-spacing="2">{spans}</text></g>'
    )


def main() -> None:
    rnd = random.Random(20261116)
    cols = []
    x = 10
    while x < W:
        cols.append(column(x, rnd))
        x += 22

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="CodePlayer — software engineer, AI tooling">
<style>
  .rain text {{ font-family: {FONT}; fill: {GREEN}; }}
  .ui {{ font-family: {FONT}; }}
  @keyframes fall {{ from {{ transform: translateY(-364px); }} to {{ transform: translateY(230px); }} }}
  @keyframes scan {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(228px); }} }}
  @keyframes blink {{ 0%, 45% {{ opacity: 1; }} 50%, 95% {{ opacity: .15; }} 100% {{ opacity: 1; }} }}
  .scan {{ animation: scan 7s linear infinite; }}
  .blink {{ animation: blink 1.6s steps(1, end) infinite; }}
</style>
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0.06"/>
    <stop offset="0.42" stop-color="#fff" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <filter id="glow" x="-25%" y="-25%" width="150%" height="150%">
    <feDropShadow dx="0" dy="0" stdDeviation="9" flood-color="#39d353" flood-opacity="0.40"/>
  </filter>
  <mask id="rainMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BG}" stop-opacity="0.97"/>
    <stop offset="0.68" stop-color="{BG}" stop-opacity="0.86"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0.10"/>
  </linearGradient>
</defs>

<rect width="{W}" height="{H}" fill="{BG}"/>
<g class="rain" mask="url(#rainMask)">
{chr(10).join(cols)}
</g>
<rect width="{W}" height="{H}" fill="url(#shade)"/>
<rect class="scan" x="0" y="0" width="{W}" height="1.5" fill="{GREEN}" opacity="0.16"/>

<!-- 边框与角标 -->
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="#1d2733"/>
<path d="M18 40 V18 H40" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0.55"/>
<path d="M{W - 40} {H - 18} H{W - 18} V{H - 40}" fill="none" stroke="{GREEN}" stroke-width="2" opacity="0.55"/>

<!-- 正文 -->
<text class="ui" x="48" y="103" font-size="42" fill="{GREEN}" opacity="0.9">&gt;<tspan class="blink">_</tspan></text>
<text class="ui" x="108" y="104" font-size="52" font-weight="700" fill="#f2f7fb" letter-spacing="1.5" filter="url(#glow)">CodePlayer</text>
<text class="ui" x="110" y="140" font-size="14" fill="#8b949e" letter-spacing="0.6">Software engineer · 10 yrs · now building agent tooling</text>
<text class="ui" x="110" y="170" font-size="13" fill="{GREEN}" opacity="0.55" letter-spacing="1.4">01000011 01010000 · local-first · zero-bloat</text>

<!-- 右下角坐标 -->
<text class="ui" x="48" y="{H - 14}" font-size="10" fill="#2e3947" letter-spacing="1.4">// 39.9042N 116.4074E · build 2026.11</text>
</svg>
"""
    out = Path(__file__).resolve().parent.parent / "assets" / "hero.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes, {len(cols)} columns)")


if __name__ == "__main__":
    main()
