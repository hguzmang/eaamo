import dash_daq as daq
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from textwrap import dedent

from preprocess import blank_fig, campuses, population, locale, _


def get_layout(number_categories, no_solutions, budget, buckets, table_d, table_pi, table_p, categories):
    ### Start building tables

    # Build the thresholds input tables
    table_header = [html.Thead(html.Tr([html.Th(None),
                    html.Th(_("Size")),
                    html.Th(_("Threshold")),
                    html.Th(_("Percent"))]))]
    rows = [html.Tr([html.Td('', id={'type': 'categories_name', 'index': i}),
        html.Td('', id={'type': 'categories_size', 'index': i}),
        html.Td(daq.NumericInput(id={'type': 'threshold', 'index': i},
                                min=0, max=0,
                                value=0,
                                size=80)),
        html.Td("0%", id={'type': 'percent', 'index': i})])
        for i in range(number_categories)]
    containment_body = [html.Tbody(rows)]
    containment_table = dbc.Table(table_header + containment_body, bordered=False, className="text-right table-borderless table-sm m-0")
    health_body = [html.Tr([html.Td(population['name'], id={'type':'population_name'}),
        html.Td(population['size'], id={'type':'population_size'}),
        html.Td(daq.NumericInput(id={'type': 'threshold_h'},
                                    min=0, max=population['size'],
                                    value=0, size=80)),
        html.Td("0%", id={'type': 'percent_h'}),
    ])]
    health_table = dbc.Table(table_header + health_body, bordered=False, className="text-right table-borderless table-sm m-0")

    # Build the solution output table
    table_header = [html.Thead(html.Tr([html.Th(None),
                    html.Th(_("Allocated Tests")),
                    html.Th(_("Group sizes"))]))]
    rows=[
        html.Tr([html.Td('',id={'type':'sol_name','index':i}) ,
                html.Td(0, id={'type': 'allocation', 'index': i}) ,
            html.Td(0, id={'type': 'groupsize', 'index': i})])
        for i in range(number_categories)]
    solutions_body = [html.Tbody(rows)]

    solutions_table = dbc.Table(table_header + solutions_body, bordered=False, className="text-right table-borderless table-sm m-0")


    ### Start building the layout

    ## Define the navbar
    dropdown_children = [
        dbc.DropdownMenuItem(campuses["campus" + str(i+1)]['label'], href="/" + "campus" + str(i+1))
        for i in range(len(campuses))
    ]
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(_("Instructions"), href="#instructions", external_link=True)),
            dbc.NavItem(dbc.NavLink(_("Model details"), href="#modeldetails", external_link=True)),
           
            dbc.DropdownMenu(
                children= dropdown_children,
                id="site-selector",
                nav=True,
                in_navbar=True,
                label=_("Select Campus")
            ),
        ],
        brand="Test & Contain. COVID-19 Optimal tests allocation",
        brand_href="#",
        color="#800080",
        # light=True,
        dark=True
        )

    bucket_headers = "___H"
    for i in range(len(categories)):
        bucket_headers += "___" +f"C{i+1}"
    bucket_headers += "__"

    ## Define the introductory header div
    intro_title = _("Test & Contain  ")
    intro_lead = _("A demonstration of the Test & Contain tool for selecting an optimal testing strategy.")
    intro_text = _("This web app assists you in finding a test allocation that best suits your priorities. We have preloaded data matching some university models. The university is able to perform group tests, where groups can be of size 1 to 10. You can access instructions or view our full parameter settings from the menu above.")
    
    spinner = dbc.Spinner(html.Div(id="loading-output"))

    asked_no_sols_card = dbc.Card(
        dbc.Row([
            
            dbc.Col([
                html.A((" More adjustments"), href='http://104.215.96.205:8050/')
            ], width=3),
            dbc.Col([
                html.H5(_("Please select an approximated number of solutions to manage: ")),
            ], width=15),
            dbc.Col([
                html.Td(daq.NumericInput(id='asked_no_solutions',
                                min=0, max=100,
                                value=10,
                                size=80)),
            ], width=15),
            dbc.Col([
                dbc.Button(_("Calculate"), id='asked_no_solutions_button', color="primary"),
            ], width=15)
        ]), body=True, className="pt-1 pb-1")

    header = html.Div([
        html.H1(intro_title,style={"display":"inline"}),
        html.H1(id='location-label',style={"display":"inline"}),
        html.H4(" " + str(no_solutions) + " solutions were analyzed",style={"display":"inline"}),
        html.H4(" with a budget of " + str(budget) + " tests.",style={"display":"inline"}),
        html.Hr(),
        html.P(intro_lead, className="lead"),
        html.Hr(),
        html.P(intro_text),
        # dbc.Button(_("Instructions"), color='primary', href="#instructions", external_link=True, className="mr-2"),
        # dbc.Button(_("Model details"), color='secondary', outline=True, href="#modeldetails", external_link=True),
    ], className="bg-light rounded p-3 mb-3")

    ## Define the main div
    # Containment thresholds selector
    containment_title = _("Limit the number of unnecessary self-isolations in each category")
    containment_lead = _("Only solutions whose containment objectives lie below the thresholds are retained")
    containment_thresholds = dbc.Card([
        html.H5(containment_title),
        html.P(containment_lead, className="mb-0"),
        containment_table,
    ], body=True, className="pt-2 pb-1 mb-3")

    # Infections threshold selector
    infection_title = _("Guarantee a minimum number of prevented critical infections")
    infection_lead = _("Only solutions whose health objective lies above the threshold are retained.")
    infections_threshold = dbc.Card([
        html.H5(infection_title),
        html.P(infection_lead, className="mb-0"),
        health_table,
    ], body=True, className="pt-2 pb-1 mb-3")

    # Solution selector
    select_solution = dbc.Card(
        dbc.Row([
            dbc.Col([
                html.H5(_("Select a solution")),
                html.P(_("There are X solutions that satisfy the thresholds."), id="solution-num-sentence", className="mb-0"),
                html.P(_("Choose which one to chart using the input box.")),
            ], width=8),
            dbc.Col([
                daq.NumericInput(id="current-solution", min=1, label="Current solution", size=80, className="pt-3", labelPosition="bottom"),
            ])
        ]), body=True, className="pt-2 pb-1")

    # Bar charts
    bar_charts = dbc.Card([
        html.Div(dcc.Graph(id='bar-chart', figure=blank_fig, config={'staticPlot': True})),
    ], className="p-3 mb-3 bg-light", style={'height': '330px'})

    # Solution details
    solution_details = dbc.Card([html.H5(_("Solution details")), solutions_table], body=True, className="pt-2 pb-1 mb-3")

    # Save card
    save_card = dbc.Card([
        html.P(_("In order to save this solution for future reference, click the save button.")),
        dbc.Button(_("Save"), id='save-button', color="primary"),
        ], body=True)

    main_title = _("Find the right solution")
    main_lead = _("Adjust the thresholds (cut-offs) to narrow down the set of solutions.")

    #def construct_main_div():
    #    return 
    main_div =  html.Div([
            dbc.Row([
                dbc.Col([html.H2(main_title), html.P(main_lead),
                        containment_thresholds, infections_threshold, select_solution]),
                dbc.Col([bar_charts, solution_details, save_card], width=5)
            ], id="main_div")
        ])


    ## Additional sections

    # Saved solutions
    saved_title = _("Saved solutions")
    saved_lead = _("Click on the 'Save' button above to add the current solution to the list.")
    saved_solutions = html.Div([
        html.Hr(), html.H2(saved_title), html.P(saved_lead), dbc.Row([], id='solutions-row'), html.Hr(),
        ], className="my-3")

    # Load instructions text
    with open(f'locales/{locale}/instructions.md', encoding='utf8') as file:
        instructions_text = dedent(file.read())

    # Load model details text
    with open(f'locales/{locale}/modeldetails.md', encoding='utf8') as file:
        model_text = dedent(file.read())

    # Div containing instructions
    guide = html.Div(
        dbc.Row(dbc.Col(dcc.Markdown(instructions_text),
                        width=12, className="text-justify"), justify="center",
                        className="border rounded m-0 p-2"),
        className="mb-3", id="instructions")

    # Div containing model details
    details = html.Div(
        dbc.Row(dbc.Col(dcc.Markdown(model_text, dangerously_allow_html=True),
                            width=12, className="text-justify"), justify="center",
                            className="border rounded m-0 p-2"),
        className="mb-3", id="modeldetails")

    table_header_d = [html.Thead(html.Tr(
        [html.Th("Conectivity")] +
        [
        html.Th(categories[i]["name"])
        for i in range(number_categories)
        ]
    ))]
    rows_d=[
        html.Tr( [html.Td("A " + categories[i]["name"])] +
            [html.Td(str(round(table_d[i][j],0)))
            for j in range(number_categories)
            ])
        for i in range(number_categories)]
    solutions_body_d = [html.Tbody(rows_d)]
    

    solutions_table_d = dbc.Table(table_header_d+solutions_body_d, bordered=True, className="table table-success",
    style={"text-align": "center", "width" :"90%"})

    table_header_pi = [html.Thead(html.Tr(
        [html.Th("Co-infection")] +
        [
        html.Th(categories[i]["name"])
        for i in range(number_categories)
        ]
    ))]
    rows_pi=[
            html.Tr( [html.Td("A " + categories[i]["name"])] +
                [html.Td(str(round(table_pi[i][j],2)*100) + "%")
                for j in range(number_categories)
                ])
            for i in range(number_categories)]
    solutions_body_pi = [html.Tbody(rows_pi)]

    solutions_table_pi = dbc.Table(table_header_pi + solutions_body_pi, bordered=True, className="table table-primary",
    style={"text-align": "center", "width" :"90%"})

    table_header_p = [html.Thead(html.Tr(
        [html.Th("Infection")] +
        [
        html.Th(categories[i]["name"])
        for i in range(number_categories)
        ]
    ))]
    rows_p=[
                html.Tr( [html.Td()] +
                    [html.Td(str(round(table_p[i],2)*100) + "%")
                    for i in range(number_categories)
                    ])]
    solutions_body_p = [html.Tbody(rows_p)]
    solutions_table_p = dbc.Table(table_header_p + solutions_body_p, bordered=True, className="table table-info",
    style={"text-align": "center", "width" :"90%", "align": "center"})
    footer = html.Div([
        html.A(_("© Test and Contain 2021."), href='https://www.testandcontain.com'),
        html.P(),
        html.A(("Download the code"), href='assets/eaamo-demo.zip')
    ], className="text-left p-3")
    ## Start the DOM layout
    layout = dbc.Container([
        navbar,
        asked_no_sols_card,
        spinner,
        header,        
        main_div,
        saved_solutions,
        guide,
        details,

        solutions_table_d,
        solutions_table_pi,
        solutions_table_p,
        footer,
        # hidden elements to store data in browser
        dcc.Store(id="solutions"),
        dcc.Store(id="threshold_vals"),
        dcc.Store(id="threshold_h_val"),
        dcc.Store(id="campus_id"),
        dcc.Store(id="asked_no_solutions_store"),
        dcc.Store(id="jsoned_solutions")
    ],id="my-layout")
    
    return layout
