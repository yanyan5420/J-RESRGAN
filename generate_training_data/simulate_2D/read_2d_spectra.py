import nmrglue as ng
import pandas as pd
import numpy as np
from pathlib import Path
import os
import glob
import pathlib


def read_2d_data(file_path):
    base_path = pathlib.Path(__file__).resolve().parents[1]
    data_path = base_path.joinpath(file_path)

    new_path = Path(data_path)
    dir_list = glob.glob(os.path.join(new_path, '*'))

    data_dict = dict()
    for sub_dir in dir_list:
        meta_name = str(sub_dir).split("/")[-1]
        dic, data = ng.bruker.read_pdata(sub_dir, shape=(257, 16384))
        data[-1, :] = data[0, :]
        data_dict[meta_name] = data

    x_scale = np.linspace(13.129, -3.560, 16384)
    y_scale = np.linspace(0.0652, -0.0652, 257)

    return data_dict, x_scale, y_scale
