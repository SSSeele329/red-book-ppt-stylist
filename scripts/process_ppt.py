import os
import random
import argparse
from PIL import Image, ImageDraw, ImageFont

# 样式常量
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 1200
BG_COLOR = "#FDE8D7"
TEXT_COLOR = "#8B5A2B"
FALLBACK_FONTS = ["/System/Library/Fonts/PingFang.ttc", "Arial.ttf"]


def create_noise_background(size, color_hex):
    color = tuple(int(color_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    base = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(base)
    for _ in range(int(size[0] * size[1] * 0.05)):
        x = random.randint(0, size[0] - 1)
        y = random.randint(0, size[1] - 1)
        r, g, b = base.getpixel((x, y))
        noise = random.randint(-8, 8)
        draw.point(
            (x, y),
            fill=(
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            ),
        )
    return base


def process_images(slides_dir, output_dir, title):
    images = sorted(
        [
            f
            for f in os.listdir(slides_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    )
    if not images:
        return

    os.makedirs(output_dir, exist_ok=True)
    img_h_target = int(CANVAS_HEIGHT * 0.42)
    top_y = int(CANVAS_HEIGHT * 0.08)
    gap_y = int(CANVAS_HEIGHT * 0.04)

    font = None
    for f in ["汉仪尚巍手书.ttf"] + FALLBACK_FONTS:
        if os.path.exists(f):
            font = ImageFont.truetype(f, 25)
            break
    if not font:
        font = ImageFont.load_default()

    for i in range(0, len(images), 2):
        canvas = create_noise_background((CANVAS_WIDTH, CANVAS_HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(canvas)

        if title:
            bbox = draw.textbbox((0, 0), title, font=font)
            tw = bbox[2] - bbox[0]
            draw.text((CANVAS_WIDTH - tw - 40, 30), title, fill=TEXT_COLOR, font=font)

        pair = images[i : i + 2]
        for idx, img_name in enumerate(pair):
            with Image.open(os.path.join(slides_dir, img_name)) as slide:
                ratio = img_h_target / slide.height
                new_w = int(slide.width * ratio)
                if new_w > CANVAS_WIDTH * 0.9:
                    new_w = int(CANVAS_WIDTH * 0.9)
                    new_h = int(slide.height * (new_w / slide.width))
                else:
                    new_h = img_h_target

                slide_resized = slide.resize(
                    (new_w, new_h), Image.Resampling.LANCZOS
                )
                x_pos = (CANVAS_WIDTH - new_w) // 2
                y_pos = top_y if idx == 0 else top_y + img_h_target + gap_y
                if len(pair) == 1:
                    y_pos = top_y + (CANVAS_HEIGHT - top_y - new_h) // 2
                canvas.paste(slide_resized, (x_pos, y_pos))

        canvas.save(os.path.join(output_dir, f"封面_{i // 2 + 1}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate 2-slide stacked Xiaohongshu PPT covers."
    )
    parser.add_argument("--slides", required=True, help="Directory of slide images")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--title", default="教学课件分享", help="Top-right title text")
    args = parser.parse_args()
    process_images(args.slides, args.out, args.title)
