import dash
from dash import dcc, html, Input, Output, State
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
                dbc.NavLink("Goodbye", href="/goodbye", active="exact"),
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
    elif pathname == "/goodbye":
        return goodbye_page()
    else:
        return welcome_page()

def welcome_page():
    return html.Div(
        [
            html.H1("Welcome to the Supermart Grocery Sales Dashboard"),
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
                    id='region-dropdown',
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

def goodbye_page():
    share_url = "https://github.com/GrigoryanSargis/Visualization"  
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    twitter_url = f"https://twitter.com/intent/tweet?url={share_url}&text=Check out this dashboard!"
    
    social_buttons = html.Div([
        html.P("If you like this dashboard, you can share it!"),
        html.A(html.Button('Share on Facebook', id='facebook-share-button', className='btn btn-primary m-2'), href=facebook_url, target="_blank"),
        html.A(html.Button('Share on Twitter', id='twitter-share-button', className='btn btn-info m-2'), href=twitter_url, target="_blank")
    ])
    gif_url = "https://https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif"  # Replace with your desired GIF URL

    return html.Div(
        [
            html.H1("Goodbye!"),
            html.P("Thank you for visiting the Supermart Grocery Sales."),
            html.Img(src=gif_url, style={'width': '50%'}),
            social_buttons
        ]
    )

# Callback for updating the sales graph
@app.callback(
    Output('sales-graph', 'figure'),
    [
        Input('update-button', 'n_clicks'),
        Input('reset-button', 'n_clicks')
    ],
    [
        State('product-dropdown', 'value'),
        State('region-dropdown', 'value'),
        State('year-slider', 'value')
    ]
)
def update_graph(update_clicks, reset_clicks, selected_product, selected_region, selected_years):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'reset-button':
        return px.bar(df, x='Order Date', y='Sales', title='Sales Over Time', color_discrete_sequence=['red'])

    # Filter dataframe based on user selections
    filtered_df = df.copy()

    if selected_product:
        filtered_df = filtered_df[filtered_df['Category'] == selected_product]

    if selected_region:
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]

    if selected_years:
        filtered_df = filtered_df[
            (filtered_df['Order Date'].dt.year >= selected_years[0]) &
            (filtered_df['Order Date'].dt.year <= selected_years[1])
        ]

    fig = px.bar(filtered_df, x='Order Date', y='Sales', title='Sales Over Time', color_discrete_sequence=['red'])
    return fig

# Expose the server
server = app.server
