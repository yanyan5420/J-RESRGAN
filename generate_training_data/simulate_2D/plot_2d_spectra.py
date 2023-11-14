import plotly.graph_objects as go
import numpy as np


def plot_jres_spectra(final_data_dict, repli_name, x_scale, y_scale, temp_levels):
    fig = go.Figure()
    config = dict({'scrollZoom': True})

    temp_data = np.array(final_data_dict[repli_name])
    # # min_level = np.min(temp_data[np.nonzero(temp_data)])
    # max_level = np.max(temp_data)
    # len_data = len(temp_data[np.nonzero(temp_data)])
    # start_level = sorted(temp_data[np.nonzero(temp_data)])[len_data//3]
    # levels = np.linspace(start_level, max_level, 10)
    # step = levels[1] - levels[0]
    start_level = temp_levels[0]
    end_level = temp_levels[-1]
    levels = np.linspace(start_level, end_level, 10)
    step = levels[1] - levels[0]
    print(start_level, end_level, step)

    fig.add_trace(
        go.Contour(
            x=x_scale,
            y=y_scale,
            z=temp_data,
            contours_coloring='lines',
            line_width=2,
            # line=dict(contours_coloring='lines', line_width=2),
            contours=dict(
                start=start_level,
                end=end_level,
                size=step,
            ),

        )
    )
    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="Hz")
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        height=500,
        title_text="JRes of "+repli_name,
        template="plotly_white"
    )
    return fig


def plot_stacked_spectra(p_jres_dict, x_scale, v_space):
    fig = go.Figure()
    config = dict({'scrollZoom': True})
    v = 0
    for repli_name, p_jres_scale in p_jres_dict.items():
        fig.add_trace(go.Scatter(
            x=x_scale,
            y=p_jres_scale + v,
            name=repli_name,
            hovertext=tuple(zip(x_scale, p_jres_scale)),
            hoverinfo="text",
        ))
        v = v + v_space

    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="intensity")
    fig.update_yaxes(tickvals=[])

    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        title_text="Projection of JRes for all replicates in the group",
        template="plotly_white",
        height=500,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            itemclick="toggleothers",
            itemdoubleclick="toggle"
        )
    )
    return fig


def plot_2d_spectra(select_meta_name, processed_data_dict, x_scale, y_scale):
    fig = go.Figure()
    config = dict({'scrollZoom': True})

    temp_data = np.array(processed_data_dict[select_meta_name])
    max_level = np.max(temp_data)
    print(max_level)

    len_data = len(temp_data[np.nonzero(temp_data)])
    start_level = 0
        # sorted(temp_data[np.nonzero(temp_data)])[len_data // 3]
    levels = np.linspace(start_level, max_level, 10)
    step = levels[1] - levels[0]

    fig.add_trace(
        go.Contour(
            x=x_scale,
            y=y_scale,
            z=temp_data,
            contours_coloring='lines',
            line_width=2,
            # line=dict(contours_coloring='lines', line_width=2),
            contours=dict(
                start=0,
                end=max_level,
                size=step,
            ),

        )
    )
    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="Hz")
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        height=500,
        title_text="JRes of " + select_meta_name,
        template="plotly_white"
    )
    return fig


def plot_jres_spectra_peak_shift_page(final_data_dict, repli_name, x_scale, y_scale, temp_levels):
    fig = go.Figure()
    config = dict({'scrollZoom': True})

    if repli_name == "replicate_mean":
        temp_data = np.array(final_data_dict[repli_name])
    else:
        str_ph, data = final_data_dict[repli_name]
        temp_data = np.array(data)
        print(str_ph)

    print(repli_name)

    start_level = temp_levels[0]
    end_level = temp_levels[-1]
    levels = np.linspace(start_level, end_level, 10)
    step = levels[1] - levels[0]
    print(start_level, end_level, step)

    fig.add_trace(
        go.Contour(
            x=x_scale,
            y=y_scale,
            z=temp_data,
            contours_coloring='lines',
            line_width=2,
            # line=dict(contours_coloring='lines', line_width=2),
            contours=dict(
                start=start_level,
                end=end_level,
                size=step,
            ),

        )
    )
    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="Hz")
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        height=500,
        title_text="JRes of "+repli_name,
        template="plotly_white"
    )
    return fig


def plot_stacked_spectra_with_ph(shift_p_jres_dict, x_scale, v_space):
    fig = go.Figure()
    config = dict({'scrollZoom': True})
    v = 0
    annotations = []
    for repli_name, [str_ph, p_jres_scale] in shift_p_jres_dict.items():
        temp_ph = round(float(str_ph), 3)
        fig.add_trace(go.Scatter(
            x=x_scale,
            y=p_jres_scale + v,
            name=repli_name + ", " + "pH=" + str(temp_ph),
            hovertext=tuple(zip(x_scale, p_jres_scale)),
            hoverinfo="text",
        ))
        # add labels for each line
        annotations.append(dict(xref="paper", x=1.0, y=0 + v,
                                xanchor="left", yanchor="middle",
                                text="pH=" + str(temp_ph),
                                font=dict(family='Arial', size=14),
                                showarrow=False))
        v = v + v_space

    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="intensity")
    fig.update_yaxes(tickvals=[])

    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        annotations=annotations,
        title_text="Projection of JRes for all replicates in the group",
        template="plotly_white",
        height=500,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            itemclick="toggleothers",
            itemdoubleclick="toggle"
        )
    )
    return fig


def plot_jres_spectra_with_ph(final_data_dict, repli_name, x_scale, y_scale, temp_levels):
    fig = go.Figure()
    config = dict({'scrollZoom': True})

    repli_ph, repli_data = final_data_dict[repli_name]
    temp_data = np.array(repli_data)
    start_level = temp_levels[0]
    end_level = temp_levels[-1]
    levels = np.linspace(start_level, end_level, 10)
    step = levels[1] - levels[0]
    print(start_level, end_level, step)

    fig.add_trace(
        go.Contour(
            x=x_scale,
            y=y_scale,
            z=temp_data,
            contours_coloring='lines',
            line_width=2,
            # line=dict(contours_coloring='lines', line_width=2),
            contours=dict(
                start=start_level,
                end=end_level,
                size=step,
            ),

        )
    )
    fig.update_xaxes(title_text="ppm")
    fig.update_yaxes(title_text="Hz")
    fig['layout']['xaxis']['autorange'] = "reversed"
    fig.update_layout(
        height=500,
        title_text="JRes of "+repli_name,
        template="plotly_white"
    )
    return fig