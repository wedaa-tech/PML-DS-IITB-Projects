# PML-DS-IITB-Projects
Repository for adding projects and work while obtaining Data Science diploma with IIT-Bonmbay.


# YouTube → Image Dataset Generator & Grid Splitter

This project automates the entire pipeline of converting a **YouTube video** into a **machine-learning-ready dataset**, with clean **train/test splits**, **800×600 images**, **8×8 grid overlays**, **tile segmentation**, and a final **ZIP package** for model ingestion.

---
## Features

Capture frames directly from **YouTube videos**  
Automatically resize all frames to **800×600 (4:3 aspect ratio)**  
Split into **train (80%)** and **test (20%)** datasets  
Generate **metadata CSV** (`dataset_info.csv` and `tiles_info.csv`)  
Build **8×8 grids (64 tiles)** per image with overlays  
Export **final dataset as ZIP** (`frames_dataset_tiles.zip`)  
Fully works on **macOS and Linux**  
100% reproducible, minimal setup  

---

## Prerequisites

### System Requirements
- macOS or Linux
- Internet connection
- ~2GB disk space (for videos and extracted frames)

### Dependencies - Manual setup
Install via [Homebrew](https://brew.sh):
```bash
brew install yt-dlp ffmpeg python imagemagick


### Setup Instruction:

git clone https://github.com/<your-repo>/youtube-ml-dataset.git
cd youtube-ml-dataset

### Create a Python Virtual Environment

python3 -m venv venv
source venv/bin/activate
pip install pillow


Step 1 — Capture Frames from YouTube

chmod +x youtube_to_frames.sh
./youtube_to_frames.sh

Output:

frames_dataset/
 ├── train/
 │   ├── frame_0001.png
 │   ├── frame_0002.png
 ├── test/
 │   ├── frame_0241.png
 └── dataset_info.csv

Step 2: Build 8×8 Grid Tiles and Overlays

python split_8x8_grid_numbered_zip.py

frames_dataset_tiles/
 ├── train/
 │   ├── frame_0001_tiles/
 │   │   ├── frame_0001_tile_01.png
 │   │   ├── ...
 │   │   ├── frame_0001_grid_overlay.png
 ├── test/
 │   ├── frame_0241_tiles/
 │   │   ├── frame_0241_tile_01.png
 │   │   ├── ...
 │   │   ├── frame_0241_grid_overlay.png
 ├── tiles_info.csv
frames_dataset_tiles.zip



Full Command Summary:

# 1. Install dependencies
    brew install yt-dlp ffmpeg python imagemagick

# 2. Create environment
    python3 -m venv venv
    source venv/bin/activate
    pip install pillow

# 3. Capture frames from YouTube
    chmod +x youtube_to_frames.sh
    ./youtube_to_frames.sh

# 4. Build grid overlays, tiles, and zip dataset
    python split_8x8_grid_numbered_zip.py

# 5. Deactivate environment (optional)
    deactivate



Optional: To run entire setup with one file execution

Setting up project with setup.sh: Automatic setup

chmod +x setup.sh

./setup.sh

User will be guided interactively to:

    Enter YouTube video URL

    Choose frame interval (e.g., every 2 seconds)

    Choose total frames (e.g., 300)

Output:
Required files to be used for model training.

