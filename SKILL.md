---
name: red-book-ppt-stylist
description: 专注于将 PPT 全部页面按 1+4 模版批量制作成高质量小红书封面。当用户指定要处理的 PPT 文件夹并调用此 Skill 时，自动完成 Keynote 导出、每 5 页分组排版、并在输出目录下按 PPT 重新建立独立子文件夹归档存放；同时支持根据用户需求灵活修改排版格式（如背景色、布局、署名等）。
license: MIT
---

# 小红书 1+4 PPT 封面排版专家 (Red-Book PPT Stylist)

该 Skill 专门用于执行小红书风格的 **1+4 PPT 封面全自动批量制作流程**。用户只需指定包含 `.pptx` 的文件夹，Agent 即可自动执行全部处理，并自动新建归档文件夹结构；同时支持按用户要求随时定制或修改排版格式。

## 🤖 Agent 自动化执行守则 (Agent Execution Protocol)

当用户选择或指定了一个要处理的 PPT 文件夹（或单个 `.pptx` 文件）并触发本 Skill 时，请**无需等待每一步确认，直接全自动执行以下完整流水线**：

1. **自动定位脚本路径**：
   - 获取当前 `SKILL.md` 所在目录的绝对路径，定位 `scripts/batch_export_1plus4.py` 和 `scripts/layout_5_images.py`。
2. **自动检测 Keynote 应用名称**：
   - 检查 `/Applications` 下是 `Keynote.app` 还是 `Keynote Creator Studio.app`，传入对应的 `--app` 参数。
3. **一键执行全量导出与分组排版**：
   - 运行 `scripts/batch_export_1plus4.py --src "<用户的PPT文件夹>" --out "<输出目录>" --logo "<署名>"`。
   - 脚本会自动唤醒 Keynote 导出所有页面为高清 JPEG，按每 5 页一组合成 1+4 封面（不足 5 页的余数自动跳过）。
4. **自动新建文件夹并分类归档**：
   - 默认在桌面新建 `PPT小红书封面_1加4_全部` 总目录（或用户指定的输出目录）。
   - 在总目录下**自动为每个 PPT 重新建立独立子文件夹**（优先提取文件名前缀序号如 `01`、`02`，无序号则使用 PPT 文件名），将生成的所有 `{序号}_1plus4_part{N}.jpg` 整齐放入对应子文件夹中。
5. **汇报处理结果**：
   - 执行完毕后，向用户汇报处理的 PPT 数量、生成的封面总数以及新建归档文件夹的完整路径。

---

## 🎨 核心设计规范与自定义排版指南 (Stylist Rules & Customization)

### 默认 5 图模版 (The Elite 5 - `scripts/layout_5_images.py`)
- **画布比例**：`1648x2198 px` (3:4 竖屏高清)。
- **背景风格**：`#F5EFE2` (`RGB: 245, 239, 226`) 雅致米色，叠加 5% 强度的随机 RGB 纸质噪点纹理。
- **布局逻辑**：**1+4 模式**。
  - **1 张大图**：居上 (`1548x870`，上边距 `80px`)，带柔和投影（高斯半径 `12`，偏移 `(15, 15)`，透明度 `160/255`）。
  - **4 张小图**：下方 2x2 网格 (`754x424`，间距 `40px`)，带柔和投影（高斯半径 `8`，偏移 `(10, 10)`，透明度 `150/255`）。
- **Logo 署名**：底部居中可自定义署名（默认 `--logo "精选PPT"`，传 `""` 可隐藏），深咖啡色 `(93, 64, 55)` 宋体艺术化排版，带装饰横线及中心圆点。

### 如何根据用户需求自行修改排版格式
如果用户提出自定义排版需求（例如修改背景色、改用 1+2 / 1+1 布局、调整图片间距、更换字体或隐藏水印）：
1. **仅修改署名或输出路径**：直接通过命令行参数 `--logo "自定义署名"`（或 `--logo ""`）及 `--out "自定义路径"` 传参，无需改代码。
2. **切换为双图上下拼接版式（1+1 模式）**：调用 `scripts/process_ppt.py --slides <图片目录> --out <输出目录> --title "右上角标题"`。
3. **定制画布颜色、网格数量或阴影参数**：直接编辑 `scripts/layout_5_images.py` 中的 `BG_COLOR`、画布尺寸 `W, H`、大图尺寸 `(tw, th)` 或小图网格 `(gw, gh)` 参数后再运行流水线。

---

## 🚀 命令行调用参考

### 1. 全自动批量处理文件夹内所有 `.pptx` 并建夹归档
```bash
python3 scripts/batch_export_1plus4.py \
  --src "/path/to/pptx_folder" \
  --out "~/Desktop/PPT小红书封面_1加4_全部" \
  --logo "精选PPT" \
  --app "Keynote"
```

### 2. 单组 5 张幻灯片合成 1+4 封面
```bash
python3 scripts/layout_5_images.py \
  --slides "/path/to/5_slides_dir" \
  --out "/path/to/output.jpg" \
  --logo "精选PPT"
```

### 3. 双图上下拼接模式（1+1 备选样式）
```bash
python3 scripts/process_ppt.py \
  --slides "/path/to/slides_dir" \
  --out "/path/to/output_dir" \
  --title "教学课件分享"
```
