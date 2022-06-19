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

# worst pollution
country_air = country_mean.sort_values(by=['AirQuality','WaterQuality'], ascending=False)
country_air = country_air.reset_index()

country_air = country_air.head(10)



# worst pollution
country_water = country_mean.sort_values(by=['WaterQuality' ,'AirQuality'], ascending=False)
country_water = country_water.reset_index()

country_water = country_water.head(10)

# !!!need to fix, values over 100!
citys = df.groupby(['City', 'Country']).mean()
citys = citys.reset_index()
# top water pollution citys
city_water = citys.sort_values(by=['WaterQuality', 'AirQuality'], ascending=False)
# sort by countrys
city_water_country = df.sort_values(by=['Country','WaterQuality', 'AirQuality'], ascending=False)

# top air pollution citys
city_air = citys.sort_values(by=['AirQuality', 'WaterQuality'], ascending=False)
# sort by countrys
city_air_country = df.sort_values(by=['Country', 'AirQuality', 'WaterQuality'], ascending=False)




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
            
            
        # html.H1(className='h1',
        #         children='Air polution'),

        # dcc.Graph(id='barchart_country',
        #     className='barchart_country',
        #     figure={
        #         'data': [
        #             {'x': country_mean['Country'], 'y': country_mean['AirQuality'], 'type':'bar'}],
        #             'layout': {'title': 'גרף זיהום אוויר לפי מדינה'},
        #     }
        # ),

      
        # dcc.Input(id='amount_of_countrys',
        #     className='amount_of_countrys',
        #     placeholder='כמות מדינות להצגה',
        #     type='number',
        #     value='',
        #     min=3,
        #     max=10),
        
        # dcc.RadioItems(className='worst_best',
        #                         options=[
        #                         {'label':'המזהמות ביותר', 'value':'המזהמות ביותר'},
        #                         {'label':'הכי פחות מזהמות', 'value':'הכי פחות מזהמות'}
        #                         ],
        #                         inline=True,
        #                         value='המזהמות ביותר'
        #                         ),
    


# run web layout
app.layout=activate()

if __name__ == '__main__':
    app.run_server(debug = True, port = 6060)
