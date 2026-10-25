# Red-Book PPT Stylist (`red-book-ppt-stylist`)

专注于将 PPT 全部页面按 **1+4 模版**批量制作成高质量小红书竖屏封面（3:4 比例）的 AI Agent Skill。兼容 Claude Code、Gemini CLI / Antigravity、Codex、Cursor 等支持 `SKILL.md` 规范的 AI 编程助手。

## 🖼️ 产出效果预览

<p align="center">
  <img src="./assets/demo_1.jpg" width="45%" alt="1+4 封面效果示例 1" />
  <img src="./assets/demo_2.jpg" width="45%" alt="1+4 封面效果示例 2" />
</p>

---

## 💡 核心工作流（全自动端到端）

你只需要在 AI Agent 中指定包含 `.pptx` 文件的文件夹并触发该 Skill，Agent 就会**全自动完成以下全部流程**：

1. **全量高清导出**：自动唤醒 macOS `Keynote` 打开文件夹内的所有 `.pptx` 课件，将每一页幻灯片导出为高品质图片。
2. **智能 5 页分组**：按顺序每 5 页分为一组（最后不足 5 页的余数自动跳过，保证每张封面排版饱满）。
3. **1+4 视觉合成**：每组自动合成为 1 张 `1648x2198` 的小红书 3:4 竖屏封面（顶部 1 张大图 + 下方 2x2 四宫格小图 + 雅致米色噪点纸纹背景 + 立体高斯投影 + 底部艺术署名）。
4. **自动新建文件夹归档**：处理完成后，自动在桌面（或指定位置）新建总输出目录（默认 `PPT小红书封面_1加4_全部`），并**按每个 PPT 的序号/名称自动建立独立子文件夹**，将生成的 `{序号}_1plus4_part1.jpg`, `part2.jpg`... 整齐归档存放。

---

## 📦 1. 安装 Skill

将本仓库克隆到你所使用的 AI Agent 的 `skills` 目录中：

```bash
# 通用 Agent 目录 (Claude Code / Codex / OpenAgents 等)
git clone https://github.com/SSSeele329/red-book-ppt-stylist.git ~/.agents/skills/red-book-ppt-stylist

# Gemini CLI / Antigravity
git clone https://github.com/SSSeele329/red-book-ppt-stylist.git ~/.gemini/skills/red-book-ppt-stylist

# Claude Code 专属目录
git clone https://github.com/SSSeele329/red-book-ppt-stylist.git ~/.claude/skills/red-book-ppt-stylist
```

确保本地 Python 环境已安装 `Pillow`：
```bash
pip install Pillow
```

---

## 🤖 2. 在 AI Agent 中直接使用（推荐）

安装完成后，无需手动敲复杂的命令行。直接在对话框中把要处理的 PPT 文件夹路径发给 Agent，或者在选中文件夹后输入自然语言指令即可自动执行：

### 常用唤醒词示例：
> **示例 1（默认全自动处理）**：
> 「用 `red-book-ppt-stylist` 帮我把 `~/Desktop/我的PPT课件` 文件夹里的所有 PPT 批量做成小红书 1+4 封面。」

> **示例 2（指定底部署名与输出位置）**：
> 「调用小红书排版 skill 处理 `/Users/xxx/Desktop/三年级语文课件`，底部署名改成『王老师课件』，全部处理完新建文件夹放到桌面的『小红书待发布』目录里。」

### 自动生成的归档目录结构：
执行完毕后，Agent 会自动为你建立如下清晰的文件夹结构：
```text
~/Desktop/PPT小红书封面_1加4_全部/       <-- 自动新建的总输出文件夹
├── 01/                                 <-- 按 PPT 序号/文件名自动新建的子文件夹
│   ├── 01_1plus4_part1.jpg             <-- 第 1~5 页生成的 1+4 封面
│   ├── 01_1plus4_part2.jpg             <-- 第 6~10 页生成的 1+4 封面
│   └── 01_1plus4_part3.jpg             <-- 第 11~15 页生成的 1+4 封面
├── 02/
│   ├── 02_1plus4_part1.jpg
│   └── 02_1plus4_part2.jpg
...
```

