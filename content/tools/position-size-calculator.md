---
title: '合约仓位计算器：按风险比例反推仓位，算保证金、止损止盈与盈亏比'
date: 2026-10-14T00:00:00+08:00
lastmod: 2026-10-29T00:00:00+08:00
draft: false
description: '合约仓位计算器，输入账户资金、单笔风险比例、入场价、止损价与杠杆倍数，自动反推出该开多少仓位、所需保证金与合约张数，再结合止盈价算出潜在盈利和盈亏比，帮你按风险控制每笔仓位、避免重仓爆仓。适用于BTC、ETH等USDT本位永续合约，采用职业交易员的风险金额反推仓位逻辑，本地计算、免费在线使用、无需注册。'
slug: 'position-size-calculator'
tags: ['仓位计算器', '仓位管理', '合约', '止损止盈', '风控', '杠杆', '保证金', '盈亏比']
categories: ['交易策略']
weight: 2
icon: '⚖️'
name: '仓位计算器'
summary: '按风险比例反推仓位、保证金与止盈止损盈亏比'
faq:
  - q: '杠杆倍数会影响仓位大小吗？'
    a: '不会。仓位大小由「账户资金 × 风险比例 ÷ 止损距离」决定，和杠杆无关。杠杆只影响你需要占用多少保证金：同样的仓位，10 倍杠杆需要的保证金是 5 倍的一半。但杠杆越高，强平价越靠近入场价，止损没触发就可能先爆仓。'
  - q: '止损价该怎么设？'
    a: '止损价应该设在「这笔交易的逻辑被证明是错的」的位置，比如支撑位下方、前低附近，而不是随便一个跌幅。设好止损后，止损距离就决定了你的仓位大小——止损越近，同样风险金额下能开的仓位越大，反之越小。'
  - q: '单笔风险比例设多少合适？'
    a: '职业交易者普遍建议单笔风险控制在总资金的 1%~2%。这个数字能保证你连续亏 10 次也不伤筋动骨。新手最容易犯的错就是单笔冒 10% 以上的风险，几次止损就打回原形。'
  - q: '计算器里的「合约张数」是什么？'
    a: 'USDT 本位永续合约里，1 张合约通常代表 0.01 BTC（以 BTC-USDT 为例）。你实际下单时张数要按交易所的最小步进取整，本工具给的是理论值。'
---

> 做了交易的人都知道：止损设在哪里是技术问题，但「每笔该下多少仓」才是决定你能不能活下来的问题。仓位重了，一次止损就亏掉半个月利润；仓位轻了，看对了也赚不到钱。

这个合约仓位计算器用职业交易员的标准方法——**风险金额反推仓位**——帮你一次算清：账户资金里你愿意冒多少风险、止损距离是多少、对应该开多少仓、需要多少保证金、能下几张合约，再结合止盈价算出这笔交易的盈亏比。全程本地计算，不联网。

<div class="calc-wrap">
  <div class="calc-grid">
    <div class="calc-form">
      <div class="form-row">
        <div class="form-group">
          <label for="ps-equity">账户总资金（USDT）</label>
          <input type="number" id="ps-equity" value="10000" min="0" step="1" inputmode="decimal">
        </div>
        <div class="form-group">
          <label for="ps-risk">单笔风险比例（%）</label>
          <input type="number" id="ps-risk" value="1" min="0" step="0.1" inputmode="decimal">
          <span class="hint">建议 1%~2%，新手别超过 2%</span>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="ps-side">方向</label>
          <select id="ps-side">
            <option value="long" selected>做多</option>
            <option value="short">做空</option>
          </select>
        </div>
        <div class="form-group">
          <label for="ps-lev">杠杆倍数</label>
          <input type="number" id="ps-lev" value="10" min="1" step="1" inputmode="decimal">
          <span class="hint">只影响保证金，不影响仓位大小</span>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="ps-entry">入场价</label>
          <input type="number" id="ps-entry" value="80000" min="0" step="1" inputmode="decimal">
        </div>
        <div class="form-group">
          <label for="ps-stop">止损价</label>
          <input type="number" id="ps-stop" value="78000" min="0" step="1" inputmode="decimal">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="ps-tp">止盈价（可选）</label>
          <input type="number" id="ps-tp" value="84000" min="0" step="1" inputmode="decimal">
          <span class="hint">留空则不计算盈亏比</span>
        </div>
        <div class="form-group">
          <label for="ps-ctval">单张合约面值（BTC）</label>
          <input type="number" id="ps-ctval" value="0.01" min="0.00000001" step="0.001" inputmode="decimal">
          <span class="hint">BTC-USDT 永续通常 1 张 = 0.01 BTC</span>
        </div>
      </div>
      <div class="calc-actions">
        <button type="button" id="ps-calc" class="btn btn-primary">计算仓位</button>
        <button type="button" id="ps-reset" class="btn btn-ghost">重置</button>
      </div>
    </div>
    <div class="calc-results">
      <div class="result-grid" id="ps-results" aria-live="polite"></div>
    </div>
  </div>
