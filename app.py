from logging import PlaceHolder
import dash
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app
from callbacks import *


# load csv to df
df = pd.read_csv('cities_air_quality_water_pollution.18-10-2021.csv')


# some arrange, regex, names etc...
df.columns = ['City', 'Region', 'Country', 'AirQuality', 'WaterQuality']

df = df.drop(['Region'],axis=1)

df['Country'] = df['Country'].str.replace('"', '')


# make air quality values rigth
df['AirQuality'] = 100-df['AirQuality']
# air quality 100 = worst , 0 = clear
# water pollution 100 = best, 0 = no pollution


country_mean = df.groupby(['Country']).mean().reset_index()
country_clear = country_mean['Country'].str.strip()
country_mean['Country'] = country_clear

list_of_countrys = country_mean['Country'].tolist()

# worst pollution
country_air = country_mean.sort_values(by=['AirQuality','WaterQuality'], ascending=False)

country_air = country_air.head(10)



# worst pollution
country_water = country_mean.sort_values(by=['WaterQuality' ,'AirQuality'], ascending=False)

country_water = country_water.head(10)

citys = df.groupby(['City']).mean()
citys = citys.reset_index()
# top water pollution citys
city_water = citys.sort_values(by=['WaterQuality', 'AirQuality'], ascending=False)


# top air pollution citys
city_air = citys.sort_values(by=['AirQuality', 'WaterQuality'], ascending=False)
# sort by countrys
city_air_country = df.sort_values(by=['Country', 'AirQuality', 'WaterQuality'], ascending=False)


# water tab layout
water = html.Div(id='container_water',

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
                            dcc.Dropdown(id='countrys_water',
                                        className='dropdown_c',
                                        options= [
                                            {'label':i, 'value':i} for i in list_of_countrys
                                        ],
                                        multi=True,
                                        placeholder='...בחר אילו מדינות תרצה להציג'
                            ),

                            dcc.Graph(
                                id='top_citys_water',
                                className='top_citys',
                                figure={
                                    'data':[
                                        {'x':city_water['City'], 'y':city_water['WaterQuality'], 'type':'bar'}],
                                        }
                                ),
                            dcc.RadioItems(id='values_above',
                                            className='top_n_countrys',
                                            options= [
                                                {'label':'75', 'value':'75'},
                                                {'label':'85', 'value':'85'},
                                                {'label':'90', 'value':'90'},
                                                
                                            ],
                                            value='75')
                        ])

# air tab layout
air = html.Div(id='container_air',
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
                                ),
                            dcc.RadioItems(id='top_n_countrys_air',
                                            className='top_n_countrys',
                                            options= [
                                                {'label':'5', 'value':'5'},
                                                {'label':'10', 'value':'10'},
                                                {'label':'15', 'value':'15'},
                                            ],
                                            value='10')            
                        ])






# app layout
def activate():
    return html.Div(className='main',
            children=[
            dcc.Tabs(id='tabs',
                    value='זיהום אוויר',
                    children=[
                        dcc.Tab(id='air',
                                label='זיהום אוויר',
                                value='זיהום אוויר'),
                        dcc.Tab(id='water',
                                label='זיהום מים',
                                value='זיהום מים')
                            ]
                        ),
                   html.Div(id='tab_content')
        ])

# run web layout
app.layout=activate()

if __name__ == '__main__':
    app.run_server(debug = True, port = 6060)
