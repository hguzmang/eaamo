import preprocess  # this needs to be imported first!

from app_service import dash_app, app
import callbacks
import dash
import dash_core_components as dcc
import dash_html_components as html

if __name__ == '__main__':
    dash_app.run_server(debug=True, host="0.0.0.0", port="8050")