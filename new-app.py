from collections import OrderedDict
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datashader as ds
import datashader.transfer_functions as tf
import pandas as pd
import numpy as np


from influxdb import InfluxDBClient


def set_database():
    """
    Return a list of measurement in the database
    """
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('indaba_session')
    query = 'select last( * ) from "Indaba Session"'

    result = client.query(query)

    result_list = list(result.get_points())
    return result_list


def get_pandas_dataframe():
    """
    Returns a pandas dataframe of dates
    """
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('indaba_session')
    query = 'select * from "Indaba Session"'

    result = client.query(query)

    result_list = list(result.get_points())
    df = pd.DataFrame(result_list)  # use pandas data frame
    return df


def get_devices():
    """
    Returns devices
    """
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('indaba_session')
    query = 'select * from "Indaba Session"'

    result = client.query(query)

    devices = []

    # Add new device to list of devices
    result_list = list(result.get_points())
    for i in range(len(result_list)):
        if (result_list[i]['sensor']) not in devices:
            devices.append(result_list[i]['sensor'])
    return devices


# Set up axes

x = get_pandas_dataframe()[['time']].apply(pd.to_datetime)
y = get_pandas_dataframe()[['Relative Humidity']]


# Layout

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "/assets/style.css",
]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

fig1 = {
    "data": [
        {
            "x": x,
            "y": y,
            "type": "heatmap",
            "showscale": False,
            "colorscale": [[0, "rgba(255, 255, 255,0)"], [1, "#a3a7b0"]],
        }
    ],
    "layout": {
        "margin": {"t": 50, "b": 20},
        "height": 250,
        "xaxis": {
            "showline": True,
            "zeroline": False,
            "showgrid": False,
            "showticklabels": True,
            "color": "#a3a7b0",
        },
        "yaxis": {
            "fixedrange": True,
            "showline": False,
            "zeroline": False,
            "showgrid": False,
            "showticklabels": False,
            "ticks": "",
            "color": "#a3a7b0",
        },
        "plot_bgcolor": "#23272c",
        "paper_bgcolor": "#23272c",
    },
}

fig2 = {
    "data": [
        {
            "x": x,
            "y": y,
            "type": "heatmap",
            "showscale": False,
            "colorscale": [[0, "rgba(255, 255, 255,0)"], [1, "#75baf2"]],
        }
    ],
    "layout": {
        "margin": {"t": 50, "b": 20},
        "height": 250,
        "xaxis": {
            "fixedrange": True,
            "showline": True,
            "zeroline": False,
            "showgrid": False,
            "showticklabels": True,
            "color": "#a3a7b0",
        },
        "yaxis": {
            "fixedrange": True,
            "showline": False,
            "zeroline": False,
            "showgrid": False,
            "showticklabels": False,
            "ticks": "",
            "color": "#a3a7b0",
        },
        "plot_bgcolor": "#23272c",
        "paper_bgcolor": "#23272c",
    },
}

app.layout = html.Div(
    [
        html.Div(
            id="header",
            children=[
                html.Div(
                    [
                        html.H3(
                            "Visualize Temperature Data and Relative Humidity"
                        )
                    ],
                    className="eight columns",
                ),
                html.Div([html.Img(id="logo", src=app.get_asset_url("dash-logo.png"))]),
            ],
            className="row",
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Click and drag on the plot for high-res view of\
             selected data",
                            id="header-1",
                        ),
                        dcc.Graph(
                            id="graph-1", figure=fig1, config={"doubleClick": "reset"}
                        ),
                    ],
                    className="twelve columns",
                )
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            children=[
                                html.Span(children=["0"], id="header-2-strong"),
                                html.Span(
                                    children=[" points selected"], id="header-2-p"
                                ),
                            ],
                            id="header-2",
                        ),
                        dcc.Graph(id="graph-2", figure=fig2),
                    ],
                    className="twelve columns",
                )
            ],
            className="row",
        ),
    ]
)




if __name__ == '__main__':
    app.run_server(debug=True)
