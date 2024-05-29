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
                dbc.NavLink("Profit Distribution by Region and City", href="/sunburst", active="exact"),
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
    if pathname == "/sunburst":
        return sunburst_layout()
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

def sunburst_layout():
    return dbc.Container([
        html.H1("Profit Distribution by Region and City", className="text-light"),
        dcc.Graph(
            id='sunburst-graph-page',
            figure=px.sunburst(df, path=['Region', 'City'], values='Profit', color='Profit', title='Profit Distribution by Region and City')
        )
    ])


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

