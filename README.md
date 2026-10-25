# Red-Book PPT Stylist (`red-book-ppt-stylist`)

专注于将 PPT 全部页面按 **1+4 模版**批量制作成高质量小红书竖屏封面（3:4 比例）的 Agent Skill。兼容 Claude Code、Gemini CLI / Antigravity、Codex 等支持 `SKILL.md` 规范的 AI 编程助手。

## ✨ 特性

- **1+4 黄金视觉布局**：顶部 1 张大图（`1548x870`）+ 下方 2x2 网格 4 张小图（`754x424`），在 `1648x2198` 高清 3:4 竖屏画布上最大化展示课件细节。
- **质感纸纹与立体投影**：`#F5EFE2` 雅致米色背景叠加 5% 随机纸质噪点，配合高斯模糊立体投影。
- **底部艺术署名**：自动渲染带中心圆点装饰线的宋体艺术化底部署名，支持通过 `--logo` 参数自定义或隐藏。
- **Keynote 全自动批量流水线**：支持通过 AppleScript 驱动 macOS Keynote 将 `.pptx` 全量导出为高清图片，并按每 5 页一组自动合成封面。

## 📦 安装方式

### 作为 AI Agent Skill 安装

将本仓库克隆到你的全局或项目级 `skills` 目录：

```bash
# Claude Code / 通用 ~/.agents/skills
git clone https://github.com/SSSeele329/red-book-ppt-stylist.git ~/.agents/skills/red-book-ppt-stylist

# Gemini CLI / Antigravity
git clone https://github.com/SSSeele329/red-book-ppt-stylist.git ~/.gemini/skills/red-book-ppt-stylist
```

### Python 依赖

```bash
pip install Pillow
```

## 🚀 命令行快速使用

### 1. 将 5 张幻灯片图片合成为 1+4 小红书封面

```bash
python3 scripts/layout_5_images.py \
  --slides ./my_slides_5 \
  --out ./cover_1plus4.jpg \
  --logo "精选PPT"
```

### 2. 批量导出文件夹内所有 `.pptx` 并生成封面（macOS）

```bash
python3 scripts/batch_export_1plus4.py \
  --src ~/Desktop/PPT源文件 \
  --out ~/Desktop/PPT小红书封面_1加4_全部 \
  --logo "精选PPT" \
  --app "Keynote"
```

### 3. 双图上下拼接模式（1+1 备选样式）

```bash
python3 scripts/process_ppt.py \
  --slides ./my_slides \
  --out ./output_covers \
  --title "教学课件分享"
```

## 📄 License

[MIT](./LICENSE)
