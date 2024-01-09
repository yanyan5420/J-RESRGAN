# import needed libraries
import cv2
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
from plotly.subplots import make_subplots


def plot_part_region_spectrum(img_i, img_o, colorbar_min, colorbar_max):
    
    img_i = np.array(img_i)
    img_i = img_i / np.max(img_i)

    x_scale_1 = np.linspace(13.129, -3.560, img_i.shape[1])
    y_scale_1 = np.linspace(0.0652, -0.0652, img_i.shape[0])

    # Find the indexes corresponding to 3.2 and 4 in the x_scale array
    start_index_1 = np.argmin(np.abs(x_scale_1 - 4))
    end_index_1 = np.argmin(np.abs(x_scale_1 - 3.2))

    # Slicing the image data to the relevant part
    temp_data_1 = img_i[:, start_index_1:end_index_1]
    x_scale_1 = x_scale_1[start_index_1:end_index_1]

    heatmap1 = go.Heatmap(
                    z=temp_data_1,
                    x=x_scale_1,
                    y=y_scale_1,
                    colorscale='Jet',
                    zmin=colorbar_min,
                    zmax=colorbar_max,
                    )

    img_o = np.array(img_o)
    img_o = img_o / np.max(img_o)

    x_scale_2 = np.linspace(13.129, -3.560, img_o.shape[1])
    y_scale_2 = np.linspace(0.0652, -0.0652, img_o.shape[0])

    # Find the indexes corresponding to 1.5 and 4 in the x_scale array
    start_index_2 = np.argmin(np.abs(x_scale_2 - 4))
    end_index_2 = np.argmin(np.abs(x_scale_2 - 3.2))

    # Slicing the image data to the relevant part
    temp_data_2 = img_o[:, start_index_2:end_index_2]
    x_scale_2 = x_scale_2[start_index_2:end_index_2]

    heatmap2 = go.Heatmap(
                    z=temp_data_2,
                    x=x_scale_2,
                    y=y_scale_2,
                    colorscale='Jet',
                    zmin=colorbar_min,
                    zmax=colorbar_max,
                    )

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Input", "Output"))

    fig.add_trace(heatmap1, row=1, col=1)
    fig.add_trace(heatmap2, row=1, col=2)

    fig.update_xaxes(title_text="F2 (ppm)", row=1, col=1, autorange="reversed", tickfont=dict(size=22))
    fig.update_yaxes(title_text="F1 (ppm)", row=1, col=1, tickfont=dict(size=22))
    fig.update_xaxes(title_text="F2 (ppm)", row=1, col=2, autorange="reversed", tickfont=dict(size=22))

    fig.update_layout(
        font=dict(size=22),
    )
    fig.update_layout(
        coloraxis=dict(colorscale='Jet', cmin=colorbar_min, cmax=colorbar_max, colorbar_tickfont_size=22),
        font=dict(size=22)
    )

    fig.show()
    # return