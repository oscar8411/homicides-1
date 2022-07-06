import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
import os

#os.system('find . | grep -E "(.ipynb_checkpoints$|\.pyc$|\.pyo$)" | xargs rm -rf')
#os.rmdir('C:\Users\mjsoto\Documents\homicides\pages\.ipynb_checkpoints')

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.MINTY]
)

dl.print_registry()
navbar = dbc.NavbarSimple(
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("top_nav")
        ],
    ),
    brand="HOMICIDIOS EN COLOMBIA",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
