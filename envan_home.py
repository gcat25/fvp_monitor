#!/usr/bin/python3
"""
version 1.0.1 --- changelog
1) minor changes in layout

version 1.0.0 --- changelog
1) New struct as multipage dash app (details here: https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91)
Present file becomes app included in global structure
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from envan_navbar import navbar
import base64

home_image_filename = 'google_sancol.png'
encoded_image = base64.b64encode(open(home_image_filename, 'rb').read())
nav = navbar()
body = html.Div([
        html.H2(" -- Energy and dust monitor @ S. Colombano L. - Italy. N 45.1815 - E 9.4793"),
        html.H3(" --  Plant nominal power 3 kW - East-West orientation"),
        html.Table([
             html.Tr([
                 html.Td([
                    html.P("Energy balance recordings since nov 2019."),
                    html.Br(),
                    html.P("Dust levels  recordings since jan 2021 ")],
                 ),
                 html.Td(
                     html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()), width=600),
                 ),
             ]),
        ])
      ])

def home():
    layout = html.Div([
    nav,
    body
    ])
    return layout

# app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
# app.layout = Homepage()
# if __name__ == "__main__":
#    app.run_server()
