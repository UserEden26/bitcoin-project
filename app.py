from logging import PlaceHolder
from multiprocessing.sharedctypes import Value
import dash
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app
from water_callbacks import *


# app layout
def activate():
    return html.Div(
        className="main",
        children=[
            dcc.Tabs(
                id="tabs",
                value="זיהום אוויר",
                children=[
                    dcc.Tab(id="air", className='air', label="זיהום אוויר", value="זיהום אוויר"),
                    dcc.Tab(id="water", className='water', label="זיהום מים", value="זיהום מים"),
                ],
            ),
            html.Div(id="tab_content"),
        ],
    )


# run web layout
app.layout = activate()

if __name__ == "__main__":
    app.run_server(debug=True, port=6060)
