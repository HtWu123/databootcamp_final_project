import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# 假设我们已经有了一个名为clean_data的清洗过的DataFrame
clean_data = pd.read_csv('data/clean_data.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('污染物数据分析'),
    dcc.Dropdown(
        id='pollutant-selector',
        options=[
            {'label': '二氧化氮 (NO2)', 'value': 'NO2'},
            {'label': '细颗粒物 (PM2.5)', 'value': 'PM2.5'},
            {'label': '臭氧 (O3)', 'value': 'O3'}
        ],
        value='NO2'  # 默认值
    ),
    dcc.Graph(id='pollution-graph')
])

@app.callback(
    Output('pollution-graph', 'figure'),
    Input('pollutant-selector', 'value')
)
def update_graph(selected_pollutant):
    filtered_data = clean_data[clean_data['Name'] == selected_pollutant]
    fig = px.line(filtered_data, x='Start_Date', y='Data Value', title=f'{selected_pollutant} Levels Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
