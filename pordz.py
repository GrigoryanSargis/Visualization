import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample DataFrame for demonstration
data = {
    'Region': ['East', 'West', 'South', 'North'],
    'Sales': [2345, 5678, 1234, 4321]
}
df = pd.DataFrame(data)

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
                dbc.NavLink("Sales Distribution", href="/sales-distribution", active="exact"),
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
        dcc.Location(id='url', refresh=False),
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
    elif pathname == "/sales-distribution":
        return sales_distribution_layout()
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
            html.P([
                "For more details, you can view the data ",
                html.A("here", href="https://www.kaggle.com/mohamedharris/supermart-grocery-sales-retail-analytics-dataset", target="_blank"),
                "."
            ])
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

def sales_distribution_layout():
    return dbc.Container([
        html.H1("Sales Distribution By Region"),
        dcc.Graph(
            id='sales-distribution-graph',
            figure=px.pie(df, values='Sales', names='Region', title='Sales Distribution By Region')
        )
    ])

# Expose the server
server = app.server

