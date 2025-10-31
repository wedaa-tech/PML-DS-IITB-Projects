#!/bin/bash
# ===========================================================
# 🎞️  YouTube → ML Dataset Generator (High Quality + Metadata)
# Author: ChatGPT (Cordial Dude edition)
# ===========================================================
# Features:
# ✅ Stable (downloads video before processing)
# ✅ Captures frames at user-defined interval
# ✅ High quality (q:v=2)
# ✅ Creates train/test split
# ✅ Auto-generates dataset_info.csv with metadata
# ===========================================================

# --- Config ---
BASE_DIR="frames_dataset"
TRAIN_DIR="$BASE_DIR/train"
TEST_DIR="$BASE_DIR/test"
TEMP_FILE="temp_youtube_video.mp4"
CSV_FILE="$BASE_DIR/dataset_info.csv"

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

# --- Step 1: Download video safely ---
echo "⬇️  Downloading video locally for stable processing..."
yt-dlp -f "best[ext=mp4]" -o "$TEMP_FILE" --no-playlist "$YT_URL"

if [ ! -f "$TEMP_FILE" ]; then
    echo "❌ Error: Video download failed."
    exit 1
fi

# --- Step 2: Extract frames ---
echo "🎥 Extracting frames every $GAP seconds (FPS=$FPS)..."
ffmpeg -hide_banner -loglevel error -i "$TEMP_FILE" -vf "fps=$FPS" -frames:v "$TOTAL_FRAMES" -q:v 2 "$BASE_DIR/frame_%04d.png"

if [ $? -ne 0 ]; then
    echo "❌ Frame extraction failed."
    exit 1
fi

# --- Step 3: Train/Test split ---
echo "📂 Splitting frames into train/test sets..."
TOTAL=$(ls "$BASE_DIR"/*.png | wc -l | tr -d ' ')
TEST_COUNT=$((TOTAL / 5))  # 20% test
COUNT=0

for IMG in "$BASE_DIR"/*.png; do
    if [ $COUNT -lt $TEST_COUNT ]; then
        mv "$IMG" "$TEST_DIR/"
    else
        mv "$IMG" "$TRAIN_DIR/"
    fi
    COUNT=$((COUNT + 1))
done

# --- Step 4: Generate dataset_info.csv ---
echo "🧾 Generating dataset_info.csv..."

VIDEO_TITLE=$(yt-dlp --get-title "$YT_URL")
DATE_CAPTURED=$(date "+%Y-%m-%d %H:%M:%S")

echo "image_path,set_type,timestamp,video_title,source_url" > "$CSV_FILE"

for IMG in "$TRAIN_DIR"/*.png; do
    echo "$IMG,train,$DATE_CAPTURED,\"$VIDEO_TITLE\",$YT_URL" >> "$CSV_FILE"
done
for IMG in "$TEST_DIR"/*.png; do
    echo "$IMG,test,$DATE_CAPTURED,\"$VIDEO_TITLE\",$YT_URL" >> "$CSV_FILE"
done

# --- Step 5: Cleanup ---
rm -f "$TEMP_FILE"

# --- Summary ---
echo "✅ Done!"
echo "📊 Metadata file: $CSV_FILE"
echo "📁 Train images: $(ls -1 $TRAIN_DIR | wc -l)"
echo "📁 Test images:  $(ls -1 $TEST_DIR | wc -l)"
echo "-----------------------------------------------------------"
echo "🎯 High-quality frames captured at every $GAP seconds"
echo "🖼️ All frames are PNGs — full resolution"
echo "📘 CSV file includes paths, timestamps, and source info"
echo "-----------------------------------------------------------"
