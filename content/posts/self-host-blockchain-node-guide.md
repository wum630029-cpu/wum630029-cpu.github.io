---
title: '自行搭建区块链节点完整指南：从零开始运行以太坊与 Solana 节点，硬件配置与运维技巧'
date: 2026-07-08T00:00:00+08:00
draft: false
description: '不想依赖 Infura 或 Alchemy 等第三方节点服务商？本文手把手教你搭建以太坊执行层 Geth 与共识层 Lighthouse 全节点及 Solana 节点。涵盖服务器硬件选型、操作系统环境优化、客户端安装同步、状态剪裁节省空间、同步加速技巧与运维监控告警设置，让你掌控区块链数据与 RPC 接口。'
slug: 'self-host-blockchain-node-guide'
tags: ['区块链节点', '以太坊', 'Solana', '全节点', 'Linux', '运维', 'RPC', '节点搭建']
categories: ['链上操作实战指南']
readingTime: 10
---

> 自己跑过全节点，才算真正理解区块链。
>
> 用 Infura、Alchemy 等第三方 RPC 服务很方便，但你每次查询、每笔交易都在依赖一个中心化入口。运行你自己的节点意味着：不信任第三方、完全掌控数据、免除速率限制、还能为网络去中心化出一份力。
>
> 本文教你从零搭建以太坊（执行层+共识层）和 Solana 的全节点，涵盖硬件选型、安装配置、状态剪裁、日常运维等全部环节。

---

## 一、为什么要自己跑节点？

在开始操作之前，先明确三个核心价值：

| 对比项 | 第三方 RPC 服务 | 自建节点 |
|--------|:-------------:|:--------:|
| 隐私 | 你的 IP 和查询内容对服务商可见 | 完全私密 |
| 速率限制 | 免费版有配额（通常 100k 请求/天） | 无限制 |
| 延迟 | 公共同步延迟（多人共享） | 本地局域网级 |
| 数据验证 | 信任服务商返回正确数据 | 本地全验证 |
| 月费 | 免费版有限，付费版 $50+/月 | 仅服务器成本 |
| 运维负担 | 无需维护 | 需自行维护 |

**适合自建节点的场景：**
- 你跑 DeFi 机器人的套利脚本，需要高频低延迟 RPC
- 你要验证链上交易的真实性
- 你想为网络去中心化做贡献
- 你开发 dApp 需要稳定可靠的测试环境

> ⚠️ **坦诚告知**：跑全节点需要一定的 Linux 基础（SSH、命令行、systemd）。如果你是纯新手，建议先用第三方 RPC 服务过渡，同时用本文在测试网练手。

---

## 二、硬件选型

### 以太坊全节点

以太坊有**执行层**（Execution Layer, EL）和**共识层**（Consensus Layer, CL）两个客户端需要同时运行。

| 配置项 | 最低要求 | 推荐配置（长期） |
|--------|:-------:|:--------------:|
| CPU | 4 核 | 8 核以上 |
| 内存 | 16 GB | 32 GB |
| 存储 | 2 TB SSD | 4 TB NVMe SSD |
| 带宽 | 100 Mbps | 500 Mbps+ |
| 系统 | Ubuntu 22.04+ | Ubuntu 24.04 LTS |

**存储是最关键的瓶颈**。以太坊全节点目前（2026 年中）的数据量约 **1.5 TB**，且每月增长 ~20 GB。**必须使用 NVMe SSD**，SATA SSD 的 IOPS 跟不上同步速度，可能导致节点永远无法追赶上最新区块。

> 💡 **省钱技巧**：使用"快照同步"（Snap Sync）+ 状态剪裁（Pruning），可以将存储需求降低到 500-800 GB。下文会详细介绍。

### Solana 全节点

Solana 对硬件要求远高于以太坊：

| 配置项 | 最低要求（验证节点） | 推荐配置 |
|--------|:----------------:|:--------:|
| CPU | 12 核 / 24 线程 | 24 核 / 48 线程（AMD Threadripper / Intel Xeon） |
| 内存 | 128 GB | 256 GB |
| 存储 | 1 TB NVMe（账本）+ 512 GB（账户） | 2 TB + 1 TB NVMe |
| GPU | 可选 | NVIDIA 4090（加速 PoH 验证） |
| 带宽 | 1 Gbps | 10 Gbps |

