import os
import subprocess
import shutil
import re
import time
import tempfile
import argparse
from pathlib import Path


def run_applescript(ppt_path, export_folder, app_name="Keynote"):
    script = f'''
    set p to "{ppt_path}" as POSIX file
    set e to "{export_folder}" as POSIX file
    tell application "{app_name}"
        activate
        set doc to open p
        delay 3
        export doc to e as slide images with properties {{image format:JPEG, skipped slides:false}}
        close doc saving no
    end tell
    '''
    subprocess.run(["osascript", "-e", script], capture_output=True)


def process_batch(src_dir, output_root, logo_text="精选PPT", app_name="Keynote"):
    src_dir = os.path.expanduser(src_dir)
    output_root = os.path.expanduser(output_root)
    layout_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "layout_5_images.py"
    )

    os.makedirs(output_root, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="ppt_temp_exports_")

    try:
        subprocess.run(["open", "-a", app_name])
        time.sleep(2)

        ppts = [f for f in os.listdir(src_dir) if f.lower().endswith(".pptx")]

        def get_num(s):
            m = re.search(r"\d+", s)
            return int(m.group()) if m else 999

        ppts.sort(key=get_num)

        for ppt in ppts:
            ppt_name = os.path.splitext(ppt)[0]
            folder_match = re.match(r"^\d+", ppt_name)
            folder_name = folder_match.group() if folder_match else ppt_name

            ppt_path = os.path.join(src_dir, ppt)
            ppt_temp_dir = os.path.join(temp_dir, folder_name)
            if os.path.exists(ppt_temp_dir):
                shutil.rmtree(ppt_temp_dir)
            os.makedirs(ppt_temp_dir)

            print(f"Processing {ppt}...")
            run_applescript(ppt_path, ppt_temp_dir, app_name=app_name)

            images = sorted(
                [
                    i
                    for i in os.listdir(ppt_temp_dir)
                    if i.lower().endswith((".jpeg", ".jpg", ".png"))
                ]
            )
            num_templates = len(images) // 5

            if num_templates == 0:
                print(
                    f"  Skipping {ppt}: Only {len(images)} images found (need at least 5)."
                )
                shutil.rmtree(ppt_temp_dir)
                continue

            final_dir = os.path.join(output_root, folder_name)
            os.makedirs(final_dir, exist_ok=True)

            for i in range(num_templates):
                group_dir = os.path.join(ppt_temp_dir, f"group_{i}")
                os.makedirs(group_dir)

                for j in range(5):
                    shutil.copy(
                        os.path.join(ppt_temp_dir, images[i * 5 + j]), group_dir
                    )

                output_file = os.path.join(
                    final_dir, f"{folder_name}_1plus4_part{i + 1}.jpg"
                )

                cmd = [
                    "python3",
                    layout_script,
                    "--slides",
                    group_dir,
                    "--out",
                    output_file,
                    "--logo",
                    logo_text,
                ]
                res = subprocess.run(cmd, capture_output=True, text=True)

                if res.returncode == 0:
                    print(f"  Done: Part {i + 1} -> {output_file}")
                else:
                    print(f"  Error processing {ppt} Part {i + 1}: {res.stderr}")

            shutil.rmtree(ppt_temp_dir)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Batch export PPTX files via Keynote and generate 1+4 Xiaohongshu covers."
    )
    parser.add_argument(
        "--src", required=True, help="Directory containing .pptx files"
    )
    parser.add_argument(
        "--out",
        default=os.path.join(os.path.expanduser("~"), "Desktop", "PPT小红书封面_1加4_全部"),
        help="Output root directory",
    )
    parser.add_argument(
        "--logo", default="精选PPT", help="Bottom signature text"
    )
    parser.add_argument(
        "--app",
        default="Keynote Creator Studio",
        help="macOS Keynote application name (e.g. 'Keynote' or 'Keynote Creator Studio')",
    )
    args = parser.parse_args()
    process_batch(args.src, args.out, args.logo, args.app)
