# Neon 架构解析 · 幻灯片索引

由 `gen_neon_bento.py` 自动生成，请勿手改；改动幻灯片后重新运行生成脚本即可刷新。

- 总页数：**91**
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
| 16 | 04 组件逐层拆解：读写路径贯穿 | PROXY | neon_proxy_params_compat：启动参数透传的兼容开关 | `s-params-compat` |
| 17 | 04 组件逐层拆解：读写路径贯穿 | PROXY | Proxy 为什么依赖 Redis：无状态集群的共享短时状态层 | `s-proxy-redis` |
| 18 | 04 组件逐层拆解：读写路径贯穿 | PROXY · TLS | Neon 的 TLS：两跳加密，两套证书 | `s-tls-overview` |
| 19 | 04 组件逐层拆解：读写路径贯穿 | PROXY · TLS | 客户端握手：SSLRequest 升级，或直接开打 TLS | `s-tls-handshake` |
| 20 | 04 组件逐层拆解：读写路径贯穿 | PROXY · TLS | CertResolver：一张通配证，按 SNI 剥域名匹配 | `s-tls-cert` |
| 21 | 04 组件逐层拆解：读写路径贯穿 | PROXY · TLS | SCRAM Channel Binding：把认证钉在这张叶子证上 | `s-tls-cbind` |
| 22 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE · TLS | 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres | `s-tls-compute` |
| 23 | 04 组件逐层拆解：读写路径贯穿 | PROXY · TLS | pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界 | `s-tls-router` |
| 24 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute Node — patched PostgreSQL 的四点关键改动 | `s-comp1` |
| 25 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl —— compute 容器里的 PostgreSQL 监护进程 | `s-computectl` |
| 26 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | 内部端口 3081 —— 4 个路由，两类调用方 | `s-cc-internal` |
| 27 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute VM 里都有哪些常驻进程 | `s-cc-procs` |
| 28 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl 状态机 —— ComputeStatus 全 11 态 | `s-comp-sm` |
| 29 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | POST /configure 之后：compute_ctl 与 PG 的这 2 秒 | `s-cfg-seq` |
| 30 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | Bootstrap Template 机制（本地 Fork 特性） | `s-boot` |
| 31 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | basebackup：无状态 Compute 的冷启动包 | `s-basebackup` |
| 32 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | ComputeSpec：一份「期望状态」文档，热加载不重启 | `s-compute-spec` |
| 33 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | lakebase_mode：Databricks 托管形态总开关 | `s-lakebase` |
| 34 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | LFC：Local File Cache | `s-lfc` |
| 35 | 04 组件逐层拆解：读写路径贯穿 | COMPUTE | DDL Forwarding：库/角色变更实时联动控制面 | `s-ddl-fwd` |
| 36 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | WAL 服务：Paxos-like 复制 | `s-sk1` |
| 37 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 的 6 个持久 LSN + 1 个派生值 | `s-lsn` |
| 38 | 04 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | SK 成员迁移：generation 双阶段递增（RFC 035） | `s-sk-migrate` |
| 39 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 侧关键 LSN（timeline.rs / models.rs） | `s-ps-lsn` |
| 40 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver — 存储引擎核心 | `s-ps1` |
| 41 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | 多租户模型：Tenant / Timeline | `s-ps-model` |
| 42 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | Layer 文件：不可变的两级 LSM | `s-ps-layer` |
| 43 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | 写入缓冲 InMemoryLayer：pageserver 的 MemTable | `s-ps-inmem` |
| 44 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | S3 上怎么区分 L0 / L1：光看文件名就够了 | `s-ps-layer-name` |
| 45 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | LayerMap：(Key, LSN) 二维查找索引 | `s-layermap` |
| 46 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | index_part.json：远端 timeline 的权威清单 | `s-indexpart` |
| 47 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | PS 本地 tenant 目录：config-v1 逐段解码 | `s-tenant-dir` |
| 48 | 04 组件逐层拆解：读写路径贯穿 | PAGESERVER | heatmap-v1.json：attached 端产，secondary 端用 | `s-heatmap` |
| 49 | 04 组件逐层拆解：读写路径贯穿 | 读路径 | Page → LSN：Compute 怎么知道该用什么 LSN 请求 | `s-read-lsn` |
| 50 | 04 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Broker & Storage Controller | `s-bc` |
| 51 | 04 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Controller 的元数据表（依赖一套独立 PG） | `s-storcon-schema` |
| 52 | **05 核心原理深度剖析** | 分节页 | — | `s-div4` |
| 53 | 05 核心原理深度剖析 | PAGESERVER | 为什么 S3 有延迟：Ephemeral Layer 的滚动策略 | `s-flush-policy` |
| 54 | 05 核心原理深度剖析 | PAGESERVER | L0 什么时候变成 L1：计数阈值 + 事件驱动 | `s-l0-compact-trigger` |
| 55 | 05 核心原理深度剖析 | PAGESERVER | 一条 WAL 的完整生命周期：8 个 LSN 检查点 | `s-lsn-chain` |
| 56 | 05 核心原理深度剖析 | PAGESERVER | WAL Redo：每租户独立的 seccomp 沙箱 | `s-walredo` |
| 57 | 05 核心原理深度剖析 | PAGESERVER | 沙箱边界细节：seccomp 白名单、加固与逃逸风险 | `s-walredo-sec` |
| 58 | 05 核心原理深度剖析 | 全链路 | 背压：三层限速把写入速度钉在存储能力上 | `s-bp` |
| 59 | 05 核心原理深度剖析 | PAGESERVER | Compaction & GC 关键参数 | `s-compact` |
| 60 | 05 核心原理深度剖析 | PAGESERVER | Timeline / 分支 GC：谁能被回收 | `s-gc` |
| 61 | 05 核心原理深度剖析 | PAGESERVER | History Window 配在哪：一路从控制台落到 pageserver 的 GC | `s-pitr-cfg` |
| 62 | 05 核心原理深度剖析 | PAGESERVER | Sharding & Generation Number | `s-shard` |
| 63 | 05 核心原理深度剖析 | PAGESERVER | Secondary Location：热备用的只读缓存 | `s-secondary` |
| 64 | 05 核心原理深度剖析 | 协调层 | 如何防止 Compute / Pageserver 脑裂 | `s-splitbrain` |
| 65 | **06 标志性能力实现** | 分节页 | — | `s-div5` |
| 66 | 06 标志性能力实现 | BRANCHING | Copy-on-Write 分支 —— Neon 的杀手锏 | `s-branch1` |
| 67 | 06 标志性能力实现 | BRANCHING | CoW 分支 vs 传统快照 | `s-branch2` |
| 68 | 06 标志性能力实现 | BRANCHING | Synthetic Size：与物理布局解耦的计费 | `s-synsize` |
| 69 | 06 标志性能力实现 | BRANCHING | 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现） | `s-schema-diff` |
| 70 | 06 标志性能力实现 | BRANCHING | Time Travel：查询「过去某一刻」的数据库 | `s-time-travel` |
| 71 | 06 标志性能力实现 | PROXY | wake_compute：从「连接请求」到「一台活着的 Postgres」 | `s-wake` |
| 72 | 06 标志性能力实现 | 核心卖点 | Scale-to-Zero：闲置即销毁 | `s-s2z` |
| 73 | 06 标志性能力实现 | 核心卖点 | Autoscaling：三个组件，一套 goal-CU 算法 | `s-auto` |
| 74 | 06 标志性能力实现 | 核心卖点 | 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀 | `s-auto-nego` |
| 75 | 06 标志性能力实现 | 存储底座 | 多云对象存储支持 | `s-cloud` |
| 76 | **07 运维·限制·对比·落地** | 分节页 | — | `s-div6` |
| 77 | 07 运维·限制·对比·落地 | 数字 | 关键参数一览 | `s-numbers` |
| 78 | 07 运维·限制·对比·落地 | COMPUTE | 读懂 compute 日志：四类方括号前缀 | `s-log-prefix` |
| 79 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 周期任务清单：以 timeline_manager 为调度中枢 | `s-sk-tasks` |
| 80 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound | `s-sk-logs` |
| 81 | 07 运维·限制·对比·落地 | SAFEKEEPER | 不启 compute 怎么测 SK 的 WAL 读写：三条路 | `s-sk-notest` |
| 82 | 07 运维·限制·对比·落地 | PAGESERVER | pageserver 周期任务清单：per-tenant 三件套 + 进程级全局 | `s-ps-tasks` |
| 83 | 07 运维·限制·对比·落地 | PAGESERVER | 读懂 pageserver 日志：稳态刷屏行逐条解码 | `s-ps-logs` |
| 84 | 07 运维·限制·对比·落地 | PAGESERVER | 不启 compute 怎么测 PS 的页面读写：读端天生可裸测 | `s-ps-notest` |
| 85 | 07 运维·限制·对比·落地 | 可观测 | 关键指标：从背压到冷启动，看哪几个数就够 | `s-metrics` |
| 86 | 07 运维·限制·对比·落地 | 故障演练 | 两个典型故障：SK 单点宕机 / PS 实例宕机 | `s-failure` |
| 87 | 07 运维·限制·对比·落地 | 局限 | 架构局限 & Tradeoff：清醒地知道边界在哪 | `s-tradeoff` |
| 88 | 07 运维·限制·对比·落地 | 开发方向 | 近期 Git 历史脉络（本 Fork） | `s-dev` |
| 89 | 07 运维·限制·对比·落地 | 源码 | 想深挖？从这里开始 | `s-src` |
| 90 | 07 运维·限制·对比·落地 | 总结 | Neon 的核心设计哲学 | `s-sum` |
| 91 | 07 运维·限制·对比·落地 | — | Thank You | `s-end` |