Solana 的性能要求意味着**普通云服务器不适合跑 Solana 验证节点**。如果只是想接入 Solana 网络查询数据，可以考虑运行 **RPC 节点**（要求略低）或使用 Geyser 插件过滤数据。

---

## 三、搭建以太坊节点

### 3.1 选择客户端组合

以太坊执行层和共识层有多种客户端实现，**推荐搭配**：

| 执行层 | 共识层 | 特点 |
|:------:|:------:|:----:|
| **Geth** | **Lighthouse** | 最成熟、文档最全、社区最大 |
| Nethermind | Prysm | 性能优秀、资源占用低 |
| Erigon | Teku | 存储效率极高（剪裁后可 <500 GB） |
| Besu | Nimbus | Java 生态、企业级支持 |

本文以 **Geth + Lighthouse** 为例——这是最主流的组合，遇到问题最容易搜到答案。

### 3.2 安装 Geth

1. 添加 Geth 官方 PPA 软件源：运行 add-apt-repository 命令，加 -y 参数自动确认，源地址为 ppa:ethereum/ethereum
2. 更新软件包索引：运行 apt update
3. 安装 Geth：运行 apt install 命令，加 -y 自动确认，安装 geth 包
4. 验证安装：运行 geth version 查看版本号

### 3.3 安装 Lighthouse

1. 先切换到临时目录 /tmp
2. 下载最新预编译二进制：用 wget 从 GitHub 官方 releases 的 latest 地址下载，文件名用 $(uname -m) 自动匹配系统架构（x86_64 或 aarch64）
3. 解压：用 tar -xzf 解压 lighthouse-*.tar.gz 压缩包
4. 把解压出的 lighthouse 可执行文件移动到 /usr/local/bin/ 目录，让它全局可用
5. 安装编译依赖：运行 apt install，安装 libclang-dev 和 libssl-dev 两个库
6. 验证安装：运行 lighthouse --version 查看版本号

### 3.4 初始化数据目录

1. 创建总数据目录 /data/ethereum：用 sudo mkdir -p 递归创建
2. 把该目录的所有者改为当前用户：用 sudo chown -R $USER:$USER，避免后续写权限问题
3. 创建 Geth 执行层数据目录 /data/ethereum/execution
4. 创建 Lighthouse 共识层数据目录 /data/ethereum/consensus

### 3.5 生成 JWT 密钥

共识层和执行层之间通过 JWT（JSON Web Token）认证通信：

1. 用 openssl rand -hex 32 生成 32 字节的随机十六进制字符串，去掉换行符后写入 /data/ethereum/jwt.hex
2. 这条命令输出的就是共识层与执行层之间认证用的 JWT 密钥文件，路径为 /data/ethereum/jwt.hex

### 3.6 启动 Geth（执行层）

运行 geth 启动执行层，核心参数如下：

1. 网络接口：用 --http 开启 HTTP-RPC，--http.addr 绑定 127.0.0.1（仅本机可访问），--http.port 设为 8545，--http.api 开放 eth、net、web3、txpool 这组 API；再用 --ws 开启 WebSocket，--ws.addr 绑定 127.0.0.1，--ws.port 设为 8546，--ws.api 开放 eth、net、web3
2. 认证接口：用 --authrpc.addr 绑定 127.0.0.1、--authrpc.port 设为 8551、--authrpc.jwtsecret 指向 /data/ethereum/jwt.hex，供共识层连接认证
3. 数据与同步：--datadir 指定数据目录为 /data/ethereum/execution
4. 最后把日志重定向写入 /data/ethereum/execution/geth.log 文件并放到后台运行

参数说明：
- --syncmode snap：使用快照同步，速度最快
- --cache 4096：分配 4 GB 内存作为数据库缓存（根据你的内存调整）
- --txlookuplimit 0：不保留历史交易索引（省空间，不影响实时查询）

> ⏱ **初次同步约需 6-12 小时**，取决于网络和磁盘速度。可以通过查看日志进度：用 tail -f 命令持续跟踪 /data/ethereum/execution/geth.log，配合 grep 过滤 "Imported" 关键字。

