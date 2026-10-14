---
title: '空投查询工具：查进行中空投的参与条件、截止时间与难度'
date: 2026-10-14T00:00:00+08:00
lastmod: 2026-10-14T00:00:00+08:00
draft: false
description: '空投查询工具，汇总进行中与历史主流空投的参与条件、截止时间、难度与预计价值，支持按状态和类型筛选、关键词搜索，快速判断还能领哪些空投、自己有没有漏领。数据整理自币安公告与项目官方等公开渠道，参与前务必到官方认领页核实，谨防钓鱼链接与假代币，免费在线使用、无需注册，先查再领、别为无价值的空投白花 Gas。'
slug: 'airdrop-checker'
tags: ['空投查询', '空投查询工具', '钱包空投检查', '空投', '领空投', '空投日历']
categories: ['链上与DeFi']
weight: 4
icon: '🪂'
name: '空投查询'
summary: '查进行中/历史空投的参与条件、截止时间与难度'
faq:
  - q: '这个空投查询工具的数据从哪来？'
    a: '整理自币安公告、项目官方与 RootData/Tokenomist 等公开渠道，截至 2026 年 10 月。空投信息变化快，截止时间与参与条件请以项目官方渠道为准，本工具用于快速筛选、缩小范围。'
  - q: '怎么判断一个空投值不值得做？'
    a: '看三个指标：难度（参与成本高不高）、预计价值（奖池和单人预期）、截止时间（还来不来得及）。核心公式是「预期收益 = 获奖概率 × 预估代币价值 − 交互成本」，成本大于预期收益的「牛马任务」直接跳过。'
  - q: '历史空投列出来有什么用？'
    a: '两个用处：一是帮你复盘自己错过的机会、理解主流的参与条件；二是这些条件基本就是未来空投的模板——早期用过产品、持有域名、做过跨链和治理，几乎每个大空投都逃不出这几类。'
  - q: '空投代币要交税吗？'
    a: '多数地区把领到空投视为应税收入，卖出产生的差价另有资本利得税。不同国家规则不同，建议咨询税务专业人士，本工具不提供税务建议。'
---

> 空投一年几百个，但真正值得动手的没几个。这个工具帮你把「进行中」和「历史大空投」摆在一起：按状态、类型筛选，搜关键词，一眼看清每个空投的参与条件、截止时间、难度和大概价值——再决定要不要花 Gas 和时间去折腾。

所有数据整理自公开公告，**参与前务必到项目官方渠道二次核实**，只从官方认领页领取，任何让你「转账解锁」或「输入助记词」的都是钓鱼。

<div class="db-toolbar">
  <input type="search" id="ad-search" class="db-search" placeholder="搜索空投名称 / 项目 / 关键词…" aria-label="搜索空投">
  <div class="db-filters" id="ad-status-filters">
    <span class="filter-label">按状态</span>
  </div>
  <div class="db-filters" id="ad-type-filters">
    <span class="filter-label">按类型</span>
  </div>
</div>

<div class="db-count" id="ad-count"></div>
<div class="db-list" id="ad-list" aria-live="polite"></div>
<p class="db-note">※ 数据整理自公开公告，截至 2026 年 10 月 14 日。空投的截止时间、参与条件与奖池随时可能调整，请以项目官方渠道为准；仅从官方认领页操作，谨防钓鱼链接与假代币。</p>

