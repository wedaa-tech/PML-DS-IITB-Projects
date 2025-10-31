"""
Grid splitting utilities for image processing.
"""

import numpy as np


def split_image_into_grid(img: np.ndarray, cols: int = 8, rows: int = 8) -> list:
    """
    Split an image into a grid of tiles.
    
    Args:
        img: Image as numpy array in RGB format (H, W, 3)
        cols: Number of columns in the grid (default: 8)
        rows: Number of rows in the grid (default: 8)
        
    Returns:
        List of tile images as numpy arrays in RGB format
    """
    h, w = img.shape[:2]
    tile_h = h // rows
    tile_w = w // cols
    
    tiles = []
    for r in range(rows):
        for c in range(cols):
            y_start = r * tile_h
            y_end = y_start + tile_h
            x_start = c * tile_w
            x_end = x_start + tile_w
            
            tile = img[y_start:y_end, x_start:x_end]
            tiles.append(tile)
    
    return tiles

