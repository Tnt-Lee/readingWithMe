#!/usr/bin/env python3
"""
python build_index_flat.py  /绝对/或/相对/路径
"""
import os
from pathlib import Path

def build_index_flat(target_dir):
    target = Path(target_dir).expanduser().resolve()
    if not target.is_dir():
        print(f"❌ {target} 不是有效目录")
        return

    # 仅扫描当前目录 *.html
    html_files = sorted(p.name for p in target.glob('*.html'))

    if not html_files:
        print("⚠️ 该目录下没有 .html 文件")
        return

    index_path = target / 'index.html'
    lines = [
        '<!doctype html><html><head>',
        '<meta charset="utf-8"><title>目录索引</title>',
        '<style>body{font-family:sans-serif;margin:0}</style>',
        '</head><body>',

        # ↓↓↓ 新增导航
        '<nav style="position:sticky;top:0;background:#f5f5f5;padding:8px 12px;border-bottom:1px solid #ddd;display:flex;gap:12px;font-family:sans-serif;z-index:999;">'
        '<button onclick="history.back()" style="cursor:pointer;">← 返回上一页</button>'
        '<button onclick="location.href=\'index.html\'" style="cursor:pointer;">🏠 首页</button>'
        '</nav>',

        f'<h1 style="margin:40px">{target.name} 目录下的 HTML 文件</h1><ul>'
    ]
    for name in html_files:
        lines.append(f'<li><a href="{name}">{name}</a></li>')
    lines.append('</ul></body></html>')
    index_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✅ 已在 {index_path} 生成索引，共 {len(html_files)} 个链接")

if __name__ == '__main__':
    build_index_flat(r"app001/toHtml")