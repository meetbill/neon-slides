# Neon 架构解析 · 幻灯片索引

由 `gen_neon_bento.py` 自动生成，请勿手改；改动幻灯片后重新运行生成脚本即可刷新。

- 总页数：**122**
- 生成物：`Bento_Slides.bento.html`（内嵌 `bento/slides` JSON）

| # | 章节 | 分类 | 标题 | slide id |
|---|---|---|---|---|
| 1 | 封面 | — | Neon | `cover` |
| 2 | 封面 | 目录 | 大章节总览 | `s-toc` |
| 3 | **01 背景痛点** | 分节页 | — | `s-div1` |
| 4 | 01 背景痛点 | 理论基石 | “The log is the database.” — Aurora, SIGMOD 2017 | `s-log-is-db` |
| 5 | 01 背景痛点 | 定位 | Neon vs 传统 PostgreSQL：核心区别 | `s-position` |
| 6 | 01 背景痛点 | 定位 | 对比：Neon vs 阿里云 PolarDB-PG vs 腾讯云 TDSQL-C PG | `s-cloud-compare` |
| 7 | 01 背景痛点 | 定位 | 核心定位与核心价值 | `s-goals` |
| 8 | **02 顶层架构总览** | 分节页 | — | `s-div2` |
| 9 | 02 顶层架构总览 | 组件总览 | 六大核心组件 | `s-topo` |
| 10 | 02 顶层架构总览 | 架构 | 端到端数据流拓扑 | `s-arch` |
| 11 | **03 核心数据流：写路径 + 读路径** | 分节页 | — | `s-div-flow` |
| 12 | 03 核心数据流：写路径 + 读路径 | 写路径 | 一次 INSERT 的旅程 | `s-write` |
| 13 | 03 核心数据流：写路径 + 读路径 | 读路径 | 一次 SELECT 的旅程 | `s-read` |
| 14 | **04 标志性能力实现** | 分节页 | — | `s-div5` |
| 15 | 04 标志性能力实现 | BRANCHING | Copy-on-Write 分支 —— Neon 的杀手锏 | `s-branch1` |
| 16 | 04 标志性能力实现 | BRANCHING | CoW 分支 vs 传统快照 | `s-branch2` |
| 17 | 04 标志性能力实现 | BRANCHING | Synthetic Size：与物理布局解耦的计费 | `s-synsize` |
| 18 | 04 标志性能力实现 | BRANCHING | 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现） | `s-schema-diff` |
| 19 | 04 标志性能力实现 | BRANCHING | Time Travel：查询「过去某一刻」的数据库 | `s-time-travel` |
| 20 | 04 标志性能力实现 | PROXY | wake_compute：从「连接请求」到「一台活着的 Postgres」 | `s-wake` |
| 21 | 04 标志性能力实现 | 核心卖点 | Scale-to-Zero：闲置即销毁 | `s-s2z` |
| 22 | 04 标志性能力实现 | 核心卖点 | Autoscaling：三个组件，一套 goal-CU 算法 | `s-auto` |
| 23 | 04 标志性能力实现 | 核心卖点 | 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀 | `s-auto-nego` |
| 24 | 04 标志性能力实现 | 存储底座 | 多云对象存储支持 | `s-cloud` |
| 25 | **05 组件逐层拆解：读写路径贯穿** | 分节页 | — | `s-div3` |
| 26 | 05 组件逐层拆解：读写路径贯穿 | PROXY | 连接代理：路由 + 认证 + Serverless 网关 | `s-proxy` |
| 27 | 05 组件逐层拆解：读写路径贯穿 | PROXY | proxy 子系统内部架构 | `s-proxy-arch` |
| 28 | 05 组件逐层拆解：读写路径贯穿 | PROXY | 连上 Neon：Proxy 怎么知道你要连哪个库 | `s-conn-route` |
| 29 | 05 组件逐层拆解：读写路径贯穿 | PROXY | neon_proxy_params_compat：启动参数透传的兼容开关 | `s-params-compat` |
| 30 | 05 组件逐层拆解：读写路径贯穿 | PROXY | Proxy 为什么依赖 Redis：无状态集群的共享短时状态层 | `s-proxy-redis` |
| 31 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | Neon 的 TLS：两跳加密，两套证书 | `s-tls-overview` |
| 32 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | 客户端握手：SSLRequest 升级，或直接开打 TLS | `s-tls-handshake` |
| 33 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | CertResolver：一张通配证，按 SNI 剥域名匹配 | `s-tls-cert` |
| 34 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | SCRAM Channel Binding：把认证钉在这张叶子证上 | `s-tls-cbind` |
| 35 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE · TLS | 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres | `s-tls-compute` |
| 36 | 05 组件逐层拆解：读写路径贯穿 | PROXY · TLS | pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界 | `s-tls-router` |
| 37 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute Node — patched PostgreSQL 的四点关键改动 | `s-comp1` |
| 38 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内核存算分离改动 · Compute 侧（改 PG 源码） | `s-core-compute` |
| 39 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内核存算分离改动 · WAL redo 进程 & 其它兼容 | `s-core-walredo` |
| 40 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 扩展打包 patch（compute/patches/ · 构建期打） | `s-ext-patches` |
| 41 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl —— compute 容器里的 PostgreSQL 监护进程 | `s-computectl` |
| 42 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内部端口 3081 —— 4 个路由，两类调用方 | `s-cc-internal` |
| 43 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Compute VM 里都有哪些常驻进程 | `s-cc-procs` |
| 44 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | compute_ctl 状态机 —— ComputeStatus 全 11 态 | `s-comp-sm` |
| 45 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | POST /configure 之后：compute_ctl 与 PG 的这 2 秒 | `s-cfg-seq` |
| 46 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | Bootstrap Template 机制（本地 Fork 特性） | `s-boot` |
| 47 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | basebackup：无状态 Compute 的冷启动包 | `s-basebackup` |
| 48 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | ComputeSpec：一份「期望状态」文档，热加载不重启 | `s-compute-spec` |
| 49 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | lakebase_mode：Databricks 托管形态总开关 | `s-lakebase` |
| 50 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | LFC：Local File Cache | `s-lfc` |
| 51 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | DDL Forwarding：库/角色变更实时联动控制面 | `s-ddl-fwd` |
| 52 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE | 内置 SQL 迁移：给「受管特权角色」配权限 | `s-migrations` |
| 53 | 05 组件逐层拆解：读写路径贯穿 | COMPUTE · 本地改造 | 让 Bootstrap 的 role 保住 BYPASSRLS：neon_bypassrls 豁免组 | `s-migrations-bypassrls` |
| 54 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | WAL 服务：Paxos-like 复制 | `s-sk1` |
| 55 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 子系统内部架构 | `s-sk-arch` |
| 56 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | Safekeeper 的 6 个持久 LSN + 1 个派生值 | `s-lsn` |
| 57 | 05 组件逐层拆解：读写路径贯穿 | SAFEKEEPER | SK 成员迁移：generation 双阶段递增（RFC 035） | `s-sk-migrate` |
| 58 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver — 存储引擎核心 | `s-ps1` |
| 59 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 子系统内部架构 | `s-ps-arch` |
| 60 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 侧关键 LSN（timeline.rs / models.rs） | `s-ps-lsn` |
| 61 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | 多租户模型：Tenant / Timeline | `s-ps-model` |
| 62 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Pageserver 存储引擎：LSM-like 分层总览 | `s-ps-lsm` |
| 63 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | Layer 文件：不可变的两级 LSM | `s-ps-layer` |
| 64 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | 写入缓冲 InMemoryLayer：pageserver 的 MemTable | `s-ps-inmem` |
| 65 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | S3 上怎么区分 L0 / L1：光看文件名就够了 | `s-ps-layer-name` |
| 66 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | LayerMap：(Key, LSN) 二维查找索引 | `s-layermap` |
| 67 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | index_part.json：远端 timeline 的权威清单 | `s-indexpart` |
| 68 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | PS 本地 tenant 目录：config-v1 逐段解码 | `s-tenant-dir` |
| 69 | 05 组件逐层拆解：读写路径贯穿 | PAGESERVER | heatmap-v1.json：attached 端产，secondary 端用 | `s-heatmap` |
| 70 | 05 组件逐层拆解：读写路径贯穿 | 读路径 | Page → LSN：Compute 怎么知道该用什么 LSN 请求 | `s-read-lsn` |
| 71 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Broker & Storage Controller | `s-bc` |
| 72 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_broker 子系统内部架构 | `s-broker-arch` |
| 73 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_controller 子系统内部架构 | `s-storcon-arch` |
| 74 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | Storage Controller 的元数据表（依赖一套独立 PG） | `s-storcon-schema` |
| 75 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | 如何防止 Compute / Pageserver 脑裂 | `s-splitbrain` |
| 76 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_scrubber：S3 的对账人与清道夫 | `s-scrubber` |
| 77 | 05 组件逐层拆解：读写路径贯穿 | 协调层 | storage_scrubber 子系统内部架构 | `s-scrubber-arch` |
| 78 | **06 核心原理深度剖析** | 分节页 | — | `s-div4` |
| 79 | 06 核心原理深度剖析 | PAGESERVER | 一条 WAL 的完整生命周期：8 个 LSN 检查点 | `s-lsn-chain` |
| 80 | 06 核心原理深度剖析 | COMPUTE | Neon 也有 checkpoint 吗：有，但分裂成两个层面 | `s-checkpoint` |
| 81 | 06 核心原理深度剖析 | PAGESERVER | 为什么 S3 有延迟：Ephemeral Layer 的滚动策略 | `s-flush-policy` |
| 82 | 06 核心原理深度剖析 | PAGESERVER | L0 什么时候变成 L1：计数阈值 + 事件驱动 | `s-l0-compact-trigger` |
| 83 | 06 核心原理深度剖析 | PAGESERVER | Compaction & GC 关键参数 | `s-compact` |
| 84 | 06 核心原理深度剖析 | PAGESERVER | Timeline / 分支 GC：谁能被回收 | `s-gc` |
| 85 | 06 核心原理深度剖析 | PAGESERVER | History Window 配在哪：一路从控制台落到 pageserver 的 GC | `s-pitr-cfg` |
| 86 | 06 核心原理深度剖析 | 全链路 | 背压：三层限速把写入速度钉在存储能力上 | `s-bp` |
| 87 | 06 核心原理深度剖析 | PAGESERVER | WAL Redo：每租户独立的 seccomp 沙箱 | `s-walredo` |
| 88 | 06 核心原理深度剖析 | PAGESERVER | 沙箱边界细节：seccomp 白名单、加固与逃逸风险 | `s-walredo-sec` |
| 89 | 06 核心原理深度剖析 | PAGESERVER | Sharding & Generation Number | `s-shard` |
| 90 | 06 核心原理深度剖析 | PAGESERVER | Secondary Location：热备用的只读缓存 | `s-secondary` |
| 91 | **07 运维·限制·对比·落地** | 分节页 | — | `s-div6` |
| 92 | 07 运维·限制·对比·落地 | 数字 | 关键参数一览 | `s-numbers` |
| 93 | 07 运维·限制·对比·落地 | COMPUTE | 读懂 compute 日志：四类方括号前缀 | `s-log-prefix` |
| 94 | 07 运维·限制·对比·落地 | 可观测 | compute 日志怎么导出：默认链路 + 三条通道 | `s-log-export` |
| 95 | 07 运维·限制·对比·落地 | 可观测 | 租户归属：log_line_prefix 还是 Collector 反查？ | `s-log-tenant` |
| 96 | 07 运维·限制·对比·落地 | 可观测 | Collector 放哪：控制面填地址，集群内部署 | `s-log-collector` |
| 97 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 周期任务清单：以 timeline_manager 为调度中枢 | `s-sk-tasks` |
| 98 | 07 运维·限制·对比·落地 | SAFEKEEPER | safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound | `s-sk-logs` |
| 99 | 07 运维·限制·对比·落地 | SAFEKEEPER | 不启 compute 怎么测 SK 的 WAL 读写：三条路 | `s-sk-notest` |
| 100 | 07 运维·限制·对比·落地 | PAGESERVER | pageserver 周期任务清单：per-tenant 三件套 + 进程级全局 | `s-ps-tasks` |
| 101 | 07 运维·限制·对比·落地 | PAGESERVER | 读懂 pageserver 日志：稳态刷屏行逐条解码 | `s-ps-logs` |
| 102 | 07 运维·限制·对比·落地 | PAGESERVER | 不启 compute 怎么测 PS 的页面读写：读端天生可裸测 | `s-ps-notest` |
| 103 | 07 运维·限制·对比·落地 | 可观测 | 关键指标：从背压到冷启动，看哪几个数就够 | `s-metrics` |
| 104 | 07 运维·限制·对比·落地 | 故障演练 | 两个典型故障：SK 单点宕机 / PS 实例宕机 | `s-failure` |
| 105 | 07 运维·限制·对比·落地 | 故障切换 | Pageserver 故障切换流程：从失联到读恢复 | `s-ps-failover` |
| 106 | 07 运维·限制·对比·落地 | 故障切换 | Compute 故障自愈：Node 静默宕机后的一次连接失败即恢复 | `s-compute-selfheal` |
| 107 | 07 运维·限制·对比·落地 | 故障切换 | Safekeeper 空盘重建：pull_timeline 把 WAL 拷回 | `s-sk-rebuild` |
| 108 | 07 运维·限制·对比·落地 | 备份恢复 | Neon 要不要备份：内建持久化 vs 仍需外部备份 | `s-backup` |
| 109 | 07 运维·限制·对比·落地 | 备份恢复 | 裸备份 S3 的陷阱：layer 文件离不开平台元数据 | `s-backup-meta` |
| 110 | 07 运维·限制·对比·落地 | 备份恢复 | Neon 官方的三条备份策略：不是「每分支 pg_dump」 | `s-backup-official` |
| 111 | 07 运维·限制·对比·落地 | 备份恢复 | 想物理快照 S3？光「停 GC」不够，要冻结全部写入 | `s-backup-freeze` |
| 112 | 07 运维·限制·对比·落地 | 备份恢复 | 创建「指定 LSN 的 root」：没有专用接口，两步拼出来 | `s-root-at-lsn` |
| 113 | 07 运维·限制·对比·落地 | 备份恢复 | root restore 后，子分支怎么办：v1 的 reparent 分流 | `s-reparent` |
| 114 | 07 运维·限制·对比·落地 | 备份恢复 | detach_ancestor 用 v1 还是 v2：多数 v1，PITR 外恢复需 v2 | `s-detach-v1v2` |
| 115 | 07 运维·限制·对比·落地 | 备份恢复 | v2 的用武之地：多级链扁平化，与 PITR 外恢复借锚点分支 | `s-detach-v2-case` |
| 116 | 07 运维·限制·对比·落地 | 备份恢复 | detach_ancestor 后，S3 上两个 root 存两份还是一份？ | `s-detach-storage` |
| 117 | 07 运维·限制·对比·落地 | 备份恢复 | role/database 归谁：spec（薄）vs LSN 快照（数据） | `s-role-db-backup` |
| 118 | 07 运维·限制·对比·落地 | 局限 | 架构局限 & Tradeoff：清醒地知道边界在哪 | `s-tradeoff` |
| 119 | 07 运维·限制·对比·落地 | 开发方向 | 近期 Git 历史脉络（本 Fork） | `s-dev` |
| 120 | 07 运维·限制·对比·落地 | 源码 | 想深挖？从这里开始 | `s-src` |
| 121 | 07 运维·限制·对比·落地 | 总结 | Neon 的核心设计哲学 | `s-sum` |
| 122 | 07 运维·限制·对比·落地 | — | Thank You | `s-end` |

