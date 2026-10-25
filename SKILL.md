---
name: red-book-ppt-stylist
description: 专注于将 PPT 全部页面按 1+4 模版批量制作成高质量小红书封面。自动分组排版，每 5 页一组，不足 5 页自动跳过。
license: MIT
---

# 小红书 1+4 PPT 封面排版专家 (Red-Book PPT Stylist)

该 Skill 专门用于执行小红书风格的 **1+4 PPT 封面批量制作流程**，确保 PPT 的每一页都能以优雅的视觉版式充分展示。

## 核心设计规范 (The Stylist Rules)
### 5图模版 (The Elite 5)
- **画布比例**：`1648x2198 px` (3:4 竖屏高清)。
- **背景风格**：`#F5EFE2` 雅致米色，叠加 5% 密度的随机 RGB 纸质噪点纹理。
- **布局逻辑**：**1+4 模式**。
  - **1张大图**：居上 (`1548x870`)，带柔和投影（半径 12，偏移 `(15, 15)`，透明度 `160/255`）。
  - **4张小图**：下方 2x2 网格 (`754x424`)，带柔和投影（半径 8，偏移 `(10, 10)`，透明度 `150/255`）。
- **Logo 署名**：底部居中可自定义署名（如 `--logo "精选PPT"`），深咖啡色宋体艺术化排版，带装饰横线及中心圆点。

## 自动化批量流程 (Batch Workflow)
1. **全量导出**：
   - 使用 AppleScript 驱动 `Keynote`（或 `Keynote Creator Studio`）。
   - 打开 `.pptx` 文件并将其**所有页面**导出为高品质 JPEG 图片。
2. **5页分组 (Grouping)**：
   - 将导出的图片按顺序每 5 张分为一组。
   - **丢弃余数**：若最后剩余图片不足 5 张，则跳过该组封面制作。
3. **循环处理**：
   - 调用 `scripts/layout_5_images.py` 对每一组图片进行 1+4 排版，或直接运行 `scripts/batch_export_1plus4.py` 执行端到端批量流水线。
   - 自动识别 PPT 序号（文件名开头的数字）作为分类标识。
4. **输出归档**：
   - 默认在指定输出目录（如 `~/Desktop/PPT小红书封面_1加4_全部`）下按 PPT 序号建立子文件夹，封面命名为 `{序号}_1plus4_part{N}.jpg`。

## 快速使用
### 1. 单组 5 张幻灯片合成 1+4 封面
```bash
python3 scripts/layout_5_images.py --slides /path/to/5_slides_dir --out /path/to/output.jpg --logo "精选PPT"
```

### 2. 批量导出目录下所有 `.pptx` 并生成 1+4 封面 (macOS Keynote)
```bash
python3 scripts/batch_export_1plus4.py --src /path/to/pptx_folder --out ~/Desktop/PPT小红书封面_1加4_全部 --logo "精选PPT"
```

## 资源与环境
- **主要脚本**：
  - `scripts/layout_5_images.py`：核心 1+4 画布合成与阴影噪点渲染引擎
  - `scripts/batch_export_1plus4.py`：Keynote 自动化导出 + 5页分组批量流水线
  - `scripts/process_ppt.py`：双图上下拼接版封面生成脚本（1+1 备选样式）
- **环境依赖**：Python 3.8+、`Pillow` (`pip install Pillow`)、macOS Keynote（仅批量导出 `.pptx` 时需要）
- **字体降级**：优先使用系统宋体 (`Songti.ttc`)，无果则自动降级至 `PingFang.ttc`。
