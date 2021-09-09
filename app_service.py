'''
MIT License

Optimal Testing and Containment Strategies for Universities in Mexico amid COVID-19

Copyright © 2021 Test and Contain. Luis Benavides-Vázquez, Héctor Alonso Guzmán-Gutiérrez, Jakob Jonnerby, Philip Lazos, Edwin Lock, Francisco J. Marmolejo-Cossío, Ninad Rajgopal,and José Roberto Tello-Ayala. https://www.testandcontain.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import dash
import dash_bootstrap_components as dbc

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/tables.css'], title="EAAMO demo", suppress_callback_exceptions=True)
app = dash_app.server