import dash
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app


@app.callback(
    Output('num_main_barchart', 'value'),
    Input('num_main_barchart', 'value'),
    State('num_main_barchart', 'min'),
    State('num_main_barchart', 'max')
)
def limit_values(number, min_possible, max_possible):
    if number < min_possible:
        number = min_possible
    elif number > max_possible:
        number = max_possibleS
    return number
