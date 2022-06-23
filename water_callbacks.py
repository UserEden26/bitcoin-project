import dash
from dash import Dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app
from callbacks import *

# top water pollution citys
city_water = citys.sort_values(by=["WaterQuality"], ascending=False)

# water tab layout
water = html.Div(
    id="container_water",
    children=[
        html.H1(className="h1", children="זיהום מים"),
        dcc.Graph(
            id="barchart_country_water",
            className="barchart_country",
            figure=
                px.bar(country_water,
                    x=country_water["Country"],
                    y=country_water["WaterQuality"])
            ,
        ),
        dcc.Dropdown(
            id="countrys_water",
            className="dropdown_c",
            options=[{"label": i, "value": i} for i in list_of_countrys],
            multi=True,
            placeholder="...בחר אילו מדינות תרצה להציג",
        ),
        dcc.Graph(
            id="top_citys_water",
            className="top_citys",
            figure={
                "data": [
                    {
                        "x": city_water["City"],
                        "y": city_water["WaterQuality"],
                        "type": "bar",
                    }
                ],
            },
        ),
        dcc.RangeSlider(
            id="range_city",
            max=citys["WaterQuality"].max(),
            min=citys["WaterQuality"].min(),
            marks={
                i: f"{i}"
                for i in range(
                    int(citys["WaterQuality"].min()), int(citys["WaterQuality"].max())
                )[::5]
            },
            value=[90, 100],
            allowCross=False,
        ),  

    ],
)


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

# country filter
@app.callback(
  Output('barchart_country_water','figure'),
  Input('countrys_water','value')
  )

def coutrys_select(countrys):
  if countrys is None or countrys==[]:
    return px.bar(country_water,
            x=country_water["Country"],
            y=country_water["WaterQuality"])

  elif countrys is not None:
    df = country_mean.loc[country_mean["Country"].isin(countrys)]
    df = df.sort_values(by=["WaterQuality"], ascending=False)
    fig = px.bar(df,
          x=df["Country"],
          y=df['WaterQuality'])
    return fig
    


# city filter
@app.callback(
  Output('top_citys_water','figure'),
  Input('range_city','value'),
  Input("barchart_country_water", 'hoverData'),
  Input("barchart_country_water", 'clickData'),
  Input("barchart_country_water", 'selectedData'),
  prevent_initial_update=True
)

# show citys per hover country on first grafh
def city_graf_w(value, hovdata ,clickdata, selecteddata): 
    filter_df = df.loc[(df['WaterQuality'] >= value[0]) & (df['WaterQuality'] <=value[1])]
    filter_df = filter_df.sort_values(['WaterQuality'], ascending=False)

    fig = px.bar(filter_df,
            x=filter_df['City'],
            y=filter_df['WaterQuality'])

    hov_country = hovdata['points'][0]['x']
    hover_country_data = filter_df[filter_df.Country== hov_country]
    fig2 = px.bar(hover_country_data,
                x=hover_country_data['City'],
                y=hover_country_data['WaterQuality'])
    if hovdata == None: 
        return fig
    else:
        return fig2



# click country change city 
