import dash
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app
from app import *


# select which pollution
@app.callback(
    Output('tab_content','children'),
    Input('tabs','value')
)


def type_of_pollution(tab):
    if tab == 'זיהום אוויר':
        return air

    elif tab == 'זיהום מים':
        return water
                


# water callbacks

@app.callback(
  Output('top_citys_water','figure'),
  Input('values_above','value')
)

def city_graf_w(above):
  above = int(above)
  df = city_water.loc[city_water['WaterQuality'] >= above]
  fig = px.bar(df,
        x=df['City'],
        y=df['WaterQuality'])
  return fig




# trying..
# @app.callback(
#     Output('barchart_country_water','figure'),
#     Input('countrys_water','value')
# )

# def select_countrys(dropdown_value):
#     dff = df[df.state.str.contains('|'.join(dropdown_value))]
#     dff = df.sort_values(by=['WaterQuality'])
#     if dropdown_value is None:
#         return {'data': [{'x': country_water['Country'], 'y': country_water['WaterQuality'], 'type':'bar'}],
#                                             'layout': {'title': 'גרף זיהום מים לפי מדינה'}}

#     fig =   px.bar(dff,
#             x=dff['City'],
#             y=dff['WaterQuality'])
#     return fig

    