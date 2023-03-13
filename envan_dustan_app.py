#!/usr/bin/python3
"""
version 1.0.1 --- changelog
1) sum df date no more modify df itself
2) fix bug on mean value
3) added info image on dust limit

version 1.0.0 --- changelog
1) New struct as multipage dash app (details here: https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91)
Present file becomes app included in global structure
"""

import sys
import pandas as pd
# import dash
import dash_table
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from envan_navbar import navbar
# from dash.dependencies import Input, Output
# from flask import request
from envan_sparse import mlog, global_constants
import base64

DUST_DATA_FILE = 'dust-log.csv'
nav = navbar()

def dustan_read_csv_data():
    attempt = 0
    while attempt < global_constants["MAX_ATTEMPT"]:
        try:
            dust_dataframe = pd.read_csv(DUST_DATA_FILE)
            break
        except:
            attempt += 1
    if attempt >= global_constants["MAX_ATTEMPT"]:
        mlog('FATAL', "Could not read csv dust data")
        sys.exit("Error reading csv dust data")
    dust_dataframe.columns = ['date_time', 'info1', 'voltage_read','info2','dust_density']
    dust_dataframe['date_time'] = pd.to_datetime(dust_dataframe['date_time'], format='%d-%m-%Y@%H:%M:%S %z')
#    print(dust_dataframe['date_time'][0])
    return dust_dataframe


def dustan_restrict_data(df, date):
#    print(date)
    restdf = df.copy()
    restdf['date'] = restdf['date_time'].dt.date    # https://stackoverflow.com/questions/16176996/keep-only-date-part-when-using-pandas-to-datetime
#    print(restdf)
    restdf = restdf.loc[restdf['date'] == date]
    return restdf


def dustan_prepare_sum_data(df):
    rdf = df.copy()

    rdf.loc[:, 'dt'] = rdf['date_time'].shift(-1) - rdf['date_time']
    rdf.loc[:, 'dt'] = rdf['dt'].dt.total_seconds()

    rdf.loc[:, 'global_dust'] = rdf['dust_density'] * rdf['dt']  # calculate weight dust density (ugr/m3)
    day_total = rdf.sum(0, numeric_only=True)  # sum over the day
#    print(day_total)
    mean_dust = f"{day_total['global_dust']/day_total['dt']:.3f}"
#    print(mean_dust)

    return mean_dust


def dustan_app(df, current_date):
    global limit_date, x_axis, tab_status, old_num_clicks

    rdf = dustan_restrict_data(df, current_date)
    limit_image_filename = 'dust_limit.png'
    encoded_image = base64.b64encode(open(limit_image_filename, 'rb').read())

    if not rdf.empty:
        mean_dust = dustan_prepare_sum_data(rdf)
