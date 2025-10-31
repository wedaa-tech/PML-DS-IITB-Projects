import os
import csv
import shutil
from PIL import Image, ImageDraw, ImageFont

# ===========================================================
# 🧩 Split 800x600 images into 8x8 (64 tiles)
# + Semi-transparent yellow grid with black numbers
# + Auto-generate metadata CSV
# + Zip the final dataset (train/test + CSV)
# ===========================================================

# --- Configuration ---
SRC_BASE = "frames_dataset"              # Input dataset
DST_BASE = "frames_dataset_tiles"        # Output tiles dataset
ZIP_FILE = "frames_dataset_tiles.zip"    # Final compressed dataset
TILE_COLS = 8
TILE_ROWS = 8
IMG_W, IMG_H = 800, 600
TILE_W, TILE_H = IMG_W // TILE_COLS, IMG_H // TILE_ROWS
DRAW_GRID = True
CSV_FILE = os.path.join(DST_BASE, "tiles_info.csv")

# --- Create output structure ---
os.makedirs(os.path.join(DST_BASE, "train"), exist_ok=True)
os.makedirs(os.path.join(DST_BASE, "test"), exist_ok=True)

# --- Load font for numbering ---
try:
    FONT = ImageFont.truetype("Arial.ttf", 16)
except:
    FONT = ImageFont.load_default()

# --- Create metadata file ---
with open(CSV_FILE, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["tile_path", "set_type", "parent_image", "row", "col", "tile_index"])

    def split_image(img_path, dst_folder, set_type):
        """Splits a single 800x600 image into 64 tiles and adds grid overlay"""
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        os.makedirs(dst_folder, exist_ok=True)
        img = Image.open(img_path).convert("RGB")
        w, h = img.size

        # Resize safety
        if w != IMG_W or h != IMG_H:
            img = img.resize((IMG_W, IMG_H))

        # === GRID OVERLAY VISUALIZATION ===
        if DRAW_GRID:
            grid_img = img.copy().convert("RGBA")
            overlay = Image.new("RGBA", grid_img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)

            # Semi-transparent yellow grid lines
            for r in range(1, TILE_ROWS):
                y = r * TILE_H
                draw.line([(0, y), (IMG_W, y)], fill=(255, 255, 0, 160), width=2)
            for c in range(1, TILE_COLS):
                x = c * TILE_W
                draw.line([(x, 0), (x, IMG_H)], fill=(255, 255, 0, 160), width=2)

            # Black cell numbers (1–64)
            tile_index = 1
            for r in range(TILE_ROWS):
                for c in range(TILE_COLS):
                    text = str(tile_index)
                    text_x = c * TILE_W + TILE_W / 2 - 8
                    text_y = r * TILE_H + TILE_H / 2 - 8
                    draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=FONT)
                    tile_index += 1

            combined = Image.alpha_composite(grid_img, overlay)
            grid_out_path = os.path.join(dst_folder, f"{base_name}_grid_overlay.png")
            combined.convert("RGB").save(grid_out_path)

        # === TILE EXTRACTION ===
        tile_index = 1
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                left, upper = c * TILE_W, r * TILE_H
                right, lower = left + TILE_W, upper + TILE_H
                tile = img.crop((left, upper, right, lower))

                tile_filename = f"{base_name}_tile_{tile_index:02d}.png"
                tile_path = os.path.join(dst_folder, tile_filename)
                tile.save(tile_path)
                writer.writerow([tile_path, set_type, base_name, r + 1, c + 1, tile_index])
                tile_index += 1

    # --- Process train/test images ---
    for set_type in ["train", "test"]:
        src_dir = os.path.join(SRC_BASE, set_type)
        dst_dir = os.path.join(DST_BASE, set_type)

        print(f"📂 Processing {set_type.upper()} images...")
        for img_file in os.listdir(src_dir):
            if img_file.lower().endswith(".png"):
                img_path = os.path.join(src_dir, img_file)
                img_out_folder = os.path.join(dst_dir, f"{os.path.splitext(img_file)[0]}_tiles")
                split_image(img_path, img_out_folder, set_type)

print("✅ All images split and grid overlays generated!")
print(f"📊 Metadata saved to: {CSV_FILE}")

# --- ZIP CREATION ---
print("📦 Creating ZIP archive...")

if os.path.exists(ZIP_FILE):
    os.remove(ZIP_FILE)

shutil.make_archive(DST_BASE, 'zip', DST_BASE)

print("✅ Dataset successfully zipped!")
print(f"📁 ZIP file: {ZIP_FILE}")
print("-----------------------------------------------------------")
print("🎯 Your dataset is ready for ML training or upload.")
print("-----------------------------------------------------------")
