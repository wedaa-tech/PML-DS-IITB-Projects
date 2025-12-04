"""
generate_per_frame_labels_csv.py
----------------------------------------------------
Generates a single CSV file per split (train/test) with all tile labels.
Each 800x600 frame is divided into an 8x8 grid (64 tiles).

Outputs:
---------
frames_dataset_tiles/train/objects_train_dataset.csv   ← One CSV with all train tiles
frames_dataset_tiles/test/objects_test_dataset.csv    ← One CSV with all test tiles

CSV Format:
-----------
image_filename,cell_number,cell_row,cell_col,label,c1,c2,c3,...,c64

Each row represents ONE TILE (64 rows per image).
- image_filename: e.g., "frame_0084_grid_overlay.png"
- cell_number: 1-64 (tile number)
- cell_row: 1-8 (row in 8x8 grid)
- cell_col: 1-8 (column in 8x8 grid)
- label: 0 (none), 1 (ball), 2 (bat), 3 (stump)
- c1 to c64: default 0.0 (float values)

Example:
--------
frame_0084_grid_overlay.png,1,1,1,0,0.0,0.0,...,0.0
frame_0084_grid_overlay.png,2,1,2,0,0.0,0.0,...,0.0
...
frame_0084_grid_overlay.png,64,8,8,0,0.0,0.0,...,0.0

Label Mapping:
--------------
0: none
1: ball
2: bat
3: stump

Features:
---------
- Generates one consolidated CSV file per split
- Each row = one tile (64 rows per image)
- Default label is 0 (none) for all tiles
- Default c1-c64 values are 0.0 (float)
- Preserves existing tiles if they exist

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
NUM_TILES = GRID_COLS * GRID_ROWS  # 64 tiles

# Label map (as per modeling task)
LABEL_MAP = {
    "none": 0,
    "ball": 1,
    "bat": 2,
    "stump": 3  # Note: requirement says "stump" not "stumps"
}
# =================================================


def process_split(split_name: str):
    """Process 'train' or 'test' split to generate consolidated labels CSV."""
    frames_dir = os.path.join(BASE_DATA_DIR, split_name)
    tiles_split_dir = os.path.join(TILES_BASE_DIR, split_name)
    ensure_dir(tiles_split_dir)
    
    # Output CSV path: frames_dataset_tiles/{train|test}/objects_{split}_dataset.csv
    if split_name == "train":
        output_csv_path = os.path.join(tiles_split_dir, "objects_train_dataset.csv")
    else:
        output_csv_path = os.path.join(tiles_split_dir, "objects_test_dataset.csv")

    frame_files = sorted([
        f for f in os.listdir(frames_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    print(f"\nProcessing {split_name.upper()} split - {len(frame_files)} frames found")

    # Prepare column names: image_filename,cell_number,cell_row,cell_col,label,c1,c2,...,c64
    column_names = ["image_filename", "cell_number", "cell_row", "cell_col", "label"] + [f"c{i}" for i in range(1, NUM_TILES + 1)]
    
    # List to store all tile records (64 rows per image)
    all_records = []

    for fname in tqdm(frame_files, desc=f"Processing {split_name}"):
        frame_id = os.path.splitext(fname)[0]
        img_path = os.path.join(frames_dir, fname)
        
        # Create output folder for tiles
        frame_tile_dir = os.path.join(tiles_split_dir, f"{frame_id}_tiles")
        ensure_dir(frame_tile_dir)
        
        # Check if tiles already exist
        first_tile_path = os.path.join(frame_tile_dir, "tile_01.png")
        tiles_exist = os.path.exists(first_tile_path)
        
        if not tiles_exist:
            # Generate tiles if they don't exist
            img = read_image(img_path)
            
            # Split into 8×8 grid tiles
            tiles = split_image_into_grid(img, cols=GRID_COLS, rows=GRID_ROWS)
            if len(tiles) != NUM_TILES:
                print(f"WARNING: {fname}: Expected {NUM_TILES} tiles, got {len(tiles)} — skipping")
                continue

            # Save tiles
            for i, tile in enumerate(tiles):
                tile_filename = f"tile_{i+1:02d}.png"
                tile_path = os.path.join(frame_tile_dir, tile_filename)
                cv2.imwrite(tile_path, cv2.cvtColor(tile, cv2.COLOR_RGB2BGR))
        
        # Image filename: use grid overlay name format (e.g., "frame_0084_grid_overlay.png")
        image_filename = f"{frame_id}_grid_overlay.png"
        
        # Check if there's an existing per-frame CSV with labels
        per_frame_csv = os.path.join(frame_tile_dir, f"{frame_id}_labels.csv")
        existing_labels = {}
        
        if os.path.exists(per_frame_csv):
            # Load existing labels if per-frame CSV exists
            try:
                existing_df = pd.read_csv(per_frame_csv)
                # Map existing labels by TileIndex
                for _, row in existing_df.iterrows():
                    tile_idx = int(row['TileIndex'])
                    label_code = int(row['LabelCode'])
                    existing_labels[tile_idx] = label_code
            except Exception as e:
                print(f"Warning: Could not read existing labels for {frame_id}: {e}")
        
        # Generate 64 rows (one per tile) for this image
        tile_index = 1
        for row_idx in range(1, GRID_ROWS + 1):  # 1 to 8
            for col_idx in range(1, GRID_COLS + 1):  # 1 to 8
                # Get label from existing labels or default to 0
                label = existing_labels.get(tile_index, LABEL_MAP["none"])
                
                # Create record for this tile
                record = {
                    "image_filename": image_filename,
                    "cell_number": tile_index,
                    "cell_row": row_idx,
                    "cell_col": col_idx,
                    "label": label
                }
                
                # Add c1 to c64 columns, all default to 0.0 (float)
                for c in range(1, NUM_TILES + 1):
                    record[f"c{c}"] = 0.0
                
                all_records.append(record)
                tile_index += 1
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_records, columns=column_names)
    df.to_csv(output_csv_path, index=False)
    
    print(f"\nGenerated labels CSV: {output_csv_path}")
    print(f"Total images: {len(frame_files)}")
    print(f"Total tile rows: {len(all_records)} (64 rows per image)")
    print(f"CSV columns: {len(column_names)} (image_filename, cell_number, cell_row, cell_col, label, c1-c64)")


if __name__ == "__main__":
    for split in ["train", "test"]:
        process_split(split)
    print("\nAll label CSVs generated successfully!")
    print("Note: One CSV file per split (train/test) with all tiles")
    print("Each image generates 64 rows (one per tile)")
    print("Default label is 0 (none) for all tiles")
    print("Default c1-c64 values are 0.0 (float)")
