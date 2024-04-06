import pandas as pd
import numpy as np
import geopandas as gpd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


# 加载数据
clean_data = pd.read_csv('data/clean_data.csv')
nyc_boroughs = gpd.read_file('data/nyc_boroughs.geojson')
uhf42_gdf = gpd.read_file('data/UHF42.geo.json')


def plot_average_levels(pollutant_name, legend_label):
    data = clean_data
    column_name = 'Data Value'
    pollutant_data = data[data['Name'] == pollutant_name]
    avg_pollutant_by_name = pollutant_data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
    merged_data = nyc_boroughs.merge(avg_pollutant_by_name, how='left', left_on='name', right_on='Geo Place Name')
    fig = px.choropleth_mapbox(merged_data, geojson=merged_data.geometry, locations=merged_data.index,
                               color=column_name,
                               color_continuous_scale="Viridis", range_color=(merged_data['Data Value'].min(), merged_data['Data Value'].max()),
                               mapbox_style="carto-positron", zoom=9, center={"lat": 40.7128, "lon": -74.0059},
                               opacity=0.5, labels={'Data Value': legend_label},
                               hover_name='name')

    return fig


def plot_average_levels_by_uhf42(pollutant_name, legend_label):
    data = clean_data[clean_data['Name'] == pollutant_name]
    avg_pollutant_by_uhf42 = data.groupby('Geo Place Name')['Data Value'].mean().reset_index()
    merged_data = uhf42_gdf.merge(avg_pollutant_by_uhf42, how='left', left_on='GEONAME', right_on='Geo Place Name')
    fig = px.choropleth_mapbox(merged_data, geojson=merged_data.geometry, locations=merged_data.index, color='Data Value',
                               color_continuous_scale="Viridis", range_color=(merged_data['Data Value'].min(), merged_data['Data Value'].max()),
                               mapbox_style="carto-positron", zoom=9, center={"lat": 40.7128, "lon": -74.0059},
                               opacity=0.5, labels={'Data Value': legend_label}, 
                               hover_name='GEONAME')  
    return fig


