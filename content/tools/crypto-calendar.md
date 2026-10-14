---
title: '加密货币项目日历：近期代币解锁与空投关键节点'
date: 2026-10-14T00:00:00+08:00
lastmod: 2026-10-14T00:00:00+08:00
draft: false
description: '加密货币项目日历，汇总近期主流代币解锁时间表与空投关键节点。代币解锁帮你提前避雷供应冲击，空投节点帮你盯紧截止时间不漏领。数据整理自 Tokenomist、RootData 与项目官方公告，按金额与时间排序，本地展示、免费在线查询、无需注册，仅供参考、不构成投资建议，帮助用户提前避雷、守住利润、少踩坑。'
slug: 'crypto-calendar'
tags: ['加密货币空投日历', '代币解锁日历', '代币解锁', '空投日历', '项目日历', '解锁时间表']
categories: ['链上与DeFi']
weight: 6
icon: '🗓️'
name: '项目日历'
summary: '查近期代币解锁与空投关键节点，提前避雷/埋伏'
faq:
  - q: '代币解锁为什么会影响价格？'
    a: '解锁意味着锁仓的筹码进入市场流通，早期投资者、团队或生态奖励拿到代币后可能卖出套现，形成抛压。解锁比例越大（尤其超过流通量 5% 甚至翻倍时），短期价格压力越明显。'
  - q: '悬崖解锁和线性解锁有什么区别？'
    a: '悬崖解锁（cliff）是一次性释放一大批，对价格冲击集中；线性解锁（linear）是每天/每周少量释放，压力更分散。日历里已经帮你标出类型。'
  - q: '看了解锁日历就能避雷吗？'
    a: '能避掉一部分。大额解锁前谨慎追高，尤其是那些解锁量占比流通量很高的项目。但解锁也可能被市场提前消化，或项目方用利好对冲，所以日历是「风险提示」而非「卖出信号」。'
  - q: '空投节点和空投查询工具有什么区别？'
    a: '空投查询工具按「参与条件/难度」帮你挑值得做的空投；这个日历只盯「时间」——什么节点该领、什么节点截止，两个配合用：先查再领、按日历盯时间。'
---

> 币圈每天都在发生两件影响你钱包的事：代币解锁砸盘，空投截止漏领。这个日历把两者排在一张时间表里——解锁前别追高，空投截止前别漏领。

数据整理自 Tokenomist、RootData、币安公告与项目官方，截至 2026 年 10 月 14 日。**具体解锁时间与金额以链上/官方为准**，本日历用于提前预警、快速筛选。

<div class="db-tabs" id="cal-tabs" role="tablist">
  <button type="button" class="db-tab active" data-tab="unlock">代币解锁</button>
  <button type="button" class="db-tab" data-tab="airdrop">空投节点</button>
</div>

<div class="db-count" id="cal-count"></div>
<div class="db-list" id="cal-list" aria-live="polite"></div>
<p class="db-note">※ 数据整理自 Tokenomist / WuBlockchain、RootData、币安公告与项目官方，截至 2026-10-14。解锁时间与金额随时可能调整，请以链上和官方公告为准，本日历仅供参考、不构成投资建议。</p>

