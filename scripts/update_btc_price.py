#!/usr/bin/env python3
"""每月从 Binance 拉取 BTCUSDT 月度 K 线收盘价，更新定投计算器内嵌的 BTC_MONTHLY 数组。

用法：python3 scripts/update_btc_price.py
退出码：0 = 成功（含「无变化」）；1 = 出错。
"""
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1M&limit=500"
FILE = "content/tools/bitcoin-dca-calculator.md"


def fetch_klines():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def build_block(rows):
    lines = ["  var BTC_MONTHLY = ["]
    for i, (y, m, p) in enumerate(rows):
        comma = "," if i < len(rows) - 1 else ""
        lines.append(f"  [{y},{m},{p}]{comma}")
    lines.append("  ];")
    return "\n".join(lines)


def main():
    klines = fetch_klines()
    rows = []
    for k in klines:
        open_ms = k[0]
        close = float(k[4])
        dt = datetime.fromtimestamp(open_ms / 1000, tz=timezone.utc)
        rows.append((dt.year, dt.month, f"{close:.2f}"))

    if not rows:
        print("❌ Binance 返回空数据")
        sys.exit(1)

    with open(FILE, encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"  var BTC_MONTHLY = \[.*?\n  \];", re.S)
    new_block = build_block(rows)
    new_content, n = pattern.subn(lambda _m: new_block, content, count=1)
    if n != 1:
        print("❌ 未找到 BTC_MONTHLY 数组块，中止")
        sys.exit(1)

    if new_content == content:
        print(f"ℹ️ 数据无变化（共 {len(rows)} 个月，最新 {rows[-1]}）")
        sys.exit(0)

    with open(FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ 已更新 {len(rows)} 个月度价格，最新 {rows[-1]}")
    sys.exit(0)


if __name__ == "__main__":
    main()