<script>
(function () {
  var AIRDROPS = [
    { name: '币安 USD1 空投', chain: '币安 CEX', status: '进行中', type: '持币', diff: '低',
      deadline: '2026-10-30', value: '1.5 亿 WLFI + 250 万 USD1',
      desc: '在币安现货/资金/杠杆/合约账户持有稳定币 USD1 即可参与，按持仓量瓜分奖池。',
      points: ['持有 USD1（现货或资金账户即可）', '放合约/杠杆账户享 1.2 倍奖励加成', '借币买入 USD1 按 7 折计算持仓'],
      link: '币安 App 内参与（以官方公告为准）' },
    { name: 'Sonic (S) 最后领取', chain: 'Sonic', status: '进行中', type: '交互', diff: '低',
      deadline: '2026-10-15', value: '未领的 3269 万 S 将销毁',
      desc: '2024/2025 年在 Sonic 活跃过的地址可领取空投，截止后未领取代币将被销毁。',
      points: ['2024 或 2025 年在 Sonic 链上活跃', '截止 10-15 前完成领取'],
      link: 'my.soniclabs.com/airdrop' },
    { name: 'Pharos (PROS) 领取', chain: 'Pharos', status: '进行中', type: '交互', diff: '低',
      deadline: '2026-10-25', value: '多组合格条件',
      desc: '测试网参与者、Stake Before the Stake 贡献者、Discord 角色与 OKX 钱包活动用户可领。',
      points: ['测试网参与 / 质押贡献 / Discord 角色', 'OKX 钱包活动用户'],
      link: 'claim.pharos.xyz' },
    { name: 'Pheasant Network (PNT)', chain: 'Pheasant', status: '进行中', type: '交互', diff: '低',
      deadline: '10-06 起 21 天', value: '按快照活跃度',
      desc: 'Season 1 领取，按 2026-09-08 快照的综合生态活跃度分配。',
      points: ['2026-09-08 快照前有生态交互'],
      link: 'home.pheasant.network' },
    { name: 'Meteora LP 激励 S2', chain: 'Solana', status: '进行中', type: '流动性', diff: '中',
      deadline: '2026-10-21', value: '按积分/门槛',
      desc: '流动性激励 Season 2 领取，需达到最低积分与代币门槛。',
      points: ['满足最低积分门槛', '满足最低代币持仓门槛'],
      link: '官方渠道领取' },
    { name: 'Grass 第二阶段奖励', chain: 'Grass / Solana', status: '进行中', type: '带宽', diff: '低',
      deadline: '2027-01-22', value: 'USDC 奖励',
      desc: '共享过带宽（Epoch）的用户按阶段发放 USDC 奖励。',
      points: ['曾通过 Grass 共享带宽'],
      link: '官方 App 领取' },
    { name: 'Concrete (CT) PoolX', chain: 'Bitget / 币安 Alpha', status: '已结束', type: '质押', diff: '中',
      deadline: '2026-10-12', value: '111 万 CT 池',
      desc: 'Bitget PoolX 锁仓 BTC 瓜分 CT 空投，另有币安 Alpha 积分领取通道。',
      points: ['锁仓 BTC（0.0001~50 BTC）', '或持有 ≥223 币安 Alpha 积分'],
      link: '已结束，仅供复盘' },
    { name: 'Uniswap (UNI)', chain: 'Ethereum', status: '已结束', type: '交互', diff: '低',
      deadline: '2020-09', value: '早期每人 400 UNI',
      desc: '在快照前于 Uniswap 上 swap 过一次即可，是最简单的空投模板。',
      points: ['快照前在 Uniswap 交易过'],
      link: '历史参考' },
    { name: 'ENS', chain: 'Ethereum', status: '已结束', type: '持币', diff: '低',
      deadline: '2021-11', value: '约 500~8000 美元',
      desc: '持有 .eth 域名的用户获得治理代币，按持有域名数量分配。',
      points: ['注册并持有 .eth 域名'],
      link: '历史参考' },
    { name: 'Optimism (OP)', chain: 'Optimism', status: '已结束', type: '交互', diff: '中',
      deadline: '2022 起多轮', value: '中位约 1100 美元',
      desc: '用过 Optimism 桥和 DeFi、参与过 Gitcoin 捐赠或治理的用户，多轮分发。',
      points: ['使用 Optimism 桥', '在 Optimism 上用 DeFi / 治理'],
      link: '历史参考' },
    { name: 'Arbitrum (ARB)', chain: 'Arbitrum', status: '已结束', type: '交互', diff: '中',
      deadline: '2023-03', value: '约 800~1400 美元',
      desc: '在 Arbitrum 上桥接、兑换、提供流动性，按多因子打分，是最大 L2 空投。',
      points: ['桥接资产到 Arbitrum', '兑换 / 提供流动性 / 治理投票'],
      link: '历史参考' },
    { name: 'Starknet (STRK)', chain: 'Starknet', status: '已结束', type: '交互', diff: '中',
      deadline: '2024-02', value: '约 300~5000 美元',
      desc: '与 Starknet 应用交互、使用官方桥，早期社区与开源贡献者额外分配。',
      points: ['使用 Starknet 官方桥', '与 Starknet 应用交互'],
      link: '历史参考' }
  ];

  var STATUS = ['全部', '进行中', '已结束'];
  var TYPES = ['全部', '交互', '持币', '流动性', '质押', '带宽'];
  var curStatus = '全部', curType = '全部', curQ = '';

  var listEl = document.getElementById('ad-list');
  var countEl = document.getElementById('ad-count');

  function tag(text, cls) {
    return '<span class="tag' + (cls ? ' ' + cls : '') + '">' + text + '</span>';
  }
  function diffTag(d) {
    return d === '低' ? tag('难度低', 'tag-green') : d === '中' ? tag('难度中', 'tag-gold') : tag('难度高', 'tag-red');
  }
  function statusTag(s) {
    return s === '进行中' ? tag('进行中', 'tag-green') : s === '即将开始' ? tag('即将开始', 'tag-gold') : tag('已结束');
  }

  function buildFilters() {
    var sf = document.getElementById('ad-status-filters');
    STATUS.forEach(function (s) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'filter-chip' + (s === curStatus ? ' active' : '');
      b.textContent = s;
      b.addEventListener('click', function () { curStatus = s; refresh(); });
      sf.appendChild(b);
    });
    var tf = document.getElementById('ad-type-filters');
    TYPES.forEach(function (t) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'filter-chip' + (t === curType ? ' active' : '');
      b.textContent = t;
      b.addEventListener('click', function () { curType = t; refresh(); });
      tf.appendChild(b);
    });
  }

  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function refresh() {
    var chips = document.querySelectorAll('.filter-chip');
    chips.forEach(function (c) {
      var active = (c.textContent === curStatus) || (c.textContent === curType);
      c.classList.toggle('active', active);
    });
    var rows = AIRDROPS.filter(function (a) {
      if (curStatus !== '全部' && a.status !== curStatus) return false;
      if (curType !== '全部' && a.type !== curType) return false;
      if (curQ) {
        var hay = (a.name + a.chain + a.desc + a.value).toLowerCase();
        if (hay.indexOf(curQ.toLowerCase()) === -1) return false;
      }
      return true;
    });
    countEl.textContent = '共 ' + rows.length + ' 个空投（' + (curStatus === '全部' ? '全部状态' : curStatus) + ' · ' + (curType === '全部' ? '全部类型' : curType) + '）';
    listEl.innerHTML = '';
    if (!rows.length) {
      listEl.innerHTML = '<div class="db-empty">没有匹配的空投，换个筛选条件或关键词试试。</div>';
      return;
    }
    rows.forEach(function (a) {
      var card = document.createElement('div');
      card.className = 'db-card';
      var pts = (a.points || []).map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('');
      card.innerHTML =
        '<div class="db-card-head">' +
          '<span class="db-card-title">' + esc(a.name) + '</span>' +
          '<span class="db-card-tags">' + statusTag(a.status) + ' ' + diffTag(a.diff) + '</span>' +
        '</div>' +
        '<div class="db-card-tags" style="margin-bottom:8px">' + tag(esc(a.type), 'tag') + ' ' + tag(esc(a.chain), 'tag') + '</div>' +
        '<div class="db-card-desc">' + esc(a.desc) + '</div>' +
        (pts ? '<ul>' + pts + '</ul>' : '') +
        '<div class="db-meta"><span>⏱ 截止 <b>' + esc(a.deadline) + '</b></span><span>💰 价值 <b>' + esc(a.value) + '</b></span><span>🔗 <b>' + esc(a.link) + '</b></span></div>';
      listEl.appendChild(card);
    });
  }

  document.getElementById('ad-search').addEventListener('input', function (e) {
    curQ = e.target.value.trim();
    refresh();
  });

  buildFilters();
  refresh();
})();
</script>