<script>
(function () {
  var UNLOCKS = [
    { token: 'RAIN', amt: 404.6, unit: '亿', pct: '5.74%', type: '线性', time: '10 月', warn: false },
    { token: 'HYPE', amt: 331.69, unit: '亿', pct: '0.88%', type: '悬崖', time: '10 月', warn: false },
    { token: 'SOL', amt: 232, unit: '亿', pct: '0.33%', type: '线性', time: '10 月', warn: false },
    { token: 'CC', amt: 101.64, unit: '亿', pct: '2.14%', type: '线性', time: '10 月', warn: false },
    { token: 'BTW', amt: 100.8, unit: '亿', pct: '1%', type: '悬崖', time: '10 月', warn: false },
    { token: 'ZEC', amt: 64.62, unit: '亿', pct: '0.29%', type: '线性', time: '10 月', warn: false },
    { token: 'TRUMP', amt: 58.86, unit: '亿', pct: '9.94%', type: '线性', time: '10 月', warn: true },
    { token: 'WLD', amt: 50.91, unit: '亿', pct: '2.37%', type: '线性', time: '10 月', warn: false },
    { token: 'ENA', amt: 49.46, unit: '亿', pct: '2.32%', type: '悬崖', time: '10-05', warn: false, note: '投资者份额加速一次性释放' },
    { token: 'ZRO', amt: 44.99, unit: '亿', pct: '4.04%', type: '悬崖', time: '10 月', warn: false },
    { token: 'ASTER', amt: 39.89, unit: '亿', pct: '2.06%', type: '线性', time: '10 月', warn: false },
    { token: 'PUMP', amt: 38.73, unit: '亿', pct: '1.51%', type: '线性', time: '10 月', warn: false },
    { token: 'AVAX', amt: 33.85, unit: '亿', pct: '0.70%', type: '线性', time: '10 月', warn: false },
    { token: 'TAO', amt: 32.63, unit: '亿', pct: '0.98%', type: '线性', time: '10 月', warn: false },
    { token: 'MORPHO', amt: 29.93, unit: '亿', pct: '1.66%', type: '线性', time: '10 月', warn: false },
    { token: 'NEAR', amt: 27.03, unit: '亿', pct: '0.44%', type: '线性', time: '10 月', warn: false },
    { token: 'SUI', amt: 24.74, unit: '亿', pct: '0.52%', type: '悬崖', time: '10 月', warn: false },
    { token: 'STABLE', amt: 24.48, unit: '亿', pct: '3.37%', type: '线性', time: '10 月', warn: false },
    { token: 'FF', amt: 24.47, unit: '亿', pct: '6.62%', type: '悬崖', time: '10 月', warn: true },
    { token: 'XPL', amt: 21.33, unit: '亿', pct: '5.02%', type: '悬崖', time: '10 月', warn: true },
    { token: 'ARB', amt: 21.25, unit: '亿', pct: '1.81%', type: '悬崖', time: '10 月', warn: false },
    { token: 'APR', amt: 20.22, unit: '亿', pct: '46.67%', type: '悬崖', time: '10 月', warn: true, note: '释放量接近流通量一半，警惕稀释' },
    { token: 'H (Humanity)', amt: 18.69, unit: '亿', pct: '6.84%', type: '悬崖', time: '10 月', warn: true },
    { token: 'CARDS', amt: 16.54, unit: '亿', pct: '9.60%', type: '悬崖', time: '10 月', warn: true },
    { token: 'CONX', amt: 13.48, unit: '亿', pct: '1.39%', type: '悬崖', time: '10 月', warn: false },
    { token: 'DBR', amt: 11.8, unit: '亿', pct: '10.25%', type: '悬崖', time: '10 月', warn: true },
    { token: 'ALLO', amt: 1.6, unit: '亿', pct: '约 64% 流通', type: '首次解锁', time: '11 月', warn: true, note: '首次内部解锁约 1.6 亿枚，占当时流通约 64%' },
    { token: 'HUMA', amt: 4.6, unit: '亿', pct: '约 4.6%', type: '首次解锁', time: '11-26', warn: true, note: '首次内部解锁推迟至 11-26，约 4.59 亿枚' },
    { token: 'KAITO', amt: 0.0368, unit: '亿', pct: '—', type: '悬崖', time: '10-20', warn: false, note: '约 368 万美元' },
    { token: 'NIGHT', amt: 0.043, unit: '亿', pct: '—', type: '悬崖', time: '10-09 / 11-09', warn: false, note: 'Midnight，每月约 430 万美元' }
  ];

  var AIRDROPS = [
    { name: '币安 USD1 空投', date: '10-02 ~ 10-30', status: '进行中', note: '持有 USD1 瓜分 1.5 亿 WLFI + 250 万 USD1' },
    { name: 'Concrete (CT) PoolX', date: '10-04 ~ 10-12', status: '已结束', note: 'Bitget 锁仓 BTC 瓜分 111 万 CT' },
    { name: 'Pheasant (PNT) 领取', date: '10-06 起 21 天', status: '进行中', note: '按 09-08 快照活跃度领取' },
    { name: 'Sonic (S) 领取截止', date: '10-15', status: '截止', note: '截止后未领 3269 万 S 销毁' },
    { name: 'Meteora LP 激励 S2', date: '10-21', status: '截止', note: '领取窗口关闭' },
    { name: 'Pharos (PROS) 领取截止', date: '10-25', status: '截止', note: '测试网 / 质押 / OKX 钱包用户' },
    { name: 'Grass 第二阶段', date: '至 2027-01-22', status: '进行中', note: '带宽分享者发 USDC 奖励' }
  ];

  var listEl = document.getElementById('cal-list');
  var countEl = document.getElementById('cal-count');
  var cur = 'unlock';

  function tag(text, cls) { return '<span class="tag' + (cls ? ' ' + cls : '') + '">' + text + '</span>'; }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function renderUnlock() {
    var sorted = UNLOCKS.slice().sort(function (a, b) { return b.amt - a.amt; });
    countEl.textContent = '共 ' + sorted.length + ' 个解锁节点，按金额从大到小排序';
    listEl.innerHTML = '';
    sorted.forEach(function (u) {
      var card = document.createElement('div');
      card.className = 'db-card';
      card.innerHTML =
        '<div class="db-card-head">' +
          '<span class="db-card-title">' + esc(u.token) + '</span>' +
          '<span class="db-card-tags">' + tag(u.type) + tag(u.time) + (u.warn ? tag('⚠ 高稀释', 'tag-red') : '') + '</span>' +
        '</div>' +
        '<div class="db-meta" style="margin-top:0;margin-bottom:6px">' +
          '<span>💰 解锁金额 <b>' + esc(u.amt + ' ' + u.unit) + ' 美元</b></span>' +
          '<span>📊 占流通/供应 <b>' + esc(u.pct) + '</b></span>' +
        '</div>' +
        (u.note ? '<div class="db-card-desc">' + esc(u.note) + '</div>' : '');
      listEl.appendChild(card);
    });
  }

  function renderAirdrop() {
    countEl.textContent = '共 ' + AIRDROPS.length + ' 个空投关键节点';
    listEl.innerHTML = '';
    AIRDROPS.forEach(function (a) {
      var st = a.status === '进行中' ? tag('进行中', 'tag-green') : a.status === '截止' ? tag('截止', 'tag-gold') : tag('已结束');
      var card = document.createElement('div');
      card.className = 'db-card';
      card.innerHTML =
        '<div class="db-card-head">' +
          '<span class="db-card-title">' + esc(a.name) + '</span>' +
          '<span class="db-card-tags">' + st + '</span>' +
        '</div>' +
        '<div class="db-meta" style="margin-top:0;margin-bottom:6px"><span>⏱ 时间 <b>' + esc(a.date) + '</b></span></div>' +
        '<div class="db-card-desc">' + esc(a.note) + '</div>';
      listEl.appendChild(card);
    });
  }

  function refresh() {
    if (cur === 'unlock') renderUnlock(); else renderAirdrop();
  }

  document.getElementById('cal-tabs').addEventListener('click', function (e) {
    var btn = e.target.closest('.db-tab');
    if (!btn) return;
    cur = btn.getAttribute('data-tab');
    document.querySelectorAll('.db-tab').forEach(function (b) { b.classList.toggle('active', b === btn); });
    refresh();
  });

  refresh();
})();
</script>