## 按分类归组

- **PAGESERVER**（25 页）：58 Pageserver — 存储引擎核心、59 Pageserver 子系统内部架构、60 Pageserver 侧关键 LSN（timeline.rs / models.rs）、61 多租户模型：Tenant / Timeline、62 Pageserver 存储引擎：LSM-like 分层总览、63 Layer 文件：不可变的两级 LSM、64 写入缓冲 InMemoryLayer：pageserver 的 MemTable、65 S3 上怎么区分 L0 / L1：光看文件名就够了、66 LayerMap：(Key, LSN) 二维查找索引、67 index_part.json：远端 timeline 的权威清单、68 PS 本地 tenant 目录：config-v1 逐段解码、69 heatmap-v1.json：attached 端产，secondary 端用、79 一条 WAL 的完整生命周期：8 个 LSN 检查点、81 为什么 S3 有延迟：Ephemeral Layer 的滚动策略、82 L0 什么时候变成 L1：计数阈值 + 事件驱动、83 Compaction & GC 关键参数、84 Timeline / 分支 GC：谁能被回收、85 History Window 配在哪：一路从控制台落到 pageserver 的 GC、87 WAL Redo：每租户独立的 seccomp 沙箱、88 沙箱边界细节：seccomp 白名单、加固与逃逸风险、89 Sharding & Generation Number、90 Secondary Location：热备用的只读缓存、100 pageserver 周期任务清单：per-tenant 三件套 + 进程级全局、101 读懂 pageserver 日志：稳态刷屏行逐条解码、102 不启 compute 怎么测 PS 的页面读写：读端天生可裸测
- **COMPUTE**（18 页）：37 Compute Node — patched PostgreSQL 的四点关键改动、38 内核存算分离改动 · Compute 侧（改 PG 源码）、39 内核存算分离改动 · WAL redo 进程 & 其它兼容、40 扩展打包 patch（compute/patches/ · 构建期打）、41 compute_ctl —— compute 容器里的 PostgreSQL 监护进程、42 内部端口 3081 —— 4 个路由，两类调用方、43 Compute VM 里都有哪些常驻进程、44 compute_ctl 状态机 —— ComputeStatus 全 11 态、45 POST /configure 之后：compute_ctl 与 PG 的这 2 秒、46 Bootstrap Template 机制（本地 Fork 特性）、47 basebackup：无状态 Compute 的冷启动包、48 ComputeSpec：一份「期望状态」文档，热加载不重启、49 lakebase_mode：Databricks 托管形态总开关、50 LFC：Local File Cache、51 DDL Forwarding：库/角色变更实时联动控制面、52 内置 SQL 迁移：给「受管特权角色」配权限、80 Neon 也有 checkpoint 吗：有，但分裂成两个层面、93 读懂 compute 日志：四类方括号前缀
- **备份恢复**（10 页）：108 Neon 要不要备份：内建持久化 vs 仍需外部备份、109 裸备份 S3 的陷阱：layer 文件离不开平台元数据、110 Neon 官方的三条备份策略：不是「每分支 pg_dump」、111 想物理快照 S3？光「停 GC」不够，要冻结全部写入、112 创建「指定 LSN 的 root」：没有专用接口，两步拼出来、113 root restore 后，子分支怎么办：v1 的 reparent 分流、114 detach_ancestor 用 v1 还是 v2：多数 v1，PITR 外恢复需 v2、115 v2 的用武之地：多级链扁平化，与 PITR 外恢复借锚点分支、116 detach_ancestor 后，S3 上两个 root 存两份还是一份？、117 role/database 归谁：spec（薄）vs LSN 快照（数据）
- **SAFEKEEPER**（7 页）：54 WAL 服务：Paxos-like 复制、55 Safekeeper 子系统内部架构、56 Safekeeper 的 6 个持久 LSN + 1 个派生值、57 SK 成员迁移：generation 双阶段递增（RFC 035）、97 safekeeper 周期任务清单：以 timeline_manager 为调度中枢、98 safekeeper 常见刷屏日志诊断：首段未初始化 vs 预期 NotFound、99 不启 compute 怎么测 SK 的 WAL 读写：三条路
- **协调层**（7 页）：71 Storage Broker & Storage Controller、72 storage_broker 子系统内部架构、73 storage_controller 子系统内部架构、74 Storage Controller 的元数据表（依赖一套独立 PG）、75 如何防止 Compute / Pageserver 脑裂、76 storage_scrubber：S3 的对账人与清道夫、77 storage_scrubber 子系统内部架构
- **PROXY**（6 页）：20 wake_compute：从「连接请求」到「一台活着的 Postgres」、26 连接代理：路由 + 认证 + Serverless 网关、27 proxy 子系统内部架构、28 连上 Neon：Proxy 怎么知道你要连哪个库、29 neon_proxy_params_compat：启动参数透传的兼容开关、30 Proxy 为什么依赖 Redis：无状态集群的共享短时状态层
- **BRANCHING**（5 页）：15 Copy-on-Write 分支 —— Neon 的杀手锏、16 CoW 分支 vs 传统快照、17 Synthetic Size：与物理布局解耦的计费、18 分支 Schema Diff：Butterfly 的实现（Neon 上游未实现）、19 Time Travel：查询「过去某一刻」的数据库
- **PROXY · TLS**（5 页）：31 Neon 的 TLS：两跳加密，两套证书、32 客户端握手：SSLRequest 升级，或直接开打 TLS、33 CertResolver：一张通配证，按 SNI 剥域名匹配、34 SCRAM Channel Binding：把认证钉在这张叶子证上、36 pg-sni-router：嵌进主 Proxy 的运维端口，以及 sslmode 边界
- **可观测**（4 页）：94 compute 日志怎么导出：默认链路 + 三条通道、95 租户归属：log_line_prefix 还是 Collector 反查？、96 Collector 放哪：控制面填地址，集群内部署、103 关键指标：从背压到冷启动，看哪几个数就够
- **定位**（3 页）：5 Neon vs 传统 PostgreSQL：核心区别、6 对比：Neon vs 阿里云 PolarDB-PG vs 腾讯云 TDSQL-C PG、7 核心定位与核心价值
- **核心卖点**（3 页）：21 Scale-to-Zero：闲置即销毁、22 Autoscaling：三个组件，一套 goal-CU 算法、23 扩缩容前的两道关卡：调度器插槽 & vm-monitor 安全阀
- **故障切换**（3 页）：105 Pageserver 故障切换流程：从失联到读恢复、106 Compute 故障自愈：Node 静默宕机后的一次连接失败即恢复、107 Safekeeper 空盘重建：pull_timeline 把 WAL 拷回
- **读路径**（2 页）：13 一次 SELECT 的旅程、70 Page → LSN：Compute 怎么知道该用什么 LSN 请求
- **目录**（1 页）：2 大章节总览
- **理论基石**（1 页）：4 “The log is the database.” — Aurora, SIGMOD 2017
- **组件总览**（1 页）：9 六大核心组件
- **架构**（1 页）：10 端到端数据流拓扑
- **写路径**（1 页）：12 一次 INSERT 的旅程
- **存储底座**（1 页）：24 多云对象存储支持
- **COMPUTE · TLS**（1 页）：35 第二跳：compute_ctl 把内部 CA 证书塞进 Postgres
- **COMPUTE · 本地改造**（1 页）：53 让 Bootstrap 的 role 保住 BYPASSRLS：neon_bypassrls 豁免组
- **全链路**（1 页）：86 背压：三层限速把写入速度钉在存储能力上
- **数字**（1 页）：92 关键参数一览
- **故障演练**（1 页）：104 两个典型故障：SK 单点宕机 / PS 实例宕机
- **局限**（1 页）：118 架构局限 & Tradeoff：清醒地知道边界在哪
- **开发方向**（1 页）：119 近期 Git 历史脉络（本 Fork）
- **源码**（1 页）：120 想深挖？从这里开始
- **总结**（1 页）：121 Neon 的核心设计哲学
