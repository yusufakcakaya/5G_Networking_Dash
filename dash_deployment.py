import datetime
import json
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash
import pandas as pd
import plotly.graph_objs as go
from datetime import date

from plotly.subplots import make_subplots

# Build App
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# ----------------------------------------------------------------------
# .CSV FILES\

mun = pd.read_csv('data/demand_driven_municipality_capacity_results.csv')
townships = json.load(open("townships.geojson", "r"))
township_id = {}
for feature in townships['features']:
    feature['id'] = feature['properties']['name']
    township_id[feature['properties']['name']] = feature['id']

township_csv = []
for feature in mun.municipalities.unique():
    township_csv.append(feature)

for feature in township_csv:
    if feature not in township_id.keys():
        township_id[feature] = feature

mun['id'] = mun['municipalities'].apply(lambda x: township_id[x])

top_50 = mun.sort_values(by='capacity_margin', ascending=False).head(50)

low = mun.sort_values(by='capacity_margin', ascending=True).head(20)
low.capacity_margin = (low.capacity_margin * -1)

Amsterdam = mun[mun['id'] == 'Amsterdam']
Apeldoorn = mun[mun['id'] == 'Apeldoorn']

hybrid = (mun.query("strategy == 'Hybrid'"))
cell = (mun.query("strategy == 'Small Cells'"))
spectrum = (mun.query("strategy == 'Spectrum Integration'"))
S1 = (mun.query("scenario == 'Scenario 1 (30 Mbps)'"))
S2 = (mun.query("scenario == 'Scenario 2 (100 Mbps)'"))
S3 = (mun.query("scenario == 'Scenario 3 (300 Mbps)'"))

# ----------------------------------------------------------------------
# .CSV demand_driven_postcode_data_results.csv
post = pd.read_csv('data/demand_driven_postcode_data_results.csv')
limit = post.query("spectrum_limitations == 'all_spectrum'")
# ----------------------------------------------------------------------
# .CSV demand_driven_aggregate_cost_results
cost = pd.read_csv('data/demand_driven_aggregate_cost_results.csv')
cost['cost'] = cost['cost'].str.replace(',', '').astype(float)
sorted_cost = cost.sort_values(by=['cost'], ascending=True)
sorted_cost.loc[:, "cost"] = '€ ' + sorted_cost["cost"].map('{:,.0f}'.format)

# ----------------------------------------------------------------------
# .CSV demand_driven_aggregate_geotype_cost
geo = pd.read_csv('data/demand_driven_aggregate_geotype_cost.csv')
# ----------------------------------------------------------------------
# .CSV demand_driven_geotype_data_results

geopop = pd.read_csv('data/geopop.csv')
most_costy = geopop.sort_values(by='cost', ascending=False).head(50)
rural4 = geopop.query("geotype== 'Rural 4'")

# ----------------------------------------------------------------------

gt = pd.read_csv('data/demand_driven_aggregate_geotype_cost.csv')
gt.loc[:, "cost"] = '€' + gt["cost"].map('{:,.0f}'.format)

countries = ['China', ' Korea', 'United States of America', 'Spain', 'United Kingdom',
             'Canada', 'Australia', 'Saudi Arabia', 'Italy', 'Finland ']

# ------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------
Current_Date = datetime.datetime.today().strftime('%Y,%m,%d')
print('Current Date: ' + str(Current_Date))

year = int(Current_Date[:4])
month = int(Current_Date[5:7])
day = int(Current_Date[8:])


def drawTextHead(text):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H6(text),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


# Text field


def drawText(text):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.P(text),
                ], style={'text-align': 'center'})
            ])
        ),
    ])


# ------------------------------------------------------------------------------

