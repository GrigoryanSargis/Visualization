import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the sidebar
sidebar = dbc.Col(
    [
        html.H2("Navigation", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Welcome", href="/", active="exact"),
                dbc.NavLink("Correlation Analysis", href="/correlation-analysis", active="exact"),
                dbc.NavLink("Grades Distribution", href="/grades-distribution", active="exact"),
                dbc.NavLink("Pair Plots", href="/pair-plots", active="exact"),
                dbc.NavLink("Ages and Groups Analysis", href="/ages-groups-analysis", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    md=2,
)

# Define the content for each page
content = dbc.Col(
    id="page-content",
    md=10
)

# Define the layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                sidebar,
                content
            ],
        ),
    ],
    fluid=True,
)

# Define the callbacks to update the page content based on the URL
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/correlation-analysis":
        return correlation_page()
    elif pathname == "/grades-distribution":
        return grades_page()
    elif pathname == "/pair-plots":
        return pair_plots_page()
    elif pathname == "/ages-groups-analysis":
        return ages_groups_page()
    else:
        return welcome_page()

def welcome_page():
    return html.Div(
        [
            html.H1("Welcome to the Student Performance Dashboard"),
            html.P("""
            This dashboard provides an analysis of student performance data.
            Use the navigation sidebar to explore different aspects of the data.
            """),
            html.H3("Data Overview"),
            html.Ul(
                [
                    html.Li("Sales: Total sales across different regions"),
                    html.Li("Profit: Profit data for different items"),
                    html.Li("Region: Sales data categorized by region"),
                    html.Li("Category: Different product categories"),
                    html.Li("Date: Sales data across different dates"),
                ]
            ),
            html.P('For more details, you can view the data [here](https://www.kaggle.com/mohamedharris/supermart-grocery-sales-retail-analytics-dataset).')
        ]
    )

def correlation_page():
    return html.Div(
        [
            html.H1("Correlation Analysis"),
            html.P("""
            In this section, we analyze the correlations between different variables in the dataset.
            Correlation analysis helps in understanding the relationships between different factors,
            such as how sales and profit are related across different regions and categories.
            """),
            html.P("""
            Understanding these relationships can help in making data-driven decisions, such as
            identifying key drivers of profit and optimizing strategies accordingly.
            """)
            # Add more detailed correlation analysis content here
        ]
    )

def grades_page():
    return html.Div(
        [
            html.H1("Correlation Analysis"),
            html.P("""
            In this section, we analyze the correlations between different variables in the dataset.
            Correlation analysis helps in understanding the relationships between different factors,
            such as how sales and profit are related across different regions and categories.
            """),
            html.P("""
            Understanding these relationships can help in making data-driven decisions, such as
            identifying key drivers of profit and optimizing strategies accordingly.
            """)
            # Add more detailed correlation analysis content here
        ]
    )

def pair_plots_page():
    return html.Div(
        [
            html.H1("Correlation Analysis"),
            html.P("""
            In this section, we analyze the correlations between different variables in the dataset.
            Correlation analysis helps in understanding the relationships between different factors,
            such as how sales and profit are related across different regions and categories.
            """),
            html.P("""
            Understanding these relationships can help in making data-driven decisions, such as
            identifying key drivers of profit and optimizing strategies accordingly.
            """)
            # Add more detailed correlation analysis content here
        ]
    )

def ages_groups_page():
    return html.Div(
        [
            html.H1("Correlation Analysis"),
            html.P("""
            In this section, we analyze the correlations between different variables in the dataset.
            Correlation analysis helps in understanding the relationships between different factors,
            such as how sales and profit are related across different regions and categories.
            """),
            html.P("""
            Understanding these relationships can help in making data-driven decisions, such as
            identifying key drivers of profit and optimizing strategies accordingly.
            """)
            # Add more detailed correlation analysis content here
        ]
    )

# Ensure the server can be accessed externally if needed
server = app.server
