# Neon 架构解析 · 幻灯片索引

由 `gen_neon_bento.py` 自动生成，请勿手改；改动幻灯片后重新运行生成脚本即可刷新。

- 总页数：**116**
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
| 13 | **04 标志性能力实现** | 分节页 | — | `s-div5` |
| 14 | 04 标志性能力实现 | BRANCHING | Copy-on-Write 分支 —— Neon 的杀手锏 | `s-branch1` |
| 15 | 04 标志性能力实现 | BRANCHING | CoW 分支 vs 传统快照 | `s-branch2` |
| 16 | 04 标志性能力实现 | BRANCHING | Synthetic Size：与物理布局解耦的计费 | `s-synsize` |
| 17 | 04 标志性能力实现 | BRANCHING | 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现） | `s-schema-diff` |
| 18 | 04 标志性能力实现 | BRANCHING | Time Travel：查询「过去某一刻」的数据库 | `s-time-travel` |
| 19 | 04 标志性能力实现 | PROXY | wake_compute：从「连接请求」到「一台活着的 Postgres」 | `s-wake` |
| 20 | 04 标志性能力实现 | 核心卖点 | Scale-to-Zero：闲置即销毁 | `s-s2z` |
| 21 | 04 标志性能力实现 | 核心卖点 | Autoscaling：三个组件，一套 goal-CU 算法 | `s-auto` |
| 22 | 04 标志性能力实现 | 核心卖点 | 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀 | `s-auto-nego` |
| 23 | 04 标志性能力实现 | 存储底座 | 多云对象存储支持 | `s-cloud` |
| 24 | **05 组件逐层拆解：读写路径贯穿** | 分节页 | — | `s-div3` |
| 25 | 05 组件逐层拆解：读写路径贯穿 | PROXY | 连接代理：路由 + 认证 + Serverless 网关 | `s-proxy` |
| 26 | 05 组件逐层拆解：读写路径贯穿 | PROXY | proxy 子系统内部架构 | `s-proxy-arch` |
| 27 | 05 组件逐层拆解：读写路径贯穿 | PROXY | 连上 Neon：Proxy 怎么知道你要连哪个库 | `s-conn-route` |
| 28 | 05 组件逐层拆解：读写路径贯穿 | PROXY | neon_proxy_params_compat：启动参数透传的兼容开关 | `s-params-compat` |
| 29 | 05 组件逐层拆解：读写路径贯穿 | PROXY | Proxy 为什么依赖 Redis：无状态集群的共享短时状态层 | `s-proxy-redis` |
| 30 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | Neon 的 TLS：两跳加密，两套证书 | `s-tls-overview` |
| 31 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | 客户端握手：SSLRequest 升级，或直接开打 TLS | `s-tls-handshake` |
| 32 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | CertResolver：一张通配证，按 SNI 剥域名匹配 | `s-tls-cert` |
| 33 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | SCRAM Channel Binding：把认证钉在这张叶子证上 | `s-tls-cbind` |
| 34 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE · TLS | 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres | `s-tls-compute` |
| 35 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界 | `s-tls-router` |
| 36 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute Node — patched PostgreSQL 的四点关键改动 | `s-comp1` |
| 37 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内核存算分离改动 · Compute 侧（改 PG 源码） | `s-core-compute` |
| 38 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内核存算分离改动 · WAL redo 进程 & 其它兼容 | `s-core-walredo` |
| 39 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 扩展打包 patch（compute/patches/ · 构建期打） | `s-ext-patches` |
| 40 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl —— compute 容器里的 PostgreSQL 监护进程 | `s-computectl` |
| 41 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内部端口 3081 —— 4 个路由，两类调用方 | `s-cc-internal` |
| 42 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute VM 里都有哪些常驻进程 | `s-cc-procs` |
| 43 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl 状态机 —— ComputeStatus 全 11 态 | `s-comp-sm` |
| 44 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | POST /configure 之后：compute_ctl 与 PG 的这 2 秒 | `s-cfg-seq` |
| 45 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Bootstrap Template 机制（本地 Fork 特性） | `s-boot` |
| 46 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | basebackup：无状态 Compute 的冷启动包 | `s-basebackup` |
| 47 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | ComputeSpec：一份「期望状态」文档，热加载不重启 | `s-compute-spec` |
| 48 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | lakebase_mode：Databricks 托管形态总开关 | `s-lakebase` |
| 49 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | LFC：Local File Cache | `s-lfc` |
| 50 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | DDL Forwarding：库/角色变更实时联动控制面 | `s-ddl-fwd` |
| 51 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | WAL 服务：Paxos-like 复制 | `s-sk1` |
| 52 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 子系统内部架构 | `s-sk-arch` |
| 53 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 的 6 个持久 LSN + 1 个派生值 | `s-lsn` |
| 54 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | SK 成员迁移：generation 双阶段递增（RFC 035） | `s-sk-migrate` |
| 55 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver — 存储引擎核心 | `s-ps1` |
| 56 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 子系统内部架构 | `s-ps-arch` |
| 57 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 侧关键 LSN（timeline.rs / models.rs） | `s-ps-lsn` |
| 58 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | 多租户模型：Tenant / Timeline | `s-ps-model` |
| 59 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 存储引擎：LSM-like 分层总览 | `s-ps-lsm` |
| 60 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Layer 文件：不可变的两级 LSM | `s-ps-layer` |
| 61 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | 写入缓冲 InMemoryLayer：pageserver 的 MemTable | `s-ps-inmem` |
| 62 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | S3 上怎么区分 L0 / L1：光看文件名就够了 | `s-ps-layer-name` |
| 63 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | LayerMap：(Key, LSN) 二维查找索引 | `s-layermap` |
| 64 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | index_part.json：远端 timeline 的权威清单 | `s-indexpart` |
| 65 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | PS 本地 tenant 目录：config-v1 逐段解码 | `s-tenant-dir` |
| 66 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | heatmap-v1.json：attached 端产，secondary 端用 | `s-heatmap` |
| 67 | 05 组件逐层拆解：读写路径贯穿 | 读路径 | Page → LSN：Compute 怎么知道该用什么 LSN 请求 | `s-read-lsn` |
| 68 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Broker & Storage Controller | `s-bc` |
| 69 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_broker 子系统内部架构 | `s-broker-arch` |
| 70 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_controller 子系统内部架构 | `s-storcon-arch` |
| 71 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Controller 的元数据表（依赖一套独立 PG） | `s-storcon-schema` |
| 72 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | 如何防止 Compute / Pageserver 脑裂 | `s-splitbrain` |
| 73 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_scrubber：S3 的对账人与清道夫 | `s-scrubber` |
| 74 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_scrubber 子系统内部架构 | `s-scrubber-arch` |
| 75 | **06 核心原理深度剖析** | 分节页 | — | `s-div4` |
| 76 | 06 核心原理深度剖析 | PAGESERVER | 一条 WAL 的完整生命周期：8 个 LSN 检查点 | `s-lsn-chain` |
| 77 | 06 核心原理深度剖析 | COMPUTE | Neon 也有 checkpoint 吗：有，但分裂成两个层面 | `s-checkpoint` |
| 78 | 06 核心原理深度剖析 | PAGESERVER | 为什么 S3 有延迟：Ephemeral Layer 的滚动策略 | `s-flush-policy` |
| 79 | 06 核心原理深度剖析 | PAGESERVER | L0 什么时候变成 L1：计数阈值 + 事件驱动 | `s-l0-compact-trigger` |
| 80 | 06 核心原理深度剖析 | PAGESERVER | Compaction & GC 关键参数 | `s-compact` |
| 81 | 06 核心原理深度剖析 | PAGESERVER | Timeline / 分支 GC：谁能被回收 | `s-gc` |
| 82 | 06 核心原理深度剖析 | PAGESERVER | History Window 配在哪：一路从控制台落到 pageserver 的 GC | `s-pitr-cfg` |
| 83 | 06 核心原理深度剖析 | 全链路 | 背压：三层限速把写入速度钉在存储能力上 | `s-bp` |
| 84 | 06 核心原理深度剖析 | PAGESERVER | WAL Redo：每租户独立的 seccomp 沙箱 | `s-walredo` |
| 85 | 06 核心原理深度剖析 | PAGESERVER | 沙箱边界细节：seccomp 白名单、加固与逃逸风险 | `s-walredo-sec` |
| 86 | 06 核心原理深度剖析 | PAGESERVER | Sharding & Generation Number | `s-shard` |
| 87 | 06 核心原理深度剖析 | PAGESERVER | Secondary Location：热备用的只读缓存 | `s-secondary` |
| 88 | **07 运维·限制·对比·落地** | 分节页 | — | `s-div6` |
| 89 | 07 运维·限制·对比·落地 | 数字 | 关键参数一览 | `s-numbers` |
| 90 | 07 运维·限制·对比·落地 | COMPUTE | 读懂 compute 日志：四类方括号前缀 | `s-log-prefix` |
| 91 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 周期任务清单：以 timeline_manager 为调度中枢 | `s-sk-tasks` |
| 92 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound | `s-sk-logs` |
| 93 | 07 运维·限制·对比·落地 | SAFEKEEPER | 不启 compute 怎么测 SK 的 WAL 读写：三条路 | `s-sk-notest` |
| 94 | 07 运维·限制·对比·落地 | PAGESERVER | pageserver 周期任务清单：per-tenant 三件套 + 进程级全局 | `s-ps-tasks` |
| 95 | 07 运维·限制·对比·落地 | PAGESERVER | 读懂 pageserver 日志：稳态刷屏行逐条解码 | `s-ps-logs` |
| 96 | 07 运维·限制·对比·落地 | PAGESERVER | 不启 compute 怎么测 PS 的页面读写：读端天生可裸测 | `s-ps-notest` |
| 97 | 07 运维·限制·对比·落地 | 可观测 | 关键指标：从背压到冷启动，看哪几个数就够 | `s-metrics` |
| 98 | 07 运维·限制·对比·落地 | 故障演练 | 两个典型故障：SK 单点宕机 / PS 实例宕机 | `s-failure` |
| 99 | 07 运维·限制·对比·落地 | 故障切换 | Pageserver 故障切换流程：从失联到读恢复 | `s-ps-failover` |
| 100 | 07 运维·限制·对比·落地 | 故障切换 | Compute 故障自愈：Node 静默宕机后的一次连接失败即恢复 | `s-compute-selfheal` |
| 101 | 07 运维·限制·对比·落地 | 故障切换 | Safekeeper 空盘重建：pull_timeline 把 WAL 拷回 | `s-sk-rebuild` |
| 102 | 07 运维·限制·对比·落地 | 备份恢复 | Neon 要不要备份：内建持久化 vs 仍需外部备份 | `s-backup` |
| 103 | 07 运维·限制·对比·落地 | 备份恢复 | 裸备份 S3 的陷阱：layer 文件离不开平台元数据 | `s-backup-meta` |
| 104 | 07 运维·限制·对比·落地 | 备份恢复 | Neon 官方的三条备份策略：不是「每分支 pg_dump」 | `s-backup-official` |
| 105 | 07 运维·限制·对比·落地 | 备份恢复 | 想物理快照 S3？光「停 GC」不够，要冻结全部写入 | `s-backup-freeze` |
| 106 | 07 运维·限制·对比·落地 | 备份恢复 | 创建「指定 LSN 的 root」：没有专用接口，两步拼出来 | `s-root-at-lsn` |
| 107 | 07 运维·限制·对比·落地 | 备份恢复 | root restore 后，子分支怎么办：v1 的 reparent 分流 | `s-reparent` |
| 108 | 07 运维·限制·对比·落地 | 备份恢复 | detach_ancestor 用 v1 还是 v2：多数 v1，PITR 外恢复需 v2 | `s-detach-v1v2` |
| 109 | 07 运维·限制·对比·落地 | 备份恢复 | v2 的用武之地：多级链扁平化，与 PITR 外恢复借锚点分支 | `s-detach-v2-case` |
| 110 | 07 运维·限制·对比·落地 | 备份恢复 | detach_ancestor 后，S3 上两个 root 存两份还是一份？ | `s-detach-storage` |
| 111 | 07 运维·限制·对比·落地 | 备份恢复 | role/database 归谁：spec（薄）vs LSN 快照（数据） | `s-role-db-backup` |
| 112 | 07 运维·限制·对比·落地 | 局限 | 架构局限 & Tradeoff：清醒地知道边界在哪 | `s-tradeoff` |
| 113 | 07 运维·限制·对比·落地 | 开发方向 | 近期 Git 历史脉络（本 Fork） | `s-dev` |
| 114 | 07 运维·限制·对比·落地 | 源码 | 想深挖？从这里开始 | `s-src` |
| 115 | 07 运维·限制·对比·落地 | 总结 | Neon 的核心设计哲学 | `s-sum` |
| 116 | 07 运维·限制·对比·落地 | — | Thank You | `s-end` |