</div>

<script>
(function () {
  function $(id) { return document.getElementById(id); }
  var equityEl = $('ps-equity'), riskEl = $('ps-risk'), sideEl = $('ps-side'),
      levEl = $('ps-lev'), entryEl = $('ps-entry'), stopEl = $('ps-stop'),
      tpEl = $('ps-tp'), ctvalEl = $('ps-ctval'), resultsEl = $('ps-results');

  function num(el) { var v = parseFloat(el.value); return isNaN(v) ? 0 : v; }
  function fmt(n, d) { return n.toLocaleString('en-US', { maximumFractionDigits: d === undefined ? 0 : d }); }
  function fmtUsd(n) { return '$' + fmt(n); }
  function fmtQty(n) { return n.toLocaleString('en-US', { minimumFractionDigits: 4, maximumFractionDigits: 4 }) + ' BTC'; }

  function card(label, value, cls, sub) {
    var d = document.createElement('div');
    d.className = 'stat-card';
    d.innerHTML = '<div class="stat-label">' + label + '</div>' +
      '<div class="stat-value' + (cls ? ' ' + cls : '') + '">' + value + '</div>' +
      (sub ? '<div class="stat-sub">' + sub + '</div>' : '');
    return d;
  }

  function calc() {
    var equity = num(equityEl), riskPct = num(riskEl), lev = num(levEl),
        entry = num(entryEl), stop = num(stopEl), tp = num(tpEl), ctval = num(ctvalEl);
    var side = sideEl.value;
    resultsEl.innerHTML = '';

    if (equity <= 0 || entry <= 0 || stop <= 0) {
      resultsEl.appendChild(card('提示', '请填写账户资金、入场价与止损价', '', ''));
      return;
    }

    var riskAmount = equity * riskPct / 100;
    var stopDistPrice = side === 'long' ? entry - stop : stop - entry;
    var tpPrice = 0, hasTp = false;
    if (tp > 0) {
      if (side === 'long' && tp > entry) { tpPrice = tp - entry; hasTp = true; }
      if (side === 'short' && tp < entry) { tpPrice = entry - tp; hasTp = true; }
    }

    if (stopDistPrice <= 0) {
      resultsEl.appendChild(card('提示', side === 'long' ? '做多时止损价应低于入场价' : '做空时止损价应高于入场价', '', ''));
      return;
    }

    var stopDistPct = stopDistPrice / entry * 100;
    var qty = riskAmount / stopDistPrice;                 // BTC
    var notional = qty * entry;                            // USDT
    var margin = lev > 0 ? notional / lev : 0;             // USDT
    var contracts = ctval > 0 ? qty / ctval : 0;           // 张
    var profit = hasTp ? qty * tpPrice : 0;                // USDT
    var rr = hasTp && riskAmount > 0 ? profit / riskAmount : 0;

    resultsEl.appendChild(card('风险金额', fmtUsd(riskAmount), '', '账户资金的 ' + fmt(riskPct, 1) + '%'));
    resultsEl.appendChild(card('止损距离', fmtUsd(stopDistPrice) + '（' + fmt(stopDistPct, 2) + '%）', '', '入场到止损的价格差'));
    resultsEl.appendChild(card('仓位数量', fmtQty(qty), '', '名义价值 ' + fmtUsd(notional)));
    resultsEl.appendChild(card('所需保证金', fmtUsd(margin), '', '按 ' + fmt(lev) + ' 倍杠杆'));
    resultsEl.appendChild(card('合约张数', fmt(contracts, 2) + ' 张', '', '每张 ' + fmt(ctval, 3) + ' BTC，下单需取整'));
    resultsEl.appendChild(card('潜在盈利', hasTp ? fmtUsd(profit) : '未设止盈', hasTp ? 'pos' : '', hasTp ? '价格到达止盈价时' : '填止盈价后可计算'));
    resultsEl.appendChild(card('盈亏比', hasTp ? '1 : ' + fmt(rr, 2) : '—', 'hl', hasTp ? '潜在盈利 ÷ 潜在亏损' : '潜在盈利 ÷ 风险金额'));

    if (lev > 0 && stopDistPct > 0) {
      var liqPct = 100 / lev;
      var warn = lev >= 20 ? '高杠杆下强平价距入场仅约 ' + fmt(liqPct, 1) + '%（不含维持保证金），止损可能来不及触发就先爆仓' :
        '当前 ' + fmt(lev) + ' 倍杠杆，强平价距入场约 ' + fmt(liqPct, 1) + '%，止损距离 ' + fmt(stopDistPct, 2) + '%' + (stopDistPct > liqPct ? '（止损在强平价之外，较安全）' : '（注意：止损已超出强平价，可能先被强平）');
      var w = document.createElement('div');
      w.className = 'stat-card hl';
      w.style.gridColumn = '1 / -1';
      w.innerHTML = '<div class="stat-label">风险提醒</div><div class="stat-value" style="font-size:0.95rem;font-weight:600;color:var(--ink)">' + warn + '</div>';
      resultsEl.appendChild(w);
    }
  }

  $('ps-calc').addEventListener('click', calc);
  $('ps-reset').addEventListener('click', function () {
    equityEl.value = '10000'; riskEl.value = '1'; sideEl.value = 'long';
    levEl.value = '10'; entryEl.value = '80000'; stopEl.value = '78000';
    tpEl.value = '84000'; ctvalEl.value = '0.01';
    calc();
  });

  calc();
})();
</script>

