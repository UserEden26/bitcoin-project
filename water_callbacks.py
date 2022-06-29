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


# coutrys graph 
c_graph_water =  px.bar(country_water,
                        x=country_water["Country"],
                        y=country_water["WaterQuality"],
                        range_y=[0,100],
                        title='ה10 מדינות עם זיהום המים הגבוה ביותר',
                        template="plotly_dark",
                                color_continuous_scale='reds',
                                range_color=[0,100],
                                color=country_water['WaterQuality'])
c_graph_water.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=28),
c_graph_water.update_coloraxes(showscale=False)
# c_graph_water.update_xaxes(title_text='ערים') 
c_graph_water.update_yaxes(title_text='איכות מים')
if len(country_water.index)>10:
    c_graph_water.update_xaxes(nticks=5)              
            

# city graph 
fig_city_water=px.bar(city_water,
                            x=city_water["City"],
                            y=city_water["WaterQuality"],
                            range_y=[0,100],
                            title='זיהום המים בערים',
                            template="plotly_dark",
                            color_continuous_scale='reds',
                            range_color=[0,100],
                            color=city_water['WaterQuality'])
fig_city_water.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=28)
fig_city_water.update_coloraxes(showscale=False)
fig_city_water.update_xaxes(title_text='ערים',
                            nticks=5) 
fig_city_water.update_yaxes(title_text='')


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
                figure=c_graph_water),
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
                figure=fig_city_water
            ),
        ),
        html.Button(
            id='creat_file',
            className='creat_file_water',
            children='ייצא גרף'
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
    return c_graph_water

  elif countrys is not None:
    df = country_mean.loc[country_mean["Country"].isin(countrys)]
    df = df.sort_values(by=["WaterQuality"], ascending=False)
    fig = px.bar(df,
          x=df["Country"],
          y=df['WaterQuality'],
          range_y=[0,100],
          title='מדינות מזהמות לאחר בחירה',
          template="plotly_dark",
                                color_continuous_scale='reds',
                                range_color=[0,100],
                                color=df['WaterQuality'])
    fig.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=28),
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(title_text='מדינות') 
    fig.update_yaxes(title_text='איכות מים')
    return fig
    


# city filter
@app.callback(
  Output('top_citys_water','figure'),
  Output('range_city_water','value'),
  Output("barchart_country_water", 'hoverData'),
  Input('range_city_water','value'),
  Input("barchart_country_water", 'hoverData'),
  prevent_initial_update=True
)

# show citys per hover country on first grafh
def city_graf_w(value, hovdata): 
    filter_df = df.loc[(df['WaterQuality'] >= value[0]) & (df['WaterQuality'] <=value[1])]
    filter_df = filter_df.sort_values(['WaterQuality'], ascending=False)
    

    # all citys table
    fig = px.bar(filter_df,
                x=filter_df['City'],
                y=filter_df['WaterQuality'],
                range_y=[0,100],
                title=f'ערים מזהמות בטווח זיהום {value[0]}-{value[1]}',
                template="plotly_dark",
                                color_continuous_scale='reds',
                                range_color=[0,100],
                                color=filter_df['WaterQuality'])
    fig.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=28),
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(title_text='ערים') 
    fig.update_yaxes(title_text='')
    if len(filter_df.index)>10:
        fig.update_xaxes(nticks=5)
    
    l=[]

    if hovdata is not None:
        hov_country = hovdata['points'][0]['x']
        hover_country_data = filter_df[filter_df.Country== hov_country]

        if hover_country_data.empty is False:
            fig2 = px.bar(hover_country_data,
                                x=hover_country_data['City'],
                                y=hover_country_data['WaterQuality'],
                                range_y=[0,100],
                                title=(f'בטווח {value[0]}-{value[1]} {hov_country} זיהום המים בערי'),
                                template="plotly_dark",
                                color_continuous_scale='reds',
                                range_color=[0,100],
                                color=hover_country_data['WaterQuality'])
            fig2.update_layout(
                        title_x=0.5,
                        font_size=20,
                        hoverlabel_font_size=28),
            fig2.update_coloraxes(showscale=False)
            fig2.update_xaxes(title_text='ערים') 
            fig2.update_yaxes(title_text='')
               
            if len(hover_country_data.index)>10:
                fig2.update_xaxes(nticks=5)
                l= [fig2, value, hovdata]
            l= [fig2, value, hovdata] 

        elif hover_country_data.empty is True:
            value=[0,100]
            hovdata = None
            l= [fig, value, hovdata]
    
    elif hovdata is None:
        l= [fig, value, hovdata]
    return l
    


    


