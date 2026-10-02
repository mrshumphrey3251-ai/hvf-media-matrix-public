"""
HVF Executive Presentation Compiler — Hardened Regex Markdown to Standalone HTML Deck
DFARS 252.227-7018 Compliant Architecture.
"""

import os
import sys
import re

def parse_markdown_to_slides(md_content: str):
    # Strip Byte Order Mark (BOM) and leading/trailing whitespace
    content = md_content.lstrip("\ufeff").strip()
    
    # Strip YAML frontmatter between opening and closing ---
    frontmatter_pattern = r'^---\s*\n.*?\n---\s*(\n|$)'
    content = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL).strip()
    
    # Split slides ONLY on lines containing strictly '---'
    raw_slides = re.split(r'(?m)^\s*---\s*$', content)
    slides = [s.strip() for s in raw_slides if s.strip()]
    return slides

def markdown_chunk_to_html(chunk: str) -> str:
    lines = chunk.splitlines()
    html_lines = []
    in_list = False
    in_table = False
    table_rows = []
    
    for line in lines:
        line_str = line.strip()
        
        # Detect Markdown Table Row
        if line_str.startswith("|") and line_str.endswith("|"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
                
            cols = [c.strip() for c in line_str.split("|")[1:-1]]
            # Skip Markdown alignment rows like | :--- | :--- |
            if all(set(c).issubset({'-', ':', ' '}) for c in cols if c):
                continue
                
            table_rows.append(cols)
            in_table = True
            continue
        else:
            if in_table:
                t_html = ["<table>"]
                for r_idx, row in enumerate(table_rows):
                    tag = "th" if r_idx == 0 else "td"
                    cells = "".join(f"<{tag}>{c}</{tag}>" for c in row)
                    t_html.append(f"<tr>{cells}</tr>")
                t_html.append("</table>")
                html_lines.append("".join(t_html))
                table_rows = []
                in_table = False

        # Headers
        if line_str.startswith("# "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h1>{line_str[2:]}</h1>")
            continue
        elif line_str.startswith("## "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h2>{line_str[3:]}</h2>")
            continue
        elif line_str.startswith("### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h3>{line_str[4:]}</h3>")
            continue
            
        # Lists
        if line_str.startswith("* ") or line_str.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = line_str[2:]
            html_lines.append(f"<li>{item_text}</li>")
            continue
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
                
        # Paragraphs
        if line_str:
            html_lines.append(f"<p>{line_str}</p>")
            
    if in_list:
        html_lines.append("</ul>")
    if in_table:
        t_html = ["<table>"]
        for r_idx, row in enumerate(table_rows):
            tag = "th" if r_idx == 0 else "td"
            cells = "".join(f"<{tag}>{c}</{tag}>" for c in row)
            t_html.append(f"<tr>{cells}</tr>")
        t_html.append("</table>")
        html_lines.append("".join(t_html))

    raw_html = "\n".join(html_lines)
    raw_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', raw_html)
    raw_html = re.sub(r'`(.*?)`', r'<code>\1</code>', raw_html)
    return raw_html

def compile_deck(source_path: str, output_path: str):
    with open(source_path, "r", encoding="utf-8") as f:
        md = f.read()

    slides_md = parse_markdown_to_slides(md)
    slides_html = [markdown_chunk_to_html(s) for s in slides_md]

    slides_divs = []
    for idx, s_html in enumerate(slides_html):
        active_class = " active" if idx == 0 else ""
        slides_divs.append(f"""
        <div class="slide{active_class}" id="slide-{idx+1}">
            <div class="slide-content">
                {s_html}
            </div>
            <div class="slide-footer">
                <span>HVF SOVEREIGN SCADA DEFENSE MATRIX | CAGE: 1AHA8 | OK HB 2992 & DFARS 252.227-7018</span>
                <span>SLIDE {idx+1} OF {len(slides_html)}</span>
            </div>
        </div>
        """)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT EBONY: Sovereign SCADA Defense -- Executive Briefing</title>
    <style>
        :root {{
            --bg-void: #06090e;
            --bg-panel: #0d131a;
            --border-dim: #1f2d3d;
            --accent-cyan: #00f0ff;
            --accent-green: #00ff88;
            --text-main: #e2e8f0;
            --text-dim: #94a3b8;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-void);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .deck-container {{
            width: 92vw;
            max-width: 1250px;
            height: 88vh;
            max-height: 780px;
            background-color: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        .slide {{
            display: none;
            flex-direction: column;
            height: 100%;
            padding: 48px 64px;
            overflow-y: auto;
        }}
        .slide.active {{
            display: flex;
        }}
        .slide-content {{
            flex: 1;
        }}
        h1 {{
            color: var(--accent-cyan);
            font-size: 2.3rem;
            margin-top: 10px;
            margin-bottom: 12px;
            letter-spacing: 1px;
            border-bottom: 2px solid var(--accent-cyan);
            padding-bottom: 12px;
        }}
        h2 {{
            color: var(--accent-cyan);
            font-size: 1.85rem;
            margin-top: 0;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-dim);
            padding-bottom: 8px;
        }}
        h3 {{
            color: var(--text-dim);
            font-size: 1.2rem;
            font-weight: 400;
            margin-top: 0;
            margin-bottom: 24px;
        }}
        p, li {{
            font-size: 1.12rem;
            line-height: 1.65;
            color: var(--text-main);
        }}
        ul {{
            margin-top: 16px;
            padding-left: 28px;
        }}
        li {{
            margin-bottom: 14px;
        }}
        strong {{
            color: #ffffff;
            font-weight: 700;
        }}
        code {{
            background-color: rgba(0, 240, 255, 0.1);
            color: var(--accent-cyan);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            border: 1px solid rgba(0, 240, 255, 0.2);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 0.95rem;
        }}
        th, td {{
            border: 1px solid var(--border-dim);
            padding: 12px 16px;
            text-align: left;
        }}
        th {{
            background-color: rgba(0, 240, 255, 0.08);
            color: var(--accent-cyan);
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        td {{
            background-color: rgba(13, 19, 26, 0.7);
        }}
        .slide-footer {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            color: var(--text-dim);
            border-top: 1px solid var(--border-dim);
            padding-top: 14px;
            margin-top: 18px;
            font-family: monospace;
        }}
        .controls {{
            position: absolute;
            bottom: 20px;
            right: 32px;
            display: flex;
            gap: 12px;
            z-index: 100;
        }}
        button {{
            background-color: #1e293b;
            color: var(--text-main);
            border: 1px solid var(--border-dim);
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-family: monospace;
            font-weight: bold;
            transition: all 0.2s;
        }}
        button:hover {{
            background-color: var(--accent-cyan);
            color: var(--bg-void);
            border-color: var(--accent-cyan);
        }}
        @media print {{
            body {{
                overflow: visible;
                height: auto;
                background-color: #ffffff;
                color: #000000;
            }}
            .deck-container {{
                width: 100%;
                max-width: none;
                height: auto;
                max-height: none;
                border: none;
                box-shadow: none;
            }}
            .slide {{
                display: flex !important;
                page-break-after: always;
                height: 100vh;
                border-bottom: 2px solid #ccc;
            }}
            .controls {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="deck-container">
        {"".join(slides_divs)}
    </div>
    <div class="controls">
        <button onclick="prevSlide()">&larr; PREV</button>
        <button onclick="nextSlide()">NEXT &rarr;</button>
        <button onclick="window.print()">PRINT / PDF</button>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');

        function showSlide(index) {{
            slides[currentSlide].classList.remove('active');
            currentSlide = (index + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');
        }}

        function nextSlide() {{ showSlide(currentSlide + 1); }}
        function prevSlide() {{ showSlide(currentSlide - 1); }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
                prevSlide();
            }}
        }});
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[SUCCESS] Re-compiled {len(slides_md)} clean slides into: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    src = "governance/briefings/2026-09-25_oklahoma_commerce_executive_briefing.md"
    dst = "governance/briefings/2026-09-25_oklahoma_commerce_executive_briefing.html"
    compile_deck(src, dst)
