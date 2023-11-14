import pandas as pd
import numpy as np
from scipy.stats import truncnorm
import json
import pathlib
from pathlib import Path
import glob
import os
import cv2
import nmrglue as ng
import plotly
from basicsr.utils import FileClient, imfrombytes, img2tensor
import plotly.express as px
from scipy.ndimage import gaussian_filter


from PIL import Image
import os

def check_images_in_folder(folder_path):
    # List all files in the directory
    files = os.listdir(folder_path)

    # Filter for tif images
    tif_files = [f for f in files if f.lower().endswith('.tif') or f.lower().endswith('.tiff')]

    for tif_file in tif_files:
        file_path = os.path.join(folder_path, tif_file)
        # print(file_path)
        img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if img is None or img.size == (0, 0) or np.max(img) == 0:
            print(f"Image {tif_file} seems to be None or corrupted.")

        # try:
        #     with Image.open(file_path) as img:
        #         # Check if image is None or empty
        #         if img is None or img.size == (0, 0):
        #             print(f"Image {tif_file} seems to be None or corrupted.")
        # except Exception as e:
        #     print(f"Error reading image {tif_file}. Error: {e}")

# Use the function
folder_path = 'datasets/DF2K/JRES_train_sigma_07_LR/'
check_images_in_folder(folder_path)