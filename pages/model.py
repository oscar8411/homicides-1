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

def sarimax_forecast_city(SARIMAX_model, df, periods):
    # Forecast
    n_periods = periods

    forecast_df = pd.DataFrame({"month_index":pd.date_range(df.index[-1], periods = n_periods, freq='MS').month},
                    index = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods = n_periods, freq='MS'))

    fitted, confint = SARIMAX_model.predict(n_periods=n_periods, 
                                            return_conf_int=True,
                                            exogenous=forecast_df[['month_index']])
    index_of_fc = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods = n_periods, freq='MS')

    # make series for plotting purpose
    fitted_series = pd.Series(fitted, index=index_of_fc)
    lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    upper_series = pd.Series(confint[:, 1], index=index_of_fc)
    return fitted_series

# Create figure
def graficar():

    df = df_hom[['fecha','cantidad']]

    df = df.set_index('fecha')
    df = df.resample('M').sum()
    df.columns = ['total']
    df['month_index'] = df.index.month

    name = 'model/SARIMAX_total.pkl'

    with open(name, 'rb') as pkl:
        SARIMA_model = pickle.load(pkl)
        a = sarimax_forecast_city(SARIMA_model,df, 5)

    df = df.reset_index()
    df_2 = a.to_frame().reset_index()
    df_2.columns = ['fecha','total']
    df_2

    x1 = df['fecha']
    y1 = df['total']
    x2 = df_2['fecha']
    y2 = df_2['total']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1,
                        mode='lines',
                        name='original'))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                        mode='lines',
                        name='fitted'))
    grafica = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '80vh', 'display': 'inline-block'})
    return grafica

def layout():
    return dbc.Row([dbc.Col(graficar(), width=12),
                    ])
