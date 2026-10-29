# Bing 重建计划（2026-10-29 起）

> 目标：Bing 收录 → 排名 → 点击 → 流量 → 注册。
> 数据来源：Bing Webmaster API 实测（2026-10-29 拉取），旧站 203 篇文章已全部下架，旧 URL 404。

## 一、重建前的基线（别再凭感觉选题）

| 指标 | 数值 |
|---|---|
| 91 天展示 / 点击 | 26,862 / 1,128（日均 12.4 点击，CTR 4.2%） |
| 近 43 天展示 / 点击 | 5,978 / 589 |
| 流量集中度 | USDT 集群占 **48.6%** 展示 |

按集群拆（近 43 天）：

| 集群 | 展示占比 | 点击 | CTR | 平均排名 | 判断 |
|---|---:|---:|---:|---:|---|
| USDT 汇率/兑换 | **48.6%** | 65 | 2.2% | 8.1 | 基本盘，排名差，**最大提升空间** |
| 币安卡/虚拟卡 | 6.0% | 98 | **27.1%** | **3.2** | 排名最好，**要扩量** |
| 概念词（MetaMask/合约等） | 10.0% | 52 | 8.7% | 6.0 | 稳定辅助 |
| 注册/下载/邀请码 | 4.4% | 13 | 4.9% | 7.8 | 转化词，**排名最差** |
| C2C | 3.3% | 16 | 8.1% | 6.2 | 中 |
| 手续费/API/量化 | 3.3% | 26 | 13.0% | 6.5 | 中 |
| Binance Pay | 2.2% | 22 | 16.7% | 4.4 | 小而稳 |
| 充值/入金 | 1.5% | 12 | 13.2% | 4.6 | 小但转化 |
| 提现/出金 | 1.4% | 26 | **30.2%** | 4.8 | 小但转化最高 |

**三条结论**

1. 先恢复 USDT 汇率：它决定展示量的天花板，排名 8.1 → 前 5，点击能翻数倍。
2. 币安卡集群是现成的优势项（排名 3.2、CTR 27%），直接扩成 3 篇。
3. 注册/邀请码是转化词但排名最差，别指望它带量，靠内链从流量页导过去。

## 二、目标（可验收）

| 时间 | 收录 | 日展示 | 月点击 |
|---|---|---:|---:|
| 4 周 | 18 篇上线并收录 | ≥ 150 | ≥ 300 |
| 8 周 | 24 篇 | ≥ 300 | ≥ 900 |
| 12 周 | 30 篇 | ≥ 500 | ≥ 1,500，USDT 页进前 5 |

## 三、slug 策略

**建议破例：6 个流量页沿用旧 slug，其余一律新 slug。**

| 沿用 slug | 91 天数据 | 理由 |
|---|---|---|
| `usdt-to-cny-guide` | 5,569 展示 / 102 点击 | 全站第一，换成新 slug 等于从零爬 |
| `binance-withdraw-guide` | 2,281 / 109 | 第二 |
| `binance-card-guide` | 1,256 / 216 | 点击第一，排名 3.3 |
| `binance-deposit-guide` | 822 / 46 | 转化路径 |
| `binance-pay-guide` | 596 / 57 | 稳定 |
| `binance-c2c-guide` | 256 / 11 | 稳定 |

Bing 指南 §20「保持 URL 稳定」——同一 URL 重发新内容，历史权重能接上；换新 slug 则一切归零。
如果坚持全新 slug，把这 6 篇换成：`usdt-cny-rate-2027`、`binance-withdraw-card-guide`、`binance-card-apply-guide`、`binance-recharge-guide`、`binance-pay-transfer-guide`、`binance-c2c-buy-sell-guide`。

## 四、18 篇排期（6 周，每周 3 篇）

节奏说明：每周 3 篇是按 Bing 反垃圾条款（避免大规模无审核生成）定的上限，别冲量。

