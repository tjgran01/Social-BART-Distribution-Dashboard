import pandas as pd
import plotly.express as px

import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from pathlib import Path

import statsmodels.api as sm
from statsmodels.formula.api import ols

from components import jumbotron, accordion

#### Main Function (Essentially) #####

features_of_non_interest = ["balloon_number", "pump_event_number", "start_pump",
                            "end_pump", "number_of_release_actions", "balloon_outcome",
                            "game_condition", "game_opponent", "id"]

balloon_wise_features = ["total_balloon_duration",
                         "total_pumps_for_balloon", "number_of_pump_actions",
                         "balloon_pop_point"]

pump_event_features = ["pump_event_duration", "onset_from_balloon_start", "pump_event_pumps"]

grouping_features = ["game_condition", "balloon_outcome", "game_opponent", "No Grouping"]

df = pd.read_csv("./test/sbart_balloon_features.csv")

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = dbc.Container(children=[
    jumbotron,
    accordion,
    dbc.Row([
        html.H2(children="Individual Variable Distributions"),
        dcc.Markdown('''
        To use the below graph chose the variable you wish to view from the "Select Variable To Look Over" dropdown menu.

        If you wish to compare two diffierent distributions, you can also select from the "Select Variable to Group by" dropdown.
        Bear in mind, however, that the distributions **are not ballanced in terms of their counts**. So, the shapes of the distributions
        are probably a more reasonable thing to view.

        Finally, there are some serious outliers in these distributions, which may make the graphs ... uninformative.
        To adjust these values use the "Min / Max Adjustments (To Manually Clamp Outliers)" range slider
        to set your mins and maxes accordingly.
        '''),

        html.Div(children=[
                            html.Label("Select Variable To Look Over: "),
                            dcc.Dropdown(
                                         id="var-select-x",
                                         options=[{"label": elm, "value": elm} for elm in df.columns if elm not in features_of_non_interest],
                                         multi=False,
                                         value="total_balloon_duration",
                                         style={"width": "70%"}
                                        ),
                            html.Label("Select Variable To Group By: "),
                            dcc.Dropdown(
                                         id="var-select-grouping",
                                         options=[{"label": elm, "value": elm} for elm in grouping_features],
                                         multi=False,
                                         value="No Grouping",
                                         style={"width": "70%"}
                                        ),
                            html.Label("Min / Max Adjustments (To Manually Clamp Outliers)"),
                            dcc.RangeSlider(
                                       id='max-slider',
                                      ),
                            dcc.Graph(id="dist-graph")
        ]
    )]),

    dbc.Row([
        html.H2(children="Trendlines"),
        html.Div(children=[
                            html.Label("Select X Variable To Look Over: "),
                            dcc.Dropdown(
                                         id="var-select-x-reg",
                                         options=[{"label": elm, "value": elm} for elm in df.columns if elm not in features_of_non_interest],
                                         multi=False,
                                         value="total_balloon_duration",
                                         style={"width": "70%"}
                                        ),
                            html.Label("Select Y Variable To Look Over: "),
                            dcc.Dropdown(
                                         id="var-select-y-reg",
                                         options=[{"label": elm, "value": elm} for elm in df.columns if elm not in features_of_non_interest],
                                         multi=False,
                                         value="total_balloon_duration",
                                         style={"width": "70%"}
                                        ),
                            dcc.Dropdown(
                                         id="grouping-reg",
                                         options=[{"label": elm, "value": elm} for elm in grouping_features],
                                         multi=False,
                                         value="No Grouping",
                                         style={"width": "70%"}
                                        ),
                            dcc.Graph(id="reg-graph")
        ]
    )]),

    dbc.Row([
        html.H2(children="Individual Participant Exploration"),
        html.Label("Select Participant To Look Over: "),

        dcc.Dropdown(
                     id="par-select",
                     options=[{"label": elm, "value": elm} for elm in df["id"].unique()],
                     multi=False,
                     value=1,
                     style={"width": "70%"}
                    ),

        html.Label("Select Opponent: "),

        dcc.Dropdown(
                     id="opponent-select",
                     style={"width": "70%"}
                    ),

        dbc.Col([
            html.Div(children=[
                dcc.Graph(id="par-line-pep"),

        ])
        ], width=6),

        dbc.Col([
            html.Div(children=[
                dcc.Graph(id="par-line-delay"),
        ])
        ], width=6),
    ]),
])

#### Main Function (Essentially) #####
@app.callback(
    Output('max-slider', 'min'),
    Output('max-slider', 'max'),
    Output('max-slider', 'marks'),
    Output('max-slider', 'value'),
    Input('var-select-x', 'value'),
    )

def update_max_slider(x_var):
    marks = {
             df[x_var].min(): {"label": f"{df[x_var].min()}"},
             df[x_var].max(): {"label": f"{df[x_var].max()}"}
            }

    values = [df[x_var].min(), df[x_var].max()]
    return df[x_var].min(), df[x_var].max(), marks, values

#### Callabcks #### GRAPHS

@app.callback(
    Output('dist-graph', 'figure'),
    Input('var-select-x', 'value'),
    Input('max-slider', 'value'),
    Input('var-select-grouping', 'value'),
    )

def update_figure(x_var, clamps, grouping):

    if x_var in balloon_wise_features:
        samples = df[df["onset_from_balloon_start"] == 0]
    else:
        samples = df
        if x_var == "onset_from_balloon_start":
            samples = df[df["onset_from_balloon_start"] != 0]

    samples = samples[samples[x_var] <= clamps[1]]
    samples = samples[samples[x_var] >= clamps[0]]

    if grouping != "No Grouping":
        fig = px.histogram(samples, x=x_var, color=grouping, marginal="rug")
    else:
        fig = px.histogram(samples, x=x_var, marginal="rug")

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('reg-graph', 'figure'),
    Input('var-select-x-reg', 'value'),
    Input('var-select-y-reg', 'value'),
    Input('grouping-reg', 'value')
    )

def update_figure(x_var, y_var, grouping):

    samples = df

    if grouping != "No Grouping":
        fig = px.scatter(samples, x=x_var, y=y_var, color=grouping, trendline='ols')
    else:
        fig = px.scatter(samples, x=x_var, y=y_var, trendline='ols')

    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('par-line-pep', 'figure'),
    Input('par-select', 'value'),
    Input('opponent-select', 'value')
    )

def update_par_figure(ids, opp):

    if opp:
        ids = [ids, opp]

    if isinstance(ids, list):
        samples = df[df["id"].isin(ids)]
    else:
        samples = df[df["id"] == id]

    fig = px.line(samples, x="balloon_number", y="pump_event_pumps", color="id")
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('par-line-delay', 'figure'),
    Input('par-select', 'value'),
    Input('opponent-select', 'value')
    )

def update_par_figure_1(ids, opp):

    if opp:
        ids = [ids, opp]

    if isinstance(ids, list):
        samples = df[df["id"].isin(ids)]
    else:
        samples = df[df["id"] == id]

    fig = px.line(samples, x="balloon_number", y="total_pumps_for_balloon", color="id")
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output('opponent-select', 'options'),
    Input('par-select', 'value')
)

def show_opponents(id):

    samples = df[df["id"] == id]
    return [{"label": elm, "value": elm} for elm in samples["game_opponent"].unique()]


if __name__ == '__main__':
    app.run_server(debug=True)
