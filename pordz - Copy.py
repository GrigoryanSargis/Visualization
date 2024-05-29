import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample DataFrame for demonstration
df = pd.read_csv('Supermart Grocery Sales - Retail Analytics Dataset.csv')
df = df.drop(columns=['State', 'Order ID'])
df['Order Date'] = pd.to_datetime(df['Order Date'], format="mixed")
df = df.drop_duplicates()
def app():
    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
    app.title = "Supermart Grocery Sales Dashboard"

# Define the sales distribution layout
    sales_distribution_layout = dbc.Container([
        html.H1("Sales Distribution per Region", className="text-light"),
        dcc.Graph(
            id='sales-distribution-graph',
            figure=px.pie(df, values='Sales', names='Region', title='Sales Distribution per Region')
    )
])
if __name__ == "__main__":
    app()


