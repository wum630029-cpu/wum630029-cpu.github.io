#!/usr/bin/env python3
"""
批量优化 Hugo 文章 frontmatter 中的 description 长度。
规则：description 控制在 50-155 字符之间，超出部分在最后一个完整标点处截断。
"""
import re
from pathlib import Path

CONTENT_DIR = Path("/Users/wuzhimin/wum630029-cpu.github.io/content")
# 中文和英文标点
PUNCTUATIONS = set("。，；！？.,;!?")

def truncate_at_punct(text: str, max_len: int = 150) -> str:
    """在 max_len 之前最后一个标点处截断"""
    if len(text) <= max_len:
        return text
    # 从 max_len 往前找第一个标点
    for i in range(max_len, 0, -1):
        if text[i] in PUNCTUATIONS:
            return text[:i+1]
    # 如果没找到标点，直接截断
    return text[:max_len]

def process_file(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None

    # 规范化非标准 frontmatter：---title: -> ---\ntitle:
    if not text.startswith("---\n"):
        text = text.replace("---", "---\n", 1)

    # 找到 frontmatter 结束位置
    end_match = re.search(r'\n---\s*\n', text[3:])
    if not end_match:
        return None

    front_end = 3 + end_match.end()
    frontmatter = text[3:3+end_match.start()]
    body = text[front_end:]

    # 提取 description
    desc_match = re.search(r"^description:\s*['\"]?(.*?)(?<!\\)['\"]?\s*$", frontmatter, re.MULTILINE)
    if not desc_match:
        return None

    original_desc = desc_match.group(1).strip().strip("'\"")
    original_len = len(original_desc)

    if original_len <= 155:
        return None  # 不需要修改

    new_desc = truncate_at_punct(original_desc, 150)
    new_len = len(new_desc)

    # 替换 frontmatter 中的 description
    old_line = desc_match.group(0)
    new_line = f"description: '{new_desc}'"
    new_frontmatter = frontmatter.replace(old_line, new_line, 1)

    # 确保 frontmatter 末尾有换行符，避免 --- 粘连
    if not new_frontmatter.endswith("\n"):
        new_frontmatter += "\n"

    new_text = f"---\n{new_frontmatter}---\n{body}"
    md_path.write_text(new_text, encoding="utf-8")

    return {
        "file": str(md_path),
        "before": original_desc,
        "before_len": original_len,
        "after": new_desc,
        "after_len": new_len,
    }

def main():
    files = list(CONTENT_DIR.rglob("*.md"))
    results = []
    for f in files:
        result = process_file(f)
        if result:
            results.append(result)

    print(f"已优化 {len(results)} 个文件的 description")
    for r in results[:10]:
        print(f"  {r['file'].split('/')[-1]}: {r['before_len']} → {r['after_len']} 字符")
    if len(results) > 10:
        print(f"  ... 还有 {len(results)-10} 个文件")

if __name__ == "__main__":
    main()
