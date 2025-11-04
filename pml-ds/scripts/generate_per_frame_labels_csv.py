"""
generate_per_frame_labels_csv.py
----------------------------------------------------
Generates per-frame labeled CSVs for dataset images.
Each 800x600 frame in data/frames_dataset/{train,test}/
is divided into an 8x8 grid (64 tiles).

Outputs:
---------
data/frames_dataset_tiles/{train,test}/{frame_id}_tiles/
    ├── tile_01.png
    ├── ...
    └── {frame_id}_labels.csv   ← 64 rows, default labels = none (0)

Label Mapping:
--------------
none  -> 0
ball  -> 1
bat   -> 2
stumps-> 3

Features:
---------
- Safe reruns: Skips frames that already have tiles and CSV files
- Preserves existing labeled data - never overwrites
- Only processes new frames from frames_dataset/{train,test}/

After generation, manually edit each {frame_id}_labels.csv
to assign the correct label to tiles containing bats, balls, or stumps.

Author: Cordial Dude
----------------------------------------------------
"""

import os
import sys
import cv2
import pandas as pd
from tqdm import tqdm

# Add parent directory to path to find src module
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import utilities from your shared modules
from src.utils import read_image, ensure_dir
from src.grid_split import split_image_into_grid


# ================= CONFIGURATION =================
# Determine base directory (pml-ds) regardless of where script is run from
BASE_DIR = parent_dir  # Parent of scripts/ is pml-ds/
BASE_DATA_DIR = os.path.join(BASE_DIR, "frames_dataset")
TILES_BASE_DIR = os.path.join(BASE_DIR, "frames_dataset_tiles")
GRID_COLS, GRID_ROWS = 8, 8

# Label map (as per modeling task)
LABEL_MAP = {
    "none": 0,
    "ball": 1,
    "bat": 2,
    "stumps": 3
}
# =================================================


def process_split(split_name: str):
    """Process 'train' or 'test' split to generate tiles + per-frame label CSVs."""
    frames_dir = os.path.join(BASE_DATA_DIR, split_name)
    tiles_split_dir = os.path.join(TILES_BASE_DIR, split_name)
    ensure_dir(tiles_split_dir)

    frame_files = sorted([
        f for f in os.listdir(frames_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    print(f"\nProcessing {split_name.upper()} split - {len(frame_files)} frames found")

    processed_count = 0
    skipped_count = 0

    for fname in tqdm(frame_files, desc=f"Processing {split_name}"):
        frame_id = os.path.splitext(fname)[0]
        img_path = os.path.join(frames_dir, fname)
        
        # Create output folder for tiles
        frame_tile_dir = os.path.join(tiles_split_dir, f"{frame_id}_tiles")
        ensure_dir(frame_tile_dir)
        
        # Check if tiles and CSV already exist
        csv_path = os.path.join(frame_tile_dir, f"{frame_id}_labels.csv")
        first_tile_path = os.path.join(frame_tile_dir, "tile_01.png")
        
        if os.path.exists(csv_path) and os.path.exists(first_tile_path):
            skipped_count += 1
            continue  # Skip frames that already have tiles and CSV
        
        img = read_image(img_path)

        # Split into 8×8 grid tiles
        tiles = split_image_into_grid(img, cols=GRID_COLS, rows=GRID_ROWS)
        if len(tiles) != 64:
            print(f"WARNING: {fname}: Expected 64 tiles, got {len(tiles)} — skipping")
            continue

        # Save tiles and collect metadata
        records = []
        for i, tile in enumerate(tiles):
            tile_filename = f"tile_{i+1:02d}.png"
            tile_path = os.path.join(frame_tile_dir, tile_filename)
            cv2.imwrite(tile_path, cv2.cvtColor(tile, cv2.COLOR_RGB2BGR))

            records.append({
                "ImageFileName": fname,
                "TrainOrTest": split_name,
                "TileIndex": i + 1,  # 1–64
                "TilePath": tile_path,
                "LabelText": "none",
                "LabelCode": LABEL_MAP["none"]
            })

        # Save per-frame CSV (only if it doesn't exist)
        if not os.path.exists(csv_path):
            pd.DataFrame(records).to_csv(csv_path, index=False)
            processed_count += 1
        else:
            skipped_count += 1
    
    print(f"  Processed: {processed_count} new frames")
    if skipped_count > 0:
        print(f"  Skipped: {skipped_count} existing frames")


if __name__ == "__main__":
    for split in ["train", "test"]:
        process_split(split)
    print("\nAll per-frame label CSVs processed!")
    print("Note: Existing tiles and CSVs are preserved and skipped")
    print("Only new frames are processed and added")
