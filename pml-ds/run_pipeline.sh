#!/bin/bash
# ===========================================================
# YouTube → Image Dataset Pipeline Execution Script
# ===========================================================
# This script executes the complete pipeline in sequence:
# 1. youtube_video_to_frames.sh - Extract frames from YouTube video
# 2. generate_dataset_info_csv.py - Generate dataset metadata CSV
# 3. split_8x8_grid_numbered.py - Split images into 8x8 grid tiles
# 4. generate_per_frame_labels_csv.py - Generate per-frame labels CSV
# ===========================================================

set -e  # Exit immediately on error

# --- Check if virtual environment exists ---
if [ ! -d "venv" ]; then
  echo "Error: Virtual environment not found!"
  echo "Please run './setup.sh' first to set up the environment."
  exit 1
fi

# --- Activate venv ---
echo "Activating Python environment..."
source venv/bin/activate

# --- Verify required scripts exist ---
echo "Verifying required scripts..."

if [ ! -f "scripts/youtube_video_to_frames.sh" ]; then
  echo "Error: Missing scripts/youtube_video_to_frames.sh!"
  exit 1
fi

if [ ! -f "scripts/generate_dataset_info_csv.py" ]; then
  echo "Error: Missing scripts/generate_dataset_info_csv.py!"
  exit 1
fi

if [ ! -f "scripts/split_8x8_grid_numbered.py" ]; then
  echo "Error: Missing scripts/split_8x8_grid_numbered.py!"
  exit 1
fi

if [ ! -f "scripts/generate_per_frame_labels_csv.py" ]; then
  echo "Error: Missing scripts/generate_per_frame_labels_csv.py!"
  exit 1
fi

# --- Make shell script executable ---
chmod +x scripts/youtube_video_to_frames.sh

# --- Step 1: Extract frames from YouTube video ---
echo ""
echo "==========================================================="
echo "Step 1: Extracting frames from YouTube video"
echo "==========================================================="
./scripts/youtube_video_to_frames.sh

# --- Step 2: Generate dataset info CSV ---
echo ""
echo "==========================================================="
echo "Step 2: Generating dataset info CSV"
echo "==========================================================="
python scripts/generate_dataset_info_csv.py

# --- Step 3: Split images into 8x8 grid tiles ---
echo ""
echo "==========================================================="
echo "Step 3: Splitting images into 8x8 grid tiles"
echo "==========================================================="
python scripts/split_8x8_grid_numbered.py

# --- Step 4: Generate per-frame labels CSV ---
echo ""
echo "==========================================================="
echo "Step 4: Generating per-frame labels CSV"
echo "==========================================================="
python scripts/generate_per_frame_labels_csv.py

# --- Deactivate environment ---
deactivate

# --- Completion summary ---
echo ""
echo "==========================================================="
echo "Pipeline execution completed successfully!"
echo "==========================================================="
echo "Output generated:"
echo " - frames_dataset/train → Training frames (800×600)"
echo " - frames_dataset/test  → Test frames (800×600)"
echo " - frames_dataset_tiles/ → 8x8 grid tiles + overlays"
echo " - dataset_info.csv → Dataset metadata"
echo " - per_frame_labels.csv → Per-frame labels"
echo "==========================================================="
echo "Next steps:"
echo "1. Label your images/tiles as needed"
echo "2. Run 'python scripts/check_label_distribution.py' to check label distribution"
echo "==========================================================="

