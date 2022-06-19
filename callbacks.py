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
        return html.Div(id='container_air',
                        children=[
                            html.H1(className='h1', 
                                    children='זיהום אוויר'),

                            dcc.Graph(id='barchart_country_water',
                                    className='barchart_country',
                                    figure={
                                        'data': [
                                            {'x': country_air['Country'], 'y': country_air['AirQuality'], 'type':'bar'}],
                                            'layout': {'title': 'גרף זיהום אוויר לפי מדינה'},
                                        }
                                ),
                            dcc.Graph(
                                className='top_citys',
                                figure={
                                    'data':[
                                        {'x':city_air['City'], 'y':city_air['AirQuality'], 'type':'bar'}],
                                        }
                                )            
                        ])


    elif tab == 'זיהום מים':
        return html.Div(id='container_water',

                        children=[
                            html.H1(className='h1', 
                                    children='זיהום מים'),

                            dcc.Graph(id='barchart_country_water',
                                    className='barchart_country',
                                    figure={
                                        'data': [
                                            {'x': country_water['Country'], 'y': country_water['WaterQuality'], 'type':'bar'}],
                                            'layout': {'title': 'גרף זיהום מים לפי מדינה'},
                                        }
                                ),
                            dcc.Graph(
                                className='top_citys',
                                figure={
                                    'data':[
                                        {'x':city_water['City'], 'y':city_water['WaterQuality'], 'type':'bar'}],
                                        }
                                )
                        ])

