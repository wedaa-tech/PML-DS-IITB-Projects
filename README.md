# PML-DS-IITB-Projects

Repository for projects and coursework completed during the Data Science diploma program at IIT Bombay.

---

## YouTube Video to Image Dataset Generator

This project automates the complete pipeline for converting YouTube videos into machine-learning-ready datasets. The workflow includes frame extraction, automatic resizing, train/test splitting, 8×8 grid tile generation, metadata export, and final ZIP packaging for model ingestion.

---

## Features

- Capture frames directly from YouTube videos with configurable intervals
- Automatic resizing of all frames to 800×600 pixels (4:3 aspect ratio)
- Automatic train/test split (80% train, 20% test)
- 8×8 grid overlay generation (64 tiles per image) with numbered visualization
- Metadata CSV export for dataset and tile information
- Final dataset packaged as ZIP archive
- Cross-platform support for macOS and Linux
- Fully automated setup and execution
- Reproducible workflow with minimal manual intervention

---

## Prerequisites

### System Requirements

- macOS or Linux operating system
- Active internet connection for video download
- Approximately 2GB free disk space (for videos and extracted frames)
- Python 3.x installed

### Required Dependencies

Install the following dependencies via Homebrew:

```bash
brew install yt-dlp ffmpeg python imagemagick
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/<your-username>/PML-DS-IITB-Projects.git
cd PML-DS-IITB-Projects/pml-ds
```

### Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install pillow
```

---

## Usage

### Method 1: Manual Step-by-Step Execution

#### Step 1: Capture Frames from YouTube Video

Make the script executable and run it:

```bash
chmod +x youtube_video_to_frames.sh
./youtube_video_to_frames.sh
```

When prompted, provide:
- YouTube video URL
- Time gap between frames (in seconds, e.g., 2)
- Total number of frames to capture (e.g., 300)

**Output Structure:**

```
frames_dataset/
├── train/
│   ├── frame_0001.png
│   ├── frame_0002.png
│   └── ...
├── test/
│   ├── frame_0241.png
│   └── ...
└── dataset_info.csv
```

#### Step 2: Generate 8×8 Grid Tiles and Overlays

Run the Python script to split images into tiles and create grid overlays:

```bash
python split_8x8_grid_numbered.py
```

**Output Structure:**

```
frames_dataset_tiles/
├── train/
│   ├── frame_0001_tiles/
│   │   ├── frame_0001_tile_01.png
│   │   ├── frame_0001_tile_02.png
│   │   ├── ...
│   │   └── frame_0001_grid_overlay.png
│   └── ...
├── test/
│   ├── frame_0241_tiles/
│   │   ├── frame_0241_tile_01.png
│   │   ├── ...
│   │   └── frame_0241_grid_overlay.png
│   └── ...
├── tiles_info.csv
└── frames_dataset_tiles.zip
```

### Method 2: Automated Setup and Execution

For a fully automated setup, use the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Check and install required dependencies (if missing)
- Create and configure the Python virtual environment
- Prompt for YouTube video URL
- Prompt for frame capture interval (e.g., every 2 seconds)
- Prompt for total number of frames to capture (e.g., 300)
- Automatically execute the entire pipeline

**Final Output:**

The script generates all required files for model training:
- Training and test image frames (800×600)
- 8×8 grid tiles for each image
- Grid overlay visualizations
- Metadata CSV files
- Complete dataset ZIP archive

---

## Complete Command Reference

For quick reference, here is the complete command sequence:

```bash
# 1. Install dependencies
brew install yt-dlp ffmpeg python imagemagick

# 2. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install pillow

# 3. Capture frames from YouTube video
chmod +x youtube_video_to_frames.sh
./youtube_video_to_frames.sh

# 4. Generate grid overlays, tiles, and ZIP archive
python split_8x8_grid_numbered.py

# 5. Deactivate virtual environment (optional)
deactivate
```

---

## Output Files

### Dataset Information (`dataset_info.csv`)

Contains metadata for each frame including:
- Image path
- Set type (train/test)
- Timestamp
- Video title
- Source URL

### Tiles Information (`tiles_info.csv`)

Contains metadata for each tile including:
- Tile path
- Set type (train/test)
- Parent image name
- Row and column position
- Tile index (1-64)

### ZIP Archive (`frames_dataset_tiles.zip`)

Complete dataset package containing:
- All training and test tiles
- Grid overlay images
- Metadata CSV files
- Ready for model training or distribution

---

## Project Structure

```
PML-DS-IITB-Projects/
├── README.md
├── LICENSE
└── pml-ds/
    ├── setup.sh                          # Automated setup script
    ├── youtube_video_to_frames.sh        # Frame extraction script
    └── split_8x8_grid_numbered.py        # Grid tile generation script
```

---

## Technical Details

### Image Specifications

- Input: YouTube video (any format supported by yt-dlp)
- Output resolution: 800×600 pixels (4:3 aspect ratio)
- Format: PNG
- Quality: High (q:v=2)

### Grid Specifications

- Grid size: 8×8 (64 tiles per image)
- Tile size: 100×75 pixels per tile
- Overlay: Semi-transparent yellow grid lines with black numbered labels

### Dataset Split

- Training set: 80% of captured frames
- Test set: 20% of captured frames
- Split is performed sequentially (first 20% to test, remainder to train)

---

## License

See LICENSE file for details.

---

## Contributing

This is a project repository for IIT Bombay Data Science diploma coursework. For questions or issues, please open an issue in the repository.
