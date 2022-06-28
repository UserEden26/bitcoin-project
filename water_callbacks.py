from tkinter import font
from turtle import title
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
city_water = df.sort_values(by=["WaterQuality", 'AirQuality'], ascending=False)

# water tab layout
water = html.Div(
    id="container_water",
    className='container_water',
    children=[
        html.H1(className="h1", children="זיהום מים"),
        html.Div(className='container_barchart_country',
                children=
            dcc.Graph(
                id="barchart_country_water",
                className="barchart_country",
                figure=
                    px.bar(country_water,
                        x=country_water["Country"],
                        y=country_water["WaterQuality"],
                        range_y=[0,100],
                        title='ה10 מדינות עם זיהום המים הגבוה ביותר',
                        template="plotly_dark")
                
            ),
        ),
        html.Div(className='container_dropdown_c',
                children=
            dcc.Dropdown(
                id="countrys_water",
                className="dropdown_c",
                options=[{"label": i, "value": i} for i in list_of_countrys],
                multi=True,
                placeholder="...בחר אילו מדינות תרצה להציג",
            ),
        ),
        html.Div(className='container_top_citys',
                children=
            dcc.Graph(
                id="top_citys_water",
                className="top_citys",
                figure=px.bar(city_water,
                            x=city_water["City"],
                            y=city_water["WaterQuality"],
                            range_y=[0,100],
                            title='זיהום המים בערים',
                            template="plotly_dark")
            ),
        ),
        html.Button(
            id='reset_country_grafh_water',
            className='reset_country_grafh',
            children='איתחול גרף'
        ),
        html.Div(className='container_range_city',
                children=
            dcc.RangeSlider(
                id="range_city_water",
                className="range_city",
                max=citys["WaterQuality"].max(),
                min=citys["WaterQuality"].min(),
                marks={
                    i: f"{i}"
                    for i in range(
                        int(citys["WaterQuality"].min()), int(citys["WaterQuality"].max())
                    )[::5]
                },
                value=[5, 100],
                allowCross=False,
            ),
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
    fig2=px.bar(country_water,
            x=country_water["Country"],
            y=country_water["WaterQuality"],
            range_y=[0,100],
            title='ה10 מדינות עם זיהום המים הגדול ביותר',
            template="plotly_dark")
    return fig2

  elif countrys is not None:
    df = country_mean.loc[country_mean["Country"].isin(countrys)]
    df = df.sort_values(by=["WaterQuality"], ascending=False)
    fig = px.bar(df,
          x=df["Country"],
          y=df['WaterQuality'],
          range_y=[0,100],
          title='מדינות מזהמות לאחר בחירה',
          template="plotly_dark")
    return fig
    


# city filter
@app.callback(
  Output('top_citys_water','figure'),
  Output('range_city_water','value'),
  Input('range_city_water','value'),
  Input("barchart_country_water", 'hoverData'),
  Input('reset_country_grafh_water', 'n_clicks'),
  prevent_initial_update=True
)

# show citys per hover country on first grafh
def city_graf_w(value, hovdata, click_reset): 
    filter_df = df.loc[(df['WaterQuality'] >= value[0]) & (df['WaterQuality'] <=value[1])]
    filter_df = filter_df.sort_values(['WaterQuality'], ascending=False)
    

    # all citys table
    fig = px.bar(filter_df,
                x=filter_df['City'],
                y=filter_df['WaterQuality'],
                range_y=[0,100],
                title='ערים מזהמות לאחר הגבלת הסינון',
                template="plotly_dark")
    fig.update_layout(
                font_size=20
                )
    
    while hovdata is None:
        return fig, value
    
    if hovdata is not None:
        hov_country = hovdata['points'][0]['x']
        hover_country_data = filter_df[filter_df.Country== hov_country]

        if hover_country_data.empty is False:
            fig2 = px.bar(hover_country_data,
                                x=hover_country_data['City'],
                                y=hover_country_data['WaterQuality'],
                                range_y=[0,100],
                                title=(f'{hov_country} הערים המזהמות לאחר סינון ב'),
                                template="plotly_dark",
                                color_continuous_scale='reds',
                                range_color=[0,100],
                                color=hover_country_data['WaterQuality'])
            fig2.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=24),
            fig2.update_coloraxes(showscale=False)
            fig2.update_xaxes(title_text='ערים') 
            fig2.update_yaxes(title_text='איכות מים')
            return fig2, value   

        elif click_reset or hover_country_data.empty is True:
            value=[0,100]
            dff=df.loc[(df['WaterQuality'] >= value[0]) & (df['WaterQuality'] <=value[1])]
            dff = dff.sort_values(['WaterQuality'], ascending=False)
            fig3 = px.bar(dff,
                x=dff['City'],
                y=dff['WaterQuality'],
                range_y=[0,100],
                title='ערים מזהמות לאחר הגבלת הסינון',
                template="plotly_dark")
            fig3.update_layout(
                font_size=20
                )
            print(dff)
            return fig3, value 
        
        

        

    # try:
        
    #     hov_country = hovdata['points'][0]['x']
    #     hover_country_data = filter_df[filter_df.Country== hov_country]
    #     fig2 = px.bar(hover_country_data,
    #                         x=hover_country_data['City'],
    #                         y=hover_country_data['WaterQuality'],
    #                         range_y=[0,100],
    #                         title=(f'{hov_country} הערים המזהמות לאחר סינון ב'),
    #                         template="plotly_dark",
    #                         color_continuous_scale='reds',
    #                         range_color=[0,100],
    #                         color=hover_country_data['WaterQuality'])
    #     fig2.update_layout(
    #                 title_x=0.5,
    #                 font_size=20,
    #                 hoverlabel_font_size=24),
    #     fig2.update_coloraxes(showscale=False)    
    #     return fig2, value

    # except:
    #     if type(hovdata['points'][0]['x']) is None:
    #         return fig, value

    #     elif hover_country_data.empty is True:
    #         change=[0,100]
    #         return fig, change

    # finally:
    #     if click_reset:
    #         return fig, value



