"""
Utility functions for image processing and file operations.
"""

import os
import cv2
import numpy as np


def read_image(img_path: str) -> np.ndarray:
    """
    Read an image file and return it as a numpy array in RGB format.
    
    Args:
        img_path: Path to the image file
        
    Returns:
        numpy array of the image in RGB format (H, W, 3)
    """
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Failed to read image from {img_path}")
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def ensure_dir(dir_path: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        dir_path: Path to the directory
    """
    os.makedirs(dir_path, exist_ok=True)

