import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px  # 导入plotly.express来创建图表

# 加载数据
clean_data = pd.read_csv('data/clean_data.csv')  # 确保路径正确
nyc_boroughs = gpd.read_file('data/nyc_boroughs.geojson')
uhf42_geo_path = 'data/UHF42.geo.json'
uhf42_gdf = gpd.read_file(uhf42_geo_path)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pollutant Data Visualization"),
    html.Div([
        html.H3("Select Pollutant:"),
        dcc.Dropdown(
            id='pollutant-dropdown',
            options=[
                {'label': 'Nitrogen dioxide (NO2)', 'value': 'Nitrogen dioxide (NO2)'},
                {'label': 'Fine particles (PM 2.5)', 'value': 'Fine particles (PM 2.5)'},
                {'label': 'Ozone (O3)', 'value': 'Ozone (O3)'}
            ],
            value='Nitrogen dioxide (NO2)'
        )
    ]),
    html.Div([
        html.H3("Select Visualization Type:"),
        dcc.RadioItems(
            id='visualization-type',
            options=[
                {'label': 'Average Levels by Borough', 'value': 'borough'},
                {'label': 'Average Levels by UHF42 Area', 'value': 'uhf42'},
                {'label': 'Average Levels by Season and Borough', 'value': 'season'},
                {'label': 'Average Levels by Year', 'value': 'year'}
            ],
            value='borough'
        )
    ]),
    html.Div(id='output-graph')
])

@app.callback(
    Output('output-graph', 'children'),
    [Input('pollutant-dropdown', 'value'), Input('visualization-type', 'value')]
)
def update_graph(pollutant_name, visualization_type):
    # Convert pollutant name to match the column names in your dataset
    # Assuming the pollutants are column names in your dataset
    pollutant_col = {
        'NO2': 'Nitrogen dioxide (NO2)',  # The key here should be the 'value' from the dropdown
        'PM2.5': 'Fine particles (PM2.5)',
        'O3': 'Ozone (O3)'
    }.get(pollutant_name, 'NO2')

    if visualization_type == 'borough':
        # Assuming 'Geo Place Name' matches the 'name' in nyc_boroughs and you want to visualize 'Data Value'
        data = clean_data[clean_data['Name'] == pollutant_col]
        avg_pollutant_by_borough = data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
        fig = px.choropleth(
            avg_pollutant_by_borough,
            geojson=nyc_boroughs.geometry.__geo_interface__,
            locations='Geo Place Name',
            color='Data Value',
            color_continuous_scale="Viridis",
            featureidkey="properties.name"
        )
        fig.update_geos(fitbounds="locations", visible=False)

    elif visualization_type == 'uhf42':
        # Similarly, for UHF42 areas
        data = clean_data[clean_data['Name'] == pollutant_col]
        avg_pollutant_by_uhf42 = data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
        fig = px.choropleth(
            avg_pollutant_by_uhf42,
            geojson=uhf42_gdf.geometry.__geo_interface__,
            locations='Geo Place Name',
            color='Data Value',
            color_continuous_scale="Viridis",
            featureidkey="properties.GEONAME"
        )
        fig.update_geos(fitbounds="locations", visible=False)

    elif visualization_type == 'season':
        # Assuming there is a 'Season' column and 'Data Value' to visualize
        data = clean_data[(clean_data['Name'] == pollutant_col) & (clean_data['Geo Type Name'] == 'Borough')]
        fig = px.bar(
            data,
            x='Geo Place Name',
            y='Data Value',
            color='Season',
            barmode='group'
        )

    elif visualization_type == 'year':
        # Assuming there is a 'Year' column
        data = clean_data[clean_data['Name'] == pollutant_col]
        avg_pollutant_by_year = data.groupby('Year')['Data Value'].mean().reset_index()
        fig = px.line(
            avg_pollutant_by_year,
            x='Year',
            y='Data Value',
            markers=True
        )

    # Update layout if necessary
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar={
            'title':'Average Level'
        }
    )

    return dcc.Graph(figure=fig)  # Return a Dash Graph component


if __name__ == '__main__':
    app.run_server(debug=True)
