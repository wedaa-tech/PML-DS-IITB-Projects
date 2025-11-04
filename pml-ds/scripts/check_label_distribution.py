"""
check_label_distribution.py
----------------------------------------------------
Reads all per-frame labeling CSVs under:
    data/frames_dataset_tiles/{train,test}/

Summarizes label frequencies per split and per class.

Author: Cordial Dude
----------------------------------------------------
"""

import os
import sys
import pandas as pd
from collections import Counter

# Determine base directory (pml-ds) regardless of where script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
BASE_DIR = os.path.join(parent_dir, "frames_dataset_tiles")

# Label code mapping
LABEL_CODE_MAP = {
    0: "no object",
    1: "ball",
    2: "bat",
    3: "stump"
}

def analyze_split(split_name):
    split_dir = os.path.join(BASE_DIR, split_name)
    frame_dirs = [os.path.join(split_dir, d) for d in os.listdir(split_dir)
                  if os.path.isdir(os.path.join(split_dir, d))]

    label_counts = Counter()
    frame_stats = []

    for frame_dir in frame_dirs:
        csvs = [f for f in os.listdir(frame_dir) if f.endswith("_labels.csv")]
        if not csvs:
            print(f"DEBUG: No labels CSV found in {frame_dir}")
            continue
        csv_path = os.path.join(frame_dir, csvs[0])
        print(f"DEBUG: Processing labels CSV: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"DEBUG:   - CSV contains {len(df)} rows")
        counts = df['LabelCode'].value_counts().to_dict()
        # Convert code keys to strings for display
        counts_str = {str(k): v for k, v in counts.items()}
        print(f"DEBUG:   - Label code distribution: {counts_str}")
        # Update label_counts with LabelCode values
        label_counts.update(counts)

        # store per-frame info
        total = len(df)
        none = counts.get(0, 0)  # Code 0 = no object
        non_none = total - none
        frame_stats.append({
            'Frame': os.path.basename(frame_dir),
            'TotalTiles': total,
            'NoneTiles': none,
            'NonNoneTiles': non_none
        })

    # Summary
    total_labels = sum(label_counts.values())
    print(f"\n{split_name.upper()} SPLIT SUMMARY")
    # Sort by label code for consistent output
    for code in sorted(label_counts.keys()):
        cnt = label_counts[code]
        pct = (cnt / total_labels) * 100
        label_name = LABEL_CODE_MAP.get(code, f"unknown({code})")
        print(f"Code {code} ({label_name:<12}): {cnt:6d} ({pct:5.2f}%)")

    # Find frames with no objects
    no_obj_frames = [f for f in frame_stats if f['NonNoneTiles'] == 0]
    print(f"\nFrames with NO objects: {len(no_obj_frames)} out of {len(frame_stats)}")

    return label_counts, frame_stats


if __name__ == "__main__":
    for split in ["train", "test"]:
        analyze_split(split)