### 3.7 启动 Lighthouse（共识层）

运行 lighthouse bn 启动信标节点（共识层），核心参数如下：

1. 用 --datadir 指定数据目录为 /data/ethereum/consensus
2. 用 --network mainnet 指定连接以太坊主网
3. 用 --execution-endpoint 指向 http://127.0.0.1:8551 连接执行层，--execution-jwt 指定 JWT 密钥文件路径 /data/ethereum/jwt.hex
4. 用 --checkpoint-sync-url 指向 https://sync-mainnet.beaconcha.in，从可信检查点快速同步
5. 用 --http 开启 HTTP API，--http-address 绑定 127.0.0.1，--http-port 设为 5052
6. 最后把日志写入 /data/ethereum/consensus/lighthouse.log 并放到后台运行

参数说明：
- --checkpoint-sync-url：从可信检查点同步，大幅缩短共识层同步时间（从数天缩短到数分钟）
- 共识层无需 --http-api 暴露给公网（除非你需要远程信标链 API）

### 3.8 验证节点状态

1. 检查 Geth 同步进度：运行 geth attach 连接到本地节点，用 --datadir 指定数据目录，再用 --exec 参数执行 eth.syncing 查询；如果返回 false 表示已同步完成，如果返回对象则可以看到当前区块和最高区块的差值
2. 检查 Lighthouse 状态：用 curl 请求 http://127.0.0.1:5052/eth/v1/node/syncing 接口，配合 jq 格式化输出
3. 检查对等节点数量：运行 geth attach 后执行 net.peerCount 查询
4. 查看日志：用 tail -f 持续跟踪 /data/ethereum/execution/geth.log 和 /data/ethereum/consensus/lighthouse.log

**同步完成后的表现：**
- Geth 日志稳定输出 "Imported new chain segment" 每 12 秒
- eth.syncing 返回 false
- Lighthouse 日志输出 "Slot tick" 跟随当前 slot

### 3.9 配置 systemd 服务（推荐）

手动启动的进程会在 SSH 断开后终止。用 systemd 让节点开机自启：

1. 创建 Geth 的 systemd 服务单元，用 sudo tee 写入 /etc/systemd/system/geth.service，内容要点：
   - Unit 段：描述为 Geth Execution Layer，在网络就绪（network.target）之后启动
   - Service 段：以当前用户运行，Type 设为 simple，崩溃自动重启（Restart 设为 always，间隔 RestartSec 为 30 秒）
   - ExecStart 启动命令为 /usr/bin/geth，参数与 3.6 节手动启动一致（数据目录、HTTP 端口 8545、WebSocket 端口 8546、认证 RPC 端口 8551、snap 同步、4 GB 缓存、关闭历史交易索引）
   - Install 段：WantedBy 设为 multi-user.target，实现开机自启
2. 创建 Lighthouse 的 systemd 服务单元，用 sudo tee 写入 /etc/systemd/system/lighthouse.service，内容要点：
   - Unit 段：在网络就绪和 geth.service 之后启动（保证执行层先就绪），即 After 与 Wants 都包含 network.target 和 geth.service
   - ExecStart 启动命令为 /usr/local/bin/lighthouse bn，参数与 3.7 节一致（数据目录、主网、执行层端点、JWT 密钥、检查点同步、HTTP API 端口 5052）
   - 同样配置自动重启（Restart=always、RestartSec=30）与开机自启（WantedBy=multi-user.target）
3. 重新加载 systemd 配置：运行 sudo systemctl daemon-reload
4. 设置开机自启：运行 sudo systemctl enable geth lighthouse
5. 启动两个服务：分别运行 sudo systemctl start geth 和 sudo systemctl start lighthouse
6. 检查状态：运行 sudo systemctl status geth 和 sudo systemctl status lighthouse 确认运行正常

---

## 四、使用你的节点

### 4.1 本地调用 RPC

节点同步完成后，你就可以用它来发送交易和查询链上数据了：

1. 获取最新区块号：用 curl 向 http://127.0.0.1:8545 发送 POST 请求，请求头 Content-Type 设为 application/json，请求体用 JSON-RPC 2.0 格式调用 eth_blockNumber 方法（无参数，id 为 1）
2. 返回示例为 {"jsonrpc":"2.0","id":1,"result":"0x132a3f8"}，其中 result 是十六进制区块号，换算成十进制为 20033528

