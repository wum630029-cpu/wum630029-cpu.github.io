---
title: '谁在发行美股代币？BTech、Backed、Ondo三大发行方牌照与资金安全对比，倒闭了钱能拿回来吗'
date: 2026-09-17T00:00:00+08:00
draft: false
description: '美股代币背后是谁在发行、你的钱押在谁身上？本文拆解 BTech（币安 bStocks）、Backed（xStocks）、Ondo 三大发行方的注册地、监管牌照、底层托管与破产隔离，用对比表看懂追踪凭证、结构化票据、上链注册三种架构的靠谱度排序，并给出买前查验发行方与抵押品的三步清单，回答倒闭时钱能不能拿回来。'
slug: 'us-stock-token-issuers-guide'
tags: ['美股代币', '代币化证券', 'RWA', 'bStocks', 'xStocks', 'Ondo', '发行方', '监管牌照']
categories: ['美股教程']
readingTime: 9
---

> 你在币安花 250 美元买一枚「特斯拉代币」，页面写着「特斯拉 · 1:1 足额背书」。但真正对你的持仓负责的，不是特斯拉，不是币安这家交易所，而是注册在阿布扎比的一家公司——**BTech Holdings**。下单前你有没有问过：这家公司是谁？它持什么牌照？它倒闭的那天，你手里的代币还能不能换成钱？

能换还是不能换，早在你下单前，就被「谁在发行、底层押了什么、出事时谁来接管」这三件事决定了。本文从「发行方」这个最被忽视、却最要命的角度讲起，系统覆盖：

- 美股代币的「发行方」到底是谁，为什么不是交易所
- BTech、Backed、Ondo 三大发行方：注册地、牌照、底层托管逐条对比
- 追踪凭证、结构化票据、上链注册三种架构，风险天差地别
- 发行方倒闭或违约时，你的钱在谁手里、能不能拿回来
- 买之前三步查验：把「谁在发行」查清楚再下单

💡 **学习前提**：还没分清美股代币和真实股票的区别？先看 [什么是美股代币](/what-is-us-stock-token-guide/) 和 [美股代币 vs 传统美股](/us-stock-token-vs-traditional-stock-guide/)；价格与折溢价原理见 [美股代币定价机制详解](/us-stock-token-pricing-mechanism-guide/)。本文是系列十五（链上美股与 RWA 专题）第 4 篇，下一篇推荐：**代币化证券赛道：RWA 如何改变传统资产配置**。

