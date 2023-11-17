import dash
from dash import html, dcc, Input, Output
import plotly.graph_objs as go
import numpy as np
import glob
import os
import cv2
import argparse


parser = argparse.ArgumentParser(description="Description of your script.")
parser.add_argument('-l', '--lr', type=str, default='upload', help='Input LR spectrum')
parser.add_argument('-s', '--sr', type=str, default='results', help="Output SR spectrum")
args = parser.parse_args()

data = cv2.imread(args.sr, cv2.IMREAD_UNCHANGED)

# Create a Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.RangeSlider(
        id='colorscale-range',
        min=0,
        max=1,
        step=0.01,
        marks={i / 10: str(i / 10) for i in range(11)},
        value=[0.2, 0.8]
    ),
    dcc.Loading(
        id="loading-1",
        type="default",  # Change to 'graph', 'cube', 'circle', 'dot', or 'default'
        fullscreen=False,  # Set to True for fullscreen loading spinner
        children=html.Div([dcc.Graph(id='heatmap')])
    )
])


# Callback to update heatmap
@app.callback(
    Output('heatmap', 'figure'),
    [Input('colorscale-range', 'value')]
)
def update_heatmap(scale_values):
    # Simulate a delay to mimic long processing time
    import time
    time.sleep(1)  # Remove this in your actual application

    return {
        'data': [go.Heatmap(
            z=data,
            zmin=scale_values[0],  # Update zmin
            zmax=scale_values[1]  # Update zmax
        )]
    }


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)