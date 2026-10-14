---
title: '比特币定投计算器：回测真实历史价格，算清每月定投收益与一次性买入对比'
date: 2026-10-14T00:00:00+08:00
lastmod: 2026-10-14T00:00:00+08:00
draft: false
description: '比特币定投计算器，用2017年至今真实历史月度价格回测每月定投收益。输入定投金额、起止时间与手续费率，自动算出总投入、累计买入的比特币数量、当前市值、总收益率与平均成本价，并和一次性买入做对比，直观看到定投摊平成本的效果。数据取自交易所公开行情，全程本地计算，帮助新手判断定投是否适合自己，免费在线使用，无需注册。'
slug: 'bitcoin-dca-calculator'
tags: ['定投计算器', '定投', '比特币', 'DCA', '定投回测', '投资收益', '计算器']
categories: ['交易策略']
weight: 1
icon: '📈'
name: '定投计算器'
summary: '用真实历史价格回测每月定投收益，对比一次性买入'
faq:
  - q: '这个定投计算器用的是什么价格数据？'
    a: '用的是比特币 2017 年 8 月至 2026 年 10 月的真实月度收盘价（来自交易所公开行情）。每月定投假设在当月收盘价买入，因此回测结果反映的是真实历史走势，不是拍脑袋假设。'
  - q: '定投和一次性买入，到底哪个收益更高？'
    a: '长期看两者没有绝对优劣：市场单边上涨时一次性买入更优（本金更早进场），震荡或先跌后涨时定投更优（摊低平均成本）。计算器里的「对比一次性买入」会直接用你的参数算出两者差距，你一试便知。'
  - q: '手续费率该怎么填？'
    a: '现货买入手续费一般约 0.1%。如果你通过邀请码注册（币安 BT123 享 20% 手续费返佣），实际成本会更低。手续费率填 0 就是不计手续费的理论值。'
  - q: '历史回测能代表未来收益吗？'
    a: '不能。历史回测只说明「过去这么定投会发生什么」，未来涨跌无法预测。本工具用于理解定投机制、辅助决策，不构成投资建议。'
---

> 定投到底能不能赚钱？网上说「每月买 100 美元比特币，几年后翻几十倍」的帖子很多，但没人给你一个能自己改参数、用真实价格算一遍的工具。

这个定投计算器用 **2017 年至今的真实比特币月度价格**做回测——你输入每月投多少钱、从哪年开始投、投到哪年，它立刻算出你的总投入、累计买了多少比特币、现在值多少钱、赚了多少，还顺手和「一开始就全仓买入」对比一次。所有计算都在本地浏览器完成，不联网、不收集任何数据。

<div class="calc-wrap">
  <div class="calc-grid">
    <div class="calc-form">
      <div class="form-group">
        <label for="dca-amount">每月定投金额（美元）</label>
        <input type="number" id="dca-amount" value="100" min="1" step="1" inputmode="numeric">
        <span class="hint">100 美元 ≈ 720 人民币（按 1:7.2 估算）</span>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="dca-start">开始时间</label>
          <select id="dca-start"></select>
        </div>
        <div class="form-group">
          <label for="dca-end">结束时间</label>
          <select id="dca-end"></select>
        </div>
      </div>
      <div class="form-group">
        <label for="dca-fee">单次买入手续费率（%）</label>
        <input type="number" id="dca-fee" value="0.1" min="0" step="0.01" inputmode="decimal">
        <span class="hint">现货买入手续费约 0.1%，用邀请码注册可享返佣抵扣</span>
      </div>
      <div class="calc-actions">
        <button type="button" id="dca-calc" class="btn btn-primary">计算收益</button>
        <button type="button" id="dca-reset" class="btn btn-ghost">重置</button>
      </div>
    </div>
    <div class="calc-results">
      <div class="result-grid" id="dca-results" aria-live="polite"></div>
    </div>
  </div>
  <div class="calc-chart">
    <div class="chart-legend">
      <span><i class="legend-dot" style="background:var(--gold)"></i>组合市值</span>
      <span><i class="legend-dot" style="background:var(--muted)"></i>累计投入</span>
    </div>
    <svg id="dca-chart" viewBox="0 0 720 240" role="img" aria-label="定投累计投入与组合市值曲线"></svg>
  </div>
