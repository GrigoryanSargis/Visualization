import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
    dcc.Graph(figure=fig_sales_over_time),
    dcc.Graph(figure=fig_top_selling_categories),
    dcc.Graph(figure=fig_sales_by_region)

])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('product-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('Region-dropdown', 'value')]
)
def update_graph(selected_product, selected_year_range, Region):
    if Region == None:
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


if __name__ == '__main__':
    app.run_server(debug=True)
