import dash
import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/tables.css'], title="Test & Contain", suppress_callback_exceptions=True)
app = dash_app.server