</div>

<script>
(function () {
  var BTC_MONTHLY = [
  [2017,8,4724.89],
  [2017,9,4378.51],
  [2017,10,6463.0],
  [2017,11,9838.96],
  [2017,12,13716.36],
  [2018,1,10285.1],
  [2018,2,10326.76],
  [2018,3,6923.91],
  [2018,4,9246.01],
  [2018,5,7485.01],
  [2018,6,6390.07],
  [2018,7,7730.93],
  [2018,8,7011.21],
  [2018,9,6626.57],
  [2018,10,6371.93],
  [2018,11,4041.32],
  [2018,12,3702.9],
  [2019,1,3434.1],
  [2019,2,3813.69],
  [2019,3,4103.95],
  [2019,4,5320.81],
  [2019,5,8555.0],
  [2019,6,10854.1],
  [2019,7,10080.53],
  [2019,8,9587.47],
  [2019,9,8289.34],
  [2019,10,9140.85],
  [2019,11,7541.89],
  [2019,12,7195.23],
  [2020,1,9352.89],
  [2020,2,8523.61],
  [2020,3,6410.44],
  [2020,4,8620.0],
  [2020,5,9448.27],
  [2020,6,9138.55],
  [2020,7,11335.46],
  [2020,8,11649.51],
  [2020,9,10776.59],
  [2020,10,13791.0],
  [2020,11,19695.87],
  [2020,12,28923.63],
  [2021,1,33092.98],
  [2021,2,45135.66],
  [2021,3,58740.55],
  [2021,4,57694.27],
  [2021,5,37253.81],
  [2021,6,35045.0],
  [2021,7,41461.83],
  [2021,8,47100.89],
  [2021,9,43824.1],
  [2021,10,61299.8],
  [2021,11,56950.56],
  [2021,12,46216.93],
  [2022,1,38466.9],
  [2022,2,43160.0],
  [2022,3,45510.34],
  [2022,4,37630.8],
  [2022,5,31801.04],
  [2022,6,19942.21],
  [2022,7,23293.32],
  [2022,8,20050.02],
  [2022,9,19422.61],
  [2022,10,20490.74],
  [2022,11,17163.64],
  [2022,12,16542.4],
  [2023,1,23125.13],
  [2023,2,23141.57],
  [2023,3,28465.36],
  [2023,4,29233.21],
  [2023,5,27210.35],
  [2023,6,30472.0],
  [2023,7,29232.25],
  [2023,8,25940.78],
  [2023,9,26962.56],
  [2023,10,34639.77],
  [2023,11,37723.96],
  [2023,12,42283.58],
  [2024,1,42580.0],
  [2024,2,61130.98],
  [2024,3,71280.01],
  [2024,4,60672.0],
  [2024,5,67540.01],
  [2024,6,62772.01],
  [2024,7,64628.0],
  [2024,8,58973.99],
  [2024,9,63327.59],
  [2024,10,70292.01],
  [2024,11,96407.99],
  [2024,12,93576.0],
  [2025,1,102429.56],
  [2025,2,84349.94],
  [2025,3,82550.01],
  [2025,4,94172.0],
  [2025,5,104591.88],
  [2025,6,107146.5],
  [2025,7,115764.08],
  [2025,8,108246.35],
  [2025,9,114048.93],
  [2025,10,109608.01],
  [2025,11,90360.0],
  [2025,12,87648.22],
  [2026,1,78741.09],
  [2026,2,66973.26],
  [2026,3,68284.48],
  [2026,4,76346.57],
  [2026,5,73674.39],
  [2026,6,58624.71],
  [2026,7,62887.88],
  [2026,8,78581.29],
  [2026,9,83623.6],
  [2026,10,83543.25]
  ];

  var startSel = document.getElementById('dca-start');
  var endSel = document.getElementById('dca-end');
  var amountEl = document.getElementById('dca-amount');
  var feeEl = document.getElementById('dca-fee');
  var resultsEl = document.getElementById('dca-results');
  var chartEl = document.getElementById('dca-chart');

  BTC_MONTHLY.forEach(function (m, i) {
    var label = m[0] + '年' + m[1] + '月';
    startSel.appendChild(new Option(label, String(i)));
    endSel.appendChild(new Option(label, String(i)));
  });
  startSel.value = '0';
  endSel.value = String(BTC_MONTHLY.length - 1);

  function fmtUSD(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }
  function fmtBTC(n) {
    return n.toLocaleString('en-US', { minimumFractionDigits: 4, maximumFractionDigits: 4 }) + ' BTC';
  }
  function fmtPrice(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }
  function fmtPct(n) {
    return (n >= 0 ? '+' : '') + n.toFixed(1) + '%';
  }

  function card(label, value, cls, sub) {
    var d = document.createElement('div');
    d.className = 'stat-card';
    d.innerHTML = '<div class="stat-label">' + label + '</div>' +
      '<div class="stat-value' + (cls ? ' ' + cls : '') + '">' + value + '</div>' +
      (sub ? '<div class="stat-sub">' + sub + '</div>' : '');
    return d;
  }

  function calc() {
    var amount = parseFloat(amountEl.value);
    var feePct = parseFloat(feeEl.value);
    if (isNaN(amount)) amount = 0;
    if (isNaN(feePct)) feePct = 0;

    var si = parseInt(startSel.value, 10);
    var ei = parseInt(endSel.value, 10);
    if (si > ei) {
      var t = si; si = ei; ei = t;
      startSel.value = String(si);
      endSel.value = String(ei);
    }

    resultsEl.innerHTML = '';

    if (amount <= 0) {
      resultsEl.appendChild(card('提示', '请输入大于 0 的定投金额', '', ''));
      chartEl.innerHTML = '';
      return;
    }

    var btc = 0, invested = 0;
    var pv = [], pc = [];
    var i;
    for (i = si; i <= ei; i++) {
      var price = BTC_MONTHLY[i][2];
      btc += amount * (1 - feePct / 100) / price;
      invested += amount;
      pv.push(btc * price);
      pc.push(invested);
    }

    var latestPrice = BTC_MONTHLY[ei][2];
    var value = btc * latestPrice;
    var profit = value - invested;
    var roi = invested > 0 ? profit / invested * 100 : 0;
    var avgCost = btc > 0 ? invested / btc : 0;

    var startPrice = BTC_MONTHLY[si][2];
    var lumpBtc = invested * (1 - feePct / 100) / startPrice;
    var lumpValue = lumpBtc * latestPrice;
    var diff = value - lumpValue;

    resultsEl.appendChild(card('总投入', fmtUSD(invested), '', '共 ' + (ei - si + 1) + ' 个月'));
    resultsEl.appendChild(card('累计买入', fmtBTC(btc), '', '平均成本 ' + fmtPrice(avgCost)));
    resultsEl.appendChild(card('当前市值', fmtUSD(value), '', '现价 ' + fmtPrice(latestPrice)));
    resultsEl.appendChild(card('总收益', fmtUSD(profit) + '（' + fmtPct(roi) + '）', profit >= 0 ? 'pos' : 'neg', ''));
    resultsEl.appendChild(card('平均成本价', fmtPrice(avgCost), '', '现价 ' + fmtPrice(latestPrice)));
    resultsEl.appendChild(card('对比一次性买入', (diff >= 0 ? '定投多赚 ' : '一次性多赚 ') + fmtUSD(Math.abs(diff)), 'hl',
      '同样金额在开始月一次买入，当前价值 ' + fmtUSD(lumpValue)));

    drawChart(pv, pc, si, ei);
  }

  function drawChart(pv, pc, si, ei) {
    var W = 720, H = 240, padT = 14, padB = 18, padL = 6, padR = 6;
    var n = pv.length;
    var maxV = 1;
    var i;
    for (i = 0; i < n; i++) {
      if (pv[i] > maxV) maxV = pv[i];
      if (pc[i] > maxV) maxV = pc[i];
    }
    function x(i) { return n <= 1 ? W / 2 : padL + (W - padL - padR) * i / (n - 1); }
    function y(v) { return padT + (H - padT - padB) * (1 - v / maxV); }

    var grid = '';
    var g;
    for (g = 0; g <= 4; g++) {
      var gy = padT + (H - padT - padB) * g / 4;
      grid += '<line x1="' + padL + '" y1="' + gy + '" x2="' + (W - padR) + '" y2="' + gy + '" stroke="var(--border)" stroke-width="1"/>';
    }

    var valPath = '', costPath = '', areaPath = '';
    for (i = 0; i < n; i++) {
      var cx = x(i), cy = y(pv[i]);
      valPath += (i === 0 ? 'M' : 'L') + cx.toFixed(1) + ' ' + cy.toFixed(1);
      var cyc = y(pc[i]);
      costPath += (i === 0 ? 'M' : 'L') + cx.toFixed(1) + ' ' + cyc.toFixed(1);
      areaPath += (i === 0 ? 'M' : 'L') + cx.toFixed(1) + ' ' + cy.toFixed(1);
    }
    if (n > 0) {
      areaPath += 'L' + x(n - 1).toFixed(1) + ' ' + (H - padB) + 'L' + x(0).toFixed(1) + ' ' + (H - padB) + 'Z';
    }

    var label = '<text x="' + padL + '" y="12" font-size="12" fill="var(--faint)">' +
      BTC_MONTHLY[si][0] + '年' + BTC_MONTHLY[si][1] + '月 起 · ' + BTC_MONTHLY[ei][0] + '年' + BTC_MONTHLY[ei][1] + '月 止</text>';

    chartEl.innerHTML = grid +
      '<path d="' + areaPath + '" fill="var(--gold)" opacity="0.10"/>' +
      '<path d="' + costPath + '" fill="none" stroke="var(--muted)" stroke-width="2" stroke-dasharray="5 5"/>' +
      '<path d="' + valPath + '" fill="none" stroke="var(--gold)" stroke-width="2.5"/>' +
      label;
  }

  document.getElementById('dca-calc').addEventListener('click', calc);
  document.getElementById('dca-reset').addEventListener('click', function () {
    amountEl.value = '100';
    feeEl.value = '0.1';
    startSel.value = '0';
    endSel.value = String(BTC_MONTHLY.length - 1);
    calc();
  });

  calc();
})();
</script>

