#!/usr/bin/env python3
import os
import re
import glob

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            font-size: 15px;
            color: #1f2937;
            line-height: 1.6;
            background-color: #f9fafb;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .nav-bar {{
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 13px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .nav-bar a {{
            color: #3b82f6;
            text-decoration: none;
        }}
        .nav-bar a:hover {{
            text-decoration: underline;
        }}
        .card {{
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        h1 {{
            font-size: 24px;
            color: #111827;
            margin-top: 0;
            margin-bottom: 12px;
        }}
        h2 {{
            font-size: 18px;
            color: #1f2937;
            margin-top: 20px;
            margin-bottom: 10px;
            border-bottom: 1px solid #f3f4f6;
            padding-bottom: 5px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
        }}
        .badge-plan {{ background-color: #fef3c7; color: #92400e; }}
        .badge-spec {{ background-color: #d1fae5; color: #065f46; }}
        .badge-changelog {{ background-color: #e0f2fe; color: #0369a1; }}
        
        ul {{
            padding-left: 20px;
            margin: 10px 0;
        }}
        li {{
            margin-bottom: 8px;
        }}
        details {{
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px 15px;
            margin-top: 15px;
            background-color: #f9fafb;
        }}
        summary {{
            font-weight: 600;
            cursor: pointer;
            outline: none;
            color: #4b5563;
        }}
        summary:hover {{
            color: #111827;
        }}
        pre {{
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            margin: 10px 0;
        }}
        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            background-color: #f3f4f6;
            padding: 2px 4px;
            border-radius: 4px;
        }}
        .highlight-add {{ background-color: #d1fae5; }}
        .highlight-del {{ background-color: #fee2e2; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav-bar">
            <strong>Logs:</strong>
            {nav_links}
        </div>
        <div class="card">
            <h1>{title}</h1>
            <div>
                <span class="badge {badge_class}">{badge_text}</span>
            </div>
            {summary_content}
        </div>
        
        <div class="card">
            <h2>Core Takeaways</h2>
            {core_points}
        </div>

        <div class="card">
            <h2>Technical Details</h2>
            <details>
                <summary>View Complete Specifications & Diffs</summary>
                {detailed_content}
            </details>
        </div>
    </div>
</body>
</html>
"""

def parse_inline_markdown(text):
    # Parse inline code: `code` -> <code>code</code>
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Parse bold: **text** -> <strong>text</strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Parse italic: *text* -> <em>text</em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Parse links: [text](url) -> <a href="\2">\1</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Parse checklists
    text = text.replace('[ ]', '&#9744;').replace('[x]', '&#9745;').replace('[X]', '&#9745;')
    return text

def md_to_html_snippets(md_content):
    html_lines = []
    in_code_block = False
    in_blockquote = False
    
    for line in md_content.split('\n'):
        if line.startswith('```'):
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            if in_code_block:
                html_lines.append('</pre>')
                in_code_block = False
            else:
                html_lines.append('<pre>')
                in_code_block = True
            continue
        
        if in_code_block:
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            if escaped.startswith('+'):
                html_lines.append(f'<span class="highlight-add">{escaped}</span>')
            elif escaped.startswith('-'):
                html_lines.append(f'<span class="highlight-del">{escaped}</span>')
            else:
                html_lines.append(escaped)
            continue

        # Horizontal rule
        if line.strip() == '---':
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('<hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;">')
            continue

        # Blockquote
        if line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote style="border-left: 4px solid #d1d5db; padding-left: 15px; color: #4b5563; margin: 15px 0; font-style: italic;">')
                in_blockquote = True
            line_text = parse_inline_markdown(line[2:])
            html_lines.append(f'<p>{line_text}</p>')
            continue
        elif in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False

        if line.startswith('# '):
            html_lines.append(f'<h1>{parse_inline_markdown(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{parse_inline_markdown(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{parse_inline_markdown(line[4:])}</h3>')
        elif line.startswith('- ') or line.startswith('* '):
            item = parse_inline_markdown(line[2:])
            html_lines.append(f'<li>{item}</li>')
        else:
            p_text = parse_inline_markdown(line)
            if p_text.strip():
                html_lines.append(f'<p>{p_text}</p>')
    
    if in_blockquote:
        html_lines.append('</blockquote>')
        
    return '\n'.join(html_lines)

def process_file(md_path, all_files, output_dir):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(md_path)
    title = filename.replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    # Determine badge based on file name or content
    if 'changelog' in filename.lower():
        badge_class = 'badge-changelog'
        badge_text = 'Changelog'
    elif 'implementation' in filename.lower() or 'plan' in filename.lower():
        badge_class = 'badge-plan'
        badge_text = 'Implementation Plan'
    elif 'spec' in filename.lower() or 'design' in filename.lower():
        badge_class = 'badge-spec'
        badge_text = 'Design Spec'
    else:
        badge_class = 'badge-plan'
        badge_text = 'Implementation'
 
    # Build Navigation Links
    nav_items = []
    for other_path in all_files:
        other_name = os.path.basename(other_path).replace('.md', '.html')
        other_title = other_name.replace('.html', '').replace('_', ' ').replace('-', ' ').title()
        nav_items.append(f'<a href="{other_name}">{other_title}</a>')
    nav_links = ' | '.join(nav_items)
 
    # Extract goal/summary/objective
    summary_match = re.search(r'\*\*Goal:\*\*?\s*(.*?)(?:\n|\Z)', content)
    if not summary_match:
        obj_match = re.search(r'## Objective\s*\n*(.*?)(?:\n\n|\Z)', content, re.DOTALL)
        if obj_match:
            summary_content = f"<p><strong>Objective:</strong> {parse_inline_markdown(obj_match.group(1).strip())}</p>"
        else:
            exec_match = re.search(r'## Executive Summary.*?\n*(.*?)(?:\n\n|\Z)', content, re.DOTALL)
            if exec_match:
                summary_content = f"<p><strong>Summary:</strong> {parse_inline_markdown(exec_match.group(1).strip())}</p>"
            else:
                summary_content = "<p>Development diary log entry.</p>"
    else:
        summary_content = f"<p><strong>Goal:</strong> {parse_inline_markdown(summary_match.group(1))}</p>"
 
    # Extract list items for core points
    core_points = "<ul>"
    points_found = False
    for line in content.split('\n'):
        if line.startswith('- ') or line.startswith('* '):
            if 'TBD' not in line and 'TODO' not in line:
                item = parse_inline_markdown(line[2:])
                core_points += f"<li>{item}</li>"
                points_found = True
    core_points += "</ul>"
    if not points_found:
        core_points = "<p>See technical details below for the full update path.</p>"
 
    detailed_content = md_to_html_snippets(content)
 
    html_content = TEMPLATE.format(
        title=title,
        nav_links=nav_links,
        badge_class=badge_class,
        badge_text=badge_text,
        summary_content=summary_content,
        core_points=core_points,
        detailed_content=detailed_content
    )
 
    out_name = filename.replace('.md', '.html')
    out_path = os.path.join(output_dir, out_name)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated: {out_path}")

def main():
    input_dir = "/afs/cern.ch/work/l/lichengz/private/VHbb/cms-taug2-run3/docs/diary-log"
    output_dir = "/eos/user/l/lichengz/WEB-PORTAL/external/daily-html/cms-run3-tau-g-2/2026"
    
    md_files = glob.glob(os.path.join(input_dir, "*.md"))
    md_files.sort()
    
    for md_path in md_files:
        process_file(md_path, md_files, output_dir)

if __name__ == '__main__':
    main()
