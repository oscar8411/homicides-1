from dash import html, dcc
from dash_labs.plugins import register_page

import dash_bootstrap_components as dbc
import pandas as pd
import pickle
import plotly.graph_objects as go

from app_dataframe import df_hom

register_page(
    __name__,
    top_nav=True,
    order=5
    )

def layout():
    return dbc.Row([dbc.Col('', width=12),
                    ])