buttons = html.Div(
    [
        dbc.Button("Nederland Map",
                   href='https://www.google.com/maps/place/Hollanda/@52.1951027,3.0368069,7z/data=!3m1!4b1!4m5!3m4!1s0x47c609c3db87e4bb:0xb3a175ceffbd0a9f!8m2!3d52.132633!4d5.291266',
                   color="primary"),
        dbc.Button("5G Plans",
                   href='https://www.government.nl/topics/ict/plans-for-5g-and-testing-antennas#:~:text=In%202020%20central%20government%20will,mobile%20network%20in%20the%20future.',
                   color="primary"),
        dbc.Button("Linkedin",
                   href='https://www.linkedin.com/in/yusuf-ak%C3%A7akaya-9526a0171/',
                   color="primary"),
        dbc.Button("GitHub",
                   href='https://github.com/yusufakcakaya/5G_Networking_Dash',
                   color="primary"),
        dbc.Button("World Population",
                   href='https://population.un.org/wpp/Download/Standard/CSV/',
                   color="primary"),
    ],
    className="d-grid gap-2 d-md-block",
)

app.layout = html.Div([
    html.Div(children=[
        html.H1('5G', style={'text-align': 'center'}),
        html.H1('Analysis of the Netherlands', style={'text-align': 'center'}),
        html.H1('🌍', style={'text-align': 'center'}),
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        drawText(
                            "The first generation mobile network began as a voice call of the network. The networks, which continue to develop in parallel with "
                            "the development of technology, have started to be insufficient today and have triggered a new change."
                            "5G enables a new kind of network that is designed to connect "
                            " virtually everyone and everything together including machines, objects, and devices.", ),
                        html.Div(
                            dcc.DatePickerSingle(
                                id='input-date-picker-single',
                                min_date_allowed=date(1950, 1, 1),
                                max_date_allowed=date(2100, 12, 30),
                                initial_visible_month=date(year, month, day),
                                calendar_orientation='vertical',
                                date=date(year, month, day)
                            )),
                        html.Div(id='output-container-date-picker-single'),

                    ], width=12)])])),
        html.P(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Card(
                        dbc.CardBody([

                            dcc.Graph(

                                id='output-world_population'
                            ),

                            html.Div("( World population can guess between 1950-2100 )",style={'text-align': 'center'})

                        ])
                    ),
                ])
            ], width=6),
            dbc.Col([
                html.Div([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(),
                            dcc.Graph(
                                figure=px.choropleth(locationmode="country names",
                                                     locations=countries, color=countries, scope='world'
                                                     ).update_layout(

                                    {'geo': {
                                        'projection': {
                                            'type': 'orthographic'  # default is 'orthographic' / 'equirectangular'
                                        },
                                        'scope': 'world',
                                    }},
                                    legend_title="Country",
                                    template='plotly_dark',
                                    title='World Top 5G Users',
                                    title_x=0.5

                                ),
                                config={
                                    'displayModeBar': False
                                }
                            ),

                            html.Div("( Top 10 countries with the most extensive 5G in 2022 )",style={'text-align': 'center'}),

                        ])
                    ),
                ])
            ], width=6),
        ], align='center'),
        html.P(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Card(
                        dbc.CardBody([

                            dcc.RadioItems(
                                id='option',
                                options=[' Scenario 1 ',
                                         ' Scenario 2 ',
                                         ' Scenario 3 ',
                                         ' Hybrid ',
                                         ' Small Cells ',
                                         ' Spectrum '],
                                value='S3',
                                inline=True
                            ),
                            dcc.Graph(id="graph")
                        ])
                    ),
                ])

            ], width=12),
        ], align='center'),

        html.P(),

        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        drawText('Latency ⏳ < 1ms')
                    ], width=4),
                    dbc.Col([
                        drawText('Peak Data Rates ⬆️ 20 Gb/s')
                    ], width=4),
                    dbc.Col([
                        drawText('More IoT Devices ⚙️')
                    ], width=4)
                ])])),
        html.P(),

        dbc.Card(
            dbc.CardBody([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.pie(top_50,
                                                      values='capacity_margin',
                                                      names='municipalities',
                                                      title="High Municipalities Margin "
                                                      ).update_layout(
                                            title_x=0.5,
                                            legend_title="Town",
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                        config={
                                            'displayModeBar': False
                                        }
                                    )
                                ])
                            ),
                        ])
                    ], width=6),

                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.pie(low,
                                                      values='capacity_margin',
                                                      names='municipalities',
                                                      title="Low Municipalities Margin "
                                                      ).update_layout(
                                            title_x=0.5,
                                            legend_title="Town",
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                        config={
                                            'displayModeBar': False
                                        }
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.choropleth_mapbox(Apeldoorn,
                                                                    geojson=townships,  # Assign geojson file
                                                                    locations='id',
                                                                    hover_name='id',
                                                                    hover_data=['scenario'],
                                                                    ).update_layout(
                                            template='plotly_dark',
                                            title='💰 Apeldoorn',
                                            title_x=0.5,
                                            mapbox_style="carto-positron",
                                            mapbox_zoom=6,
                                            mapbox_center={"lat": 52.2130, "lon": 5.2794}
                                        )
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.choropleth_mapbox(Amsterdam,
                                                                    geojson=townships,  # Assign geojson file
                                                                    locations='id',
                                                                    hover_name='id',
                                                                    hover_data=['scenario'],
                                                                    ).update_layout(
                                            template='plotly_dark',
                                            title='💣 Amsterdam',
                                            title_x=0.5,
                                            mapbox_style="carto-positron",
                                            mapbox_zoom=6,
                                            mapbox_center={"lat": 52.2130, "lon": 5.2794}
                                        )
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.scatter(top_50,
                                                          x="municipalities",
                                                          y="capacity_margin",
                                                          title="Margins Over Scenarios",
                                                          color="scenario",
                                                          size="capacity_margin"
                                                          ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                        config={
                                            'displayModeBar': False
                                        }
                                    )
                                ])
                            ),
                        ])
                    ], width=12),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.bar(sorted_cost,
                                                      x="scenario",
                                                      y="cost",
                                                      color="strategy",
                                                      title="Cost Over Scenario"
                                                      ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.bar(geo, x="geotype", y="cost", title="Geotype Cost"
                                                      ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    html.P(
                                        "Spectrum Integration Strategy"
                                    ),
                                    html.P("(2x10 MHz@700 MHz, 10 MHz@1500 MHz and 40 MHz@3.5 GHz)")
                                ], style={'text-align': 'center'})

                            ]))], width=6),
                    dbc.Col([dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.P(
                                    "Small Cell Strategy"
                                ),
                                html.P('(100 MHz@3.7 GHz)')
                            ], style={'text-align': 'center'})

                        ]))], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody([
                                html.Div([
                                    html.P(
                                        "Using population density data from the demand module, "
                                        "postcodes statistical units are grouped based on a set of boundaries representing "
                                        "different percentiles of the population. Seven settlement types are using: "
                                    ),
                                    html.P("   ‍👩‍👧‍👧👨‍👩‍👦‍👦👨‍👩‍👦‍👦‍‍‍ Suburban 1 ≥ 4046 persons per km2"),
                                    html.P("   👨‍👩‍👧‍👦👨‍👩‍👧‍👦 Suburban 2 ≥ 1949 persons per km2"),
                                    html.P("👩‍🦱👨‍🦱 Rural 1 ≥ 672 persons per km2"),
                                    html.P("‍👨‍🦰👧 Rural 2 ≥ 346 persons per km2"),
                                    html.P("‍👨‍🦰👧 Rural 3 ≥ 191 persons per km2"),
                                    html.P("👨‍🦳👩‍🦳 Rural 4 ≥ 0 persons per km2"),

                                ], style={'text-align': 'center'})

                            ]))], width=12),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.bar(geopop,
                                                      x="geotype",
                                                      y="capacity_margin",
                                                      color='population',
                                                      title="Geotype Margin Over Population",
                                                      ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.bar(geo, x="geotype", y="RAN.small.cells", color='scenario',
                                                      title="Geotype RAN Small Cells for Strategy",
                                                      ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.pie(most_costy,
                                                      values='cost',
                                                      names='geotype',
                                                      title="Geotype Cost Distribution"
                                                      ).update_layout(
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.histogram(rural4, x="strategy", y="capacity_margin", color='scenario',
                                                            title="Rural 4 Margin ",
                                                            ).update_layout(

                                            legend_title="Scenario",
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                html.Br(),
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.P(
                                        "⚡ New capabilities is the use of millimetre wave  frequency bands for transmission "
                                        "between roughly 30–300 GHz for mobile communications.")
                                ], style={'text-align': 'center'})
                            ], width=12)])])),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=go.Figure(data=[go.Bar(
                                            name='4G',
                                            x=limit['geotype'],
                                            y=limit['Existing.capacity'],
                                            offsetgroup=0),

                                            go.Bar(
                                                name='5G',
                                                x=limit['geotype'],
                                                y=limit['Capacity.surplus'],
                                                offsetgroup=1
                                            ),
                                        ], layout=go.Layout(
                                            title="Maximum Average Capacity Per User",
                                            title_x=0.5,
                                            yaxis_title="Capacity Mpbs",
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        )
                                        )
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                    dbc.Col([
                        html.Div([
                            dbc.Card(
                                dbc.CardBody([
                                    dcc.Graph(
                                        figure=px.histogram(geopop, x="strategy", y="capacity_margin", color='scenario',
                                                            title="Overall Geotype Margin ",
                                                            ).update_layout(

                                            legend_title="Scenario",
                                            title_x=0.5,
                                            template='plotly_dark',
                                            plot_bgcolor='rgba(0, 0, 0, 0)',
                                            paper_bgcolor='rgba(0, 0, 0, 0)',
                                        ),
                                    )
                                ])
                            ),
                        ])
                    ], width=6),
                ], align='center'),
                html.Br(),
                buttons

            ]), color='dark'
        )
    ]),
    ''' dcc.RadioItems(
        id='option',
        options=[S1, S2, S3],
        value=S3,
        inline=True
    ),
    dcc.Graph(id="graph")'''

])