### 第 1 周：恢复基本盘 + 转化入口

| 天数 | slug | 目标主词 | 标题（43–53 字） |
|---|---|---|---|
| 周一 | `usdt-to-cny-guide` | usdt 汇率 / usdt 兑人民币 | USDT 兑人民币汇率怎么看？2026 场内场外价差、卖出到手价、手续费与到账时间一次算清 |
| 周三 | `binance-register-guide` | 币安注册 | 币安怎么注册？大陆用户开户、KYC 实名认证与 BT123 邀请码 20% 返佣图文教程 |
| 周五 | `binance-card-guide` | 币安卡 / binance card | 币安卡怎么申请？虚拟卡、U 卡与实体卡的区别、支持国家、刷卡手续费与扫码消费提现路径详解 |

### 第 2 周：USDT 集群 + 卡集群扩量

| 天 | slug | 目标主词 | 标题 |
|---|---|---|---|
| 周一 | `usdt-cash-out-guide` | usdt 怎么换成人民币 | USDT 怎么换成人民币？C2C 卖币、场外换汇与提现到银行卡三条路，手续费和冻卡风险对比 |
| 周三 | `usdt-network-guide` | usdt 转账网络 | USDT 转账选哪个网络？TRC20、ERC20 与 BEP20 的手续费、到账时间和常见填错场景对比 |
| 周五 | `binance-virtual-card-guide` | 币安虚拟卡 / u 卡 | 币安虚拟卡是什么？开通条件、支持币种、消费场景、年费、提现路径与实体卡的区别一次全解析 |

### 第 3 周：卡 + 出入金

| 天 | slug | 目标主词 | 标题 |
|---|---|---|---|
| 周一 | `binance-card-eligibility-guide` | 币安卡申请条件 / 支持国家 | 币安卡哪些国家能办？大陆用户能不能申请、KYC 要求、地区限制、刷卡失败排查与替代方案全指南 |
| 周三 | `binance-withdraw-guide` | 币安提现 / 出金 | 币安怎么提现到银行卡？C2C 卖 U、链上提币与内部转账三种方式的手续费和到账时间对比 |
| 周五 | `binance-deposit-guide` | 币安充值 / 入金 | 币安怎么充值？新手 C2C 买 U、银行卡与链上转账入金的步骤、手续费和到账时间全解析 |

### 第 4 周：提现长尾 + C2C/Pay

| 天 | slug | 目标主词 | 标题 |
|---|---|---|---|
| 周一 | `binance-withdraw-to-alipay-guide` | 币安提现到支付宝 | 币安提现到支付宝怎么操作？C2C 卖 U 的到账时间、限额、冻卡风险与申诉流程避坑全攻略 |
| 周三 | `binance-c2c-guide` | 币安 c2c | 币安 C2C 怎么买币卖币？选商家、付款、防冻卡与申诉流程的完整实操与新手常见坑汇总盘点 |
| 周五 | `binance-pay-guide` | binance pay / 币安支付 | 币安 Pay 怎么用？转账、扫码消费、限额、手续费规则与和 USDT 转账的区别一次讲清 |

### 第 5 周：注册相关 + 费用

| 天 | slug | 目标主词 | 标题 |
|---|---|---|---|
| 周一 | `binance-app-download-guide` | 币安下载 / 币安 app | 币安 App 怎么下载？安卓 APK、苹果海外 Apple ID 与防山寨安装包识别教程 |
| 周三 | `binance-invite-code-guide` | 币安邀请码 | 币安邀请码怎么填？BT123 手续费返佣领取、注册后补填规则、旧码失效与真假辨别一次讲清 |
| 周五 | `binance-fee-rebate-guide` | 币安手续费 | 币安手续费怎么算？现货与合约费率、BNB 抵扣、20% 邀请码返佣叠加的实测对比与省钱顺序 |

### 第 6 周：技术与概念扩面

