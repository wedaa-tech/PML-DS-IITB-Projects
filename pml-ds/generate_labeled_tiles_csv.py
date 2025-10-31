#!/usr/bin/env python3
"""
Wrapper script to run generate_labeled_tiles_csv.py from the pml-ds directory.
This script simply executes the main script located in the scripts/ subdirectory.
"""

import os
import sys
import subprocess

# Get the directory where this script is located (pml-ds)
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(script_dir, "scripts")
main_script = os.path.join(scripts_dir, "generate_per_frame_labels_csv.py")

# Check if the main script exists
if not os.path.exists(main_script):
    print(f"Error: Could not find {main_script}")
    sys.exit(1)

# Execute the main script with all arguments passed through
sys.exit(subprocess.run([sys.executable, main_script] + sys.argv[1:]).returncode)