## 按分类归组

- **PAGESERVER**（23 页）：39 Pageserver 侧关键 LSN（timeline.rs / models.rs）、40 Pageserver — 存储引擎核心、41 多租户模型：Tenant / Timeline、42 Layer 文件：不可变的两级 LSM、43 写入缓冲 InMemoryLayer：pageserver 的 MemTable、44 S3 上怎么区分 L0 / L1：光看文件名就够了、45 LayerMap：(Key, LSN) 二维查找索引、46 index_part.json：远端 timeline 的权威清单、47 PS 本地 tenant 目录：config-v1 逐段解码、48 heatmap-v1.json：attached 端产，secondary 端用、53 为什么 S3 有延迟：Ephemeral Layer 的滚动策略、54 L0 什么时候变成 L1：计数阈值 + 事件驱动、55 一条 WAL 的完整生命周期：8 个 LSN 检查点、56 WAL Redo：每租户独立的 seccomp 沙箱、57 沙箱边界细节：seccomp 白名单、加固与逃逸风险、59 Compaction & GC 关键参数、60 Timeline / 分支 GC：谁能被回收、61 History Window 配在哪：一路从控制台落到 pageserver 的 GC、62 Sharding & Generation Number、63 Secondary Location：热备用的只读缓存、82 pageserver 周期任务清单：per-tenant 三件套 + 进程级全局、83 读懂 pageserver 日志：稳态刷屏行逐条解码、84 不启 compute 怎么测 PS 的页面读写：读端天生可裸测
- **COMPUTE**（13 页）：24 Compute Node — patched PostgreSQL 的四点关键改动、25 compute_ctl —— compute 容器里的 PostgreSQL 监护进程、26 内部端口 3081 —— 4 个路由，两类调用方、27 Compute VM 里都有哪些常驻进程、28 compute_ctl 状态机 —— ComputeStatus 全 11 态、29 POST /configure 之后：compute_ctl 与 PG 的这 2 秒、30 Bootstrap Template 机制（本地 Fork 特性）、31 basebackup：无状态 Compute 的冷启动包、32 ComputeSpec：一份「期望状态」文档，热加载不重启、33 lakebase_mode：Databricks 托管形态总开关、34 LFC：Local File Cache、35 DDL Forwarding：库/角色变更实时联动控制面、78 读懂 compute 日志：四类方括号前缀
- **SAFEKEEPER**（6 页）：36 WAL 服务：Paxos-like 复制、37 Safekeeper 的 6 个持久 LSN + 1 个派生值、38 SK 成员迁移：generation 双阶段递增（RFC 035）、79 safekeeper 周期任务清单：以 timeline_manager 为调度中枢、80 safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound、81 不启 compute 怎么测 SK 的 WAL 读写：三条路
- **PROXY**（5 页）：14 连接代理：路由 + 认证 + Serverless 网关、15 连上 Neon：Proxy 怎么知道你要连哪个库、16 neon_proxy_params_compat：启动参数透传的兼容开关、17 Proxy 为什么依赖 Redis：无状态集群的共享短时状态层、71 wake_compute：从「连接请求」到「一台活着的 Postgres」
- **PROXY · TLS**（5 页）：18 Neon 的 TLS：两跳加密，两套证书、19 客户端握手：SSLRequest 升级，或直接开打 TLS、20 CertResolver：一张通配证，按 SNI 剥域名匹配、21 SCRAM Channel Binding：把认证钉在这张叶子证上、23 pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界
- **BRANCHING**（5 页）：66 Copy-on-Write 分支 —— Neon 的杀手锏、67 CoW 分支 vs 传统快照、68 Synthetic Size：与物理布局解耦的计费、69 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现）、70 Time Travel：查询「过去某一刻」的数据库
- **协调层**（3 页）：50 Storage Broker & Storage Controller、51 Storage Controller 的元数据表（依赖一套独立 PG）、64 如何防止 Compute / Pageserver 脑裂
- **核心卖点**（3 页）：72 Scale-to-Zero：闲置即销毁、73 Autoscaling：三个组件，一套 goal-CU 算法、74 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀
- **定位**（2 页）：5 Neon vs 传统 PostgreSQL：核心区别、6 核心定位与核心价值
- **读路径**（2 页）：12 一次 SELECT 的旅程、49 Page → LSN：Compute 怎么知道该用什么 LSN 请求
- **目录**（1 页）：2 大章节总览
- **理论基石**（1 页）：4 “The log is the database.” — Aurora, SIGMOD 2017
- **组件总览**（1 页）：8 六大核心组件
- **架构**（1 页）：9 端到端数据流拓扑
- **写路径**（1 页）：11 一次 INSERT 的旅程
- **COMPUTE · TLS**（1 页）：22 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres
- **全链路**（1 页）：58 背压：三层限速把写入速度钉在存储能力上
- **存储底座**（1 页）：75 多云对象存储支持
- **数字**（1 页）：77 关键参数一览
- **可观测**（1 页）：85 关键指标：从背压到冷启动，看哪几个数就够
- **故障演练**（1 页）：86 两个典型故障：SK 单点宕机 / PS 实例宕机
- **局限**（1 页）：87 架构局限 & Tradeoff：清醒地知道边界在哪
- **开发方向**（1 页）：88 近期 Git 历史脉络（本 Fork）
- **源码**（1 页）：89 想深挖？从这里开始
- **总结**（1 页）：90 Neon 的核心设计哲学
