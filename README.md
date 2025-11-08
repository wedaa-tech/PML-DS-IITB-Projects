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

- **macOS, Linux, or Windows** operating system
- Active internet connection for video download
- Approximately 2GB free disk space (for videos and extracted frames)
- Python 3.x installed

### Required Dependencies

#### System Dependencies

**macOS/Linux:**

Install the following system dependencies via Homebrew:

```bash
brew install yt-dlp ffmpeg python imagemagick
```

**Windows:**

Install the following system dependencies using one of these methods:

**Option 1: Using winget (Windows 10/11 - recommended)**
```powershell
winget install yt-dlp
winget install ffmpeg
winget install ImageMagick.ImageMagick
```

**Option 2: Using Chocolatey**
```powershell
choco install yt-dlp ffmpeg imagemagick
```

**Option 3: Manual Installation**
- **yt-dlp**: Download from https://github.com/yt-dlp/yt-dlp/releases
- **ffmpeg**: Download from https://ffmpeg.org/download.html
- **ImageMagick**: Download from https://imagemagick.org/script/download.php

Make sure all tools are added to your system PATH.

#### Python Dependencies

The following Python packages are required and will be installed via pip:

- `pillow` - Image processing
- `opencv-python` - Computer vision operations (cv2)
- `pandas` - Data manipulation and CSV handling
- `tqdm` - Progress bars

These will be automatically installed when using the setup script, or manually via:

**macOS/Linux:**
```bash
pip install pillow opencv-python pandas tqdm
```

**Windows:**
```powershell
pip install pillow opencv-python pandas tqdm
```

---

## Installation

### Clone the Repository

**macOS/Linux:**
```bash
git clone https://github.com/<your-username>/PML-DS-IITB-Projects.git
cd PML-DS-IITB-Projects/pml-ds
```

**Windows:**
```powershell
git clone https://github.com/<your-username>/PML-DS-IITB-Projects.git
cd PML-DS-IITB-Projects\pml-ds
```

### Create Python Virtual Environment (Manual Setup)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pillow opencv-python pandas tqdm
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install pillow opencv-python pandas tqdm
```

**Note:** On Windows, if you encounter an execution policy error when running PowerShell scripts, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Usage

### Step 1: Setup

First, run the setup script to install dependencies and create the Python virtual environment:

**macOS/Linux:**
```bash
cd pml-ds
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
cd pml-ds
.\setup.ps1
```

The setup script will:
- Check for required dependencies (yt-dlp, ffmpeg, python, imagemagick)
- Create and configure the Python virtual environment
- Install required Python packages (pillow, opencv-python, pandas, tqdm)

**Note for Windows users:** If you encounter execution policy restrictions, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 2: Execute Pipeline

After setup is complete, run the pipeline execution script:

**macOS/Linux:**
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

**Windows:**
```powershell
.\run_pipeline.ps1
```

The pipeline will execute the following scripts in sequence:

1. **youtube_video_to_frames.sh/.ps1** - Extract frames from YouTube video
   - When prompted, provide:
     - YouTube video URL
     - Time gap between frames (in seconds, e.g., 2)
     - Total number of frames to capture (e.g., 300)

2. **generate_dataset_info_csv.py** - Generate dataset metadata CSV

3. **split_8x8_grid_numbered.py** - Split images into 8×8 grid tiles and create overlays

4. **generate_per_frame_labels_csv.py** - Generate per-frame labels CSV

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
└── per_frame_labels.csv
```

### Step 3: Manual Step-by-Step Execution (Alternative)

If you prefer to run scripts individually:

**macOS/Linux:**
```bash
# Activate virtual environment
source venv/bin/activate

# Step 1: Extract frames from YouTube video
./scripts/youtube_video_to_frames.sh

# Step 2: Generate dataset info CSV
python scripts/generate_dataset_info_csv.py

# Step 3: Split images into 8×8 grid tiles
python scripts/split_8x8_grid_numbered.py

# Step 4: Generate per-frame labels CSV
python scripts/generate_per_frame_labels_csv.py

# Deactivate virtual environment
deactivate
```

**Windows:**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Step 1: Extract frames from YouTube video
.\scripts\youtube_video_to_frames.ps1

# Step 2: Generate dataset info CSV
python scripts\generate_dataset_info_csv.py

# Step 3: Split images into 8×8 grid tiles
python scripts\split_8x8_grid_numbered.py

# Step 4: Generate per-frame labels CSV
python scripts\generate_per_frame_labels_csv.py

# Deactivate virtual environment
deactivate
```

---

## Checking Label Distribution

After you have completed labeling your images, you can check the label distribution using the provided script:

**macOS/Linux:**
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Check label distribution
python scripts/check_label_distribution.py

# Deactivate virtual environment (optional)
deactivate
```

**Windows:**
```powershell
# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1

# Check label distribution
python scripts\check_label_distribution.py

# Deactivate virtual environment (optional)
deactivate
```

This script will analyze your labeled dataset and provide statistics about:
- Total number of labels
- Distribution of labels across different categories
- Label counts per frame/tile
- Any other relevant label statistics

## Complete Command Reference

For quick reference, here is the complete command sequence:

**macOS/Linux:**
```bash
# 1. Setup (run once)
cd pml-ds
chmod +x setup.sh
./setup.sh

# 2. Execute pipeline (run for each dataset)
chmod +x run_pipeline.sh
./run_pipeline.sh

# 3. After labeling, check label distribution
source venv/bin/activate
python scripts/check_label_distribution.py
deactivate
```

**Windows:**
```powershell
# 1. Setup (run once)
cd pml-ds
.\setup.ps1

# 2. Execute pipeline (run for each dataset)
.\run_pipeline.ps1

# 3. After labeling, check label distribution
.\venv\Scripts\Activate.ps1
python scripts\check_label_distribution.py
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
    ├── setup.sh                          # Setup script (macOS/Linux)
    ├── setup.ps1                         # Setup script (Windows)
    ├── run_pipeline.sh                   # Pipeline execution script (macOS/Linux)
    ├── run_pipeline.ps1                  # Pipeline execution script (Windows)
    └── scripts/
        ├── youtube_video_to_frames.sh           # Frame extraction script (macOS/Linux)
        ├── youtube_video_to_frames.ps1         # Frame extraction script (Windows)
        ├── generate_dataset_info_csv.py        # Dataset metadata generation
        ├── split_8x8_grid_numbered.py          # Grid tile generation script
        ├── generate_per_frame_labels_csv.py    # Per-frame labels CSV generation
        └── check_label_distribution.py         # Label distribution checker
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