### 4.2 安全暴露 RPC（可选）

如果需要从其他机器访问你的节点 RPC，**务必做好安全措施**：

1. **不要直接把 RPC 暴露到公网**——任何人都可以通过你的 RPC 发交易，会让你损失 Gas 费用
2. **正确的做法是先做一层反向代理 + IP 白名单**

1. 用 Nginx 做反向代理加 IP 白名单：创建站点配置文件 /etc/nginx/sites-available/eth-rpc（用 sudo tee 写入），要点如下：
   - 监听 8545 端口并启用 SSL（listen 8545 ssl）
   - server_name 填你的域名
   - 用 ssl_certificate 和 ssl_certificate_key 分别指定证书与私钥的路径
   - IP 白名单：用 allow 放行你的内网或跳板机 IP，再用 deny all 拒绝其他所有来源
   - location / 段把请求代理到本地 127.0.0.1:8545，并透传 Host 与 X-Real-IP 请求头

更安全的方法是使用 **SSH 隧道**：
1. 在本地机器上建立 SSH 隧道：运行 ssh -L 8545:127.0.0.1:8545 your-server，把服务器上的 8545 端口映射到本地 8545
2. 之后本地浏览器或脚本访问 http://127.0.0.1:8545 即可使用节点 RPC

### 4.3 查询链上数据

同步完成后，你的节点可以回答任何链上问题：

1. 查询 USDT 合约余额：用 curl 向本地节点发送 eth_call 请求，to 填 USDT 在以太坊上的合约地址 0xdAC17F958D2ee523a2206206994597C13D831ec7，data 填 balanceOf 方法选择器 0x70a08231 后接你的钱包地址（去掉 0x 前缀、补足 40 位十六进制），区块参数用 latest
2. 查询交易收据：用 curl 发送 eth_getTransactionReceipt 请求，params 填目标交易哈希（0x 开头），即可获得该笔交易的回执

### 4.4 用 WebSocket 订阅实时事件

1. 先安装 wscat 工具：运行 sudo apt install -y wscat
2. 连接 WebSocket：运行 wscat -c ws://127.0.0.1:8546
3. 连接后发送订阅请求：调用 eth_subscribe 方法，订阅类型为 newHeads（新区块头）
4. 之后每次产生新区块，你都会收到实时推送

---

## 五、存储优化与剪裁

### 5.1 理解剪裁（Pruning）

以太坊全节点默认保存所有历史状态数据（每个账户的余额、合约存储等）。Geth 的 snap 同步模式会自动剪裁不需要的旧状态，但你可能还需要进一步优化：

1. 检查当前数据使用量：运行 du -sh 查看 /data/ethereum/execution/geth/chaindata 和 /data/ethereum/execution/geth/state 两个目录的大小，其中 state 目录通常最大
2. Geth 在线剪裁（2024 年后版本支持）：运行 geth 命令，用 --datadir 指定数据目录，再执行 snapshot prune-state 子命令完成剪裁

### 5.2 使用 Erigon 获得最小存储

如果你的存储空间紧张，考虑改用 Erigon（执行层）：

1. Erigon 的存储效率极高，剪裁后仅需 400-600 GB，适合存储紧张时替代 Geth
2. 安装 Erigon：用 wget 从 GitHub 官方 releases 下载 latest 版本，文件名用 $(uname -m) 匹配系统架构；tar 解压后把 erigon 可执行文件移动到 /usr/local/bin/
3. 启动 Erigon：运行 erigon 命令，--datadir 指定 /data/ethereum/erigon，--chain mainnet 指定主网，--prune htc 剪裁历史交易、收据和调用数据（Erigon 自带 sentinel 共识层集成）

### 5.3 数据目录总览

优化后的以太坊节点数据布局（在 /data/ethereum/ 目录下）：
- execution/：Geth 数据目录
  - geth/chaindata/：约 300 GB，区块数据
  - geth/trie/：约 200 GB，状态树
  - geth/lightchaindata/：极小，light client 缓存
- consensus/：Lighthouse 数据目录
  - beacon/：约 100 GB，信标链数据
