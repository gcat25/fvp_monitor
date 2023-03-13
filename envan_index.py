#!/usr/bin/python3

"""
version 1.0.2 --- changelog
1) log date of data request

version 1.0.1 --- changelog
1) fix minor bugs

version 1.0.0 --- changelog
1) New struct as multipage dash app (details here: https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91)
Present file becomes app included in global structure
"""
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from envan_sparse import mlog
from envan_fvan_app import fvan_app as fvan
from envan_fvan_app import fvan_read_csv_data, fvan_restrict_data, fvan_prepare_sum_data
from envan_dustan_app import dustan_app as dustan
from envan_dustan_app import dustan_read_csv_data, dustan_restrict_data, dustan_prepare_sum_data

from envan_home import home
from flask import request

tab_status = 'hidden'
old_num_clicks = 0    # clicks to update button - global
# -------------- external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['fvp.css']

mlog('INFO', 'program started')
fv_df = fvan_read_csv_data()
dust_df = dustan_read_csv_data()
#current_date = pd.to_datetime('2020-11-27').date()
current_date = pd.to_datetime('today').date()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
            )
def display_page(pathname):
    if pathname == '/imp_fv':
        return fvan(fv_df, current_date)
    if pathname == '/dust_mon':
        return dustan(dust_df, current_date)
    else:
        return home()

@app.callback(
    [Output('fvan_req_data', 'data'),
     Output('fvan_dataplot', 'figure'),
     Output('fvan_period_data', 'style'),
     Output('fvan_prod_td', 'children'),
     Output('fvan_gcons_td', 'children'),
     Output('fvan_ncons_td', 'children'),
     Output('fvan_deliv_td', 'children')],
    [Input('fvan_slct_year', 'value'),
     Input('fvan_slct_month', 'value'),
     Input('fvan_slct_day', 'value'),
     Input('fvan_slct_data_to_display', 'value'),
     Input('fvan_slct_tab_data', 'value'),
     Input('fvan_update_date', 'n_clicks')]
    )
def update_fvan_output(y, m, d, sel_data_todisp, tabdata_flag, num_clicks):
    global current_date, tab_status, old_num_clicks

    graph_switcher = [
    {
        1: "power 1",
        2: "power 2",
        3: "stringa est",
        4: "stringa ovest"
    },
    {
        1: "delivered",
        2: "consumption",
        3: "verso grid",
        4: "consumo interno"
    }]
    try_date = pd.to_datetime(str(y) + '-' + str(m) + '-' + str(d)).date()

    to_log = 'fv data updated for: ' + str(request.remote_addr) + " @date: " + str(y) + '-' + str(m) + '-' + str(d)
    mlog('INFO PFV', to_log)
    fv_df = fvan_read_csv_data()    # new data read
#    print(num_clicks, '-', old_num_clicks, '\n')

    if num_clicks > old_num_clicks:
        current_date = try_date
        old_num_clicks = num_clicks

    rdf = fvan_restrict_data(fv_df, current_date)
    if not rdf.empty:
        e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f = fvan_prepare_sum_data(rdf)
        fig = go.Figure()
        x_axis = "date_time"
        fig.add_bar(x=rdf[x_axis], y=rdf[graph_switcher[sel_data_todisp].get(1)], name=graph_switcher[sel_data_todisp].get(3))
        fig.add_bar(x=rdf[x_axis], y=rdf[graph_switcher[sel_data_todisp].get(2)], name=graph_switcher[sel_data_todisp].get(4))
        fig.update_layout(title=" dati del giorno:  " + str(current_date.day) + "  -  " + str(current_date.month)
                                + "  -  " + str(current_date.year), showlegend=False)
    else:
        e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f = 0, 0, 0, 0
        x_axis = "date_time"
        fig = go.Figure()
        fig.update_layout(title=" dati assenti alla data indicata ", showlegend=False)

    if tabdata_flag == 0:
        tab_status = {'display': 'none'}
    else:
        tab_status = {'display': 'block'}

    return (rdf.to_dict('records'),         # see here: https://github.com/plotly/dash/issues/666
            fig, tab_status,
            e_prod_f, e_gross_cons_f, e_net_cons_f, e_delivered_f
            )

@app.callback(
    [Output('dustan_req_data', 'data'),
     Output('dustan_dataplot', 'figure'),
     Output('dustan_period_data', 'style'),
     Output('dustan_mean_dust', 'children')],
    [Input('dustan_slct_year', 'value'),
     Input('dustan_slct_month', 'value'),
     Input('dustan_slct_day', 'value'),
     Input('dustan_slct_tab_data', 'value'),
     Input('dustan_update_date', 'n_clicks')]
    )
def update_dustan_output(y, m, d, tabdata_flag, num_clicks):
    global current_date, tab_status, old_num_clicks

    try_date = pd.to_datetime(str(y) + '-' + str(m) + '-' + str(d)).date()

    to_log = 'dust data updated for: ' + str(request.remote_addr) + " @date: " + str(y) + '-' + str(m) + '-' + str(d)
    mlog('INFO_DUST', to_log)
    dust_df = dustan_read_csv_data()    # new data read


    if num_clicks > old_num_clicks:
        current_date = try_date
        old_num_clicks = num_clicks

    rdf = dustan_restrict_data(dust_df, current_date)
    if not rdf.empty:
        mean_dust = float(dustan_prepare_sum_data(rdf))
#        print(rdf)
#        print(mean_dust)
        fig = go.Figure()
        x_axis = "date_time"
        fig.add_bar(x=rdf[x_axis], y=rdf["dust_density"], name="dust_density")
        fig.update_layout(title=" dati del giorno:  " + str(current_date.day) + "  -  " + str(current_date.month)
                                + "  -  " + str(current_date.year), showlegend=False)
    else:
        mean_dust = 0
#        x_axis = "date_time"
        fig = go.Figure()
        fig.update_layout(title=" dati assenti alla data indicata ", showlegend=False)

    if tabdata_flag == 0:
        tab_status = {'display': 'none'}
    else:
        tab_status = {'display': 'block'}

    return (rdf.to_dict('records'),         # see here: https://github.com/plotly/dash/issues/666
            fig,
            tab_status,
            mean_dust
            )




if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)