## 按分类归组

- **PAGESERVER**（25 页）：55 Pageserver — 存储引擎核心、56 Pageserver 子系统内部架构、57 Pageserver 侧关键 LSN（timeline.rs / models.rs）、58 多租户模型：Tenant / Timeline、59 Pageserver 存储引擎：LSM-like 分层总览、60 Layer 文件：不可变的两级 LSM、61 写入缓冲 InMemoryLayer：pageserver 的 MemTable、62 S3 上怎么区分 L0 / L1：光看文件名就够了、63 LayerMap：(Key, LSN) 二维查找索引、64 index_part.json：远端 timeline 的权威清单、65 PS 本地 tenant 目录：config-v1 逐段解码、66 heatmap-v1.json：attached 端产，secondary 端用、76 一条 WAL 的完整生命周期：8 个 LSN 检查点、78 为什么 S3 有延迟：Ephemeral Layer 的滚动策略、79 L0 什么时候变成 L1：计数阈值 + 事件驱动、80 Compaction & GC 关键参数、81 Timeline / 分支 GC：谁能被回收、82 History Window 配在哪：一路从控制台落到 pageserver 的 GC、84 WAL Redo：每租户独立的 seccomp 沙箱、85 沙箱边界细节：seccomp 白名单、加固与逃逸风险、86 Sharding & Generation Number、87 Secondary Location：热备用的只读缓存、94 pageserver 周期任务清单：per-tenant 三件套 + 进程级全局、95 读懂 pageserver 日志：稳态刷屏行逐条解码、96 不启 compute 怎么测 PS 的页面读写：读端天生可裸测
- **COMPUTE**（17 页）：36 Compute Node — patched PostgreSQL 的四点关键改动、37 内核存算分离改动 · Compute 侧（改 PG 源码）、38 内核存算分离改动 · WAL redo 进程 & 其它兼容、39 扩展打包 patch（compute/patches/ · 构建期打）、40 compute_ctl —— compute 容器里的 PostgreSQL 监护进程、41 内部端口 3081 —— 4 个路由，两类调用方、42 Compute VM 里都有哪些常驻进程、43 compute_ctl 状态机 —— ComputeStatus 全 11 态、44 POST /configure 之后：compute_ctl 与 PG 的这 2 秒、45 Bootstrap Template 机制（本地 Fork 特性）、46 basebackup：无状态 Compute 的冷启动包、47 ComputeSpec：一份「期望状态」文档，热加载不重启、48 lakebase_mode：Databricks 托管形态总开关、49 LFC：Local File Cache、50 DDL Forwarding：库/角色变更实时联动控制面、77 Neon 也有 checkpoint 吗：有，但分裂成两个层面、90 读懂 compute 日志：四类方括号前缀
- **备份恢复**（10 页）：102 Neon 要不要备份：内建持久化 vs 仍需外部备份、103 裸备份 S3 的陷阱：layer 文件离不开平台元数据、104 Neon 官方的三条备份策略：不是「每分支 pg_dump」、105 想物理快照 S3？光「停 GC」不够，要冻结全部写入、106 创建「指定 LSN 的 root」：没有专用接口，两步拼出来、107 root restore 后，子分支怎么办：v1 的 reparent 分流、108 detach_ancestor 用 v1 还是 v2：多数 v1，PITR 外恢复需 v2、109 v2 的用武之地：多级链扁平化，与 PITR 外恢复借锚点分支、110 detach_ancestor 后，S3 上两个 root 存两份还是一份？、111 role/database 归谁：spec（薄）vs LSN 快照（数据）
- **SAFEKEEPER**（7 页）：51 WAL 服务：Paxos-like 复制、52 Safekeeper 子系统内部架构、53 Safekeeper 的 6 个持久 LSN + 1 个派生值、54 SK 成员迁移：generation 双阶段递增（RFC 035）、91 safekeeper 周期任务清单：以 timeline_manager 为调度中枢、92 safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound、93 不启 compute 怎么测 SK 的 WAL 读写：三条路
- **协调层**（7 页）：68 Storage Broker & Storage Controller、69 storage_broker 子系统内部架构、70 storage_controller 子系统内部架构、71 Storage Controller 的元数据表（依赖一套独立 PG）、72 如何防止 Compute / Pageserver 脑裂、73 storage_scrubber：S3 的对账人与清道夫、74 storage_scrubber 子系统内部架构
- **PROXY**（6 页）：19 wake_compute：从「连接请求」到「一台活着的 Postgres」、25 连接代理：路由 + 认证 + Serverless 网关、26 proxy 子系统内部架构、27 连上 Neon：Proxy 怎么知道你要连哪个库、28 neon_proxy_params_compat：启动参数透传的兼容开关、29 Proxy 为什么依赖 Redis：无状态集群的共享短时状态层
- **BRANCHING**（5 页）：14 Copy-on-Write 分支 —— Neon 的杀手锏、15 CoW 分支 vs 传统快照、16 Synthetic Size：与物理布局解耦的计费、17 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现）、18 Time Travel：查询「过去某一刻」的数据库
- **PROXY · TLS**（5 页）：30 Neon 的 TLS：两跳加密，两套证书、31 客户端握手：SSLRequest 升级，或直接开打 TLS、32 CertResolver：一张通配证，按 SNI 剥域名匹配、33 SCRAM Channel Binding：把认证钉在这张叶子证上、35 pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界
- **核心卖点**（3 页）：20 Scale-to-Zero：闲置即销毁、21 Autoscaling：三个组件，一套 goal-CU 算法、22 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀
- **故障切换**（3 页）：99 Pageserver 故障切换流程：从失联到读恢复、100 Compute 故障自愈：Node 静默宕机后的一次连接失败即恢复、101 Safekeeper 空盘重建：pull_timeline 把 WAL 拷回
- **定位**（2 页）：5 Neon vs 传统 PostgreSQL：核心区别、6 核心定位与核心价值
- **读路径**（2 页）：12 一次 SELECT 的旅程、67 Page → LSN：Compute 怎么知道该用什么 LSN 请求
- **目录**（1 页）：2 大章节总览
- **理论基石**（1 页）：4 “The log is the database.” — Aurora, SIGMOD 2017
- **组件总览**（1 页）：8 六大核心组件
- **架构**（1 页）：9 端到端数据流拓扑
- **写路径**（1 页）：11 一次 INSERT 的旅程
- **存储底座**（1 页）：23 多云对象存储支持
- **COMPUTE · TLS**（1 页）：34 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres
- **全链路**（1 页）：83 背压：三层限速把写入速度钉在存储能力上
- **数字**（1 页）：89 关键参数一览
- **可观测**（1 页）：97 关键指标：从背压到冷启动，看哪几个数就够
- **故障演练**（1 页）：98 两个典型故障：SK 单点宕机 / PS 实例宕机
- **局限**（1 页）：112 架构局限 & Tradeoff：清醒地知道边界在哪
- **开发方向**（1 页）：113 近期 Git 历史脉络（本 Fork）
- **源码**（1 页）：114 想深挖？从这里开始
- **总结**（1 页）：115 Neon 的核心设计哲学
