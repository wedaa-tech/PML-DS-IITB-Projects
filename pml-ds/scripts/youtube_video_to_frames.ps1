# ===========================================================
# YouTube → ML Dataset Generator (High Quality + Metadata) - Windows
# ===========================================================
# Features:
# - Stable (downloads video before processing)
# - Captures frames at user-defined interval
# - High quality (q:v=2)
# - Creates train/test split
# - Safe reruns - appends new frames without overwriting existing ones
# - Sequential frame numbering continues from existing frames
# ===========================================================

$ErrorActionPreference = "Stop"

# --- Config ---
$BASE_DIR = "frames_dataset"
$TRAIN_DIR = Join-Path $BASE_DIR "train"
$TEST_DIR = Join-Path $BASE_DIR "test"
$TEMP_FILE = "temp_youtube_video.mp4"

# --- User Inputs ---
$YT_URL = Read-Host "Enter YouTube video URL"
$GAP = Read-Host "Enter time gap between frames (in seconds, e.g. 2)"
$TOTAL_FRAMES = Read-Host "Enter total number of frames to capture (e.g. 300)"

# Convert to numbers
try {
    $GAP = [double]$GAP
    $TOTAL_FRAMES = [int]$TOTAL_FRAMES
} catch {
    Write-Host "Error: Invalid input. Please enter numeric values."
    exit 1
}

# --- Derived ---
$FPS = 1.0 / $GAP

# --- Ensure dependencies ---
if (-not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
    Write-Host "Error: yt-dlp is not installed or not in PATH."
    Write-Host "Please install yt-dlp using:"
    Write-Host "  winget install yt-dlp"
    Write-Host "  or"
    Write-Host "  choco install yt-dlp"
    exit 1
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "Error: ffmpeg is not installed or not in PATH."
    Write-Host "Please install ffmpeg using:"
    Write-Host "  winget install ffmpeg"
    Write-Host "  or"
    Write-Host "  choco install ffmpeg"
    exit 1
}

# --- Prepare directories ---
New-Item -ItemType Directory -Force -Path $TRAIN_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $TEST_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $BASE_DIR | Out-Null

# --- Find highest existing frame number ---
function Find-NextFrameNumber {
    $maxNum = 0
    $pattern = "frame_(\d+)\.png"
    
    # Check train and test directories
    $allFrames = Get-ChildItem -Path $TRAIN_DIR, $TEST_DIR -Filter "frame_*.png" -ErrorAction SilentlyContinue
    
    foreach ($file in $allFrames) {
        if ($file.Name -match $pattern) {
            $num = [int]$matches[1]
            if ($num -gt $maxNum) {
                $maxNum = $num
            }
        }
    }
    
    return $maxNum
}

$NEXT_FRAME_NUM = Find-NextFrameNumber
if ($NEXT_FRAME_NUM -gt 0) {
    $nextFrameName = "frame_{0:D4}.png" -f ($NEXT_FRAME_NUM + 1)
    Write-Host "Found existing frames. Continuing from $nextFrameName"
}

# --- Step 1: Download video safely ---
Write-Host "Downloading video locally for stable processing..."
& yt-dlp -f "best[ext=mp4]" -o $TEMP_FILE --no-playlist $YT_URL

if (-not (Test-Path $TEMP_FILE)) {
    Write-Host "Error: Video download failed."
    exit 1
}

# --- Step 2: Extract frames ---
Write-Host "Extracting frames every $GAP seconds (FPS=$FPS)..."
$outputPattern = Join-Path $BASE_DIR "frame_%04d.png"
& ffmpeg -hide_banner -loglevel error -i $TEMP_FILE -vf "fps=$FPS" -frames:v $TOTAL_FRAMES -q:v 2 $outputPattern

if ($LASTEXITCODE -ne 0) {
    Write-Host "Frame extraction failed."
    Remove-Item $TEMP_FILE -ErrorAction SilentlyContinue
    exit 1
}

# --- Step 3: Train/Test split with sequential numbering ---
Write-Host "Splitting frames into train/test sets with sequential numbering..."
$extractedFrames = Get-ChildItem -Path $BASE_DIR -Filter "frame_*.png" | Where-Object { $_.Name -match "^frame_\d+\.png$" }
$TOTAL = $extractedFrames.Count

if ($TOTAL -eq 0) {
    Write-Host "Error: No frames extracted."
    Remove-Item $TEMP_FILE -ErrorAction SilentlyContinue
    exit 1
}

$TEST_COUNT = [Math]::Floor($TOTAL / 5)  # 20% test
$COUNT = 0
$CURRENT_FRAME_NUM = $NEXT_FRAME_NUM + 1

foreach ($IMG in $extractedFrames) {
    $NEW_NAME = "frame_{0:D4}.png" -f $CURRENT_FRAME_NUM
    
    if ($COUNT -lt $TEST_COUNT) {
        Move-Item -Path $IMG.FullName -Destination (Join-Path $TEST_DIR $NEW_NAME) -Force
    } else {
        Move-Item -Path $IMG.FullName -Destination (Join-Path $TRAIN_DIR $NEW_NAME) -Force
    }
    
    $COUNT++
    $CURRENT_FRAME_NUM++
}

# --- Step 4: Cleanup ---
Remove-Item $TEMP_FILE -ErrorAction SilentlyContinue

# --- Summary ---
$trainCount = (Get-ChildItem -Path $TRAIN_DIR -Filter "*.png" -ErrorAction SilentlyContinue).Count
$testCount = (Get-ChildItem -Path $TEST_DIR -Filter "*.png" -ErrorAction SilentlyContinue).Count

Write-Host ""
Write-Host "Done!"
Write-Host "Total train images: $trainCount"
Write-Host "Total test images:  $testCount"
Write-Host "New frames added: $COUNT"
Write-Host "-----------------------------------------------------------"
Write-Host "High-quality frames captured at every $GAP seconds"
Write-Host "All frames are PNGs — full resolution"
Write-Host "Frame numbering continues sequentially from existing frames"
Write-Host ""
Write-Host "Note: Run scripts\generate_dataset_info_csv.py to generate/update dataset_info.csv"
Write-Host "-----------------------------------------------------------"

