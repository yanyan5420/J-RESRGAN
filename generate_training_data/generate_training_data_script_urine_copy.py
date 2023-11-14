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

# from simulate_2D.read_2d_spectra import read_2d_data
from simulate_2D.match_names import format_input_mixture, format_data_names
from simulate_2D.preprocess_2d_spectra import remove_water_calibration, filter_noise, smooth_data, normalize_data


def read_2d_data(file_path):
    base_path = pathlib.Path(__file__).resolve().parents[1]
    data_path = base_path.joinpath(file_path)

    new_path = Path(data_path)
    dir_list = glob.glob(os.path.join(new_path, '*'))

    data_dict = dict()
    for sub_dir in dir_list:
        meta_name = str(sub_dir).split("/")[-1]
        dic, data = ng.bruker.read_pdata(sub_dir, shape=(256, 16384))
        # data[-1, :] = data[0, :]
        data_dict[meta_name] = data

    x_scale = np.linspace(13.129, -3.560, 16384)
    y_scale = np.linspace(0.0652, -0.0652, 256)

    return data_dict, x_scale, y_scale

####
# 1. read metabolites (urine only, excluding l-malic acid, glycolic acid)
base_path = pathlib.Path(__file__).resolve().parents[1]
meta_list = []
with open(base_path.joinpath("/data/DL_JRes_NMR/Real-ESRGAN/generate_training_data/Input/urine_mixture.txt")) as file:
    for line in file.readlines():
        meta_list.append(line.strip("\n"))
format_meta_list = format_input_mixture(meta_list)
# print(len(format_meta_list))
# print(format_meta_list)

####
# 2. read and preprocess spectra
data_dict, x_scale, y_scale = read_2d_data("/data/DL_JRes_NMR/Real-ESRGAN/generate_training_data/Input/New_DB_2D/")
format_data_dict = format_data_names(data_dict)
meta_spectra_dict = dict()
for meta in format_meta_list:
    meta_spectra_dict[meta] = format_data_dict[meta]

removed_data_dict = remove_water_calibration(meta_spectra_dict, x_scale, y_scale, [4.5, 5.0], [-0.3, 0.3])
filtered_data_dict = filter_noise(removed_data_dict, 0.05)
smooth_data_dict = smooth_data(filtered_data_dict, 3, 3)
norm_data_dict = normalize_data(smooth_data_dict)
# print(norm_data_dict["creatinine"])

####
# 3. read concentrations
cons_df = pd.read_csv(base_path.joinpath("/data/DL_JRes_NMR/Real-ESRGAN/generate_training_data/Input/hmdb_modified_urine_cons.csv"), index_col=0)
urine_meta_cons_df = cons_df.loc[format_meta_list, ["Mean (uM)", "Std (uM)"]]
urine_meta_cons_df = urine_meta_cons_df.sort_values(by="Mean (uM)", ascending=False)
# urine_meta_cons_df.to_csv("urine_metabolites_concentrations.csv")
# print(urine_meta_cons_df)
# print(urine_meta_cons_df.shape)
# print(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] < 50].shape)
# print(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] > 1000].shape)

####
# N=40, 25, 15, 6, 34
# 4. sample concentrations
meta_list_40 = list(urine_meta_cons_df.index)
# meta_list_25 = list(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] > 100].index)
meta_list_15 = list(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] <= 100].index)
meta_list_8 = list(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] <= 50].index)
meta_list_6 = list(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] > 1000].index)
meta_list_34 = list(urine_meta_cons_df[urine_meta_cons_df["Mean (uM)"] <= 1000].index)


def meta_sample_cons(meta_name, meta_cons_df, sample_size):
    mean = meta_cons_df.loc[meta_name, "Mean (uM)"]
    std = meta_cons_df.loc[meta_name, "Std (uM)"]
    meta_trunc_dist = truncnorm(a=(0-mean)/std, b=np.infty, loc=mean, scale=std)
    sampled_cons_list = meta_trunc_dist.rvs(size=sample_size)
    if np.all(sampled_cons_list):
        return sampled_cons_list
    else:
        return meta_sample_cons(meta_name, meta_cons_df, sample_size)
    # return [np.round(ele, 2) for ele in sampled_cons_list]

