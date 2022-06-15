import dash
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from callbacks import *
from main_dash import app
import re


# load csv to df
df = pd.read_csv('cities_air_quality_water_pollution.18-10-2021.csv')


# some arrange, regex, names etc...
df.columns = ['City', 'Region', 'Country', 'AirQuality', 'WaterQuality']

df['Country'] = df['Country'].str.replace('"', '')

df['Region'] = df['Region'].str.replace('""', 'Not Define')
df['Region'] = df['Region'].str.replace('"', '')

# make air quality values rigth
df['AirQuality'] = 100-df['AirQuality']
# air quality 100 = worst , 0 = clear
# water pollution 100 = best, 0 = no pollution


country_mean = df.groupby(['Country']).mean()
amount_of_countrys = len(country_mean.index)


# app layout
def activate():
    return html.Div(children=[
        html.H1(className='h1',
                children='polution mission'),
        # dcc.Graph(
        #     figure={
        #         {'x':[], 'y':[], 'type':'bar', 'name'}
        #     }
        ),
        dcc.Slider(0, amount_of_countrys, 10, value=10),
        dcc.Input(
            id='num_main_barchart',
            placeholder='כמות מדינות להצגה',
            type='number',
            value='',
            min=1,
            max=177
        )
        # dcc.RangeSlider(0, 100, count=10, value=[0, 100])
    ])


# run web layout
app.layout=activate()

if __name__ == '__main__':
    app.run_server(debug = True, port = 6060)