## 这个空投查询工具怎么用

三步快速定位值得做的空投：

1. **筛选**——顶部点「进行中」只看还没结束的，点「持币」看只要持仓不折腾的类型，点「已结束」复盘历史。
2. **搜索**——直接输入项目名或链名，比如「币安」「Arbitrum」「Solana」。
3. **对比三件事**——难度（低中高）、预计价值、截止时间。难度低 + 价值高 + 还没截止的，才值得花 Gas 和精力。

> 一个反常识的结论：**「已结束」那几行才是最有信息量的**。Uniswap 只要交易过一次、ENS 只要持有一个域名、Arbitrum 只要做过跨链——未来几乎所有空投都逃不出这几类条件。与其天天追新项目，不如先把这些「基础交互」做全。

## 怎么判断一个空投值不值得做

空投不是「免费的午餐」，大多要花 Gas、花时间，还要承担女巫风险。动手前套用这条公式：

**预期收益 = 获奖概率 × 预估代币价值 − 交互成本（Gas + 时间）**

- 预期明显为正 → 值得做；为负 → 跳过。
- 越多人冲的项目，单人瓜分越少。那种「抽 2000 人每人 25U、5 万人报名」的任务，期望收益基本是零，纯属「牛马任务」。
- Gas 成本可以先到我们的[交互成本计算器](/tools/gas-cost-calculator/)估一遍，再决定要不要上。

<div class="callout callout-danger">
<div class="callout-title">⚠️ 领空投的安全红线</div>
<p style="margin:0">只从<strong>项目官方认领页</strong>领取；任何让你「先转账激活」「输入助记词/私钥」的，都是钓鱼。空投代币合约地址一定要和官方公布的核对，别领到假代币。</p>
</div>

## 交易所空投：有账户才能领

上表里「币安 USD1 空投」这类属于**交易所持币空投**，只需要持有稳定币就能瓜分，不需要链上折腾，是新手门槛最低的一类。但前提是得先有交易所账户并完成 KYC：

- [币安注册](/binance-register-guide/)——邀请码 BT123，注册后即可参与 USD1 等持币空投
- [欧易注册](/okx-register-guide/)——邀请码 60895497，也有钱包任务与空投活动

链上的「任务型/交互型」空投，则大多要一个 Web3 钱包去完成交易、签到、跨链，相关玩法见[如何从币安走向 DeFi](/binance-to-defi-guide/)。
