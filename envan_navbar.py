#!/usr/bin/python3
"""
version 1.0.0 --- changelog
1) New struct as multipage dash app (details here: https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91)
Present file becomes app included in global structure
"""
import dash_bootstrap_components as dbc

def navbar():
    navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("impianto fotovoltaico", href="/imp_fv")),
              dbc.NavItem(dbc.NavLink("monitoraggio polveri", href="/dust_mon")),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",
        )
    return navbar