## 这个计算器怎么用

按下面四步，30 秒算完一笔合约仓位：

1. **定风险**——账户总资金填你真实的保证金账户余额，单笔风险比例默认 1%（新手建议 ≤2%）。
2. **选方向与杠杆**——做多还是做空，杠杆填你实际要用的倍数。记住：杠杆只决定保证金占用，不影响仓位大小。
3. **设价格**——入场价、止损价（必填），止盈价可选。止损设在你判断「逻辑错了」的位置。
4. **看结果**——「仓位数量」和「合约张数」就是你要下的量，「所需保证金」是你得准备的资金，「盈亏比」帮你判断这笔交易值不值得做。

> 一个反直觉但关键的结论：**同样的账户和风险比例，止损越近，能开的仓位越大；止损越远，仓位越小**。因为你的风险金额是固定的，止损距离决定了每一单位仓位在止损时亏多少。

## 核心公式：风险金额反推仓位

职业交易员下单前问的不是「我要赚多少」，而是「我这笔最多亏多少」。计算器就是按这个逻辑来的：

- **风险金额 = 账户资金 × 风险比例**（例：1 万 U 冒 1% = 100 U）
- **仓位数量 = 风险金额 ÷ 止损距离**（例：100 U ÷ 2000 点 = 0.05 BTC）
- **所需保证金 = 名义价值 ÷ 杠杆**（仓位大小和杠杆无关，只影响保证金）

这套方法的精髓是：**先锁死最大亏损，再倒推仓位**，而不是凭感觉「梭哈」或「随便买一点」。

<div class="callout callout-danger">
<div class="callout-title">⚠️ 高杠杆的陷阱</div>
<p style="margin:0">杠杆不会放大你的仓位（那是风险比例决定的），但会把<strong>强平价拉到离入场价很近</strong>的位置。如果你用了 20 倍以上杠杆，强平价可能离入场价只有几个百分点，市场稍微一抖，止损单还没成交就已经被强平了。想算具体强平价，用我们的<a href="/tools/liquidation-price-calculator/">爆仓价计算器</a>。</p>
</div>

## 相关阅读

- [合约爆仓价计算器：提前知道强平位置](/tools/liquidation-price-calculator/)
- [比特币定投计算器：回测历史定投收益](/tools/bitcoin-dca-calculator/)
- [全部在线工具](/tools/)
