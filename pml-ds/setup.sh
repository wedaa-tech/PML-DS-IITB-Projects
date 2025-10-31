#!/bin/bash
# ===========================================================
# YouTube → Image Dataset Full Setup & Execution Script
# ===========================================================
# This script:
# Installs yt-dlp, ffmpeg, python3, and imagemagick (via Homebrew)
# Creates Python venv and installs Pillow
# Runs youtube_to_frames.sh to capture video frames
# Runs split_8x8_grid_numbered_zip.py to generate 8×8 tiles & ZIP
# ===========================================================

set -e  # Exit immediately on error

# --- Check if Homebrew is installed ---
if ! command -v brew &> /dev/null; then
  echo "Homebrew not found! Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew found."
fi

# --- Install dependencies ---
echo "Installing required packages..."
brew install yt-dlp ffmpeg python imagemagick || true

# --- Setup Python virtual environment ---
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
else
  echo "Python virtual environment already exists."
fi

# --- Activate venv ---
echo "Activating Python environment..."
source venv/bin/activate

# --- Install Python packages ---
echo "Installing Python packages..."
pip install --upgrade pip

# Install required packages
pip install pillow opencv-python pandas tqdm || {
  echo "Error: Failed to install Python packages"
  exit 1
}

echo "Python packages installed successfully."

# --- Verify required scripts ---
if [ ! -f "youtube_to_frames.sh" ]; then
  echo "Missing youtube_to_frames.sh! Please ensure it's in the current folder."
  exit 1
fi

if [ ! -f "split_8x8_grid_numbered_zip.py" ]; then
  echo "Missing split_8x8_grid_numbered_zip.py! Please ensure it's in the current folder."
  exit 1
fi

# --- Make shell script executable ---
chmod +x youtube_to_frames.sh

# --- Run the pipeline ---
echo "Starting YouTube frame capture..."
./youtube_to_frames.sh

echo "Building 8x8 grid overlays, tiles, and zipped dataset..."
python split_8x8_grid_numbered_zip.py

# --- Deactivate environment ---
deactivate

# --- Completion summary ---
echo " All steps completed successfully!"
echo "-----------------------------------------------------------"
echo " Final Output:"
echo " - frames_dataset/train → Training frames (800×600)"
echo " - frames_dataset/test  → Test frames (800×600)"
echo " - frames_dataset_tiles/ → 8x8 grid tiles + overlays"
echo " - frames_dataset_tiles.zip → Final zipped dataset"
echo "-----------------------------------------------------------"
echo " You’re ready to use your dataset for model training!"
echo "-----------------------------------------------------------"
