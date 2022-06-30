import dash
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app

# load csv to df
df = pd.read_csv("cities_air_quality_water_pollution.18-10-2021.csv")


# some arrange, regex, names etc...
df.columns = ["City", "Region", "Country", "AirQuality", "WaterQuality"]
df = df.drop(["Region"], axis=1)


df["Country"] = df["Country"].str.replace('"', "")
df["Country"] = df["Country"].str.strip()
df["City"] = df["City"].str.strip()

df = df.drop_duplicates(subset=["City"])

df["WaterQuality"] = df["WaterQuality"].astype(int)
df["AirQuality"] = df["AirQuality"].astype(int)

# make air quality values rigth
df["AirQuality"] = 100 - df["AirQuality"]
# air quality 100 = worst , 0 = clear
# water pollution 100 = best, 0 = no pollution


country_mean = df.groupby(["Country"]).mean().reset_index()
country_mean["AirQuality"] = country_mean["AirQuality"].round(1)
country_mean["WaterQuality"] = country_mean["WaterQuality"].round(1)


list_of_countrys = country_mean["Country"].tolist()

# worst pollution
country_air = country_mean.sort_values(
    by=["AirQuality", "WaterQuality"], ascending=False
)

country_air = country_air.head(10)


# worst pollution
country_water = country_mean.sort_values(
    by=["WaterQuality", "AirQuality"], ascending=False
)

country_water = country_water.head(10)

# make city df with country, city ,waterquality and airquality
citys = df.groupby(["City"]).mean()
citys = citys.reset_index()
citys["WaterQuality"] = citys["WaterQuality"].round(1)
citys["AirQuality"] = citys["AirQuality"].round(1)


for i in range(0,100):
    val=df.loc[(val["WaterQuality"] >= i) & (val["WaterQuality"] <=i+1)]
    if val is None:
        val1=0
    else:
        val1 = len(val.index)
    print(f'{i} : {val1}')