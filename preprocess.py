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
