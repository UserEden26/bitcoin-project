from tkinter import font
from turtle import title
import os
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
from main_dash import app
from callbacks import *

# top water pollution citys
city_water = df.sort_values(by=["WaterQuality", "AirQuality"], ascending=False)

# define bg color
bg_color = "rgb(26, 26, 26)"

# coutrys graph
c_graph_water = px.bar(
    country_water,
    x=country_water["Country"],
    y=country_water["WaterQuality"],
    range_y=[0, 100],
    title="ה10 מדינות עם זיהום המים הגבוה ביותר",
    template="plotly_dark",
    color_continuous_scale="peach",
    range_color=[1, 100],
    color=country_water["WaterQuality"],
)
c_graph_water.update_layout(
    title_x=0.5,
    font_size=20,
    hoverlabel_font_size=28,
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
),
c_graph_water.update_coloraxes(showscale=False)
c_graph_water.update_xaxes(title_text="מדינות")
c_graph_water.update_yaxes(title_text="איכות מים")


# city graph
if len(city_water.index) > 100:
    bg_color = "rgb(77, 77, 77)"
else:
    bg_color = "rgb(26, 26, 26)"
fig_city_water = px.bar(
    city_water,
    x=city_water["City"],
    y=city_water["WaterQuality"],
    range_y=[0, 100],
    title="זיהום המים בערים",
    template="plotly_dark",
    color_continuous_scale="Peach",
    range_color=[1, 100],
    color=city_water["WaterQuality"],
)
fig_city_water.update_layout(
    title_x=0.5,
    font_size=20,
    hoverlabel_font_size=28,
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
)
fig_city_water.update_coloraxes(showscale=False)
fig_city_water.update_xaxes(title_text="ערים", nticks=5)
fig_city_water.update_yaxes(title_text="")


# water tab layout
water = html.Div(
    id="big_container_water",
    children=[
        html.Div(
            id="container_water",
            className="container_water",
            children=[
                html.H1(className="h1", children="זיהום מים"),
                html.Div(
                    className="container_barchart_country",
                    children=dcc.Graph(
                        id="barchart_country_water",
                        className="barchart_country",
                        figure=c_graph_water,
                    ),
                ),
                html.Div(
                    className="container_dropdown_c",
                    children=dcc.Dropdown(
                        id="countrys_water",
                        className="dropdown_c",
                        options=[{"label": i, "value": i} for i in list_of_countrys],
                        multi=True,
                        placeholder="...בחר אילו מדינות תרצה להציג",
                    ),
                ),
                html.Div(
                    className="container_top_citys",
                    children=dcc.Graph(
                        id="top_citys_water",
                        className="top_citys",
                        figure=fig_city_water,
                    ),
                ),
                html.Button(
                    id="zero_button_water",
                    className="zero_button",
                    children="ערכי אפס",
                ),
                html.Div(
                    className="container_range_city",
                    children=dcc.RangeSlider(
                        id="range_city_water",
                        className="range_city",
                        max=100,
                        min=1,
                        marks={i: f"{i}" for i in range(0, 100)[::5]},
                        value=[1, 100],
                        allowCross=False,
                    ),
                ),
            ],
        ),
        html.Div(id="hide_container_water", className="hide_container_water", children=[]),
    ],
)

# select which pollution
@app.callback(Output("tab_content", "children"), Input("tabs", "value"))
def type_of_pollution(tab):
    if tab == "זיהום אוויר":
        return Air

    elif tab == "זיהום מים":
        return water


# water callbacks

# country filter
@app.callback(
    Output("barchart_country_water", "figure"), Input("countrys_water", "value")
)
def coutrys_select(countrys):
    if countrys is None or countrys == []:
        return c_graph_water

    elif countrys is not None:
        df = country_mean.loc[country_mean["Country"].isin(countrys)]
        df = df.sort_values(by=["WaterQuality"], ascending=False)
        if len(df.index) > 100:
            bg_color = "rgb(77, 77, 77)"
        else:
            bg_color = "rgb(26, 26, 26)"
        fig = px.bar(
            df,
            x=df["Country"],
            y=df["WaterQuality"],
            range_y=[0, 100],
            title="מדינות מזהמות לאחר בחירה",
            template="plotly_dark",
            color_continuous_scale="Peach",
            range_color=[1, 100],
            color=df["WaterQuality"],
        )
        fig.update_layout(
            title_x=0.5,
            font_size=20,
            hoverlabel_font_size=28,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
        ),
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(title_text="מדינות")
        fig.update_yaxes(title_text="איכות מים")
        return fig