@app.callback(
    Output("graph", "figure"),
    Input("option", "value"))
def display_choropleth(option):
    if option == ' Scenario 1 ':
        option = S1
    elif option == ' Scenario 2 ':
        option = S2
    elif option == ' Scenario 3 ':
        option = S3
    elif option == ' Hybrid ':
        option = hybrid
    elif option == ' Small Cells ':
        option = cell
    elif option == ' Spectrum ':
        option = spectrum
    else:
        option = mun

    fig = px.choropleth_mapbox(
        option,
        geojson=townships,
        locations='id',
        color='capacity_margin',
        hover_name='id')
    fig.update_layout(
        legend_title="Margin",
        template='plotly_dark',
        title='Nederland 5G Capacity Margin',
        title_x=0.5,
        mapbox_style="carto-positron",
        mapbox_zoom=6,
        mapbox_center={"lat": 52.2130, "lon": 5.2794})

    return fig


@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('input-date-picker-single', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')


@app.callback(
    Output('output-world_population', 'figure'),
    Input('input-date-picker-single', 'date'))
def world_population(date_value):
    date_object = date.fromisoformat(date_value)
    date_string = date_object.strftime('%B %d, %Y')
    g_year = date_string[-4:]

    pop = pd.read_csv('population.csv')
    graph_year = pop.query(f"Time=={g_year} & Variant == 'Low'")

    world_population_fig = px.choropleth(graph_year,
                                         locationmode="country names",
                                         locations=graph_year.Location,
                                         color=graph_year.PopTotal,
                                         )
    world_population_fig.update_geos(projection_type="orthographic")

    world_population_fig.update_layout(legend_title="Country",
                                       template='plotly_dark',
                                       title=f'World {g_year} Population',
                                       title_x=0.5)
    return world_population_fig


# Run app and display result inline in the notebook

###################################################
# Server Run
###################################################
if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=8000,
        dev_tools_hot_reload=True
    )
