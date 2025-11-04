#!/usr/bin/env python3
"""
generate_dataset_info_csv.py
----------------------------------------------------
Generates dataset_info.csv by scanning frames_dataset/train and frames_dataset/test
directories for PNG images.

Output CSV contains only:
- image_path: Full path to the image file
- set_type: Either "train" or "test"

The script can be run multiple times and will regenerate the CSV with current
state of the frames_dataset directory.

Author: Cordial Dude
----------------------------------------------------
"""

import os
import sys
import csv

# Determine base directory (pml-ds) regardless of where script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
BASE_DATA_DIR = os.path.join(parent_dir, "frames_dataset")
CSV_FILE = os.path.join(BASE_DATA_DIR, "dataset_info.csv")


def generate_dataset_info():
    """Generate dataset_info.csv by scanning train and test directories."""
    
    train_dir = os.path.join(BASE_DATA_DIR, "train")
    test_dir = os.path.join(BASE_DATA_DIR, "test")
    
    # Check if directories exist
    if not os.path.exists(train_dir):
        print(f"Error: Train directory not found: {train_dir}")
        sys.exit(1)
    
    if not os.path.exists(test_dir):
        print(f"Error: Test directory not found: {test_dir}")
        sys.exit(1)
    
    records = []
    
    # Process train directory
    print(f"Scanning train directory: {train_dir}")
    train_count = 0
    for img_file in sorted(os.listdir(train_dir)):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(train_dir, img_file)
            # Use relative path from BASE_DATA_DIR parent for cleaner paths
            rel_path = os.path.relpath(img_path, parent_dir)
            records.append({
                "image_path": rel_path,
                "set_type": "train"
            })
            train_count += 1
    
    # Process test directory
    print(f"Scanning test directory: {test_dir}")
    test_count = 0
    for img_file in sorted(os.listdir(test_dir)):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(test_dir, img_file)
            # Use relative path from BASE_DATA_DIR parent for cleaner paths
            rel_path = os.path.relpath(img_path, parent_dir)
            records.append({
                "image_path": rel_path,
                "set_type": "test"
            })
            test_count += 1
    
    # Write CSV file
    print(f"\nWriting dataset_info.csv: {CSV_FILE}")
    with open(CSV_FILE, mode="w", newline="") as csvfile:
        fieldnames = ["image_path", "set_type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"\nDataset info generated successfully!")
    print(f"Total train images: {train_count}")
    print(f"Total test images: {test_count}")
    print(f"Total images: {train_count + test_count}")
    print(f"CSV file: {CSV_FILE}")


if __name__ == "__main__":
    generate_dataset_info()

