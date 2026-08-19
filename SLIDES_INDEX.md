# Neon 架构解析 · 幻灯片索引

由 `gen_neon_bento.py` 自动生成，请勿手改；改动幻灯片后重新运行生成脚本即可刷新。

- 总页数：**75**
- 生成物：`Bento_Slides.bento.html`（内嵌 `bento/slides` JSON）

| # | 章节 | 分类 | 标题 | slide id |
|---|---|---|---|---|
| 1 | 封面 | — | Neon | `cover` |
| 2 | 封面 | 目录 | 大章节总览 | `s-toc` |
| 3 | **01 背景痛点** | 分节页 | — | `s-div1` |
| 4 | 01 背景痛点 | 理论基石 | “The log is the database.” — Aurora, SIGMOD 2017 | `s-log-is-db` |
| 5 | 01 背景痛点 | 定位 | Neon vs 传统 PostgreSQL：核心区别 | `s-position` |
| 6 | 01 背景痛点 | 定位 | 核心定位与核心价值 | `s-goals` |
| 7 | **02 顶层架构总览** | 分节页 | — | `s-div2` |
| 8 | 02 顶层架构总览 | 组件总览 | 六大核心组件 | `s-topo` |
| 9 | 02 顶层架构总览 | 架构 | 端到端数据流拓扑 | `s-arch` |
| 10 | **03 核心数据流：写路径 + 读路径** | 分节页 | — | `s-div-flow` |
| 11 | 03 核心数据流：写路径 + 读路径 | 写路径 | 一次 INSERT 的旅程 | `s-write` |
| 12 | 03 核心数据流：写路径 + 读路径 | 读路径 | 一次 SELECT 的旅程 | `s-read` |
| 13 | **04 组件逐层拆解：读写路径贯穿** | 分节页 | — | `s-div3` |
| 14 | 04 组件逐层拆解：读写路径贯穿 | PROXY | 连接代理：路由 + 认证 + Serverless 网关 | `s-proxy` |
| 15 | 04 组件逐层拆解：读写路径贯穿 | PROXY | 连上 Neon：Proxy 怎么知道你要连哪个库 | `s-conn-route` |
| 16 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute Node — patched PostgreSQL 的四点关键改动 | `s-comp1` |
| 17 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl —— compute 容器里的 PostgreSQL 监护进程 | `s-computectl` |
| 18 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | 内部端口 3081 —— 4 个路由，两类调用方 | `s-cc-internal` |
| 19 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute VM 里都有哪些常驻进程 | `s-cc-procs` |
| 20 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl 状态机 —— ComputeStatus 全 11 态 | `s-comp-sm` |
| 21 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | POST /configure 之后：compute_ctl 与 PG 的这 2 秒 | `s-cfg-seq` |
| 22 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Bootstrap Template 机制（本地 Fork 特性） | `s-boot` |
| 23 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | basebackup：无状态 Compute 的冷启动包 | `s-basebackup` |
| 24 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | ComputeSpec：一份「期望状态」文档，热加载不重启 | `s-compute-spec` |
| 25 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | LFC：Local File Cache | `s-lfc` |
| 26 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | DDL Forwarding：库/角色变更实时联动控制面 | `s-ddl-fwd` |
| 27 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | WAL 服务：Paxos-like 复制 | `s-sk1` |
| 28 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 三个核心 LSN | `s-lsn` |
| 29 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | SK 成员迁移：generation 双阶段递增（RFC 035） | `s-sk-migrate` |
| 30 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 侧关键 LSN（timeline.rs / models.rs） | `s-ps-lsn` |
| 31 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver — 存储引擎核心 | `s-ps1` |
| 32 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | 多租户模型：Tenant / Timeline | `s-ps-model` |
| 33 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Layer 文件：不可变的两级 LSM | `s-ps-layer` |
| 34 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | 写入缓冲 InMemoryLayer：pageserver 的 MemTable | `s-ps-inmem` |
| 35 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | S3 上怎么区分 L0 / L1：光看文件名就够了 | `s-ps-layer-name` |
| 36 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | LayerMap：(Key, LSN) 二维查找索引 | `s-layermap` |
| 37 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | index_part.json：远端 timeline 的权威清单 | `s-indexpart` |
| 38 | 04 组件逐层拆解：读写路径贯穿 | 读路径 | Page → LSN：Compute 怎么知道该用什么 LSN 请求 | `s-read-lsn` |
| 39 | 04 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Broker & Storage Controller | `s-bc` |
| 40 | 04 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Controller 的元数据表（依赖一套独立 PG） | `s-storcon-schema` |
| 41 | **05 核心原理深度剖析** | 分节页 | — | `s-div4` |
| 42 | 05 核心原理深度剖析 | PAGESERVER | 为什么 S3 有延迟：Ephemeral Layer 的滚动策略 | `s-flush-policy` |
| 43 | 05 核心原理深度剖析 | PAGESERVER | L0 什么时候变成 L1：计数阈值 + 事件驱动 | `s-l0-compact-trigger` |
| 44 | 05 核心原理深度剖析 | PAGESERVER | 一条 WAL 的完整生命周期：8 个 LSN 检查点 | `s-lsn-chain` |
| 45 | 05 核心原理深度剖析 | PAGESERVER | WAL Redo：每租户独立的 seccomp 沙箱 | `s-walredo` |
| 46 | 05 核心原理深度剖析 | PAGESERVER | 沙箱边界细节：seccomp 白名单、加固与逃逸风险 | `s-walredo-sec` |
| 47 | 05 核心原理深度剖析 | 全链路 | 背压：三层限速把写入速度钉在存储能力上 | `s-bp` |
| 48 | 05 核心原理深度剖析 | PAGESERVER | Compaction & GC 关键参数 | `s-compact` |
| 49 | 05 核心原理深度剖析 | PAGESERVER | Timeline / 分支 GC：谁能被回收 | `s-gc` |
| 50 | 05 核心原理深度剖析 | PAGESERVER | Sharding & Generation Number | `s-shard` |
| 51 | 05 核心原理深度剖析 | PAGESERVER | Secondary Location：热备用的只读缓存 | `s-secondary` |
| 52 | 05 核心原理深度剖析 | 协调层 | 如何防止 Compute / Pageserver 脑裂 | `s-splitbrain` |
| 53 | **06 标志性能力实现** | 分节页 | — | `s-div5` |
| 54 | 06 标志性能力实现 | BRANCHING | Copy-on-Write 分支 —— Neon 的杀手锏 | `s-branch1` |
| 55 | 06 标志性能力实现 | BRANCHING | CoW 分支 vs 传统快照 | `s-branch2` |
| 56 | 06 标志性能力实现 | BRANCHING | Synthetic Size：与物理布局解耦的计费 | `s-synsize` |
| 57 | 06 标志性能力实现 | BRANCHING | 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现） | `s-schema-diff` |
| 58 | 06 标志性能力实现 | PROXY | wake_compute：从「连接请求」到「一台活着的 Postgres」 | `s-wake` |
| 59 | 06 标志性能力实现 | 核心卖点 | Scale-to-Zero：闲置即销毁 | `s-s2z` |
| 60 | 06 标志性能力实现 | 核心卖点 | Autoscaling：CPU & Memory 弹性伸缩 | `s-auto` |
| 61 | 06 标志性能力实现 | 存储底座 | 多云对象存储支持 | `s-cloud` |
| 62 | **07 运维·限制·对比·落地** | 分节页 | — | `s-div6` |
| 63 | 07 运维·限制·对比·落地 | 数字 | 关键参数一览 | `s-numbers` |
| 64 | 07 运维·限制·对比·落地 | COMPUTE | 读懂 compute 日志：[NEON] / [NEON_SMGR] / [WP] / [COMMUNICATOR] | `s-log-prefix` |
| 65 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 周期任务清单：以 timeline_manager 为调度中枢 | `s-sk-tasks` |
| 66 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 常见刷屏日志诊断：ENOENT 竞态 vs 预期 NotFound | `s-sk-logs` |
| 67 | 07 运维·限制·对比·落地 | PAGESERVER | pageserver 周期任务清单：per-tenant 三件套 + 进程级全局 | `s-ps-tasks` |
| 68 | 07 运维·限制·对比·落地 | PAGESERVER | 读懂 pageserver 日志：稳态刷屏行逐条解码 | `s-ps-logs` |
| 69 | 07 运维·限制·对比·落地 | 可观测 | 关键指标：从背压到冷启动，看哪几个数就够 | `s-metrics` |
| 70 | 07 运维·限制·对比·落地 | 故障演练 | 两个典型故障：SK 单点宕机 / PS 实例宕机 | `s-failure` |
| 71 | 07 运维·限制·对比·落地 | 局限 | 架构局限 & Tradeoff：清醒地知道边界在哪 | `s-tradeoff` |
| 72 | 07 运维·限制·对比·落地 | 开发方向 | 近期 Git 历史脉络（本 Fork） | `s-dev` |
| 73 | 07 运维·限制·对比·落地 | 源码 | 想深挖？从这里开始 | `s-src` |
| 74 | 07 运维·限制·对比·落地 | 总结 | Neon 的核心设计哲学 | `s-sum` |
| 75 | 07 运维·限制·对比·落地 | — | Thank You | `s-end` |

