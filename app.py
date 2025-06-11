from dash import Dash, Input, Output, dcc, html
import dash_customizable_app_style as dcas
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
import copy
from figures import plots


df:             pd.DataFrame    = pd.read_csv("https://raw.githubusercontent.com/plotly/Figure-Friday/refs/heads/main/2025/week-23/steak-risk-survey.csv")
options:        list            = list (df.columns)[2:]
colors:         list            = ["#00FF98", "#00E1FF", "#4600CF", "#C8FF00", "#0021FF", "#E600FF", "#FF002E", "#FFF300", "#37FF00", "#00FFFA"]

grid                            = plots.create_grid(df)
choropleth_regions_fig          = plots.create_choropleth(df, "Census Division")
choropleth_counts_fig           = plots.create_choropleth(df, "Count", "Cividis")

app = Dash ("Figure Friday week 23", external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(
    id       = "main_container",
    style    = {"minHeight": "100vh"},
    children = [

        dcas.customize_app_selectors(),
        html.H1("Steak Risk Survey", className="p-4 bg-light text-primary mb-0"),
        grid,

        html.Div(
            id          = "main_div",
            className   = "m-0 p-2 w-100",
            children    = [
                html.Div(
                    className   = "row m-0 p-0",
                    children    = [
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_1", figure = choropleth_regions_fig),
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className   = "col-6 m-0 p-0",
                            children    = [
                                dcc.Loading(
                                    type        = 'cube',
                                    children    = [
                                        dcc.Graph(id = "choropleth_2", figure = choropleth_counts_fig),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className   = "col-12 m-0 p-0",
                    children    = [
                        dcc.Dropdown(
                            className   = "text-dark",
                            id          = "variable_1",
                            options     = options[0:8],
                            value       = options[0],
                        ),
                        dcc.Dropdown(
                            className   = "text-dark",
                            id          = "variable_2",
                            options     = options[7:],
                            value       = options[8],
                        ),
                        dcc.Loading(
                            type        = 'cube',
                            children    = [
                                dcc.Graph(id = "figure_1")
                            ]
                        )
                    ]
                )
            ])

    ])

@app.callback(
    Output("figure_1",      'figure'),
    Output("choropleth_1",  "figure"),
    Output("choropleth_2",  "figure"),
    Input('variable_1',     'value'),
    Input('variable_2',     'value'),
    Input("bg_color",       "value"),
    Input("text_color",     "value"),
    Input("font_type",      "value"),
)
def two_variable_corssfiltering(variable_1, 
                                variable_2, 
                                bg_color, 
                                text_color, 
                                font_type):

    filtered_df:    pd.DataFrame    = df[[variable_1, variable_2]].dropna(how="any")

    options_lst:    list            = [variable_1, variable_2]
    cat_orders:     dict            = {cat:sorted(set(list(filtered_df[cat]))) for cat in options_lst}

    figure:         Figure          = px.histogram(
                                            data_frame                = filtered_df, 
                                            x                         = variable_2, 
                                            facet_row                 = variable_1, 
                                            color                     = variable_2, 
                                            color_discrete_sequence   = colors,
                                            category_orders           = cat_orders,
                                            title                     = variable_1)
    
    figure.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]) if "=" in a.text else a.update(text=a.text))

    figure.update_layout(
        paper_bgcolor   = bg_color,
        plot_bgcolor    = bg_color,
        font_family     = font_type,
        font_color      = text_color,
        height          = 500,
        bargap          = 0.01
    )

    figure.update_xaxes(showline            = True,
                        showgrid            = False,
                        linewidth           = 0.5,
                        linecolor           = "#E7E7E7",
                        mirror              = True,
                        zeroline            = False)
    figure.update_yaxes(showline            = False,
                        showgrid            = False,
                        linewidth           = 0.5,
                        linecolor           = "#E7E7E7",
                        mirror              = False,
                        zeroline            = False)
    
    choro_1 = copy.deepcopy(choropleth_regions_fig)
    choro_2 = copy.deepcopy(choropleth_counts_fig)

    choro_1.update_layout(  paper_bgcolor   = bg_color,
                            font_family     = font_type,
                            font_color      = text_color)
    choro_1.update_geos(    bgcolor         = bg_color)

    choro_2.update_layout(  paper_bgcolor   = bg_color,
                            font_family     = font_type,
                            font_color      = text_color)
    choro_2.update_geos(    bgcolor         = bg_color)

    return figure, choro_1, choro_2

if __name__ == "__main__":
    app.run(debug=True)