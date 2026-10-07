#!/usr/bin/env python3
"""
Step 4: Build neofetch-style info card SVG.
- Renders terminal window with macOS controls.
- Displays neofetch key/value rows (User, OS, Role, Stack, Highlights, etc.).
- Animated staggered line-by-line slide & fade in.
- Supports STATIC=1 environment variable for frozen preview.
"""

import os
import argparse
import html

# Customizable card configuration
DEFAULT_CONFIG = {
    "user": "swapnil@github",
    "title_bar": "swapnil ~ neofetch",
    "fields": [
        ("OS", "macOS Sonoma / Arch Linux"),
        ("Host", "GitHub Profile Workspace"),
        ("Uptime", "Always coding"),
        ("Role", "Software Engineer & Builder"),
        ("Languages", "Python, TypeScript, Go, C++, SQL"),
        ("Frameworks", "FastAPI, React, Next.js, Node.js"),
        ("Tools", "Docker, Git, Linux, Kubernetes, AWS"),
        ("Focus", "AI Agents, Distributed Systems, Open Source"),
        ("Location", "Mumbai, India"),
        ("Contact", "swapnil.patil24@spit.ac.in"),
    ]
}

COLORS = [
    "#21262d", "#ff7b72", "#7ee787", "#f2cc60",
    "#58a6ff", "#d2a8ff", "#79c0ff", "#f0f6fc"
]


def render_info_card_svg(output_path: str = "info-card.svg", config: dict = None, width: int = 490, height: int = 430):
    if config is None:
        config = DEFAULT_CONFIG

    is_static = os.getenv("STATIC", "0").lower() in ("1", "true", "yes")

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 8px; }')
    svg_lines.append('    .header-bar { fill: #161b22; }')
    svg_lines.append('    .dot-red { fill: #ff5f56; }')
    svg_lines.append('    .dot-yellow { fill: #ffbd2e; }')
    svg_lines.append('    .dot-green { fill: #27c93f; }')
    svg_lines.append('    .title { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg_lines.append('    .term-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12.5px; }')
    svg_lines.append('    .user-header { font-weight: bold; fill: #58a6ff; }')
    svg_lines.append('    .divider { fill: #30363d; }')
    svg_lines.append('    .key { font-weight: bold; fill: #79c0ff; }')
    svg_lines.append('    .val { fill: #c9d1d9; }')
    svg_lines.append('    .cursor { fill: #58a6ff; }')

    if not is_static:
        svg_lines.append('    @keyframes lineFadeIn {')
        svg_lines.append('      0% { opacity: 0; transform: translateY(6px); }')
        svg_lines.append('      100% { opacity: 1; transform: translateY(0); }')
        svg_lines.append('    }')
        svg_lines.append('    .stagger-line {')
        svg_lines.append('      opacity: 0;')
        svg_lines.append('      animation: lineFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;')
        svg_lines.append('    }')
        svg_lines.append('    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }')
        svg_lines.append('    .cursor { animation: blink 1s infinite; }')
    else:
        svg_lines.append('    .stagger-line { opacity: 1; }')

    svg_lines.append('  </style>')

    # Background window
    svg_lines.append(f'  <rect class="bg" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="8"/>')
    svg_lines.append(f'  <path class="header-bar" d="M1 1h{width - 2}v28H1z" rx="8"/>')
    svg_lines.append('  <circle class="dot-red" cx="16" cy="14" r="4"/>')
    svg_lines.append('  <circle class="dot-yellow" cx="28" cy="14" r="4"/>')
    svg_lines.append('  <circle class="dot-green" cx="40" cy="14" r="4"/>')
    svg_lines.append(f'  <text class="title" x="{width / 2}" y="17" text-anchor="middle">{html.escape(config.get("title_bar", "terminal"))}</text>')

    start_x = 24
    start_y = 60
    line_h = 22
    line_idx = 0

    # User title
    user_title = config.get("user", "user@github")
    delay = line_idx * 0.08
    svg_lines.append(f'  <g class="stagger-line" style="animation-delay: {delay:.2f}s;">')
    svg_lines.append(f'    <text class="term-text user-header" x="{start_x}" y="{start_y}">{html.escape(user_title)}</text>')
    svg_lines.append('  </g>')
    line_idx += 1

    # Divider
    divider_str = "-" * (len(user_title) + 4)
    delay = line_idx * 0.08
    y = start_y + line_idx * line_h - 4
    svg_lines.append(f'  <g class="stagger-line" style="animation-delay: {delay:.2f}s;">')
    svg_lines.append(f'    <text class="term-text divider" x="{start_x}" y="{y}">{divider_str}</text>')
    svg_lines.append('  </g>')
    line_idx += 1

    # Key / Value fields
    for k, v in config.get("fields", []):
        y = start_y + line_idx * line_h
        delay = line_idx * 0.08
        svg_lines.append(f'  <g class="stagger-line" style="animation-delay: {delay:.2f}s;">')
        svg_lines.append(f'    <text class="term-text key" x="{start_x}" y="{y}">{html.escape(k)}:</text>')
        svg_lines.append(f'    <text class="term-text val" x="{start_x + 105}" y="{y}">{html.escape(v)}</text>')
        svg_lines.append('  </g>')
        line_idx += 1

    # Color palette blocks
    palette_y = start_y + line_idx * line_h + 10
    delay = line_idx * 0.08
    svg_lines.append(f'  <g class="stagger-line" style="animation-delay: {delay:.2f}s;">')
    for ci, color in enumerate(COLORS):
        bx = start_x + ci * 24
        svg_lines.append(f'    <rect x="{bx}" y="{palette_y}" width="20" height="12" rx="2" fill="{color}"/>')
    svg_lines.append('  </g>')

    # Terminal prompt & blinking cursor
    cursor_y = palette_y + 30
    delay = (line_idx + 1) * 0.08
    svg_lines.append(f'  <g class="stagger-line" style="animation-delay: {delay:.2f}s;">')
    svg_lines.append(f'    <text class="term-text user-header" x="{start_x}" y="{cursor_y}">$</text>')
    svg_lines.append(f'    <rect class="cursor" x="{start_x + 14}" y="{cursor_y - 11}" width="7" height="13"/>')
    svg_lines.append('  </g>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines) + "\n")

    print(f"Generated info card SVG at {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate neofetch info card SVG.")
    parser.add_argument("-o", "--output", default="info-card.svg", help="Output SVG path (default: info-card.svg)")
    parser.add_argument("-w", "--width", type=int, default=490, help="Card width in px (default: 490)")
    parser.add_argument("-H", "--height", type=int, default=430, help="Card height in px (default: 430)")
    args = parser.parse_args()

    render_info_card_svg(output_path=args.output, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