## 怎么用这个定投计算器

三步就能算完：

1. **填金额**——每月计划投多少美元，默认 100 美元（约 720 人民币）。
2. **选区间**——开始时间默认 2017 年 8 月（数据最早），结束时间默认现在。你可以只回测某一段，比如「2021 年高点开始定投到现在」，看看追高买入的后果。
3. **看结果**——上面 6 张卡片会告诉你：一共投了多少钱、买到了多少比特币、现在值多少、赚了多少、平均成本是多少，以及和一次性买入的差距。

> 想自己动手验证一个常见说法，可以试试：把开始时间选到 **2021 年 1 月**（牛市顶部附近）开始定投，看看后面两年熊市里账户是什么状态——这正是定投「摊平成本」机制最直观的演示。

## 定投 vs 一次性买入：哪个更划算

这是新手问得最多的问题，结论没有绝对答案，取决于你选的那段行情：

- **单边上涨行情**（比如 2020 年下半年到 2021 年初）：一次性买入更优，因为本金更早进场、吃到全程涨幅。
- **先跌后涨或震荡行情**（比如 2021 年底到 2023 年）：定投更优，因为你在低位买到了更多筹码，摊低了平均成本。

你可以用上面的计算器，把同一笔钱分别按「每月定投」和「一次性买入」两种方式回测，直接看数字说话——这比任何口头结论都有说服力。

## 计算结果里的指标是什么意思

- **总投入**：累计投进去的本金，不含手续费。
- **累计买入**：用「每月金额 ÷ 当月价格」累加得到的比特币数量（已扣手续费）。
- **当前市值**：累计比特币 × 结束月的价格，也就是你现在全部卖出能拿回的钱。
- **总收益**：市值减投入，正值是赚、负值是亏；括号里是收益率。
- **平均成本价**：总投入 ÷ 累计比特币，低于当前价就是浮盈，高于就是浮亏。
- **对比一次性买入**：假设你把同样的总本金在开始月一次性买入，算到现在的市值，和定投比谁高。

## 相关阅读

- [DCA 定投策略全攻略：用币安实现加密货币自动定投](/binance-dca-guide/)
- [币安定投进阶玩法](/binance-dca-advanced-guide/)
- [仓位计算器实战：每笔该下多少钱](/position-sizing-calculator-guide/)