## 按分类归组

- **PAGESERVER**（19 页）：30 Pageserver 侧关键 LSN（timeline.rs / models.rs）、31 Pageserver — 存储引擎核心、32 多租户模型：Tenant / Timeline、33 Layer 文件：不可变的两级 LSM、34 写入缓冲 InMemoryLayer：pageserver 的 MemTable、35 S3 上怎么区分 L0 / L1：光看文件名就够了、36 LayerMap：(Key, LSN) 二维查找索引、37 index_part.json：远端 timeline 的权威清单、42 为什么 S3 有延迟：Ephemeral Layer 的滚动策略、43 L0 什么时候变成 L1：计数阈值 + 事件驱动、44 一条 WAL 的完整生命周期：8 个 LSN 检查点、45 WAL Redo：每租户独立的 seccomp 沙箱、46 沙箱边界细节：seccomp 白名单、加固与逃逸风险、48 Compaction & GC 关键参数、49 Timeline / 分支 GC：谁能被回收、50 Sharding & Generation Number、51 Secondary Location：热备用的只读缓存、67 pageserver 周期任务清单：per-tenant 三件套 + 进程级全局、68 读懂 pageserver 日志：稳态刷屏行逐条解码
- **COMPUTE**（12 页）：16 Compute Node — patched PostgreSQL 的四点关键改动、17 compute_ctl —— compute 容器里的 PostgreSQL 监护进程、18 内部端口 3081 —— 4 个路由，两类调用方、19 Compute VM 里都有哪些常驻进程、20 compute_ctl 状态机 —— ComputeStatus 全 11 态、21 POST /configure 之后：compute_ctl 与 PG 的这 2 秒、22 Bootstrap Template 机制（本地 Fork 特性）、23 basebackup：无状态 Compute 的冷启动包、24 ComputeSpec：一份「期望状态」文档，热加载不重启、25 LFC：Local File Cache、26 DDL Forwarding：库/角色变更实时联动控制面、64 读懂 compute 日志：[NEON] / [NEON_SMGR] / [WP] / [COMMUNICATOR]
- **SAFEKEEPER**（5 页）：27 WAL 服务：Paxos-like 复制、28 Safekeeper 三个核心 LSN、29 SK 成员迁移：generation 双阶段递增（RFC 035）、65 safekeeper 周期任务清单：以 timeline_manager 为调度中枢、66 safekeeper 常见刷屏日志诊断：ENOENT 竞态 vs 预期 NotFound
- **BRANCHING**（4 页）：54 Copy-on-Write 分支 —— Neon 的杀手锏、55 CoW 分支 vs 传统快照、56 Synthetic Size：与物理布局解耦的计费、57 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现）
- **PROXY**（3 页）：14 连接代理：路由 + 认证 + Serverless 网关、15 连上 Neon：Proxy 怎么知道你要连哪个库、58 wake_compute：从「连接请求」到「一台活着的 Postgres」
- **协调层**（3 页）：39 Storage Broker & Storage Controller、40 Storage Controller 的元数据表（依赖一套独立 PG）、52 如何防止 Compute / Pageserver 脑裂
- **定位**（2 页）：5 Neon vs 传统 PostgreSQL：核心区别、6 核心定位与核心价值
- **读路径**（2 页）：12 一次 SELECT 的旅程、38 Page → LSN：Compute 怎么知道该用什么 LSN 请求
- **核心卖点**（2 页）：59 Scale-to-Zero：闲置即销毁、60 Autoscaling：CPU & Memory 弹性伸缩
- **目录**（1 页）：2 大章节总览
- **理论基石**（1 页）：4 “The log is the database.” — Aurora, SIGMOD 2017
- **组件总览**（1 页）：8 六大核心组件
- **架构**（1 页）：9 端到端数据流拓扑
- **写路径**（1 页）：11 一次 INSERT 的旅程
- **全链路**（1 页）：47 背压：三层限速把写入速度钉在存储能力上
- **存储底座**（1 页）：61 多云对象存储支持
- **数字**（1 页）：63 关键参数一览
- **可观测**（1 页）：69 关键指标：从背压到冷启动，看哪几个数就够
- **故障演练**（1 页）：70 两个典型故障：SK 单点宕机 / PS 实例宕机
- **局限**（1 页）：71 架构局限 & Tradeoff：清醒地知道边界在哪
- **开发方向**（1 页）：72 近期 Git 历史脉络（本 Fork）
- **源码**（1 页）：73 想深挖？从这里开始
- **总结**（1 页）：74 Neon 的核心设计哲学
