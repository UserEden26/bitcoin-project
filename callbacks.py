import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
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
country_Air = country_mean.sort_values(
    by=["AirQuality", "WaterQuality"], ascending=False
)

country_Air = country_Air.head(10)


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


# top air pollution citys
city_Air = citys.sort_values(by=["AirQuality", "WaterQuality"], ascending=False)


# air tab layout
bg_color = "rgb(26, 26, 26)"

# coutrys graph
c_graph_Air = px.bar(
    country_Air,
    x=country_Air["Country"],
    y=country_Air["AirQuality"],
    range_y=[0, 100],
    title="ה10 מדינות עם זיהום האוויר הגבוה ביותר",
    template="plotly_dark",
    color_continuous_scale="peach",
    range_color=[0, 100],
    color=country_Air["AirQuality"],
)
c_graph_Air.update_layout(
    title_x=0.5,
    font_size=20,
    hoverlabel_font_size=28,
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
),
c_graph_Air.update_coloraxes(showscale=False)
c_graph_Air.update_xaxes(title_text="מדינות")
c_graph_Air.update_yaxes(title_text="איכות אוויר")


# city graph
if len(city_Air.index) > 100:
    bg_color = "rgb(77, 77, 77)"
else:
    bg_color = "rgb(26, 26, 26)"
fig_city_Air = px.bar(
    city_Air,
    x=city_Air["City"],
    y=city_Air["AirQuality"],
    range_y=[0, 100],
    title="זיהום האוויר בערים",
    template="plotly_dark",
    color_continuous_scale="Peach",
    range_color=[0, 100],
    color=city_Air["AirQuality"],
)
fig_city_Air.update_layout(
    title_x=0.5,
    font_size=20,
    hoverlabel_font_size=28,
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
)
fig_city_Air.update_coloraxes(showscale=False)
fig_city_Air.update_xaxes(title_text="ערים", nticks=5)
fig_city_Air.update_yaxes(title_text="")


# Air tab layout
Air = html.Div(
    id="big_container_Air",
    children=[
        html.Div(
            id="container_Air",
            className="container_Air",
            children=[
                html.H1(className="h1", children="זיהום אוויר"),
                html.Div(
                    className="container_barchart_country",
                    children=dcc.Graph(
                        id="barchart_country_Air",
                        className="barchart_country",
                        figure=c_graph_Air,
                    ),
                ),
                html.Div(
                    className="container_dropdown_c",
                    children=dcc.Dropdown(
                        id="countrys_Air",
                        className="dropdown_c",
                        options=[{"label": i, "value": i} for i in list_of_countrys],
                        multi=True,
                        placeholder="...בחר אילו מדינות תרצה להציג",
                    ),
                ),
                html.Div(
                    className="container_top_citys",
                    children=dcc.Graph(
                        id="top_citys_Air",
                        className="top_citys",
                        figure=fig_city_Air,
                    ),
                ),
                html.Button(
                    id="zero_button_Air",
                    className="zero_button",
                    children="הצגת ערכי אפס",
                ),
                html.Div(
                    className="container_range_city",
                    children=dcc.RangeSlider(
                        id="range_city_Air",
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
        html.Div(id="hide_container_Air", className="hide_container_Air", children=[]),
    ],
)


# country filter
@app.callback(
    Output("barchart_country_Air", "figure"), Input("countrys_Air", "value")
)
def coutrys_select(countrys):
    if countrys is None or countrys == []:
        return c_graph_Air

    elif countrys is not None:
        df = country_mean.loc[country_mean["Country"].isin(countrys)]
        df = df.sort_values(by=["AirQuality"], ascending=False)
        if len(df.index) > 100:
            bg_color = "rgb(77, 77, 77)"
        else:
            bg_color = "rgb(26, 26, 26)"
        fig = px.bar(
            df,
            x=df["Country"],
            y=df["AirQuality"],
            range_y=[0, 100],
            title="מדינות מזהמות לאחר בחירה",
            template="plotly_dark",
            color_continuous_scale="Peach",
            range_color=[0, 100],
            color=df["AirQuality"],
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
        fig.update_yaxes(title_text="איכות אוויר")
        return fig


# city filter
@app.callback(
    Output("top_citys_Air", "figure"),
    Output("range_city_Air", "value"),
    Output("barchart_country_Air", "hoverData"),
    Input("range_city_Air", "value"),
    Input("barchart_country_Air", "hoverData"),
    prevent_initial_update=True,
)

# show citys per hover country on first grafh
def city_graf_w(value, hovdata):
    filter_df = df.loc[
        (df["AirQuality"] >= value[0]) & (df["AirQuality"] <= value[1])
    ]

    # the varible that will be returned
    l = []
    # check if there is no value for a range
    if len(filter_df.index) == 0:
        value = [0, 100]

    filter_df = df.loc[
        (df["AirQuality"] >= value[0]) & (df["AirQuality"] <= value[1])
    ]

    filter_df = filter_df.sort_values(["AirQuality"], ascending=False)

    # all citys table
    if len(filter_df.index) > 100:
        bg_color = "rgb(77, 77, 77)"
    else:
        bg_color = "rgb(26, 26, 26)"
    fig = px.bar(
        filter_df,
        x=filter_df["City"],
        y=filter_df["AirQuality"],
        range_y=[0, 100],
        title=f"ערים מזהמות בטווח זיהום {value[0]}-{value[1]}",
        template="plotly_dark",
        color_continuous_scale="peach",
        range_color=[0, 100],
        color=filter_df["AirQuality"],
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
                y=hover_country_data["AirQuality"],
                range_y=[0, 100],
                title=(f"בטווח {value[0]}-{value[1]} {hov_country} זיהום האוויר בערי"),
                template="plotly_dark",
                color_continuous_scale="peach",
                range_color=[0, 100],
                color=hover_country_data["AirQuality"],
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
            value = [0, 100]
            hovdata = None
            l = [fig, value, hovdata]

    elif hovdata is None:
        l = [fig, value, hovdata]
    return l


# zero values table
@app.callback(
    Output("hide_container_Air", "children"),
    Output("hide_container_Air", "style"),
    Output("container_Air", "style"),
    Input("zero_button_Air", "n_clicks"),
    State("hide_container_Air", "style")
)
def zero_val_Air(zero_click, style):
    zero_vals = df.loc[df["AirQuality"] == 0]
    zero_vals = zero_vals.sort_values(by="Country")
    tabl = dash_table.DataTable(
        zero_vals.to_dict("records"),
        [{"name": i, "id": i} for i in df.columns],
        id="tbl_Air",
    )
    button=html.Button(id='tabl_button_Air',className='tabl_button', children='סגור')
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
    Output("zero_button_Air", "n_clicks"),
    Input('tabl_button_Air', 'n_clicks'),
    State("hide_container_Air", "style")
)

def click_adds(click_tabl_button, style_now):
    if click_tabl_button and style_now=={"display": "none"}:
        return 