- jwt.hex：JWT 密钥，仅 64 字节

---

## 六、日常运维与监控

### 6.1 检查健康状态

1. 创建健康检查脚本 /usr/local/bin/check-eth-node.sh，脚本逻辑如下：
   - 输出标题"以太坊节点健康检查"和当前时间
   - 用 pgrep -x 检查 geth 进程：存在则输出"Geth 运行中"，否则输出"Geth 未运行"并标记为错误
   - 用 pgrep -x 检查 lighthouse 进程：存在则输出"Lighthouse 运行中"，否则输出"Lighthouse 未运行"并标记为错误
   - 用 geth attach 执行 eth.syncing 查询同步状态：返回 false 则输出"节点已同步"，否则输出"节点同步中"并标记为警告
   - 用 geth attach 执行 net.peerCount 查询并打印当前对等节点数量
   - 用 df -h 查看 /data/ethereum 的磁盘占用并打印使用百分比
2. 给脚本加上可执行权限：运行 chmod +x /usr/local/bin/check-eth-node.sh
3. 运行检查：执行 /usr/local/bin/check-eth-node.sh 查看各项健康指标

### 6.2 设置警报

1. 创建监控脚本 /usr/local/bin/watch-eth-node.sh，脚本逻辑如下：
   - 用 geth attach 查询 net.peerCount 得到对等节点数，若少于 3 个，就调用 Telegram Bot API（把 BOT_TOKEN 和 CHAT_ID 替换成你自己的）发送消息，内容提示对等节点不足并附上当前数量
   - 用 df 查看 /data/ethereum 的可用空间，若少于 50 GB（即 50000000 KB），同样通过 Telegram 发送磁盘空间不足的告警，并带上换算后的剩余 GB 数
2. 用 crontab 设置定时任务：每 15 分钟运行一次该脚本，cron 表达式为 */15 * * * *

### 6.3 节点升级

以太坊客户端经常更新，建议每月检查一次版本：

1. Geth 升级：运行 sudo apt update 更新索引，再用 sudo apt upgrade -y geth 升级，完成后 sudo systemctl restart geth 重启服务
2. Lighthouse 升级（重新下载二进制）：
   - 用 wget 下载最新版本到 /tmp/lighthouse.tar.gz，文件名用 $(uname -m) 匹配系统架构
   - 先 sudo systemctl stop lighthouse 停止旧进程
   - 解压 /tmp/lighthouse.tar.gz 到 /tmp
   - 把解压出的 lighthouse 移动到 /usr/local/bin/ 覆盖旧版
   - sudo systemctl start lighthouse 重新启动

---

## 七、搭建 Solana RPC 节点

如果你需要访问 Solana 生态，运行一个 Solana RPC 节点：

1. 安装 Solana CLI：用 sh 执行官方安装脚本（从 https://release.anza.xyz/stable/install 下载），然后把安装目录加入 PATH 环境变量，最后运行 solana --version 验证安装
2. 创建数据目录：运行 mkdir -p /data/solana 并进入该目录
3. 生成 validator 身份密钥：运行 solana-keygen new 并指定输出文件为 ~/validator-keypair.json（RPC 节点也需要一个身份密钥）
4. 启动 RPC 节点：运行 solana-validator，核心参数如下：
   - --identity 指定身份密钥文件 ~/validator-keypair.json
   - --ledger 指定账本目录 /data/solana/ledger，--accounts 指定账户目录 /data/solana/accounts
   - --rpc-port 8899 开放 RPC 端口
   - 用多个 --entrypoint 指定主网入口节点（entrypoint.mainnet-beta.solana.com:8001 到 entrypoint5）
   - --limit-ledger-size 50000000 限制账本大小
   - --enable-rpc-transaction-history 和 --rpc-pubsub-enable 开启交易历史与 PubSub 订阅
   - --no-snapshot-fetch-in-parallel 关闭并行抓取快照
   - 日志写入 /data/solana/solana.log 并放到后台运行

> ⚠️ **Solana 节点运维负担较重**，日均日志量可达 10+ GB。建议启用日志轮转：用 sudo tee 把 logrotate 配置写入 /etc/logrotate.d/solana，对 /data/solana/solana.log 每天轮转一次（daily）、保留 7 份（rotate 7）、启用压缩（compress）、文件缺失或为空时跳过（missingok 与 notifempty）、用 copytruncate 方式截断以便日志持续写入。

