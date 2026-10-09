# Neon 架构 PPT (Bento Slides)

## 文件说明

| 文件 | 用途 |
|------|------|
| `gen_neon_bento.py` | Python 生成器脚本，定义所有 slide 内容和布局 |
| `Bento_Slides.bento.html` | 全量单文件 HTML 演示文稿（105 页），浏览器直接打开即可放映 |
| `Neon_A_概览与能力.bento.html` | 分册 A：背景痛点 + 顶层架构 + 核心数据流 + 标志性能力 |
| `Neon_B_组件与原理.bento.html` | 分册 B：组件逐层拆解 + 核心原理深度剖析 |
| `Neon_C_运维与落地.bento.html` | 分册 C：运维·限制·对比·落地 |

## 分册拆分说明

全量 deck 页数过多（105 页），`gen_neon_bento.py` 在生成全量 HTML 的同时，
按「受众」自动切出 3 本可独立放映的分册（单一数据源，复用同一批 slide）。
**每本内部再按主题切成若干子章节（section）**，各自生成分节页；
每本的子章节编号都从 **01** 本地重排、页脚也从 **1** 重新编号，三本互不干扰：

| 分册 | 子章节（01 起本地编号） | 适用场景 |
|------|------|----------|
| **A《概览与能力》** | 01 背景痛点 / 02 顶层架构总览 / 03 核心数据流 / 04 标志性能力实现 | 面向初识者、对外介绍，讲清楚「是什么 + 能做什么」 |
| **B《组件与原理》** | 01 接入层 Proxy & TLS / 02 Compute / 03 Safekeeper / 04 Pageserver / 05 协调层 / 06 核心原理深度剖析 | 面向研发深读，逐组件 + 原理级细节 |
| **C《运维·备份恢复·局限落地》** | 01 日志·可观测·故障演练 / 02 备份与恢复 / 03 局限·演进·总结 | 面向 SRE/落地，运维、备份恢复、局限 & tradeoff |

每本自带独立的 cover + 本册目录 + 结尾页。

### 拆分配置：脚本末尾的 `DECKS` 表

分册边界集中在 `DECKS` 一张表里，每本列出若干 `sections`，每个 section 的
`pick` 决定从 master 挑哪些内容页（都保持 master 原始顺序）。`pick` 三种形态：

| 形态 | 含义 | 维护成本 |
|------|------|----------|
| `{"chapter": N}` | 第 N 章全部内容页 | 全自动：新增 slide 落到该章就自动纳入 |
| `{"chapter": N, "kickers": [...]}` | 第 N 章中 kicker（左上角分类标签）命中集合的页 | 半自动：按组件/主题分流同一章 |
| `{"ids": [...]}` | 显式按 slide id 列举，顺序即列表顺序 | 编排型：精确控制顺序与归属 |

> B 册用 `kickers` 把原「组件逐层拆解」一章按 PROXY/COMPUTE/SAFEKEEPER/PAGESERVER/协调层
> 分流成 5 个子章节；C 册用 `ids` 把运维章重新编排成 日志诊断 / 备份恢复 / 局限总结 三组。
> 新增 slide 后：若用 `chapter` 规则会自动纳入；若用 `ids` 规则，需把新 id 补进对应 section 的列表
> （未知 id 会直接报错，不会静默漏页）。

## 如何修改内容

编辑 `gen_neon_bento.py` 中对应 slide 的文本/布局，然后按以下步骤重新生成。

## 生成 JSON

```bash
cd ppt
python3 gen_neon_bento.py
# 输出:
#   /tmp/neon_bento_deck.json          （全量 deck JSON，供嵌入 master）
#   SLIDES_INDEX.md                    （全量索引）
#   Neon_A_概览与能力.bento.html        （分册 A，直接可放映）
#   Neon_B_组件与原理.bento.html        （分册 B，直接可放映）
#   Neon_C_运维与落地.bento.html        （分册 C，直接可放映）
```

脚本会打印全量 slide 数量、JSON 大小，以及每本分册的页数。

> 注意：分册 HTML 由脚本直接读取当前的 `Bento_Slides.bento.html` 作为模板
> （复用其外壳 + 运行时），再把切片后的 JSON 嵌进去。所以**先确保 master 是最新的**
> （见下方「一键生成 + 替换」），再跑一次脚本即可让三本分册同步刷新。

## 将 JSON 替换到 HTML

HTML 文件中 `<script type="application/bento+json" id="bento-doc">` 与 `</script>` 之间的内容就是 deck JSON。替换方法：

```bash
python3 - <<'EOF'
import re

html_path = "Bento_Slides.bento.html"
json_path = "/tmp/neon_bento_deck.json"

html = open(html_path, encoding="utf-8").read()
new_json = open(json_path, encoding="utf-8").read()

pattern = re.compile(
    r'(<script type="application/bento\+json" id="bento-doc">\n)(.*?)(\n    </script>)',
    re.S,
)
new_html, n = pattern.subn(lambda m: m.group(1) + new_json + m.group(3), html, count=1)
assert n == 1, f"替换失败，匹配数 = {n}"

open(html_path, "w", encoding="utf-8").write(new_html)
print("替换完成，文件大小:", len(new_html))
EOF
```

## 一键生成 + 替换

```bash
cd ppt
python3 gen_neon_bento.py && python3 - <<'EOF'
import re
html_path = "Bento_Slides.bento.html"
html = open(html_path, encoding="utf-8").read()
new_json = open("/tmp/neon_bento_deck.json", encoding="utf-8").read()
pattern = re.compile(r'(<script type="application/bento\+json" id="bento-doc">\n)(.*?)(\n    </script>)', re.S)
new_html, n = pattern.subn(lambda m: m.group(1) + new_json + m.group(3), html, count=1)
assert n == 1
open(html_path, "w", encoding="utf-8").write(new_html)
print("Done. slides embedded.")
EOF
```

## 验证

```bash
python3 - <<'EOF'
import re, json
html = open("Bento_Slides.bento.html", encoding="utf-8").read()
m = re.search(r'<script type="application/bento\+json" id="bento-doc">\n(.*?)\n    </script>', html, re.S)
doc = json.loads(m.group(1).replace("\\u003c", "<"))
print(f"JSON valid, {len(doc['slides'])} slides")
EOF
```
