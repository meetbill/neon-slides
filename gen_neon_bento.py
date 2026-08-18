# -*- coding: utf-8 -*-
"""Generate the Neon architecture deck as bento/slides JSON."""
import json
import math

W, H = 1280, 720
BG = "#0A1120"
BG2 = "#0D1729"
FG = "#E8EDF4"
DIM = "#9AA9BF"
FAINT = "#6B7C94"
AC = "#00E599"
AC2 = "#FF9E8A"
PANEL = "rgba(255,255,255,0.045)"
EDGE = "rgba(255,255,255,0.11)"
SANS = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
        "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif")
MONO = "'SF Mono', ui-monospace, Menlo, Consolas, 'Courier New', monospace"

# Arrow / connector strokes — single bright colour so they pop on the
# dark canvas and never blend into box borders or body text.
ARROW = "#FFD54A"                  # bright amber/yellow — reads at the back
A_NEU = ARROW
A_GRN = ARROW
A_ORG = ARROW
A_BLU = ARROW
A_PUR = ARROW
A_RED = ARROW

slides = []


def T(eid, x, y, w, h, html, fs=17, fw=500, color=FG, align="left",
      valign="top", lh=1.55, ff=SANS, **kw):
    e = dict(id=eid, type="text", x=x, y=y, w=w, h=h, rotation=0, opacity=1,
             html=html, fontSize=fs, fontFamily=ff, fontWeight=fw, color=color,
             align=align, valign=valign, lineHeight=lh)
    e.update(kw)
    return e


def R(eid, x, y, w, h, fill=PANEL, stroke=EDGE, sw=1, radius=14, **kw):
    e = dict(id=eid, type="shape", shape="rect", x=x, y=y, w=w, h=h, fill=fill,
             stroke=stroke, strokeWidth=sw, radius=radius, rotation=0, opacity=1)
    e.update(kw)
    return e


def CIRC(eid, x, y, w, h, fill=None, stroke=None, sw=2, **kw):
    e = dict(id=eid, type="shape", shape="ellipse", x=x, y=y, w=w, h=h,
             fill=fill or "rgba(0,229,153,0.14)",
             stroke=stroke or "rgba(0,229,153,0.6)",
             strokeWidth=sw, rotation=0, opacity=1, radius=0)
    e.update(kw)
    return e


def LN(eid, x, y, w, h, stroke=None, sw=2, end="arrow", dashed=False,
       thick=None, **kw):
    """Arrow from (x,y) to (x+w, y+h).

    Bento renders a line as a HORIZONTAL segment of length `w` and thickness
    `h`, then orients it via `rotation`. So w/h are NOT a delta vector: a
    vertical arrow written as w=0,h=50 has length 0 and is invisible.
    We therefore convert the caller's (dx,dy) into the renderer's
    length/thickness/rotation form. Color comes from `fill`, not `stroke`.
    """
    x1, y1 = x, y
    x2, y2 = x + w, y + h
    length = max(math.hypot(x2 - x1, y2 - y1), 1)
    t = thick or 12                      # thickness drives arrowhead size
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    color = stroke or ARROW
    e = dict(id=eid, type="shape", shape="line",
             x=round(cx - length / 2, 2), y=round(cy - t / 2, 2),
             w=round(length, 2), h=t,
             fill=color, stroke=color, strokeWidth=sw,
             rotation=round(math.degrees(math.atan2(y2 - y1, x2 - x1)), 2),
             opacity=1)
    if end:
        e["lineEnd"] = end
    if dashed:
        e["strokeStyle"] = "dashed"
    e.update(kw)
    return e


def footer(n):
    return T("footer", 96, 686, 1088, 20,
             "Neon · Serverless Postgres 架构解析　·　{{date}}　·　" + f"{n:02d} / {{{{pages:2}}}}",
             fs=12, fw=500, color=FAINT, ff=MONO, lh=1)


def kicker(txt, color=AC):
    return T("kicker", 96, 60, 900, 22, txt.upper(), fs=13, fw=700,
             color=color, ff=MONO, letterSpacing=3, role="kicker",
             fx={"enter": "fade-up", "order": 0})


def title(txt, w=1088):
    return T("stitle", 96, 88, w, 58, txt, fs=38, fw=800, color=FG, lh=1.08,
             role="title", fx={"enter": "fade-up", "order": 1})


def accent_rule():
    return R("arule", 96, 150, 60, 5, fill=AC, stroke="none", sw=0, radius=3)


def divider(sid, chapter, ttl, page):
    """Section-divider slide: chapter number + title only, minimal."""
    base(sid, [
        R("divbg", 0, 0, W, H, fill="rgba(0,229,153,0.035)", stroke="none", sw=0, radius=0),
        T("divnum", 96, 260, 1088, 90,
          f"{chapter:02d}", fs=72, fw=900, color=AC, ff=MONO, lh=1,
          fx={"enter": "fade-up", "order": 0}),
        R("divbar", 96, 356, 100, 5, fill=AC2, stroke="none", sw=0, radius=3),
        T("divttl", 96, 388, 1088, 100,
          ttl, fs=48, fw=800, color=FG, lh=1.15,
          fx={"enter": "fade-up", "order": 1}),
        footer(page),
    ], notes=f"分节页：第 {chapter} 章 {ttl}")


def base(sid, els, morph=False, bg=BG, notes=""):
    s = dict(id=sid, background=bg, transition="morph" if morph else "none",
             notes=notes, elements=els)
    slides.append(s)
    return s


def std(sid, kick, ttl, body_els, n, morph=False, notes="", tw=1088):
    els = [kicker(kick), title(ttl, tw), accent_rule()] + body_els + [footer(n)]
    base(sid, els, morph=morph, notes=notes)


def card(idp, x, y, w, h, head, lines, hc=AC, fs=15, headfs=17, gap=None):
    """A panel card with heading + body html lines."""
    els = [R(idp + "bg", x, y, w, h)]
    els.append(T(idp + "h", x + 20, y + 16, w - 40, 26, head, fs=headfs,
                 fw=800, color=hc, lh=1.1))
    body = "<br>".join(lines)
    els.append(T(idp + "b", x + 20, y + 50, w - 40, h - 62, body, fs=fs,
                 fw=500, color=DIM, lh=1.5))
    return els


# ═══════════════════════════ SLIDES ═══════════════════════════

# ─────── Slide 1: Cover ───────
p = 1
base("cover", [
    R("coverbg", 0, 0, W, H, fill="rgba(0,229,153,0.035)", stroke="none", sw=0, radius=0),
    T("cover-title", 96, 200, 1088, 180,
      "Neon",
      fs=120, fw=900, color=FG, lh=1, align="left",
      fx={"enter": "fade-up", "order": 0}),
    T("cover-sub", 96, 360, 1088, 60,
      "开源 Serverless Postgres 数据库平台",
      fs=36, fw=600, color=DIM, lh=1.3,
      fx={"enter": "fade-up", "order": 1}),
    T("cover-tag", 96, 440, 1088, 30,
      "存储计算分离 · Copy-on-Write 分支 · Scale-to-Zero",
      fs=18, fw=500, color=AC, ff=MONO, lh=1.4,
      fx={"enter": "fade-up", "order": 2}),
    R("cover-bar", 96, 510, 120, 4, fill=AC2, stroke="none", sw=0, radius=2),
    T("cover-author", 96, 540, 1088, 24,
      "作者：meetbill",
      fs=15, fw=500, color=FAINT, ff=MONO, lh=1.4,
      fx={"enter": "fade-up", "order": 3}),
    footer(p),
], notes="封面: Neon 是什么 — 开源的 Serverless Postgres 平台")


p += 1
base("s-toc", [
    kicker("目录", color=AC),
    title("大章节总览", 1088),
    accent_rule(),
    *[e for i, (num, ttl, desc) in enumerate([
        ("01", "背景痛点", "传统 PostgreSQL 的运维/扩缩容/分支痛点"),
        ("02", "顶层架构总览", "六大核心组件 + 端到端数据流拓扑"),
        ("03", "核心数据流", "一次 INSERT / SELECT 的完整旅程：写路径 + 读路径"),
        ("04", "组件逐层拆解", "Compute / Pageserver / Safekeeper，读写路径贯穿"),
        ("05", "核心原理深度剖析", "落盘策略、L0→L1、LSN 链路、沙箱、背压、GC、分片、防脑裂"),
        ("06", "标志性能力实现", "CoW 分支、Proxy、Scale-to-Zero、Autoscaling、多云存储"),
        ("07", "运维·限制·对比·落地", "关键数字、可观测、故障演练、局限 & tradeoff、总结"),
    ]) for e in (
        R(f"toc{i}bg", 96, 176 + i * 68, 1088, 58, fill="rgba(255,255,255,0.035)", stroke=EDGE, radius=10),
        T(f"toc{i}n", 116, 187 + i * 68, 70, 36, num, fs=24, fw=900, color=AC, ff=MONO),
        T(f"toc{i}t", 200, 184 + i * 68, 300, 24, ttl, fs=16.5, fw=800, color=FG),
        T(f"toc{i}d", 200, 210 + i * 68, 940, 20, desc, fs=11.5, fw=500, color=DIM),
    )],
    footer(p),
], notes="总目录：七大章节导航——背景痛点/顶层架构总览/核心数据流/组件逐层拆解/核心原理深度剖析/标志性能力实现/运维限制对比落地")


p += 1
divider("s-div1", 1, "背景痛点", p)
# ─────── Slide 1.5: The log is the database ───────
p += 1
std("s-log-is-db", "理论基石", "“The log is the database.” — Aurora, SIGMOD 2017", [
    T("lid-quote", 96, 168, 1088, 60,
      "&ldquo;<b>The log <i>is</i> the database.</b>&rdquo;<br>"
      "<span style='font-size:12px'>— Verbitski et al., <i>Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases</i>, SIGMOD 2017</span>",
      fs=17, color=FG, lh=1.5, align="left"),
    # Left: 关键观察
    R("lid-obs-bg", 96, 244, 530, 180, fill=PANEL, stroke=EDGE, radius=12),
    T("lid-obs-h", 116, 256, 500, 22, "关键观察", fs=14, fw=800, color=AC),
    T("lid-obs-b", 116, 284, 490, 128,
      "PostgreSQL/MySQL 的<b>崩溃恢复</b>就是「从检查点开始重放 WAL」——<br>"
      "说明 WAL 本身<b>已足够重建任意页面</b>。<br><br>"
      "既然如此：<b>页面物化</b>这件事可以从 compute 剥离，交给存储层自己完成。",
      fs=13, color=DIM, lh=1.7),
    # Right: Aurora 的做法
    R("lid-aur-bg", 656, 244, 530, 180, fill=PANEL, stroke=EDGE, radius=12),
    T("lid-aur-h", 676, 256, 500, 22, "Aurora 的落地", fs=14, fw=800, color=AC2),
    T("lid-aur-b", 676, 284, 500, 128,
      "• Compute <b>只发 redo 日志</b>，不再写脏页 / 刷 checkpoint<br>"
      "• WAL → 跨 3 AZ 共 6 副本存储层<br>"
      "• 各副本<b>独立重放 WAL 物化页面</b>；读时按 (Page, LSN) 版本请求<br>"
      "• 网络流量降到约 <b>1/7.7</b>（只传 redo 而非整页）",
      fs=12.5, color=DIM, lh=1.7),
    # Bottom: Neon 的再进一步
    R("lid-neon-bg", 96, 444, 1088, 176, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=12),
    T("lid-neon-h", 116, 456, 1000, 22, "Neon = 这个思想的开源重实现，再往前一步", fs=14, fw=800, color=AC),
    T("lid-neon-b", 116, 484, 1048, 128,
      "把 Aurora 合在一起的存储层<b>再拆两半</b>：<br>"
      "&nbsp;&nbsp;• <b>Safekeeper</b> — Paxos-like 共识，只负责 WAL 的持久化与仲裁<br>"
      "&nbsp;&nbsp;• <b>Pageserver</b> — 消费 WAL，用 delta / image layer 类 LSM 结构物化页面，冷数据下沉对象存储（S3）<br>"
      "&nbsp;&nbsp;• <b>Compute</b> — 替换 smgr、去掉 checkpoint、启动不扫 data directory 的<b>无状态 Postgres</b><br>"
      "代价：多一跳网络　　收益：两层可分别针对<b>低延迟写</b>和<b>高吞吐读</b>优化，页面物化可建在廉价对象存储上。",
      fs=13, color=DIM, lh=1.7),
], p, notes="Aurora SIGMOD 2017 论文提出的核心观察『The log is the database.』：WAL 已足够重建任意页面（因为崩溃恢复就是重放 WAL），所以页面物化可以从计算节点剥离到存储层。Aurora 做法：compute 只发 redo 日志、不写脏页 / 不做 checkpoint；WAL 跨 3 AZ 共 6 副本；副本各自独立重放物化；按 (Page, LSN) 版本请求；网络流量降到约 1/7.7。这是存算分离和 Serverless 数据库的理论基石。Neon 是这一思想的开源重实现，并把 Aurora 合在一起的存储层进一步拆成 Safekeeper（WAL 共识层）+ Pageserver（页面物化 + 类 LSM 分层 + 对象存储）；compute 替换 smgr、去掉 checkpoint、启动不扫 data dir。仓库中虽不直接使用『log is the database』这个句子，但 docs/rfcs/004-durability.md:64 明确对比过 Aurora 的差异。参考文献：Verbitski et al., Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases, SIGMOD 2017。")


# ─────── Slide 2: 核心定位 ───────
p += 1
std("s-position", "定位", "Neon vs 传统 PostgreSQL：核心区别", [
    T("pos-left-h", 96, 190, 520, 26, "传统 PostgreSQL", fs=18, fw=700, color=AC2),
    T("pos-left-b", 96, 222, 520, 340,
      "• 本地磁盘 8KB page 文件<br>"
      "• WAL 写本地 + 归档<br>"
      "• 备份：pg_basebackup / WAL archive<br>"
      "• 分支：逻辑复制/物理快照（重量级）<br>"
      "• 计算节点有状态<br>"
      "• PITR：WAL 完整回放，天级/时级",
      fs=16, color=DIM, lh=1.7),
    T("pos-right-h", 680, 190, 520, 26, "Neon", fs=18, fw=700, color=AC),
    T("pos-right-b", 680, 222, 520, 340,
      "• 无本地状态，GetPage@LSN 从 Pageserver 拉取<br>"
      "• WAL → Safekeeper Paxos 多数派<br>"
      "• Pageserver 分层不可变 layer + S3<br>"
      "• 秒级 Copy-on-Write 分支（只写元数据）<br>"
      "• 计算节点<b>无状态</b>，可 scale-to-zero<br>"
      "• LSN 直接寻址，任意 LSN 秒级建 branch",
      fs=16, color=DIM, lh=1.7),
    R("pos-div", 636, 190, 2, 400, fill="rgba(255,255,255,0.12)", stroke="none", sw=0, radius=1),
], p, notes="对比传统 Postgres 与 Neon 存储计算分离架构")


p += 1
std("s-goals", "定位", "核心定位与核心价值", [
    T("goal-pos-h", 96, 168, 1088, 24, "核心定位", fs=15, fw=800, color=AC),
    T("goal-pos-b", 96, 196, 1088, 46,
      "<b>存算分离 · 版本化存储 · Serverless</b> 的开源 Postgres 平台 —— "
      "计算节点是打了补丁的 Postgres 内核，SQL/协议层对应用透明；"
      "存储层按 LSN 版本化归档，是分支与时间旅行的共同基础（非字面意义上的\"未修改内核 100% 兼容\"）。",
      fs=13.5, color=DIM, lh=1.6),
    T("goal-val-h", 96, 254, 1088, 22, "核心价值", fs=15, fw=800, color=AC),
    *card("goal1", 96, 284, 530, 158,
          "Scale-to-Zero：自动休眠 / 唤醒", [
              "闲时计算节点自动挂起（suspend），零占用成本",
              "有请求时秒级冷启动唤醒，用户几乎无感",
              "→ 落地：第 06 章 Scale-to-Zero / Autoscaling",
          ], hc=AC, fs=13, headfs=15.5),
    *card("goal2", 656, 284, 530, 158,
          "Instant Branch：即时数据库分支", [
              "Copy-on-Write，创建分支只写元数据，不拷数据",
              "任意 LSN 秒级建分支，替代重量级快照/逻辑复制",
              "→ 落地：第 06 章 CoW 分支 / Synthetic Size",
          ], hc=AC2, fs=13, headfs=15.5),
    *card("goal3", 96, 452, 530, 158,
          "Time Travel：时间旅行查询", [
              "按历史 LSN / 时间点直接查询过去某一状态",
              "与 Instant Restore 共享同一套变更历史窗口机制",
              "→ 落地：第 05 章 LSN 链路、第 06 章分支",
          ], hc="#C89EFF", fs=13, headfs=15.5),
    *card("goal4", 656, 452, 530, 158,
          "计算 / 存储独立弹性、按量计费", [
              "计算可无限横向扩展、故障后快速重建，与存储解耦",
              "存储层独立演进（分片、GC、多云对象存储）",
              "→ 落地：第 04 章组件拆解、第 05 章深度剖析",
          ], hc="#7CB3F4", fs=13, headfs=15.5),
], p, notes="核心定位：存算分离+版本化存储+Serverless 的开源 Postgres 平台，兼容性表述避免用'100%兼容/unmodified'（docs/core_changes.md:5-7,43 显示内核有补丁、WAL格式不兼容原生PG，这是长期目标而非现状）。核心价值四点：①Scale-to-Zero 对应 compute_tools 的 suspend/cold-start 机制（libs/compute_api/src/spec.rs:208-211, compute_tools/src/monitor.rs）；②Instant Branch 对应 pageserver 分支只写元数据不拷贝数据（pageserver/src/tenant.rs:5081-5083,5104-5108）；③Time Travel 是 Neon 官方文档确认使用的术语（neon.com/docs 明确有 Time Travel queries 功能，与 instant restore/branching from the past 共享 history window 变更历史机制），不同于 storage_controller 里那个高危运维恢复API（time_travel_remote_storage），此处特指面向用户的历史状态查询；④计算存储独立弹性对应 README.md:16-20 架构分离 + consumption_metrics.md 中存储/计算分别计量的指标体系。")


p += 1
divider("s-div2", 2, "顶层架构总览", p)
# ─────── Slide 3: 顶层组件 Overview ───────
p += 1
std("s-topo", "组件总览", "六大核心组件", [
    # 两行三列排布组件 cards
    *card("c1", 96, 180, 340, 170,
          "Compute Node", ["无状态 patched PostgreSQL", "pgxn/neon smgr hook", "walproposer 推 WAL", "compute_ctl 管理启停"], hc=AC),
    *card("c2", 470, 180, 340, 170,
          "Pageserver", ["存储引擎核心", "GetPage@LSN 服务", "WAL 摄入 → Layer 文件", "S3/GCS 上传"]),
    *card("c3", 844, 180, 340, 170,
          "Safekeeper", ["Paxos-like WAL 服务", "3 副本 quorum=2", "保证 commit 持久化", "WAL segment 备份到 S3"], hc=AC2),
    *card("c4", 96, 380, 340, 170,
          "Storage Broker", ["gRPC pub/sub 50051", "无状态服务发现", "SK pub → PS sub", "SafekeeperTimelineInfo"], hc="#7CB3F4"),
    *card("c5", 470, 380, 340, 170,
          "Storage Controller", ["PS + SK 统一管理", "Tenant/Shard 调度", "代次号(generation)发放", "迁移 & Secondary"]),
    *card("c6", 844, 380, 340, 170,
          "Proxy", ["Postgres 协议路由", "认证: SCRAM/JWT/Link", "SQL over HTTP", "WebSocket 网关"], hc="#C89EFF"),
], p, notes="Neon 6 大核心组件：Compute / Pageserver / Safekeeper / Broker / Controller / Proxy")

# ─────── Slide 4: 架构拓扑图 ───────
p += 1
std("s-arch", "架构", "端到端数据流拓扑", [
    # Client
    R("a-cli", 540, 168, 200, 38, fill="rgba(200,158,255,0.15)", stroke="rgba(200,158,255,0.5)"),
    T("a-cli-t", 540, 174, 200, 28, "Client (psql / App)", fs=13, fw=600, color="#C89EFF", align="center"),
    LN("a-l1", 640, 206, 0, 26, stroke=A_PUR, sw=2),
    # Proxy
    R("a-proxy", 510, 232, 260, 34, fill="rgba(200,158,255,0.10)", stroke="rgba(200,158,255,0.4)"),
    T("a-proxy-t", 510, 238, 260, 26, "Proxy (路由 + 认证 + HTTP)", fs=12, fw=600, color="#C89EFF", align="center"),
    # Proxy 按 -pooler 后缀分流到两个端口
    LN("a-l2p", 519, 266, 0, 28, stroke=A_PUR, sw=2),
    T("a-l2p-l", 300, 272, 216, 14, "&lt;ep&gt;-pooler → :6432", fs=9, fw=600, color="#C89EFF", align="right", ff=MONO),
    LN("a-l2d", 732, 266, 0, 28, stroke=A_GRN, sw=2),
    T("a-l2d-l", 744, 272, 200, 14, "&lt;ep&gt; 直连 → :5432", fs=9, fw=600, color=AC, align="left", ff=MONO),
    # Compute Node 容器（同 Pod 内 PgBouncer + Postgres 两进程）
    R("a-comp", 430, 294, 424, 82, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.45)"),
    T("a-comp-t", 430, 297, 424, 16, "Compute Node · 同 Pod / 同节点", fs=10, fw=700, color=AC, align="center"),
    # PgBouncer 子进程
    R("a-pgb", 442, 318, 154, 50, fill="rgba(200,158,255,0.12)", stroke="rgba(200,158,255,0.45)"),
    T("a-pgb-t", 442, 322, 154, 18, "PgBouncer", fs=12, fw=700, color="#C89EFF", align="center"),
    T("a-pgb-b", 442, 342, 154, 24, ":6432 · transaction", fs=9, fw=500, color=FAINT, align="center", ff=MONO),
    # Postgres 子进程
    R("a-pg", 626, 318, 212, 50, fill="rgba(0,229,153,0.12)", stroke="rgba(0,229,153,0.5)"),
    T("a-pg-t", 626, 322, 212, 18, "Postgres (无状态)", fs=12, fw=700, color=AC, align="center"),
    T("a-pg-b", 626, 342, 212, 24, ":5432 · walproposer + smgr", fs=9, fw=500, color=FAINT, align="center", ff=MONO),
    # PgBouncer → Postgres（本地 loopback 复用连接）
    LN("a-pgb-pg", 596, 343, 30, 0, stroke=A_PUR, sw=2, thick=9),
    # Postgres -> Safekeeper push WAL（垂直向下）
    LN("a-l3", 510, 376, 0, 24, stroke=A_ORG, sw=2, thick=9),
    T("a-wallab", 300, 380, 200, 16, "push WAL", fs=11, fw=700, color=A_ORG, align="right"),
    # Postgres <- Pageserver GetPage@LSN（Postgres 底部经 smgr 请求 PS）
    LN("a-l4", 800, 400, 0, -24, stroke=A_GRN, sw=2, thick=9),
    T("a-pglab", 886, 380, 160, 16, "GetPage@LSN", fs=11, fw=700, color=A_GRN),
    # Safekeeper
    R("a-sk", 400, 400, 220, 44, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.5)"),
    T("a-sk-t", 400, 406, 220, 36, "Safekeeper x3", fs=13, fw=700, color=AC2, align="center"),
    # Pageserver
    R("a-ps", 660, 400, 220, 44, fill="rgba(0,229,153,0.10)", stroke="rgba(0,229,153,0.5)"),
    T("a-ps-t", 660, 406, 220, 36, "Pageserver", fs=13, fw=700, color=AC, align="center"),
    # PS -> SK pull WAL (PS 主动建连拉取)
    LN("a-l5", 660, 422, -40, 0, sw=2, thick=10),
    T("a-skps", 580, 450, 120, 16, "PS 拉取 WAL", fs=10, fw=600, color=ARROW, align="center"),
    # SK -> S3 (WAL 备份)
    LN("a-l6b", 510, 444, 70, 146, stroke=AC2, sw=2, dashed=True),
    T("a-s3lab2", 400, 505, 120, 16, "WAL 备份", fs=10, fw=600, color=AC2, align="right"),
    # PS -> S3 (layer 上传)
    LN("a-l6", 770, 444, -70, 146, stroke=A_GRN, sw=2, dashed=True),
    T("a-s3lab", 760, 505, 120, 16, "layer 上传", fs=10, fw=600, color=AC, align="left"),
    # S3 (bottom center)
    R("a-s3", 500, 590, 280, 42, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)"),
    T("a-s3-t", 500, 596, 280, 22, "S3 / GCS / Azure Blob", fs=13, fw=600, color=AC, align="center"),
    T("a-s3-sub", 500, 616, 280, 14, "layer files + WAL segments", fs=10, fw=500, color=FAINT, align="center"),
    # Storage Controller (left, 控制面, 与 Broker 独立) —— 直连 SK 与 PS
    R("a-ct", 96, 500, 240, 44, fill="rgba(124,179,244,0.10)", stroke="rgba(124,179,244,0.4)"),
    T("a-ct-t", 96, 506, 240, 22, "Storage Controller", fs=12, fw=700, color="#7CB3F4", align="center"),
    T("a-ct-sub", 96, 526, 240, 14, "控制面 · 直连 PS/SK · 不经 Broker", fs=10, fw=500, color=FAINT, align="center"),
    T("a-ct-arr-l", 96, 472, 240, 16, "heartbeat + reconcile", fs=10, fw=600, color="#7CB3F4", align="center"),
    LN("a-ct-sk", 336, 512, 69, -64, stroke="#7CB3F4", sw=2, dashed=True),
    LN("a-ct-ps", 336, 526, 332, -76, stroke="#7CB3F4", sw=2, dashed=True),
    # Storage Broker (right, 数据面 pub/sub) —— SK 双向 pub+sub，PS 以 sub 为主
    R("a-br", 944, 500, 240, 44, fill="rgba(124,179,244,0.10)", stroke="rgba(124,179,244,0.4)"),
    T("a-br-t", 944, 506, 240, 22, "Storage Broker", fs=12, fw=700, color="#7CB3F4", align="center"),
    T("a-br-sub", 944, 526, 240, 14, "数据面 · SK pub+sub · PS sub", fs=10, fw=500, color=FAINT, align="center"),
    T("a-br-arr-l", 944, 472, 240, 16, "gRPC pub/sub timeline 状态", fs=10, fw=600, color="#7CB3F4", align="center"),
    LN("a-br-ps", 944, 512, -69, -64, stroke="#7CB3F4", sw=2, dashed=True),
    LN("a-br-sk", 944, 526, -332, -76, stroke="#7CB3F4", sw=2, dashed=True),
    # SK → Broker (pub 方向)，与 Broker→SK 反向表达双向 pub+sub
    LN("a-sk-br", 618, 448, 328, 74, stroke=AC2, sw=2, dashed=True),
    T("a-sk-br-l", 720, 500, 140, 14, "SK pub", fs=10, fw=600, color=AC2, align="center"),
], p, notes="端到端数据流：Client → Proxy。Proxy 按连接串是否带 -pooler 后缀分流：带后缀走 PgBouncer :6432，不带走 Postgres :5432（butterfly DEFAULT_PGBOUNCER_PORT=6432）。"
   "PgBouncer 与 Postgres 是同一 Compute Pod / 同节点内的两个进程，PgBouncer 经本地回环复用到 Postgres；"
   "pool_mode=transaction，default_pool_size = 0.9 * max_connections（随 compute flavor 规格变化），由管控面下发到 compute spec 的 pgbouncer_settings，compute_ctl 启动时通过 pgbouncer admin console(:6432) tune_pgbouncer 生效。"
   "Postgres 侧：walproposer push WAL → Safekeeper（Paxos 多数派持久化）；smgr hook 发 GetPage@LSN 到 Pageserver。"
   "Pageserver walreceiver 主动连接 SK 拉取 WAL stream（方向 PS→SK 建连，SK→PS 数据流）。"
   "Storage Broker 数据面 gRPC pub/sub：SK 双向 pub+sub（SK 间也靠 broker 交换 LSN），PS 主要 sub 选主/切换，找不到候选时 publish discovery request → SK 回 discovery response。"
   "SK 会选举一个实例把 WAL segment 备份到 S3（safekeeper/src/wal_backup.rs），PS 把 layer files 上传到同一 S3；两条上传路径互相独立，只是复用同一 remote_storage 抽象。"
   "Storage Controller 是控制面：直接 HTTP heartbeat + reconcile 管理 PS 和 SK，storage_controller crate 无 broker 依赖，与 Storage Broker 完全独立。")


p += 1
divider("s-div-flow", 3, "核心数据流：写路径 + 读路径", p)
# ─────── Slide 12: 写路径 ───────
p += 1
std("s-write", "写路径", "一次 INSERT 的旅程", [
    *[e for i, (n, txt, c) in enumerate([
        ("1", "Compute 执行 INSERT，生成 WAL record 到 wal_buffers", AC),
        ("2", "commit → <b>walproposer</b> bgworker 并发推送到 3 个 Safekeeper", AC2),
        ("3", "每个 SK <b>fsync WAL 到本地 SSD</b>，ACK 自己的 flushLSN", AC2),
        ("4", "walproposer 计算 <b>commitLSN = 多数派确认位置</b>（quorum=2 of 3）", AC2),
        ("5", "Compute 返回 <b>COMMIT OK</b> 给 client　←　到这里就已持久化", AC),
        ("6", "异步：SK 向 <b>Storage Broker</b> push SafekeeperTimelineInfo", "#7CB3F4"),
        ("7", "Pageserver 订阅 broker，从 commitLSN 最大的 SK 拉 WAL 流", "#7CB3F4"),
        ("8", "解码 → 按 key 写 <b>open in-memory layer</b>（reorder buffer）", "#C89EFF"),
        ("9", "达 checkpoint_distance (256MB) → freeze → flush 成 <b>L0 delta layer</b>", "#C89EFF"),
        ("10", "compaction: L0 → L1 delta → L1 image；layer 上传 <b>S3</b>（带 generation 前缀）", "#C89EFF"),
    ]) for e in (
        R(f"wr{i}bg", 96, 174 + i * 42, 1088, 36, fill="rgba(255,255,255,0.035)", stroke="none", sw=0, radius=8),
        T(f"wr{i}nt", 108, 181 + i * 42, 30, 18, n, fs=12, fw=800, color=c, align="center", ff=MONO),
        T(f"wr{i}t", 150, 180 + i * 42, 1020, 22, txt, fs=14, fw=500, color=DIM, lh=1.4),
    )],
    T("wr-note", 96, 604, 1088, 40,
      "<b>commit 延迟只依赖 Safekeeper 多数派</b> —— Pageserver 挂掉不影响写入，S3 上传完全异步。",
      fs=14, color=AC, lh=1.5),
], p, notes="写路径 10 步：WAL → walproposer → SK 多数派 fsync → commit OK；异步经 broker 到 Pageserver → layer → S3")


# ─────── Slide 12: 读路径 GetPage@LSN ───────
p += 1
std("s-read", "读路径", "一次 SELECT 的旅程", [
    *[e for i, (n, txt, c) in enumerate([
        ("1", "Compute 执行 SELECT，需要页 P → 查 <b>shared_buffers</b>，未命中", AC),
        ("2", "查 <b>Neon LFC</b>（Local File Cache，本地 SSD 缓存），未命中", AC),
        ("3", "pgxn/neon <b>smgr hook</b> 发出 GetPage@LSN(P, last_written_lsn)", AC2),
        ("4", "Pageserver：若 target_lsn &gt; 已摄入 LSN → <b>阻塞等 WAL 到达</b>（背压保护）", AC2),
        ("5", "<b>LayerMap</b> 定位覆盖 (key, LSN) 的最新 image layer + 之上所有 delta layer", "#7CB3F4"),
        ("6", "本地读 layer 文件；本地 miss 则<b>按需从 S3 下载</b>", "#7CB3F4"),
        ("7", "通过 tenant 专属 <b>seccomp 沙箱 WAL-redo 进程</b> replay 出目标版本页", "#C89EFF"),
        ("8", "返回 8 KB page → Compute 缓存到 shared_buffers/LFC → executor 组装结果", AC),
    ]) for e in (
        R(f"rd{i}bg", 96, 178 + i * 48, 1088, 40, fill="rgba(255,255,255,0.035)", stroke="none", sw=0, radius=8),
        R(f"rd{i}n", 108, 186 + i * 48, 24, 24, fill="rgba(255,255,255,0.10)", stroke="none", sw=0, radius=12),
        T(f"rd{i}nt", 108, 190 + i * 48, 24, 18, n, fs=12, fw=800, color=c, align="center", ff=MONO),
        T(f"rd{i}t", 146, 188 + i * 48, 1020, 22, txt, fs=14, fw=500, color=DIM, lh=1.4),
    )],
    T("rd-note", 96, 570, 1088, 30,
      "关键：<b>没有 image layer 时必须 replay WAL</b> —— 这是 Pageserver 需要 compaction 生成 image 的原因。",
      fs=14, color=FAINT, lh=1.5),
], p, notes="读路径 8 步：shared_buffers → LFC → GetPage@LSN → LayerMap → layer 文件 → WAL redo → 返回页")


p += 1
divider("s-div3", 4, "组件逐层拆解：读写路径贯穿", p)
# ─────── Slide 5: Compute 层概述 ───────
p += 1
std("s-proxy", "PROXY", "连接代理：路由 + 认证 + Serverless 网关", [
    T("px-desc", 96, 170, 1088, 50,
      "Proxy 是所有外部连接的唯一入口。解析 SNI 确定 project，从 control plane 拿目标 compute 信息。",
      fs=15, color=DIM, lh=1.6),
    *card("px1", 96, 235, 530, 190,
          "入口协议", [
              "① <b>Postgres over TCP</b>　—　标准 psql / 驱动",
              "② <b>Postgres over WebSocket</b>　—　浏览器 / Edge",
              "&nbsp;&nbsp;（@neondatabase/serverless）",
              "③ <b>SQL over HTTP</b>　—　单次 POST + JSON",
              "&nbsp;&nbsp;无 TCP 长连，适合 Serverless / Edge Function",
              "&nbsp;&nbsp;强制 extended query（参数化，防注入）",
          ], hc="#C89EFF", fs=14, headfs=16),
    *card("px2", 660, 235, 530, 190,
          "认证方式", [
              "• <b>console</b>：SCRAM-SHA-256 via cloud console API",
              "• <b>link</b>：Magic-link 登录（浏览器跳转）",
              "• <b>JWT</b>：第三方签发（Clerk 等）via JWKS",
              "• <b>password</b>：直连 Postgres 认证表（本地调试）",
              "",
              "查询取消需 <b>Redis</b> 做跨实例传播",
          ], hc=AC2, fs=14, headfs=16),
    # Rest broker
    *card("px3", 96, 452, 1088, 110,
          "REST Broker 模式（新功能）", [
              "• --is-rest-broker：配合 subzero-core 提供 <b>PostgREST 风格 REST API</b>",
              "• GET /database/rest/v1/items?select=id,name&amp;id=eq.1",
              "• 支持 JWT 认证 + CORS headers",
          ], hc=AC, fs=14, headfs=16),
], p, notes="Proxy: TCP/WebSocket/HTTP 三协议入口，SCRAM/JWT/Link 认证，新增 REST Broker 模式")

