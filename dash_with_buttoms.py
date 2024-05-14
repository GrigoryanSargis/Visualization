import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
#dataset
df = pd.read_csv('Supermart Grocery Sales - Retail Analytics Dataset.csv')

df = df.drop(columns=['State'])
df = df.drop(columns=['Order ID'])
df['Order Date'] = pd.to_datetime(df['Order Date'],format="mixed")
df = df.drop_duplicates()

app = dash.Dash(__name__)


fig_sales_over_time = px.sunburst(df, path=['Region', 'City'], values='Profit', color='Profit')

fig_top_selling_categories = px.bar(df.groupby('Category')['Sales'].sum().reset_index(), x='Category', y='Sales')

fig_sales_by_region = px.pie(df.groupby('Region')['Sales'].sum().reset_index(), values='Sales', names='Region')

app.layout = html.Div(children=[
    html.H1(children='Supermart Grocery Sales Dashboard'),
    dcc.Graph(id='sales-graph'),
    html.Br(),
    html.Label('Select Product:'),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': prod, 'value': prod} for prod in df['Category'].unique()],
        value=df['Category'].unique()[0],
        clearable=False
    ),
    html.Br(),
    html.Label('Select Region:'),
    dcc.Dropdown(
        id='Region-dropdown',
        options=[{'label': prod, 'value': prod} for prod in df['Region'].unique()],
        value=None,
        clearable=True
    ),
    html.Br(),
    html.Label('Select Year Range:'),
    dcc.RangeSlider(
        id='year-slider',
        min=df['Order Date'].dt.year.min(),
        max=df['Order Date'].dt.year.max(),
        value=[df['Order Date'].dt.year.min(), df['Order Date'].dt.year.max()],
        marks={str(year): str(year) for year in range(df['Order Date'].dt.year.min(), df['Order Date'].dt.year.max() + 1)},
        step=None
    ),
    html.Button('Update Graph', id='update-button', n_clicks=0),
    html.Button('Reset Filters', id='reset-button', n_clicks=0),
    dcc.Graph(id='sunburst-graph', figure=fig_sales_over_time),
    dcc.Graph(id='bar-graph', figure=fig_top_selling_categories),
    dcc.Graph(id='pie-graph', figure=fig_sales_by_region),
    html.Div(id='social-buttons')
])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('update-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('product-dropdown', 'value'),
     State('year-slider', 'value'),
     State('Region-dropdown', 'value')]
)
def update_graph(update_clicks, reset_clicks, selected_product, selected_year_range, Region):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'update-button':
        if Region is None:
            filtered_df = df[(df['Category'] == selected_product) &
                             (df['Order Date'].dt.year >= selected_year_range[0]) &
                             (df['Order Date'].dt.year <= selected_year_range[1])]
        else:
            filtered_df = df[(df['Category'] == selected_product) &
                             (df['Order Date'].dt.year >= selected_year_range[0]) &
                             (df['Order Date'].dt.year <= selected_year_range[1]) &
                             (df['Region'] == Region)]

        return {
            'data': [{
                'x': filtered_df['Order Date'],
                'y': filtered_df['Sales'],
                'type': 'bar',
                'name': 'Sales'
            }],
            'layout': {
                'title': f'Sales of Product {selected_product}',
                'xaxis': {'title': 'Order Date'},
                'yaxis': {'title': 'Sales'}
            }
        }
    elif button_id == 'reset-button':
        # Reset all filters to default values
        return {
            'data': [],
            'layout': {}
        }
    else:
        # No button click, return empty graph
        return {
            'data': [],
            'layout': {}
        }

@app.callback(
    Output('social-buttons', 'children'),
    [Input('sales-graph', 'figure')]
)
def add_social_buttons(figure):
    share_url = "https://github.com/GrigoryanSargis/Visualization"  # Replace with your dashboard URL
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    twitter_url = f"https://twitter.com/intent/tweet?url={share_url}&text=Check out this notebook!"

    return html.Div([
        html.A(html.Button('Share on Facebook', id='facebook-share-button'), href=facebook_url, target="_blank"),
        html.A(html.Button('Share on Twitter', id='twitter-share-button'), href=twitter_url, target="_blank")
    ])



if __name__ == '__main__':
    app.run_server(debug=True)
