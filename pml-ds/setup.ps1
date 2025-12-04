# ===========================================================
# YouTube → Image Dataset Setup Script (Windows)
# ===========================================================
# This script handles the setup and installation:
# - Checks for required dependencies (yt-dlp, ffmpeg, python3, imagemagick)
# - Creates Python venv and installs required packages
# ===========================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================="
Write-Host "YouTube → Image Dataset Setup (Windows)"
Write-Host "==========================================================="
Write-Host ""

# --- Check if Python is installed ---
Write-Host "Checking for Python..."
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion"
} catch {
    Write-Host "Error: Python is not installed or not in PATH."
    Write-Host "Please install Python 3.x from https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation."
    exit 1
}

# --- Check for required dependencies ---
Write-Host ""
Write-Host "Checking for required dependencies..."

$missingDeps = @()

# Check yt-dlp
try {
    $null = Get-Command yt-dlp -ErrorAction Stop
    Write-Host "✓ yt-dlp found"
} catch {
    Write-Host "✗ yt-dlp not found"
    $missingDeps += "yt-dlp"
}

# Check ffmpeg
try {
    $null = Get-Command ffmpeg -ErrorAction Stop
    Write-Host "✓ ffmpeg found"
} catch {
    Write-Host "✗ ffmpeg not found"
    $missingDeps += "ffmpeg"
}

# Check imagemagick
try {
    $null = Get-Command magick -ErrorAction Stop
    Write-Host "✓ ImageMagick found"
} catch {
    Write-Host "✗ ImageMagick not found"
    $missingDeps += "imagemagick"
}

# --- Install missing dependencies ---
if ($missingDeps.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing dependencies detected: $($missingDeps -join ', ')"
    Write-Host ""
    Write-Host "Please install missing dependencies using one of the following methods:"
    Write-Host ""
    Write-Host "Option 1: Using Chocolatey (recommended)"
    Write-Host "  Install Chocolatey from https://chocolatey.org/install"
    Write-Host "  Then run: choco install $($missingDeps -join ' ')"
    Write-Host ""
    Write-Host "Option 2: Using winget (Windows 10/11)"
    Write-Host "  winget install yt-dlp"
    Write-Host "  winget install ffmpeg"
    Write-Host "  winget install ImageMagick.ImageMagick"
    Write-Host ""
    Write-Host "Option 3: Manual installation"
    Write-Host "  - yt-dlp: https://github.com/yt-dlp/yt-dlp/releases"
    Write-Host "  - ffmpeg: https://ffmpeg.org/download.html"
    Write-Host "  - ImageMagick: https://imagemagick.org/script/download.php"
    Write-Host ""
    $continue = Read-Host "Continue with setup anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# --- Setup Python virtual environment ---
Write-Host ""
Write-Host "Setting up Python virtual environment..."
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
} else {
    Write-Host "Python virtual environment already exists."
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

# --- Install Python packages ---
Write-Host ""
Write-Host "Installing Python packages..."
python -m pip install --upgrade pip

$packages = @("pillow", "opencv-python", "pandas", "tqdm", "ultralytics")
foreach ($package in $packages) {
    Write-Host "Installing $package..."
    python -m pip install $package
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Python packages"
    exit 1
}

Write-Host ""
Write-Host "Python packages installed successfully."

# --- Completion summary ---
Write-Host ""
Write-Host "==========================================================="
Write-Host "Setup completed successfully!"
Write-Host "==========================================================="
Write-Host "Next steps:"
Write-Host "1. Run '.\run_pipeline.ps1' to execute the dataset generation pipeline"
Write-Host "2. After labeling, use 'python scripts\check_label_distribution.py' to check label distribution"
Write-Host "==========================================================="

