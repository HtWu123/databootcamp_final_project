import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import geopandas as gpd

# Load the data
clean_data = pd.read_csv('data/clean_data.csv')  # Update this path
with open('data/nyc_boroughs.geojson') as f:
    nyc_boroughs_geojson = gpd.read_file(f)

# Prepare the data
no2_data = clean_data[clean_data['Name'] == 'Nitrogen dioxide (NO2)']
avg_no2_by_borough = no2_data.groupby('Geo Place Name')['Data Value'].mean().reset_index()

# Create the choropleth map
fig = px.choropleth_mapbox(avg_no2_by_borough,
                           geojson=nyc_boroughs_geojson,
                           locations='Geo Place Name',
                           featureidkey='properties.boro_name',
                           color='Data Value',
                           color_continuous_scale='Viridis',
                           range_color=(0, 50),
                           mapbox_style='carto-positron',
                           zoom=9, center={'lat': 40.7, 'lon': -73.9},
                           opacity=0.5,
                           labels={'Data Value': 'Average NO2 Level'},
                           title='Average NO2 Levels by Borough in NYC')
# Set the title
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Average NO2 Levels by Borough in NYC'),
    dcc.Graph(id='no2-choropleth', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
