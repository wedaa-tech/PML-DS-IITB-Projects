#!/bin/bash
# ===========================================================
# YouTube → ML Dataset Generator (High Quality + Metadata)
# Author: ChatGPT (Cordial Dude edition)
# ===========================================================
# Features:
# - Stable (downloads video before processing)
# - Captures frames at user-defined interval
# - High quality (q:v=2)
# - Creates train/test split
# - Safe reruns - appends new frames without overwriting existing ones
# - Sequential frame numbering continues from existing frames
# ===========================================================

# --- Config ---
BASE_DIR="frames_dataset"
TRAIN_DIR="$BASE_DIR/train"
TEST_DIR="$BASE_DIR/test"
TEMP_FILE="temp_youtube_video.mp4"

# --- User Inputs ---
read -p "Enter YouTube video URL: " YT_URL
read -p "Enter time gap between frames (in seconds, e.g. 2): " GAP
read -p "Enter total number of frames to capture (e.g. 300): " TOTAL_FRAMES

# --- Derived ---
FPS=$(awk "BEGIN {print 1/$GAP}")

# --- Ensure dependencies ---
if ! command -v yt-dlp &> /dev/null; then
    echo "Installing yt-dlp via Homebrew..."
    brew install yt-dlp
fi
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg via Homebrew..."
    brew install ffmpeg
fi

# --- Prepare directories ---
mkdir -p "$TRAIN_DIR"
mkdir -p "$TEST_DIR"
mkdir -p "$BASE_DIR"

# --- Find highest existing frame number ---
find_next_frame_number() {
    local max_num=0
    # Check train and test directories
    for f in "$TRAIN_DIR"/frame_*.png "$TEST_DIR"/frame_*.png; do
        if [ -f "$f" ]; then
            # Extract number from frame_XXXX.png format
            local num=$(basename "$f" | sed -E 's/frame_([0-9]+)\.png/\1/')
            # Convert to integer (removes leading zeros)
            num=$((10#$num))
            if [ "$num" -gt "$max_num" ]; then
                max_num=$num
            fi
        fi
    done
    echo $max_num
}

NEXT_FRAME_NUM=$(find_next_frame_number)
if [ "$NEXT_FRAME_NUM" -gt 0 ]; then
    echo "Found existing frames. Continuing from frame_$(printf "%04d" $((NEXT_FRAME_NUM + 1))).png"
fi

# --- Step 1: Download video safely ---
echo "Downloading video locally for stable processing..."
yt-dlp -f "best[ext=mp4]" -o "$TEMP_FILE" --no-playlist "$YT_URL"

if [ ! -f "$TEMP_FILE" ]; then
    echo "Error: Video download failed."
    exit 1
fi

# --- Step 2: Extract frames ---
echo "Extracting frames every $GAP seconds (FPS=$FPS)..."
ffmpeg -hide_banner -loglevel error -i "$TEMP_FILE" -vf "fps=$FPS" -frames:v "$TOTAL_FRAMES" -q:v 2 "$BASE_DIR/frame_%04d.png"

if [ $? -ne 0 ]; then
    echo "Frame extraction failed."
    exit 1
fi

# --- Step 3: Train/Test split with sequential numbering ---
echo "Splitting frames into train/test sets with sequential numbering..."
TOTAL=$(ls "$BASE_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ')
if [ "$TOTAL" -eq 0 ]; then
    echo "Error: No frames extracted."
    exit 1
fi
TEST_COUNT=$((TOTAL / 5))  # 20% test
COUNT=0
CURRENT_FRAME_NUM=$((NEXT_FRAME_NUM + 1))

for IMG in "$BASE_DIR"/*.png; do
    # Skip if not a frame file (safety check)
    if [ ! -f "$IMG" ]; then continue; fi
    
    NEW_NAME=$(printf "frame_%04d.png" $CURRENT_FRAME_NUM)
    if [ $COUNT -lt $TEST_COUNT ]; then
        mv "$IMG" "$TEST_DIR/$NEW_NAME"
    else
        mv "$IMG" "$TRAIN_DIR/$NEW_NAME"
    fi
    COUNT=$((COUNT + 1))
    CURRENT_FRAME_NUM=$((CURRENT_FRAME_NUM + 1))
done

# --- Step 4: Cleanup ---
rm -f "$TEMP_FILE"

# --- Summary ---
echo ""
echo "Done!"
echo "Total train images: $(ls -1 $TRAIN_DIR/*.png 2>/dev/null | wc -l | tr -d ' ')"
echo "Total test images:  $(ls -1 $TEST_DIR/*.png 2>/dev/null | wc -l | tr -d ' ')"
echo "New frames added: $COUNT"
echo "-----------------------------------------------------------"
echo "High-quality frames captured at every $GAP seconds"
echo "All frames are PNGs — full resolution"
echo "Frame numbering continues sequentially from existing frames"
echo ""
echo "Note: Run scripts/generate_dataset_info_csv.py to generate/update dataset_info.csv"
echo "-----------------------------------------------------------"