#        print('**', mean_dust)
        x_axis = "date_time"
        fig = go.Figure()
        fig.add_bar(x=rdf[x_axis], y=rdf["dust_density"], name='dust_density')
        fig.update_layout(title=" dati del giorno:  " + str(current_date.day) + "  -  " + str(current_date.month) + "  -  " +
                                str(current_date.year), showlegend=False)
    else:
        mean_dust = 0
        x_axis = "date_time"
        fig = go.Figure()
        fig.update_layout(title=" dati assenti alla data indicata ", showlegend=False)

    layout = html.Div([
        nav,
        html.H3("Rilevazione polveri PM 2.5 - S. Colombano L. - Italy", style={'text-align': 'center'}),
        html.H5("Position: N45.1815 - E9.4793 " + global_constants["SW_VERSION"], style={'text-align': 'center'}),
        html.Div([
            html.Table(
                html.Tr([
                    html.Td(
                        html.H5('*  year-month-day'),
                        ),
                    html.Td(
                        dcc.Dropdown(
                            id="dustan_slct_year",
                            className="per_sel_menu_tiny",
                            options=[
                                     {"label": "2019", "value": 2019},
                                     {"label": "2020", "value": 2020},
                                     {"label": "2021", "value": 2021},
                                     {"label": "2022", "value": 2022}],
                            multi=False,
                            value=current_date.year,
                            clearable=False
                        )
                    ),
                    html.Td(
                        dcc.Dropdown(
                            id="dustan_slct_month",
                            className="per_sel_menu_tiny",
                            options=[
                                 {"label": "jan", "value": 1},
                                 {"label": "feb", "value": 2},
                                 {"label": "mar", "value": 3},
                                 {"label": "apr", "value": 4},
                                 {"label": "may", "value": 5},
                                 {"label": "jun", "value": 6},
                                 {"label": "jul", "value": 7},
                                 {"label": "aug", "value": 8},
                                 {"label": "sep", "value": 9},
                                 {"label": "oct", "value": 10},
                                 {"label": "nov", "value": 11},
                                 {"label": "dec", "value": 12}],
                            multi=False,
                            value=current_date.month,
                            clearable=False
                        )
                    ),
                    html.Td(
                        dcc.Dropdown(
                            id="dustan_slct_day",
                            className="per_sel_menu_tiny",
                            options=[
                                {"label": "1", "value": 1},
                                {"label": "2", "value": 2},
                                {"label": "3", "value": 3},
                                {"label": "4", "value": 4},
                                {"label": "5", "value": 5},
                                {"label": "6", "value": 6},
                                {"label": "7", "value": 7},
                                {"label": "8", "value": 8},
                                {"label": "9", "value": 9},
                                {"label": "10", "value": 10},
                                {"label": "11", "value": 11},
                                {"label": "12", "value": 12},
                                {"label": "13", "value": 13},
                                {"label": "14", "value": 14},
                                {"label": "15", "value": 15},
                                {"label": "16", "value": 16},
                                {"label": "17", "value": 17},
                                {"label": "18", "value": 18},
                                {"label": "19", "value": 19},
                                {"label": "20", "value": 20},
                                {"label": "21", "value": 21},
                                {"label": "22", "value": 22},
                                {"label": "23", "value": 23},
                                {"label": "24", "value": 24},
                                {"label": "25", "value": 25},
                                {"label": "26", "value": 26},
                                {"label": "27", "value": 27},
                                {"label": "28", "value": 28},
                                {"label": "29", "value": 29},
                                {"label": "30", "value": 30}],
                            multi=False,
                            value=current_date.day,
                            clearable=False
                        )
                    ),
                    html.Td(
                        html.Button('update',
                                    id="dustan_update_date",
                                    className="button",
                                    n_clicks=0
                        )
                    ),
                    html.Td(
                        dcc.Dropdown(
                            id="dustan_slct_tab_data",
                            className="per_sel_menu_medium",
                            options=[
                                {"label": "nascondi tabella dati ", "value": 0},
                                {"label": "mostra tabella dati", "value": 1}],
                            multi=False,
                            value=0,
                            clearable=False
                        )
                    ),
                ])
            )],
        className="menu"),
        html.Br(),
        html.Div(
            html.Table(
                html.Tr([
                    html.Td(html.P('*   day data as ugr/m3')),
                    html.Td(html.P('medium density:')),
                    html.Td(
                            html.P(mean_dust, id="dustan_mean_dust"),
                            className='period_data'
                            )
                ])
            )

        ),
        html.Div(
            dcc.Graph(
                id='dustan_dataplot',
                figure=fig
            )
        ),
        html.Div([
            html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()), width=600)
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Div(
            dash_table.DataTable(
                id='dustan_req_data',
                columns=[{"name": i, "id": i} for i in rdf.columns],
                data=rdf.to_dict('records'),
                style_header={
                    'backgroundColor': 'rgb(80, 80, 80)',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontsize': '3rem'
                },
                style_cell={
                    'backgroundColor': 'rgb(100, 100, 100)',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'margin': '15px'
                }
            ),
            className='tab_data_to_display',
            id='dustan_period_data',
            style={'display': 'block'}
        )
        ])

    return layout
