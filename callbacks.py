import dash
import time, random, pandas as pd, json
from dash.dash import no_update
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State, MATCH, ALL
from app import dash_app

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from preprocess import blank_fig, health_label
from preprocess import population, _, campuses

from layout import get_layout
import flask
import numpy as np
import os
from dash.exceptions import PreventUpdate

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@dash_app.callback(
   Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    print ("Displaying", pathname)
    if pathname == '/':
        dash.callback_context.response.set_cookie('campus_cookie', "/campus1")
        return get_layout(len(campuses["campus1"]["categories"]), campuses["campus1"]["no_solutions"], campuses["campus1"]["budget"], campuses["campus1"]["buckets"], campuses["campus1"]["d"], campuses["campus1"]["pi"], campuses["campus1"]["p"], campuses["campus1"]["categories"])
    else:
        dash.callback_context.response.set_cookie('campus_cookie', pathname)
        
        return get_layout(len(campuses[pathname[1:]]["categories"]), campuses[pathname[1:]]["no_solutions"], campuses[pathname[1:]]["budget"], campuses[pathname[1:]]["buckets"], campuses[pathname[1:]]["d"], campuses[pathname[1:]]["pi"], campuses[pathname[1:]]["p"], campuses[pathname[1:]]["categories"])
    
    
@dash_app.callback(
    [Output(component_id='location-label', component_property='children'),
    Output('campus_id', 'data')
    ],   
    [
    Input('page-content', 'children')
    ]
)

def update_campus(page_content):
    allcookies=dict(flask.request.cookies)
    if 'campus_cookie' in allcookies:
        campus_id_prev = allcookies['campus_cookie']
    if (campus_id_prev is None):
        return campuses['campus1']['label'],"campus1"
    return campuses[campus_id_prev[1:]]['label'],campus_id_prev[1:]

def get_fig(solution, campus_id):
    """Generates figure from a solution row."""
    categories = campuses[campus_id]['categories']
    k = len(categories)
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=[_("# Unnecessarily self-isolating individuals"),
                                        _("# Prevented critical infections")],
                        specs=[[{}], [{}]], shared_xaxes=False,
                    shared_yaxes=False, vertical_spacing=0.25, row_heights=[k, 1])
    # Create subfigures
    contain_labels = [f'Containment {i}' for i in range(1,k+1)]
    y_prev=[cat['name'] for cat in categories]
    x_prev=solution[contain_labels]
    x_prev=np.trunc(x_prev).astype(int).tolist()
    contain_fig = go.Bar(
                x=x_prev,
                y=[y_prev[i]+"<br>("+str(x_prev[i])+")   " for i in range(k)],
                marker=dict(color='purple',
                            line=dict(color='black', width=0)),
                orientation='h')
    x_prev = -solution[health_label]
    x_prev=np.trunc(x_prev).astype(int).tolist()
    y_prev = [population['name']]
    health_fig = go.Bar(
                x=x_prev,#-solution[health_label],
                y=[y_prev[i]+"<br>("+str(x_prev[i])+")   " for i in range(len(y_prev))],#y_prev,#[population['name']],
                marker=dict(color=['orange'],
                            line=dict(color='black', width=0)),
                orientation='h')
    # Add subfigures to fig
    fig.append_trace(contain_fig, 1, 1)
    fig.append_trace(health_fig, 2, 1)
    # Add annotation to end of containment bars
    #for i in range(k):
    #    count = int(solution[contain_labels][i])
    #    fig.add_annotation(xref='x1', yref='y1', x=count, y=i, xshift=10, xanchor="left", text=str(count), showarrow=False)

    # Add annotation to end of health bar
    #count = int(-solution[health_label])
    #fig.add_annotation(xref='x2', yref='y2', x=count, xshift=10, y=0, xanchor="left", text=str(count), showarrow=False)

    # Fix the x-axis of health bar subplot
    fig.update_xaxes(range=[0, sum(cat['size'] for cat in categories)], row=2, col=1)

    fig.layout.update(margin=dict(l=0, r=10, t=20, b=0),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      showlegend=False)
    fig.update_yaxes(autorange='reversed')
    fig.layout.height = 300
    return fig

@dash_app.callback(
    [Output({'type': 'threshold', 'index': MATCH}, 'value'),
    Output({'type': 'threshold', 'index': MATCH}, 'max'),
    Output({'type': 'categories_size', 'index': MATCH}, 'children')],
    Input('campus_id','data'),
    State({'type': 'threshold', 'index': MATCH}, 'id')

)

def update_size_treshold(campus_id, id):
    """Update the size"""
    print("Running 'update_size_threshold'.")  
    categories = campuses[campus_id]['categories']
    i = int(id['index'])
    if campus_id is not None: 
        thres_size_string = int(categories[i]['size'])
    else:
        thres_size_string = None
    return thres_size_string, thres_size_string, thres_size_string

