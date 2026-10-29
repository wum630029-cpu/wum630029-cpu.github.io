#!/usr/bin/env python3
"""
IndexNow 删除通知脚本。

文章批量下架后运行，把已删除的旧 URL 提交给 Bing 等搜索引擎，
让它们尽快重新抓取、确认 404 并从索引里移除。

用法：
  python3 scripts/indexnow_removed.py

注意：
  - URL 列表来自 scripts/removed-urls.txt（每行一个完整 URL）
  - 必须在删除已经生效（旧 URL 真的返回 404）之后运行，
    否则搜索引擎重新抓取时会看到 200，等同于告诉它页面还在
"""
import json
import sys
import urllib.request
from pathlib import Path

# ========== 配置 ==========
HOST = "coinvado.net"
KEY = "7275888e4b33465699b61524ef72d30a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
URLS_PATH = Path(__file__).with_name("removed-urls.txt")
BATCH_SIZE = 10000  # IndexNow 单次上限
ENDPOINT = "https://www.bing.com/indexnow"
# ==========================


def push(urls: list[str]) -> int:
    payload = json.dumps(
        {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}
    ).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        print(e.read().decode("utf-8", "ignore"))
        return e.code


def main() -> None:
    if not URLS_PATH.exists():
        print(f"错误：找不到 {URLS_PATH}")
        sys.exit(1)

    urls = [line.strip() for line in URLS_PATH.read_text().splitlines() if line.strip().startswith("http")]
    if not urls:
        print("错误：URL 列表为空")
        sys.exit(1)

    print(f"待通知删除的 URL：{len(urls)} 个")
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i : i + BATCH_SIZE]
        code = push(batch)
        print(f"批次 {i // BATCH_SIZE + 1}：{len(batch)} 条 → HTTP {code}")
        if code not in (200, 202):
            sys.exit(1)
    print("完成")


if __name__ == "__main__":
    main()
