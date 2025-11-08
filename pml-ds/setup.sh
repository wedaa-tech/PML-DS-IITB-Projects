#!/bin/bash
# ===========================================================
# YouTube → Image Dataset Setup Script
# ===========================================================
# This script handles the setup and installation:
# - Installs yt-dlp, ffmpeg, python3, and imagemagick (via Homebrew)
# - Creates Python venv and installs required packages
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

# --- Make scripts executable ---
echo "Making scripts executable..."
chmod +x scripts/youtube_video_to_frames.sh
chmod +x run_pipeline.sh 2>/dev/null || true

# --- Completion summary ---
echo ""
echo "==========================================================="
echo "Setup completed successfully!"
echo "==========================================================="
echo "Next steps:"
echo "1. Run './run_pipeline.sh' to execute the dataset generation pipeline"
echo "2. After labeling, use 'python scripts/check_label_distribution.py' to check label distribution"
echo "==========================================================="