---

## 八、常见问题排查

### 8.1 同步速度太慢

1. 检查磁盘 IO：运行 iostat -x 1 查看，确保 %util 不超过 90%、await 不超过 10ms
2. 检查带宽：先运行 sudo apt install -y nethogs 安装，再运行 sudo nethogs 查看各进程的带宽占用
3. 检查对等节点：运行 geth attach 后执行 net.peerCount 查询
4. 如果 peerCount 太少，在 Geth 启动参数中增加 --maxpeers 50，提高最大对等节点数

### 8.2 节点同步中断后重启

1. 查看上次中断的日志：运行 tail -50 查看 /data/ethereum/execution/geth.log 最后 50 行
2. 安全重启流程：
   - 先 sudo systemctl stop lighthouse 停止共识层
   - 再 sudo systemctl stop geth 停止执行层
   - 等待 30 秒让数据库安全关闭（sleep 30）
   - sudo systemctl start geth 启动执行层
   - 等 Geth 完全启动后再启动 Lighthouse（sleep 60）
   - sudo systemctl start lighthouse 启动共识层

### 8.3 数据库损坏

1. Geth 提供了修复工具：运行 geth 命令并指定数据目录，执行 removedb 子命令——注意这会删除所有数据，需要重新同步
2. 更好的选择是保留链数据、仅重新同步状态：运行 geth 并指定数据目录，加上 --syncmode snap 参数重新做快照同步

---

## 九、资源消耗参考

以下是经过 3 个月稳定运行的实测数据：

| 指标 | 以太坊（Geth+Lighthouse） | Solana RPC 节点 |
|------|:------------------------:|:---------------:|
| CPU 平均占用 | 15-30% | 40-70% |
| 内存占用 | 8-16 GB | 64-120 GB |
| 磁盘增长 | ~20 GB/月 | ~100 GB/月 |
| 月流量 | 约 2-5 TB | 约 10-30 TB |
| 月电费（估算） | $20-40 | $80-200 |
| 月服务器租金 | $30-80（独服） | $200-500（独服） |

---

## 十、值得尝试的其他节点

除了以太坊和 Solana，还有一些有趣的全节点可以自己跑：

- **Bitcoin Core**：存储约 600 GB，配置最简易，跑过即对比特币有更深理解
- **Polygon Edge**：兼容以太坊，数据量较小（~200 GB），适合低配机器
- **Arbitrum Nitro**：Layer 2 全节点，需要 L1 节点配合运行
- **BNB Chain**：基于 Geth 分叉，存储约 300 GB，配置与 Geth 基本一致

1. 下载 Bitcoin Core：用 wget 下载 27.0 版本 x86_64 的 Linux 安装包（从 bitcoincore.org 的 bin 目录下载）
2. 解压：用 tar 解压 bitcoin-*.tar.gz 压缩包
3. 安装：用 sudo install 把解压出的 bitcoin-27.0/bin 目录下的可执行文件装到 /usr/local/bin
4. 启动：运行 bitcoind，加 -daemon 后台运行、-datadir=/data/bitcoin 指定数据目录

---

## 最后

自己跑节点是一趟有回报的技术旅程。第一周需要花些时间调试同步速度，之后就基本不用管了。一旦节点追上链头，你就有了一条完全属于你自己的区块链入口——不限速、不收费、不依赖任何人。这份自主权，正是加密货币最初的理念。

> 🔗 **扩展阅读**：
> - [Geth 官方文档](https://geth.ethereum.org/docs/)
> - [Lighthouse Book](https://lighthouse-book.sigmaprime.io/)
> - [Solana 验证节点指南](https://docs.anza.xyz/operations/setup-solana-validator)
> - [以太坊节点监控工具 ethdo](https://github.com/wealdtech/ethdo)

想看更完整的内容？可看 CoinVado 社区的[区块链节点类型](https://coinvado.com/posts/blockchain-node-types-full-light-archive-2026/)，与本篇图文互为补充；更多教程与最新资讯，欢迎访问 [CoinVado](https://coinvado.com/zh/)。
