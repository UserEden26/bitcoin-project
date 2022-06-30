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
df['City'] = df["City"].str.strip()

df = df.drop_duplicates(subset=['City'])

df["WaterQuality"] = df["WaterQuality"].astype(int)
df["AirQuality"] = df["AirQuality"].astype(int)

# make air quality values rigth
df["AirQuality"] = 100 - df["AirQuality"]
# air quality 100 = worst , 0 = clear
# water pollution 100 = best, 0 = no pollution


country_mean = df.groupby(["Country"]).mean().reset_index()


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
citys = df.groupby(['City']).mean()
citys = citys.reset_index()

# top air pollution citys
city_air = citys.sort_values(by=["AirQuality", "WaterQuality"], ascending=False)




# air tab layout
air = html.Div(
    id="container_air",
    className='container_air',
    children=[
        html.H1(className="h1", children="זיהום אוויר"),
        dcc.Graph(
            id="barchart_country_water",
            className="barchart_country",
            figure={
                "data": [
                    {
                        "x": country_air["Country"],
                        "y": country_air["AirQuality"],
                        "type": "bar",
                    }
                ],
                "layout": {"title": "גרף זיהום אוויר לפי מדינה"},
            },
        ),
        dcc.Graph(
            className="top_citys",
            figure={
                "data": [
                    {"x": city_air["City"], "y": city_air["AirQuality"], "type": "bar"}
                ],
            },
        ),
        dcc.RadioItems(
            id="top_n_countrys_air",
            className="top_n_countrys",
            options=[
                {"label": "5", "value": "5"},
                {"label": "10", "value": "10"},
                {"label": "15", "value": "15"},
            ],
            value="10",
        ),
    ],
)





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

    