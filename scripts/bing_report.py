#!/usr/bin/env python3
"""
Bing 周报脚本：拉 coinvado.net 的查询、页面、点击/展示数据，直接在终端看排名和流量。

用法：
  BING_API_KEY=你的key python3 scripts/bing_report.py

需要：
  pip install requests   （有 certifi 就用系统证书，避免 SSL 报错）

输出：
  1) 近 90 天每日点击/展示
  2) 查询词 Top 20（按展示）
  3) 页面 Top 20（按展示）
  4) 注册/下载/邀请码类转化词的排名现状
"""
import os
import sys
from collections import defaultdict

import requests

try:
    import certifi

    VERIFY = certifi.where()
except ImportError:  # pragma: no cover
    VERIFY = True

BASE = "https://ssl.bing.com/webmaster/api.svc/json/"
SITE = "https://coinvado.net"
CLUSTER_KEYWORDS = {
    "USDT/汇率": ["usdt", "汇率", "兑换人民币", "换人民币", "泰达币"],
    "币安卡": ["币安卡", "binance card", "虚拟卡", "u卡", "u 卡"],
    "提现/出金": ["提现", "出金", "卖币"],
    "充值/入金": ["充值", "入金", "怎么买"],
    "C2C": ["c2c", "p2p"],
    "Pay/支付": ["binance pay", "币安支付", "币安pay"],
    "注册/下载/邀请码": ["注册", "下载", "邀请码", "开户", "app", "官网", "bt123"],
}


def fetch(method: str, key: str) -> list:
    resp = requests.get(
        BASE + method,
        params={"apikey": key, "siteUrl": SITE},
        verify=VERIFY,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json().get("d", []) or []


def main() -> None:
    key = os.environ.get("BING_API_KEY")
    if not key:
        print("错误：请先设置环境变量 BING_API_KEY")
        sys.exit(1)

    queries = defaultdict(lambda: [0, 0, 0.0, 0])
    for row in fetch("GetQueryStats", key):
        q = (row.get("Query") or "").strip().lower()
        if not q:
            continue
        imp = row.get("Impressions", 0) or 0
        entry = queries[q]
        entry[0] += row.get("Clicks", 0) or 0
        entry[1] += imp
        entry[2] += (row.get("AvgImpressionPosition") or 0) * max(imp, 1)
        entry[3] += max(imp, 1)

    pages = defaultdict(lambda: [0, 0, 0.0, 0])
    for row in fetch("GetPageStats", key):
        url = row.get("Query") or row.get("Url") or ""
        imp = row.get("Impressions", 0) or 0
        entry = pages[url]
        entry[0] += row.get("Clicks", 0) or 0
        entry[1] += imp
        entry[2] += (row.get("AvgImpressionPosition") or 0) * max(imp, 1)
        entry[3] += max(imp, 1)

    traffic = fetch("GetRankAndTrafficStats", key)
    if traffic:
        imp = sum(r.get("Impressions", 0) or 0 for r in traffic)
        clicks = sum(r.get("Clicks", 0) or 0 for r in traffic)
        print(f"== 流量（{len(traffic)} 天）==")
        print(f"展示 {imp:,} | 点击 {clicks:,} | 日均 {clicks / len(traffic):.1f} 点击\n")

    def top(items, n=20):
        rows = [
            (k, v[0], v[1], v[2] / v[3] if v[3] else 0)
            for k, v in items.items()
        ]
        return sorted(rows, key=lambda r: -r[2])[:n]

    print("== 查询词 Top 20（展示）==")
    for q, clicks, imp, pos in top(queries):
        print(f"{imp:6} 展示 {clicks:4} 点击  排名 {pos:4.1f}  {q}")

    print("\n== 页面 Top 20（展示）==")
    for url, clicks, imp, pos in top(pages):
        print(f"{imp:6} 展示 {clicks:4} 点击  排名 {pos:4.1f}  {url}")

    print("\n== 集群表现 ==")
    total = sum(v[1] for v in queries.values()) or 1
    for name, keys in CLUSTER_KEYWORDS.items():
        sel = {k: v for k, v in queries.items() if any(word in k for word in keys)}
        imp = sum(v[1] for v in sel.values())
        clicks = sum(v[0] for v in sel.values())
        pos = sum(v[2] for v in sel.values()) / max(sum(v[3] for v in sel.values()), 1)
        print(
            f"{name:16} 展示 {imp:6}（{imp / total:5.1%}）"
            f" 点击 {clicks:4}  CTR {clicks / max(imp, 1):5.1%}  排名 {pos:4.1f}"
        )


if __name__ == "__main__":
    main()
