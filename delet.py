import dash
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
import re

# load csv to df
df = pd.read_csv('cities_air_quality_water_pollution.18-10-2021.csv')


# some arrange, regex, names etc...
df.columns = ['City', 'Region', 'Country', 'AirQuality', 'WaterQuality']

df['Country'] = df['Country'].str.replace('"', '')

df = df.drop(['Region'],axis=1)

# make air quality values rigth
df['AirQuality'] = 100-df['AirQuality']
# air quality 100 = worst , 0 = clear
# water pollution 100 = best, 0 = no pollution



country_mean = df.groupby(['Country']).mean()

country_air = country_mean.sort_values(by=['AirQuality','WaterQuality'], ascending=False)
country_air = country_air.reset_index()
country_air = country_air.head(10)

country_water = country_mean.sort_values(by=['WaterQuality' ,'AirQuality'], ascending=False)
country_water = country_water.reset_index()
country_water = country_water.head(10)

city_water1 = df.groupby(['City', 'Country']).mean()
city_water1 = city_water1.reset_index()
city_water = df.sort_values(by=['Country', 'WaterQuality','AirQuality'], ascending=False)
print(city_water1)

city_air = df.sort_values(by=['Country', 'AirQuality','WaterQuality'], ascending=False)