| 天 | slug | 目标主词 | 标题 |
|---|---|---|---|
| 周一 | `binance-api-trading-guide` | 币安 api | 币安 API 怎么开通？密钥权限设置、现货下单、风控限制与量化策略接入的新手入门教程 |
| 周三 | `metamask-guide` | metamask | MetaMask 小狐狸钱包怎么用？创建钱包、添加网络、导入助记词与防钓鱼设置完整教程 |
| 周五 | `what-is-futures-contract-guide` | 合约 | 合约交易是什么？杠杆、保证金、做多做空、强平与爆仓机制一次讲明白的新手入门指南与风险清单 |

## 五、单篇写作规格

**frontmatter**

```
title: 43–53 字，主词放前 6 字
date / lastmod: lastmod 首次发布同 date，后续只改 lastmod
description: 150–160 字，一句话说清「给谁、解决什么、含哪些信息」
slug: 定死，写之前查一遍没和现存页冲突
tags: 5–6 个（含 1 个主词、1 个同义词）
categories: 对应 hub（新手入门 / 币安 / 交易策略 / 美股代币 / 链上与DeFi / 资产安全）
```

**正文结构**（按 Bing §15/§17/§18）

1. 开头 3 行内给结论（别写背景铺垫）
2. 一张总览表（费率/门槛/到账时间/风险）
3. 分步骤或分场景展开，每节一个判断标准
4. 「常见误区」5 条以内，每条给正确做法
5. FAQ 4–6 条，问题用真实搜索句式
6. 免责声明
7. 不写代码块

**内链**（每篇 3–4 条，锚文本统一口径）

- 1 条向上：指向所属集群的枢纽页（USDT → `usdt-to-cny-guide`；币安功能 → `binance-register-guide`）
- 1–2 条横向：同集群兄弟页
- 1 条转化：`[币安注册](https://www.bsmkweb.cc/register?ref=BT123)`
- 不写裸 URL，不写「点击这里」

## 六、内链拓扑

```
usdt-to-cny-guide（枢纽）
  ├─ usdt-cash-out-guide
  ├─ usdt-network-guide
  └─ → 币安注册（转化）

binance-register-guide（枢纽）
  ├─ binance-app-download-guide
  ├─ binance-invite-code-guide
  ├─ binance-fee-rebate-guide
  ├─ binance-deposit-guide ─┬─ binance-c2c-guide
  │                         └─ binance-pay-guide
  ├─ binance-withdraw-guide ── binance-withdraw-to-alipay-guide
  └─ binance-card-guide ──┬─ binance-virtual-card-guide
                          └─ binance-card-eligibility-guide

工具页（现有 6 个）↔ 对应文章互链
```

## 七、发布与通知

- 每周一/三/五各发 1 篇，写完即 commit + push
- 部署后工作流自动跑 IndexNow（全站 sitemap）
- 新页额外在 Bing WMT 手动 URL 提交（配额 100/日），当天提交即可
- 不发草稿、不预留空 slug

## 八、监控（每周一跑一次）

```
BING_API_KEY=xxx python3 scripts/bing_report.py
```

看四个数：收录页数、展示、点击、注册词平均排名。阈值：

- 4 周：新页收录 ≥ 12；USDT 页排名进前 6
- 8 周：展示 ≥ 300/日；注册词排名进前 6
- 12 周：点击 ≥ 50/日

某篇 3 周不进前 20 → 改标题 + 补内链；进前 10 但不进前 5 → 补对比表和 FAQ。

## 九、红线（踩了会掉排名甚至被清出索引）

- 薄内容 + 注册卡的纯导流页（Bing §11 明确点名 affiliate-only）
- 一周超过 5 篇、不核对事实的批量生成（Abuse：大规模自动生成内容）
- 一页打多个主词，自己跟自己抢（旧站申请码页就吃过这个亏）
- 再改 slug（Bing §20）
- 买外链、cloaking、隐藏文字