@dash_app.callback(
    [Output({'type': 'threshold_h'}, 'value'),
    Output({'type': 'threshold_h'}, 'max'),
    Output({'type': 'population_size'},'children')],
    Input('campus_id','data')
)
def update_size_threshold_Healt(campus_id):
    print("Running 'update_size_threshold_Healt'.", campus_id) 
    if campus_id is not None:  
        population = campuses[campus_id]['population']
    return 0, population, population
    
@dash_app.callback(
    Output({'type': 'categories_name', 'index': MATCH}, 'children'),
    Output({'type': 'sol_name', 'index': MATCH}, 'children'),
    Input('campus_id','data'),
    State({'type': 'threshold', 'index': MATCH}, 'id')

)
def update_names(campus_id, id):
    """Update the names"""
    print("Running 'update_names'.", campus_id)  
    categories = campuses[campus_id]['categories'] 
    if campus_id is not None:
        i = int(id['index'])
        return f"{categories[i]['name']}",f"{categories[i]['name']}"
    else:
        return None

@dash_app.callback(
    Output({'type': 'percent', 'index': MATCH}, 'children'),
    Input({'type': 'threshold', 'index': MATCH}, 'value'),
    Input('campus_id','data'),
    State({'type': 'threshold', 'index': MATCH}, 'id')
)
def update_percentage(threshold, campus_id, id):
    """Update the percentage box corresponding to the threshold value that was updated."""
    print("Running 'update_percentage'.") 
    categories = campuses[campus_id]['categories'] 
    i = int(id['index'])
    if threshold is not None:
        div = int(categories[i]['size'])
        percentage =  0 if (div == 0) else (int(threshold) * 100 / div)
        return f"{round(percentage, 2)}%"
    else:
        return f"100%"

@dash_app.callback(
    Output({'type': 'percent_h'}, 'children'),
    Input({'type': 'threshold_h'}, 'value'),
    Input('campus_id','data')
)
def update_percentage_Healt(threshold, campus_id):
    """Update the percentage box corresponding to the threshold value that was updated."""
    print("Running 'update_percentage_Health'.") 
    population = campuses[campus_id]['population'] 
    if threshold is not None:
        percentage = int(threshold) * 100 / int(population)
        return f"{round(percentage, 2)}%"
    else:
        return f"0.0%"

           
@dash_app.callback(
    Output("asked_no_solutions_store","data"),
    Output("loading-output", "children"),
    Input("asked_no_solutions", "value"),
    #Input(component_id='asked_no_solutions', component_property='n_clicks'),
    State('campus_id','data')
)
def update_asked_solutions(asked_no_solutions, campus_id):
    print("Running 'update_asked_solutions'.")
    #Improve the efficiencia of calculation calls
    if campus_id is None:
        print ("Default campus")
        campus_id = "campus1"
        return "done",""
    print (campus_id)
    os.system('julia pareto/pareto.jl data/'+ campus_id +'.json ' + str(asked_no_solutions) + ' data/'+ campus_id +'.csv')
    print("From method")    
    return "done",""

##This method has problems when there are different number of categories            
@dash_app.callback(
    Output("bar-chart", "figure"),
    Output({'type': 'allocation', 'index': ALL}, 'children'),
    Output({'type': 'groupsize', 'index': ALL}, 'children'),
    Input("jsoned_solutions", "data"),
    Input("current-solution", "value"),
    State('campus_id','data'),
    State("solutions", "data"),
    
)
def update_displayed_solution(jsoned_solutions, sol_index, campus_id, solutions):
    """Updates the figure and the allocation/group size boxes when current_solution is modified."""
    print("Running 'update_displayed_solution'.")
    k = len (campuses[campus_id]['categories'])
    # If sol_index is None, return None
    if sol_index is None:
        return blank_fig, (None,)*k, (None,)*k
    # If sol_index is not an int, do nothing.
    elif not isinstance(sol_index, int):
        return no_update, [no_update]*k, [no_update]*k
    # Load the solution from dataframe
    row_index = solutions[sol_index-1]
    jsoned_solutions = json.loads(jsoned_solutions)
    specific = jsoned_solutions['data'][row_index]
    specific2 = pd.DataFrame(specific, jsoned_solutions['columns'])
    # Get updated bar chart
    fig = get_fig(specific2[0], campus_id)
    # Get allocation and group sizes
    g_labels = [f'g{i}' for i in range(1,k+1)]
    t_labels = [f't{i}' for i in range(1,k+1)]
    t = list(specific2[0][t_labels])
    g = list(specific2[0][g_labels])
    # Return figure, allocation, and group sizes
    return fig, t, g


