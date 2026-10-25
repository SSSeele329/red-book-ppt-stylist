import os
import random
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


def draw_shadowed_image(canvas, img, box, radius, offset, shadow_alpha):
    img = ImageOps.fit(img, (box[2], box[3]), Image.Resampling.LANCZOS)
    x, y, w, h = box
    padding = radius * 2
    shadow_img = Image.new("RGBA", (w + padding * 2, h + padding * 2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rectangle(
        [padding, padding, padding + w, padding + h], fill=(0, 0, 0, shadow_alpha)
    )
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius))
    canvas.paste(
        shadow_img, (x - padding + offset[0], y - padding + offset[1]), shadow_img
    )
    canvas.paste(img, (x, y))


def add_noise(image, intensity=5):
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            n = random.randint(-intensity, intensity)
            pixels[x, y] = (
                max(0, min(255, r + n)),
                max(0, min(255, g + n)),
                max(0, min(255, b + n)),
            )
    return image


def process_5_images(slides_dir, output_path, logo_text="精选PPT"):
    # Canvas Settings (3:4 High-Res Portrait)
    W, H = 1648, 2198
    # Elegant Beige: #F5EFE2 -> (245, 239, 226)
    BG_COLOR = (245, 239, 226)
    canvas = Image.new("RGB", (W, H), BG_COLOR)
    canvas = add_noise(canvas, 5)

    # Load 5 images
    all_files = sorted(
        [
            f
            for f in os.listdir(slides_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    if len(all_files) < 5:
        print(f"Error: Need at least 5 images in {slides_dir}")
        return

    images = [Image.open(os.path.join(slides_dir, all_files[i])) for i in range(5)]

    # Top image: 1 large (1548x870)
    tw, th = 1548, 870
    tx, ty = (W - tw) // 2, 80
    draw_shadowed_image(canvas, images[0], (tx, ty, tw, th), 12, (15, 15), 160)

    # Grid: 2x2 small (754x424)
    gw, gh = 754, 424
    sx, sy = 40, 40
    start_y = ty + th + 80
    start_x = (W - (gw * 2 + sx)) // 2

    draw_shadowed_image(canvas, images[1], (start_x, start_y, gw, gh), 8, (10, 10), 150)
    draw_shadowed_image(
        canvas, images[2], (start_x + gw + sx, start_y, gw, gh), 8, (10, 10), 150
    )
    draw_shadowed_image(
        canvas, images[3], (start_x, start_y + gh + sy, gw, gh), 8, (10, 10), 150
    )
    draw_shadowed_image(
        canvas,
        images[4],
        (start_x + gw + sx, start_y + gh + sy, gw, gh),
        8,
        (10, 10),
        150,
    )

    # Logo / Watermark
    if logo_text:
        draw = ImageDraw.Draw(canvas)
        main_txt = logo_text.replace("PPT", "").strip()
        suffix = " PPT" if "PPT" in logo_text.upper() else ""

        font_candidates = [
            "/System/Library/Fonts/Supplemental/Songti.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        font_p = next((f for f in font_candidates if os.path.exists(f)), None)

        if font_p:
            t_font = ImageFont.truetype(font_p, 70)
            s_font = ImageFont.truetype(font_p, 45)
        else:
            t_font = ImageFont.load_default()
            s_font = ImageFont.load_default()

        b_m = draw.textbbox((0, 0), main_txt, font=t_font)
        tw_m = b_m[2] - b_m[0]
        b_s = draw.textbbox((0, 0), suffix, font=s_font) if suffix else (0, 0, 0, 0)
        total_tw = tw_m + (b_s[2] - b_s[0])

        lx = (W - total_tw) // 2
        ly = H - 180
        txt_col = (93, 64, 55)

        draw.text((lx + 2, ly + 2), main_txt, font=t_font, fill=(0, 0, 0, 30))
        draw.text((lx, ly), main_txt, font=t_font, fill=txt_col)
        if suffix:
            draw.text((lx + tw_m + 5, ly + 20), suffix, font=s_font, fill=txt_col)

        line_y = ly + 90
        draw.line(
            [(lx - 10, line_y), (lx + total_tw + 10, line_y)], fill=txt_col, width=2
        )
        draw.ellipse(
            [
                lx + total_tw // 2 - 3,
                line_y + 15,
                lx + total_tw // 2 + 3,
                line_y + 21,
            ],
            fill=txt_col,
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path)
    print(f"5-Image Template generated at: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate 1+4 Xiaohongshu PPT cover image from 5 slide images."
    )
    parser.add_argument(
        "--slides", required=True, help="Directory containing at least 5 slide images"
    )
    parser.add_argument("--out", required=True, help="Output image file path")
    parser.add_argument(
        "--logo", default="精选PPT", help="Bottom signature text (empty string to hide)"
    )
    args = parser.parse_args()
    process_5_images(args.slides, args.out, args.logo)