# ─────── 连接 Neon：endpoint 路由三法 ───────
p += 1
std("s-conn-route", "PROXY", "连上 Neon：Proxy 怎么知道你要连哪个库", [
    T("cr-desc", 96, 166, 1088, 40,
      "Postgres 协议里<b>没有「我要连哪个集群」这个字段</b>。Proxy 必须从三个地方之一挖出 endpoint_id，"
      "统一在 <span style='font-family:" + MONO + "'>ComputeUserInfoMaybeEndpoint::parse</span>（<span style='font-family:" + MONO + "'>credentials.rs:74</span>）。",
      fs=13.5, color=DIM, lh=1.5),
    # three columns
    R("cr1-bg", 96, 212, 350, 268, fill=PANEL, stroke=EDGE, radius=12),
    T("cr1-n", 114, 224, 200, 18, "① 优先级最高", fs=11, fw=800, color=AC, ff=MONO),
    T("cr1-h", 114, 246, 320, 22, "options 启动参数", fs=15, fw=800, color=AC),
    T("cr1-b", 114, 274, 320, 196,
      "启动包 <span style='font-family:" + MONO + "'>options</span> 串里塞 <span style='font-family:" + MONO + "'>-c</span> 风格 token：<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>?options=endpoint%3Dep-xxx</span><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>project=</span> 是<b>旧写法</b>，仍兼容<br><br>"
      "解析：<span style='font-family:" + MONO + "'>options_raw()</span> 拆词后<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>parse_endpoint_param</span> 取前缀<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>.at_most_one()</span> —— 出现<b>两个</b><br>"
      "&nbsp;&nbsp;endpoint/project token 就<b>判为歧义</b>，<br>"
      "&nbsp;&nbsp;直接当没有（None）<br><br>"
      "示例：<span style='font-family:" + MONO + "'>-ckey=1 endpoint=bar -c geqo=off</span>",
      fs=11.5, color=DIM, lh=1.7),
    R("cr2-bg", 465, 212, 350, 268, fill=PANEL, stroke=EDGE, radius=12),
    T("cr2-n", 483, 224, 200, 18, "② 常规路径", fs=11, fw=800, color=AC2, ff=MONO),
    T("cr2-h", 483, 246, 320, 22, "TLS SNI 主机名", fs=15, fw=800, color=AC2),
    T("cr2-b", 483, 274, 320, 196,
      "TLS 握手时的 SNI = <span style='font-family:" + MONO + "'>&lt;endpoint&gt;.&lt;common-name&gt;</span><br>"
      "&nbsp;&nbsp;第一个 <b>.</b> 前的 label 就是 endpoint_id<br>"
      "&nbsp;&nbsp;后半段必须命中 Proxy 证书里的 CN 集合<br><br>"
      "<span style='font-family:" + MONO + "'>endpoint_sni()</span>（<span style='font-family:" + MONO + "'>credentials.rs:63</span>）<br><br>"
      "<b>两个保留子域不走 SNI 路由</b>：<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>api</span>（serverless driver）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>apiauth</span>（auth broker）<br><br>"
      "WebSocket 客户端没有 SNI →<br>"
      "&nbsp;&nbsp;用 HTTP <b>Host 头</b>顶上（<span style='font-family:" + MONO + "'>pglb/mod.rs:190</span>）",
      fs=11.5, color=DIM, lh=1.7),
    R("cr3-bg", 834, 212, 350, 268, fill=PANEL, stroke=EDGE, radius=12),
    T("cr3-n", 852, 224, 200, 18, "③ 兜底 HACK", fs=11, fw=800, color="#C89EFF", ff=MONO),
    T("cr3-h", 852, 246, 320, 22, "Password Hack", fs=15, fw=800, color="#C89EFF"),
    T("cr3-b", 852, 274, 320, 196,
      "给<b>老 libpq / 不支持 SNI</b> 的客户端留的后门：<br>"
      "<b>把 endpoint 名塞进密码字段</b><br><br>"
      "格式（<span style='font-family:" + MONO + "'>password_hack.rs:16</span>）：<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>endpoint=&lt;name&gt;;&lt;password&gt;</span><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>endpoint=&lt;name&gt;$&lt;password&gt;</span><br>"
      "&nbsp;&nbsp;<b>;</b> 和 <b>$</b> 谁先出现按谁切<br><br>"
      "触发条件：①② <b>都拿不到</b> endpoint 时<br>"
      "&nbsp;&nbsp;（<span style='font-family:" + MONO + "'>auth_quirks</span>，<span style='font-family:" + MONO + "'>backend/mod.rs:211</span>）<br>"
      "&nbsp;&nbsp;Proxy 先发 <b>CleartextPassword</b> 请求<br>"
      "&nbsp;&nbsp;密码本身<b>不在 Proxy 校验</b>，透传给 compute",
      fs=11.5, color=DIM, lh=1.7),
    # bottom band: priority rules
    R("cr4-bg", 96, 494, 1088, 168, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("cr4-h", 116, 506, 900, 20, "优先级与冲突规则", fs=13, fw=800, color=AC),
    T("cr4-b", 116, 532, 1048, 124,
      "<span style='font-family:" + MONO + "'>match (endpoint_option, endpoint_from_domain)</span>　（<span style='font-family:" + MONO + "'>credentials.rs:106</span>）<br>"
      "• 两者都有且<b>不一致</b> → 直接报错 <span style='font-family:" + MONO + "'>InconsistentProjectNames</span>，<b>拒绝连接</b>（不猜、不偏向任何一方）<br>"
      "• 两者一致 / 只有一个 → <span style='font-family:" + MONO + "'>a.or(b)</span>，即 <b>options 优先于 SNI</b><br>"
      "• 都没有 → endpoint_id = None → 落到 <b>Password Hack</b>；payload 也解不出就返回 <span style='font-family:" + MONO + "'>MissingEndpointName</span>，<br>"
      "&nbsp;&nbsp;错误文案直接教用户「升级 libpq 支持 SNI，或加 <span style='font-family:" + MONO + "'>?options=endpoint%3D&lt;id&gt;</span>」（<span style='font-family:" + MONO + "'>auth/mod.rs:50</span>）<br>"
      "• 埋点：<span style='font-family:" + MONO + "'>SniKind</span> 指标区分 <span style='font-family:" + MONO + "'>Sni</span> / <span style='font-family:" + MONO + "'>NoSni</span> / <span style='font-family:" + MONO + "'>PasswordHack</span>，可观测各路径占比",
      fs=12, color=DIM, lh=1.7),
], p, notes="连接 Neon 的 endpoint 路由三法，统一入口 ComputeUserInfoMaybeEndpoint::parse（proxy/src/auth/credentials.rs:74-156），由 proxy/src/proxy/mod.rs:53 每连接调一次。① options 启动参数：?options=endpoint%3Dep-xxx，project= 是旧写法仍兼容；解析 options_raw()（pqproto.rs:398）拆词 + parse_endpoint_param（password_hack.rs:33）取前缀 + .at_most_one() 保证唯一，出现两个 token 或同时有 endpoint= 和 project= 都判歧义返回 None（测试 credentials.rs:317,336）。② TLS SNI：<endpoint>.<common-name>，第一个点前 label 是 endpoint_id，后半段必须在证书 CN 集合内，endpoint_sni() credentials.rs:63；保留子域 api（SERVERLESS_DRIVER_SNI）和 apiauth（AUTH_BROKER_SNI）不走 SNI 路由，见 serverless/mod.rs:60；SNI 从 stream.rs:266 sni_hostname() 取，WebSocket 客户端无 SNI 用 HTTP Host 头代替（pglb/mod.rs:190）。③ Password Hack：给不支持 SNI 的老客户端，格式 endpoint=<name>;<password> 或 endpoint=<name>$<password>，分号和美元符谁先出现按谁切（password_hack.rs:16-30）；只在①②都失败时触发，在 auth_quirks（backend/mod.rs:211）里 TryFrom 失败分支调 hacks::password_hack_no_authentication（hacks.rs:63），Proxy 先发 AuthenticationCleartextPassword（flow.rs:77），密码不在 Proxy 校验直接透传 compute。优先级：match (endpoint_option, endpoint_from_domain) credentials.rs:106，两者不一致直接 InconsistentProjectNames 拒连；一致或只有一个用 a.or(b) 即 options 优先；都没有则 None 落 Password Hack，解不出返回 MissingEndpointName 并提示升级 libpq 或加 ?options=endpoint%3D<id>（auth/mod.rs:50）。SniKind 指标区分 Sni/NoSni/PasswordHack。")

# ─────── Slide 5: Compute 层概述 ───────
p += 1
std("s-comp1", "COMPUTE", "Compute Node — patched PostgreSQL 的四点关键改动", [
    T("comp-desc", 96, 166, 1088, 40,
      "Compute 是<b>打了补丁的 PostgreSQL</b>。每张卡片正文都分成两段："
      "<span style='color:" + AC + ";font-weight:800'>■ 插件 pgxn/neon</span>（`shared_preload_libraries` 加载，改造主体）与 "
      "<span style='color:#FF9E8A;font-weight:800'>■ 内核 patch</span>（改 PG 源码，只在插件够不到时才动）。",
      fs=13, color=DIM, lh=1.6),
    *card("cm1", 96, 212, 530, 218,
          "① 替换 smgr <span style='font-size:11px;font-weight:700;color:#C89EFF;background:rgba(200,158,255,0.15);padding:2px 6px;border-radius:4px'>EXT + PATCH</span>", [
              "<span style='color:" + AC + ";font-weight:800'>■ 插件（主体）</span>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>libpagestore.c:1649</span> 装 <b>smgr_hook = smgr_neon</b>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>neon_read</span> → LFC miss 则 GetPage@LSN（:1367）",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>neon_write</span> → 写 LFC + 补 WAL-log，<b>不落 md</b>（:1596）",
              "",
              "<span style='color:#FF9E8A;font-weight:800'>■ 内核 patch（3 条，凿出 hook 点）</span>",
              "&nbsp;&nbsp;· smgr 接口对扩展开放（core_changes.md:179）",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>smgropen()</span> 加 relpersistence 区分 unlogged（:193）",
              "&nbsp;&nbsp;· dbsize 改用 <span style='font-family:" + MONO + "'>dbsize_hook</span>，不扫 data dir（:221）",
          ], hc=AC, fs=11.5, headfs=15),
    *card("cm2", 656, 212, 530, 218,
          "② WAL → SK 走 bgworker <span style='font-size:11px;font-weight:700;color:#C89EFF;background:rgba(200,158,255,0.15);padding:2px 6px;border-radius:4px'>EXT + PATCH</span>", [
              "<span style='color:" + AC + ";font-weight:800'>■ 插件（主体）</span>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>walproposer_pg.c:689</span> 注册 <b>walproposer bgworker</b>",
              "&nbsp;&nbsp;· :1566 读 <span style='font-family:" + MONO + "'>GetFlushRecPtr()</span> 广播 3 台 SK",
              "&nbsp;&nbsp;· 等 <b>quorum=2</b> 达成即 commit ACK；与 smgr <b>两条独立路径</b>",
              "",
              "<span style='color:#FF9E8A;font-weight:800'>■ 内核 patch（2 条，辅助）</span>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>ProcessInterrupts</span> 加 callback 做背压（:325）",
              "&nbsp;&nbsp;· walproposer 在 checkpointer <b>之后</b>关停（:388）",
              "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#888'>——保证最后一条 CheckPoint WAL 能推到 SK</span>",
          ], hc=AC2, fs=11.5, headfs=15),
    *card("cm3", 96, 442, 530, 218,
          "③ checkpoint 掏空 <span style='font-size:11px;font-weight:700;color:#00E599;background:rgba(0,229,153,0.15);padding:2px 6px;border-radius:4px'>纯 EXT</span>", [
              "<span style='color:" + AC + ";font-weight:800'>■ 插件（全部）</span>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>neon_writeback / immedsync / registersync</span> 全 <b>no-op</b>",
              "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#888'>pagestore_smgr.c:1230, 1888, 1922</span>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>BufferSync()</span> 刷脏页 → 底层 fsync <b>被架空</b>",
              "",
              "<span style='color:#FF9E8A;font-weight:800'>■ 内核 patch：无</span>",
              "&nbsp;&nbsp;· checkpointer 进程 &amp; CheckPoint WAL record 都是 PG <b>原生、照常跑</b>",
              "&nbsp;&nbsp;· 能纯插件做到，正是因为 ① 已把整张 smgr 表换掉",
              "&nbsp;&nbsp;· 持久化靠 <span style='font-family:" + MONO + "'>XLogInsert</span> → 本地 fsync → walproposer",
          ], hc="#C89EFF", fs=11.5, headfs=15),
    *card("cm4", 656, 442, 530, 218,
          "④ 启动跳过 replay <span style='font-size:11px;font-weight:700;color:#FF9E8A;background:rgba(255,158,138,0.15);padding:2px 6px;border-radius:4px'>纯 PATCH</span>", [
              "<span style='color:" + AC + ";font-weight:800'>■ 插件：无</span>",
              "&nbsp;&nbsp;· 启动流程 / <span style='font-family:" + MONO + "'>pg_control</span> 语义，插件<b>拦不到</b>",
              "&nbsp;&nbsp;· 外围逻辑在 Rust 侧：compute_ctl 清空 pgdata + 拉 basebackup",
              "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#888'>compute.rs:1201, 1601 · basebackup.rs:1-11</span>",
              "",
              "<span style='color:#FF9E8A;font-weight:800'>■ 内核 patch（改 xlog.c）</span>",
              "&nbsp;&nbsp;· 读 <span style='font-family:" + MONO + "'>neon.signal</span> 的 LSN <b>直接进 running</b>（:119-135）",
              "&nbsp;&nbsp;· <b>不读 checkpoint record、不做 WAL replay</b>",
              "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>pg_control</span> 伪装 DB_SHUTDOWNED（xlog_utils.rs:159）",
          ], hc="#7CB3F4", fs=11.5, headfs=15),
], p, notes="讲这页时先立设计原则：docs/core_changes.md:14-17 明确 'Most of the Neon-specific code is in the extensions, and for any new features, that is preferred over modifying core PostgreSQL code' —— 绝大多数改造在 pgxn/neon 扩展（shared_preload_libraries 加载），内核 patch 只在扩展够不到的地方动刀，且 core_changes.md 每条 patch 都带一节 'How to get rid of the patch'，长期目标是全部推上游、让未修改的 PG 也能跑 Neon 存储（:4-7）。徽章含义：[EXT]=纯扩展；[PATCH]=纯内核 patch；[EXT + PATCH]=扩展是主体但依赖内核 patch 凿出 hook 点。① 替换 smgr [EXT + PATCH]：主体是扩展——pagestore_smgr.c:2220 定义 neon_smgr 结构体（smgr_read=neon_read/smgr_write=neon_write），libpagestore.c:1649-1651 装 smgr_hook=smgr_neon / smgr_init_hook / dbsize_hook；permanent 关系 read 走 LFC→GetPage@LSN（:1367-1471），write 走 LFC+补 WAL-log（:1596-1675），临时/unlogged 表 fallback md。依赖三个内核 patch：core_changes.md:179-191 'Make smgr interface available to extensions'（改 smgr.c/smgr.h 共 275 行，凿出 smgr_hook，已提上游 commitfest 47/4428 但推进极慢）、:193-211 'Added relpersistence argument to smgropen()'（让 smgr 实现能区分 permanent/unlogged/temp，否则无法差异化处理 unlogged 表）、:221-232 'Use smgr and dbsize_hook for size calculations'（原生 dbsize.c 直接扫 data directory 算大小，在 Neon 下不成立）。② WAL→SK [EXT + PATCH]：主体是扩展——walproposer_pg.c:689 walprop_register_bgworker 注册 bgworker（bgw_library_name='neon', BgWorkerStart_RecoveryFinished），:180 WalProposerMain，:1566 XLogBroadcastWalProposer 读 GetFlushRecPtr()（本地已 fsync 的 pg_wal）广播给 3 台 SK，quorum=2 达成即 commit。依赖两个辅助 patch：core_changes.md:325-354 'Backpressure if pageserver doesn't ingest WAL fast enough'（在 ProcessInterrupts 里加 ProcessInterruptsCallback + retry label，让 PS 消费 WAL 落后时能在 compute 侧反压）、:388-395 'Shut down walproposer after checkpointer'（调整关停顺序，确保 checkpointer 最后一条 CheckPoint WAL record 也能推给 SK）。③ checkpoint 掏空 [EXT]：没有独立 patch，checkpointer 进程和 CheckPoint WAL record 都是 PG 原生行为、照常跑；扩展只是把 smgr 的刷盘方法做成 no-op——neon_writeback (pagestore_smgr.c:1230)/neon_immedsync (1888)/neon_registersync (1922) 对 permanent 关系全空转（日志打 'writeback noop'/'immedsync noop'），BufferSync 遍历脏页调下来时底层 fsync 被架空。这条能纯扩展实现，正是因为 ① 已经把整个 smgr 表换掉了。持久化真正靠 AM 层 XLogInsert → 本地 pg_wal fsync → walproposer → SK quorum。④ 启动跳过 crash recovery [PATCH]：这是真·内核 patch，启动流程和 pg_control 语义扩展拦不到——core_changes.md:119-135 'Allow startup without reading checkpoint record' 改 xlog.c，读 neon.signal（也兼容 zenith.signal）里的 LSN 作为起点、直接认定该 LSN 一致，不读最后的 checkpoint record、不做 WAL redo；'How to get rid of the patch' 一栏写的是 '???'，说明连 Neon 自己都还没想好怎么消掉。配套的不是插件也不是 patch，而是 Rust 侧：libs/postgres_ffi/src/xlog_utils.rs:159-176 generate_pg_control 造出 checkPoint=0 / state=DB_SHUTDOWNED 的假 pg_control 塞进 basebackup tarball；compute_tools/src/compute.rs:1201 create_pgdata 清空目录、:1601-1650 prepare_pgdata 拉 tarball 解压（pageserver/src/basebackup.rs:1-11：只含 non-relational data——pg_control/SLRU/filenodemap/twophase/neon.signal/dummy WAL segment，关系文件是占位空文件）。注意 core_changes.md:145-146 记了备选方案是往 tarball 里塞假 checkpoint record，但被否了——怕假 WAL 意外流到 safekeeper 覆盖真 WAL。")

# ─────── compute_ctl 总览 ───────
p += 1
std("s-computectl", "COMPUTE", "compute_ctl —— compute 容器里的 PostgreSQL 监护进程", [
    T("cc-desc", 96, 162, 1088, 36,
      "compute_ctl 是 compute 容器的 <b>entrypoint / 1 号进程</b>，postgres 是它 fork 出来的子进程。"
      "它把「控制面给的 <span style='font-family:" + MONO + "'>ComputeSpec</span>」翻译成「一个连好存储、建好库和角色的可用 PG」。"
      "<span style='color:" + DIM + "'>compute_tools/src/bin/compute_ctl.rs:1-35 · README.md</span>",
      fs=12, color=DIM, lh=1.55),
    # Left: lifecycle
    R("cc-l-bg", 96, 204, 636, 344, fill=PANEL, stroke=EDGE, radius=12),
    T("cc-l-h", 116, 216, 600, 22, "启动流程  ComputeNode::run()  compute.rs:627", fs=14, fw=800, color=AC),
    T("cc-l-b", 116, 246, 600, 294,
      "<b>①</b> 拉起两个 HTTP server：<b>3080</b> 对控制面 / <b>3081</b> 对本机组件<br>"
      "<b>②</b> <span style='font-family:" + MONO + "'>wait_spec()</span>(:752) —— spec 来自 CLI 参数，或阻塞等 "
      "<span style='font-family:" + MONO + "'>POST /configure</span><br>"
      "<b>③</b> <span style='font-family:" + MONO + "'>start_compute()</span>(:793) 冷启动，顺序做四件事：<br>"
      "&nbsp;&nbsp;· 下载 remote extensions<br>"
      "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>prepare_pgdata()</span>(:1601)：清空 pgdata、写 postgresql.conf、<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;sync safekeepers 定起点、拉 <b>basebackup</b> 解压、写 pg_hba<br>"
      "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>start_postgres()</span>(:1789) fork 出 postgres<br>"
      "&nbsp;&nbsp;· <span style='font-family:" + MONO + "'>configure_as_primary()</span>(:2179) → <span style='font-family:" + MONO + "'>apply_config()</span>(:1972)<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;按 <b>ApplySpecPhase</b> 建 role/db/extension，最后跑 bootstrap template<br>"
      "<b>④</b> 状态置 <b style='color:" + AC + "'>Running</b>(:1039)，起 vm-monitor<br>"
      "<b>⑤</b> 等 postgres 退出 → 清理（失败时多等 30s 便于抓日志）<br><br>"
      "<b style='color:" + AC2 + "'>热变更</b>：configurator 线程(configurator.rs:13)常驻，监听到<br>"
      "&nbsp;&nbsp;ConfigurationPending → <span style='font-family:" + MONO + "'>reconfigure()</span>(:2089)：改 conf + "
      "<span style='font-family:" + MONO + "'>pg_reload_conf</span> + 重放 spec SQL，<b>不重启 PG</b>",
      fs=11.5, color=DIM, lh=1.62),
    # Right: HTTP API
    R("cc-r-bg", 752, 204, 432, 344, fill=PANEL, stroke=EDGE, radius=12),
    T("cc-r-h", 772, 216, 400, 22, "HTTP 双端口  http/server.rs:38", fs=13, fw=800, color=AC2),
    T("cc-r-b", 772, 244, 396, 296,
      "<b style='color:" + FG + "'>3080 外部</b> —— 控制面 + 监控抓取<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/status</span> 状态机状态 · <span style='font-family:" + MONO + "'>/configure</span> 下发 spec<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/terminate</span> 停机 · <span style='font-family:" + MONO + "'>/promote</span> 副本升主<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/check_writability</span> 可写探活<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/dbs_and_roles</span> <span style='font-family:" + MONO + "'>/database_schema</span><br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/lfc/prewarm</span> <span style='font-family:" + MONO + "'>/lfc/offload</span><br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/metrics</span> <span style='font-family:" + MONO + "'>/autoscaling_metrics</span>"
      "<span style='color:" + FAINT + "'>（免鉴权）</span><br><br>"
      "<b style='color:" + FG + "'>3081 内部</b> —— neon 扩展 / local_proxy<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/extensions</span> 装扩展 · <span style='font-family:" + MONO + "'>/grants</span> 补授权<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/extension_server/{file}</span> 拉扩展文件<br>"
      "&nbsp;<span style='font-family:" + MONO + "'>/refresh_configuration</span> 自触发重配<br>"
      "<span style='color:" + AC2 + ";font-size:10px'>⚠ 实测绑 <span style='font-family:" + MONO + "'>::</span>(0.0.0.0) 且免鉴权，"
      "注释里 TODO 想改回 loopback 未落地（server.rs:194-197）</span>",
      fs=11, color=DIM, lh=1.5),
    # Bottom band
    R("cc-b-bg", 96, 560, 1088, 96, fill="rgba(124,179,244,0.06)", stroke="rgba(124,179,244,0.3)", radius=10),
    T("cc-b-h", 116, 572, 900, 20, "核心数据结构", fs=13, fw=800, color="#7CB3F4"),
    T("cc-b-b", 116, 598, 1048, 50,
      "• <span style='font-family:" + MONO + "'>ComputeNodeParams</span>(compute.rs:85) 命令行来的静态参数 ｜ "
      "<span style='font-family:" + MONO + "'>ComputeNode</span>(:139) 全局单例，内含 <span style='font-family:" + MONO + "'>Mutex&lt;ComputeState&gt;</span>(:173) ｜ "
      "<span style='font-family:" + MONO + "'>ParsedSpec</span>(:254) 校验并解出 tenant/timeline 后的 spec<br>"
      "• 顺带管的周边：<span style='font-family:" + MONO + "'>pgbouncer</span> 参数下发、local_proxy 配置、swap/磁盘扩容、LFC prewarm/offload",
      fs=12, color=DIM, lh=1.62),
], p, notes="compute_ctl 是 compute 容器的 entrypoint（Docker entrypoint 或 systemd ExecStart），是 Pod 里的 1 号/监护进程，postgres 是它 fork 的子进程。源码 compute_tools crate，入口 bin/compute_ctl.rs（main 在 :213），核心逻辑 compute_tools/src/compute.rs。职责一句话：把控制面给的 ComputeSpec 翻译成一个连好存储、建好库和角色的可用 PG。启动流程 ComputeNode::run() compute.rs:627：① 起两个 HTTP server，external 3080（compute_ctl.rs:78）给控制面和监控，internal 3081（:83）给 neon 扩展和 local_proxy；② wait_spec()(:752)，spec 可以启动时用 CLI 参数带进来，也可以阻塞等控制面 POST /configure 推过来；③ start_compute()(:793) 冷启动：下载 remote extensions → prepare_pgdata()(:1601) 清空 pgdata、写 postgresql.conf、sync safekeepers 确定起点 LSN、拉 basebackup tarball 解压、写 pg_hba → 调整 swap/磁盘 → 起 monitor 和 configurator 线程 → start_postgres()(:1789) fork postgres → configure_as_primary()(:2179) 调 apply_config()(:1972) 按 ApplySpecPhase 各阶段建 role/database/extension，最后（在 extension phase 之后）跑 bootstrap template（spec_apply.rs:358）；④ 状态置 Running(:1039)，起 vm-monitor；⑤ 等 postgres 退出后清理，失败时多等 30s 方便抓日志。热变更走 configurator 线程（configurator.rs:13 configurator_main_loop）常驻循环，等到 ConfigurationPending 或 RefreshConfigurationPending 就调 reconfigure()(compute.rs:2089)，重写 postgresql.conf + pg_reload_conf + 重放 spec SQL，不重启 PG。HTTP 路由定义在 http/server.rs:38-49，外部路由 :94-127，内部路由 :66-84；/metrics 和 /autoscaling_metrics 免鉴权，其余外部路由要鉴权；内部还有 /failpoints 仅测试构建开放。⚠ 3081 端口实际绑定 Ipv6Addr::UNSPECIFIED（http/server.rs:196，等价于双栈 :: / 0.0.0.0），并非注释所说的 loopback；:194-195 有 TODO 说明是因为 GitHub Actions runner 不允许绑 localhost 才临时放开，一直未改回。内部 router（:64-87）也没挂 AsyncRequireAuthorizationLayer，所以 /extensions /grants /refresh_configuration /extension_server/* 事实上暴露给整个 Pod 网络且免鉴权，安全靠部署侧 NetworkPolicy 兜底。pgxn/neon 里 curl 目标虽然写的 http://localhost:{neon.extension_server_port}/...（extension_server.c:49、libpagestore.c:1078），但那只是客户端选择走 loopback，服务端并没做绑定收敛。核心结构体：ComputeNodeParams(compute.rs:85) 静态 CLI 参数、ComputeNode(:139) 全局单例内含 Mutex<ComputeState>(:173) 存 status/pspec/metrics、ParsedSpec(:254) 是校验并解出 tenant_id/timeline_id 后的 spec。本页只讲总览，具体细节分散在相邻各页：状态机（11 个状态，responses.rs:174）在下一页，ComputeSpec 字段在 s-compute-spec，basebackup 在 s-basebackup，bootstrap template 在 s-boot，DDL 反向同步在 s-ddl-fwd。")

# ─────── Slide 5.6: 3081 内部端口的两类调用方 ───────
p += 1
std("s-cc-internal", "COMPUTE", "内部端口 3081 —— 4 个路由，两类调用方", [
    T("ci-desc", 96, 162, 1088, 34,
      "PG 后端（backend / bgworker）靠 GUC <span style='font-family:" + MONO + "'>neon.extension_server_port</span> 找到 3081，"
      "该 GUC 由 compute_ctl 启动时写进 postgresql.conf（<span style='color:" + DIM + "'>compute_tools/src/config.rs:345</span>），"
      "然后用 <b>libcurl</b> 回调。<b style='color:" + AC2 + "'>4 个路由里 Postgres 只用其中 2 个。</b>",
      fs=12, color=DIM, lh=1.5),
    # Left: the two routes Postgres itself calls
    R("ci-l-bg", 96, 204, 700, 348, fill="rgba(0,229,153,0.055)", stroke="rgba(0,229,153,0.3)", radius=12),
    T("ci-l-h", 116, 216, 660, 22, "① Postgres（pgxn/neon 扩展）主动调 —— 只有这两个", fs=13.5, fw=800, color=AC),
    T("ci-l-b", 116, 246, 660, 294,
      "<b style='color:" + FG + "'>POST /extension_server/{filename}</b>"
      "<span style='color:" + FAINT + "'>　pgxn/neon/extension_server.c:33</span><br>"
      "&nbsp;· <span style='font-family:" + MONO + "'>neon_download_extension_file_http</span>，挂在 "
      "<span style='font-family:" + MONO + "'>download_extension_file_hook</span> 上（:110-111）<br>"
      "&nbsp;· <b>时机</b>：执行 <span style='font-family:" + MONO + "'>CREATE EXTENSION xxx</span>（或 PG 加载扩展库）时，本地 "
      "<span style='font-family:" + MONO + "'>$PGSHAREDIR/extension/xxx--*.sql</span> / "
      "<span style='font-family:" + MONO + "'>$PKGLIBDIR/xxx.so</span> 不存在 → PG 走 hook → "
      "compute_ctl 从对象存储把扩展文件拉下来塞进容器 FS，PG 再重试 open<br>"
      "&nbsp;· 每个 SQL / so 文件一次请求，<span style='font-family:" + MONO + "'>?is_library=true</span> 区分二进制<br><br>"
      "<b style='color:" + FG + "'>POST /refresh_configuration</b>"
      "<span style='color:" + FAINT + "'>　pgxn/neon/libpagestore.c:1058</span><br>"
      "&nbsp;· <span style='font-family:" + MONO + "'>hadron_request_configuration_refresh</span>，"
      "<b>仅在 lakebase_mode</b>（Hadron fork 的 GUC）下启用（:1065）<br>"
      "&nbsp;· <b>时机</b>：backend 跟 pageserver 掉线或读到异常，怀疑自己被路由到了<b>错误的 PS</b>"
      "（比如那台是 secondary）→ 主动「戳」一下 compute_ctl，让它去问控制面拉新 spec<br>"
      "&nbsp;· 4 处触发：<span style='font-family:" + MONO + "'>:1367</span> EOF · "
      "<span style='font-family:" + MONO + "'>:1374</span> 读 COPY 失败 · "
      "<span style='font-family:" + MONO + "'>:1381</span> 意外返回码 · "
      "<span style='font-family:" + MONO + "'>:1390</span> 上层收尾<br>"
      "&nbsp;· <b style='color:" + AC2 + "'>best-effort</b>：3s 超时，失败只记 WARNING，"
      "连续失败超过阈值才 cancel 当前 query",
      fs=11, color=DIM, lh=1.52),
    # Right: local_proxy's two routes
    R("ci-r-bg", 812, 204, 372, 348, fill="rgba(200,158,255,0.06)", stroke="rgba(200,158,255,0.3)", radius=12),
    T("ci-r-h", 832, 216, 332, 22, "② 不是 Postgres 调的 —— local_proxy", fs=13, fw=800, color="#C89EFF"),
    T("ci-r-b", 832, 246, 332, 294,
      "<b style='color:" + FG + "'>POST /extensions</b><br>"
      "&nbsp;装 <span style='font-family:" + MONO + "'>pg_session_jwt</span> 0.3.1 到 schema "
      "<span style='font-family:" + MONO + "'>auth</span><br><br>"
      "<b style='color:" + FG + "'>POST /grants</b><br>"
      "&nbsp;给 JWKS 里声明的 role 补 schema 授权<br><br>"
      "<b>调用方</b>：local_proxy —— Neon Auth / serverless driver 在 Pod 内的边车<br>"
      "<b>时机</b>：<span style='font-family:" + MONO + "'>connect_to_local_postgres</span> 对某个库<b>首次</b>建连接池时，"
      "各 db 一次，走信号量串行<br>"
      "<span style='color:" + FAINT + "'>proxy/src/serverless/backend.rs:311-341</span><br><br>"
      "要求 compute 已在 <b style='color:" + AC + "'>Running</b>，否则 <span style='font-family:" + MONO + "'>/extensions</span> 直接拒<br>"
      "<span style='color:" + FAINT + "'>compute_tools/…/routes/extensions.rs:19</span>",
      fs=11, color=DIM, lh=1.52),
    # Bottom band
    R("ci-b-bg", 96, 564, 1088, 92, fill="rgba(255,158,138,0.07)", stroke="rgba(255,158,138,0.32)", radius=10),
    T("ci-b-h", 116, 576, 900, 20, "⚠ 「内部」只是命名，不是隔离", fs=13, fw=800, color=AC2),
    T("ci-b-b", 116, 602, 1048, 46,
      "• 客户端侧确实打 <span style='font-family:" + MONO + "'>http://localhost:{neon.extension_server_port}/…</span>"
      "（extension_server.c:49、libpagestore.c:1078），但那只是<b>调用方选择</b>走 loopback<br>"
      "• 服务端实测绑 <span style='font-family:" + MONO + "'>Ipv6Addr::UNSPECIFIED</span>（<span style='font-family:" + MONO + "'>::</span> / 0.0.0.0，server.rs:196-197），"
      "内部 router（:64-87）<b>也没挂鉴权层</b> → 4 个路由对整个 Pod 网络可达且免鉴权，只能靠部署侧 <b>NetworkPolicy</b> 兜底",
      fs=11.5, color=DIM, lh=1.6),
], p, notes="本页把 3081 内部端口的 4 个路由按调用方分成两类，要点：3081 不等于「Postgres 专用端口」，Postgres 只用其中 2 个。端口发现机制：compute_ctl 启动时把 internal http port 写成 GUC neon.extension_server_port 进 postgresql.conf（compute_tools/src/config.rs:345），PG 后端（普通 backend 或 bgworker）读这个 GUC 拿到端口，用 libcurl 发 HTTP。第一类，Postgres 自己调的两个：（1）POST /extension_server/{filename}，实现在 pgxn/neon/extension_server.c:33 neon_download_extension_file_http，通过 :110-111 挂在 PG 的 download_extension_file_hook 上。触发时机是用户执行 CREATE EXTENSION xxx，或者 PG 需要加载某个扩展的动态库时，发现本地 $PGSHAREDIR/extension/xxx--*.sql 或 $PKGLIBDIR/xxx.so 不存在，于是走 hook，hook 请求 compute_ctl 从对象存储（remote extension storage）把文件下载下来写进容器文件系统，PG 再重试 open。粒度是每个 SQL 文件或 so 文件一次请求，查询参数 ?is_library=true 用来区分二进制库和 SQL 脚本，60s 超时。（2）POST /refresh_configuration，实现在 pgxn/neon/libpagestore.c:1058 hadron_request_configuration_refresh，只在 lakebase_mode 这个 Hadron fork 引入的 GUC 打开时才启用（:1065 判断）。触发时机是 Postgres backend 跟 pageserver 的连接掉线或者读到异常响应，backend 怀疑自己被路由到了错误的 pageserver（典型是那台 PS 现在只是 secondary，或者分片映射已经变了），于是主动「戳」一下 compute_ctl，让 compute_ctl 去问控制面重新拉一份 spec。libpagestore.c 里有 4 处调用它：:1367 读到 EOF、:1374 读 COPY 数据失败、:1381 收到意外返回码、:1390 上层收尾时兜底。这条路径是 best-effort 的：3s 超时，失败只打 WARNING 不报错，只有连续失败超过阈值才会 cancel 当前 query。第二类，不是 Postgres 调的：/extensions 和 /grants 是 local_proxy 调的。local_proxy 是 Neon Auth / serverless driver 在 Pod 内的边车进程，在 proxy/src/serverless/backend.rs:311-341 的 connect_to_local_postgres 里，对某个 database 第一次建连接池时调这两个接口：/extensions 安装 pg_session_jwt 扩展（版本 0.3.1，装到 schema auth，常量在 local_conn_pool.rs:44-46），/grants 给 JWKS 配置里声明的 role 补 schema 授权。每个 db 只做一次，并且用信号量限并发。/extensions 的 handler 要求 compute 状态必须是 Running（routes/extensions.rs:19），否则直接拒。最后一个要点，「内部」只是命名不是隔离：pgxn 里 curl 的目标 URL 确实写的是 http://localhost:{port}（extension_server.c:49、libpagestore.c:1078），但那只是客户端选择走 loopback；服务端 ip() 函数对 external 和 internal 两个 server 都返回 Ipv6Addr::UNSPECIFIED（http/server.rs:196-197，等价于 :: / 0.0.0.0），:194-195 的 TODO 注释说明是因为 GitHub Actions runner 不允许绑 localhost 才临时放开、一直没改回；而且内部 router（:64-87）没有挂 AsyncRequireAuthorizationLayer。两者叠加的结果是这 4 个路由对整个 Pod 网络可达且免鉴权，安全性只能靠部署侧 NetworkPolicy 兜底。")

# ─────── Slide 5.7: Compute VM 进程清单 ───────
p += 1
std("s-cc-procs", "COMPUTE", "Compute VM 里都有哪些常驻进程", [
    T("cp-desc", 96, 162, 1088, 36,
      "以 <span style='font-family:" + MONO + "'>compute_ctl</span> 为 <b>PID 1</b>，postgres 是它 fork 的子进程；其余守护进程由 "
      "<span style='font-family:" + MONO + "'>sysvInitAction: respawn</span> 拉起，源码见 "
      "<span style='color:" + DIM + "'>compute/vm-image-spec-bookworm.yaml</span>。",
      fs=12, color=DIM, lh=1.5),
    # Group A: 主线 (compute_ctl + postgres)
    R("cp-a-bg", 96, 204, 348, 180, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=12),
    T("cp-a-h", 116, 216, 308, 22, "主线（PID 1 → child）", fs=13, fw=800, color=AC),
    T("cp-a-b", 116, 244, 308, 130,
      "<b style='color:" + FG + "'>compute_ctl</b>（PID 1，Pod entrypoint）<br>"
      "&nbsp;· 监护、状态机、HTTP 3080/3081<br>"
      "&nbsp;· 源码 <span style='font-family:" + MONO + "'>compute_tools/</span>，入口 "
      "<span style='font-family:" + MONO + "'>bin/compute_ctl.rs</span><br><br>"
      "<b style='color:" + FG + "'>postgres</b>（postmaster + backends）<br>"
      "&nbsp;· 5432，compute_ctl fork 的孙进程<br>"
      "&nbsp;· pgxn/neon 扩展在这里加载",
      fs=11, color=DIM, lh=1.55),
    # Group B: 连接接入层
    R("cp-b-bg", 456, 204, 344, 180, fill="rgba(200,158,255,0.06)", stroke="rgba(200,158,255,0.3)", radius=12),
    T("cp-b-h", 476, 216, 304, 22, "连接接入层", fs=13, fw=800, color="#C89EFF"),
    T("cp-b-b", 476, 244, 304, 130,
      "<b style='color:" + FG + "'>pgbouncer</b>　<span style='color:" + FAINT + "'>0.0.0.0:6432</span><br>"
      "&nbsp;· transaction pooling，max_client_conn=10000<br>"
      "&nbsp;· 配置 <span style='font-family:" + MONO + "'>compute/etc/pgbouncer.ini</span><br><br>"
      "<b style='color:" + FG + "'>local_proxy</b>　<span style='color:" + FAINT + "'>0.0.0.0:10432</span><br>"
      "&nbsp;· Neon Authorize：验 JWT + 管 "
      "<span style='font-family:" + MONO + "'>pg_session_jwt</span><br>"
      "&nbsp;· 只对开了 Auth 的项目起作用",
      fs=11, color=DIM, lh=1.55),
    # Group C: 指标 exporter
    R("cp-c-bg", 812, 204, 372, 180, fill="rgba(124,179,244,0.06)", stroke="rgba(124,179,244,0.3)", radius=12),
    T("cp-c-h", 832, 216, 332, 22, "指标导出（Prometheus）", fs=13, fw=800, color="#7CB3F4"),
    T("cp-c-b", 832, 244, 332, 130,
      "<b style='color:" + FG + "'>postgres-exporter</b>　<span style='color:" + FAINT + "'>PG → Prom</span><br>"
      "&nbsp;· <span style='font-family:" + MONO + "'>--no-collector.database</span> 关库大小采集<br>"
      "<b style='color:" + FG + "'>pgbouncer-exporter</b>　<span style='color:" + FAINT + "'>pgbouncer → Prom</span><br>"
      "<b style='color:" + FG + "'>sql-exporter</b>　<span style='color:" + FAINT + "'>:9399</span> 通用 SQL 指标<br>"
      "<b style='color:" + FG + "'>sql-exporter-autoscaling</b>　"
      "<span style='color:" + FAINT + "'>:9499</span> 给 autoscaler 用",
      fs=11, color=DIM, lh=1.55),
    # Group D: sysinit (一次性)
    R("cp-d-bg", 96, 400, 348, 168, fill="rgba(255,158,138,0.06)", stroke="rgba(255,158,138,0.3)", radius=12),
    T("cp-d-h", 116, 412, 308, 22, "启动一次性（sysinit）", fs=13, fw=800, color=AC2),
    T("cp-d-b", 116, 440, 308, 118,
      "<b style='color:" + FG + "'>cgconfigparser</b> 建 cgroup <span style='font-family:" + MONO + "'>neon-postgres</span><br>"
      "<b style='color:" + FG + "'>chmod-resize-swap</b> 收紧 <span style='font-family:" + MONO + "'>/neonvm/bin/resize-swap</span><br>"
      "<b style='color:" + FG + "'>chmod-set-disk-quota</b> 同上（磁盘配额脚本）<br>"
      "<b style='color:" + FG + "'>rsyslogd-socket-symlink</b> "
      "<span style='font-family:" + MONO + "'>/dev/log →</span> pg 侧管道",
      fs=11, color=DIM, lh=1.55),
    # Group E: compute_ctl 内嵌任务
    R("cp-e-bg", 456, 400, 344, 168, fill="rgba(255,255,255,0.045)", stroke=EDGE, radius=12),
    T("cp-e-h", 476, 412, 304, 22, "compute_ctl 内嵌线程 / task", fs=13, fw=800, color=FG),
    T("cp-e-b", 476, 440, 304, 118,
      "<b>HTTP servers</b> 3080 / 3081（http/server.rs）<br>"
      "<b>configurator</b> 热变更循环（configurator.rs:13）<br>"
      "<b>compute-monitor</b> 追踪最近活跃时间戳<br>"
      "<b>vm-monitor</b> <span style='color:" + FAINT + "'>libs/vm_monitor</span>，仅当 "
      "<span style='font-family:" + MONO + "'>AUTOSCALING</span> 环境变量置位时起<br>"
      "&nbsp;· 跟 autoscaler 协商扩缩容",
      fs=11, color=DIM, lh=1.55),
    # Group F: 日志
    R("cp-f-bg", 812, 400, 372, 168, fill="rgba(154,169,191,0.06)", stroke=EDGE, radius=12),
    T("cp-f-h", 832, 412, 332, 22, "日志", fs=13, fw=800, color=FG),
    T("cp-f-b", 832, 440, 332, 118,
      "<b style='color:" + FG + "'>rsyslogd</b> —— PG/组件日志汇聚<br>"
      "&nbsp;· PG 通过 <span style='font-family:" + MONO + "'>/dev/log</span>（软链到 "
      "<span style='font-family:" + MONO + "'>rsyslogpipe</span>）写入<br>"
      "&nbsp;· 其它守护把 <span style='font-family:" + MONO + "'>stderr</span> 直接重定向到<br>"
      "&nbsp;&nbsp;&nbsp;<span style='font-family:" + MONO + "'>/dev/virtio-ports/tech.neon.log.0</span><br>"
      "&nbsp;&nbsp;&nbsp;（VM host 侧收）",
      fs=11, color=DIM, lh=1.55),
    # Bottom band
    R("cp-b2-bg", 96, 584, 1088, 72, fill="rgba(0,229,153,0.05)", stroke="rgba(0,229,153,0.28)", radius=10),
    T("cp-b2-h", 116, 596, 900, 20, "小结", fs=13, fw=800, color=AC),
    T("cp-b2-b", 116, 620, 1048, 30,
      "客户端流量 <b>入口链</b>：<span style='font-family:" + MONO + "'>proxy →</span>（可选 <span style='font-family:" + MONO + "'>local_proxy →</span>）<span style='font-family:" + MONO + "'>pgbouncer → postgres</span>&nbsp;&nbsp;｜&nbsp;&nbsp;"
      "<b>控制面链</b>：<span style='font-family:" + MONO + "'>compute_ctl :3080/:3081</span>&nbsp;&nbsp;｜&nbsp;&nbsp;"
      "<b>观测</b> 4 个 exporter + rsyslog",
      fs=11.5, color=DIM, lh=1.4),
], p, notes="本页把 compute VM 内所有常驻和一次性进程列全，来源是 compute/vm-image-spec-bookworm.yaml（vm-image-spec-bullseye.yaml 内容对齐）。9 个常驻守护进程（sysvInitAction: respawn）：（1）compute_ctl 是 Pod entrypoint / PID 1，由 VM entrypoint 直接拉起，不在 vm-image-spec 的 commands 列表里；负责监护、状态机、HTTP 3080/3081，源码在 compute_tools/ crate，入口 bin/compute_ctl.rs。（2）postgres 是 compute_ctl fork 出来的子进程，跑 postmaster + backends + bgworkers，pgxn/neon 扩展在这里加载，监听 5432。（3）pgbouncer 监听 0.0.0.0:6432，transaction pooling，配置见 compute/etc/pgbouncer.ini，max_client_conn=10000、default_pool_size=64、auth_type=scram-sha-256，通过 unix_socket_dir=/tmp/ 也暴露 socket。（4）local_proxy 监听 0.0.0.0:10432，Neon Authorize 组件，校验客户端 JWT、维护 pg_session_jwt 扩展和 JWKS 授权，reload 通过 SIGHUP（compute_tools/src/local_proxy.rs）；只有开了 Neon Auth 的项目才实际用到，但进程本身对所有 compute 常驻。（5）postgres-exporter Prometheus PG 指标；启动参数 --no-collector.database 关掉 pg_database_size_bytes 采集（会因为坏 db 打爆日志），DATA_SOURCE_NAME 走 cloud_admin@postgres 本地 socket。（6）pgbouncer-exporter Prometheus pgbouncer 指标，通过 unix socket 连 pgbouncer。（7）sql-exporter 监听 :9399，跑通用 SQL-based 指标采集（Neon 定义的 collector 集合）。（8）sql-exporter-autoscaling 监听 :9499，给 autoscaler 拉的一份专用指标（LFC hit/miss、working set size 等）。（9）rsyslogd 用 postgres 用户跑（这样能写自己的 pid 文件），配置 /etc/compute_rsyslog.conf，Postgres 通过 /dev/log 软链到 /var/db/postgres/rsyslogpipe 写日志。4 个 sysinit（只在启动阶段跑一次，不常驻）：cgconfigparser 建 cgroup neon-postgres（vm-monitor 靠这个做资源限制），chmod-resize-swap 和 chmod-set-disk-quota 把这两个特权脚本改成 0711（compute_ctl 通过 sudoers 白名单以 root 跑它们，其他人只能执行不能读），rsyslogd-socket-symlink 建 /dev/log → rsyslogpipe 软链。compute_ctl 进程内还嵌着几个 tokio task / 后台线程，它们不是独立进程但常驻：两个 HTTP server（external 3080、internal 3081，http/server.rs），configurator 热变更循环（configurator.rs:13 configurator_main_loop 等 ConfigurationPending / RefreshConfigurationPending），compute-monitor（源码注释里叫 compute-monitor，跟踪 PG 最近活跃时间戳），vm-monitor（libs/vm_monitor，仅当 AUTOSCALING 环境变量置位时才起，只 linux 上跑，需要 cgroup v2，跟 VM autoscaling 协议协商 downscale / 请求 upscale）。数据面调用链：客户端 → proxy → 可选 local_proxy → pgbouncer → postgres（5432）；控制面：cplane → compute_ctl 3080（JWT），Pod 内 neon 扩展 / local_proxy → compute_ctl 3081（无鉴权）；观测：4 个 exporter + rsyslog；日志 stderr 走 virtio-port /dev/virtio-ports/tech.neon.log.0，PG 走 syslog 管道。")

# ─────── Slide 6: Compute 状态机 ───────
p += 1
std("s-comp-sm", "COMPUTE", "compute_ctl 状态机 —— ComputeStatus 全 11 态", [
    T("sm-desc", 96, 150, 1088, 34,
      "这是 <b>compute_ctl 进程内部</b>的状态（<span style='font-family:" + MONO + "'>ComputeStatus</span>，"
      "<span style='color:" + DIM + "'>libs/compute_api/src/responses.rs:174</span>），"
      "不是控制面侧 endpoint 的 init/active/suspended 状态。",
      fs=12, color=DIM, lh=1.5),
    # start pseudo-state
    CIRC("sm-start", 154, 190, 16, 16, fill="rgba(232,237,244,0.9)", stroke="rgba(232,237,244,0.4)", sw=2),
    T("sm-start-l", 176, 190, 120, 16, "compute spawned", fs=9.5, fw=600, color=FAINT),
    LN("sm-a0", 162, 206, 0, 60, sw=2),
    # Empty
    R("sm-empty", 112, 272, 104, 42, fill="rgba(255,255,255,0.07)", stroke=EDGE, radius=10),
    T("sm-empty-t", 112, 272, 104, 42, "Empty", fs=13, fw=700, color=FG, align="center", valign="middle"),
    LN("sm-a1", 216, 282, 36, -52, sw=2),
    LN("sm-a2", 216, 304, 36, 52, sw=2),
    # ConfigurationPending / Configuration (spec 后到)
    R("sm-cp", 256, 196, 190, 42, fill="rgba(255,158,138,0.11)", stroke="rgba(255,158,138,0.42)", radius=10),
    T("sm-cp-t", 256, 196, 190, 42, "ConfigurationPending", fs=12, fw=700, color=AC2, align="center", valign="middle"),
    LN("sm-a3", 446, 217, 36, 0, sw=2),
    R("sm-cf", 486, 196, 160, 42, fill="rgba(255,158,138,0.11)", stroke="rgba(255,158,138,0.42)", radius=10),
    T("sm-cf-t", 486, 196, 160, 42, "Configuration", fs=12, fw=700, color=AC2, align="center", valign="middle"),
    LN("sm-a4", 646, 217, 46, 51, sw=2),
    # Init (spec 已就绪)
    R("sm-init", 256, 352, 190, 42, fill="rgba(124,179,244,0.1)", stroke="rgba(124,179,244,0.4)", radius=10),
    T("sm-init-t", 256, 352, 190, 42, "Init", fs=13, fw=700, color="#7CB3F4", align="center", valign="middle"),
    LN("sm-a5", 446, 373, 36, 0, sw=2),
    LN("sm-a6", 446, 358, 244, -62, sw=2),
    # Failed
    LN("sm-a7", 566, 238, 0, 110, sw=2),
    T("sm-a7-l", 574, 274, 100, 16, "配置失败", fs=10, fw=600, color="#FF8080"),
    R("sm-fail", 486, 352, 160, 42, fill="rgba(255,80,80,0.1)", stroke="rgba(255,80,80,0.42)", radius=10),
    T("sm-fail-t", 486, 352, 160, 42, "Failed", fs=13, fw=700, color="#FF7070", align="center", valign="middle"),
    # Running
    R("sm-run", 696, 272, 124, 44, fill="rgba(0,229,153,0.14)", stroke="rgba(0,229,153,0.55)", radius=10),
    T("sm-run-t", 696, 272, 124, 44, "Running", fs=14, fw=800, color=AC, align="center", valign="middle"),
    # Running -> ConfigurationPending (/configure 带 spec)
    LN("sm-a8", 698, 276, -246, -36, sw=2, dashed=True),
    # Termination group
    R("sm-tg", 866, 186, 306, 112, fill="rgba(255,80,80,0.055)", stroke="rgba(255,80,80,0.26)", radius=12),
    R("sm-tf", 876, 196, 286, 40, fill="rgba(255,80,80,0.1)", stroke="rgba(255,80,80,0.4)", radius=9),
    T("sm-tf-t", 876, 196, 286, 40, "TerminationPendingFast", fs=11.5, fw=700, color="#FF8080", align="center", valign="middle"),
    R("sm-ti", 876, 246, 286, 40, fill="rgba(255,80,80,0.1)", stroke="rgba(255,80,80,0.4)", radius=9),
    T("sm-ti-t", 876, 246, 286, 40, "TerminationPendingImmediate", fs=11.5, fw=700, color="#FF8080", align="center", valign="middle"),
    LN("sm-a9", 820, 282, 52, -66, sw=2),
    LN("sm-a10", 820, 290, 52, -24, sw=2),
    LN("sm-a11", 1056, 298, 0, 28, sw=2),
    R("sm-term", 956, 330, 200, 42, fill="rgba(255,80,80,0.14)", stroke="rgba(255,80,80,0.5)", radius=10),
    T("sm-term-t", 956, 330, 200, 42, "Terminated", fs=13, fw=800, color="#FF8080", align="center", valign="middle"),
    T("sm-term-n", 876, 378, 300, 34,
      "Fast 停 PG 后<b>再等 30s</b> 给控制面看状态<br>Immediate 立即返回",
      fs=10, color=FAINT, align="center", lh=1.5),
    # Refresh 子环
    LN("sm-a12", 710, 316, -30, 150, sw=2),
    LN("sm-a13", 546, 394, -20, 72, sw=2),
    R("sm-rcp", 430, 470, 256, 44, fill="rgba(124,179,244,0.1)", stroke="rgba(124,179,244,0.42)", radius=10),
    T("sm-rcp-t", 430, 470, 256, 44, "RefreshConfigurationPending", fs=11.5, fw=700, color="#7CB3F4", align="center", valign="middle"),
    LN("sm-a14", 686, 486, 46, 0, sw=2),
    LN("sm-a15", 736, 504, -48, 0, sw=2, dashed=True),
    R("sm-rc", 736, 470, 230, 44, fill="rgba(124,179,244,0.1)", stroke="rgba(124,179,244,0.42)", radius=10),
    T("sm-rc-t", 736, 470, 230, 44, "RefreshConfiguration", fs=12, fw=700, color="#7CB3F4", align="center", valign="middle"),
    LN("sm-a16", 890, 470, -80, -152, sw=2),
    T("sm-rc-n", 976, 470, 208, 44,
      "虚线 = 重配失败退回重试<br>成功则回到 Running",
      fs=10, color=FAINT, lh=1.5),
    # Bottom band
    R("sm-b-bg", 96, 540, 1088, 116, fill="rgba(0,229,153,0.05)", stroke="rgba(0,229,153,0.26)", radius=10),
    T("sm-b-h", 116, 550, 900, 20, "两个 pending 入口：谁能调、谁在调", fs=12.5, fw=800, color=AC),
    T("sm-b-b", 116, 574, 1048, 76,
      "<b>启动分叉</b>：spec 启动时就有 → <span style='font-family:" + MONO + "'>Empty→Init→Running</span>；要等控制面推 → "
      "<span style='font-family:" + MONO + "'>Empty→ConfigurationPending→Configuration→Running</span>。<br>"
      "<b style='color:" + AC2 + "'>→ ConfigurationPending</b>　由 <span style='font-family:" + MONO + "'>:3080/configure</span>（带 spec、要 JWT、阻塞）触发，"
      "前置状态只放行 <span style='font-family:" + MONO + "'>Empty | Running</span>（<span style='color:" + FAINT + "'>configure.rs:37</span>）。"
      "控制面下发 spec、PS/SK 拓扑回调、PS 巡检补偿都走这条。<br>"
      "<b style='color:#7CB3F4'>→ RefreshConfigurationPending</b>　由 <span style='font-family:" + MONO + "'>:3081/refresh_configuration</span>（不带 spec，compute 自己去拉）触发，"
      "放行 <span style='font-family:" + MONO + "'>Running | Failed | RefreshConfigurationPending</span>（<span style='color:" + FAINT + "'>compute.rs:2048</span>）。"
      "<b>目前只有 Postgres 自己在调</b>——控制面侧已全部切到 <span style='font-family:" + MONO + "'>/configure</span>。<br>"
      "<b style='color:#FF8080'>⚠ Failed 实际救不回来</b>：<span style='font-family:" + MONO + "'>reconfigure()</span> 只重写 conf + reload + 跑 SQL，"
      "<b>从不 start_postgres</b>；PG 没起来时必然失败并自旋，或因 <span style='font-family:" + MONO + "'>pageserver_conninfo</span> 未变被去重直接漂白成 Running。正道是 "
      "<span style='font-family:" + MONO + "'>/terminate</span> 后重建。",
      fs=10, color=DIM, lh=1.62),
], p, morph=True, notes="这是 compute_ctl 的状态机，跟控制面侧 endpoint 的 init/active/suspended/stopped/released 是两套完全不同的东西。枚举定义在 libs/compute_api/src/responses.rs:174-202，实例状态存在 ComputeState.status（compute_tools/src/compute.rs:176），初值 Empty（:215），所有迁移统一走 set_status（:229 内层 / :1178 外层封装），每次迁移都 notify_all 唤醒等在 state_changed 条件变量上的线程，外部通过 GET :3080/status 观测。官方图见 compute_tools/README.md:40-64，一共 11 个状态。11 个状态逐个说：Empty —— 启动时没带 spec，等控制面推；ConfigurationPending —— 收到了配置请求（有 spec），等 configurator 线程处理；Init —— spec 启动时就有，正在做首次启动和配置；Running —— 配好了在跑；Configuration —— 正在应用新 spec；Failed —— 启动或配置失败，compute 快要退出、或者等控制面来终止它；TerminationPendingFast —— 收到终止请求，停 PG 之后额外等 30s 再从 /terminate 返回，留窗口给控制面抓状态和日志；TerminationPendingImmediate —— 同上但不等那 30s，立即返回；Terminated —— PG 已停；RefreshConfigurationPending —— 有人请求刷新 spec；RefreshConfiguration —— 正在应用刷新（互斥，此时再来 signal_refresh_configuration 会返 500）。关键边：Empty 有三条出边——有 spec 直接 Init、没 spec 走 ConfigurationPending、也可以直接被 /terminate 打到 TerminationPending*（本页图上只画了 Running 的终止边）。Init 失败 → Failed，成功 → Running。Configuration 失败 → Failed，成功 → Running。两个 pending 入口的触发者：（1）ConfigurationPending 由 POST :3080/configure 触发，门槛 Empty | Running（configure.rs:37），控制面下发 spec、PS/SK 拓扑回调（notify-attach/notify-safekeepers）、PS 巡检补偿 job 都走这条路。（2）RefreshConfigurationPending 由 POST :3081/refresh_configuration 触发，门槛 Running | Failed | RefreshConfigurationPending（compute.rs:2048-2058），Init 静默忽略，其余报错。目前唯一还在调这个接口的是 Postgres 自己（pgxn/neon/libpagestore.c hadron_request_configuration_refresh，仅 lakebase_mode 生效），backend 跟 pageserver 交互异常时自触发（6 个调用点：:1169 重连超阈值、:1286 EOF、:1293 读 COPY 失败、:1299 意外返回码、:1390 上层兜底）；控制面侧的所有调用方已全部切到 /configure。RefreshConfiguration 成功回 Running，失败退回 RefreshConfigurationPending 重试（configurator.rs:159/181）。Failed → RefreshConfigurationPending 这条边状态机上允许但实际无法真正恢复：reconfigure()（compute.rs:2089-2176）全程假设 Postgres 在跑——只做重写 conf + pg_reload_conf + apply_spec_sql，从不 start_postgres；PG 没起来时这些操作必然失败并自旋在 RefreshConfigurationPending，或者因为新拉到的 spec 的 pageserver_conninfo 跟当前相同被 configurator.rs:125-138 的去重逻辑直接跳过、漂白成 Running 但 PG 仍然没启动。所以 Failed 的正道恢复路径是控制面识别 Failed 后走 /terminate → 重建（走完整冷启动 start_compute）。TerminationPendingFast 的 30s 不是等 PG 停，是 PG 已停完之后额外的观察窗口（compute.rs:1146-1155 delay_exit），给控制面时间抓状态和日志。")

# ─────── Slide 7: Bootstrap Template ───────
p += 1
std("s-boot", "COMPUTE", "Bootstrap Template 机制（本地 Fork 特性）", [
    T("boot-desc", 96, 170, 1088, 50,
      "首次启动时按序执行镜像内 SQL 脚本，实现类似 Supabase initial-schema 的自动初始化。",
      fs=16, color=DIM, lh=1.6),
    *card("bt1", 96, 240, 530, 260,
          "设计要点", [
              "• 脚本路径：/usr/local/share/compute-bootstrap/&lt;template&gt;/",
              "  └─ init-scripts/ + migrations/",
              "• spec 字段：bootstrap_template: Option&lt;String&gt;",
              "• 按文件名字典序执行（simple_query 整文件发送）",
              "• 文件名只允许 [A-Za-z0-9_-]（防路径穿越）",
              "• 执行位置：extension phase 之后",
              "• SAVEPOINT 探测事务泄漏",
          ], fs=14, headfs=16),
    *card("bt2", 660, 240, 530, 260,
          "幂等保证", [
              "• neon.compute_bootstrap 表：整模板 marker",
              "• neon.compute_bootstrap_scripts 表：",
              "  (template, script, applied_at, attempted_at, error)",
              "• 脚本级进度，失败后 scale-to-zero 重启续跑",
              "• 失败原因可通过 SQL 查询（解决 pod 日志丢失问题）",
              "",
              "git 4 连续 commit: 首版 → 续跑 → 记录 error → 事务泄漏修复",
          ], hc=AC2, fs=14, headfs=16),
], p, notes="Bootstrap Template：compute 首次启动执行内置 SQL，幂等表保证续跑，SAVEPOINT 防事务泄漏")


# ─────── basebackup ───────
p += 1
std("s-basebackup", "COMPUTE", "basebackup：无状态 Compute 的冷启动包", [
    T("bb-desc", 96, 168, 1088, 36,
      "Compute 本地无数据，启动时向 Pageserver 拉一个 tarball 现造 PGDATA 骨架。"
      "注意：与 PostgreSQL 的 <span style='font-family:" + MONO + "'>pg_basebackup</span> <b>毫无关系</b>（代码注释自己吐槽命名不好）。",
      fs=14, color=DIM, lh=1.5),
    # left: what's inside
    R("bb1-bg", 96, 214, 540, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("bb1-h", 116, 228, 500, 24, "tar 包里有什么（＝没有用户数据）", fs=16, fw=800, color=AC),
    T("bb1-b", 116, 262, 500, 240,
      "<b>只装非关系型数据</b>，关系文件一个都不带：<br>"
      "• <span style='font-family:" + MONO + "'>global/pg_control</span>　由 checkpoint 记录<b>现场合成</b><br>"
      "• SLRU：<span style='font-family:" + MONO + "'>pg_xact</span>（clog）、<span style='font-family:" + MONO + "'>pg_multixact/{offsets,members}</span><br>"
      "• 目录骨架 + <span style='font-family:" + MONO + "'>PG_VERSION</span> + <span style='font-family:" + MONO + "'>pg_filenode.map</span>（relmap）<br>"
      "• two-phase 文件（未决 2PC 事务）、aux files（含复制槽状态）<br>"
      "• <span style='font-family:" + MONO + "'>PGDATA_SPECIAL_FILES</span>、<span style='font-family:" + MONO + "'>pg_hba.conf</span><br>"
      "• <b>一个 dummy WAL segment</b> ＋ <span style='font-family:" + MONO + "'>neon.signal</span>/<span style='font-family:" + MONO + "'>zenith.signal</span><br>"
      "&nbsp;&nbsp;signal 里写 <span style='font-family:" + MONO + "'>PREV LSN: …</span>，供 PG 拼首条记录 xl_prev<br><br>"
      "<b>唯一的例外</b>：unlogged 表的 init fork 会带上，<br>"
      "&nbsp;&nbsp;且被<b>同时当 main fork 发一份</b>（PG 的 reinit.c 依赖它）",
      fs=11.5, color=DIM, lh=1.65),
    # right: mechanics
    R("bb2-bg", 656, 214, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("bb2-h", 676, 228, 490, 24, "怎么生成 / 怎么加速", fs=16, fw=800, color=AC2),
    T("bb2-b", 676, 262, 490, 240,
      "<span style='font-family:" + MONO + "'>send_basebackup_tarball(timeline, req_lsn, …)</span><br>"
      "&nbsp;&nbsp;所有内容都是从 layer 里 <b>GetPage 读出来现拼的</b><br>"
      "&nbsp;&nbsp;→ 所以能取<b>任意历史 LSN</b>，这正是分支/PITR 的地基<br><br>"
      "<b>prev_lsn 的限制</b>：PS 只留最新记录的前驱<br>"
      "&nbsp;&nbsp;→ 非时间线末尾取包时只能填 <span style='font-family:" + MONO + "'>Lsn(0)</span><br><br>"
      "<b>full_backup=true</b>（调试/导出）才连关系文件全带<br>"
      "<b>replica=true</b> 走 hot standby 变体<br>"
      "<b>gzip</b> 可选压缩<br><br>"
      "<b>BasebackupCache</b>：本地磁盘缓存成品 tar<br>"
      "&nbsp;&nbsp;固定参数组合（gzip=true, full=false, replica=false）<br>"
      "&nbsp;&nbsp;后台异步 prepare，命中则 scale-to-zero 唤醒更快",
      fs=11.5, color=DIM, lh=1.65),
    # bottom
    R("bb3-bg", 96, 528, 1088, 134, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("bb3-h", 116, 540, 600, 20, "为什么这样设计", fs=13, fw=800, color=AC),
    T("bb3-b", 116, 566, 1048, 88,
      "• <b>启动时间与数据量解耦</b>：包大小只随「库/表数量、SLRU 大小」增长，与实际数据体积无关 → TB 级库也能秒级起<br>"
      "• <b>关系数据留给 GetPage 按需拉</b>：真正用到的页才走网络，配合 LFC / prewarm 逐步变热<br>"
      "• <b>shard 0 必须自足</b>：dbdir、SLRU 等非 rel-block key 固定落 shard 0，所以出包只问 shard 0（见 Sharding 页）<br>"
      "• 代价：SLRU 很大时（长事务、海量 multixact）包会变大，冷启动变慢 —— 这也是 SLRU 分片/裁剪的动因",
      fs=12, color=DIM, lh=1.65),
], p, notes="basebackup 是无状态 compute 的冷启动包，与 pg_basebackup 无关（代码注释明确吐槽命名）。内容只有非关系型数据：现场合成的 global/pg_control、SLRU(pg_xact clog / pg_multixact offsets+members)、目录骨架+PG_VERSION+pg_filenode.map relmap、two-phase 文件、aux files、PGDATA_SPECIAL_FILES、pg_hba.conf、一个 dummy WAL segment、neon.signal 与 zenith.signal（写 PREV LSN 供 PG 拼 xl_prev）。唯一例外是 unlogged 表的 init fork 会带且同时当 main fork 发一份，因为 PG reinit.c 依赖。生成方式 send_basebackup_tarball，所有内容都是从 layer GetPage 现拼，所以能取任意历史 LSN，这是分支和 PITR 的地基。prev_lsn 限制：PS 只保留最新记录的前驱，非时间线末尾只能填 Lsn(0)。参数 full_backup 才带关系文件（调试导出用）、replica 走 hot standby 变体、gzip 可选。BasebackupCache 在本地磁盘缓存固定参数组合(gzip=true,full=false,replica=false)的成品 tar，后台异步 prepare，加速 scale-to-zero 唤醒。设计意义：启动时间与数据量解耦，包大小只随库表数量和 SLRU 大小增长；关系数据留给 GetPage 按需拉；shard 0 自足所以只问 shard 0。代价是 SLRU 大时包变大。代码：pageserver/src/basebackup.rs:102 send_basebackup_tarball，:788 signal 文件，pageserver/src/basebackup_cache.rs。")

# ─────── compute spec ───────
p += 1
std("s-compute-spec", "COMPUTE", "ComputeSpec：一份「期望状态」文档，热加载不重启", [
    T("cs-desc", 96, 168, 1088, 38,
      "ComputeSpec（<span style='font-family:" + MONO + "'>libs/compute_api/src/spec.rs:35</span>）是<b>声明式</b>的期望状态：谁来跑、连哪个存储、要哪些库/角色/参数。"
      "compute_ctl 拉取后按序 apply，改配置只 <span style='font-family:" + MONO + "'>pg_ctl reload</span>。",
      fs=13.5, color=DIM, lh=1.5),
    # left: what's in the spec
    R("cs1-bg", 96, 214, 540, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("cs1-h", 116, 228, 500, 24, "spec 里有什么（期望状态）", fs=16, fw=800, color=AC),
    T("cs1-b", 116, 262, 500, 244,
      "<b>集群终态</b> <span style='font-family:" + MONO + "'>cluster</span>：roles / databases /<br>"
      "&nbsp;&nbsp;postgresql.conf + settings（GenericOption 列表）<br>"
      "<b>命令式增量</b> <span style='font-family:" + MONO + "'>delta_operations</span>：DROP/RENAME 等<br>"
      "&nbsp;&nbsp;无法用静态终态表达的操作<br>"
      "<b>存储身份</b>：tenant_id / timeline_id / mode<br>"
      "&nbsp;&nbsp;（Primary / Replica / Static(lsn)）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>pageserver_connection_info</span>（分片连接描述）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>safekeeper_connstrings</span> + generation<br>"
      "<b>扩展/代理</b>：remote_extensions、pgbouncer_settings、<br>"
      "&nbsp;&nbsp;local_proxy_config（JWT 认证）<br>"
      "<b>行为开关</b>：skip_pg_catalog_updates、<br>"
      "&nbsp;&nbsp;drop_subscriptions_before_start、audit_log_level、<br>"
      "&nbsp;&nbsp;autoprewarm、<span style='font-family:" + MONO + "'>bootstrap_template</span>（首启脚本名）",
      fs=11.5, color=DIM, lh=1.62),
    # right: consumption phases
    R("cs2-bg", 656, 214, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("cs2-h", 676, 228, 490, 24, "compute_ctl 怎么消费（首启顺序）", fs=16, fw=800, color=AC2),
    T("cs2-b", 676, 262, 490, 244,
      "拉取：<span style='font-family:" + MONO + "'>GET /compute/api/v2/computes/{id}/spec</span><br>"
      "&nbsp;&nbsp;（<span style='font-family:" + MONO + "'>compute_tools/src/spec.rs:77</span>）<br>"
      "① 前置：下载 remote extensions、prepare_pgdata、<br>"
      "&nbsp;&nbsp;按需 resize swap / 设 disk quota<br>"
      "② prepare_pgdata：写 postgresql.conf → sync<br>"
      "&nbsp;&nbsp;safekeepers 取 LSN → 拉 basebackup → pg_hba<br>"
      "③ apply_spec_sql：<b>有序 phase</b> 建角色/库/扩展<br>"
      "&nbsp;&nbsp;（<span style='font-family:" + MONO + "'>spec_apply.rs</span> 的 ApplySpecPhase 枚举）<br>"
      "④ <span style='font-family:" + MONO + "'>bootstrap_template</span> 脚本<b>最后</b>跑<br>"
      "⑤ handle_migrations 异步执行（<b>不阻塞冷启动</b>）<br><br>"
      "reconfigure：活着时改配置，重跑 apply_spec_sql +<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>pg_ctl reload</span>，<b>不重启 Postgres</b>",
      fs=11.5, color=DIM, lh=1.62),
    # bottom band: butterfly generation + hot reload
    R("cs3-bg", 96, 528, 1088, 134, fill="rgba(255,158,138,0.06)", stroke="rgba(255,158,138,0.3)", radius=10),
    T("cs3-h", 116, 540, 900, 20, "Butterfly 怎么生成 & 两种下发", fs=13, fw=800, color=AC2),
    T("cs3-b", 116, 566, 1048, 88,
      "• <b>集中生成</b>：<span style='font-family:" + MONO + "'>lib_compute_spec.py</span> 的 get_compute_spec，先查 Redis 缓存否则现建并缓存；roles 从 SCRAM 密文、settings 按 ComputeFlavor 算内存/连接 GUC<br>"
      "• <b>拉（poll）</b>：<span style='font-family:" + MONO + "'>api_compute_spec.py</span> 直接把 spec 作为 HTTP body 返回 —— 正是 compute_ctl 轮询的那个 URL<br>"
      "• <b>推（push）</b>：<span style='font-family:" + MONO + "'>POST /configure</span>（全量、<b>阻塞</b>到 Running，角色/库变更立即生效）<br>&nbsp;&nbsp;vs <span style='font-family:" + MONO + "'>POST /refresh_configuration</span>（<b>非阻塞</b>，只比对 pageserver_conninfo，轻量 nudge）<br>"
      "• 版本：butterfly 侧 <span style='font-family:" + MONO + "'>spec_version/spec_changed_at</span> 注入 JSON（Rust struct 不含，serde 忽略未知字段），数据变更 bump_spec_version + 失效缓存",
      fs=11.5, color=DIM, lh=1.66),
], p, notes="ComputeSpec（libs/compute_api/src/spec.rs:35）是声明式期望状态文档。主要字段：cluster（Cluster spec.rs:524：roles/databases/postgresql_conf/settings GenericOption 列表）、delta_operations（DeltaOp DROP/RENAME 等命令式增量）、tenant_id/timeline_id、mode（ComputeMode Primary/Replica/Static(lsn) spec.rs:470）、pageserver_connection_info（分片连接 spec.rs:245，旧字段 pageserver_connstring）、safekeeper_connstrings + safekeepers_generation、storage_auth_token、remote_extensions（RemoteExtSpec）、pgbouncer_settings、local_proxy_config（JWT）、skip_pg_catalog_updates、reconfigure_concurrency、drop_subscriptions_before_start、audit_log_level、autoprewarm/offload_lfc_interval_seconds、suspend_timeout_seconds、bootstrap_template、format_version/operation_uuid/features。compute_ctl 消费：get_config_from_control_plane（compute_tools/src/spec.rs:77）GET {base}/compute/api/v2/computes/{compute_id}/spec。start_compute（compute.rs:793）：前置下载 remote extensions、prepare_pgdata、按需 swap resize/disk quota。prepare_pgdata（compute.rs:1601）写 postgresql.conf → sync safekeepers 取 LSN → 拉 basebackup → 更新 pg_hba/pg_ident。apply_config（compute.rs:1972）跑 apply_spec_sql（spec_apply.rs:40）驱动 ApplySpecPhase 有序枚举（CreatePrivilegedRole...CreateAndAlterRoles...CreateAndAlterDatabases...HandleNeonExtension...DropRoles...），bootstrap_template SQL 最后跑（spec_apply.rs:358 run_bootstrap_template:1381）；handle_migrations（spec_apply.rs:243）异步跑固定 append-only 迁移列表不阻塞冷启动。reconfigure（compute.rs:2089）活时改配置重跑 apply_spec_sql + pg_ctl reload 不重启。Butterfly 生成：lib_compute_spec.py:576 get_compute_spec 先 Redis 缓存否则 _build_spec_dict（504）组装，_build_roles（46）从 SCRAM 密文、_build_settings（218）按 ComputeFlavor calculate_pg_settings_for_memory 算 GUC，_build_pageserver_connection_info（465）建分片 map。下发两路：poll = api_compute_spec.py:163 GET spec 直接返回 body（compute_ctl 轮询该 URL）；push = lib_pod_runtime_configurator.py PodRuntimeConfigurator.configure 按 compute status 选 POST /configure（全量阻塞，port 3080，configure.rs:21，状态 ConfigurationPending 阻塞到 Running）或 POST /refresh_configuration（非阻塞，refresh_configuration.rs 只翻状态 RefreshConfigurationPending，configurator.rs 只比对 pageserver_conninfo 变才 reconfigure，port 3081）。configurator_main_loop（configurator.rs:13）监听两种 pending。角色/库变更必须 /configure 才立即生效（lib_compute_configure.py 注释 9-21）。版本：Endpoint.spec_version（models.py:324）emitted 为 spec_version/spec_changed_at 注入 JSON dict（lib_compute_spec.py:539），Rust ComputeSpec 只有 format_version:f32 和 operation_uuid，serde 忽略未知字段（spec.rs:38）；bump_spec_version（lib_endpoint_core.py:31）数据变更时 +1 并 mark_endpoint_spec_changed 失效 Redis 缓存。")

# ─────── Slide 8: LFC (Local File Cache) ───────
p += 1
std("s-lfc", "COMPUTE", "LFC：Local File Cache", [
    T("lfc-desc", 96, 170, 1088, 44,
      "Compute 本地磁盘上的页缓存，介于 shared_buffers 和 Pageserver 之间；"
      "<span style='font-family:" + MONO + "'>pgxn/neon/file_cache.c</span>",
      fs=14, color=DIM, lh=1.5),
    R("lfc1-bg", 96, 222, 530, 260, fill=PANEL, stroke=EDGE, radius=12),
    T("lfc1-h", 116, 238, 490, 24, "结构与读路径", fs=16, fw=800, color=AC),
    T("lfc1-b", 116, 272, 490, 200,
      "单文件存放所有 relation 页，用共享 hash map 按<br>"
      "<span style='font-family:" + MONO + "'>BufferTag</span> 寻址；<b>LRU</b> 淘汰，粒度=chunk<br>"
      "&nbsp;&nbsp;chunk = <b>128 页 = 1 MiB</b>（省 hash 内存 + 提升局部性）<br><br>"
      "读路径顺序：<br>"
      "shared_buffers → prefetch 结果 → <b>LFC</b> → Pageserver<br><br>"
      "启动时文件 <span style='font-family:" + MONO + "'>O_TRUNC</span> 重建，<b>不跨重启保留</b><br>"
      "临时/unlogged 表直接跳过 LFC",
      fs=12.5, color=DIM, lh=1.6),
    R("lfc2-bg", 656, 222, 530, 260, fill=PANEL, stroke=EDGE, radius=12),
    T("lfc2-h", 676, 238, 490, 24, "关键 GUC & 跨重启保温", fs=16, fw=800, color=AC2),
    T("lfc2-b", 676, 272, 490, 200,
      "<span style='font-family:" + MONO + "'>neon.max_file_cache_size</span>　硬上限(MB)，启动定<br>"
      "<span style='font-family:" + MONO + "'>neon.file_cache_size_limit</span>　软上限，可在线调<br>"
      "<span style='font-family:" + MONO + "'>neon.file_cache_path</span>　默认 file.cache<br><br>"
      "<b>Prewarm / Offload</b>（跨 suspend 保温）：<br>"
      "• get_local_cache_state() 导出 chunk-key 状态<br>"
      "• 压缩后上传到 endpoint storage（compute_prewarm.rs）<br>"
      "• 下次启动 autoprewarm=true 时下载并回放<br>"
      "• vm_monitor 据内存压力在线调 size_limit",
      fs=12.5, color=DIM, lh=1.6),
], p, notes="LFC 是 compute 本地磁盘页缓存，读路径 shared_buffers→prefetch→LFC→Pageserver。单文件+共享hash map+LRU，chunk=128页=1MiB。启动O_TRUNC重建不保留状态，靠 prewarm/offload 机制跨 suspend 保温：导出chunk-key状态压缩上传到endpoint storage，下次启动autoprewarm回放。GUC: max_file_cache_size硬上限, file_cache_size_limit软上限可在线调, file_cache_path默认file.cache")

# ─────── DDL Forwarding ───────
p += 1
std("s-ddl-fwd", "COMPUTE", "DDL Forwarding：库/角色变更实时联动控制面", [
    T("ddl-desc", 96, 164, 1088, 34,
      "用户直接跑 <span style='font-family:" + MONO + "'>CREATE DATABASE</span> / <span style='font-family:" + MONO + "'>DROP ROLE</span> 时，"
      "pgxn/neon 插件在<b>事务提交前</b>把变更 PATCH 给控制面，让控制台实时反映 db/role 状态。"
      "<span style='color:" + DIM + "'>pgxn/neon/neon_ddl_handler.c</span>",
      fs=12, color=DIM, lh=1.55),
    # Left card: capture mechanism
    R("ddl-l-bg", 96, 208, 530, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("ddl-l-h", 116, 220, 490, 22, "① 捕获：ProcessUtility_hook + 子事务栈", fs=14, fw=800, color=AC),
    T("ddl-l-b", 116, 250, 494, 250,
      "<b>ProcessUtility_hook</b> 拦截 DDL（neon_ddl_handler.c:1377）<br>"
      "&nbsp;&nbsp;→ 记录到 <b>DdlHashTable</b>（db_table + role_table）<br><br>"
      "<b>子事务用哈希表栈</b>处理 SAVEPOINT（:99）：<br>"
      "&nbsp;&nbsp;• START_SUB → PushTable（压栈）<br>"
      "&nbsp;&nbsp;• COMMIT_SUB → MergeTable（并入下层）<br>"
      "&nbsp;&nbsp;• ABORT_SUB → PopTable（丢弃）<br><br>"
      "<b>提交时发送</b>：NeonXactCallback 在<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>XACT_EVENT_PRE_COMMIT</span> 调 SendDeltas（:533）<br>"
      "<span style='color:" + AC2 + "'>⚠ 已知缺陷：转发后事务仍可能 abort，暂未处理（源码头注释）</span>",
      fs=11.5, color=DIM, lh=1.6),
    # Right card: HTTP protocol
    R("ddl-r-bg", 656, 208, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("ddl-r-h", 676, 220, 490, 22, "② 转发：HTTP PATCH 到控制面", fs=14, fw=800, color=AC2),
    T("ddl-r-b", 676, 250, 492, 250,
      "<span style='font-family:" + MONO + "'>PATCH {neon.console_url}?endpoint_id=ep-xxx</span><br>"
      "&nbsp;&nbsp;（curl，超时 3s，重试 5 次）<br>"
      "Auth：<span style='font-family:" + MONO + "'>Bearer</span> per-compute JWT<br>"
      "&nbsp;&nbsp;（env <span style='font-family:" + MONO + "'>NEON_CONTROL_PLANE_TOKEN</span>，:1444）<br><br>"
      "Body：<span style='font-family:" + MONO + "'>{\"dbs\":[…], \"roles\":[…]}</span><br>"
      "&nbsp;&nbsp;• <span style='font-family:" + MONO + "'>op=set</span>（create/alter upsert）/ <span style='font-family:" + MONO + "'>op=del</span>（drop）<br>"
      "&nbsp;&nbsp;• name / old_name(rename) / owner<br>"
      "&nbsp;&nbsp;• password + encrypted_password（角色）<br><br>"
      "控制面更新 <b>neon_pg_databases / neon_pg_roles</b><br>"
      "&nbsp;&nbsp;按 (branch_id, name) 唯一索引幂等 upsert",
      fs=11.5, color=DIM, lh=1.6),
    # Bottom: anti-loop
    R("ddl-b-bg", 96, 520, 1088, 138, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("ddl-b-h", 116, 532, 900, 20, "防止「控制面 → compute → 控制面」双写循环", fs=13, fw=800, color=AC),
    T("ddl-b-b", 116, 558, 1048, 92,
      "• 控制面下发 <b>ComputeSpec</b> 让 compute_ctl 建库/建角色时，compute_ctl 先执行 "
      "<span style='font-family:" + MONO + "'>SET neon.forward_ddl = false</span>，这样它执行 spec 里的 DDL 就不会再回调控制面<br>"
      "• <b>token 与 writer 身份绑定</b>：控制面校验请求 token 的 compute_id 必须 = endpoint 当前 compute_id；"
      "endpoint 换 writer 会递增 writer_generation，旧 compute 的 token 即便没过期也无法再回调<br>"
      "• GUC：<span style='font-family:" + MONO + "'>neon.console_url</span>（回调地址，必配）、"
      "<span style='font-family:" + MONO + "'>neon.forward_ddl</span>（默认 on）",
      fs=12, color=DIM, lh=1.6),
], p, notes="DDL Forwarding：用户直接执行 CREATE DATABASE/DROP ROLE 等，pgxn/neon 插件 ProcessUtility_hook 拦截记到 DdlHashTable，子事务用哈希表栈处理 SAVEPOINT（PushTable/MergeTable/PopTable），事务 PRE_COMMIT 时 NeonXactCallback 调 SendDeltasToControlPlane，curl PATCH 到 neon.console_url?endpoint_id=xxx，Bearer per-compute JWT（NEON_CONTROL_PLANE_TOKEN），body {dbs:[],roles:[]} op=set/del + name/old_name/owner/password。控制面 upsert neon_pg_databases/neon_pg_roles 按 (branch_id,name) 幂等。防双写循环：compute_ctl 执行 spec DDL 前 SET neon.forward_ddl=false。token 与 writer 身份绑定，换 writer 递增 writer_generation 使旧 token 失效。已知缺陷：转发后事务仍可能 abort 未处理。源码 pgxn/neon/neon_ddl_handler.c，控制面 handlers/compute_callback/hook_ddl_notify.py。")

# ─────── Slide 16: Safekeeper ───────
p += 1
std("s-sk1", "SAFEKEEPER", "WAL 服务：Paxos-like 复制", [
    T("sk-desc", 96, 172, 1088, 40,
      "Safekeeper 是<b>推模式</b>的 WAL 中转 + 复制服务。"
      "commit 延迟只依赖 SK 多数派，与 Pageserver / S3 完全解耦。",
      fs=15, color=DIM, lh=1.7),
    # Paxos role mapping
    R("sk-role-bg", 96, 218, 1088, 34, fill="rgba(124,179,244,0.08)", stroke="rgba(124,179,244,0.3)", radius=8),
    T("sk-role", 116, 224, 1048, 22,
      "Paxos 角色 ▸ <b>Compute (walproposer) = Proposer + Learner</b>　|　"
      "<b>Safekeeper = Acceptor</b>　|　Pageserver = <span style='color:" + FAINT + "'>共识之外的 WAL 消费者</span>"
      "　<span style='font-size:10px;color:" + FAINT + "'>(docs/rfcs/004-durability.md:162)</span>",
      fs=12, fw=600, color=FG, lh=1.3),
    # 3 SK visual
    R("sk-a", 130, 260, 200, 120, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.5)"),
    T("sk-at", 130, 274, 200, 24, "SK-1", fs=16, fw=800, color=AC2, align="center"),
    T("sk-ab", 130, 306, 200, 70, "flushLSN: 0/1A2B00<br>last_log_term: 5", fs=12, fw=500, color=DIM, ff=MONO, align="center", lh=1.7),
    R("sk-b", 540, 260, 200, 120, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.5)"),
    T("sk-bt", 540, 274, 200, 24, "SK-2 (leader)", fs=16, fw=800, color=AC2, align="center"),
    T("sk-bb", 540, 306, 200, 70, "flushLSN: 0/1A2B00<br>last_log_term: 5 ✓", fs=12, fw=500, color=DIM, ff=MONO, align="center", lh=1.7),
    R("sk-c", 950, 260, 200, 120, fill="rgba(255,158,138,0.05)", stroke="rgba(255,158,138,0.3)"),
    T("sk-ct", 950, 274, 200, 24, "SK-3 (lag)", fs=16, fw=800, color=FAINT, align="center"),
    T("sk-cb", 950, 306, 200, 70, "flushLSN: 0/1A1F00<br>last_log_term: 5", fs=12, fw=500, color=DIM, ff=MONO, align="center", lh=1.7),
    # walproposer
    R("sk-wp", 490, 440, 300, 50, fill="rgba(0,229,153,0.10)", stroke="rgba(0,229,153,0.5)"),
    T("sk-wpt", 490, 452, 300, 26, "walproposer (compute bgworker)", fs=14, fw=700, color=AC, align="center"),
    # walproposer PUSHES WAL upward into each SK (arrows start on the wp top edge,
    # end on each SK box bottom edge)
    LN("sk-l1", 560, 440, -330, -60, stroke=A_GRN, sw=2),
    LN("sk-l2", 640, 440, 0, -60, stroke=A_GRN, sw=2),
    LN("sk-l3", 720, 440, 330, -60, stroke=A_GRN, sw=2),
    T("sk-pushl", 96, 448, 360, 20, "push WAL → 3 SK", fs=12, fw=700, color=A_GRN),
    T("sk-cml", 810, 448, 374, 20, "commitLSN = 多数派 min(flushLSN)", fs=12, fw=700, color=A_GRN, align="right"),
    # bottom text
    T("sk-bottom", 96, 500, 1088, 172,
      "• <b>NodeID = (term, uuid)</b>，握手阶段提升 term；<span style='font-family:" + MONO + "'>term_history</span> 里的 <b>last_log_term</b> 区分历史代次（旧文档的 epoch）<br>"
      "• 恢复：从 quorum 中选 (last_log_term, flushLSN) 最大的 SK 做 leader，补齐 restartLSN..<span style='font-family:" + MONO + "'>commit_lsn</span><br>"
      "• <b>Learner 也是 Compute 自己</b>：walproposer 从 quorum 收 flushLSN 算出 commit_lsn，即「学到」哪段已被选定，据此 ACK client commit<br>"
      "• 稳态数据流是 <b>Compute → SK</b>，SK 之间不互相打 WAL；<b>故障恢复时</b> 落后的 SK 会通过 pg 复制协议<br>"
      "&nbsp;&nbsp;直接<b>从对等 SK 拉缺失 WAL</b>（<span style='font-family:" + MONO + "'>safekeeper/src/recovery.rs</span>，不走 S3）<br>"
      "• <b>形式化验证</b>：safekeeper/spec/ 目录有 TLA+ 规范",
      fs=13, color=DIM, lh=1.75),
], p, notes="Paxos 角色映射（docs/rfcs/004-durability.md:162-163）：Compute walproposer = Proposer + Learner（一身二任），Safekeeper = Acceptor，Pageserver 不在共识内，是下游 WAL 消费者。walservice.md:123-125 也明写 proposer=compute、acceptor=safekeeper。Learner 为什么是 Compute：walproposer 从 quorum 收集 flush_lsn 计算 commit_lsn（GetAcknowledgedByQuorumWALPosition walproposer.c:1994），即学到哪段 WAL 已被多数派选定，据此 ACK client commit。Pageserver 虽然也消费 WAL，但它不参与投票、commit_lsn 的推进不等它。Safekeeper Paxos-like 复制：3 副本，quorum=2，term/last_log_term/commit_lsn，TLA+ 规范。数据流路径：稳态是 Compute walproposer 推向 3 台 SK，SK 之间不主动互连；故障恢复时落后的 SK 从对等 SK 拉 WAL，见 safekeeper/src/recovery.rs recovery_main_loop 每 2s（CHECK_INTERVAL_MS=2000）自检，recovery_needed 选 (last_log_term, flush_lsn) 严格领先且 term==last_log_term 的 peer 做 donor，且有活的 compute 在流时 donors 强制置空避免抢；recover() 先 HTTP GET /v1/tenant/{}/timeline/{} 拿 donor term_history，本地 VoteRequest 得自己 term_history，TermHistory::find_highest_common_point 求最高公共点截断本地 WAL、发 ProposerElected；recovery_stream 用 Postgres 物理复制协议连 donor pg 端口发 START_REPLICATION PHYSICAL {lsn} (term='{term}')，注释明确 It will make safekeeper give out not committed WAL (up to flush_lsn)，能追未 committed 尾巴，S3 上 offloaded WAL 只有已 committed 段做不到。S3 offload 服务的是别的目的：timeline_eviction 冷 timeline 驱逐、Pageserver 灾难恢复。pull_timeline.rs 是另一个整表 tar 打包路径，用于新增 SK 成员 / 成员变更 RFC 035，不是正常追赶。")

# ─────── Slide 17: LSN 概念 ───────
p += 1
std("s-lsn", "SAFEKEEPER", "Safekeeper 三个核心 LSN", [
    T("lsn-desc", 96, 170, 1088, 30,
      "所有 LSN 都是 64 位 WAL 偏移。以下三个 LSN 描述 WAL 在 SK 集群中的确认进度（新→老）。"
      "<span style='color:" + DIM + "'>源码：safekeeper/src/safekeeper.rs</span>",
      fs=14, color=DIM, lh=1.5),
    # table
    *[e for i, (k, v, col) in enumerate([
        ("FlushLSN", "单个 SK 本地已 fsync 到磁盘的位置", "#7CB3F4"),
        ("CommitLSN", "多数派 SK 已确认的位置。<b>Compute ACK client commit 的依据</b>；恢复保证此前记录不丢", AC),
        ("RestartLSN", "全部 SK 都已确认的位置。SK 之前的 WAL 可截断", AC2),
    ]) for e in (
        R(f"lsn{i}bg", 96, 220 + i * 60, 1088, 52, fill="rgba(255,255,255,0.035)", stroke="none", sw=0, radius=10),
        T(f"lsn{i}k", 116, 234 + i * 60, 300, 26, k, fs=15, fw=800, color=col, ff=MONO),
        T(f"lsn{i}v", 424, 234 + i * 60, 750, 26, v, fs=14, fw=500, color=DIM, lh=1.4),
    )],
], p, notes="LSN 术语表（纯 SK 三个）：FlushLSN、CommitLSN、RestartLSN。last_written_lsn 已挪到 s-read-lsn（Compute 侧 LwLSN cache），remote_consistent_lsn 已在 s-ps-lsn 覆盖，避免重复。")

# ─────── Safekeeper 成员迁移流程 ───────
p += 1
std("s-sk-migrate", "SAFEKEEPER", "SK 成员迁移：generation 双阶段递增（RFC 035）", [
    T("skm-desc", 96, 164, 1088, 34,
      "SK 集合稳态时 <b>generation 不变</b>。只有 storcon 触发 SK 迁移（下线/扩缩容/换机）才会变——"
      "一次迁移让 generation <b>跳两级</b>：n → n+1 (joint) → n+2 (final)。"
      "<span style='color:" + DIM + "'>safekeeper_service.rs:1248/1364, RFC 035</span>",
      fs=12, color=DIM, lh=1.55),
    # Row 1: three state boxes with arrows
    R("skm-s1-bg", 96, 210, 340, 90, fill="rgba(124,179,244,0.10)", stroke="rgba(124,179,244,0.5)", radius=12),
    T("skm-s1-h", 116, 220, 300, 22, "gen = n（稳态）", fs=14, fw=800, color="#7CB3F4"),
    T("skm-s1-b", 116, 246, 300, 46,
      "sk_set = [<b>A, B, C</b>]<br>new_sk_set = None",
      fs=12, color=DIM, lh=1.5, ff=MONO),
    T("skm-a1", 436, 245, 40, 24, "→", fs=22, fw=800, color=DIM, align="center"),
    R("skm-s2-bg", 476, 210, 328, 90, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.5)", radius=12),
    T("skm-s2-h", 496, 220, 300, 22, "gen = n+1（joint）", fs=14, fw=800, color=AC2),
    T("skm-s2-b", 496, 246, 290, 46,
      "sk_set = [<b>A, B, C</b>]<br>new_sk_set = [<b>C, D, E</b>]",
      fs=12, color=DIM, lh=1.5, ff=MONO),
    T("skm-a2", 804, 245, 40, 24, "→", fs=22, fw=800, color=DIM, align="center"),
    R("skm-s3-bg", 844, 210, 340, 90, fill="rgba(0,229,153,0.10)", stroke="rgba(0,229,153,0.5)", radius=12),
    T("skm-s3-h", 864, 220, 300, 22, "gen = n+2（final）", fs=14, fw=800, color=AC),
    T("skm-s3-b", 864, 246, 300, 46,
      "sk_set = [<b>C, D, E</b>]<br>new_sk_set = None",
      fs=12, color=DIM, lh=1.5, ff=MONO),
    # Row 2: 3 columns of numbered steps aligned under the states above
    R("skm-c1-bg", 96, 314, 340, 340, fill=PANEL, stroke=EDGE, radius=12),
    T("skm-c1-h", 116, 326, 300, 22, "① 起 joint —— 递增 gen 一次", fs=13, fw=800, color="#7CB3F4"),
    T("skm-c1-b", 116, 356, 300, 288,
      "<b>1.</b> 读 timelines 表拿当前配置<br>"
      "<b>2.</b> 已在 joint 且目标不同 → 拒绝；<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;目标相同 → 续跑（幂等）<br>"
      "<b>3.</b> <span style='color:" + AC2 + "'>generation.next()</span>（n → n+1），<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;desired_set 写入 new_sk_set，<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;<b>CAS 到 storcon PG</b>（uniqueness + 线性化）<br><br>"
      "<span style='color:" + FAINT + "'>失败 CAS 立刻中止；说明有另一次</span><br>"
      "<span style='color:" + FAINT + "'>迁移抢跑（race）</span>",
      fs=11.5, color=DIM, lh=1.7),
    R("skm-c2-bg", 448, 314, 388, 340, fill=PANEL, stroke=EDGE, radius=12),
    T("skm-c2-h", 468, 326, 340, 22, "② 传播 joint + 同步位点", fs=13, fw=800, color=AC2),
    T("skm-c2-b", 468, 356, 348, 288,
      "<b>4.</b> <span style='font-family:" + MONO + "'>PUT /membership</span> 到<b>旧集合</b>（quorum），<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;取 max ⟨last_log_term, flush_lsn⟩ 作为<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;<b>sync_position</b>；同时通知 cplane<br>"
      "<b>5.</b> 对<b>新增</b> SK 做 <span style='font-family:" + MONO + "'>pull_timeline</span>（从旧集<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;合 quorum 拉 tar 包，非 S3）<br>"
      "<b>6.</b> bump_term(sync_term) 到新集合<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:" + FAINT + "'>（当前代码 TODO，未实现）</span><br>"
      "<b>7.</b> <span style='font-family:" + MONO + "'>PUT /membership</span> 到<b>新集合</b>，<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;<b>轮询到 quorum 追上 sync_position</b>",
      fs=11.5, color=DIM, lh=1.7),
    R("skm-c3-bg", 848, 314, 336, 340, fill=PANEL, stroke=EDGE, radius=12),
    T("skm-c3-h", 868, 326, 296, 22, "③ 提交 final —— 再递增一次", fs=13, fw=800, color=AC),
    T("skm-c3-b", 868, 356, 296, 288,
      "<b>8.</b> <span style='color:" + AC2 + "'>generation.next()</span>（n+1 → n+2），<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;new_conf = {gen=n+2, sk_set=新,<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;new_sk_set=None}，写库；同时向<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;<b>safekeeper_timeline_pending_ops</b><br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;插入被剔除 SK 的 <span style='font-family:" + MONO + "'>exclude</span> 操作<br>"
      "<b>9.</b> finish_migration：<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;• PUT /membership 到新集合（final）<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;• reconciler 消费 exclude ops<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;• cplane_notify（compute 停止对旧 SK<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;要 quorum）",
      fs=11.5, color=DIM, lh=1.7),
], p, notes="SK 成员迁移 9 步（RFC 035 + safekeeper_service.rs:migrate_to_new_sk_set）：generation 双阶段递增：① 起 joint（步骤 1-3，gen n→n+1，CAS 到 storcon PG 的 timelines 表）② 传播 joint（步骤 4-7：PUT membership 到旧集合拿 sync_position、pull_timeline 初始化新 SK、bump_term 当前未实现、PUT membership 到新集合并等 quorum 追齐 sync_position）③ 提交 final（步骤 8-9，gen n+1→n+2，写 new_conf + exclude ops 队列，finish 阶段 PUT final + reconciler 处理 exclude + 通知 cplane）。SK 侧被动规则：看到更高 gen 就切换并持久化 control file；收到更低 gen 消息一律拒绝（防脑裂核心）。步骤 8 之后迁移不可回滚。")

# ─────── Pageserver LSN 术语表 ───────
p += 1
std("s-ps-lsn", "PAGESERVER", "Pageserver 侧关键 LSN（timeline.rs / models.rs）", [
    T("pslsn-desc", 96, 166, 1088, 30,
      "以下 LSN 从最\"新\"到最\"老\"排列，描述了 WAL 在 Pageserver 内的消化进度。"
      "<span style='color:" + DIM + "'>源码：pageserver/src/tenant/timeline.rs:260-343、libs/pageserver_api/src/models.rs:1546-1579</span>",
      fs=12, color=DIM, lh=1.5),
    *[e for i, (k, v, col) in enumerate([
        ("last_record_lsn",
         "已在内存中处理完的最新 WAL 记录 LSN（timeline.rs:273）。<b>最靠前</b>",
         AC),
        ("prev_record_lsn",
         "上一条记录的 LSN（设置 xl_prev 指针用）。≤ last_record_lsn",
         "#7CB3F4"),
        ("disk_consistent_lsn",
         "已落盘到本地 layer 文件的 LSN（timeline.rs:282）。<b>崩溃重启从这里开始重放 WAL</b>",
         "#7CB3F4"),
        ("remote_consistent_lsn",
         "已成功上传到 S3 的 LSN（当前 generation 视角，projected）。≤ disk_consistent_lsn",
         "#FFB080"),
        ("remote_consistent_lsn_visible",
         "广播给 SK 的远程一致 LSN（经 deletion queue generation 校验不回退）。<b>SK 据此回收 WAL</b>",
         "#FFB080"),
        ("min_readable_lsn",
         "= max(planned_gc_cutoff, applied_gc_cutoff)（routes.rs:482）。<b>对外暴露的可读历史最早点</b>；创建分支/临时 endpoint 用它",
         AC2),
        ("applied_gc_cutoff_lsn",
         "GC 已<b>实际</b>清理到的 LSN（timeline.rs:327）。早于此的 layer 数据可能已不存在；≤ min_readable_lsn",
         AC2),
        ("initdb_lsn",
         "根 timeline 的起点（timeline.rs:343）。<b>永不变</b>，历史最早",
         "#C89EFF"),
    ]) for e in (
        R(f"pslsn{i}bg", 96, 202 + i * 58, 1088, 50,
          fill="rgba(255,255,255,0.035)", stroke="none", sw=0, radius=10),
        T(f"pslsn{i}k", 116, 214 + i * 58, 330, 24, k, fs=13, fw=800, color=col, ff=MONO),
        T(f"pslsn{i}v", 460, 214 + i * 58, 710, 24, v, fs=12, fw=500, color=DIM, lh=1.4),
    )],
], p, notes="Pageserver LSN 术语表（从新到老）：last_record_lsn → prev_record_lsn → disk_consistent_lsn → remote_consistent_lsn(projected) → remote_consistent_lsn_visible（广播给 SK，SK 据此回收 WAL）→ min_readable_lsn = max(planned_gc_cutoff, applied_gc_cutoff)（创建分支/临时 endpoint 看这个）→ applied_gc_cutoff_lsn（GC 实际清理位置，≤ min_readable_lsn，因为 min_readable_lsn 是它和 planned 的 max）→ initdb_lsn（根 timeline 起点，永不变）。源码 timeline.rs:260-343、models.rs:1546-1579、routes.rs:470-501。")

# ─────── Slide 9: Pageserver 概述 ───────
p += 1
std("s-ps1", "PAGESERVER", "Pageserver — 存储引擎核心", [
    T("ps-quote", 96, 172, 1088, 46,
      "&ldquo;Scalable storage backend for the compute nodes&rdquo;　— docs/pageserver.md",
      fs=15, fw=500, color=FAINT, ff=MONO, lh=1.5),
    *card("ps-r1", 96, 236, 350, 190,
          "① 服务读请求", [
              "响应 Compute 的",
              "GetPage@LSN(key, lsn)",
              "",
              "按需重建任意版本的",
              "8KB 页面",
          ], fs=15, headfs=17),
    *card("ps-r2", 465, 236, 350, 190,
          "② 摄入 WAL", [
              "从 Safekeeper 拉取",
              "streaming replication",
              "",
              "解码 → 按 key 分桶",
              "→ 写 Layer 文件",
          ], hc=AC2, fs=15, headfs=17),
    *card("ps-r3", 834, 236, 350, 190,
          "③ 上传对象存储", [
              "Layer 文件上传",
              "S3 / GCS / Azure Blob",
              "",
              "S3 是唯一持久化底座",
              "（无 Pageserver 副本）",
          ], hc="#7CB3F4", fs=15, headfs=17),
    T("ps-note", 96, 452, 1088, 110,
      "<b>关键设计：</b>S3 是所有 timeline 数据唯一的持久化存储底座 —— Pageserver 本身没有副本。"
      "本地磁盘仅作为 layer 缓存；可配置 Secondary Pageserver 热备加速故障切换，本身不承担持久化。<br>"
      "独立的容错 WAL 服务（Safekeeper）用于降低写延迟：commit 不需要等 Pageserver 或 S3。",
      fs=15, color=DIM, lh=1.8),
], p, notes="Pageserver 三大职责：GetPage@LSN、WAL 摄入、S3 上传。S3 是 timeline 数据唯一持久化底座，本地磁盘仅为 layer 缓存。")

# ─────── Slide 9: Tenant / Timeline 模型 ───────
p += 1
std("s-ps-model", "PAGESERVER", "多租户模型：Tenant / Timeline", [
    T("mdl-desc", 96, 175, 1088, 42,
      "Pageserver 是多租户的：Tenant（项目）→ Timeline（分支）二级模型。",
      fs=16, color=DIM, lh=1.6),
    # tree diagram
    R("mdl-t", 96, 235, 300, 44, fill="rgba(0,229,153,0.10)", stroke="rgba(0,229,153,0.5)"),
    T("mdl-tt", 96, 244, 300, 30, "Tenant  &lt;32-hex-id&gt;", fs=14, fw=700, color=AC, align="center", ff=MONO),
    LN("mdl-l1", 150, 279, 0, 40, end=None, stroke=A_NEU, sw=2),
    R("mdl-tl1", 150, 319, 280, 40, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.4)"),
    T("mdl-tl1t", 150, 327, 280, 26, "Timeline main  &lt;32-hex-id&gt;", fs=13, fw=600, color=AC2, align="center", ff=MONO),
    LN("mdl-l2", 200, 359, 0, 40, end=None, stroke=A_NEU, sw=2),
    R("mdl-tl2", 200, 399, 300, 40, fill="rgba(255,158,138,0.07)", stroke="rgba(255,158,138,0.3)"),
    T("mdl-tl2t", 200, 407, 300, 26, "└ Timeline dev @LSN 0/16F9A00", fs=12, fw=600, color=AC2, align="center", ff=MONO),
    LN("mdl-l3", 250, 439, 0, 40, end=None, stroke=A_NEU, sw=2),
    R("mdl-tl3", 250, 479, 300, 40, fill="rgba(255,158,138,0.05)", stroke="rgba(255,158,138,0.22)"),
    T("mdl-tl3t", 250, 487, 300, 26, "└ Timeline test @LSN 0/1A20C10", fs=12, fw=600, color=AC2, align="center", ff=MONO),
    # right side details
    *card("mdl-r", 620, 218, 566, 430,
          "磁盘布局与 Key 空间", [
              ".neon/tenants/&lt;tenant_shard_id&gt;/timelines/&lt;timeline_id&gt;/&lt;layer files&gt;",
              "",
              "<b>Key 编码</b>（18 字节，打平成一维空间）:",
              "(spcnode, dbnode, relnode, forknum, blocknum)",
              "",
              "<b>TenantId / TimelineId</b>：均为 128-bit 随机 ID，",
              "　序列化为 32-hex 字符串（libs/utils/src/id.rs Id([u8;16])）",
              "",
              "<b>tenant_shard_id</b>：格式 &lt;tenant_id&gt;-&lt;shard_slug&gt;（如 ...-0001）；",
              "　<span style='color:" + FAINT + "'>count=0 只是历史兼容特例、退化成裸 tenant_id 无后缀，</span>",
              "　<span style='color:" + FAINT + "'>RFC 031 建议新建 tenant 规范做法是显式传 count=1</span>",
              "",
              "<b>LSN</b>：64 位 WAL 偏移 = 数据版本轴 + 分支锚点",
              "<b>Layer 文件名</b>：&lt;key_start&gt;-&lt;key_end&gt;__&lt;lsn_start&gt;-&lt;lsn_end&gt;-&lt;generation&gt;",
              "　<span style='font-size:11px;color:" + FAINT + "'>示例：000...000-FFF...FFF__00000000014E8F20-00000000014E8F99-00000001</span>",
              "<b>Generation</b>：末尾 8 位 hex 后缀（-{g:08x}），每次 attach 单调递增，",
              "　彻底避免 split-brain 覆盖（无需 STONITH）",
          ], hc="#7CB3F4", fs=13, headfs=16),
], p, notes="Tenant/Timeline 二级模型：本地/远端目录路径的第一段实际是 tenant_shard_id（pageserver/src/config.rs:313 tenant_path、:337 timeline_path），不是裸 tenant_id。TenantShardId Display（libs/utils/src/shard.rs:206-215）：shard_count==0 时退化成裸 tenant_id.fmt 无后缀，这是 RFC 031（docs/rfcs/031-sharding-static.md:254）标注的\"backward compatibility\"特例；count>=1 时格式是 <tenant_id>-<shard_slug>，4 位 hex（shard_number, shard_count 各 2 位），RFC 031 举的例子就是\"a single-shard tenant's prefix will be 0001\"，即建议新建 tenant 从一开始就显式传 count=1，不要用 count=0 的兼容路径，方便后续 shard split 时前缀格式统一不需要隐式迁移。storage_controller do_tenant_create 的 ShardParameters::default() 是 count=0（libs/pageserver_api/src/models.rs:493-499），但这只是字面默认值，不代表推荐用法。Baidu 内部 butterfly 平台的 sdk_sc_tenant.py:46-59 每次创建 tenant 都显式传 shard_parameters.count=1、stripe_size=32768，与 RFC 建议一致，因此实际创建出来的 tenant_shard_id 一开始就带 -0001 后缀。TenantId 与 TimelineId 都是 128-bit 随机数，序列化为 32 位十六进制字符串（libs/utils/src/id.rs:24 struct Id([u8; 16]); TimelineId/TenantId 都是对它的 newtype 包装，id.rs:272 TimelineId(Id)）。Key 18 字节打平。Layer 文件名格式 key_start-key_end__lsn_start-lsn_end-generation，Generation 是 u32 序列化为 8 位 hex 后缀（libs/utils/src/generation.rs GenerationFileSuffix Display: write!(f, \"-{g:08x}\")），拼在 key_range/lsn_range 之后，通过 remote_timeline_client.rs 的 generation.get_suffix() 构造 S3 object key。示例 000000000000000000000000000000000000-FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF__00000000014E8F20-00000000014E8F99-00000001 中末尾 -00000001 即 generation=1")

# ─────── Slide 10: Layer 文件 ───────
p += 1
std("s-ps-layer", "PAGESERVER", "Layer 文件：不可变的两级 LSM", [
    T("ly-desc", 96, 172, 1088, 44,
      "所有<b>落盘</b>数据存为<b>不可变</b> Layer 文件。两种类型，二维划分：Key 范围 × LSN 范围。"
      "<span style='font-size:12.5px;color:" + FAINT + "'>（落盘之前还有一层内存写缓冲 InMemoryLayer，见下一页）</span>",
      fs=16, color=DIM, lh=1.6),
    *card("ly1", 96, 232, 530, 150,
          "Image Layer（快照）", [
              "某一 LSN 上、一段 key 范围的<b>完整页快照</b>",
              "",
              "文件名: &lt;start_key&gt;-&lt;end_key&gt;__&lt;lsn&gt;",
              "读取时作为重建的基础镜像",
          ], fs=14, headfs=16),
    *card("ly2", 656, 232, 530, 150,
          "Delta Layer（增量）", [
              "一段 LSN 范围 × 一段 key 范围内的<b>所有 WAL 记录</b>",
              "",
              "文件名: &lt;start_key&gt;-&lt;end_key&gt;__&lt;lsn1&gt;-&lt;lsn2&gt;",
              "读取时在 image 之上逐条 replay",
          ], hc=AC2, fs=14, headfs=16),
    # L0 / L1 illustration
    T("ly-l0h", 96, 408, 300, 24, "L0（覆盖全 key 空间）", fs=14, fw=700, color=AC2),
    R("ly-l0a", 96, 440, 400, 22, fill="rgba(255,158,138,0.18)", stroke="rgba(255,158,138,0.4)", radius=4),
    R("ly-l0b", 96, 468, 400, 22, fill="rgba(255,158,138,0.14)", stroke="rgba(255,158,138,0.35)", radius=4),
    R("ly-l0c", 96, 496, 400, 22, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.3)", radius=4),
    T("ly-l0n", 96, 522, 400, 20, "顺序 flush，LSN 递增，累积 10 个触发 compaction", fs=11, color=FAINT),
    LN("ly-arrow", 516, 470, 60, 0, stroke=A_GRN, sw=2),
    T("ly-arrl", 506, 440, 90, 20, "compaction", fs=11, fw=600, color=AC, align="center"),
    T("ly-l1h", 600, 408, 300, 24, "L1（按 key 切分）", fs=14, fw=700, color=AC),
    R("ly-l1a", 600, 440, 130, 78, fill="rgba(0,229,153,0.16)", stroke="rgba(0,229,153,0.45)", radius=4),
    R("ly-l1b", 740, 440, 130, 78, fill="rgba(0,229,153,0.12)", stroke="rgba(0,229,153,0.4)", radius=4),
    R("ly-l1c", 880, 440, 130, 78, fill="rgba(0,229,153,0.08)", stroke="rgba(0,229,153,0.35)", radius=4),
    T("ly-l1n", 600, 522, 500, 20, "128 MB 目标大小，image_creation_threshold=3 时物化 image", fs=11, color=FAINT),
    # vs LSM-Tree / RocksDB
    R("ly-cmp-bg", 96, 548, 1088, 128, fill=PANEL, stroke=EDGE, radius=10),
    T("ly-cmp-h", 116, 558, 400, 20, "vs 传统 LSM-Tree / RocksDB", fs=13, fw=800, color=AC),
    T("ly-cmp-b", 116, 582, 1048, 90,
      "• <b>只有 L0 → L1 两级</b>（RocksDB 通常 L0~L6+ 多级放大压缩），无 size-tiered 深度合并<br>"
      "&nbsp;&nbsp;<b>但 L1 内 delta 可纵向叠 3~10 层</b>，达 <span style='font-family:" + MONO + "'>image_creation_threshold</span>（默认 3）就物化一张 image 压平；"
      "<b>层级标签仍只有 L0 / L1</b><br>"
      "• Delta layer <b>存 WAL 记录</b>（redo op），非 KV put/delete；读时需 walredo 进程回放才能得到页<br>"
      "• 二维索引：Key 范围 × <b>LSN 范围</b>（多版本内建），RocksDB 只有 Key 一维、旧版本靠 seq# 或删除标记<br>"
      "• 文件<b>不可变、直接上传 S3</b>；本地磁盘只是缓存，冷分层天然到对象存储，不做 SSTable 本地长期驻留",
      fs=11, color=DIM, lh=1.6),
], p, notes="Layer 文件：Image（快照）+ Delta（增量），L0（全 key 空间）→ L1（按 key 切分），只有两级 LSM。补充：L1 内同一 key range 上 delta 可纵向叠 3~10 层（count_deltas 注释 layer_map.rs:843-845 'in practice between 3 and 10'），达 image_creation_threshold（默认 3）就物化 image 压平下面的 delta 栈，但层级标签仍只有 L0/L1 两个值，不存在 L2/L3。is_l0 判定见 layer_map.rs:793 is_delta_layer && key_range==Key::MIN..Key::MAX。compact_level0（compaction.rs:1839）doc 明确 'compact and reshuffle them as Level 1 files'，L0 进 L1 出一跳到底。数据变多的消化方式：L1 delta 按 key 切分变多（横向变宽 128MB 一份 compaction_target_size），以及 image 物化压平 delta 栈，都不是加深层数。")

# ─────── Slide 10a: InMemoryLayer = pageserver 的 MemTable ───────
p += 1
std("s-ps-inmem", "PAGESERVER", "写入缓冲 InMemoryLayer：pageserver 的 MemTable", [
    T("im-desc", 96, 166, 1088, 44,
      "上一页两级 LSM 都在磁盘 / S3 上。它们<b>之前</b>，ingest 的 WAL 先进一层内存写缓冲 "
      "<span style='font-family:" + MONO + "'>InMemoryLayer</span> —— 等价 LSM 的 <b>MemTable</b>。"
      "所以 pageserver 严格说是<b>三级</b>：内存写缓冲 → L0 → L1。",
      fs=13, color=DIM, lh=1.6),
    # ── pipeline diagram ──
    R("im-bandA", 86, 228, 529, 120, fill="rgba(255,158,138,0.06)", stroke="rgba(255,158,138,0.28)", radius=10),
    T("im-bandA-l", 96, 234, 509, 20, "① InMemoryLayer（内存写缓冲 = MemTable 等价物）", fs=12, fw=800, color=AC2),
    R("im-bandB", 664, 228, 520, 120, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.28)", radius=10),
    T("im-bandB-l", 674, 234, 500, 20, "② 两级 LSM（不可变，磁盘 → S3）", fs=12, fw=800, color=AC),
    R("im-b1", 96, 266, 220, 72, fill="rgba(255,158,138,0.16)", stroke="rgba(255,158,138,0.45)", radius=8),
    T("im-b1t", 96, 278, 220, 22, "open_layer", fs=15, fw=800, color=AC2, align="center", ff=MONO),
    T("im-b1s", 96, 304, 220, 18, "可写 · MemTable", fs=11, color=DIM, align="center"),
    R("im-b2", 385, 266, 220, 72, fill="rgba(200,158,255,0.14)", stroke="rgba(200,158,255,0.45)", radius=8),
    T("im-b2t", 385, 278, 220, 22, "frozen_layers", fs=15, fw=800, color="#C89EFF", align="center", ff=MONO),
    T("im-b2s", 385, 304, 220, 18, "不可变队列 · 待 flush", fs=11, color=DIM, align="center"),
    R("im-b3", 674, 266, 220, 72, fill="rgba(255,158,138,0.10)", stroke="rgba(255,158,138,0.35)", radius=8),
    T("im-b3t", 674, 278, 220, 22, "L0 delta", fs=15, fw=800, color=AC2, align="center", ff=MONO),
    T("im-b3s", 674, 304, 220, 18, "磁盘 · 不可变", fs=11, color=DIM, align="center"),
    R("im-b4", 963, 266, 220, 72, fill="rgba(0,229,153,0.14)", stroke="rgba(0,229,153,0.45)", radius=8),
    T("im-b4t", 963, 278, 220, 22, "L1 delta/image", fs=15, fw=800, color=AC, align="center", ff=MONO),
    T("im-b4s", 963, 304, 220, 18, "S3 · 按 key 切分", fs=11, color=DIM, align="center"),
    LN("im-a1", 316, 302, 69, 0, stroke=A_NEU, sw=2),
    T("im-a1l", 305, 244, 90, 18, "freeze", fs=11, fw=700, color=FAINT, align="center"),
    LN("im-a2", 605, 302, 69, 0, stroke=A_GRN, sw=2),
    T("im-a2l", 594, 244, 90, 18, "flush 写盘", fs=11, fw=700, color=AC, align="center"),
    LN("im-a3", 894, 302, 69, 0, stroke=A_GRN, sw=2),
    T("im-a3l", 883, 244, 90, 18, "compaction", fs=11, fw=700, color=FAINT, align="center"),
    # ── two cards ──
    *card("im-c1", 96, 366, 530, 294,
          "“in-memory” 其实名不副实", [
              "结构注释直言：<b>页面数据不在内存</b>，而在一个",
              "<b>ephemeral file</b>（本地临时文件，走 page_cache 缓冲）",
              "",
              "内存里只放<b>索引</b>：",
              "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>BTreeMap&lt;Key, VecMap&lt;Lsn, IndexEntry&gt;&gt;</span>",
              "&nbsp;&nbsp;（IndexEntry = 该页版本在文件里的偏移）",
              "",
              "文件 <b>append-only</b>：读时先查内存索引，再按偏移读文件",
              "<span style='color:#888'>inmemory_layer.rs:1-5（注释）· :70（index）</span>",
          ], hc=AC2, fs=12, headfs=15),
    *card("im-c2", 656, 366, 530, 294,
          "三级流水线 & 落盘触发", [
              "<b>创建</b>：首条 WAL 到达时 <span style='font-family:" + MONO + "'>get_layer_for_write</span>",
              "&nbsp;&nbsp;新建 open_layer（layer_manager.rs:395-429）",
              "<b>freeze</b>：<span style='font-family:" + MONO + "'>checkpoint_distance</span> 累计字节 / 定时 tick",
              "&nbsp;&nbsp;到阈值 → 挪进 frozen_layers，换开新 open_layer（:451-464）",
              "<b>flush</b>：后台取 <span style='font-family:" + MONO + "'>frozen_layers.front()</span>",
              "&nbsp;&nbsp;→ create_delta_layer 写成不可变 L0（timeline.rs:5000,5158）",
              "",
              "<b>读路径</b>：open + frozen <b>优先于</b>磁盘 layer map",
              "&nbsp;&nbsp;（跟 LSM 先查 memtable 再查 SST 一致，timeline.rs:658-697）",
          ], hc=AC, fs=12, headfs=15),
], p, notes="pageserver 有 MemTable 等价物，就叫 InMemoryLayer（pageserver/src/tenant/storage_layer/inmemory_layer.rs）。层级对应：LSM active memtable ↔ LayerMap.open_layer:Option<Arc<InMemoryLayer>>（layer_manager.rs:395-429 get_layer_for_write，首条 WAL 到达时创建）；LSM immutable memtable ↔ LayerMap.frozen_layers:VecDeque<Arc<InMemoryLayer>>（layer_manager.rs:451-464 try_freeze_in_memory_layer：open_layer.freeze(end_lsn) 后 push_back 到 frozen_layers、清空 open_layer、next_open_layer_at=end_lsn）；memtable flush→SSTable ↔ flush_frozen_layer→create_delta_layer 生成 L0 delta（timeline.rs:5000 取 frozen_layers.front()，5158-5255 flush_frozen_layer）。关键差异：inmemory_layer.rs:1-5 注释明说 'The in-memory part of the name is a bit misleading: the actual page versions are held in an ephemeral file, not in memory. The metadata for each page version, i.e. its position in the file, is kept in memory'——真正在内存的只是 index:RwLock<BTreeMap<CompactKey,VecMap<Lsn,IndexEntry>>>（inmemory_layer.rs:70），IndexEntry 是 ephemeral file 内偏移；文件 append-only（EphemeralFile，走 page_cache）。freeze 触发：open_layer.tick()/checkpoint_distance（timeline.rs:2128-2164）。读路径优先级：ReadPathLayerId::InMemoryLayer 先查 open_layer+frozen_layers 再查磁盘（timeline.rs:658-697,2603-2608），与 LSM 先 memtable 后 SST 一致。所以严格说 pageserver 是三级：open_layer(可写,非纯内存)→frozen_layers(不可变待flush)→磁盘 L0/L1（真正的两级 LSM）。")

# ─────── Slide 10b: 从文件名区分 L0 / L1（S3 视角）───────
p += 1
std("s-ps-layer-name", "PAGESERVER", "S3 上怎么区分 L0 / L1：光看文件名就够了", [
    T("lyn-desc", 96, 172, 1088, 40,
      "文件名里的 key 范围<b>就是</b>运行时判定 L0/L1 用的同一个字段，没有独立的 L0 标记位——文件名本身即权威来源。",
      fs=14, color=DIM, lh=1.6),
    R("lyn-ex-bg", 96, 224, 1088, 150, fill="rgba(255,255,255,0.035)", stroke=EDGE, radius=10),
    T("lyn-ex-h", 116, 236, 400, 20, "示例（真实 S3 目录）", fs=12, fw=800, color=AC, ff=MONO),
    T("lyn-ex-b", 116, 260, 1048, 104,
      "000...0000-<b style='color:" + AC2 + "'>0300...0002</b>__14E8F20-2301681-00000001　　"
      "<span style='color:" + AC2 + "'>← key_end 不是全 F，L1</span><br>"
      "000...0000-<b style='color:" + AC + "'>FFFF...FFFF</b>__2301681-23058B1-00000001　　"
      "<span style='color:" + AC + "'>← key_end = Key::MAX 全 F，L0</span><br>"
      "000...0000-<b style='color:" + AC + "'>FFFF...FFFF</b>__23058B1-2309D39-00000001　　<span style='color:" + AC + "'>← L0</span><br>"
      "000...0000-<b style='color:" + AC + "'>FFFF...FFFF</b>__2309D39-230E4A9-00000001　　<span style='color:" + AC + "'>← L0</span><br>"
      "index_part.json-00000001　　<span style='color:" + FAINT + "'>← 索引清单，非 layer 文件</span>",
      fs=12.5, color=DIM, lh=1.7, ff=MONO),
    *card("lyn1", 96, 396, 350, 190,
          "判定规则", [
              "<span style='font-family:" + MONO + "'>key_start-key_end</span> 覆盖<b>整个</b> key 空间",
              "（<span style='font-family:" + MONO + "'>Key::MIN..Key::MAX</span>，全 0…全 F）",
              "　→ <b style='color:" + AC + "'>L0</b>",
              "",
              "只覆盖<b>一段子区间</b>（非全 F）",
              "　→ <b style='color:" + AC2 + "'>L1</b>（按 key 切分后的产物）",
          ], hc="#7CB3F4", fs=13, headfs=15),
    *card("lyn2", 460, 396, 350, 190,
          "Key 是 18 字节 = 36 hex", [
              "<span style='font-family:" + MONO + "'>KEY_SIZE = 18</span>（pageserver_api/key.rs）",
              "序列化后正好 36 个十六进制字符",
              "",
              "<span style='font-family:" + MONO + "'>Key::MAX</span> = 全字段取各自类型 MAX",
              "　→ 打印出来就是 36 个 <b>F</b>",
          ], hc=AC2, fs=13, headfs=15),
    *card("lyn3", 824, 396, 360, 190,
          "为什么可靠：单一数据源", [
              "文件名解析出的 key_range 直接构成",
              "<span style='font-family:" + MONO + "'>PersistentLayerDesc.key_range</span>",
              "",
              "<span style='font-family:" + MONO + "'>index_part.json</span> 的 LayerFileMetadata",
              "只存 file_size/generation/shard，",
              "<b>没有</b>单独的 is_l0 字段，永远现算",
          ], hc=AC, fs=12.5, headfs=15),
], p, notes="is_l0 判定：pageserver/src/tenant/layer_map.rs:792-795 pub fn is_l0(key_range,is_delta_layer){is_delta_layer && key_range==&(Key::MIN..Key::MAX)}。Key 18字节：libs/pageserver_api/src/key.rs:36 KEY_SIZE=18；Key::MAX/MIN定义:351-358/343-350，各字段取类型MAX/0；from_hex(:361)断言长度必须36 hex。文件名→字段单一数据源：DeltaLayerName::parse_str(layer_name.rs:63-107)直接解析__前后为key_range；PersistentLayerDesc::from_filename(layer_desc.rs:146-164)照搬无二次查表；LayerMap::is_l0再读这同一个key_range字段。index_part.json的LayerFileMetadata(remote_timeline_client/index.rs:234-244)只有file_size/generation/shard三个字段，没有is_l0，L0/L1永远现算，不存在与文件名不一致的情况。image vs delta文件名结构区分：delta Display(layer_name.rs:110-121)__后两个LSN一个'-'分隔；image Display(:209-218)__后只有一个LSN。用户提供5个文件里前4个key_end=FFFF...FFFF(=Key::MAX)是L0，第1个key_end=0300...0002(非全F)是L1，index_part.json-00000001是索引清单非layer文件，末尾-00000001是generation后缀。")

# ─────── Slide 11: LayerMap ───────
p += 1
std("s-layermap", "PAGESERVER", "LayerMap：(Key, LSN) 二维查找索引", [
    T("lm-desc", 96, 170, 1088, 44,
      "读路径关键结构：给定 (key, end_lsn)，找出覆盖它的最新 layer。"
      "<span style='font-family:" + MONO + "'>pageserver/src/tenant/layer_map.rs</span>",
      fs=14, color=DIM, lh=1.5),
    R("lm1-bg", 96, 222, 530, 252, fill=PANEL, stroke=EDGE, radius=12),
    T("lm1-h", 116, 238, 490, 24, "两步查询 search(key, end_lsn)", fs=16, fw=800, color=AC),
    T("lm1-b", 116, 272, 490, 190,
      "① <b>选版本</b>：historic 是 BTreeMap&lt;Lsn, Version&gt;<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>range(..=lsn).next_back()</span> → O(log V)<br>"
      "② <b>查 key</b>：该版本内的持久化红黑树<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>nodes.range(..=key).next_back()</span> → O(log N)<br>"
      "③ <b>选层</b>：select_layer 优先级<br>"
      "&nbsp;&nbsp;image &gt; delta &gt; in-memory layer<br>"
      "返回 SearchResult { layer, lsn_floor }",
      fs=12.5, color=DIM, lh=1.65),
    R("lm2-bg", 656, 222, 530, 252, fill=PANEL, stroke=EDGE, radius=12),
    T("lm2-h", 676, 238, 490, 24, "为什么用持久化（不可变）红黑树", fs=16, fw=800, color=AC2),
    T("lm2-b", 676, 272, 490, 190,
      "<span style='font-family:" + MONO + "'>rpds::RedBlackTreeMapSync&lt;i128, (lsn_end, layer)&gt;</span><br>"
      "• 树本身只索引 <b>Key 一维</b>；LSN 维度靠<b>多版本</b>表达<br>"
      "• 每次插入产生新 version，旧 version 不可变<br>"
      "• 版本 clone <b>O(1)</b>，避免逐 LSN 全量拷贝的平方级内存<br>"
      "• 插入须 LSN 递增；曾评估 im crate，因 bug 改用 rpds<br>"
      "• 代码注释里的 “R-Tree” 是遗留命名，实现不是 R-tree",
      fs=12.5, color=DIM, lh=1.65),
    R("lm3-bg", 96, 490, 1088, 172, fill=PANEL, stroke=EDGE, radius=10),
    T("lm3-h", 116, 502, 500, 20, "L0 / L1 在 map 中的处理差异 & 回溯修改", fs=13, fw=800, color=AC),
    T("lm3-b", 116, 528, 1048, 125,
      "• <b>L0 delta</b> 的 key 范围恒为 <span style='font-family:" + MONO + "'>Key::MIN..Key::MAX</span>，放进索引树没有区分度 → 额外存一份 "
      "<span style='font-family:" + MONO + "'>l0_delta_layers: Vec</span>，查询时<b>线性扫描</b><br>"
      "• <b>L1</b> 层 key 范围互不重叠 → 由红黑树索引，单次 O(log N) 命中<br>"
      "• <b>回溯修改是痛点</b>：compaction 会产出较旧 LSN 的层、GC 会删历史层，但旧 version 无法原地改<br>"
      "&nbsp;&nbsp;→ BufferedHistoricLayerCoverage 先缓冲变更，再从变更点<b>重建</b>后续所有 version<br>"
      "• 设计权衡见 Neon 博客 persistent-structures-in-neons-wal-indexing（代码注释直接引用）",
      fs=12, color=DIM, lh=1.65),
], p, notes="LayerMap 是读路径的 (key, LSN) 索引。核心是持久化红黑树 rpds::RedBlackTreeMapSync：树只索引 key 一维，LSN 维度用不可变结构的多版本表达，版本 clone O(1)。查询两步：BTreeMap 按 LSN 选 version O(log V)，再在该 version 的树里按 key 查 O(log N)，最后 select_layer 按 image > delta > in-memory 优先级选。L0 层 key 范围是全域，单独放 Vec 线性扫。compaction/GC 造成的回溯修改要靠 BufferedHistoricLayerCoverage 缓冲 + 重建。")

# ─────── index_part.json ───────
p += 1
std("s-indexpart", "PAGESERVER", "index_part.json：远端 timeline 的权威清单", [
    T("ip-desc", 96, 168, 1088, 36,
      "S3 上没有目录列举语义，Pageserver 不靠 LIST 恢复状态，而是读一个 JSON 清单重建 LayerMap。"
      "<span style='font-family:" + MONO + "'>remote_timeline_client/index.rs</span>",
      fs=14, color=DIM, lh=1.5),
    # left: content
    R("ip1-bg", 96, 214, 540, 296, fill=PANEL, stroke=EDGE, radius=12),
    T("ip1-h", 116, 228, 500, 24, "里面装了什么（struct IndexPart）", fs=16, fw=800, color=AC),
    T("ip1-b", 116, 262, 500, 236,
      "<span style='font-family:" + MONO + "'>layer_metadata: HashMap&lt;LayerName, LayerFileMetadata&gt;</span><br>"
      "&nbsp;&nbsp;→ <b>全部 layer 的文件名 + 大小 + generation + shard</b><br>"
      "&nbsp;&nbsp;→ 不变量：索引里列出的 layer <b>必须已存在于 S3</b><br>"
      "<span style='font-family:" + MONO + "'>disk_consistent_lsn</span>　该 timeline 已落盘的 LSN<br>"
      "<span style='font-family:" + MONO + "'>metadata: TimelineMetadata</span>　含 ancestor / ancestor_lsn<br>"
      "<span style='font-family:" + MONO + "'>lineage</span>　分支血缘；<span style='font-family:" + MONO + "'>gc_blocking</span>　GC 阻断标记<br>"
      "<span style='font-family:" + MONO + "'>gc_compaction</span>　bottommost compaction 断点（可续跑）<br>"
      "<span style='font-family:" + MONO + "'>deleted_at / archived_at / marked_invisible_at</span>　生命周期<br>"
      "<span style='font-family:" + MONO + "'>rel_size_migration(_at)</span>　rel size 读路径版本切换<br><br>"
      "<b>version 字段当前 = 15</b>，KNOWN_VERSIONS 1..15 全部可读<br>"
      "&nbsp;&nbsp;→ 必须<b>前后双向兼容</b>，改字段就得升版本 + 加测试",
      fs=11.5, color=DIM, lh=1.65),
    # right: role
    R("ip2-bg", 656, 214, 528, 296, fill=PANEL, stroke=EDGE, radius=12),
    T("ip2-h", 676, 228, 490, 24, "它在系统里的三个角色", fs=16, fw=800, color=AC2),
    T("ip2-b", 676, 262, 490, 236,
      "<b>① 启动即真相</b>：attach 时读 index 重建 LayerMap，<br>"
      "&nbsp;&nbsp;本地磁盘为空也能立刻服务（layer 按需下载）<br><br>"
      "<b>② 防脑裂的裁决者</b>：key 带 generation 后缀<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>…/index_part.json-&lt;gen hex&gt;</span><br>"
      "&nbsp;&nbsp;新 PS 取<b>能读到的最高 generation</b>那份为起点<br>"
      "&nbsp;&nbsp;老 PS 写自己那份，互不覆盖（RFC 025）<br><br>"
      "<b>③ GC / 删除的记账本</b>：GC 只把 layer 从 index<br>"
      "&nbsp;&nbsp;<b>解链</b>，对象先悬挂；真删要走 deletion queue<br>"
      "&nbsp;&nbsp;+ <span style='font-family:" + MONO + "'>/upcall/v1/validate</span> 校验 generation<br><br>"
      "S3 路径：<span style='font-family:" + MONO + "'>tenants/&lt;tenant_shard_id&gt;/timelines/&lt;tl_id&gt;/</span>",
      fs=11.5, color=DIM, lh=1.65),
    # bottom
    R("ip3-bg", 96, 524, 1088, 138, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("ip3-h", 116, 536, 600, 20, "为什么不直接 LIST S3？", fs=13, fw=800, color=AC),
    T("ip3-b", 116, 562, 1048, 92,
      "• <b>LIST 慢且贵</b>：一个 timeline 可能上万 layer，冷启动逐页 LIST 要秒级～分钟级，还按请求计费<br>"
      "• <b>LIST 无法表达元信息</b>：ancestor_lsn、GC 状态、compaction 断点这些都不在文件名里<br>"
      "• <b>LIST 结果最终一致，读不出「一致快照」</b>：写入中途 LIST 可能看到半套 layer；单个 JSON 的<b>原子 PUT</b> 天然是一致点<br>"
      "• 代价：index 是 timeline 级<b>写热点</b>，每批 layer 变更都要重传整份（生产上层数多时 index 自身可达 MB 级）",
      fs=12, color=DIM, lh=1.65),
], p, notes="index_part.json 是远端 timeline 的权威清单，Pageserver 靠它而不是 LIST S3 来重建状态。内容：layer_metadata 全部 layer 文件名+元数据（不变量：索引列出的必须已在S3）、disk_consistent_lsn、TimelineMetadata（含 ancestor/ancestor_lsn）、lineage 血缘、gc_blocking、gc_compaction 断点、deleted_at/archived_at/marked_invisible_at、rel_size_migration。version 当前 15，KNOWN_VERSIONS 1到15 都要能读，必须前后双向兼容。三个角色：①attach 时读它重建 LayerMap 所以本地空也能服务；②防脑裂裁决者，key 带 generation 后缀 index_part.json-<gen>，新 PS 取能读到的最高 generation，老 PS 写自己那份互不覆盖（RFC 025）；③GC 记账本，GC 只解链不删对象，真删走 deletion queue + validate 校验。不用 LIST 的原因：慢且贵、无法表达元信息、最终一致读不出一致快照。代价是 index 成为 timeline 级写热点，每次变更重传整份。代码：pageserver/src/tenant/remote_timeline_client/index.rs:29 struct IndexPart，:151 LATEST_VERSION=15，:157 FILE_NAME。")

# ─────── 读路径 LSN 定位 ───────
p += 1
std("s-read-lsn", "读路径", "Page → LSN：Compute 怎么知道该用什么 LSN 请求", [
    T("rl-desc", 96, 168, 1088, 36,
      "Pageserver 按 page + LSN 定位版本。Compute 侧通过 <b>Last Written LSN (LwLSN) 缓存</b> 为每个 page 跟踪「最后被修改的 WAL 位置」。",
      fs=14, color=DIM, lh=1.5),
    # LwLSN Cache structure
    R("rl-lw-bg", 96, 218, 530, 200, fill=PANEL, stroke=EDGE, radius=12),
    T("rl-lw-h", 116, 230, 400, 22, "LwLSN Cache（共享内存 LRU Hash）", fs=15, fw=800, color=AC),
    T("rl-lw-b", 116, 260, 490, 150,
      "<span style='font-family:" + MONO + "'>key = BufferTag(spcOid, dbOid, relNode, forkNum, blkNum)</span><br>"
      "<span style='font-family:" + MONO + "'>val = XLogRecPtr</span> = 该 page 的 <b>last_written_lsn</b>（最后修改的 WAL LSN）<br><br>"
      "• 每次产生 WAL record 时，经 <b>set_lwlsn_block_hook</b> 写入缓存<br>"
      "• 大小由 GUC <span style='font-family:" + MONO + "'>neon.last_written_lsn_cache_size</span> 控制，默认 <b>128K 条目</b><br>"
      "• LRU 淘汰后回退到全局 <b>maxLastWrittenLsn</b>（所有被淘汰页的 LSN 上界）",
      fs=12, color=DIM, lh=1.7),
    # Primary vs Replica
    R("rl-pri-bg", 646, 218, 540, 200, fill=PANEL, stroke=EDGE, radius=12),
    T("rl-pri-h", 666, 230, 400, 22, "neon_get_request_lsns()：决定请求 LSN", fs=15, fw=800, color=AC2),
    T("rl-pri-b", 666, 260, 500, 150,
      "<b>Primary 节点</b><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>request_lsn = UINT64_MAX</span>（「给我最新版」）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>not_modified_since = last_written_lsn</span>（缓存优化）<br><br>"
      "<b>Replica 节点</b><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>request_lsn = max(last_written_lsn, replay_lsn)</span><br>"
      "&nbsp;&nbsp;保证读到<b>一致性快照</b>——等同传统 PG 从磁盘读 page-at-point-in-time",
      fs=12, color=DIM, lh=1.7),
    # Flow diagram
    R("rl-flow-bg", 96, 432, 1088, 110, fill=PANEL, stroke=EDGE, radius=10),
    T("rl-flow-h", 116, 444, 600, 20, "完整调用链", fs=13, fw=800, color=AC),
    T("rl-flow-b", 116, 470, 1048, 64,
      "<span style='font-family:" + MONO + "'>SELECT WHERE id=42</span> → 执行器需要 heap/index page → Buffer Miss → "
      "<span style='font-family:" + MONO + "'>neon_readv(rel, fork, blk)</span><br>"
      "&nbsp;&nbsp;→ <span style='font-family:" + MONO + "'>neon_get_request_lsns()</span> 查 LwLSN 缓存 → "
      "构造 <span style='font-family:" + MONO + "'>GetPage@LSN</span> 发往 Pageserver<br>"
      "&nbsp;&nbsp;→ PS 用 (Key, LSN) 在 LayerMap 中定位 delta/image 栈 → walredo → 返回 8KB page",
      fs=12, color=DIM, lh=1.6),
    # Key insight
    R("rl-key-bg", 96, 556, 1088, 100, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("rl-key-h", 116, 568, 600, 20, "关键认知", fs=13, fw=800, color=AC),
    T("rl-key-b", 116, 594, 1048, 54,
      "• <b>LSN 粒度是 page（8KB block），不是单条行</b> —— 一个 page 上的几十条行共享同一个 last_written_lsn<br>"
      "• 行级可见性仍靠传统 <b>MVCC（xmin/xmax + snapshot）</b>，不涉及 LSN —— LSN 只决定 PS 返回哪个版本的物理页<br>"
      "• Primary 用 <span style='font-family:" + MONO + "'>UINT64_MAX</span> 是为了避免与 GC horizon 竞态：主节点永远要最新页就不会被 GC 掉",
      fs=12, color=DIM, lh=1.6),
], p, notes="Compute 侧通过 LwLSN Cache 跟踪每个 page 最后修改的 WAL LSN。写入时经 set_lwlsn_block_hook 更新缓存（key=BufferTag, val=XLogRecPtr），128K 条目 LRU。读时 neon_get_request_lsns() 查缓存：Primary 发 UINT64_MAX(要最新) + not_modified_since 供 PS 缓存优化；Replica 发 max(lwlsn, replay_lsn) 保证一致性快照。关键：LSN 粒度是 page 不是 row，行可见性仍靠 MVCC。代码：pgxn/neon/neon_lwlsncache.c（缓存）、pgxn/neon/pagestore_smgr.c:507（request_lsns 计算）。")



p += 1
std("s-bc", "协调层", "Storage Broker & Storage Controller", [
    *card("bc1", 96, 180, 528, 380,
          "Storage Broker", [
              "<b>纯无状态 gRPC pub/sub</b>（tonic）",
              "",
              "解决两个问题：",
              "• SK / PS 相互发现（避免 O(n²) 直连）",
              "• SK 向订阅者广播 timeline 状态",
              "",
              "流向：<b>SK 周期性 publish</b>（push_loop）",
              "&nbsp;<b>PS subscribe</b> 并据此选主/切换 SK；",
              "&nbsp;PS 找不到候选时也会 publish discovery request",
              "",
              "唯一消息类型：<b>SafekeeperTimelineInfo</b>",
              "&nbsp;(remote_consistent_lsn, backup_lsn …)",
              "",
              "默认端口 <b>50051</b>（同端口暴露 /metrics）",
              "K8s 提供容错，本身无副本",
          ], hc="#7CB3F4", fs=13, headfs=18),
    *card("bc2", 656, 180, 528, 380,
          "Storage Controller", [
              "<b>PS + SK 统一管理面</b>",
              "把「多 shard、多副本」抽象成 tenant 单一实体",
              "",
              "API 四前缀：",
              "• /v1/…　　　PS 兼容 API",
              "• /control/v1/…　注册 PS/SK、shard split",
              "• /debug/v1/…　调试",
              "• /upcall/v1/…　PS 上调 /re-attach /validate",
              "",
              "持久化：独立 PostgreSQL（diesel）只存对象",
              "调度：reconciliation-loop（intent→reconcile）",
              "SK 侧：heartbeat 探活 + SafekeeperReconcilers 调度",
              "compute hook: notify-attach / notify-safekeepers",
          ], hc=AC, fs=13, headfs=18),
], p, notes="Storage Broker 无状态服务发现，SK publish / PS subscribe（+discovery pub）；Storage Controller 统一管理 PS 和 SK，reconciliation-loop 模式")

# ─────── Storage Controller 的 PG 表结构 ───────
p += 1
std("s-storcon-schema", "协调层", "Storage Controller 的元数据表（依赖一套独立 PG）", [
    T("scs-desc", 96, 166, 1088, 40,
      "storcon 用 <b>diesel</b> 把\"谁在哪、谁归谁管、谁该干啥\"落到独立 PG。"
      "<span style='color:" + DIM + "'>只存必须持久的少量对象（generation、policy、成员集合），业务读通常走内存。见 "
      "<code>persistence.rs:49-77</code>。<span style='color:" + AC2 + "'>hadron_*</span> 两表由上游 PR #12649 引入（非本 fork），目前仅有 schema。</span>",
      fs=13, color=DIM, lh=1.6),
    *card("scs1", 96, 212, 530, 218,
          "集群拓扑（节点注册表）", [
              "<b style='color:" + FG + "'>nodes</b> — pageserver 注册：id、http/pg/grpc 地址、AZ、",
              "&nbsp;scheduling_policy、lifecycle（drain/fill 等）",
              "",
              "<b style='color:" + FG + "'>safekeepers</b> — SK 注册（cplane 同步而来）：",
              "&nbsp;region、version、host/http_port、AZ、scheduling_policy",
              "",
              "<b style='color:" + FG + "'>hadron_safekeepers</b> — SK 自注册简表：",
              "&nbsp;sk_node_id + listen_http/pg 地址",
              "&nbsp;<span style='color:" + AC2 + "'>⚠ schema-only：仅建表，无业务代码读写</span>",
          ], hc="#7CB3F4", fs=11.5, headfs=15),
    *card("scs2", 656, 212, 530, 218,
          "租户 & 分片状态", [
              "<b style='color:" + FG + "'>tenant_shards</b> — 每个 shard 一行，核心之一：",
              "&nbsp;<b>generation</b>（单调递增防脑裂）、generation_pageserver（",
              "&nbsp;当前 attach 到哪台 PS）、placement_policy、splitting、",
              "&nbsp;shard_stripe_size、config(JSON)、preferred_az_id",
              "",
              "<b style='color:" + FG + "'>metadata_health</b> — 每个 shard 的元数据健康位：",
              "&nbsp;scrubber 巡检结果 (healthy, last_scrubbed_at)，",
              "&nbsp;FK ON DELETE CASCADE → tenant_shards",
          ], hc=AC, fs=11.5, headfs=15),
    *card("scs3", 96, 442, 530, 218,
          "Timeline ↔ SK 成员编排", [
              "<b style='color:" + FG + "'>timelines</b> — timeline 到 SK 成员集合：",
              "&nbsp;start_lsn(pg_lsn)、<b>generation</b>、sk_set / new_sk_set、",
              "&nbsp;cplane_notified_generation、sk_set_notified_generation",
              "",
              "<b style='color:" + FG + "'>safekeeper_timeline_pending_ops</b> — 待下发操作队列：",
              "&nbsp;op_kind ∈ {<b>pull</b>, <b>exclude</b>, <b>delete</b>}（reconciler 消费）",
              "",
              "<b style='color:" + FG + "'>hadron_timeline_safekeepers</b> — timeline",
              "&nbsp;→ sk_node_id 映射，legacy_endpoint_id(UUID) 兼容老数据",
              "&nbsp;<span style='color:" + AC2 + "'>⚠ schema-only：仅建表，无业务代码读写</span>",
          ], hc=AC2, fs=11.5, headfs=15),
    *card("scs4", 656, 442, 530, 218,
          "运维 & Schema 版本", [
              "<b style='color:" + FG + "'>controllers</b> — storcon 副本活性表：",
              "&nbsp;(address, started_at) 双主键，用于 <b>leader 选举</b>、",
              "&nbsp;防止多副本同时决策；get_leader / update_leader",
              "&nbsp;（persistence.rs:1252-1277）",
              "",
              "<b style='color:" + FG + "'>timeline_imports</b> — 外部 timeline 导入进度：",
              "&nbsp;shard_statuses(JSONB) 记录每个 shard 的导入状态",
              "",
              "<b style='color:" + FG + "'>__diesel_schema_migrations</b> — diesel embed_migrations",
              "&nbsp;版本表；启动时自动执行 ./migrations/*.sql",
          ], hc="#C89EFF", fs=11.5, headfs=15),
], p, notes="11 张表按 4 组归类。注意 hadron_safekeepers / hadron_timeline_safekeepers 来自上游 neondatabase/neon PR #12649（commit 8f627ea0a，2025-07-17），不是本 fork 新增；这两张表只有 schema.rs 声明和 migration 建表，没有任何 insert/select 代码，所以线上是空表。")

# ─────── 防脑裂 ───────

p += 1
divider("s-div4", 5, "核心原理深度剖析", p)
# ─────── Slide 10b: 落盘 → 上传 S3 的时机策略 ───────
p += 1
std("s-flush-policy", "PAGESERVER", "为什么 S3 有延迟：Ephemeral Layer 的滚动策略", [
    T("fp-desc", 96, 172, 1088, 44,
      "Compute 写入立即持久化在 Safekeeper，但 <b>Pageserver 侧落盘/上传 S3 有延迟</b>"
      "——不是攒批，是「三选一先到先触发」的滚动阈值。",
      fs=14, color=DIM, lh=1.6),
    *card("fp1", 96, 232, 350, 260,
          "① 内存层滚动 (freeze)", [
              "<span style='font-family:" + MONO + "'>should_roll()</span> 任一命中即滚动：",
              "",
              "<b>checkpoint_distance</b>　默认 <b>256 MiB</b>",
              "　累计 WAL 达阈值",
              "",
              "<b>checkpoint_timeout</b>　默认 <b>10 min</b>",
              "　距上次滚动超时（保底，防止低",
              "　流量 timeline 长期不落盘）",
              "",
              "两者取先到的那个",
          ], hc=AC, fs=12.5, headfs=15),
    *card("fp2", 460, 232, 350, 260,
          "② 定时兜底 + 落盘", [
              "<span style='font-family:" + MONO + "'>tenant_housekeeping_loop</span>",
              "每 <b>compaction_period</b>（默认 20s，±5%",
              "抖动）tick 一次，逐 timeline 调用",
              "<span style='font-family:" + MONO + "'>maybe_freeze_ephemeral_layer()</span>",
              "",
              "→ 保证超时条件能被真正触发",
              "",
              "冻结层由 <span style='font-family:" + MONO + "'>flush_loop</span> 异步写成",
              "本地 delta 文件（不可变）",
          ], hc=AC2, fs=12.5, headfs=15),
    *card("fp3", 824, 232, 360, 260,
          "③ 立即异步上传", [
              "本地落盘完成后<b>立刻</b>",
              "<span style='font-family:" + MONO + "'>schedule_layer_file_upload()</span>",
              "丢进上传队列，无额外定时器/批处理",
              "",
              "S3 PUT 作为后台任务并发执行",
              "（受 inprogress_tasks 并发上限）",
              "",
              "延迟 ≈ checkpoint 窗口 + 上传网络耗时",
          ], hc="#7CB3F4", fs=12.5, headfs=15),
    R("fp-lsn-bg", 96, 512, 1088, 118, fill=PANEL, stroke=EDGE, radius=10),
    T("fp-lsn-h", 116, 524, 500, 20, "三段式一致性 LSN", fs=13, fw=800, color=AC),
    T("fp-lsn-b", 116, 548, 1048, 74,
      "<span style='font-family:" + MONO + "'>last_record_lsn</span>　SK→PS 已收到、内存可读（WAL receiver 每 100 条批提交一次，与 S3 无关）<br>"
      "<span style='font-family:" + MONO + "'>disk_consistent_lsn</span>　冻结层已确认写到 <b>PS 本地磁盘</b><br>"
      "<span style='font-family:" + MONO + "'>remote_consistent_lsn</span>（visible）　上传 S3 并校验 generation 非陈旧后才前移 —— 只有它前移，SK 才能裁剪 WAL",
      fs=12, color=DIM, lh=1.7),
], p, notes="should_roll() pageserver/src/tenant/timeline.rs:2672-2719，三触发条件：LSN距离/层大小达 checkpoint_distance，或 opened_at 超过 checkpoint_timeout。默认值 libs/pageserver_api/src/config.rs:851(DEFAULT_CHECKPOINT_DISTANCE=256MiB),852(DEFAULT_CHECKPOINT_TIMEOUT=10m),861(DEFAULT_COMPACTION_PERIOD=20s)。housekeeping loop: pageserver/src/tenant/tasks.rs:427-451 tenant_housekeeping_loop，sleep_jitter(period, 5%)后调用tenant.housekeeping()→maybe_freeze_ephemeral_layer (timeline.rs:2148-2178)。flush_loop: timeline.rs:4928+，flush_frozen_layer写本地delta文件→schedule_uploads (timeline.rs:5334,5366-5370)。上传调度: remote_timeline_client.rs:1269-1279 schedule_layer_file_upload→launch_queued_tasks(2022)异步发起S3 PUT，无额外批处理定时器。一致性LSN: disk_consistent_lsn(timeline.rs:282,5320)本地磁盘确认；remote_consistent_lsn_projected/_visible(remote_timeline_client.rs:533,544,111-118,2393-2401)，_visible只在上传确认+generation非陈旧后前移，是这个值通报给SK允许裁剪WAL。ingest批处理 DEFAULT_INGEST_BATCH_SIZE=100 (config.rs:688)，只影响PS内部可读性与S3无关。")

# ─────── Slide 10a-2: L0 → L1 compaction 触发时机 ───────
p += 1
std("s-l0-compact-trigger", "PAGESERVER", "L0 什么时候变成 L1：计数阈值 + 事件驱动", [
    T("l0c-desc", 96, 172, 1088, 40,
      "不是纯定时器攒批——L0 数量到阈值就立刻触发，定时轮询只是兜底。",
      fs=14, color=DIM, lh=1.6),
    *card("l0c1", 96, 224, 350, 230,
          "① 触发条件", [
              "<span style='font-family:" + MONO + "'>compaction_threshold</span>　默认 <b>10</b>",
              "　L0 delta layer 数量达到即触发",
              "",
              "compaction.rs:1902　if level0_deltas.len()",
              "&nbsp;&nbsp;&lt; threshold { 直接返回，不做事 }",
              "",
              "每次 flush 冻结层后都会检查一次",
              "（timeline.rs:5055-5056），命中就立即",
              "<span style='font-family:" + MONO + "'>l0_compaction_trigger.notify_one()</span>",
          ], hc=AC, fs=12.5, headfs=15),
    *card("l0c2", 460, 224, 350, 230,
          "② 定时兜底", [
              "<span style='font-family:" + MONO + "'>compaction_loop</span>（tasks.rs:216）",
              "醒来条件取先到者：",
              "",
              "• <span style='font-family:" + MONO + "'>compaction_period</span> 到点（默认 20s）",
              "• 事件通知（见①）",
              "• 上轮失败后的 backoff 重试",
              "",
              "上轮结果是 YieldForL0/Pending 时",
              "会立即自我重新通知，接着跑下一轮",
          ], hc=AC2, fs=12.5, headfs=15),
    *card("l0c3", 824, 224, 360, 230,
          "③ 与背压阈值的关系", [
              "<span style='font-family:" + MONO + "'>l0_flush_delay_threshold</span>",
              "　= 3×compaction_threshold = <b>30</b>",
              "　超过 → flush 拖慢到 2× 耗时",
              "",
              "<span style='font-family:" + MONO + "'>l0_flush_stall_threshold</span>",
              "　默认<b>关闭</b>，开启会完全阻塞摄入",
              "",
              "10（该合并了）&lt; 30（拖慢）&lt; stall（阻塞，默认无）",
          ], hc="#7CB3F4", fs=12.5, headfs=15),
    R("l0c-algo-bg", 96, 470, 1088, 130, fill=PANEL, stroke=EDGE, radius=10),
    T("l0c-algo-h", 116, 482, 500, 20, "合并算法：不是一把梭，是分批 + k-way merge", fs=13, fw=800, color=AC),
    T("l0c-algo-b", 116, 506, 1048, 86,
      "1. 按起始 LSN 排序，只取<b>连续无 LSN 空洞</b>的一段（compaction.rs:1967-2014），遇到断档就停<br>"
      "2. 按字节量上限截断本轮处理量（<span style='font-family:" + MONO + "'>compaction_threshold × checkpoint_distance</span>），处理不完标记未完成，留给下一轮——积压大时是分批，不是一次全吃<br>"
      "3. 选中的 L0 用 <span style='font-family:" + MONO + "'>MergeIterator</span> 做 <b>k-way 流式合并</b>（compaction.rs:2156），按 key/LSN 顺序产出新 L1 delta layer",
      fs=12, color=DIM, lh=1.7),
], p, notes="compaction_loop: pageserver/src/tenant/tasks.rs:216，wake条件取先到者：sleep(period)(tasks.rs:255,240,period来自get_compaction_period默认DEFAULT_COMPACTION_PERIOD=20s config.rs:861)，或l0_compaction_trigger.notified()(tasks.rs:256)，或上轮失败backoff(tasks.rs:254)。触发通知：timeline.rs:5055 l0_count>=get_compaction_threshold()后, :5056 notify_one()立即唤醒无需等满一个period。tasks.rs:277-278循环结果为YieldForL0/Pending时自我重新notify接着跑。阈值：compaction_threshold定义config.rs:533，默认DEFAULT_COMPACTION_THRESHOLD=10(config.rs:862,920)。检查代码compaction.rs:1902-1903 if level0_deltas.is_empty()||level0_deltas.len()<threshold提前返回(compact_level0_phase1起始:1883,提前返回:1938)。get_compaction_threshold() timeline.rs:2883。背压联动：l0_flush_delay_threshold(get_l0_flush_delay_threshold timeline.rs:2929-2957)默认=3×compaction_threshold=30(DEFAULT_L0_FLUSH_DELAY_FACTOR=3,timeline.rs:2932)，达到后flush变2倍慢(timeline.rs:5062)；l0_flush_stall_threshold(timeline.rs:2959-3007)默认DEFAULT_L0_FLUSH_STALL_FACTOR=0即禁用(timeline.rs:2963)，开启后l0_count>=阈值时完全阻塞flush(timeline.rs:5010-5011)，两者都clamp到>=compaction_threshold(timeline.rs:2955,3006)。合并算法compact_level0(compaction.rs:1840)委托compact_level0_phase1(:1883)：按起始LSN排序(:1967)取连续LSN run无空洞(:1970-2014)；delta_size_limit=max(compaction_upper_limit,compaction_threshold)*checkpoint_distance(:1983-1987)超限则fully_compacted=false留下一轮(:2002-2013)；k-way合并用MergeIterator::create_with_options(:2156-2162,来自storage_layer/merge_iterator.rs,import at:59)按key/LSN顺序产出target_file_size大小的新L1 delta layer。")

# ─────── Slide 10c: pg_current_wal_lsn 在整条 LSN 链路里的位置 ───────
p += 1
std("s-lsn-chain", "PAGESERVER", "一条 WAL 的完整生命周期：8 个 LSN 检查点", [
    T("lc-desc", 96, 172, 1088, 40,
      "<span style='font-family:" + MONO + "'>SELECT pg_current_wal_lsn();</span> 返回的只是<b>最靠前、最不保险</b>的那个检查点——"
      "compute 本机写到 OS 但未必 fsync，跟 Neon 的持久化保证无关。",
      fs=14, color=DIM, lh=1.6),
    *[e for i, (mono, desc, note, c) in enumerate([
        ("GetXLogInsertRecPtr()", "compute 内存 reserve/insert", "最大值，纯内存态", AC2),
        ("pg_current_wal_lsn()", "compute 写到 OS，未必 fsync", "GetXLogWriteRecPtr()／本题问的就是它", AC2),
        ("pg_current_wal_flush_lsn()", "compute 本地已 fsync", "GetFlushRecPtr()", AC2),
        ("availableLsn", "walproposer 已打包待发 SK", "walproposer.c:246", "#C89EFF"),
        ("flushLSN", "某 Safekeeper 本地已 fsync", "safekeeper-protocol.md:36", "#C89EFF"),
        ("commitLSN", "多数派确认 → client 收到 COMMIT OK", "quorum=2 of 3，容灾边界", AC),
        ("last_record_lsn", "Pageserver 已处理到此", "内存可读，WAL receiver 批提交", "#7CB3F4"),
        ("disk_consistent_lsn", "PS 本地磁盘落盘确认", "冻结层 flush 完成", "#7CB3F4"),
        ("remote_consistent_lsn", "S3 上传确认（visible）", "最落后，但唯一真正 crash-durable", "#7CB3F4"),
    ]) for e in (
        R(f"lc{i}bg", 96, 226 + i * 42, 1088, 36, fill="rgba(255,255,255,0.035)", stroke="none", sw=0, radius=8),
        T(f"lc{i}m", 116, 233 + i * 42, 270, 22, mono, fs=13, fw=700, color=c, ff=MONO),
        T(f"lc{i}d", 398, 234 + i * 42, 330, 20, desc, fs=13, fw=500, color=FG),
        T(f"lc{i}n", 738, 234 + i * 42, 430, 20, note, fs=11.5, fw=500, color=FAINT),
    )],
    T("lc-note", 96, 616, 1088, 40,
      "<b>不等号方向</b>：Insert ≥ Write(<span style='font-family:" + MONO + "'>pg_current_wal_lsn</span>) ≥ Flush ≥ availableLsn ≥ flushLSN ≥ commitLSN ≥ last_record_lsn ≥ disk_consistent_lsn ≥ remote_consistent_lsn。"
      "每往下一级都是更强的持久化/可见性承诺，也离 compute 越远。",
      fs=12.5, color=AC, lh=1.5),
], p, notes="pg_current_wal_lsn() = GetXLogWriteRecPtr()，src/backend/access/transam/xlogfuncs.c:279,289；未经Neon改动的原生Postgres函数(diff REL_16_1 vs REL_16_STABLE_neon的xlogfuncs.c为空)。返回LogwrtResult.Write（xlog.c:9230-9238），写到OS但未必fsync，注释xlogfuncs.c:271-276明确'written out to the kernel, but is not necessarily synced to disk'。对比：pg_current_wal_insert_lsn()→GetXLogInsertRecPtr()(xlog.c:9214-9225)最大；pg_current_wal_flush_lsn()→GetFlushRecPtr()(xlog.c:6280-6294)。walproposer只消费GetFlushRecPtr作为本地信号(walproposer_pg.c:923-930 walprop_pg_get_flush_rec_ptr,walproposer.c:296-301轮询检测新WAL广播,availableLsn在WalProposerBroadcast处bump走proposer.c:242-248)，从不修改这些getter。docs/glossary.md:107-128完整LSN链路定义；docs/safekeeper-protocol.md:8-9,36 flushLSN/commitLSN定义；pageserver/src/tenant/timeline.rs:267,1720-1721 last_record_lsn，:282,5320 disk_consistent_lsn。全链路不等式：Insert≥Write(pg_current_wal_lsn)≥Flush(pg_current_wal_flush_lsn)≥availableLsn≥flushLSN≥commitLSN≥last_record_lsn≥disk_consistent_lsn≥remote_consistent_lsn。")

# ─────── Slide 13: WAL Redo 沙箱 ───────
p += 1
std("s-walredo", "PAGESERVER", "WAL Redo：每租户独立的 seccomp 沙箱", [
    T("wr-desc", 96, 175, 1088, 60,
      "重建历史版本的页需要执行 Postgres WAL redo 代码 —— 这些代码不能信任跨租户数据。<br>"
      "Neon 的方案：<b>每个 tenant 懒启动一个独立的 postgres 子进程做 redo，seccomp(2) 限制到最小系统调用集；进程长驻复用，空闲 180s 后回收</b>。",
      fs=15, color=DIM, lh=1.7),
    # diagram
    R("wrd-ps", 96, 260, 260, 260, fill="rgba(0,229,153,0.08)", stroke="rgba(0,229,153,0.4)"),
    T("wrd-pst", 96, 274, 260, 24, "Pageserver 主进程", fs=14, fw=700, color=AC, align="center"),
    T("wrd-psn", 116, 310, 220, 200,
      "GetPage 请求<br>→ 查 LayerMap<br>→ 读取 image + deltas<br>→ 通过 pipe 发送给 redo 子进程<br>→ 收回重建后的 8KB page",
      fs=12, color=DIM, lh=1.7),
    # arrows
    LN("wrd-a1", 356, 340, 100, 0, stroke=A_ORG, sw=2),
    T("wrd-a1t", 356, 316, 100, 20, "pipe (stdin)", fs=11, fw=700, color=A_ORG, align="center"),
    LN("wrd-a2", 456, 390, -100, 0, stroke=A_GRN, sw=2),
    T("wrd-a2t", 356, 396, 100, 20, "pipe (stdout)", fs=11, fw=700, color=A_GRN, align="center"),
    # redo child 1
    R("wrd-c1", 466, 260, 320, 120, fill="rgba(255,158,138,0.08)", stroke="rgba(255,158,138,0.4)"),
    T("wrd-c1t", 466, 272, 320, 22, "tenant A: postgres --wal-redo (seccomp)", fs=12, fw=700, color=AC2, align="center", ff=MONO),
    T("wrd-c1b", 486, 300, 280, 74,
      "• 仅允许 read/write pipe<br>• 无网络、无 fs、无 fork<br>• 首请求 lazy spawn，长驻复用<br>• 崩溃不影响其他 tenant",
      fs=11, color=DIM, lh=1.6),
    R("wrd-c2", 466, 400, 320, 120, fill="rgba(255,158,138,0.05)", stroke="rgba(255,158,138,0.3)"),
    T("wrd-c2t", 466, 412, 320, 22, "tenant B: postgres --wal-redo (seccomp)", fs=12, fw=700, color=AC2, align="center", ff=MONO),
    T("wrd-c2b", 486, 440, 280, 74,
      "• 独立进程 / 独立地址空间<br>• 恶意 WAL 无法越权<br>• 空闲 180s 被回收，下次重启<br>• 复用官方 Postgres redo 代码",
      fs=11, color=DIM, lh=1.6),
    # explanation
    R("wrd-note", 820, 260, 366, 260, fill="rgba(124,179,244,0.06)", stroke="rgba(124,179,244,0.3)"),
    T("wrd-noteh", 840, 276, 320, 22, "为什么这样设计？", fs=14, fw=700, color="#7CB3F4"),
    T("wrd-noteb", 840, 306, 326, 210,
      "① 直接把 pg redo 编入 pageserver → 一个 tenant 的坏 WAL 能<b>破坏所有 tenant</b><br><br>"
      "② 抽象成 Rust 重写 → 数万行 pg C 代码，<b>维护成本爆炸</b><br><br>"
      "③ Neon 选择：<b>复用官方 pg redo</b> + 沙箱进程隔离 —— 稳定性与安全兼得",
      fs=12, color=DIM, lh=1.7),
], p, notes="每 tenant 至多一个 seccomp 沙箱 postgres 进程做 WAL redo；首请求 lazy spawn、长驻复用、空闲 180s 由 housekeeping 循环回收（tenant.rs WALREDO_IDLE_TIMEOUT）。")

# ─────── WAL Redo 沙箱细节 ───────
p += 1
std("s-walredo-sec", "PAGESERVER", "沙箱边界细节：seccomp 白名单、加固与逃逸风险", [
    *card("wrs1", 96, 172, 528, 244,
          "① syscall 白名单（walredoproc.c:174-206）", [
              "<span style='font-family:" + MONO + "'>exit_group / read / write / select / pselect6</span>　硬需求",
              "<span style='font-family:" + MONO + "'>brk</span>　内存分配（glibc 只走 brk）",
              "<span style='font-family:" + MONO + "'>mmap / munmap</span>　仅 musl 下放开（无 mallopt）",
              "<span style='font-family:" + MONO + "'>getpid</span>（assert 失败路径）<span style='font-family:" + MONO + "'>futex</span>（errbacktrace）",
              "",
              "<b>就这些。</b>没有 open/openat、没有任何 socket 调用、",
              "没有 fork/execve/clone、没有 ptrace",
              "默认动作 <b>SCMP_ACT_TRAP</b> → SIGSYS → 打印",
              "<span style='font-family:" + MONO + "'>seccomp: bad syscall &lt;n&gt;</span> 后 <span style='font-family:" + MONO + "'>_exit(1)</span>",
          ], hc=AC2, fs=13, headfs=15),
    *card("wrs2", 656, 172, 528, 244,
          "② 进沙箱前的额外加固", [
              "<span style='font-family:" + MONO + "'>close_range(3, ~0U, 0)</span>　关掉 PS 泄漏的所有 FD",
              "<span style='font-family:" + MONO + "'>mallopt(M_MMAP_MAX, 0)</span>　逼 malloc 只用 brk，",
              "&nbsp;&nbsp;这样 <b>连 mmap 都不必放开</b>",
              "Rust 侧 <span style='font-family:" + MONO + "'>.env_clear()</span>，只留 LD_LIBRARY_PATH / *SAN",
              "",
              "<b>自检式加载</b>（seccomp.c:111-171）：先验证 openat 可用",
              "→ 装只 trap openat 的测试 filter → 确认真被 trap",
              "→ 才装正式 deny handler + 全量白名单",
              "<b>时机</b>：延迟到主循环前才 enter，让启动路径不必上榜",
          ], hc="#7CB3F4", fs=13, headfs=15),
    *card("wrs3", 96, 430, 528, 214,
          "③ 逃逸风险 & 明确没做的事", [
              "<b>无 namespace、无 chroot</b> —— 文件系统隔离<b>只</b>靠不放",
              "&nbsp;&nbsp;开 open/openat；chroot + mount ns 仍是 TODO（seccomp.c:67-73）",
              "seccomp <b>只看 syscall 号，基本不查参数</b> → 已放开的",
              "&nbsp;&nbsp;read/write 上依然可以乱来",
              "stderr <b>无长度上限</b>：process.rs:133 明写「不信任子进程",
              "&nbsp;&nbsp;限制 stderr 长度，目前可无界 Vec 分配」→ 可打爆 PS 内存",
              "用 TRAP 而非 <span style='font-family:" + MONO + "'>SCMP_ACT_KILL_PROCESS</span>，是 open question",
              "<span style='font-family:" + MONO + "'>--disable-seccomp</span> 可把沙箱整体关掉",
          ], hc="#FFD54A", fs=12.5, headfs=15),
    *card("wrs4", 656, 430, 528, 214,
          "④ 租户隔离边界到哪为止", [
              "<b>一 tenant shard 一进程</b>：PostgresRedoManager，",
              "&nbsp;&nbsp;tenant.rs:1364；heavier_once_cell 合并并发 launch",
              "<b>信任模型</b>（process.rs:90-97）：首个 redo 请求<b>之前</b>可信，",
              "&nbsp;&nbsp;之后不可信 —— 前提是它已关 FD 且已自沙箱",
              "被劫持的进程<b>能看到的只有本 tenant 的数据</b>",
              "<span style='font-family:" + MONO + "'>redo_block_filter</span>：WAL 记录碰到非目标页 → warn + 忽略",
              "<span style='font-family:" + MONO + "'>NoLeakChild</span>：drop 即 SIGKILL + wait；detach 用 gate 兜底",
              "<b>注</b>：仓库内无公开的越权事故记录，以上是设计防线",
          ], hc=AC, fs=12.5, headfs=15),
], p, notes="沙箱细节全部对齐源码：白名单在 pgxn/neon_walredo/walredoproc.c:174-206（allowed_syscalls[]），默认动作 SCMP_ACT_TRAP 在 seccomp.c:167，deny handler seccomp.c:240-262 打印 seccomp: bad syscall 并 _exit(1)。#if 0 里的 shmctl/shmdt/unlink 是「优雅 shutdown 才需要」的调用，Neon 选择不放开、改用 _exit(0) 直接退（walredoproc.c:410-419）。enter_seccomp_mode 在 walredoproc.c:208-227：先 close_range(3,~0U,0) 因为 pageserver 可能漏 FD，再 mallopt(M_MMAP_MAX,0) 让 glibc malloc 只用 brk（MALLOC_NO_MMAP 定义在 62-65）。seccomp_load_rules 有自检：装 SIGSYS handler → 确认 openat 正常 → 装只 trap openat 的测试 filter → 确认 trap 触发 → 才装真 handler 和全量 filter。Rust 侧 WalRedoProcess::launch 在 process.rs:58-99：argv 是 postgres --wal-redo --tenant-shard-id，三管道，env_clear 只留 LD_LIBRARY_PATH/DYLD_LIBRARY_PATH/ASAN/UBSAN。风险面：没有 namespace/chroot，seccomp.c:67-73 把它列为未实现想法；stderr 无界是已知 TODO（process.rs:133）；--disable-seccomp 可关（walredoproc.c:346-350）。完整威胁模型见 docs/pageserver-walredo.md:13-45，设计取舍见 docs/core_changes.md:238-254。")

# ─────── 背压 ───────
p += 1
std("s-bp", "全链路", "背压：三层限速把写入速度钉在存储能力上", [
    T("bp-desc", 96, 168, 1088, 40,
      "Compute 能无限快地产 WAL，Pageserver 摄入/compaction 却有上限。三处独立机制防止差距无界扩大。",
      fs=14, color=DIM, lh=1.5),
    # Layer 1: compute
    R("bp1-bg", 96, 216, 350, 240, fill=PANEL, stroke=EDGE, radius=12),
    T("bp1-n", 116, 228, 120, 18, "① COMPUTE", fs=11, fw=800, color=AC, ff=MONO),
    T("bp1-h", 116, 250, 310, 22, "用户 backend 自己睡", fs=15, fw=800, color=AC),
    T("bp1-b", 116, 278, 310, 170,
      "lag = 本地 flushLsn − PS 反馈 LSN − 阈值<br>"
      "<span style='font-family:" + MONO + "'>write_lag</span> ← last_received_lsn　<b>500 MB</b><br>"
      "<span style='font-family:" + MONO + "'>flush_lag</span> ← disk_consistent_lsn　<b>10 GB</b><br>"
      "<span style='font-family:" + MONO + "'>apply_lag</span> ← remote_consistent_lsn　<b>0=关</b><br>"
      "&nbsp;&nbsp;开启 = <b>写</b>不许超前 S3 持久化太多<br>"
      "&nbsp;&nbsp;（钳崩溃丢失窗口，强容灾；<b>不卡读</b>）<br>"
      "挂在 <b>ProcessInterrupts</b> 回调上：lag&gt;0 就<br>"
      "<span style='font-family:" + MONO + "'>pg_usleep(10ms)</span> 并返回 true → 反复重入<br>"
      "只卡写事务；只读事务和 walsender 豁免<br>"
      "多 shard 取<b>最慢 shard</b> 的 LSN",
      fs=11.5, color=DIM, lh=1.6),
    # Layer 2: pageserver ingest
    R("bp2-bg", 465, 216, 350, 240, fill=PANEL, stroke=EDGE, radius=12),
    T("bp2-n", 485, 228, 120, 18, "② PS 摄入侧", fs=11, fw=800, color=AC2, ff=MONO),
    T("bp2-h", 485, 250, 310, 22, "L0 堆积 → 减速/停摆", fs=15, fw=800, color=AC2),
    T("bp2-b", 485, 278, 310, 170,
      "<span style='font-family:" + MONO + "'>l0_flush_delay_threshold</span><br>"
      "&nbsp;&nbsp;默认 3×compaction_threshold = <b>30 层</b><br>"
      "&nbsp;&nbsp;→ flush 后再睡「一次 flush 耗时」＝<b>2× 慢</b><br>"
      "<span style='font-family:" + MONO + "'>l0_flush_stall_threshold</span>　<b>默认关闭</b><br>"
      "&nbsp;&nbsp;→ 触发则完全阻塞到降回阈值下<br>"
      "&nbsp;&nbsp;compaction 已失败时自动豁免（防死锁）<br><br>"
      "传导到摄入：ephemeral layer <b>roll 时</b>等 flush<br>"
      "完成，从而卡住 WAL ingest 任务",
      fs=11.5, color=DIM, lh=1.6),
    # Layer 3: read path
    R("bp3-bg", 834, 216, 350, 240, fill=PANEL, stroke=EDGE, radius=12),
    T("bp3-n", 854, 228, 120, 18, "③ PS 读路径", fs=11, fw=800, color="#7CB3F4", ff=MONO),
    T("bp3-h", 854, 250, 310, 22, "等 LSN 追平 / 请求限流", fs=15, fw=800, color="#7CB3F4"),
    T("bp3-b", 854, 278, 310, 170,
      "<b>wait_lsn</b>：GetPage 要的 LSN 还没摄入 →<br>"
      "&nbsp;&nbsp;阻塞等，超时 <span style='font-family:" + MONO + "'>wait_lsn_timeout</span> <b>300 s</b><br>"
      "&nbsp;&nbsp;（pageserver/src/config.rs 另有 60 s 用于本地）<br><br>"
      "<b>l0_flush 全局并发</b>：Semaphore = <b>num_cpus</b><br>"
      "&nbsp;&nbsp;是并发数上限，不是字节预算<br><br>"
      "<b>timeline_get_throttle</b>：leaky bucket 限 RPS<br>"
      "&nbsp;&nbsp;refill_amount / refill_interval，<b>默认禁用</b>",
      fs=11.5, color=DIM, lh=1.6),
    # bottom notes
    R("bp4-bg", 96, 470, 1088, 192, fill=PANEL, stroke=EDGE, radius=10),
    T("bp4-h", 116, 482, 600, 20, "运维要点", fs=13, fw=800, color=AC),
    T("bp4-b", 116, 508, 1048, 145,
      "• <b>没有超时上限</b>：PS 挂掉/追不上时反馈 LSN 停止推进，写事务被 10 ms 一轮地无限期节流 —— 这是有意的取舍，"
      "用写可用性换 lag 有界<br>"
      "• <b>可观测</b>：<span style='font-family:" + MONO + "'>neon.backpressure_throttling_time()</span> 累计节流微秒数、"
      "<span style='font-family:" + MONO + "'>neon.backpressure_lsns()</span> 看三个反馈 LSN<br>"
      "&nbsp;&nbsp;Prometheus 指标 compute_backpressure_throttling_seconds_total 由前者换算<br>"
      "• <b>配置陷阱</b>：flush_lag 设得比 PS checkpoint 间隔还小会硬死锁（manifest 里有明确警告）<br>"
      "• 本地开发 control_plane 把 write_lag 压到 15 MB，便于复现节流；生产用 manifest 的 500 MB / 10 GB<br>"
      "• 旧的 <span style='font-family:" + MONO + "'>l0_flush_wait_upload</span>（flush 等上传）<b>已移除</b>，被 L0 compaction 背压取代",
      fs=11.5, color=DIM, lh=1.6),
], p, notes="背压分三层。①Compute侧：三个 max_replication_*_lag GUC，单位MB，write=500MB(对last_received_lsn) flush=10GB(对disk_consistent_lsn) apply=0关闭(对remote_consistent_lsn)。关于 apply_lag 语义：判断条件是 myFlushLsn > applyPtr + max_replication_apply_lag*MB 即本地已flush的LSN超前 remote_consistent_lsn(=已持久化到S3的最新LSN) 超过阈值才节流（walproposer_pg.c:546-548），不是等追平；=0 时该检查直接跳过(关闭)。开启的语义是限制写入速度不超前S3持久化进度太多，从而钳制 compute 崩溃/灾难恢复时的丢失窗口（强容灾），普通业务不需要。注意 apply_lag 只钳制写事务速度，不影响读：Primary 读走 neon_get_request_lsns 的 UINT64_MAX 路径仍能读到刚写入未持久化的数据。applyPtr=min_ps_feedback.remote_consistent_lsn(walproposer_pg.c:791)。实现是挂在 ProcessInterrupts 回调 backpressure_throttling_impl 上(walproposer_pg.c:625)，用户 backend 自己 pg_usleep(10ms/BACK_PRESSURE_DELAY) 后返回 true 导致反复重入，只卡写事务(am_walsender 和无事务ID即只读事务豁免，但 CREATE INDEX CONCURRENTLY 因 PROC_IN_SAFE_IC 仍节流)，多shard取最慢的。②PS摄入侧：l0_flush_delay_threshold 默认3倍compaction_threshold=30层，触发后延迟一次flush耗时即2倍慢；l0_flush_stall_threshold 默认关闭，触发则完全阻塞，compaction失败时豁免防死锁。传导路径是 ephemeral layer roll 时等 flush 完成从而卡住 ingest。③读路径：wait_lsn 等LSN追平默认超时300s；l0_flush 全局 Semaphore=num_cpus 限并发；timeline_get_throttle leaky bucket 默认禁用。运维要点：无超时上限，PS挂了写会无限期节流；用 neon.backpressure_throttling_time() 观测；flush_lag 小于 checkpoint 间隔会硬死锁。")

# ─────── Slide 14: Compaction & GC ───────
p += 1
std("s-compact", "PAGESERVER", "Compaction & GC 关键参数", [
    T("cp-desc", 96, 170, 1088, 40,
      "所有默认值来自 pageserver config，可 per-tenant override。",
      fs=15, color=DIM, lh=1.5),
    # table
    R("cpt-bg", 96, 220, 528, 380, fill=PANEL, stroke=EDGE, radius=12),
    T("cpt-h", 116, 236, 496, 26, "Compaction", fs=17, fw=800, color=AC),
    *[T(f"cpt-l{i}", 116, 274 + i * 40, 496, 26,
        f"<span style='color:#00E599;font-family:{MONO};font-weight:700'>{k}</span>&nbsp;&nbsp;{v}",
        fs=14, color=DIM, lh=1.3)
      for i, (k, v) in enumerate([
          ("checkpoint_distance", "= <b>256 MB</b>（open layer 大小）"),
          ("checkpoint_timeout", "= <b>10 min</b>"),
          ("compaction_period", "= <b>20 s</b>（扫描周期）"),
          ("compaction_threshold", "= <b>10</b> 个 L0 触发合并"),
          ("compaction_upper_limit", "= <b>20</b> 个 L0 单次上限"),
          ("compaction_target_size", "= <b>128 MB</b> (L1 目标)"),
          ("image_creation_threshold", "= <b>3</b> 个 delta → 物化 image"),
          ("背压：l0_flush_delay", "≥ <b>30</b> 层 → flush 延迟 2×"),
      ])],
    R("gc-bg", 656, 220, 528, 380, fill=PANEL, stroke=EDGE, radius=12),
    T("gc-h", 676, 236, 496, 26, "GC & 保留策略", fs=17, fw=800, color=AC2),
    *[T(f"gc-l{i}", 676, 274 + i * 40, 496, 26,
        f"<span style='color:#FF9E8A;font-family:{MONO};font-weight:700'>{k}</span>&nbsp;&nbsp;{v}",
        fs=14, color=DIM, lh=1.3)
      for i, (k, v) in enumerate([
          ("gc_period", "= <b>1 h</b>"),
          ("pitr_interval", "= <b>7 天</b> (默认保留窗口)"),
          ("gc_horizon", "= <b>64 MB</b> WAL"),
          ("max_replication_write_lag", "= <b>500 MB</b>"),
          ("max_replication_flush_lag", "= <b>10 GB</b>"),
          ("page_cache_size", "= <b>64 MB</b> (跨 tenant 共享)"),
          ("熔断器", "连续 <b>5 次</b> compact 失败 → 禁 24h"),
          ("CONCURRENT_BG_TASKS", "= <b>3/4 × CPU</b>"),
      ])],
], p, notes="Compaction 关键参数：256MB/10min/L0=10/L1=128MB/image_thr=3；GC：7 天 PITR，5 次失败熔断")

# ─────── Timeline 分支 GC ───────
p += 1
std("s-gc", "PAGESERVER", "Timeline / 分支 GC：谁能被回收", [
    T("gcx-desc", 96, 170, 1088, 44,
      "GC 删的是<b>整个历史 layer 文件</b>，不做文件内部裁剪。"
      "<span style='font-family:" + MONO + "'>tasks.rs gc_loop → gc_iteration → Timeline::gc_timeline</span>",
      fs=14, color=DIM, lh=1.5),
    R("gcx1-bg", 96, 222, 530, 262, fill=PANEL, stroke=EDGE, radius=12),
    T("gcx1-h", 116, 238, 490, 24, "两条 cutoff 取更保守的那条", fs=16, fw=800, color=AC),
    T("gcx1-b", 116, 272, 490, 202,
      "<span style='font-family:" + MONO + "'>space</span> ← <b>gc_horizon</b>（默认 64 MiB WAL）<br>"
      "&nbsp;&nbsp;= last_record_lsn − horizon<br>"
      "<span style='font-family:" + MONO + "'>time</span> ← <b>pitr_interval</b>（默认 7 天）<br>"
      "&nbsp;&nbsp;时间戳反查 LSN<br><br>"
      "<span style='font-family:" + MONO + "'>GcCutoffs::select_min() = min(space, time)</span><br>"
      "→ PITR 还没算出来时<b>什么都不能删</b><br><br>"
      "<b>gc_period</b> 默认 1 h；设为 0 或 gc_horizon=0 则关闭<br>"
      "以上均可 per-tenant override",
      fs=12.5, color=DIM, lh=1.6),
    R("gcx2-bg", 656, 222, 530, 262, fill=PANEL, stroke=EDGE, radius=12),
    T("gcx2-h", 676, 238, 490, 24, "子分支如何钉住祖先数据", fs=16, fw=800, color=AC2),
    T("gcx2-b", 676, 272, 490, 202,
      "祖先 timeline 的 <span style='font-family:" + MONO + "'>GcInfo.retain_lsns</span> 记录所有<br>"
      "子分支的分叉点：<span style='font-family:" + MONO + "'>Vec&lt;(Lsn, TimelineId, ..)&gt;</span><br>"
      "• 子 Timeline 构造时 <span style='font-family:" + MONO + "'>insert_child()</span> 登记<br>"
      "• 析构时 remove_child 摘除<br>"
      "• GC 取 <b>max_retain_lsn</b>，凡 layer 起始 LSN ≤ 它<br>"
      "&nbsp;&nbsp;一律保留（计入 layers_needed_by_branches）<br><br>"
      "<b>只锁分叉点之前</b>：起始 LSN &gt; max_retain_lsn 的层<br>"
      "&nbsp;&nbsp;仍按 cutoff 正常 GC，<b>不是整条历史都锁住</b><br>"
      "建分支时持 gc_cs 锁并校验 GC cutoff，防与 GC 竞态",
      fs=12.5, color=DIM, lh=1.6),
    R("gcx3-bg", 96, 492, 1088, 170, fill=PANEL, stroke=EDGE, radius=10),
    T("gcx3-h", 116, 504, 600, 20, "删除条件（五条全满足）· 与 S3 的关系 · 手工入口", fs=13, fw=800, color=AC),
    T("gcx3-b", 116, 530, 1048, 125,
      "<b>删一层要同时满足</b>：① 早于 space_cutoff　② 早于 time_cutoff(PITR)　③ 起始 LSN 高于所有子分支分叉点 max_retain_lsn<br>"
      "&nbsp;&nbsp;④ 不被有效 LSN lease 覆盖　⑤ 有更新的 image layer <b>完整覆盖</b>其 key 范围<br>"
      "<b>S3 侧不是立刻 DELETE</b>：schedule_gc_update 只把 layer 从 index_part.json <b>解链</b>，对象暂时悬挂，交给 scrubber 清理<br>"
      "&nbsp;&nbsp;（对比 delete_timeline 走 remote_client.delete_all()，是真删）<br>"
      "<b>手工入口</b>：PUT …/do_gc 立即触发 · DELETE …/timeline/&lt;id&gt; 删分支 · …/detach_ancestor 脱离祖先 · gc_blocking 暂停 GC",
      fs=12, color=DIM, lh=1.65),
], p, notes="GC 两条 cutoff 取 min：space 来自 gc_horizon(默认64MiB WAL)，time 来自 pitr_interval(默认7天)；PITR 未算出时不能删任何东西。gc_period 默认 1h。子分支通过祖先的 GcInfo.retain_lsns 钉住历史：GC 取 max_retain_lsn，只有起始 LSN 小于等于分叉点的 layer 才保留；起始 LSN 高于 max_retain_lsn 的层仍按 cutoff 正常回收，不是整条历史永久保留。删一层需五条件全满足，包括必须有更新的 image layer 完整覆盖其 key 范围。S3 侧 GC 只从 index_part.json 解链不立即删对象，留给 scrubber；delete_timeline 才是真删。")

# ─────── Slide 15: Sharding & Generation ───────
p += 1
std("s-shard", "PAGESERVER", "Sharding & Generation Number", [
    T("sh-desc", 96, 172, 1088, 60,
      "<b>Sharding</b>：让单 tenant 突破单机磁盘上限（目标 16 TiB）。<br>"
      "<b>Generation Number</b>：无需 STONITH 的 split-brain 防护。",
      fs=15, color=DIM, lh=1.7),
    # Sharding side
    R("sh1-bg", 96, 250, 528, 340, fill=PANEL, stroke=EDGE, radius=12),
    T("sh1-h", 116, 268, 496, 26, "Key 维度 sharding（RFC 031/032）", fs=17, fw=800, color=AC),
    T("sh1-b", 116, 298, 496, 285,
      "<b>Key</b>（不含 TimelineId / segno，timeline 是独立维度）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>Key = (spcNode, dbNode, relNode, forkNum, blkNum)</span><br>"
      "<b>分片函数</b>（Rust 与 pgxn/neon C 两侧必须逐位一致）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>h = hash_combine(mm32(relNode), mm32(blkNum/stripe_size))</span><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>shard = h % shard_count</span><br>"
      "&nbsp;&nbsp;→ 是<b>哈希</b>不是除法取模；spcNode/dbNode/forkNum 不参与<br>"
      "非 rel-block key + initfork <b>固定落 shard 0</b>（basebackup 自足）<br>"
      "<b>stripe_size</b>（页数，8 KiB/页）：上游默认 2048 = 16 MiB；<br>"
      "&nbsp;&nbsp;Butterfly 建 tenant 传 <b>32768 = 256 MiB</b><br>"
      "notify-attach webhook → Compute 更新 neon.stripe_size 与<br>"
      "&nbsp;&nbsp;neon.pageserver_connstring（多 shard 连接串）<br>"
      "<b>LSN 维度 sharding 未实现</b>（RFC 031 明确 Non-Goal）",
      fs=12, color=DIM, lh=1.6),
    # Generation
    R("sh2-bg", 656, 250, 528, 340, fill=PANEL, stroke=EDGE, radius=12),
    T("sh2-h", 676, 268, 496, 26, "Generation Number（RFC 025）", fs=17, fw=800, color=AC2),
    T("sh2-b", 676, 306, 496, 260,
      "• Tenant 每次 attach 到某 PS，由 Storage Controller<br>"
      "&nbsp;&nbsp;分配<b>单调递增的 generation 号</b><br>"
      "• S3 对象名前缀带 generation：<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>tenants/&lt;id&gt;/&lt;gen&gt;/timelines/…</span><br>"
      "• 旧代次上传永远不会覆盖新代次<br>"
      "• PS 通过 /re-attach、/validate 上调 SC 校验<br><br>"
      "<b>效果</b>：无需 fencing/STONITH，即可安全支持迁移、",
      fs=13, color=DIM, lh=1.7),
    T("sh2-b2", 676, 550, 496, 30,
      "&nbsp;&nbsp;主备切换、Secondary Location",
      fs=13, color=DIM, lh=1.7),
], p, notes="Key = (spcNode, dbNode, relNode, forkNum, blkNum)，不含 TimelineId（timeline 是 tenant 内独立维度）。分片函数：hash_combine(murmurhash32(relNode), murmurhash32(blkNum/stripe_size)) % shard_count，注意是哈希不是简单除法。非 rel-block key（dbdir, slru 等）和 initfork 固定 shard 0，确保 shard 0 能独立出 basebackup。上游默认 stripe_size=2048(16MiB)，管控面传 32768(256MiB)。LSN 维度 sharding 未落地。Generation number 是无需 STONITH 的 split-brain 防护")

# ─────── Secondary Pageserver ───────
p += 1
std("s-secondary", "PAGESERVER", "Secondary Location：热备用的只读缓存", [
    T("secx-desc", 96, 170, 1088, 44,
      "Secondary <b>不服务读写、不摄入 WAL</b>，只靠 heatmap 驱动下载，维持一份温缓存。"
      "<span style='font-family:" + MONO + "'>pageserver/src/tenant/secondary.rs</span>",
      fs=14, color=DIM, lh=1.5),
    R("sec1-bg", 96, 222, 530, 252, fill=PANEL, stroke=EDGE, radius=12),
    T("sec1-h", 116, 238, 490, 24, "Heatmap：告诉 Secondary 下载什么", fs=16, fw=800, color=AC),
    T("sec1-b", 116, 272, 490, 190,
      "Attached 侧周期性上传 heatmap（JSON）：<br>"
      "&nbsp;&nbsp;HeatMapTenant{ generation, timelines[..] }<br>"
      "&nbsp;&nbsp;每层带 access_time + <b>cold</b> 标记<br>"
      "Secondary 只拉 <span style='font-family:" + MONO + "'>hot_layers()</span>，跳过 cold 层<br><br>"
      "上传/下载周期：<br>"
      "&nbsp;&nbsp;heatmap_period 默认 <b>60s</b>（有 secondary 才设）<br>"
      "&nbsp;&nbsp;下载默认间隔同样 60s，按 5% jitter 打散",
      fs=12.5, color=DIM, lh=1.6),
    R("sec2-bg", 656, 222, 530, 252, fill=PANEL, stroke=EDGE, radius=12),
    T("sec2-h", 676, 238, 490, 24, "调度 & 故障切换时的预热", fs=16, fw=800, color=AC2),
    T("sec2-b", 676, 272, 490, 190,
      "Storage Controller 调度（tenant_shard.rs）：<br>"
      "&nbsp;&nbsp;PlacementPolicy::Attached(n) → 1 主 + n 个 Secondary<br>"
      "&nbsp;&nbsp;描述接口 node_secondary 字段即取自此 intent<br><br>"
      "<b>迁移前预热</b>：Reconciler 迁移目的地若是 Secondary，<br>"
      "&nbsp;&nbsp;先调 tenant_secondary_download 拉满层再切<br>"
      "&nbsp;&nbsp;→ 提升后直接读本地盘，<b>避免冷启动 S3 回源</b><br>"
      "drain 迁移还会比对 secondary_lag（落后字节数）",
      fs=12.5, color=DIM, lh=1.6),
    R("sec3-bg", 96, 492, 1088, 90, fill=PANEL, stroke=EDGE, radius=10),
    T("sec3-b", 116, 508, 1048, 62,
      "目录结构与 Attached 模式<b>完全相同</b>，晋升时不搬文件、原地转正；"
      "Secondary 层文件同样纳入磁盘用量驱逐（disk-usage eviction）。<br>"
      "定位：warm standby，用<b>本地磁盘 layer 缓存</b>换故障切换/迁移时的低延迟，代价是不做实时数据同步（仍以 S3 index 为准）。",
      fs=12, color=DIM, lh=1.6),
], p, notes="Secondary 不服务客户端、不摄入 WAL，只维持温缓存。Attached 侧上传 heatmap(默认60s周期)标记每层access_time和cold位，Secondary只拉hot_layers跳过cold层。SC按PlacementPolicy::Attached(n)调度1主n从，node_secondary字段来自调度intent。迁移前Reconciler会调用tenant_secondary_download预热目的地，之后可以直接读本地盘避免冷启动S3回源；drain时还会比对secondary_lag。目录结构与attached完全相同，晋升不搬文件。")

# ─────── Slide 18: Broker & Controller ───────

p += 1
std("s-splitbrain", "协调层", "如何防止 Compute / Pageserver 脑裂", [
    T("sb-desc", 96, 168, 1088, 36,
      "网络分区、VM 挂起、软件 bug 都可能让「一个身份」同时活两个进程。Neon 不 STONITH，而用 <b>单调递增编号</b> 让老进程<b>写不进也覆盖不了</b>。",
      fs=14, color=DIM, lh=1.5),
    # Left panel: Compute / Safekeeper (term)
    R("sb1-bg", 96, 216, 540, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("sb1-n", 116, 228, 200, 18, "COMPUTE ↔ SAFEKEEPER", fs=11, fw=800, color=AC, ff=MONO),
    T("sb1-h", 116, 250, 500, 22, "term：Paxos-like 单调轮次号", fs=15, fw=800, color=AC),
    T("sb1-b", 116, 278, 500, 230,
      "<b>场景</b>：老 compute 被认为挂了 → 拉起新 compute，但老 compute 又活过来<br><br>"
      "<b>机制</b>：SK 侧持久化 <span style='font-family:" + MONO + "'>acceptor_state.term</span><br>"
      "&nbsp;&nbsp;walproposer 启动先发 VoteRequest → 多数派 SK ACK 后<br>"
      "&nbsp;&nbsp;term 单调递增（<span style='font-family:" + MONO + "'>safekeeper.rs:1078</span> 持久化到磁盘）<br><br>"
      "<b>老 compute 的下场</b><br>"
      "&nbsp;&nbsp;发 AppendRequest 携带旧 term → SK 见 <span style='font-family:" + MONO + "'>term &gt; msg.term</span><br>"
      "&nbsp;&nbsp;→ 回 <b>term-only</b> 响应（<span style='font-family:" + MONO + "'>safekeeper.rs:1316</span>）<br>"
      "&nbsp;&nbsp;→ walproposer 感知后<b>整个重新选举，不能续写</b><br><br>"
      "任一 SK term 提升即触发全局 term 升级；<br>"
      "generation 不匹配也会 <span style='font-family:" + MONO + "'>bail!</span> 直接拒绝（storcon 变更配置）",
      fs=11.5, color=DIM, lh=1.7),
    # Right panel: Pageserver (generation number)
    R("sb2-bg", 656, 216, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("sb2-n", 676, 228, 200, 18, "PAGESERVER ↔ S3", fs=11, fw=800, color=AC2, ff=MONO),
    T("sb2-h", 676, 250, 500, 22, "generation number：S3 key 后缀", fs=15, fw=800, color=AC2),
    T("sb2-b", 676, 278, 500, 230,
      "<b>场景</b>：PS 无响应 → 迁移 tenant 到 PS-B；但 PS-A 又活过来写 S3<br><br>"
      "<b>机制</b>：Storage Controller 是 generation 的<b>唯一颁发者</b><br>"
      "&nbsp;&nbsp;每次 attach / 重启 <span style='font-family:" + MONO + "'>/re-attach</span> → generation +1<br>"
      "&nbsp;&nbsp;所有 layer / index S3 key 带 <b>hex 后缀</b>（8 字节 u32）<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>xxx.__.gen-000000A3</span><br><br>"
      "<b>老 PS 的下场</b><br>"
      "&nbsp;&nbsp;仍能上传，但 key 里带旧 generation → <b>永不冲突</b><br>"
      "&nbsp;&nbsp;index_part.json 版本号最高者胜（新 PS 加载最新）<br>"
      "&nbsp;&nbsp;<b>DELETE 前必须先 <span style='font-family:" + MONO + "'>/upcall/v1/validate</span></b><br>"
      "&nbsp;&nbsp;storcon 核验 generation 仍最新才允许物理删除<br><br>"
      "→ 老 PS 覆盖不了、删不掉，最坏留些垃圾 S3 对象，靠 tombstone/GC 清",
      fs=11.5, color=DIM, lh=1.7),
    # Bottom band: design principles
    R("sb3-bg", 96, 530, 1088, 132, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("sb3-h", 116, 542, 600, 20, "共同的设计取舍", fs=13, fw=800, color=AC),
    T("sb3-b", 116, 568, 1048, 88,
      "• <b>不依赖 STONITH</b>：假设总能杀掉 EC2 实例不现实（VM 挂起、宿主机 hung） → 用<b>编号防御性写入</b>代替强制杀进程<br>"
      "• <b>控制面单点颁发编号</b>：storcon 用一个内建 Postgres 强一致存 generation；SK 用 Paxos 自己维护 term —— <b>都不在存储节点上跑共识</b><br>"
      "• <b>正确 &gt; 可用</b>：允许老进程继续跑一会，但保证它<b>写入的对象和新进程隔离</b>；数据完整性优于短暂多写<br>"
      "• storcon <b>自己脑裂</b>（RFC 037）：靠 K8s Lease + 启动读取 leader → 有限期共存，随后自动收敛",
      fs=12, color=DIM, lh=1.7),
], p, notes="双条防线 —— Compute/SK 侧用 term（Paxos），PS/S3 侧用 generation number（storcon 颁发的单调计数器）。Compute 脑裂：SK 持久化 acceptor_state.term，老 walproposer 用旧 term 发 AppendRequest 被 SK 拒绝返回 term_only 触发重新选举，见 safekeeper/src/safekeeper.rs:1316 handle_append_request。Generation 不匹配也直接 bail! 拒绝（storcon 变更 mconf）。PS 脑裂：所有 S3 key 带 generation 后缀（8字节hex u32），迁移或重启 storcon /re-attach 会递增 generation，老 PS 仍可上传但 key 隔离永不冲突。DELETE 必须先经 /upcall/v1/validate 让 storcon 核验 generation 仍最新，见 pageserver/src/deletion_queue/validator.rs 与 storage_controller/src/service.rs:2535。设计取舍：不依赖 STONITH、控制面单点颁发编号（storcon 用内建 Postgres，SK 用 Paxos）、正确优先于可用、storcon 自己脑裂靠 K8s Lease + RFC 037。参考：RFC 025-generation-numbers.md、RFC 028-pageserver-migration.md、RFC 037-storage-controller-restarts.md。")


p += 1
divider("s-div5", 6, "标志性能力实现", p)
# ─────── Slide 19: Branching intro (morph target) ───────
p += 1
std("s-branch1", "BRANCHING", "Copy-on-Write 分支 —— Neon 的杀手锏", [
    T("br-big", 96, 210, 700, 120, "&lt; 100 ms", fs=110, fw=900, color=AC, lh=1,
      fx={"countUp": False}),
    T("br-bigl", 100, 340, 700, 40, "创建一个分支所需时间", fs=22, fw=600, color=DIM),
    *card("br-why", 96, 410, 1088, 150,
          "为什么这么快？", [
              "创建 branch = <b>只写一行元数据</b>：(new_timeline_id, ancestor_timeline_id, ancestor_lsn)",
              "<b>不复制任何 layer 文件</b>。父分支的所有 layer 被子分支隐式共享。",
              "读：子分支 miss → 递归到 ancestor 找　|　写：新 WAL 只写子分支目录，父分支不受影响。",
          ], hc=AC2, fs=15, headfs=18),
], p, notes="Branch = 只写一行元数据，不复制 layer 文件，秒级完成")

# ─────── Slide 20: Branching detail (morph from 19) ───────
p += 1
std("s-branch2", "BRANCHING", "CoW 分支 vs 传统快照", [
    # keep morph headline el
    T("br-big", 96, 172, 400, 60, "CoW vs 快照", fs=34, fw=800, color=AC, lh=1.1),
    # comparison table
    R("brt-bg", 96, 240, 1088, 300, fill=PANEL, stroke=EDGE, radius=12),
    # header
    T("brt-h0", 130, 258, 300, 26, "维度", fs=14, fw=800, color=FG),
    T("brt-h1", 470, 258, 340, 26, "传统 PG 复制 / 快照", fs=14, fw=800, color=AC2),
    T("brt-h2", 830, 258, 340, 26, "Neon Branch", fs=14, fw=800, color=AC),
    R("brt-hdiv", 130, 292, 1024, 1, fill="rgba(255,255,255,0.12)", stroke="none", sw=0, radius=0),
    *[e for i, (d, a, b) in enumerate([
        ("拷贝数据？", "是（GB → TB 级）", "否，仅元数据"),
        ("建立时间", "分钟 ~ 小时", "秒级（&lt; 100 ms）"),
        ("从历史 LSN 建", "需 PITR 完整回放", "直接指定 ancestor_lsn"),
        ("物理开销", "复制后独立占用", "0，直到 diverge 才增长"),
        ("逻辑大小归属", "复制后独立计", "父/子都是完整逻辑大小"),
    ]) for e in (
        T(f"brt-d{i}", 130, 312 + i * 44, 320, 24, d, fs=14, fw=600, color=DIM),
        T(f"brt-a{i}", 470, 312 + i * 44, 340, 24, a, fs=14, fw=500, color=FAINT),
        T(f"brt-b{i}", 830, 312 + i * 44, 340, 24, b, fs=14, fw=500, color=FG),
    )],
    T("br-note", 96, 556, 1088, 40,
      "GC 删 layer 时需考虑所有 child 的 ancestor_lsn + pitr_interval(7天) + gc_horizon(64MB) 的并集。",
      fs=13, color=FAINT, lh=1.5),
], p, morph=True, notes="CoW 分支对比传统快照：不拷贝数据、秒级、可从历史 LSN 建")

# ─────── Slide 21: Synthetic Size ───────
p += 1
std("s-synsize", "BRANCHING", "Synthetic Size：与物理布局解耦的计费", [
    T("ss-desc", 96, 180, 1088, 90,
      "因为物理大小依赖 CoW 共享 + compaction 时机，<b>用物理字节计费对用户不公平也不可预测</b>。<br>"
      "Neon 定义 <b>Synthetic Size</b>：只从逻辑大小 + WAL 保留量推算，与底层实现完全解耦。",
      fs=16, color=DIM, lh=1.8),
    *card("ss1", 96, 300, 528, 220,
          "Synthetic Size 的价值", [
              "• 计费独立于存储实现细节",
              "• 改进物理层（更好的 compaction）",
              "&nbsp;&nbsp;只降低 Neon 自己的 COGS",
              "&nbsp;&nbsp;<b>不改变用户账单</b>",
              "• 分支共享的数据不重复计费",
              "• 可预测：用户能自己估算",
          ], fs=14, headfs=17),
    *card("ss2", 656, 300, 528, 220,
          "计算输入", [
              "• 各 timeline 的逻辑大小",
              "• 分支拓扑（共享祖先部分只计一次）",
              "• pitr_interval 窗口内保留的 WAL 量",
              "",
              "→ 一个确定性函数，不依赖 layer 文件的",
              "&nbsp;&nbsp;实际磁盘占用",
          ], hc=AC2, fs=14, headfs=17),
], p, notes="Synthetic size 从逻辑大小+WAL 量推算，与物理布局解耦，保证计费可预测")


# ─────── 分支 Schema Diff ───────
p += 1
std("s-schema-diff", "BRANCHING", "分支 Schema Diff：Butterfly 的实现（Neon 上游未实现）", [
    T("sd-desc", 96, 168, 1088, 40,
      "Neon 上游<b>没有</b> schema/branch diff 功能，只提供 <span style='font-family:" + MONO + "'>pg_dump --schema-only</span> 原语；"
      "Butterfly 在其之上封装了「与父分支对比」的能力。",
      fs=14, color=DIM, lh=1.5),
    # left: Neon primitive
    R("sd1-bg", 96, 216, 540, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("sd1-n", 116, 228, 200, 18, "NEON UPSTREAM", fs=11, fw=800, color=AC, ff=MONO),
    T("sd1-h", 116, 250, 500, 22, "只提供 pg_dump 原语，没有 diff", fs=15, fw=800, color=AC),
    T("sd1-b", 116, 278, 500, 230,
      "<b>可用的构件</b>：每台 compute 都暴露<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>GET /database_schema?database=&lt;db&gt;</span><br>"
      "&nbsp;&nbsp;→ compute_ctl 内部 shell 出 <span style='font-family:" + MONO + "'>pg_dump --schema-only</span><br>"
      "&nbsp;&nbsp;→ 把 DDL 文本流式返回<br><br>"
      "<b>代码位置</b><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>compute_tools/src/catalog.rs:57</span> get_database_schema<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>http/routes/database_schema.rs:25</span> HTTP handler<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>compute_tools/src/http/openapi_spec.yaml:176</span><br><br>"
      "<b>关于 diff 的历史提及</b>：仅 <span style='font-family:" + MONO + "'>docs/rfcs/003-laptop-cli.md:232</span><br>"
      "&nbsp;&nbsp;2022 年 CLI 设计草案里一句 <b>neon snapshot diff</b><br>"
      "&nbsp;&nbsp;针对本地 snapshot，非分支，<b>从未落地</b>",
      fs=11.5, color=DIM, lh=1.7),
    # right: Butterfly implementation
    R("sd2-bg", 656, 216, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("sd2-n", 676, 228, 200, 18, "BUTTERFLY", fs=11, fw=800, color=AC2, ff=MONO),
    T("sd2-h", 676, 250, 490, 22, "分支 ↔ 父分支对比（scope 受限）", fs=15, fw=800, color=AC2),
    T("sd2-b", 676, 278, 490, 230,
      "<b>API</b>　<span style='font-family:" + MONO + "'>GET /api/v2/branches/:id/schema-diff</span><br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>?database=&lt;db&gt;</span>　只接 database，<b>无第二 branch 参数</b><br>"
      "&nbsp;&nbsp;仅比对<b>直接父分支</b>；root 分支返回 BadParam<br><br>"
      "<b>核心流程</b>　<span style='font-family:" + MONO + "'>lib_branch_schema.py</span><br>"
      "&nbsp;&nbsp;① find_active_pod × 2（父/子各自定位）<br>"
      "&nbsp;&nbsp;② ThreadPoolExecutor <b>并发</b> fetch_schema<br>"
      "&nbsp;&nbsp;&nbsp;&nbsp;→ 各调各 pod 的 <span style='font-family:" + MONO + "'>/database_schema</span><br>"
      "&nbsp;&nbsp;③ clean_schema 剔除 pg_dump timestamp/version 头<br>"
      "&nbsp;&nbsp;④ Python <span style='font-family:" + MONO + "'>difflib.unified_diff</span> 出报告<br><br>"
      "<b>返回</b>　unified-diff 文本 + <span style='font-family:" + MONO + "'>lines_added</span> /<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>lines_removed</span> / <span style='font-family:" + MONO + "'>has_changes</span>",
      fs=11.5, color=DIM, lh=1.7),
    # bottom band
    R("sd3-bg", 96, 530, 1088, 132, fill="rgba(255,158,138,0.06)", stroke="rgba(255,158,138,0.3)", radius=10),
    T("sd3-h", 116, 542, 900, 20, "为什么只对比父分支 & Neon 为什么没做", fs=13, fw=800, color=AC2),
    T("sd3-b", 116, 568, 1048, 88,
      "• <b>父子对齐 CoW 语义</b>：子分支继承父分支所有 layer，diff = 「从 ancestor_lsn 之后子分支上做了哪些 DDL」，与 branching 模型天然对齐<br>"
      "• <b>任意分支对比</b>需要显式路径找 LCA、可能跨 project／跨 shard，控制面复杂度高；先满足 90% 场景（review 一次变更）<br>"
      "• Neon 上游只关心「让 compute 能被 dump」；<b>UI/diff 是控制面职责</b>，故只提供原语不做上层功能 ── 与 Butterfly 分工合理<br>"
      "• 前端：<span style='font-family:" + MONO + "'>branch-schema-diff.json</span> 直接调该 API；几乎每个分支页面都挂 「Schema Diff」 tab",
      fs=12, color=DIM, lh=1.7),
], p, notes="分支 Schema Diff：Neon 上游没有实现（grep .rs/.py/.md/.go 关于 schema_diff/branch diff 全无命中，只在 docs/rfcs/003-laptop-cli.md:232 有 2022 年一句 CLI 草案 neon snapshot diff 从未实现）。Neon 只提供构件：GET /database_schema?database=<db> 每个 compute 上暴露，compute_ctl 内部 shell 出 pg_dump --schema-only 流式返回 DDL，代码 compute_tools/src/catalog.rs:57 get_database_schema、http/routes/database_schema.rs:25、openapi_spec.yaml:176。Butterfly 在其上封装 GET /api/v2/branches/:branch_id/schema-diff?database=<db>，代码 handlers/branch/api_branch_schema_diff.py:32、lib_branch_schema.py。scope 只支持与直接父分支对比（api_branch_schema_diff.py:53 取 branch_b_obj.parent_branch_id；无父返回 BadParam）。流程：find_active_pod × 2 定位父子 pod → ThreadPoolExecutor 并发 fetch_schema 各调 compute_ctl HTTP /database_schema → clean_schema 剔除 pg_dump timestamp/version 头减 diff 噪声 → difflib.unified_diff。返回 unified-diff 文本+ lines_added/lines_removed/has_changes。前端 branch-schema-diff.json 直接调，每个分支页都挂 Schema Diff tab。文档 static/docs/schema-diff.md、api/branches.md:486。设计取舍：父子对齐 CoW 语义、任意分支对比需 LCA 复杂度高、Neon 上游只做原语上层留给控制面。")


# ─────── Slide 22: Proxy ───────

p += 1
std("s-wake", "PROXY", "wake_compute：从「连接请求」到「一台活着的 Postgres」", [
    T("wk-desc", 96, 166, 1088, 38,
      "Proxy <b>每次连接前都会调一次</b> wake_compute（<span style='font-family:" + MONO + "'>connect_compute.rs:114</span>）；"
      "连接失败且错误可重试时<b>作废缓存再叫一次</b> —— 这就是「compute 已经被销毁、缓存过期」的自愈路径。",
      fs=13.5, color=DIM, lh=1.5),
    # left: proxy side
    R("wk1-bg", 96, 212, 540, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("wk1-n", 116, 224, 260, 18, "PROXY 侧（RUST）", fs=11, fw=800, color=AC, ff=MONO),
    T("wk1-h", 116, 246, 500, 22, "缓存优先 + 单飞 + 退避重试", fs=15, fw=800, color=AC),
    T("wk1-b", 116, 274, 500, 232,
      "① 先查 <b>node_info 缓存</b>（moka）<span style='font-family:" + MONO + "'>cache/node_info.rs:8</span><br>"
      "&nbsp;&nbsp;默认 <span style='font-family:" + MONO + "'>size=4000, idle_ttl=4m</span>（<b>空闲</b> TTL，非绝对）<br>"
      "&nbsp;&nbsp;命中即返回，标记 <span style='font-family:" + MONO + "'>ColdStartInfo::WarmCached</span><br>"
      "&nbsp;&nbsp;<b>失败也缓存</b>，但只 30s（或按 retry_info.retry_at）<br>"
      "② miss → 取 <b>per-endpoint 许可</b>（ApiLocks）再<b>二次查缓存</b><br>"
      "&nbsp;&nbsp;防惊群 dog-piling；另有 endpoint 级限流<br>"
      "③ 真正发 <span style='font-family:" + MONO + "'>GET /wake_compute?session_id=&amp;<br>"
      "&nbsp;&nbsp;application_name=&amp;endpointish=ep-xxx</span><br>"
      "&nbsp;&nbsp;头带 <span style='font-family:" + MONO + "'>Authorization: Bearer &lt;jwt&gt;</span> + X-Request-ID<br>"
      "④ 可重试错误 → <b>指数退避</b>重试<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>num_retries=8, base=100ms, exp=1.6</span> ≈ 总 7s<br>"
      "&nbsp;&nbsp;wake 成功后连 PG 另有一套：<span style='font-family:" + MONO + "'>5 次 / 200ms / ×2</span>",
      fs=11.5, color=DIM, lh=1.66),
    # right: butterfly side
    R("wk2-bg", 656, 212, 528, 300, fill=PANEL, stroke=EDGE, radius=12),
    T("wk2-n", 676, 224, 260, 18, "BUTTERFLY 侧（PYTHON）", fs=11, fw=800, color=AC2, ff=MONO),
    T("wk2-h", 676, 246, 490, 22, "分布式锁 + 温池取 pod + 等就绪", fs=15, fw=800, color=AC2),
    T("wk2-b", 676, 274, 490, 232,
      "① 解析 <span style='font-family:" + MONO + "'>endpointish</span> → endpoint_id + <b>pooled 标记</b><br>"
      "&nbsp;&nbsp;（<span style='font-family:" + MONO + "'>-pooler</span> 后缀＝走 PgBouncer）<br>"
      "② <b>Redis 分布式锁</b> <span style='font-family:" + MONO + "'>wake:{endpoint_id}</span>，TTL 30s<br>"
      "③ 锁内按需<b>补齐前置状态</b>：Project storage attach、<br>"
      "&nbsp;&nbsp;分支 unarchive；<span style='font-family:" + MONO + "'>RESTARTING/RESTORING</span> 直接回可重试 503<br>"
      "④ 绑定 compute：<b>复用现有健康 pod</b>，否则从<br>"
      "&nbsp;&nbsp;<b>温 pod 池</b>分配 —— <b>热路径上不创建 k8s pod</b><br>"
      "⑤ 新分配则<b>同步等就绪</b>：每 <b>0.5s</b> 轮询 status，<br>"
      "&nbsp;&nbsp;最多 <b>8s</b> 等到 RUNNING；超时回 503 +<br>"
      "&nbsp;&nbsp;<span style='font-family:" + MONO + "'>RETRY_POD_INIT_IN_PROGRESS, retry_delay_ms=1000</span><br>"
      "⑥ pooled 模式额外 sleep <b>1s</b> 让 PgBouncer<br>"
      "&nbsp;&nbsp;清掉 <span style='font-family:" + MONO + "'>server_login_retry</span> 陈旧缓存",
      fs=11.5, color=DIM, lh=1.66),
    # bottom: wire contract
    R("wk3-bg", 96, 526, 1088, 136, fill="rgba(0,229,153,0.06)", stroke="rgba(0,229,153,0.3)", radius=10),
    T("wk3-h", 116, 538, 900, 20, "线上协议（两侧字段严格对齐）", fs=13, fw=800, color=AC),
    T("wk3-b", 116, 564, 1048, 92,
      "<b>成功 200</b>　<span style='font-family:" + MONO + "'>{\"address\": \"10.244.1.23:5432\", \"server_name\": null, \"aux\": {endpoint_id, project_id, branch_id, compute_id, cold_start_info}}</span><br>"
      "&nbsp;&nbsp;Proxy 用 <span style='font-family:" + MONO + "'>address</span> 拆 host:port；<span style='font-family:" + MONO + "'>server_name</span> 有值则 <b>SslMode::Require</b>，null 则 Disable；<span style='font-family:" + MONO + "'>aux</span> 进 metrics<br>"
      "&nbsp;&nbsp;pooled 时 port 换成 <b>PgBouncer 端口</b>；Rust 侧结构体 <span style='font-family:" + MONO + "'>WakeCompute</span>（<span style='font-family:" + MONO + "'>control_plane/messages.rs:289</span>）<br>"
      "<b>失败</b>　<span style='font-family:" + MONO + "'>{error, status:{code, message, details:{user_facing_message, error_info.reason, retry_info.retry_delay_ms}}}</span><br>"
      "&nbsp;&nbsp;可重试 reason：<span style='font-family:" + MONO + "'>RUNNING_OPERATIONS / CONCURRENCY_LIMIT_REACHED / LOCK_ALREADY_TAKEN / ENDPOINT_IDLE / PROJECT_UNDER_MAINTENANCE</span>",
      fs=11.5, color=DIM, lh=1.7),
], p, notes="wake_compute 全链路。Proxy 侧：connect_compute.rs:114 每次连接前无条件调 wake_compute；连接失败且 err.should_retry_wake_compute() 为真且节点信息来自缓存，则 invalidate_cache 后再 wake（connect_compute.rs:135-154，retry.rs:64 大部分 IO 错误都算可重试，含义是 compute 可能已销毁缓存过期）。wake_compute 实现 cplane_proxy_v1.rs:409：先查 node_info 缓存（check_cache! 宏 416-435），moka Cache（cache/node_info.rs:8），默认 CACHE_DEFAULT_OPTIONS=size=4000,idle_ttl=4m（config.rs:119，--wake-compute-cache），命中标 ColdStartInfo::WarmCached（466）；错误也缓存但用 CplaneExpiry 默认 30s（cache/common.rs:13,92），若控制面返回 retry_info.retry_at 则用它。miss 后取 per-endpoint ApiLocks 许可（443-450）再二次查缓存防 dog-piling，还有 wake_compute_endpoint_rate_limiter 限流（452）。真正 HTTP 见 do_wake_compute（272-336）：GET .../wake_compute?session_id=&application_name=&endpointish=，头 Authorization Bearer jwt + X-Request-ID。重试 proxy/src/proxy/wake_compute.rs:31 循环 + retry_after 指数退避，配置 WAKE_COMPUTE_DEFAULT_VALUES=num_retries=8,base_retry_wait_duration=100ms,retry_wait_exponent_base=1.6 约 7s（config.rs:256）；wake 成功后连 PG 用 CONNECT_TO_COMPUTE_DEFAULT_VALUES=5次/200ms/×2（config.rs:252）。per-endpoint wake 并发锁默认 permits=0 即关闭（config.rs:308）。Butterfly 侧 handlers/proxy_callback/api_compute_wake.py:33 GET /wake_compute + @require_proxy_auth：compute_wake_impl（lib_compute_wake.py:704）解析 endpointish 为 endpoint_id+pooled；wake_endpoint_under_lock（612）校验后取 Redis 分布式锁 wake:{endpoint_id} TTL 30s（lib_endpoint_wake_lock.py:12）；_wake_under_lock（551）处理 Project storage attach、分支 unarchive、状态校验（RESTARTING/RESTORING 回可重试 503，只有 SUSPENDED/ACTIVE 继续）；_bind_endpoint_compute（491）复用健康 pod 或从温 pod 池 allocate_endpoint_compute 分配（热路径不创建 k8s pod）；新分配则 _wait_endpoint_compute_ready（176）每 WAKE_READY_POLL_INTERVAL_SECONDS=0.5s 轮询最多 WAKE_READY_TIMEOUT_SECONDS=8s 等 RUNNING，超时返回 503 + RETRY_POD_INIT_IN_PROGRESS + retry_delay_ms=1000；pooled 额外 _wait_pooler_settle sleep WAKE_POOLER_SETTLE_SECONDS=1.0s 清 PgBouncer server_login_retry 陈旧缓存。协议：成功 200 返回 {address, server_name, aux}（_build_wake_response lib_compute_wake.py:664），Proxy 侧 parse_host_port 拆 address，server_name 有值走 SslMode::Require 否则 Disable，aux 变 MetricsAuxInfo，Rust 结构体 WakeCompute（messages.rs:289）字段名严格对齐；pooled 时 port 用 DEFAULT_PGBOUNCER_PORT。失败返回 {error, status.code, status.message, status.details.user_facing_message/error_info.reason/retry_info.retry_delay_ms}（make_proxy_error lib_proxy_error.py:38），可重试 reason 有 RUNNING_OPERATIONS/CONCURRENCY_LIMIT_REACHED/LOCK_ALREADY_TAKEN/ENDPOINT_IDLE/PROJECT_UNDER_MAINTENANCE。")

# ─────── Slide 23: Scale-to-Zero ───────
p += 1
std("s-s2z", "核心卖点", "Scale-to-Zero：闲置即销毁", [
    T("s2z-big", 300, 200, 680, 120, "0", fs=200, fw=900, color=AC, lh=1, align="center",
      fx={"countUp": True}),
    T("s2z-l", 300, 340, 680, 40, "闲置时的资源消耗（计算层完全销毁）", fs=22, fw=600, color=DIM, align="center"),
    *card("s2z1", 96, 410, 528, 190,
          "如何实现？", [
              "• compute-monitor 跟踪最后活动时间",
              "• 超时 → control plane 销毁 pod",
              "• 数据安全：WAL 已在 SK 多数派持久化",
              "&nbsp;&nbsp;pages 在 Pageserver / S3",
              "• 唤醒：新连接 → proxy → control plane → 启动新 compute",
              "• 全流程 PGDATA 重建（basebackup + on-demand）",
          ], fs=14, headfs=16),
    *card("s2z2", 656, 410, 528, 190,
          "Prewarm 加速唤醒", [
              "• endpoint_storage：持久化 LFC 缓存快照",
              "• 唤醒后异步 prewarm 热页到 shared_buffers",
              "• 典型唤醒延迟：<b>数百 ms ~ 数秒</b>",
              "",
              "RFC 2025-03-17: compute-prewarm",
              "• cancellation 支持（不阻塞启动）",
          ], hc=AC2, fs=14, headfs=16),
], p, notes="Scale-to-Zero: 闲置销毁 compute pod，唤醒重建 PGDATA，Prewarm 加速")

# ─────── Slide 24: Autoscaling ───────
p += 1
std("s-auto", "核心卖点", "Autoscaling：CPU & Memory 弹性伸缩", [
    T("auto-desc", 96, 175, 1088, 50,
      "Neon 可以<b>秒级调整 Compute 的 CPU 和内存</b>，无需重启 Postgres。",
      fs=16, color=DIM, lh=1.6),
    *card("au1", 96, 240, 528, 280,
          "NeonVM + K8s", [
              "• NeonVM：基于 QEMU 的轻量虚拟化，K8s 管理",
              "• 支持 CPU 热插拔 + 内存热加/减",
              "• autoscaler-agent：集群级调度器",
              "• vm_monitor（compute 内部）：",
              "&nbsp;&nbsp;— 通过 axum WebSocket 双向通信",
              "&nbsp;&nbsp;— 管理 neon-postgres cgroup",
              "&nbsp;&nbsp;— memory.max / memory.high 动态调整",
              "&nbsp;&nbsp;— 联动 LFC file_cache_size_limit",
          ], fs=14, headfs=16),
    *card("au2", 656, 240, 528, 280,
          "弹性策略", [
              "• 根据 CPU 利用率 + 内存压力 + 连接数",
              "• 扩容：立即生效（无需重启）",
              "• 缩容：优雅释放，等事务完成",
              "• 最小→最大 CU 范围由用户配置",
              "",
              "与 Scale-to-Zero 互补：",
              "• 完全闲置 → Zero（销毁 VM）",
              "• 有负载 → 在 min~max 间自动伸缩",
              "• 峰值 → 自动扩到 max CU",
          ], hc=AC2, fs=14, headfs=16),
], p, notes="Autoscaling: NeonVM + autoscaler-agent + vm_monitor，CPU 热插拔 + 内存弹性，无需重启")

# ─────── Slide 25: 多云存储 ───────
p += 1
std("s-cloud", "存储底座", "多云对象存储支持", [
    T("cl-desc", 96, 175, 1088, 40,
      "Pageserver 的存储后端抽象为 Rust trait，支持插拔不同云提供商。",
      fs=16, color=DIM, lh=1.6),
    *card("cl1", 96, 240, 340, 200,
          "AWS S3", [
              "• 初始也是唯一实现",
              "• 生产验证最多",
              "• 支持所有功能",
              "• 兼容 S3 API 的对象存储",
          ], hc=AC, fs=14, headfs=16),
    *card("cl2", 470, 240, 340, 200,
          "Google GCS（新）", [
              "• commit 85ce109: 初版实现",
              "• commit 39e4f23: Range 请求支持",
              "• commit 6a35a3e: upload permit 死锁修复",
              "• Bytes Range 对按需下载至关重要",
          ], hc="#7CB3F4", fs=14, headfs=16),
    *card("cl3", 844, 240, 340, 200,
          "Azure Blob", [
              "• 较早支持",
              "• 仓库中已有完整 trait 实现",
              "• 适配 Azure 原生 API",
              "",
          ], hc=AC2, fs=14, headfs=16),
    *card("cl4", 96, 470, 1088, 90,
          "Direct IO 对齐（commit 26b47b5）", [
              "可配置对齐方式，优化不同存储硬件（NVMe 4KB / 传统 512B）的 I/O 性能。",
              "Pageserver 本地 layer 文件的读写走 Direct IO 路径。",
          ], hc=FAINT, fs=14, headfs=16),
], p, notes="多云存储：S3 / GCS / Azure Blob，Rust trait 抽象，可插拔。新增 GCS + Direct IO 对齐。")


p += 1
divider("s-div6", 7, "运维·限制·对比·落地", p)
# ─────── Slide 26: 关键数字汇总 chart ───────
p += 1
std("s-numbers", "数字", "关键参数一览", [
    R("num-bg", 96, 180, 1088, 450, fill=PANEL, stroke=EDGE, radius=14),
    *[e for i, (cat, items) in enumerate([
        ("Pageserver", [
            "checkpoint_distance = 256 MB",
            "compaction_period = 20s",
            "compaction_threshold = 10 (L0)",
            "compaction_target = 128 MB (L1)",
            "image_creation = ≥3 deltas",
            "page_cache = 64 MB 共享",
        ]),
        ("GC & 保留", [
            "pitr_interval = 7 天",
            "gc_horizon = 64 MB WAL",
            "gc_period = 1 小时",
            "熔断 = 5 次失败 → 禁 24h",
            "背压 write_lag = 500 MB",
            "背压 flush_lag = 10 GB",
        ]),
        ("Safekeeper", [
            "副本数 = 3，quorum = 2",
            "协议 = Paxos-like",
            "TLA+ 形式化验证 ✓",
            "动态成员变更 ✓",
            "",
            "",
        ]),
        ("Compute", [
            "状态 = 无状态",
            "Scale-to-Zero ✓",
            "Autoscaling = NeonVM 热调",
            "Bootstrap 模板 ✓",
            "Prewarm 恢复 ✓",
            "PG 14/15/16/17",
        ]),
    ]) for e in (
        T(f"num-h{i}", 130 + i * 260, 200, 240, 26, cat, fs=15, fw=800, color=[AC, AC2, "#7CB3F4", "#C89EFF"][i]),
        *[T(f"num-{i}-{j}", 130 + i * 260, 238 + j * 32, 240, 24, line, fs=12, fw=500, color=DIM, lh=1.3, ff=MONO)
          for j, line in enumerate(items)],
    )],
], p, notes="所有关键参数一览：Pageserver/GC/Safekeeper/Compute 四列")

# ─────── Metrics & 可观测 ───────
p += 1
std("s-metrics", "可观测", "关键指标：从背压到冷启动，看哪几个数就够", [
    *[e for i, (cat, hc, rows) in enumerate([
        ("背压 / 限流", AC2, [
            ("pageserver_tenant_throttling_wait_usecs_sum_global", "被限流累计等待微秒，按 kind（pagestream）"),
            ("pageserver_tenant_throttling_count_global", "限流次数；另有 accounted_start/finish 一对"),
            ("compute_backpressure_throttling_seconds_total", "compute 侧被 walproposer 限速的累计秒数"),
        ]),
        ("Layer / 读放大", "#7CB3F4", [
            ("pageserver_layer_count{level=frozen|L0|L1}", "各级 layer 数量（不含 open ephemeral）"),
            ("pageserver_layers_per_read", "服务单次读访问的 layer 数 = 读放大"),
            ("pageserver_storage_operations_seconds{op=compact}", "compact / create images / layer flush 耗时"),
        ]),
        ("WAL lag", "#C89EFF", [
            ("safekeeper_commit_lsn / flush_lsn / backup_lsn", "SK 三条水位线，两两相减就是各段 lag"),
            ("safekeeper_peer_horizon_lsn", "最落后 SK 的 LSN —— 单点掉队的第一信号"),
            ("pageserver_wait_lsn_seconds", "PS 等 WAL 到达的耗时（wait_lsn 完成时记）"),
        ]),
        ("GC / WALredo / 冷启动", AC, [
            ("pageserver_storage_operations_seconds{op=gc}", "GC 耗时；另有 op=find gc cutoffs"),
            ("pageserver_wal_redo_seconds + _records/_bytes_histogram", "redo 延迟 + 每次重放的记录数/字节数"),
            ("pageserver_basebackup_query_seconds", "冷启动关键路径，桶按 5ms~60s 专门设计"),
        ]),
    ]) for e in (
        R(f"mt-bg{i}", 96, 172 + i * 116, 1088, 106),
        T(f"mt-h{i}", 116, 182 + i * 116, 300, 22, cat, fs=14, fw=800, color=hc),
        *[x for j, (mn, desc) in enumerate(rows) for x in (
            T(f"mt-n{i}-{j}", 116, 210 + i * 116 + j * 22, 470, 20, mn, fs=11, fw=600, color=FG, ff=MONO, lh=1.3),
            T(f"mt-d{i}-{j}", 600, 210 + i * 116 + j * 22, 570, 20, desc, fs=11, fw=500, color=DIM, lh=1.3),
        )],
    )],
    T("mt-tail", 96, 640, 1088, 44,
      "此外：<span style='font-family:" + MONO + "'>proxy_compute_connection_latency_seconds</span>（带 cold_start_info 标签）看 Proxy 侧冷启动；"
      "<span style='font-family:" + MONO + "'>/metrics.json</span> 里 compute_ctl 的 <span style='font-family:" + MONO + "'>total_startup_ms</span> 把冷启动拆成 "
      "wait_for_spec / sync_safekeepers / pageserver_connect / basebackup / start_postgres / config 各段。",
      fs=11.5, color=FAINT, lh=1.6),
], p, notes="指标定义位置：背压 pageserver/src/metrics.rs:4289-4353（global 与 per-tenant 两套，标签 kind=pagestream）；compute 侧 backpressure_throttling_time() 在 pgxn/neon/neon.c:713，经 sql_exporter 暴露为 compute_backpressure_throttling_seconds_total。Layer：pageserver_layer_count metrics.rs:705-712、layers_per_read metrics.rs:136-170（含 batch/amortized 三个 global 变体）、storage_operations_seconds metrics.rs:88-128（operation 枚举 59-86 含 compact / create images / layer flush / layer flush delay / gc / find gc cutoffs）。WAL lag：safekeeper/src/metrics.rs:570-647 一整组 LSN gauge，peer_horizon_lsn 610-617 是最落后 SK；PS 侧 last_record_lsn 633-639、disk_consistent_lsn 642-648、wait_lsn_seconds 484-490、wait_lsn_in_progress_micros 504-518。WALredo：metrics.rs:2993-3035，含 wal_redo_seconds、records/bytes histogram、process_launch_duration。冷启动：basebackup_query_seconds metrics.rs:2259-2266 用专门的 COMPUTE_STARTUP_BUCKETS(2244-2251) 5ms~60s；proxy/src/metrics.rs:71-74 的 compute_connection_latency_seconds 标签组在 314-321 含 cold_start_info；compute_ctl 的 ComputeMetrics 结构在 libs/compute_api/src/responses.rs:244-284，不进 Prometheus，走 /metrics.json 给控制面。注意 Grafana dashboard JSON 不在本仓库。")

# ─────── 故障演练 ───────
p += 1
std("s-failure", "故障演练", "两个典型故障：SK 单点宕机 / PS 实例宕机", [
    *card("fl1", 96, 172, 528, 300,
          "① Safekeeper 3 副本挂 1", [
              "<b>写不受影响</b>：quorum = ⌊3/2⌋+1 = 2，剩 2 台照样成多数派",
              "&nbsp;&nbsp;commit_lsn = 第 k 名的 flush_lsn（walproposer.c:1994）",
              "<b>代价</b>：延迟下限变成「第二快 SK 的 fsync」，尾延迟可能升",
              "&nbsp;&nbsp;某台掉队触发背压（walproposer_pg.c:491-517）",
              "",
              "<b>恢复回来怎么追</b>：",
              "• 有活 compute → walproposer 重新握手投票，按",
              "&nbsp;&nbsp;find_highest_common_point 截断重写落后 SK 的 WAL",
              "• 无 compute 在流 → peer-to-peer：recovery.rs 每 2s",
              "&nbsp;&nbsp;选 (last_log_term, flush_lsn) 领先的 donor 用 pg 复制协议拉",
              "• 本地全丢 → pull_timeline 整表 tar 快照",
              "",
              "<b>数据风险</b>：已 commit 的在 ≥2 盘 → 0 丢失；",
              "&nbsp;&nbsp;未 commit 的尾巴可能被更高 term 的 proposer 覆盖（正常）",
          ], hc="#C89EFF", fs=12, headfs=15),
    *card("fl2", 656, 172, 528, 300,
          "② Pageserver 实例宕机", [
              "<b>PS 之间不跑共识</b>：靠 storage controller + generation number",
              "<b>检测</b>：心跳 5s 一次，漏 30s（max_offline_interval）判 Offline",
              "&nbsp;&nbsp;service.rs:129-143 / heartbeater.rs",
              "<b>重分配</b>：ToOffline → demote_attached → 重新调度到活 PS",
              "&nbsp;&nbsp;→ 入队 reconciler（service.rs:7988-8057）",
              "",
              "<b>读的影响</b>：",
              "• 有热 secondary（heatmap 预拉 + AttachedMulti 重叠）→ 切换近乎无感",
              "• 无 secondary → 新 PS 从 S3 拉 index_part.json，按需拉 layer，",
              "&nbsp;&nbsp;最近 WAL 从 SK 重新 ingest；读极新 LSN 会 wait_lsn 阻塞",
              "",
              "<b>从 S3 重建</b>：扫本地 config → /re-attach 拿新 generation →",
              "&nbsp;&nbsp;逐 tenant 从远端加载 timeline，重建 LayerMap，过 disk_consistent_lsn",
              "&nbsp;&nbsp;之后的 WAL 继续从 SK 追（mgr.rs / tenant.rs）",
          ], hc="#7CB3F4", fs=12, headfs=15),
    T("fl-tail", 96, 486, 1088, 130,
      "<b>共同底座：generation number 换掉了 fencing。</b> 每次 attach 由 controller 发单调递增 generation，写进 S3 对象 key 后缀；"
      "旧 PS 就算没死透、还在写，也因 generation 更小而被判 stale、只能降级 secondary（mgr.rs:626-635），不会脑裂覆盖。<br>"
      "<b>代价</b>：删除 / 推进 remote_consistent_lsn 都要向 controller 校验 generation —— 控制面挂了期间 S3 GC 停摆、SK 上 WAL 会堆积"
      "（RFC 025:718-724，留了手动「逃生」generation 兜底）。这换来的是<b>迁移 / 重启永不脑裂丢数据</b>。",
      fs=12.5, color=DIM, lh=1.7),
], p, notes="SK 单点：quorum=2，1 挂仍可写，commit_lsn=GetAcknowledgedByQuorumWALPosition（walproposer.c:1994-2026），term-gated 提交（未追上 propTermStartLsn 的 SK 贡献按 0 算）。恢复两条路：walproposer 重选（safekeeper.rs:1052-1220 handle_vote/handle_elected + truncate_wal）或 peer recovery（recovery.rs:38-232，CHECK_INTERVAL_MS=2000，donor 须 term==last_log_term 且 term>=my.term，有活 compute 在流时强制不抢）；全丢用 pull_timeline.rs。WAL trim 到 min(remote_consistent_lsn, backup_lsn, commit_lsn, flush_lsn)（remove_wal.rs:5-33）。PS 宕机：controller 心跳 HEARTBEAT_INTERVAL=5s、MAX_OFFLINE_INTERVAL=30s（service.rs:129-143），heartbeater.rs:281/419 判 offline，ToOffline handler service.rs:7988-8057 clear observed location + demote_attached（tenant_shard.rs:337）+ schedule（:701）+ 入队 reconciler（并发默认 128）。单节点集群 / 全挂时跳过重调度。读失败窗口：有 warm secondary 近乎无缝（RFC 028:63-70/104-176），无则新 PS 下 index_part.json 再懒拉 layer，wait_lsn 阻塞到 wait_lsn_timeout（timeline.rs:1782-1836）。compute 侧经 notify-attach 改写 neon.pageserver_connstring 并 SIGHUP（libpagestore.c:130,266-350）。重建三步：扫本地 config（mgr.rs:392-417）→ /re-attach 拿 generation（mgr.rs:340-386，缺席 tenant 本地内容删）→ attach 逐 timeline 从远端加载（tenant.rs:1690-1829，download_index_part，缺层按需拉）。stale PS 校验 generation 前不 upload/delete（RFC 025:826-887），generation 变小即降 secondary（mgr.rs:626-635）。")

# ─────── 局限 & tradeoff ───────
p += 1
std("s-tradeoff", "局限", "架构局限 & Tradeoff：清醒地知道边界在哪", [
    *card("to1", 96, 172, 528, 214,
          "写入侧", [
              "<b>单写者</b>：每 (tenant, timeline) 同一时刻只能一个 primary",
              "&nbsp;&nbsp;写（multitenancy.md:57，共识 + epoch 主动防双写）",
              "读副本只做<b>物理复制</b>只读，共享同一份 PS 存储（RFC 036）",
              "",
              "<b>每次读页都是一次到 PS 的 RPC</b>：compute 无本地持久页缓存",
              "&nbsp;&nbsp;网络抖动直接进读路径；靠 LFC 缓解但不消除",
              "读极新 LSN 会 wait_lsn 阻塞等 WAL 到达",
          ], hc=AC2, fs=12.5, headfs=15),
    *card("to2", 656, 172, 528, 214,
          "存储侧", [
              "<b>写放大</b>：老 compaction 放大 ∝ 逻辑库大小（最坏近平方）",
              "&nbsp;&nbsp;bottom-most gc-compaction 才把它压到常数级 1.5~2×（RFC 043）",
              "单 PS 本地占用可达逻辑库<b>数倍</b>（LSM 膨胀，RFC 031）",
              "",
              "<b>Sharding 静态</b>：建 tenant 时定死，只能事后 split（RFC 031/032）",
              "S3 无廉价 mv：需要 rename 的操作都被放大成拷贝（RFC 022:33）",
              "无跨 branch / 跨 timeline join —— 存储严格按 timeline 切分",
          ], hc="#7CB3F4", fs=12.5, headfs=15),
    *card("to3", 96, 400, 1088, 216,
          "控制面 & 一致性 —— generation number 方案的代价（RFC 025）", [
              "• <b>强依赖控制面可达</b>：PS 重启后要拿到新 generation 才恢复服务 —— 以前控制面挂了也能服务，现在不行（:701-717）",
              "• <b>控制面挂 → S3 GC 停摆</b>：删除要 generation 校验，安全但持续烧钱（:718-720）",
              "• <b>控制面挂 → SK 磁盘可能涨满</b>：推进 remote_consistent_lsn 也要校验，长时间中断 WAL 堆积（:721-724，留手动逃生 generation）",
              "• <b>迁移期多 attach</b>：新 attachment 可见 LSN 可能「倒退」到旧 attach 尚未 flush 的点（:220-231）",
              "• storage controller 本身：部分网络隔离可能引发可用性事故（RFC 2025-02-14:33,52）；direct I/O 放弃了内核 page cache 收益（RFC 2025-04-30）",
              "",
              "<b>本质取舍</b>：Neon 复用控制面已有的强一致 DB 当「唯一真相源」，<b>不再自建一套存储层共识</b>（Design Tenet, RFC 025:59-69）——",
              "换来迁移/重启永不脑裂，代价是把可用性绑在控制面上。这是一个清醒的、写进设计文档的选择，不是疏漏。",
          ], hc="#FFD54A", fs=12.5, headfs=15),
], p, notes="局限全部有据。单写者：docs/multitenancy.md:57-59、walservice.md:110-115、RFC 004:15,143；读副本物理复制 RFC 036。每读一 RPC + wait_lsn：timeline.rs:1782-1885、walservice.md:92-105。写放大：RFC 043:9,108-142（bottom-most gc-compaction 目标常数写放大，例子 1.5~2×）、RFC 038:26（aux v2 固定写放大）、RFC 031:12-21（单 PS 本地占用数倍逻辑库）、031:395-408（layer-spreading 被否因需单节点扛全部写和 compaction）。S3 无 mv：RFC 022:33。静态 sharding：RFC 031/032。跨 branch 无 join：timeline 严格 per-tenant，RFC 021:26、035:454-462。控制面 tradeoff 全部 RFC 025：:701-717 依赖控制面才恢复、:718-720 GC 停摆、:721-724 SK 涨满 + 手动逃生 generation、:220-231 迁移期 LSN 倒退、:636-696 对象泄漏靠 scrubber 清、:551-573 同 node ID 复用 VM 的竞态（当前 EC2 ephemeral disk 部署安全）。Design Tenet「已有强一致控制面 DB，避免再造共识」RFC 025:59-69。storage controller 可用性 RFC 2025-02-14:33,52；direct IO 取舍 RFC 2025-04-30:142-148。gc-compaction 失败不重试 RFC 043:163-179。")

# ─────── Slide 27: 近期开发方向 ───────
p += 1
std("s-dev", "开发方向", "近期 Git 历史脉络（本 Fork）", [
    *card("dv1", 96, 175, 528, 170,
          "① Compute Bootstrap Template (4 commits)", [
              "6a0b80a → 首版：模板目录 + 幂等表",
              "919a00c → 脚本级续跑 + 移到 ext 后",
              "7406531 → 错误信息记录到表",
              "db853f1 → 事务泄漏修复（SAVEPOINT 探测）",
          ], hc=AC, fs=14, headfs=16),
    *card("dv2", 656, 175, 528, 170,
          "② 多云存储扩展", [
              "85ce109 → GCS 初版实现",
              "39e4f23 → GCS Range 请求",
              "6a35a3e → GCS upload 死锁修复",
              "26b47b5 → Direct IO 对齐配置",
          ], hc="#7CB3F4", fs=14, headfs=16),
    *card("dv3", 96, 375, 528, 170,
          "③ Storage 生命周期 & 运维", [
              "SK 动态成员变更（last_log_term）",
              "Storage Controller: safekeeper_migrate_abort",
              "PS 检测数据损坏 → 反馈到 SK 和 PG",
              "Deletion API 改进 RFC",
          ], hc=AC2, fs=14, headfs=16),
    *card("dv4", 656, 375, 528, 170,
          "④ Compute Prewarm & Proxy", [
              "prewarm timespans / cancellation",
              "spec apply 精细化",
              "Proxy REST broker + JWT + CORS",
              "ConnectError 分类精细化",
          ], hc="#C89EFF", fs=14, headfs=16),
], p, notes="近期 4 条开发主线：Bootstrap Template / 多云存储 / 运维闭环 / Compute Prewarm + Proxy 演进")

# ─────── Slide 28: 源码入口 ───────
p += 1
std("s-src", "源码", "想深挖？从这里开始", [
    T("src-list", 96, 180, 1088, 440,
      "<b>Pageserver：</b><br>"
      "　pageserver/src/tenant.rs, page_service.rs, walingest.rs, walredo.rs<br><br>"
      "<b>Safekeeper：</b><br>"
      "　safekeeper/src/safekeeper.rs, receive_wal.rs, send_wal.rs, recovery.rs<br><br>"
      "<b>Storage Controller：</b><br>"
      "　storage_controller/src/service.rs, reconciler.rs, scheduler.rs<br><br>"
      "<b>Compute：</b><br>"
      "　compute_tools/src/compute.rs, spec_apply.rs, bin/compute_ctl.rs<br><br>"
      "<b>PG 扩展：</b><br>"
      "　pgxn/neon/ （smgr hook + walproposer）<br><br>"
      "<b>Proxy：</b><br>"
      "　proxy/src/serverless/, proxy/, auth/<br><br>"
      "<b>RFC 合集：</b><br>"
      "　docs/rfcs/ （60+ 篇 RFC，最权威的设计文档）",
      fs=15, color=DIM, lh=1.5, ff=MONO),
], p, notes="核心源码入口：pageserver/safekeeper/controller/compute/pgxn/proxy, 以及 60+ RFC")

# ─────── Slide 29: 总结 ───────
p += 1
std("s-sum", "总结", "Neon 的核心设计哲学", [
    T("sum-b", 96, 190, 1088, 350,
      "① <b>存储计算彻底分离</b>：Compute 无状态、可销毁，存储在 Pageserver + S3<br><br>"
      "② <b>WAL 独立持久化</b>：Safekeeper Paxos 多数派 fsync，commit 不等存储和 S3<br><br>"
      "③ <b>不可变 Layer 文件</b>：所有数据写为 append-only 的 layer → S3，无覆盖<br><br>"
      "④ <b>Copy-on-Write 分支</b>：只写元数据，读时递归到 ancestor，零拷贝<br><br>"
      "⑤ <b>Generation Number</b>：无需 fencing 即可安全迁移，split-brain 不丢数据<br><br>"
      "⑥ <b>Scale-to-Zero + Autoscaling</b>：全弹性，按需付费<br><br>"
      "⑦ <b>Postgres 兼容</b>：基于 patch 后的官方 PG14/15/16/17，100% SQL 兼容",
      fs=16, color=DIM, lh=1.55),
], p, notes="七大设计哲学总结：存储计算分离 / WAL 独立 / 不可变层 / CoW 分支 / Generation / 弹性 / PG 兼容")

# ─────── Slide 30: Back cover ───────
p += 1
base("s-end", [
    R("end-bg", 0, 0, W, H, fill="rgba(0,229,153,0.04)", stroke="none", sw=0, radius=0),
    T("end-title", 96, 260, 1088, 120,
      "Thank You",
      fs=96, fw=900, color=FG, lh=1,
      fx={"enter": "fade-up", "order": 0}),
    T("end-sub", 96, 390, 1088, 40,
      "https://github.com/neondatabase/neon",
      fs=20, fw=500, color=AC, ff=MONO, lh=1,
      fx={"enter": "fade-up", "order": 1}),
    T("end-tags", 96, 450, 1088, 30,
      "Serverless · Postgres · Open Source",
      fs=16, fw=500, color=FAINT, ff=MONO, lh=1.4,
      fx={"enter": "fade-up", "order": 2}),
    R("end-bar", 96, 510, 60, 4, fill=AC2, stroke="none", sw=0, radius=2),
    footer(p),
], notes="Thanks slide — GitHub link")


# ═══════════════════════════ OUTPUT ═══════════════════════════

doc = {
    "format": "bento/slides",
    "version": 1,
    "title": "Neon — Serverless Postgres 架构全解析",
    "docId": "neon-arch-deck-2026",
    "size": {"width": W, "height": H},
    "theme": {
        "background": BG,
        "color": FG,
        "accent": AC,
        "fontFamily": SANS,
    },
    "meta": {
        "author": "meetbill",
        "company": "",
        "subject": "Neon Architecture Deep Dive",
        "event": ""
    },
    "slides": slides,
}

out = json.dumps(doc, ensure_ascii=False, indent=2)
# Escape < to prevent script tag injection
out = out.replace("<", "\\u003c")

with open("/tmp/neon_bento_deck.json", "w") as f:
    f.write(out)

print(f"Generated {len(slides)} slides, wrote to /tmp/neon_bento_deck.json")
print(f"JSON size: {len(out)} bytes")

