# Neon 架构 PPT (Bento Slides)

## 文件说明

| 文件 | 用途 |
|------|------|
| `gen_neon_bento.py` | Python 生成器脚本，定义所有 slide 内容和布局 |
| `Bento_Slides.bento.html` | 最终的单文件 HTML 演示文稿，浏览器直接打开即可放映 |

## 如何修改内容

编辑 `gen_neon_bento.py` 中对应 slide 的文本/布局，然后按以下步骤重新生成。

## 生成 JSON

```bash
cd ppt
python3 gen_neon_bento.py
# 输出: /tmp/neon_bento_deck.json
```

脚本会打印 slide 数量和 JSON 文件大小。

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