####
# 5. construct mixture spectra


def sum_mixture_spectra(n, mixture_list, whole_meta_spectra_dict, whole_cons_df):
    sum_data = 0
    for meta_name in mixture_list:
        temp_cons = whole_cons_df.loc[meta_name, n]
        temp_protons = 1
        temp_data = np.array(whole_meta_spectra_dict[meta_name])
        temp_intensity = temp_data * temp_cons * temp_protons
        sum_data = sum_data + temp_intensity
    return sum_data


def scale_HR_to_0_256(im):
    if np.max(im) < 256:
        scale_size = 255 // np.max(im)
        scale_im = im * scale_size
    else:
        scale_size = np.max(im) / 255
        scale_im = im / scale_size
    return scale_im


def scale_HR_to_0_1(im):
    scaled_im = (im - np.min(im)) / (np.max(im) - np.min(im))
    return scaled_im

# (data-np.min(data))/(np.max(data)-np.min(data))

def add_gaussian_filter(mix_arr, sigma):
    add_noise_arr = gaussian_filter(np.array(mix_arr), sigma)
    return add_noise_arr


def bicubic_down_sampling(mix_arr, scale_factor):
    img_resized = cv2.resize(mix_arr, (0, 0), fx=1 / scale_factor, fy=1 / scale_factor, interpolation=cv2.INTER_CUBIC)
    return img_resized


def area_down_sampling(mix_arr, scale_factor):
    img_resized = cv2.resize(mix_arr, (0, 0), fx=1 / scale_factor, fy=1 / scale_factor, interpolation=cv2.INTER_AREA)
    return img_resized


def generate_mixture_spectra(meta_name_list, meta_cons_df, whole_meta_spectra_dict, sample_size, filename):
    meta_cons_dict = dict()
    for meta_name in meta_name_list:
        sampled_cons_list = meta_sample_cons(meta_name, meta_cons_df, sample_size)
        meta_cons_dict[meta_name] = sampled_cons_list
    whole_cons_df = pd.DataFrame.from_dict(meta_cons_dict, orient='index')

    # mix_meta_list = []
    for i in range(whole_cons_df.shape[1]):
        mix_meta = sum_mixture_spectra(i, meta_name_list, whole_meta_spectra_dict, whole_cons_df)
        scaled_im = scale_HR_to_0_256(mix_meta)
        # scaled_im = scale_HR_to_0_1(mix_meta)

        image_lr = add_gaussian_filter(scaled_im, sigma=(0, 7))
        image_lr_ds = area_down_sampling(image_lr, 2)

        cv2.imwrite("/data/DL_JRes_NMR/Real-ESRGAN/datasets/DF2K/JRES_train_sigma_07_HR/" + filename + '_' +
                    '{0}'.format(str(i+1).zfill(4)) + ".tif", scaled_im)
        cv2.imwrite("/data/DL_JRes_NMR/Real-ESRGAN/datasets/DF2K/JRES_train_sigma_07_LR/" + filename + '_' +
                    '{0}'.format(str(i+1).zfill(4))+".tif", image_lr_ds)

        print("finish "+str(i), filename, np.max(scaled_im), np.min(scaled_im), 
              np.max(image_lr_ds), np.min(image_lr_ds))

    # print(mix_meta.shape)
    return


generate_mixture_spectra(meta_list_6, urine_meta_cons_df, norm_data_dict, 1000, "mix_6")
generate_mixture_spectra(meta_list_8, urine_meta_cons_df, norm_data_dict, 1000, "mix_8")
generate_mixture_spectra(meta_list_15, urine_meta_cons_df, norm_data_dict, 1000, "mix_15")
generate_mixture_spectra(meta_list_34, urine_meta_cons_df, norm_data_dict, 1000, "mix_34")
generate_mixture_spectra(meta_list_40, urine_meta_cons_df, norm_data_dict, 1000, "mix_40")