# city filter
@app.callback(
    Output("top_citys_water", "figure"),
    Output("range_city_water", "value"),
    Output("barchart_country_water", "hoverData"),
    Input("range_city_water", "value"),
    Input("barchart_country_water", "hoverData"),
    prevent_initial_update=True,
)

# show citys per hover country on first grafh
def city_graf_w(value, hovdata):
    filter_df = df.loc[
        (df["WaterQuality"] >= value[0]) & (df["WaterQuality"] <= value[1])
    ]

    # the varible that will be returned
    l = []
    # check if there is no value for a range
    if len(filter_df.index) == 0:
        value = [1, 100]

    filter_df = df.loc[
        (df["WaterQuality"] >= value[0]) & (df["WaterQuality"] <= value[1])
    ]

    filter_df = filter_df.sort_values(["WaterQuality"], ascending=False)

    # all citys table
    if len(filter_df.index) > 100:
        bg_color = "rgb(77, 77, 77)"
    else:
        bg_color = "rgb(26, 26, 26)"
    fig = px.bar(
        filter_df,
        x=filter_df["City"],
        y=filter_df["WaterQuality"],
        range_y=[0, 100],
        title=f"ערים מזהמות בטווח זיהום {value[0]}-{value[1]}",
        template="plotly_dark",
        color_continuous_scale="peach",
        range_color=[1, 100],
        color=filter_df["WaterQuality"],
    )
    fig.update_layout(
        title_x=0.5,
        font_size=20,
        hoverlabel_font_size=28,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
    ),
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(title_text="ערים")
    fig.update_yaxes(title_text="")
    if len(filter_df.index) > 10:
        fig.update_xaxes(nticks=5)

    if hovdata is not None:
        hov_country = hovdata["points"][0]["x"]
        hover_country_data = filter_df[filter_df.Country == hov_country]

        if hover_country_data.empty is False:
            if len(hover_country_data.index) > 100:
                bg_color = "rgb(77, 77, 77)"
            else:
                bg_color = "rgb(26, 26, 26)"
            fig2 = px.bar(
                hover_country_data,
                x=hover_country_data["City"],
                y=hover_country_data["WaterQuality"],
                range_y=[0, 100],
                title=(f"בטווח {value[0]}-{value[1]} {hov_country} זיהום המים בערי"),
                template="plotly_dark",
                color_continuous_scale="peach",
                range_color=[1, 100],
                color=hover_country_data["WaterQuality"],
            )
            fig2.update_layout(
                title_x=0.5,
                font_size=20,
                hoverlabel_font_size=28,
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
            ),
            fig2.update_coloraxes(showscale=False)
            fig2.update_xaxes(title_text="ערים")
            fig2.update_yaxes(title_text="")
            if len(hover_country_data.index) > 10:
                fig2.update_xaxes(nticks=5)
                l = [fig2, value, hovdata]
            l = [fig2, value, hovdata]

        elif hover_country_data.empty is True:
            value = [1, 100]
            hovdata = None
            l = [fig, value, hovdata]

    elif hovdata is None:
        l = [fig, value, hovdata]
    return l


# zero values table
@app.callback(
    Output("hide_container_water", "children"),
    Output("hide_container_water", "style"),
    Output("container_water", "style"),
    Input("zero_button_water", "n_clicks"),
    State("hide_container_water", "style")
)
def zero_val_water(zero_click, style):
    zero_vals = df.loc[df["WaterQuality"] == 0]
    zero_vals = zero_vals.sort_values(by="Country")
    tabl = dash_table.DataTable(
        zero_vals.to_dict("records"),
        [{"name": i, "id": i} for i in df.columns],
        id="tbl_water",
    )
    button=html.Button(id='tabl_button_water',className='tabl_button', children='סגור')
    container_return = [[tabl,button], {"display": "none"}, {"filter": "blur(0)"}]

    if style=={"display": "block"} and zero_click:
        hide_see = {"display": "none", 'overflow':'scroll', 'background-color':'none'}
        blur = {"filter": "blur(0)"}
        container_return = [[tabl,button], hide_see, blur]

    elif style=={"display": "none"} and zero_click:
        hide_see = {"display": "block",'overflow':'scroll', 'background-color':'rgb(245,245,245)'}
        blur = {"filter": "blur(4px)"}
        container_return = [[tabl,button], hide_see, blur]
    return container_return



@app.callback(
    Output("zero_button_water", "n_clicks"),
    Input('tabl_button_water', 'n_clicks'),
    State("hide_container_water", "style")
)

def click_adds(click_tabl_button, style_now):
    if click_tabl_button and style_now=={"display": "none"}:
        return 
        