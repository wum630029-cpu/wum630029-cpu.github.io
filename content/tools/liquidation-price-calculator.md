---
title: '合约爆仓价计算器：输入杠杆与仓位算强平价，提前知道爆仓位置'
date: 2026-10-14T00:00:00+08:00
lastmod: 2026-10-14T00:00:00+08:00
draft: false
description: '合约爆仓价计算器，输入方向、杠杆倍数、开仓均价、仓位数量与维持保证金率，自动算出强平价格、距强平价的距离、初始保证金与爆仓时亏损，帮你提前知道仓位会在什么价位被强平，避免杠杆过重被提前爆仓。采用逐仓模式标准公式计算，适用于BTC、ETH等USDT本位永续合约，本地计算、免费在线使用、无需注册，帮助新手做好合约风控。'
slug: 'liquidation-price-calculator'
tags: ['爆仓价计算器', '爆仓价', '强平价', '合约', '杠杆', '保证金', '风控']
categories: ['交易策略']
weight: 3
icon: '💥'
faq:
  - q: '爆仓价和强平价是一回事吗？'
    a: '是同一件事，叫法不同。强平价（Liquidation Price）是指当标记价格触及这个价位时，你的仓位保证金不足以维持仓位，会被系统强制平仓，也就是俗称的「爆仓」。本工具按逐仓（isolated）模式估算。'
  - q: '为什么计算器算的和交易所显示的不一样？'
    a: '强平价是估算值，交易所会额外计入强平手续费、资金费率，且维持保证金率随仓位档位变化。此外资金费率如果从保证金里扣除，也会让强平价向标记价靠近。所以结果当作参考，实际以交易所下单页显示为准。'
  - q: '杠杆越高，爆仓价越近吗？'
    a: '是的。逐仓模式下，10 倍杠杆的强平价距入场价约 9.5%（100÷10 再减维持保证金率），50 倍杠杆就只有约 1.5%。这就是高杠杆「一抖就爆仓」的原因。'
  - q: '全仓模式和逐仓模式的爆仓价一样吗？'
    a: '不一样。全仓模式用整个账户余额作为保证金兜底，爆仓价会远很多，但一旦爆仓是整账户归零。本工具按逐仓模式计算，更保守、也最常用。'
---

> 很多人在合约里爆仓，不是看错了方向，而是**根本不知道自己会在什么价位爆仓**。开了 20 倍杠杆，账户里还剩多少保证金能扛、价格跌到多少会被强平——脑子里是一笔糊涂账。

这个爆仓价计算器按逐仓（isolated）模式，输入你的杠杆、开仓价和仓位数量，立刻算出强平价格、距爆仓还有多远、爆仓时会亏掉多少保证金。知道自己「安全垫」有多厚，才敢说你在做风控，而不是在赌。

<div class="calc-wrap">
  <div class="calc-grid">
    <div class="calc-form">
      <div class="form-row">
        <div class="form-group">
          <label for="liq-side">方向</label>
          <select id="liq-side">
            <option value="long" selected>做多</option>
            <option value="short">做空</option>
          </select>
        </div>
        <div class="form-group">
          <label for="liq-lev">杠杆倍数</label>
          <input type="number" id="liq-lev" value="10" min="1" step="1" inputmode="decimal">
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="liq-entry">开仓均价</label>
          <input type="number" id="liq-entry" value="80000" min="0" step="1" inputmode="decimal">
        </div>
        <div class="form-group">
          <label for="liq-qty">仓位数量（BTC）</label>
          <input type="number" id="liq-qty" value="0.1" min="0" step="0.0001" inputmode="decimal">
        </div>
      </div>
      <div class="form-group">
        <label for="liq-mmr">维持保证金率（%）</label>
        <input type="number" id="liq-mmr" value="0.5" min="0" step="0.01" inputmode="decimal">
        <span class="hint">BTC 通常 0.5%，仓位越大档位越高、此值越高</span>
      </div>
      <div class="calc-actions">
        <button type="button" id="liq-calc" class="btn btn-primary">计算强平价</button>
        <button type="button" id="liq-reset" class="btn btn-ghost">重置</button>
      </div>
    </div>
    <div class="calc-results">
      <div class="result-grid" id="liq-results" aria-live="polite"></div>
    </div>
  </div>
</div>

