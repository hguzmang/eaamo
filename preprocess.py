'''
MIT License

Optimal Testing and Containment Strategies for Universities in Mexico amid COVID-19

Copyright © 2021 Test and Contain. Luis Benavides-Vázquez, Héctor Alonso Guzmán-Gutiérrez, Jakob Jonnerby, Philip Lazos, Edwin Lock, Francisco J. Marmolejo-Cossío, Ninad Rajgopal,and José Roberto Tello-Ayala. https://www.testandcontain.com/

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import pandas as pd
import json
import gettext

cat_file='categories.json'

# Set up localisation
locale = 'en'


with open('data/' + cat_file) as file:        
        campuses = json.load(file)[0][locale]
        categories = campuses['campus1']['categories']
population = {'name': 'University', 'size': sum(cat['size'] for cat in categories)}

if locale == 'es':
    population['name'] = 'Universidad'

# Rename the column names of dataframe so that we don't run into surprises down the road.
health_label = ['Health']

# Any other module can now import the variables in this file, including
# categories, population, k
# df
# etc.

# Compute figure to show when there are no solutions
import plotly.graph_objects as go
blank_fig = go.Figure()
blank_fig.add_annotation(xref="paper", yref="paper",
                         showarrow=False, text="No solution found.",
                         font=dict(size=24,
                         color="purple"))
blank_fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))


tr = gettext.translation('base', localedir='locales', languages=[locale])
tr.install()
_ = tr.gettext
