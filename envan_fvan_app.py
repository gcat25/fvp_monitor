#!/usr/bin/python3
"""
version 1.0.1 --- changelog
1) sum df date no more modify df itself

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

FV_DATA_FILE = 'aurora-log.csv'
nav = navbar()

def fvan_read_csv_data():
    attempt = 0
    while attempt < global_constants["MAX_ATTEMPT"]:
        try:
            fv_dataframe = pd.read_csv(FV_DATA_FILE)
            break
        except:
            attempt += 1
    if attempt >= global_constants["MAX_ATTEMPT"]:
        mlog('FATAL', "Could not read csv fv data")
        sys.exit("Error reading csv fvpanels data")
#    fv_dataframe = pd.read_csv(FV_DATA_FILE)  # now file reading is checked for errors ---- see above
    fv_dataframe.columns = ['date_time', 'power 1', 'power 2', 'delivered', 'consumption']
    fv_dataframe['date_time'] = pd.to_datetime(fv_dataframe['date_time'], format='%d/%b/%Y@%H:%M:%S')
    return fv_dataframe


def fvan_restrict_data(df, date):
#    print(date)
    restdf = df.copy()
    restdf['date'] = restdf['date_time'].dt.date    # https://stackoverflow.com/questions/16176996/keep-only-date-part-when-using-pandas-to-datetime
    restdf = restdf.loc[restdf['date'] == date]
    return restdf


def fvan_prepare_sum_data(df):
    rdf = df.copy()

    rdf.loc[:, 'dt'] = rdf['date_time'].shift(-1) - rdf['date_time']
    rdf.loc[:, 'dt'] = rdf['dt'].dt.total_seconds()

    rdf.loc[:, 'e_prod'] = rdf['delivered'] * rdf['dt']  # calculate production (kwh)
    rdf.loc[:, 'e_gross_cons'] = rdf['consumption'] * rdf['dt']  # calculate gross compsumption

    # calculate net consumption - see: https://datatofish.com/if-condition-in-pandas-dataframe/ ...
    rdf.loc[rdf['e_prod'] >= rdf['e_gross_cons'], 'e_net_cons'] = 0
    rdf.loc[rdf['e_prod'] < rdf['e_gross_cons'], 'e_net_cons'] = rdf['e_gross_cons'] - rdf['e_prod']
    # ... and energy delivered to grid
    rdf.loc[rdf['e_prod'] >= rdf['e_gross_cons'], 'e_delivered'] = rdf['e_prod'] - rdf['e_gross_cons']
    rdf.loc[rdf['e_prod'] < rdf['e_gross_cons'], 'e_delivered'] = 0
#    rdf.loc[:, 'e_delivered'] = 500  # fake for test ??
#    rdf.loc[:, 'e_net_cons'] = 500  #
    day_total = rdf.sum(0) / 3600000    # data in KWh

    e_prod_f = f"{day_total['e_prod']:.3f}"
    e_gross_cons_f = f"{day_total['e_gross_cons']:.3f}"
    e_net_cons_f = f"{day_total['e_net_cons']:.3f}"
    e_delivered_f = f"{day_total['e_delivered']:.3f}"

    return e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f


def fvan_app(df, current_date):
    global limit_date, x_axis, tab_status, old_num_clicks, SW_VERSION

    rdf = fvan_restrict_data(df, current_date)

    if not rdf.empty:
        e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f = fvan_prepare_sum_data(rdf)
        x_axis = "date_time"
        fig = go.Figure()
        fig.add_bar(x=rdf[x_axis], y=rdf["power 1"], name='stringa est')
        fig.add_bar(x=rdf[x_axis], y=rdf["power 2"], name='stringa ovest')
        fig.update_layout(title=" dati del giorno:  " + str(current_date.day) + "  -  " + str(current_date.month) + "  -  " +
                                str(current_date.year), showlegend=False)
    else:
        e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f = 0, 0, 0, 0
        x_axis = "date_time"
        fig = go.Figure()
        fig.update_layout(title=" dati assenti alla data indicata ", showlegend=False)

    layout = html.Div([
        nav,
        html.H3("Analisi impianto FV - S. Colombano L. - Italy", style={'text-align': 'center'}),
        html.H5("Position: N45.1815 - E9.4793 - presentation sw vers. : " + global_constants["SW_VERSION"], style={'text-align': 'center'}),
        html.Div([
            html.Table(
               html.Tr([
                    html.Td(
                        html.H5('  year-month-day'),
                        ),
                    html.Td(
                        dcc.Dropdown(
                            id="fvan_slct_year",
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
                            id="fvan_slct_month",
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
                            id="fvan_slct_day",
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
                                    id="fvan_update_date",
                                    className="button",
                                    n_clicks=0
                        )
                    ),
                    html.Td(
                        dcc.Dropdown(
                            id="fvan_slct_data_to_display",
                            className="per_sel_menu_medium",
                            options=[
                                {"label": "string power", "value": 0},
                                {"label": "delivered & consumption", "value": 1}],
                            multi=False,
                            value=0,
                            clearable=False
                        )
                    ),
                    html.Td(
                        dcc.Dropdown(
                            id="fvan_slct_tab_data",
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
                    html.Td(html.P('day data (kwh)')),

                    html.Td(html.P('gross production:')),
                    html.Td(
                            html.P(e_prod_f, id="fvan_prod_td"),
                            className='period_data'
                            ),
                    html.Td(html.P('gross consumption:')),
                    html.Td(
                            html.P(e_gross_cons_f, id="fvan_gcons_td"),
                            className='period_data'
                           ),
                    html.Td(html.P('net consumption:')),
                    html.Td(
                            html.P(e_net_cons_f, id="fvan_ncons_td"),
                            className='period_data'
                            ),
                    html.Td(html.P('energy to grid:')),
                    html.Td(
                            html.P(e_delivered_f, id="fvan_deliv_td"),
                            className='period_data'
                           )
                ])
            )

        ),
        html.Div(
            dcc.Graph(
                id='fvan_dataplot',
                figure=fig
            )
        ),
        html.Div(
            dash_table.DataTable(
                id='fvan_req_data',
                columns=[{"name": i, "id": i} for i in df.columns],
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
            id='fvan_period_data',
            style={'display': 'block'}
        )
        ])

    return layout