---

## 🎨 3. 自定义与修改排版格式

你可以根据自己的视觉偏好，**直接用自然语言让 Agent 帮你修改排版脚本**，或者手动调整脚本参数：

### 方式 A：直接让 AI Agent 帮你改版式（零代码）
在对话中直接告诉 Agent 你的排版需求，Agent 会自动修改 `scripts/layout_5_images.py` 并重新生成：
- *「把背景颜色从米色改成浅莫兰迪绿（`#E8F0E8`），去掉底部的文字水印。」*
- *「我不想要 1+4 布局，帮我改成 **1+2 布局**（上面 1 张大图，下面左右各 1 张中等大小的图），每 3 页 PPT 生成一张。」*
- *「帮我用双图上下拼接模式（`process_ppt.py`）处理这个文件夹，右上角标题写『今日干货分享』。」*

### 方式 B：手动调整核心排版参数
打开 [`scripts/layout_5_images.py`](./scripts/layout_5_images.py)，可自由定制以下视觉参数：

| 可调项 | 代码位置与默认参数 | 修改说明 |
| :--- | :--- | :--- |
| **底部署名 / 隐藏水印** | `--logo "精选PPT"` | 运行命令时传入 `--logo "你的名字"`，或传 `--logo ""` 完全隐藏底部水印 |
| **画布尺寸与比例** | `W, H = 1648, 2198` | 默认 3:4 竖屏高清，可按需改为 `1200, 1600` 或 `1080, 1440` |
| **背景颜色与纸纹噪点** | `BG_COLOR = (245, 239, 226)`<br>`add_noise(canvas, 5)` | 修改 RGB 元组即可更换背景色；将 `5` 改为 `0` 可关闭纸质噪点纹理 |
| **顶部大图尺寸与阴影** | `tw, th = 1548, 870`<br>`radius=12, offset=(15, 15)` | 调整顶部主图的宽高、上边距 `ty = 80` 以及高斯模糊阴影半径与透明度 |
| **下方四宫格尺寸与间距** | `gw, gh = 754, 424`<br>`sx, sy = 40, 40` | 调整下方 2x2 网格小图的尺寸与水平/垂直间距 |
| **署名与装饰线字体颜色** | `txt_col = (93, 64, 55)`<br>`font_candidates = [...]` | 可添加自定义字体路径（如手写体 `.ttf`）及修改文字 RGB 颜色 |

> 💡 **内置备选版式（1+1 上下双图拼接）**：
> 仓库同时内置了 [`scripts/process_ppt.py`](./scripts/process_ppt.py)，支持每 2 页 PPT 上下垂直拼接为一张 `900x1200` 封面，并在右上角添加自定义标题。

---

## 🛠️ 4. 命令行独立运行说明（脱离 Agent 手动调用）

如果你不通过 Agent，也可以直接在终端运行脚本：

### 批量处理整个文件夹的 `.pptx`
```bash
python3 scripts/batch_export_1plus4.py \
  --src ~/Desktop/待处理PPT文件夹 \
  --out ~/Desktop/PPT小红书封面_1加4_全部 \
  --logo "精选PPT" \
  --app "Keynote"
```
*(注：如果你安装的是 Apple Creator Studio 版 Keynote，可将 `--app` 设为 `"Keynote Creator Studio"`)*

### 单组 5 张图片合成 1+4 封面
```bash
python3 scripts/layout_5_images.py \
  --slides ./my_5_slides_dir \
  --out ./cover_1plus4.jpg \
  --logo "精选PPT"
```

### 双图上下拼接模式（1+1 样式）
```bash
python3 scripts/process_ppt.py \
  --slides ./my_slides_dir \
  --out ./output_covers \
  --title "教学课件分享"
```

---

## 📄 License

[MIT](./LICENSE)
