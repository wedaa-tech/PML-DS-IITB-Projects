# ===========================================================
# YouTube → Image Dataset Pipeline Execution Script (Windows)
# ===========================================================
# This script executes the complete pipeline in sequence:
# 1. youtube_video_to_frames.ps1 - Extract frames from YouTube video
# 2. generate_dataset_info_csv.py - Generate dataset metadata CSV
# 3. split_8x8_grid_numbered.py - Split images into 8x8 grid tiles
# 4. generate_per_frame_labels_csv.py - Generate per-frame labels CSV
# ===========================================================

$ErrorActionPreference = "Stop"

# --- Check if virtual environment exists ---
if (-not (Test-Path "venv")) {
    Write-Host "Error: Virtual environment not found!"
    Write-Host "Please run '.\setup.ps1' first to set up the environment."
    exit 1
}

# --- Activate venv ---
Write-Host "Activating Python environment..."
$activateScript = "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "Error: Could not find virtual environment activation script."
    exit 1
}

# --- Verify required scripts exist ---
Write-Host "Verifying required scripts..."

$requiredScripts = @(
    "scripts\youtube_video_to_frames.ps1",
    "scripts\generate_dataset_info_csv.py",
    "scripts\split_8x8_grid_numbered.py",
    "scripts\generate_per_frame_labels_csv.py"
)

foreach ($script in $requiredScripts) {
    if (-not (Test-Path $script)) {
        Write-Host "Error: Missing $script!"
        exit 1
    }
}

# --- Step 1: Extract frames from YouTube video ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Step 1: Extracting frames from YouTube video"
Write-Host "==========================================================="
& "scripts\youtube_video_to_frames.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Frame extraction failed."
    exit 1
}

# --- Step 2: Generate dataset info CSV ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Step 2: Generating dataset info CSV"
Write-Host "==========================================================="
python scripts\generate_dataset_info_csv.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Dataset info CSV generation failed."
    exit 1
}

# --- Step 3: Split images into 8x8 grid tiles ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Step 3: Splitting images into 8x8 grid tiles"
Write-Host "==========================================================="
python scripts\split_8x8_grid_numbered.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Grid tile generation failed."
    exit 1
}

# --- Step 4: Generate per-frame labels CSV ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Step 4: Generating per-frame labels CSV"
Write-Host "==========================================================="
python scripts\generate_per_frame_labels_csv.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Per-frame labels CSV generation failed."
    exit 1
}

# --- Completion summary ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Pipeline execution completed successfully!"
Write-Host "==========================================================="
Write-Host "Output generated:"
Write-Host " - frames_dataset\train → Training frames (800×600)"
Write-Host " - frames_dataset\test  → Test frames (800×600)"
Write-Host " - frames_dataset_tiles\ → 8x8 grid tiles + overlays"
Write-Host " - dataset_info.csv → Dataset metadata"
Write-Host " - per_frame_labels.csv → Per-frame labels"
Write-Host "==========================================================="
Write-Host "Next steps:"
Write-Host "1. Label your images/tiles as needed"
Write-Host "2. Run 'python scripts\check_label_distribution.py' to check label distribution"
Write-Host "==========================================================="

