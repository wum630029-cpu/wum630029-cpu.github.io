#!/usr/bin/env python3
"""
IndexNow 自动推送脚本。
在 Hugo 构建完成后运行，将 sitemap 中的所有 URL 推送给 Bing 等搜索引擎。

用法：
  python3 scripts/push_indexnow.py

需要配置：
  - HOST: 你的域名
  - KEY: IndexNow API Key（已从 hugo.toml 的 meta 标签中提取）
"""
import xml.etree.ElementTree as ET
import urllib.request
import json
import sys
from pathlib import Path

# ========== 配置 ==========
HOST = "wum630029-cpu.github.io"
KEY = "7275888e4b33465699b61524ef72d30a"
SITEMAP_PATH = Path("/Users/wuzhimin/wum630029-cpu.github.io/public/sitemap.xml")
# 支持多个搜索引擎端点
ENDPOINTS = [
    "https://www.bing.com/indexnow",
    # "https://yandex.com/indexnow",  # 如需推送 Yandex，取消注释
]
# 每次推送的最大 URL 数量（IndexNow 限制）
BATCH_SIZE = 10000
# ==========================

def parse_sitemap(path: Path) -> list[str]:
    """解析 sitemap.xml，提取所有 URL"""
    if not path.exists():
        print(f"错误：找不到 sitemap 文件 {path}")
        sys.exit(1)

    tree = ET.parse(path)
    root = tree.getroot()
    # sitemap namespace
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text for loc in root.findall(".//ns:loc", ns)]
    return urls

def push_urls(urls: list[str]) -> bool:
    """批量推送 URL 给 IndexNow"""
    payload = {
        "host": HOST,
        "key": KEY,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")

    all_ok = True
    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": f"IndexNow-Python/{HOST}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                body = resp.read().decode("utf-8")
                if status == 200:
                    print(f"  ✓ {endpoint} - 成功 ({len(urls)} 个 URL)")
                else:
                    print(f"  ✗ {endpoint} - HTTP {status}: {body}")
                    all_ok = False
        except Exception as e:
            print(f"  ✗ {endpoint} - 错误: {e}")
            all_ok = False

    return all_ok

def push_single_url(url: str) -> bool:
    """推送单个 URL（GET 方式，适合 CI 中只推送新文章）"""
    all_ok = True
    for endpoint in ENDPOINTS:
        full_url = f"{endpoint}?url={url}&key={KEY}"
        try:
            with urllib.request.urlopen(full_url, timeout=30) as resp:
                status = resp.status
                if status == 200:
                    print(f"  ✓ {endpoint} - 成功推送 {url}")
                else:
                    print(f"  ✗ {endpoint} - HTTP {status} ({url})")
                    all_ok = False
        except Exception as e:
            print(f"  ✗ {endpoint} - 错误: {e} ({url})")
            all_ok = False
    return all_ok

def main():
    if not SITEMAP_PATH.exists():
        print("错误：请先运行 `hugo` 构建站点，生成 sitemap.xml")
        sys.exit(1)

    urls = parse_sitemap(SITEMAP_PATH)
    print(f"从 sitemap 读取到 {len(urls)} 个 URL")

    if len(urls) == 0:
        print("没有 URL 需要推送")
        return

    # 分批推送
    total = len(urls)
    ok_count = 0
    for i in range(0, total, BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        print(f"\n推送第 {i+1}-{min(i+BATCH_SIZE, total)} / {total} 个 URL...")
        if push_urls(batch):
            ok_count += len(batch)

    print(f"\n完成！成功推送 {ok_count}/{total} 个 URL")
    print("\n提示：首次推送后，建议将本脚本加入构建流程：")
    print("  hugo && python3 scripts/push_indexnow.py")

if __name__ == "__main__":
    main()