> 🔵 **注册链接**：想实操美股代币，先要有币安账户。[通过邀请链接注册](https://www.bsmkweb.cc/register?ref=BT123)（邀请码 **BT123**，享现货与合约手续费返佣）；🟧 欧易用户可用 [OKX 注册链接](https://www.promooboost.com/join/60895497)（邀请码 **60895497**）。**返佣披露**：以上为返佣推广链接，注册成功后我可能获得平台佣金，不影响你的费率与操作。

<div class="callout callout-tldr">
<div class="callout-title">TL;DR</div>
<ul>
<li><strong>结论一：</strong>美股代币的「发行方」不是币安、欧易、Bybit 这些交易所，而是它们背后的离岸 SPV——bStocks 是币安关联的 BTech Holdings，xStocks 是瑞士 Backed，Ondo 是英属维尔京的 Ondo Global Markets；你的钱本质押在这些 SPV 的承诺与底层托管上，不是押在交易所信用上。</li>
<li><strong>结论二：</strong>三大发行方各有真牌照（ADGM、瑞士 DLT、美国 SEC 系），但牌照只约束发行与披露，不等于「你直接持有股票」——除直接上链注册的 Securitize 一类外，其余都是凭证或票据性质的信用敞口，无投票权、无直接股息请求权。</li>
<li><strong>结论三：</strong>判断发行方靠谱度的核心不是「是否 1:1 背书」，而是「发行方不能行动时，谁控制抵押品」——优先选有独立担保受托人或独立托管明确披露的产品；买之前用三步查验（查发行主体、查底层托管与储备证明、查破产隔离条款）过滤掉不透明的发行方。</li>
</ul>
</div>

---

## 一、先纠正一个直觉：你买的不是「美股」，是「发行方对你的承诺」

在传统券商买苹果，链条很干净：券商是通道，股权登记在独立的**过户代理（transfer agent）**名下，券商倒闭有 SIPC 兜底，股票还是你的股票。但美股代币不是这样。

美股代币由**发行方（Issuer）**铸造，你手里的代币在法律上是「代表某种金融工具的凭证」或「票据」，是**对发行方的一份债权/信用敞口**，不是股权本身。币安、Bybit、Kraken 这些平台扮演的是**分销渠道**，把发行方的代币摆上订单簿，但发行责任、底层资产的持有，都在发行方手里。

以币安 bStocks 为例，你买一枚代币，完整的对手方链条是这样的：

| 环节 | 是谁 | 扮演角色 |
|---|---|---|
| 你下单的场所 | 币安 / Nest Exchange | 分销与撮合 |
| 你下单的实际券商 | Nest Trading（ADGM 持牌） | 执行、清算 |
| 发行主体 | BTech Holdings Ltd（ADGM SPV） | 铸造代币、对持有人负责 |
| 底层股票 | Alpaca Securities（纽约，FINRA/SIPC 成员） | 持有并托管真实股票 |

> **实操示例**：假设 BTech Holdings 出问题，而币安平台本身正常——你打开 App，代币可能还在，但兑换成真股、或按 1:1 赎回的通道会先停摆。反过来，币安平台出问题而 BTech 没事，你仍可尝试通过发行方层面的赎回通道把代币换回来。两者不是一回事，这是理解「发行方」的第一层意义。

据 RWA.xyz 数据（[链捕手整理](https://www.chaincatcher.com/article/2282639)，截至 2026 年 8 月中旬），代币化股票总规模约 **25 亿美元**，半年涨了近三倍：Ondo 约占 34.6%（8.66 亿美元）、币安 bStocks 约 24.5%（6.14 亿美元）、xStocks 约 22.4%（5.6 亿美元），前三家吃掉约 80%。规模反映的是接受度，不代表安全度——安全度要往下拆。

## 二、三大发行方逐一拆解：谁在背后、持什么牌照

把三家发行方的「老底」摊开，差异比想象中更大：

| 维度 | BTech Holdings（bStocks） | Backed（xStocks） | Ondo（Ondo Stocks） |
|---|---|---|---|
| 发行主体 | BTech Holdings Ltd，阿布扎比 ADGM SPV | Backed Assets (JE) Ltd，泽西岛 SPV | Ondo Global Markets (BVI) Ltd，英属维尔京 SPV |
| 背后集团 | 币安关联实体 | Kraken（2025-12 收购） | Ondo Finance |
| 牌照/监管 | ADGM FSRA 批准「代表特定金融工具的凭证」 | 瑞士 DLT 法案、列支敦士登 FMA | Reg S 离岸票据 + 美国 SEC 系（Oasis Pro） |
| 法律定性 | 凭证（certificate） | 追踪凭证（债务工具） | 结构性票据 / 贷款票据 |
| 底层托管 | Alpaca Securities（真股） | Alpaca（真股）+ InCore Bank（现金） | Alpaca（真股）+ BitGo（现金/稳定币） |
| 抵押/担保 | 1:1 背书 + 每日 Proof of Collateral | 1:1 + Lloyd's 1.75 亿美元补充保险 | 100.5% 超额抵押 + Ankura 担保受托 |

**BTech Holdings（币安 bStocks）**：注册在阿布扎比全球市场（ADGM）的独立 SPV，产品是首批被 ADGM FSRA 纳入官方名单的代币化证券之一。币安 2025 年 12 月已取得 ADGM 全牌照（交易所、清算所、经纪商三类活动），底层股票由纽约 Alpaca Securities 执行、清算与托管。关键历史：[aiying 的合规复盘](https://aiying.cc/uae/binance-bstocks-55b-adgm-compliance/) 指出，币安 2021 年那批股票代币（经德国合作方 CM-Equity 发行）因「借牌」被德国 BaFin 叫停，总交易量不到 7300 万美元；2026 版则从「借牌」转向「自己拿牌」。这是理解它合规性的重要背景。

**Backed（xStocks）**：瑞士苏黎世公司，发行主体是泽西岛的 Backed Assets (JE) Ltd。xStocks 2025 年 6 月底上线 Solana，约 60 个股票与 ETF 标的；[2025 年 12 月被 Kraken 母公司 Payward 收购](https://backed.fi/news-updates/backed-joins-kraken)。它的设计更「开放」：接入 Hyperliquid、Kraken、Bybit、Gate 等多个场地，还接入 Broadridge 治理平台让代币持有者首次能参与公司投票。

**Ondo（Ondo Stocks）**：发行主体是英属维尔京的 Ondo Global Markets (BVI) Ltd，走「结构性票据 + 超额抵押」路线，由 Ankura Trust 同时担任每日证明的验证代理与第一顺位担保受托人。2025 年 10 月收购美国 SEC 注册的券商 Oasis Pro 后，补齐了美国本土牌照，2026 年 7 月 [Oasis Pro Markets 拿到 FINRA 授权](https://ondo.finance/blog/finra-authorizations-to-offer-tokenized-equities)，可向美国投资者提供代币化股票与基金。

> **实操示例**：同样是「1:1」，三家背书的严密程度不同。假设真股跌了 2%，三家代币都跟着跌 2%——这一步三家一样。真正的差别在「极端情况」：Ondo 有 100.5% 的超额抵押和独立担保受托人，xStocks 有 Lloyd's 保险和独立托管，而 bStocks 的储备证明能验证「有对应股票」，但公开材料里对「出事时谁来接管」披露得最少。这一差别，正是第四节要展开的。

## 三、三种架构决定风险等级：追踪凭证 vs 结构化票据 vs 上链注册

「发行方」只是表层，决定你风险等级的是它背后的**产品架构**。目前市场通行的三种架构：

| 架构 | 你持有的是什么 | 代表 | 风险定位 |
|---|---|---|---|
| 追踪/债务凭证 | 对发行方 SPV 的凭证或债权，无股权 | bStocks、xStocks、Robinhood | 纯信用敞口，依赖发行方+托管 |
| 结构化票据 | 对离岸主体的贷款票据，超额抵押 | Ondo | 信用敞口，多一层独立担保 |
| 上链注册股份 | 链上登记的真实股份 | Securitize、Superstate | 最接近真股，但标的偏机构 |

关键结论一句话：**除了「上链注册股份」这一类，其余美股代币本质上都是「对发行方的信用敞口」，不是股权。** 你的收益来自价格跟踪，你的风险来自「发行方会不会违约、底层托管牢不牢」。

这也是为什么链捕手把这场竞争定性为「[发行、分销、清算的三层博弈](https://www.chaincatcher.com/article/2282639)」——独立发行方（Ondo、xStocks）手里只有「发行」一环，没有自带用户和流动性；而交易所自建发行（币安 bStocks、Robinhood、Bitget 的 rTokens）则把发行、分销、清结算全攥在自己手里。对用户来说，前者意味着「发行方和分销渠道分离，出问题能分开追责」，后者意味着「对手方高度集中，一条链出问题全线受影响」。

## 四、发行方出事时，你的钱到底在哪

这是全文最该记住的一节。专业机构（[degate 对发行方违约恢复路径的分析](https://degate.com/playbook/tokenized-stocks-issuer-failure-recovery/)）给出的判断很扎心：**核心问题不是「是否 1:1 足额支持」，而是「发行方不能行动时，谁控制抵押品」。**

拆开看三种恢复路径：

| 发行方 | 出事时谁接管抵押品 | 你的恢复形态 |
|---|---|---|
| Ondo | Ankura 作为担保受托人，持有人可指示其取得抵押品变现分配 | 现金或稳定币，非一定交付真股 |
| xStocks | 三方账户控制协议下的独立 Security Agent | 按招股书分配，含 Lloyd's 保险兜底 |
| bStocks | 公开材料未列明独立 security agent 与违约程序 | 机制披露最不完整，需自行向发行方主张 |

三个反直觉但重要的点：

1. **SIPC 误区**：代币持有人和券商客户差一层关系，SIPC 并不直接保护代币持有人；bStocks、Robinhood 类产品更是「完全没有 SIPC 式保护」的描述。你看到的 Alpaca、InCore 这些 SIPC/FINRA 监管托管方，保护的是「券商层面」，不直接等于「保护你」。

2. **托管集中度高于标签所示**：Alpaca Securities 同时出现在 xStocks、Ondo 等多家发行的底层——意味着底层券商的真实集中度，比「不同发行方」这几个字看起来要高。某一底层券商出问题，可能波及多家发行方。

3. **恢复形态不保证是「股票」**：即便有担保受托人，你最终拿到手的是现金或稳定币等价物，而非底层真股；「1:1 价值恢复、快速到账、明确时间表」这三样，没有任何发行方敢承诺。

> **实操示例**：假设某发行方破产。若你持有 Ondo，路径是「指示 Ankura 取得超额抵押的股票 → 变现 → 按比例分配」，理论上有个可执行的入口；若你持有的产品从未披露独立托管与接管程序，你连「该找谁、该走哪条程序」都要现查——等你查明白，清算可能已经走完。这就是为什么「破产隔离与接管机制」要写在买之前的检查清单第一条。

## 五、买之前三步查验：把「谁在发行」查清楚再下单

落到动作，买任何美股代币前，花五分钟走完这三步：

1. **查发行主体**：点开该代币的官方说明或招股书，找到「Issuer / 发行方」是谁——注册在哪个法域、持什么牌照。查不到发行主体、或只写「某平台发行」而无独立法律实体的，直接放弃。

2. **查底层托管与储备证明**：有没有每日或链上储备证明？托管方是不是知名的受监管机构（Alpaca、BitGo、InCore 等）？有没有**独立的**担保受托人（security agent）——注意「独立」二字，和发行方同属一个集团的托管不叫隔离。

3. **查破产隔离与违约条款**：招股书里有没有「bankruptcy-remote（破产隔离）」安排？发行方不能行动时，谁有权接管抵押品、按什么顺序分配？这一步查不到明确答案的，说明你的钱在出事时「没有路」。

可以对照这张快速打分表：

| 检查项 | 该问的问题 | 不过关的表现 |
|---|---|---|
| 发行主体 | 谁是 Issuer、注册在哪、持什么牌照 | 找不到独立发行实体 |
| 底层托管 | 托管方是谁、是否受监管、是否独立 | 托管方与发行方同属一集团且无独立担保 |
| 储备证明 | 能否每日/链上验证 1:1 | 没有可查的储备证明 |
| 破产隔离 | 有没有 security agent、接管程序 | 招股书无违约/接管条款 |

三条全绿的产品，才谈得上「发行方层面相对靠谱」；缺任何一条，都意味着你在赌发行方「不出事」，而不是「出事了也有人兜」。

## 常见误区

1. 「币安上买的，币安会兜底」→ 错。发行方是 BTech Holdings，币安是分销渠道；发行方层面的违约，不自动由交易所承担。
2. 「1:1 足额背书 = 绝对安全」→ 错。关键不是有没有对应股票，而是「出事时谁控制这批股票、能不能接管」。
3. 「有牌照 = 我能直接持有股票」→ 错。牌照约束发行与披露，多数产品是凭证/票据，无投票权、无直接股息请求权。
4. 「SIPC 会保护我的代币」→ 错。代币持有人不是券商客户，SIPC 不直接覆盖。
5. 「发行方被大公司收购就安全了」→ 未必。收购改变股权结构，不自动改变产品架构和你的索偿优先级。
6. 「规模大的发行方一定靠谱」→ 规模反映接受度，不反映破产隔离设计的严谨度。

## 常见问题

**怎么知道我买的这个代币到底是哪家发行的？**
在平台的代币详情页或官方说明里找「Issuer / 发行方」字段；链上可进一步核对合约部署方地址是否与发行方披露一致。若两者对不上，以招股书和监管备案为准。

**bStocks 的发行方 BTech 和币安是什么关系？**
BTech Holdings 是币安集团的关联实体、注册在 ADGM 的独立 SPV。法律上它是独立的发行主体，但发行方、交易场所（Nest Exchange）、转换券商（Nest Trading）同属币安集团生态，对手方集中度较高。

**三家发行方里，谁的「破产隔离」设计最清晰？**
从公开材料看，Ondo（Ankura 担保受托 + 超额抵押）和 xStocks（三方账户控制协议下的独立 Security Agent + Lloyd's 保险）披露得较完整；bStocks 在「独立 security agent 与违约程序」上的公开披露相对最少。这也影响出事时的追索路径是否清晰。

**发行方倒闭，我能拿回的是股票还是现金？**
不保证是股票。多数情况是抵押品被接管后变现，按比例以现金或稳定币分配，且没有快速到账或明确时间表的保证。能否启动追索，取决于招股书里有没有写清楚接管机制。

**美国用户能买这些代币吗？**
多数离岸发行方（bStocks、Ondo 离岸票据等）明确排除美国用户。Ondo 通过收购 Oasis Pro 拿到 FINRA 授权后，美国合规路径正在打开，但能否购买仍以各产品最新的官方口径和居住地限制为准。

## 总结：核心要点回顾

1. 美股代币的发行方是**离岸 SPV**，不是交易所——你的钱押在 SPV 的承诺与底层托管上，不是押在平台信用上。
2. 三大发行方各有**真牌照**，但「牌照」不等于「直接持股」——除上链注册类，其余都是凭证/票据性质的信用敞口。
3. 三种架构风险排序：**上链注册 > 有独立担保的结构化票据 > 纯追踪凭证**，关键看独立担保与破产隔离有没有配齐。
4. 靠谱度核心指标 = **独立托管 + 独立担保受托人 + 破产隔离**，而不是「1:1」或「规模大」。
5. 买前走完**三步查验**：查发行主体、查底层托管与储备证明、查破产隔离条款——三绿再下单。

## 📖 推荐阅读

- [币安 bStocks 全解析：20+ 标的一览、碎股与 7×24 小时交易](/binance-bstocks-overview-guide/)
- [币安买美股实操：USDC 入金到首次买入完整流程](/binance-bstocks-buy-guide/)
- [美股代币五大风险：价格偏差、流动性、托管、发行方与监管](/us-stock-token-five-risks-guide/)
- [美股代币 vs 传统美股：股东权益、分红与投票权对比](/us-stock-token-vs-traditional-stock-guide/)

## 🟦 注册链接

想实际操作美股代币，先开好账户：
- [币安注册](https://www.bsmkweb.cc/register?ref=BT123)（邀请码 **BT123**，享手续费返佣）
- 🟧 欧易（OKX）：[欧易注册](https://www.promooboost.com/join/60895497)（邀请码 **60895497**）

### 📌 更多学习资源

想横向看币安 bStocks 与 OKX、Bitget、Gate 各平台代币化股票的对比？CoinVado 社区的 [bStocks vs OKX/Bitget/Gate 代币化股票对比](https://coinvado.com/posts/bstocks-vs-okx-bitget-gate-tokenized-stocks-2026/) 与本文互为补充；更多教程与最新资讯，欢迎访问 [CoinVado](https://coinvado.com/zh/)。

---

*免责声明：本文仅供信息参考，不构成投资、法律或税务建议。美股代币存在发行方信用、托管、流动性、地域限制与链上操作等风险，极端情况下可能本金全损；文中对发行方的梳理基于截至 2026 年 8 月的公开材料，具体以各产品最新招股书与监管备案为准。*

*参考资料：*
- [币安官方 FAQ：bStocks 常见问题（1:1 背书、底层托管、倍数机制）](https://www.binance.com/zh-CN/support/faq/detail/f0c03cd6509a4085b4cce1636f16be38)
- [币安官方公告：bStocks 正式上线：代币化证券 1:1 支持，24/7 全天候交易](https://www.binance.com/zh-CN/support/announcement/detail/2c0c92ed15ac42d1b14bb1eac00d22bb)
- [Backed Joins Kraken（Kraken 收购 Backed Finance）](https://backed.fi/news-updates/backed-joins-kraken)
- [Ondo Finance：Oasis Pro Markets 获 FINRA 授权提供代币化股票与基金](https://ondo.finance/blog/finra-authorizations-to-offer-tokenized-equities)
- [degate：Tokenized Stocks Issuer Failure — Recovery Paths for xStocks, Ondo, and Dinari](https://degate.com/playbook/tokenized-stocks-issuer-failure-recovery/)
- [aiying：币安 bStocks 周交易额 55 亿美元创纪录——从 BaFin 叫停到 ADGM 持牌的合规跃迁](https://aiying.cc/uae/binance-bstocks-55b-adgm-compliance/)
- [链捕手：代币化股票的三层博弈——发行、分销与清算](https://www.chaincatcher.com/article/2282639)
