import os
import csv
import shutil
from PIL import Image, ImageDraw, ImageFont

# ===========================================================
# Split 800x600 images into 8x8 (64 tiles)
# + Semi-transparent yellow grid with black numbers
# + Auto-generate/update metadata CSV (appends, doesn't overwrite)
# + Safe reruns - skips existing tiles, preserves labeled data
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

# --- Load font for numbering (cross-platform) ---
FONT = None
# Try common font paths for different operating systems
font_paths = [
    "Arial.ttf",  # Current directory
    "/System/Library/Fonts/Helvetica.ttc",  # macOS
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
    "C:/Windows/Fonts/arial.ttf",  # Windows
    "C:/Windows/Fonts/Arial.ttf",  # Windows (alternative)
]

for font_path in font_paths:
    try:
        if os.path.exists(font_path):
            FONT = ImageFont.truetype(font_path, 16)
            break
    except:
        continue

# Fallback to default font if no font found
if FONT is None:
    try:
        FONT = ImageFont.truetype("arial.ttf", 16)  # Try lowercase
    except:
        FONT = ImageFont.load_default()

# --- Create or append to metadata file ---
csv_exists = os.path.exists(CSV_FILE)
with open(CSV_FILE, mode="a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Write header only if file is new
    if not csv_exists:
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

        # Check if tiles already exist for this frame
        grid_out_path = os.path.join(dst_folder, f"{base_name}_grid_overlay.png")
        first_tile_path = os.path.join(dst_folder, f"{base_name}_tile_01.png")
        
        if os.path.exists(first_tile_path) and os.path.exists(grid_out_path):
            print(f"  Skipping {base_name} - tiles already exist")
            return False  # Indicate frame was skipped
        
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
        
        return True  # Indicate frame was processed

    # --- Process train/test images ---
    for set_type in ["train", "test"]:
        src_dir = os.path.join(SRC_BASE, set_type)
        dst_dir = os.path.join(DST_BASE, set_type)

        print(f"\nProcessing {set_type.upper()} images...")
        processed_count = 0
        skipped_count = 0
        
        for img_file in os.listdir(src_dir):
            if img_file.lower().endswith(".png"):
                img_path = os.path.join(src_dir, img_file)
                img_out_folder = os.path.join(dst_dir, f"{os.path.splitext(img_file)[0]}_tiles")
                was_processed = split_image(img_path, img_out_folder, set_type)
                if was_processed:
                    processed_count += 1
                else:
                    skipped_count += 1
        
        print(f"  Processed: {processed_count} new frames")
        if skipped_count > 0:
            print(f"  Skipped: {skipped_count} existing frames")

print("\nAll images processed!")
print(f"Metadata saved/updated: {CSV_FILE}")
print("-----------------------------------------------------------")
print("Note: CSV file is appended to (not overwritten)")
print("Existing tiles are preserved and skipped")
print("-----------------------------------------------------------")

# --- ZIP CREATION (optional - commented out to avoid overwriting) ---
# Uncomment if you want to recreate ZIP on each run
# print("\nCreating ZIP archive...")
# if os.path.exists(ZIP_FILE):
#     os.remove(ZIP_FILE)
# shutil.make_archive(DST_BASE, 'zip', DST_BASE)
# print("Dataset successfully zipped!")
# print(f"ZIP file: {ZIP_FILE}")

print("\nYour dataset is ready for ML training or upload.")
print("-----------------------------------------------------------")
