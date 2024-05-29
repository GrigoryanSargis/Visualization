import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample DataFrame for demonstration
df = pd.read_csv('Supermart Grocery Sales - Retail Analytics Dataset.csv')
df = df.drop(columns=['State', 'Order ID'])
df['Order Date'] = pd.to_datetime(df['Order Date'], format="mixed")
df = df.drop_duplicates()

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
                dbc.NavLink("Interactive Graphs", href="/interactive_graphs", active="exact"),
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
    elif pathname == "/interactive_graphs":
        return interactive_graphs_layout()
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
def interactive_graphs_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label('Select Product:', className='text-light'),
                dcc.Dropdown(
                    id='product-dropdown',
                    options=[{'label': prod, 'value': prod} for prod in df['Category'].unique()],
                    value=df['Category'].unique()[0],
                    clearable=False,
                    className='mb-3'
                ),
                html.Label('Select Region:', className='text-light'),
                dcc.Dropdown(
                    id='Region-dropdown',
                    options=[{'label': region, 'value': region} for region in df['Region'].unique()],
                    value=None,
                    clearable=True,
                    className='mb-3'
                ),
                html.Label('Select Year Range:', className='text-light'),
                dcc.RangeSlider(
                    id='year-slider',
                    min=int(df['Order Date'].dt.year.min()),
                    max=int(df['Order Date'].dt.year.max()),
                    value=[int(df['Order Date'].dt.year.min()), int(df['Order Date'].dt.year.max())],
                    marks={str(year): str(year) for year in range(int(df['Order Date'].dt.year.min()), int(df['Order Date'].dt.year.max()) + 1)},
                    step=None,
                    className='mb-3'
                ),
                dbc.Button('Update Graph', id='update-button', color='primary', className='mr-2'),
                dbc.Button('Reset Filters', id='reset-button', color='secondary', className='ml-2')
            ], width=4),

            dbc.Col([
                dcc.Graph(id='sales-graph')
            ], width=8)
        ], className='mb-4'),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-graph', figure=px.bar(df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales', title='Top Selling Categories'))
            ], width=12)
        ]),

        html.Div(id='social-buttons', className='text-center mt-4')
    ])

# Expose the server
server = app.server