## 这个项目日历怎么用

- **代币解锁**：按金额从大到小排列。看到自己持有的币出现在靠前位置，先看「占流通比例」——超过 5% 甚至翻倍的（标了 ⚠ 高稀释），解锁前要警惕抛压，谨慎追高。
- **空投节点**：按时间排。标「截止」的是即将关闭领取窗口的，别漏领；标「进行中」的可以到[空投查询工具](/tools/airdrop-checker/)看参与条件。

## 大额解锁为什么是风险信号

解锁不直接等于下跌，但它是最常见的短期利空之一：

- **筹码从锁定变流通**：早期投资人、团队、生态基金拿到币后可能卖出。
- **占比决定冲击大小**：解锁量占流通量 1% 以内影响有限；像 APR（约 46.67%）、ALLO（约 64%）、MON（曾列超 140%）这种，本质是流通盘成倍放大，冲击要重视。
- **悬崖 vs 线性**：一次性悬崖解锁集中在一天，冲击更猛；线性解锁分散，压力平滑。

> 实操建议：日历里标了 ⚠ 高稀释的项目，解锁日前后**别加杠杆追多**；已经在持仓的，提前评估自己的成本和退出位置。

## 空投节点别漏领

空投领取几乎都有截止时间，过了就作废甚至销毁：

- **Sonic**：10-15 截止，未领的 3269 万 S 将被销毁。
- **Pharos**：10-25 截止，测试网/质押/OKX 钱包用户要抓紧。
- **币安 USD1**：10-30 结束，持币即可参与，[币安注册](/binance-register-guide/)后（BT123）在 App 内完成。

要盯更多空投的参与条件，用[空投查询工具](/tools/airdrop-checker/)配合日历，先查再领。

## 相关阅读

- [空投查询工具：查进行中空投](/tools/airdrop-checker/)
- [链上交互成本计算器](/tools/gas-cost-calculator/)
- [稳定币脱锚风险与应对](/stablecoin-depeg-risk-guide/)