<script>
(function () {
  function $(id) { return document.getElementById(id); }
  var sideEl = $('liq-side'), levEl = $('liq-lev'), entryEl = $('liq-entry'),
      qtyEl = $('liq-qty'), mmrEl = $('liq-mmr'), resultsEl = $('liq-results');

  function num(el) { var v = parseFloat(el.value); return isNaN(v) ? 0 : v; }
  function fmt(n, d) { return n.toLocaleString('en-US', { maximumFractionDigits: d === undefined ? 0 : d }); }
  function fmtUsd(n) { return '$' + fmt(n); }

  function card(label, value, cls, sub) {
    var d = document.createElement('div');
    d.className = 'stat-card';
    d.innerHTML = '<div class="stat-label">' + label + '</div>' +
      '<div class="stat-value' + (cls ? ' ' + cls : '') + '">' + value + '</div>' +
      (sub ? '<div class="stat-sub">' + sub + '</div>' : '');
    return d;
  }

  function calc() {
    var side = sideEl.value, lev = num(levEl), entry = num(entryEl),
        qty = num(qtyEl), mmr = num(mmrEl) / 100;
    resultsEl.innerHTML = '';

    if (entry <= 0 || qty <= 0 || lev <= 0) {
      resultsEl.appendChild(card('提示', '请填写开仓均价、仓位数量与杠杆', '', ''));
      return;
    }

    var notional = qty * entry;          // 仓位价值
    var im = notional / lev;              // 初始保证金
    var mm = notional * mmr;              // 维持保证金
    var dist = (im - mm) / qty;           // 每 BTC 的缓冲距离
    var liqPrice = side === 'long' ? entry - dist : entry + dist;
    var distPct = dist / entry * 100;
    var lossAtLiq = im;                   // 爆仓时约亏掉全部初始保证金

    resultsEl.appendChild(card('仓位名义价值', fmtUsd(notional), '', qty.toLocaleString('en-US', {maximumFractionDigits:4}) + ' BTC'));
    resultsEl.appendChild(card('初始保证金', fmtUsd(im), '', '按 ' + fmt(lev) + ' 倍杠杆'));
    resultsEl.appendChild(card('维持保证金', fmtUsd(mm), '', '维持保证金率 ' + fmt(mmr * 100, 2) + '%'));
    resultsEl.appendChild(card('强平价（爆仓价）', fmtUsd(liqPrice), 'hl', side === 'long' ? '低于此价将触发强平' : '高于此价将触发强平'));
    resultsEl.appendChild(card('距强平价', fmt(distPct, 2) + '%', distPct < 5 ? 'neg' : '', '价格再波动 ' + fmtUsd(dist) + ' 即爆仓'));
    resultsEl.appendChild(card('爆仓亏损', '约 ' + fmtUsd(lossAtLiq), 'neg', '强平时约亏掉全部初始保证金'));

    if (lev >= 20) {
      var w = document.createElement('div');
      w.className = 'stat-card hl';
      w.style.gridColumn = '1 / -1';
      w.innerHTML = '<div class="stat-label">风险提醒</div><div class="stat-value" style="font-size:0.95rem;font-weight:600;color:var(--ink)">' + fmt(lev) + ' 倍杠杆下强平价距入场仅 ' + fmt(distPct, 2) + '%，市场轻微波动就可能被强平，建议降低杠杆或设好止损。</div>';
      resultsEl.appendChild(w);
    }
  }

  $('liq-calc').addEventListener('click', calc);
  $('liq-reset').addEventListener('click', function () {
    sideEl.value = 'long'; levEl.value = '10'; entryEl.value = '80000';
    qtyEl.value = '0.1'; mmrEl.value = '0.5';
    calc();
  });

  calc();
})();
</script>

## 爆仓价是怎么算出来的

逐仓（isolated）模式下，强平价的计算逻辑很清晰：

1. **初始保证金** = 仓位价值 ÷ 杠杆（例：0.1 BTC × 8 万 ÷ 10 倍 = 800 U）
2. **维持保证金** = 仓位价值 × 维持保证金率（例：8000 × 0.5% = 40 U）
3. **缓冲金额** = 初始保证金 − 维持保证金（例：800 − 40 = 760 U，这是你能承受的最大浮亏）
4. **强平价** = 开仓价 − 缓冲金额 ÷ 仓位数量（做多：80000 − 760÷0.1 = **72400**）

换成更直观的一句话：**做多时，你的浮亏一旦超过「初始保证金减去维持保证金」，就会被强平**。杠杆越高，初始保证金越薄，缓冲越少，强平价自然越靠近开仓价。

## 一个必须记住的规律

逐仓模式下，强平价距开仓价的比例，大致等于：

- 做多：**100 ÷ 杠杆 − 维持保证金率**
- 做空：**100 ÷ 杠杆 − 维持保证金率**

也就是说：

| 杠杆 | 强平价距开仓价（约） |
| --- | --- |
| 3 倍 | 32.8% |
| 5 倍 | 19.5% |
| 10 倍 | 9.5% |
| 20 倍 | 4.5% |
| 50 倍 | 1.5% |
| 100 倍 | 0.5% |

**50 倍杠杆时，价格只要反向波动 1.5% 就爆仓**——这就是为什么高杠杆合约本质是「赌波动」，而不是「投资」。

<div class="callout callout-warning">
<div class="callout-title">⚠️ 结果仅供参考</div>
<p style="margin:0">强平价是估算值，实际会被<strong>强平手续费、资金费率、仓位档位（维持保证金率随仓位变大而升高）</strong>影响。下单前以交易所页面显示的强平价为准。想控制仓位、避免过度杠杆，先用<a href="/tools/position-size-calculator/">仓位计算器</a>按风险比例算该下多少。</p>
</div>

## 相关阅读

- [合约止盈止损设置实战](/futures-risk-management-guide/)
- [仓位计算器：按风险比例反推该开多少仓](/tools/position-size-calculator/)
- [资金管理：仓位与风险控制](/capital-management-guide/)