@dash_app.callback(
    Output("solutions", "data"),
    Output("threshold_vals", "data"),
    Output("threshold_h_val", "data"),
    Output("solution-num-sentence", "children"),
    Output("current-solution", "value"),
    Output("current-solution", "max"),
    Output("jsoned_solutions", "data"),
    Input({'type': 'threshold', 'index': ALL}, 'value'),
    Input({'type': 'threshold_h'}, 'value'),
    Input("asked_no_solutions_store", "data"),
    State('campus_id', 'data'),
    State("current-solution", "value")
)
def update_solution_set(thresholds, threshold_h, asked_no_solutions, campus_id, current_sol):
    """Updates the set of solutions stored when one of the thresholds changes."""
    print("Running 'update_solution_set'.")
    #if (campus_id.has_changed):
    #    print ("Campus has changed")
    # Check that all thresholds are integers, otherwise do nothing.
    if not all(map(lambda x: isinstance(x, int), thresholds)):
        return (no_update,)*6
    sols, jsoned_solutions = get_solutions(thresholds, threshold_h, campus_id)
    num_sols = len(sols)
    if current_sol is not None and current_sol < num_sols:
        picked_sol = current_sol
    elif num_sols > 0:
        picked_sol = random.randint(1, num_sols)
    else:
        picked_sol = None
    
    if num_sols != 1:
        solutions_sentence = _("There are {} solutions that satisfy the thresholds.").format(num_sols)
    else:
        solutions_sentence = _("There is one solution that satisfies the thresholds.")
    return sols, thresholds, threshold_h, solutions_sentence, picked_sol, num_sols, jsoned_solutions

def get_solutions(thresholds, threshold_h, campus_id):
    if campus_id is not None:
        print ("Reading file", campuses[campus_id]['file'])
        df = pd.read_csv(campuses[campus_id]['file'])
        k = len(campuses[campus_id]['categories'])

        if df.columns.size != 3*k+1:
            raise Exception("Data input has inconsistent number of categories!")

        g_labels = [f'g{i}' for i in range(1,k+1)]
        t_labels = [f't{i}' for i in range(1,k+1)]
        contain_labels = [f'Containment {i}' for i in range(1,k+1)]
        health_label = ['Health']
        obj_labels =  health_label + contain_labels
        col_labels = g_labels + t_labels + obj_labels
        df.columns = col_labels
    """Return list of solutions (=indices of dataframe) that are not filtered out by thresholds."""
    df = df.sort_values(by=['Health'], ignore_index=True)
    contain_mask = (df[contain_labels] <= thresholds[:]).all(axis=1)
    health_mask = (-df[health_label] >= threshold_h).all(axis=1)
    mask = contain_mask & health_mask
    return list(mask[mask].index), df.to_json(orient="split")

@dash_app.callback(
    Output("solutions-row", "children"),
    Input('save-button', 'n_clicks'),
    State('campus_id','data'),
    State("current-solution", "value"),
    State("solutions", "data"),
    State("jsoned_solutions", "data"),
    State("solutions-row", "children")
)
def save_solution(n_clicks, campus_id, sol_index, solutions, jsoned_solutions, saved_solutions):
    """Saves the current figure and the allocations / group sizes when the save button is clicked."""
    print("Running 'save_solution'.")
    # If sol_index is not an int, do nothing.
    if not isinstance(sol_index, int):
        return no_update
    row_index = solutions[sol_index-1]
    jsoned_solutions = json.loads(jsoned_solutions)
    specific = jsoned_solutions['data'][row_index]
    specific2 = pd.DataFrame(specific, jsoned_solutions['columns'])
    k = len(campuses[campus_id]['categories'])
    # Get updated box-graph
    fig = get_fig(specific2[0], campus_id)
    # Get allocation and group sizes
    g_labels = [f'g{i}' for i in range(1,k+1)]
    t_labels = [f't{i}' for i in range(1,k+1)]
    t = list(specific2[0][t_labels])
    g = list(specific2[0][g_labels])
    # Get time at which solution is saved, to use as index
    timestamp = time.time()
    column = dbc.Col([
        dbc.Card([
            dcc.Graph(id={'type': 'saved-graph', 'index': sol_index},
                      figure=fig, config={'staticPlot': True}, className="mb-1"),
            html.Span(_("Allocation: {}.").format(t)),
            html.Span(_("Group sizes: {}.").format(g)),
            # dbc.Button("Delete", id={'type':'delete', 'index': timestamp}),
            ], id={'type': 'saved_solution', 'index': timestamp}, className="p-3 mb-3"),
    ], width=6)
    saved_solutions.append(column)
    # Return solution column
    return saved_solutions