def plot_average_levels_by_season(pollutant_name, ylabel):
    data = clean_data[clean_data['Name'] == pollutant_name]
    data = data[data['Geo Type Name'] == 'Borough']
    avg_pollutant_by_season_borough = data.groupby(['Season', 'Geo Place Name'])['Data Value'].mean().reset_index()
    borough_order = avg_pollutant_by_season_borough.groupby('Geo Place Name')['Data Value'].mean().sort_values(ascending=False).index
    fig = px.bar(avg_pollutant_by_season_borough, x='Geo Place Name', y='Data Value', color='Season', barmode='group',
                 category_orders={'Geo Place Name': borough_order})
    fig.update_layout(
        title='Average {} Levels by Season and Borough in NYC'.format(pollutant_name),
        xaxis_title='Borough',
        yaxis_title=ylabel,
        legend_title_text='Season',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_average_levels_by_year(pollutant_name, ylabel):
    data = clean_data[clean_data['Name'] == pollutant_name]
    avg_pollutant_by_year = data.groupby('Year')['Data Value'].mean().reset_index()
    fig = px.bar(avg_pollutant_by_year, x='Year', y='Data Value')
    fig.update_layout(
        title='Average {} Levels by Year in NYC'.format(pollutant_name),
        xaxis_title='Year',
        yaxis_title=ylabel
    )
    return fig

def plot_average_levels_by_year_borough(pollutant_name, ylabel):
    data = clean_data[clean_data['Name'] == pollutant_name]
    data = data[data['Geo Type Name'] == 'Borough']
    avg_pollutant_by_year_borough = data.groupby(['Year', 'Geo Place Name'])['Data Value'].mean().reset_index()
    borough_order = avg_pollutant_by_year_borough.groupby('Geo Place Name')['Data Value'].mean().sort_values(ascending=False).index
    fig = px.line(avg_pollutant_by_year_borough, x='Year', y='Data Value', color='Geo Place Name', 
                  category_orders={'Geo Place Name': borough_order}, markers=True)
    fig.update_layout(
        title='Average {} Levels by Year and Borough in NYC'.format(pollutant_name),
        xaxis_title='Year',
        yaxis_title=ylabel,
        legend_title_text='Borough',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig





function_dict = {
    'Relevant Factor By Year': {
        'Asthma emergency department visits due to PM2.5': plot_average_levels_by_year,
        'Deaths due to PM2.5': plot_average_levels_by_year,
        'Cardiovascular hospitalizations due to PM2.5 (age 40+)': plot_average_levels_by_year,
        'Respiratory hospitalizations due to PM2.5 (age 20+)': plot_average_levels_by_year,
        'Boiler Emissions- Total PM2.5 Emissions': plot_average_levels_by_year
    },
    'By Season': {
        'Nitrogen dioxide (NO2)': plot_average_levels_by_season,
        'Fine particles (PM 2.5)': plot_average_levels_by_season,
        'Ozone (O3)': plot_average_levels_by_season
    },
    'By Borough': {
        'Nitrogen dioxide (NO2)': plot_average_levels,
        'Fine particles (PM 2.5)': plot_average_levels,
        'Ozone (O3)': plot_average_levels
    },
    'By Borough By Year': {
        'Nitrogen dioxide (NO2)': plot_average_levels_by_year_borough,
        'Fine particles (PM 2.5)': plot_average_levels_by_year_borough,
        'Ozone (O3)': plot_average_levels_by_year_borough
    },
    'By UHF42': {
        'Nitrogen dioxide (NO2)': plot_average_levels_by_uhf42,
        'Fine particles (PM 2.5)': plot_average_levels_by_uhf42,
        'Ozone (O3)': plot_average_levels_by_uhf42
    }
}
y_measure_info_dic = {
        'Asthma emergency department visits due to PM2.5': 'Average Asthma emergency department visits per 10,000 people',
        'Deaths due to PM2.5': 'Average Deaths per 10,000 people',
        'Cardiovascular hospitalizations due to PM2.5 (age 40+)': 'Average Cardiovascular hospitalizations per 10,000 people',
        'Respiratory hospitalizations due to PM2.5 (age 20+)': 'Average Respiratory hospitalizations per 10,000 people',
        'Boiler Emissions- Total PM2.5 Emissions': 'Average PM2.5 Emissions (tons)',
        'Nitrogen dioxide (NO2)': 'Average NO2 Level(ppb)',
        'Fine particles (PM 2.5)': 'Average PM2.5 Level(ug/m3)',
        'Ozone (O3)': 'Average O3 Level(ppb)'
    }


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='NYC Air Pollution Visualization'),
    html.Div(children='''
        Select the chart category and content:
    '''),
    dcc.Dropdown(
        id='chart-category',
        options=[{'label': category, 'value': category} for category in function_dict.keys()],
        value='Relevant Factor By Year'
    ),
    dcc.Dropdown(
        id='chart-content',
        options=[],
        value=None
    ),
    dcc.Graph(id='chart')
])

@app.callback(
    Output('chart-content', 'options'),
    [Input('chart-category', 'value')]
)
def update_content_options(selected_category):
    return [{'label': content, 'value': content} for content in function_dict[selected_category].keys()]

@app.callback(
    Output('chart', 'figure'),
    [Input('chart-category', 'value'), Input('chart-content', 'value')]
)
def update_chart(selected_category, selected_content):
    if selected_content is None:
        return {}
    elif selected_category not in function_dict:
        return {}
    elif selected_content not in function_dict[selected_category]:
        return {}
    else:
        plot_function = function_dict[selected_category][selected_content]
        if selected_category == 'Relevant Factor By Year':
            fig = plot_function(selected_content, y_measure_info_dic[selected_content])
        elif selected_category == 'By Season':
            fig = plot_function(selected_content, y_measure_info_dic[selected_content])
        elif selected_category == 'By Borough':
            fig = plot_function(selected_content, y_measure_info_dic[selected_content])
        elif selected_category == 'By Borough By Year':
            fig = plot_function(selected_content, y_measure_info_dic[selected_content])
        elif selected_category == 'By UHF42':
            fig = plot_function(selected_content, y_measure_info_dic[selected_content])
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)